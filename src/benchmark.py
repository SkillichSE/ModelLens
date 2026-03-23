import os, re, json, time, subprocess, argparse, random
from datetime import datetime
from pathlib import Path
import requests
from config import MODELS, TESTS

GROQ_API       = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_API = "https://openrouter.ai/api/v1/chat/completions"
CEREBRAS_API   = "https://api.cerebras.ai/v1/chat/completions"
TOGETHER_API   = "https://api.together.xyz/v1/chat/completions"

REQUEST_DELAY = {"groq": 2, "openrouter": 3, "cerebras": 1, "together": 2}

TIMEOUT_BY_PROVIDER = {
    "groq":       20,
    "openrouter": 25,
    "cerebras":   15,
    "together":   25,
}

_OR_ROTATE_STATUSES = {429, 402}
_THINK_RE = re.compile(r"<think>[\s\S]*?</think>", re.IGNORECASE)

def strip_thinking(text):
    if not text:
        return text
    cleaned = _THINK_RE.sub("", text).strip()
    return cleaned if cleaned else text
def size_category(size_str):
    s = size_str.upper().replace(" ", "")
    if s in ("N/A", "UNKNOWN", ""):
        return "unknown"
    moe = re.search(r"(\d+(?:\.\d+)?)B\s*[Xx]\s*(\d+)", s)
    if moe:
        return _bucket(float(moe.group(1)))
    plain = re.search(r"(\d+(?:\.\d+)?)B", s)
    if plain:
        return _bucket(float(plain.group(1)))
    return "unknown"

def _bucket(b):
    if b <= 10:  return "small"
    if b <= 50:  return "medium"
    return "large"
def _load_openrouter_keys():
    keys = []
    i = 1
    while True:
        k = os.getenv(f"OPENROUTER_API_KEY_{i}", "").strip()
        if not k:
            break
        keys.append(k)
        i += 1
    plain = os.getenv("OPENROUTER_API_KEY", "").strip()
    if plain and plain not in keys:
        keys.append(plain)
    return keys

def eval_reasoning_smart(test_name, response):
    """
    Multi-signal reasoning evaluator.
    Accepts correct answers expressed in many natural ways,
    not just exact keyword match.
    """
    if not response:
        return {"correct": False, "score": 0, "answer_given": ""}

    text = response.strip()
    low  = text.lower()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    tail  = lines[-1].lower() if lines else low

    correct = False

    if test_name == "syllogism":
        correct = bool(re.search(r'\byes\b', tail) or re.search(r'\byes\b', low[:40]))

    elif test_name == "speed_math":
        correct = bool(
            re.search(r'\bsame\b', tail) or
            re.search(r'\bequal\b', tail) or
            re.search(r'\bneither\b', tail) or
            re.search(r'\bboth\b.*\b60\b', low) or
            re.search(r'\b60\s*km', low)
        )

    elif test_name == "river_crossing":
        correct = bool(re.search(r'\bchicken\b', tail) or re.search(r'\bchicken\b', low[:60]))

    elif test_name == "coin_flip":
        correct = bool(
            re.search(r'1\s*/\s*2', tail) or
            re.search(r'\b0\.5\b', tail) or
            re.search(r'50\s*%', tail) or
            re.search(r'\bhalf\b', tail) or
            re.search(r'1\s+in\s+2', tail)
        )

    elif test_name == "counting":
        correct = bool(re.search(r'\b11\b', tail) or re.search(r'\beleven\b', tail))

    return {
        "correct":      correct,
        "score":        100 if correct else 0,
        "answer_given": text[:120],
    }

