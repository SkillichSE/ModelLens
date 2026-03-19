# 🚀 Quick Start Guide

## Step 1: Fork & Clone

1. **Fork this repository** on GitHub
2. **Clone** to your computer:
```bash
git clone https://github.com/YOUR_USERNAME/ai-benchmarker
cd ai-benchmarker
```

## Step 2: Get Free API Keys (5-10 minutes)

### Required (Must Have):

#### 1. Groq API Key ⚡
- Visit: https://console.groq.com/keys
- Sign up with email or Google
- Click "Create API Key"
- Copy the key (starts with `gsk_...`)
- **Free forever, 30 req/min**

#### 2. Google AI Studio Key 🤖
- Visit: https://aistudio.google.com/app/apikey
- Sign in with Google account
- Click "Create API Key"
- Copy the key (starts with `AIza...`)
- **Free forever, 60 req/min**

### Optional (Can add later):

#### 3. Together AI
- Visit: https://api.together.xyz
- Get $25 free credits

#### 4. HuggingFace
- Visit: https://huggingface.co/settings/tokens
- Free tier available

## Step 3: Add Secrets to GitHub

1. Go to your forked repo on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

| Name | Value |
|------|-------|
| `GROQ_API_KEY` | Your Groq key (gsk_...) |
| `GOOGLE_API_KEY` | Your Google key (AIza...) |

**IMPORTANT:** Secret names must match exactly (all caps)!

## Step 4: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
3. Click **Save**
4. Wait 1-2 minutes

Your site will be live at:
```
https://YOUR_USERNAME.github.io/ai-benchmarker/
```

## Step 5: Run First Benchmark

1. Go to **Actions** tab
2. Click **"Daily AI Benchmark"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 5-10 minutes

After it completes:
- Green checkmark ✅ = Success!
- Red X ❌ = Check the logs for errors

## Step 6: View Your Site! 🎉

Visit:
```
https://YOUR_USERNAME.github.io/ai-benchmarker/
```

You should see:
- ✅ Benchmark results
- ✅ Model rankings
- ✅ Latest news
- ✅ Performance graphs

## Troubleshooting

### ❌ Workflow fails with "API key not found"
- Check secret names are EXACTLY: `GROQ_API_KEY` and `GOOGLE_API_KEY`
- Make sure you copied the full key (no spaces)

### ❌ Site shows "404 Not Found"
- Make sure GitHub Pages is enabled
- Check it's set to `/docs` folder
- Wait 2-3 minutes and refresh

### ❌ Site shows "First benchmark running..."
- The workflow is still running or hasn't run yet
- Go to Actions tab and check status
- Results appear after workflow completes

### ❌ Charts not showing
- Clear browser cache and refresh
- Check browser console for errors (F12)

## What Happens Next?

✅ **Automatic daily updates** at 3:00 UTC
✅ **Fresh benchmarks** every day
✅ **News aggregation** for AI updates
✅ **Zero maintenance** needed

## Customization

Want to add more models or change test prompts?

Edit: `src/config.py`

```python
MODELS = {
    "groq": {
        "your-model": {
            "id": "model-id",
            "name": "Display Name",
            ...
        }
    }
}
```

Then commit and push - next run will use new config!

## Need Help?

- 📖 Check main README.md
- 🐛 Open an issue on GitHub
- 💬 Ask in Discussions

---

**Enjoy your AI benchmarking platform! ⚡**
