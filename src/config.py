THINKING_MODELS = {
    "qwen/qwen3-32b",
    "qwen/qwen3-4b:free",
    "qwen/qwen3-coder:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "qwen-3-32b",
    "liquid/lfm-2.5-1.2b-thinking:free",
}

MODELS = {
    "groq": {
        "llama-3.1-8b": {
            "id": "llama-3.1-8b-instant",
            "name": "Llama 3.1 8B Instant",
            "provider": "Groq", "size": "8B",
            "size_category": "small", "context": "131k"
        },
        "llama-3.3-70b": {
            "id": "llama-3.3-70b-versatile",
            "name": "Llama 3.3 70B",
            "provider": "Groq", "size": "70B",
            "size_category": "large", "context": "131k"
        },
        "gpt-oss-120b": {
            "id": "openai/gpt-oss-120b",
            "name": "GPT-OSS 120B",
            "provider": "Groq", "size": "120B",
            "size_category": "large", "context": "131k"
        },
        "gpt-oss-20b": {
            "id": "openai/gpt-oss-20b",
            "name": "GPT-OSS 20B",
            "provider": "Groq", "size": "20B",
            "size_category": "medium", "context": "131k"
        },
        "llama-4-scout": {
            "id": "meta-llama/llama-4-scout-17b-16e-instruct",
            "name": "Llama 4 Scout 17B",
            "provider": "Groq", "size": "17B",
            "size_category": "medium", "context": "131k"
        },
        "qwen3-32b": {
            "id": "qwen/qwen3-32b",
            "name": "Qwen 3 32B",
            "provider": "Groq", "size": "32B",
            "size_category": "medium", "context": "32k",
            "thinking": True
        },
        "kimi-k2": {
            "id": "moonshotai/kimi-k2-instruct",
            "name": "Kimi K2",
            "provider": "Groq", "size": "N/A",
            "size_category": "unknown", "context": "131k"
        },
    },

    "openrouter": {
        "nemotron-super-120b": {
            "id": "nvidia/nemotron-3-super-120b-a12b:free",
            "name": "Nemotron 3 Super 120B",
            "provider": "OpenRouter", "size": "120B",
            "size_category": "large", "context": "262k"
        },
        "nemotron-nano-30b": {
            "id": "nvidia/nemotron-3-nano-30b-a3b:free",
            "name": "Nemotron 3 Nano 30B",
            "provider": "OpenRouter", "size": "30B",
            "size_category": "medium", "context": "256k"
        },
        "nemotron-nano-12b": {
            "id": "nvidia/nemotron-nano-12b-v2-vl:free",
            "name": "Nemotron Nano 12B",
            "provider": "OpenRouter", "size": "12B",
            "size_category": "medium", "context": "128k"
        },
        "nemotron-nano-9b": {
            "id": "nvidia/nemotron-nano-9b-v2:free",
            "name": "Nemotron Nano 9B",
            "provider": "OpenRouter", "size": "9B",
            "size_category": "small", "context": "128k"
        },
        "trinity-large": {
            "id": "arcee-ai/trinity-large-preview:free",
            "name": "Trinity Large 400B",
            "provider": "OpenRouter", "size": "400B",
            "size_category": "large", "context": "131k"
        },
        "trinity-mini": {
            "id": "arcee-ai/trinity-mini:free",
            "name": "Trinity Mini 26B",
            "provider": "OpenRouter", "size": "26B",
            "size_category": "medium", "context": "131k"
        },
        "step-3.5-flash": {
            "id": "stepfun/step-3.5-flash:free",
            "name": "Step 3.5 Flash 196B",
            "provider": "OpenRouter", "size": "196B",
            "size_category": "large", "context": "256k"
        },
        "gemma-3-27b": {
            "id": "google/gemma-3-27b-it:free",
            "name": "Gemma 3 27B",
            "provider": "OpenRouter", "size": "27B",
            "size_category": "medium", "context": "131k"
        },
        "gemma-3-12b": {
            "id": "google/gemma-3-12b-it:free",
            "name": "Gemma 3 12B",
            "provider": "OpenRouter", "size": "12B",
            "size_category": "medium", "context": "32k"
        },
        "gemma-3-4b": {
            "id": "google/gemma-3-4b-it:free",
            "name": "Gemma 3 4B",
            "provider": "OpenRouter", "size": "4B",
            "size_category": "small", "context": "32k"
        },
        "gemma-3n-e4b": {
            "id": "google/gemma-3n-e4b-it:free",
            "name": "Gemma 3n E4B",
            "provider": "OpenRouter", "size": "4B",
            "size_category": "small", "context": "8k"
        },
        "gemma-3n-e2b": {
            "id": "google/gemma-3n-e2b-it:free",
            "name": "Gemma 3n E2B",
            "provider": "OpenRouter", "size": "2B",
            "size_category": "small", "context": "8k"
        },
        "lfm-2.5-instruct": {
            "id": "liquid/lfm-2.5-1.2b-instruct:free",
            "name": "LFM 2.5 1.2B Instruct",
            "provider": "OpenRouter", "size": "1.2B",
            "size_category": "small", "context": "32k"
        },
        "lfm-2.5-thinking": {
            "id": "liquid/lfm-2.5-1.2b-thinking:free",
            "name": "LFM 2.5 1.2B Thinking",
            "provider": "OpenRouter", "size": "1.2B",
            "size_category": "small", "context": "32k",
            "thinking": True
        },
        "llama-3.3-70b": {
            "id": "meta-llama/llama-3.3-70b-instruct:free",
            "name": "Llama 3.3 70B",
            "provider": "OpenRouter", "size": "70B",
            "size_category": "large", "context": "66k"
        },
        "llama-3.2-3b": {
            "id": "meta-llama/llama-3.2-3b-instruct:free",
            "name": "Llama 3.2 3B",
            "provider": "OpenRouter", "size": "3B",
            "size_category": "small", "context": "131k"
        },
        "qwen3-coder": {
            "id": "qwen/qwen3-coder:free",
            "name": "Qwen3 Coder 480B",
            "provider": "OpenRouter", "size": "480B",
            "size_category": "large", "context": "262k",
            "thinking": True
        },
        "qwen3-next-80b": {
            "id": "qwen/qwen3-next-80b-a3b-instruct:free",
            "name": "Qwen3 Next 80B",
            "provider": "OpenRouter", "size": "80B",
            "size_category": "large", "context": "262k",
            "thinking": True
        },
        "qwen3-4b": {
            "id": "qwen/qwen3-4b:free",
            "name": "Qwen 3 4B",
            "provider": "OpenRouter", "size": "4B",
            "size_category": "small", "context": "41k",
            "thinking": True
        },
        "mistral-small-3.1": {
            "id": "mistralai/mistral-small-3.1-24b-instruct:free",
            "name": "Mistral Small 3.1 24B",
            "provider": "OpenRouter", "size": "24B",
            "size_category": "medium", "context": "128k"
        },
        "hermes-405b": {
            "id": "nousresearch/hermes-3-llama-3.1-405b:free",
            "name": "Hermes 3 405B",
            "provider": "OpenRouter", "size": "405B",
            "size_category": "large", "context": "131k"
        },
        "dolphin-mistral-24b": {
            "id": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            "name": "Dolphin Mistral 24B",
            "provider": "OpenRouter", "size": "24B",
            "size_category": "medium", "context": "32k"
        },
        "glm-4.5-air": {
            "id": "z-ai/glm-4.5-air:free",
            "name": "GLM 4.5 Air",
            "provider": "OpenRouter", "size": "N/A",
            "size_category": "medium", "context": "131k"
        },
    },

    "cerebras": {
        "llama-3.1-8b": {
            "id": "llama3.1-8b",
            "name": "Llama 3.1 8B",
            "provider": "Cerebras", "size": "8B",
            "size_category": "small", "context": "131k"
        },
        "llama-3.3-70b": {
            "id": "llama-3.3-70b",
            "name": "Llama 3.3 70B",
            "provider": "Cerebras", "size": "70B",
            "size_category": "large", "context": "131k",
            "disabled": True
        },
        "qwen3-32b": {
            "id": "qwen-3-32b",
            "name": "Qwen 3 32B",
            "provider": "Cerebras", "size": "32B",
            "size_category": "medium", "context": "131k",
            "disabled": True,
            "thinking": True
        },
    },
}