def eval_code_smart(test_name, response, fn_name):
    """Execute the function against test cases. Strips markdown and thinking."""
    cfg = TESTS["code"][test_name]
    if not response:
        return {"pass_rate": 0.0, "passed": 0, "total": len(cfg["expected"]),
                "error": "empty response"}
    code_match = re.search(r"```(?:python)?\s*\n([\s\S]+?)```", response)
    code = code_match.group(1).strip() if code_match else response.strip()
    lines, code_lines, found_def = code.splitlines(), [], False
    for line in lines:
        if line.strip().startswith("def ") or found_def:
            found_def = True
            code_lines.append(line)
    if code_lines:
        code = "\n".join(code_lines)

    results = []
    for inp, expected in zip(cfg["test_input"], cfg["expected"]):
        try:
            proc = subprocess.run(
                ["python3", "-c", f"{code}\nprint(repr({fn_name}({repr(inp)})))"],
                capture_output=True, text=True, timeout=5)
            if proc.returncode == 0:
                output = proc.stdout.strip()
                results.append({"input": repr(inp), "expected": repr(expected),
                                "got": output, "passed": output == repr(expected)})
            else:
                err = proc.stderr.strip()[:120]
                results.append({"input": repr(inp), "expected": repr(expected),
                                "got": err, "passed": False})
        except subprocess.TimeoutExpired:
            results.append({"input": repr(inp), "expected": repr(expected),
                            "got": "timeout", "passed": False})
        except Exception as e:
            results.append({"input": repr(inp), "expected": repr(expected),
                            "got": str(e)[:80], "passed": False})

    passed = sum(1 for r in results if r["passed"])
    return {
        "pass_rate": round(passed / len(results), 2),
        "passed":    passed,
        "total":     len(results),
        "details":   results,
    }

def eval_instruction_smart(test_name, response):
    if not response:
        return {"score": 0, "reason": "empty response"}
    cfg = TESTS["instruction"][test_name]

    if cfg["check"] == "json_keys":
        m = re.search(r'\{[\s\S]*\}', response)
        if not m:
            return {"score": 0, "reason": "no JSON found"}
        try:
            obj = json.loads(m.group())
            missing = [k for k in cfg["required_keys"] if k not in obj]
            return {"score": 50 if missing else 100,
                    "reason": f"missing: {missing}" if missing else "ok"}
        except json.JSONDecodeError as e:
            return {"score": 0, "reason": f"invalid JSON: {str(e)[:60]}"}

    if cfg["check"] == "numbered_list":
        lines = [l.strip() for l in response.strip().split('\n') if l.strip()]
        numbered = [l for l in lines if re.match(r'^\d+[\.\)]\s+\S', l)]
        score = 100 if len(numbered) == cfg["count"] else \
                75  if abs(len(numbered) - cfg["count"]) == 1 else \
                50  if numbered else 0
        return {"score": score, "found": len(numbered), "expected": cfg["count"]}

    if cfg["check"] == "sentence_count":
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', response.strip()) if s.strip()]
        diff = abs(len(sentences) - cfg["count"])
        score = 100 if diff == 0 else 75 if diff == 1 else 50 if diff == 2 else 0
        return {"score": score, "found": len(sentences), "expected": cfg["count"]}

    return {"score": 0, "reason": "unknown check type"}

def eval_translation_smart(test_name, response):
    if not response:
        return {"score": 0, "reason": "empty response"}
    cfg = TESTS["translation"][test_name]
    text = response.strip()
    meta = re.compile(
        r"^(here('s| is) the translation[:\s]*|translation[:\s]*|"
        r"in (russian|spanish|english)[:\s]*)", re.I)
    text = meta.sub("", text).strip()

    if cfg["check"] == "cyrillic":
        ratio = sum(1 for c in text if '\u0400' <= c <= '\u04FF') / max(len(text), 1)
        score = 100 if ratio > 0.25 else 50 if ratio > 0.05 else 0
        return {"score": score, "cyrillic_ratio": round(ratio, 3)}

    if cfg["check"] == "latin":
        ratio = sum(1 for c in text if c.isascii() and c.isalpha()) / max(len(text), 1)
        score = 100 if ratio > 0.60 else 50 if ratio > 0.30 else 0
        return {"score": score, "latin_ratio": round(ratio, 3)}

    if cfg["check"] == "spanish_words":
        low_text = text.lower()
        found = sum(1 for w in cfg["keywords"] if re.search(r"\b" + re.escape(w) + r"\b", low_text))
        score = 100 if found >= 3 else 75 if found == 2 else 50 if found == 1 else 0
        return {"score": score, "keywords_found": found}

    return {"score": 0}
