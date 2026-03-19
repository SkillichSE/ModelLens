# ⚡ AI Model Benchmarker

> Real-time rankings of free AI models. Updated daily.

Live demo: `https://YOUR_USERNAME.github.io/ai-benchmarker/`

## 🎯 Features

- **Daily automated benchmarks** of 5+ free AI models
- **Real-time rankings** by speed, code quality, and more
- **News aggregator** for AI model updates
- **Trend graphs** showing performance over time
- **Smart search** with filters and comparisons
- **Google-style design** — clean, minimal, fast

## 🚀 Quick Start

### 1. Fork this repo

Click "Fork" button on GitHub

### 2. Enable GitHub Pages

```
Settings → Pages → Source: main branch → /docs folder → Save
```

### 3. Add API Keys (Secrets)

Go to `Settings → Secrets and variables → Actions → New repository secret`

Add these secrets:

| Name | Where to get |
|------|--------------|
| `GROQ_API_KEY` | https://console.groq.com/keys |
| `GOOGLE_API_KEY` | https://aistudio.google.com/app/apikey |
| `TOGETHER_API_KEY` | https://api.together.xyz/settings/api-keys (optional) |
| `HF_TOKEN` | https://huggingface.co/settings/tokens (optional) |

### 4. Run first benchmark

```
Actions → Daily Benchmark → Run workflow
```

Wait 5-10 minutes. Your site will be live at:
```
https://YOUR_USERNAME.github.io/ai-benchmarker/
```

## 📦 Project Structure

```
ai-benchmarker/
├── .github/workflows/
│   ├── benchmark.yml      # Daily model tests
│   └── news.yml          # News aggregator
├── docs/                  # GitHub Pages site
│   ├── index.html        # Home page
│   ├── search.html       # Model search
│   ├── news.html         # News feed
│   ├── trends.html       # Trend graphs
│   ├── style.css         # Google-style CSS
│   └── app.js           # Frontend logic
├── src/
│   ├── benchmark.py      # Benchmark runner
│   ├── news_parser.py    # News scraper
│   └── config.py         # Model configs
└── data/results/         # JSON data store
```

## 🔧 Configuration

Edit `src/config.py` to:
- Add/remove models
- Change test prompts
- Adjust benchmark settings

## 📊 How it works

1. **GitHub Actions** runs daily at 3:00 UTC
2. Benchmarks all configured models
3. Saves results to `data/results/YYYY-MM-DD.json`
4. Commits to repo
5. GitHub Pages automatically updates
6. Users see fresh data!

## 🆓 Cost

Everything is **100% free**:
- ✅ GitHub Actions: 2000 min/month (we use ~300)
- ✅ GitHub Pages: Free hosting + CDN
- ✅ API keys: All free tiers

## 🤝 Contributing

PRs welcome! Ideas:
- Add more models
- New test categories
- UI improvements
- More news sources

## 📝 License

MIT - do whatever you want!

## 🌟 Star this repo

If you find this useful, give it a ⭐!