TESTS = {
    "speed": {
        "simple": "Write a haiku about artificial intelligence.",
        "medium": "Explain quantum computing in simple terms (200 words).",
        "long":   "Write a detailed tutorial on Python decorators with examples (300 words).",
    },
    "code": {
        "prime": {
            "prompt": "Write a Python function called is_prime(n) that returns True if n is prime, False otherwise. Return ONLY the function, no explanation.",
            "fn": "is_prime",
            "test_input": [2, 3, 4, 17, 100],
            "expected":   [True, True, False, True, False]
        },
        "fibonacci": {
            "prompt": "Write a Python function called fibonacci(n) that returns the nth Fibonacci number (0-indexed, so fibonacci(0)=0, fibonacci(1)=1, fibonacci(7)=13). Return ONLY the function, no explanation.",
            "fn": "fibonacci",
            "test_input": [0, 1, 7, 10],
            "expected":   [0, 1, 13, 55]
        },
        "palindrome": {
            "prompt": "Write a Python function called is_palindrome(s) that returns True if string s is a palindrome (ignore case and spaces). Return ONLY the function, no explanation.",
            "fn": "is_palindrome",
            "test_input": ["racecar", "hello", "A man a plan a canal Panama", "world"],
            "expected":   [True, False, True, False]
        }
    },
    "reasoning": {
        "syllogism": {
            "prompt": "If all bloops are razzies and all razzies are lazzies, are all bloops definitely lazzies? Answer with just Yes or No.",
            "answer": "yes"
        },
        "speed_math": {
            "prompt": "A train travels 120 km in 2 hours. Another train travels 180 km in 3 hours. Which is faster? Answer with: First, Second, or Same.",
            "answer": "same"
        },
        "river_crossing": {
            "prompt": "A farmer has a fox, a chicken, and a bag of grain. He needs to cross a river with a boat that can only carry him and one item. The fox eats the chicken if left alone, and the chicken eats the grain. What does he take first? Answer with one word: Fox, Chicken, or Grain.",
            "answer": "chicken"
        },
        "coin_flip": {
            "prompt": "I flip a fair coin 3 times and get heads each time. What is the probability of getting heads on the 4th flip? Answer with a fraction like 1/2.",
            "answer": "1/2"
        },
        "counting": {
            "prompt": "How many letters are in the word MISSISSIPPI? Answer with just the number.",
            "answer": "11"
        }
    },
    "instruction": {
        "json": {
            "prompt": 'Return a JSON object with exactly these keys: "name", "age", "city". Use any values you like. Return ONLY valid JSON, nothing else.',
            "check": "json_keys",
            "required_keys": ["name", "age", "city"]
        },
        "list": {
            "prompt": "List exactly 5 programming languages, one per line, numbered 1-5. No extra text.",
            "check": "numbered_list",
            "count": 5
        },
        "word_count": {
            "prompt": "Write a description of Paris in exactly 3 sentences. No more, no less.",
            "check": "sentence_count",
            "count": 3
        }
    },
    "translation": {
        "en_ru": {
            "prompt": "Translate to Russian: 'Artificial intelligence is changing the world.' Return only the translation.",
            "check": "cyrillic"
        },
        "ru_en": {
            "prompt": "Translate to English: 'Машинное обучение помогает решать сложные задачи.' Return only the translation.",
            "check": "latin"
        },
        "en_es": {
            "prompt": "Translate to Spanish: 'The future belongs to those who believe in the beauty of their dreams.' Return only the translation.",
            "check": "spanish_words",
            "keywords": ["el", "la", "los", "las", "que", "de", "su", "sus", "futuro", "sueños", "pertenece", "creen", "belleza"]
        }
    }
}

RATE_LIMITS = {
    "groq": 30,
    "openrouter": 8
}