def compute_quality(avg_code, reasoning_score, avg_instr, avg_trans):
    """
    Weighted quality score / 100.
    Weights sum to 1.0:
      code        35% — hardest to fake, directly executable
      reasoning   30% — logical thinking
      instruction 20% — instruction-following, practical utility
      translation 15% — multilingual capability
    """
    return round(
        avg_code        * 0.35 +
        reasoning_score * 0.30 +
        avg_instr       * 0.20 +
        avg_trans       * 0.15,
        1
    )
def _should_run_full_today():
    return datetime.now().weekday() == 0

class ModelBenchmark:
    def __init__(self, active_providers=None, active_models=None, merge=False, mode="auto"):
        self.groq_key         = os.getenv("GROQ_API_KEY")
        self.cerebras_key     = os.getenv("CEREBRAS_API_KEY")
        self.together_key     = os.getenv("TOGETHER_API_KEY")
        self._openrouter_keys = _load_openrouter_keys()
        self._or_key_index    = 0
        self._or_exhausted    = False
        self.active_providers = active_providers
        self.active_models    = active_models
        self.merge            = merge
        self.results          = []
        self._is_thinking     = False

        if mode == "auto":
            self.mode = "full" if _should_run_full_today() else "speed"
        else:
            self.mode = mode

    @property
    def openrouter_key(self):
        if not self._openrouter_keys:
            return None
        return self._openrouter_keys[self._or_key_index]

    def _rotate_openrouter_key(self):
        if self._or_key_index + 1 < len(self._openrouter_keys):
            self._or_key_index += 1
            hint = self._openrouter_keys[self._or_key_index][:12] + "..."
            print(f"\n    [openrouter] rotating → key #{self._or_key_index+1}/{len(self._openrouter_keys)} ({hint})",
                  end="", flush=True)
            time.sleep(1)
            return True
        self._or_exhausted = True
        print(f"\n    [openrouter] all {len(self._openrouter_keys)} keys at rate limit — skipping",
              flush=True)
        return False

    def _reset_or_state(self):
        self._or_key_index = 0
        self._or_exhausted = False
    def _openai_post(self, url, headers, model_id, prompt, timeout=25):
        data = {
            "model":       model_id,
            "messages":    [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens":  512,
        }
        start = time.time()
        try:
            r = requests.post(url, headers=headers, json=data, timeout=timeout)
            elapsed = time.time() - start
            if r.status_code == 200:
                body    = r.json()
                content = body["choices"][0]["message"].get("content") or ""
                usage   = body.get("usage", {})
                tokens  = usage.get("total_tokens", 0) or usage.get("completion_tokens", 0)
                return {"success": True, "content": content,
                        "total_time": round(elapsed, 3), "tokens": tokens,
                        "tokens_per_sec": round(tokens / elapsed, 2) if elapsed > 0 else 0}
            err = f"Status {r.status_code}"
            try:
                msg = r.json().get("error", {}).get("message", "")
                if msg: err += f" - {msg[:120]}"
            except Exception:
                pass
            return {"success": False, "error": err, "status_code": r.status_code}
        except requests.exceptions.Timeout:
            return {"success": False, "error": f"Timeout after {timeout}s"}
        except Exception as e:
            return {"success": False, "error": str(e)[:120]}

    def call_groq(self, model_id, prompt):
        if not self.groq_key:
            return {"success": False, "error": "GROQ_API_KEY not set"}
        return self._openai_post(GROQ_API,
            {"Authorization": f"Bearer {self.groq_key}",
             "Content-Type": "application/json"},
            model_id, prompt, timeout=TIMEOUT_BY_PROVIDER["groq"])

    def call_openrouter(self, model_id, prompt):
        if not self._openrouter_keys:
            return {"success": False, "error": "no OPENROUTER_API_KEY configured"}
        if self._or_exhausted:
            return {"success": False, "error": "all OR keys exhausted"}
        while True:
            result = self._openai_post(OPENROUTER_API, {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://modellens.ai",
                "X-Title":      "ModelLens",
            }, model_id, prompt, timeout=TIMEOUT_BY_PROVIDER["openrouter"])
            if result["success"]:
                return result
            status = result.get("status_code", 0)
            if status in _OR_ROTATE_STATUSES:
                if self._rotate_openrouter_key():
                    continue
                return {"success": False, "error": "all OR keys at rate limit"}
            return result

    def call_cerebras(self, model_id, prompt):
        if not self.cerebras_key:
            return {"success": False, "error": "CEREBRAS_API_KEY not set"}
        return self._openai_post(CEREBRAS_API,
            {"Authorization": f"Bearer {self.cerebras_key}",
             "Content-Type": "application/json"},
            model_id, prompt, timeout=TIMEOUT_BY_PROVIDER["cerebras"])

    def call_together(self, model_id, prompt):
        if not self.together_key:
            return {"success": False, "error": "TOGETHER_API_KEY not set"}
        return self._openai_post(TOGETHER_API,
            {"Authorization": f"Bearer {self.together_key}",
             "Content-Type": "application/json"},
            model_id, prompt, timeout=TIMEOUT_BY_PROVIDER["together"])

    def _call(self, provider, model_id, prompt):
        fn = {"groq": self.call_groq, "openrouter": self.call_openrouter,
              "cerebras": self.call_cerebras, "together": self.call_together}.get(provider)
        if not fn:
            return {"success": False, "error": f"unknown provider: {provider}"}
        return fn(model_id, prompt)

    def _content(self, raw):
        """Strip <think> blocks for thinking models before any evaluation."""
        return strip_thinking(raw) if self._is_thinking else (raw or "")
    def run_model(self, provider, model_info):
        delay = REQUEST_DELAY.get(provider, 2)
        mid   = model_info["id"]
        self._current_model_info = model_info
        self._reset_or_state()
        self._is_thinking = model_info.get("thinking", False)

        result = {
            "model_id":       model_info.get("key", mid),
            "model_name":     model_info["name"],
            "provider":       model_info["provider"],
            "size":           model_info["size"],
            "size_category":  size_category(model_info["size"]),
            "context":        model_info.get("context", "N/A"),
            "timestamp":      datetime.now().isoformat(),
            "benchmark_mode": self.mode,
            "tests":          {},
        }
        print("  speed...", end=" ", flush=True)
        speed_raw = []
        for name, prompt in TESTS["speed"].items():
            r = self._call(provider, mid, prompt)
            if r["success"] and r.get("tokens_per_sec", 0) > 0:
                speed_raw.append({"test": name, "time": r["total_time"],
                                  "tokens_per_sec": r["tokens_per_sec"],
                                  "tokens": r["tokens"]})
            else:
                err = r.get("error", "empty response") if not r["success"] else "0 tok/s"
                print(f"\n    [{name}] {err}", end="")
            time.sleep(delay)

        avg_tps = round(sum(x["tokens_per_sec"] for x in speed_raw) / len(speed_raw), 2) \
                  if speed_raw else 0
        result["tests"]["speed"] = {"avg_tokens_per_sec": avg_tps, "details": speed_raw}
        result["raw_speed"] = avg_tps
        print(f"done ({avg_tps} tok/s)")

        if not speed_raw:
            print("  -> model unreachable, skipping quality tests")
            result["quality_score"] = 0
            result["overall_score"] = 0
            return result
        if self.mode == "full":
            print("  code...", end=" ", flush=True)
            code_raw = []
            for name, cfg in TESTS["code"].items():
                fn_name = cfg.get("fn") or cfg["prompt"].split("called ")[1].split("(")[0].strip()
                r = self._call(provider, mid, cfg["prompt"])
                content = self._content(r.get("content", "")) if r["success"] else ""
                code_raw.append({"test": name, **eval_code_smart(name, content, fn_name)})
                if not r["success"]:
                    print(f"\n    [{name}] {r['error']}", end="")
                time.sleep(delay)
            avg_code = round(sum(x["pass_rate"] for x in code_raw) / len(code_raw) * 100, 1) \
                       if code_raw else 0
            result["tests"]["code"] = {"avg_score": avg_code, "details": code_raw}
            print(f"done ({sum(x.get('passed',0) for x in code_raw)}/"
                  f"{sum(x.get('total',0) for x in code_raw)} passed)")
            print("  reasoning...", end=" ", flush=True)
            reason_raw = []
            for name, cfg in TESTS["reasoning"].items():
                r = self._call(provider, mid, cfg["prompt"])
                content = self._content(r.get("content", "")) if r["success"] else ""
                reason_raw.append({"test": name, **eval_reasoning_smart(name, content)})
                if not r["success"]:
                    print(f"\n    [{name}] {r['error']}", end="")
                time.sleep(delay)
            correct_n       = sum(1 for x in reason_raw if x.get("correct"))
            reasoning_score = round(correct_n / len(reason_raw) * 100, 1) if reason_raw else 0
            result["tests"]["reasoning"] = {"score": reasoning_score, "correct": correct_n,
                                            "total": len(reason_raw), "details": reason_raw}
            print(f"done ({correct_n}/{len(reason_raw)} correct)")
            print("  instructions...", end=" ", flush=True)
            instr_raw = []
            for name, cfg in TESTS["instruction"].items():
                r = self._call(provider, mid, cfg["prompt"])
                content = self._content(r.get("content", "")) if r["success"] else ""
                instr_raw.append({"test": name, **eval_instruction_smart(name, content)})
                if not r["success"]:
                    print(f"\n    [{name}] {r['error']}", end="")
                time.sleep(delay)
            avg_instr = round(sum(x["score"] for x in instr_raw) / len(instr_raw), 1) \
                        if instr_raw else 0
            result["tests"]["instruction"] = {"avg_score": avg_instr, "details": instr_raw}
            print(f"done ({avg_instr}/100)")
            print("  translation...", end=" ", flush=True)
            trans_raw = []
            for name, cfg in TESTS["translation"].items():
                r = self._call(provider, mid, cfg["prompt"])
                content = self._content(r.get("content", "")) if r["success"] else ""
                trans_raw.append({"test": name, **eval_translation_smart(name, content)})
                if not r["success"]:
                    print(f"\n    [{name}] {r['error']}", end="")
                time.sleep(delay)
            avg_trans = round(sum(x["score"] for x in trans_raw) / len(trans_raw), 1) \
                        if trans_raw else 0
            result["tests"]["translation"] = {"avg_score": avg_trans, "details": trans_raw}
            print(f"done ({avg_trans}/100)")

            quality = compute_quality(avg_code, reasoning_score, avg_instr, avg_trans)
            result["quality_score"] = quality
            result["overall_score"] = quality

        else:
            quality = self._get_cached_quality(result["model_id"])
            result["quality_score"] = quality
            result["overall_score"] = quality
            if quality > 0:
                print(f"  quality: {quality} (cached from last full run)")

        return result

    def _get_cached_quality(self, model_id):
        try:
            lb = Path("../docs/data/results/leaderboard.json")
            if not lb.exists():
                return 0
            data = json.loads(lb.read_text())
            for r in data:
                if r.get("model_id") == model_id:
                    return r.get("quality_score", 0)
        except Exception:
            pass
        return 0
    def run_benchmark(self):
        print("ModelLens Benchmark")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Mode: {self.mode.upper()} "
              f"({'full quality + speed' if self.mode == 'full' else 'speed only'})")

        key_map = {
            "groq":       self.groq_key,
            "openrouter": bool(self._openrouter_keys),
            "cerebras":   self.cerebras_key,
            "together":   self.together_key,
        }
        active = []
        if self.groq_key: active.append("Groq")
        if self._openrouter_keys:
            n = len(self._openrouter_keys)
            active.append(f"OpenRouter ({n} key{'s' if n>1 else ''})")
        if self.cerebras_key: active.append("Cerebras")
        if self.together_key: active.append("Together")
        print(f"Providers: {', '.join(active) or 'none'}\n")

        for provider, models in MODELS.items():
            if self.active_providers and provider not in self.active_providers:
                print(f"Skip {provider} (not in --providers)")
                continue
            if not key_map.get(provider):
                print(f"Skip {provider} (no API key)")
                continue
            for mkey, minfo in models.items():
                if self.active_models and mkey not in self.active_models:
                    continue
                if minfo.get("disabled"):
                    print(f"  Skip {minfo['name']} (disabled in config)")
                    continue
                minfo = dict(minfo, key=mkey)
                cat   = size_category(minfo["size"])
                print(f"\n{minfo['name']} [{cat}] via {provider}")
                r = self.run_model(provider, minfo)
                if r:
                    self.results.append(r)
                    print(f"  -> quality={r['quality_score']}  speed={r['raw_speed']} tok/s")
                if provider == "openrouter" and r and r["raw_speed"] == 0:
                    time.sleep(8)

        self.save_results()
    def save_results(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        Path("../docs/data/results").mkdir(parents=True, exist_ok=True)
        for cat in ["small", "medium", "large", "unknown"]:
            speeds = [r["raw_speed"] for r in self.results
                      if r.get("size_category") == cat and r["raw_speed"] > 0]
            max_s  = max(speeds, default=1)
            for r in self.results:
                if r.get("size_category") == cat:
                    r["speed_score"] = round(r["raw_speed"] / max_s * 100, 1)

        daily_path = Path(f"../docs/data/results/{date_str}.json")
        if self.merge and daily_path.exists():
            try:
                existing   = json.loads(daily_path.read_text())
                tested_ids = {r["model_id"] for r in self.results}
                kept       = [r for r in existing if r["model_id"] not in tested_ids]
                self.results = kept + self.results
                print(f"\n  merged with {len(kept)} existing results")
            except Exception as e:
                print(f"\n  merge failed ({e}), overwriting")

        with open(daily_path, "w") as f:
            json.dump(self.results, f, indent=2)
        with open("../docs/data/results/latest.json", "w") as f:
            json.dump({"date": date_str,
                       "timestamp": datetime.now().isoformat(),
                       "results": self.results}, f, indent=2)

        def best_per_model(results, sort_key):
            seen = {}
            for r in sorted(results, key=lambda x: x.get(sort_key, 0), reverse=True):
                if r.get("quality_score", 0) == 0 and r.get("raw_speed", 0) == 0:
                    continue
                if r["model_name"] not in seen:
                    seen[r["model_name"]] = r
            return list(seen.values())

        q_board = sorted(best_per_model(self.results, "quality_score"),
                         key=lambda x: x["quality_score"], reverse=True)
        with open("../docs/data/results/leaderboard.json", "w") as f:
            json.dump(q_board, f, indent=2)

        s_board = sorted(best_per_model(self.results, "raw_speed"),
                         key=lambda x: x["raw_speed"], reverse=True)
        with open("../docs/data/results/leaderboard_speed.json", "w") as f:
            json.dump(s_board, f, indent=2)

        print(f"\nSaved {date_str}.json ({len(self.results)} models) — mode: {self.mode}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--providers", default=None)
    parser.add_argument("--models",    default=None)
    parser.add_argument("--merge",     action="store_true")
    parser.add_argument("--mode",      default="auto",
                        help="auto | speed | full")
    args = parser.parse_args()

    active_providers = [p.strip().lower() for p in args.providers.split(",") ] if args.providers else None
    active_models    = [m.strip()         for m in args.models.split(",")    ] if args.models    else None

    ModelBenchmark(
        active_providers=active_providers,
        active_models=active_models,
        merge=args.merge,
        mode=args.mode,
    ).run_benchmark()
