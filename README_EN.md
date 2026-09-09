# 🏆 Fanqie Rank Tracker

[![中文](https://img.shields.io/badge/lang-中文-red)](README.md)

> Daily tracking for Fanqie **female new books**, **male new books**, and **audiobook heat** (read ranks), with AI trend analysis and a static dashboard.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🕷️ Three channels | Daily Top 30 scrape for female new-book ranks, male new-book ranks, and audiobook heat (male + female read ranks) |
| 📊 Trend Analysis | Day-over-day comparison: new entries / dropped / rank changes / readership growth |
| 🤖 AI Summary | OpenAI-compatible API for per-channel, per-category market briefs |
| 🧭 Type compass | Multi-day aggregation of hot genres, categories, and themes |
| 🖥️ Dashboard | Editorial dashboard with channel switcher and waterfall book cards |
| 📱 Responsive | Full mobile support with slide-out sidebar |
| ⚡ Fully Automated | GitHub Actions + GitHub Pages |

---

## 📡 Channels

Fanqie web ranks use `/rank/{gender}_{list}_{category}`:

| Channel | URL prefix | What it scrapes | Dashboard |
|---------|------------|-----------------|-----------|
| Female | `/rank/0_1_*` | Female new-book ranks | `index.html?ch=female` |
| Male | `/rank/1_1_*` | Male new-book ranks | `index.html?ch=male` |
| Audio | `/rank/1_2_*` + `/rank/0_2_*` | Male + female read ranks | `index.html?ch=audio` |

> Fanqie's website has no dedicated audiobook chart. Audiobooks share the same catalog as novels (TTS / audio), so this project uses read ranks as the heat signal. Category names are prefixed with `男频 · ` / `女频 · `.

Female history stays in `data/fanqie_female_new_ranks_*.json`. Male and audio snapshots go to `data/male/` and `data/audio/`.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Git**
- A GitHub account
- (Optional) An OpenAI-compatible API key for AI analysis

### Step 1: Fork the Repository

Click the **Fork** button on the top-right corner of the GitHub page.

### Step 2: Enable GitHub Pages

1. Go to your forked repo → **Settings** → **Pages**
2. Under Source, select **Deploy from a branch**
3. Select `main` branch and `/ (root)` directory
4. Click **Save**

Your dashboard will be live at: `https://<your-username>.github.io/<repo>/`

### Step 3: Configure Secrets (Optional, for AI Analysis)

Add these repository secrets:

| Secret Name | Description | Example |
|---|---|---|
| `API_BASE_URL` | OpenAI-compatible API endpoint | `https://api.openai.com/v1` |
| `API_KEY` | API key | `sk-xxxxxxxxxxxxx` |
| `API_MODEL` | Model name | `gpt-4o-mini` |

If these secrets are not configured, the system falls back to rule-based summaries.

### Step 4: Trigger the First Run Manually

1. Go to repo → **Actions** → **Daily Fanqie Rank Scraper**
2. Click **Run workflow**
3. Wait 8–15 minutes for all three channels

### Step 5: Sit Back and Relax

GitHub Actions runs daily at **UTC 00:17 (08:17 Beijing Time)**.

---

## 🔌 Latest Data API

| Channel | Index | All | Per type |
|---|---|---|---|
| Female | `api/lastest.json` | `api/lastest/all.json` | `api/lastest/<type>.json` |
| Male | `api/male/lastest.json` | `api/male/lastest/all.json` | `api/male/lastest/<type>.json` |
| Audio | `api/audio/lastest.json` | `api/audio/lastest/all.json` | `api/audio/lastest/<type>.json` |
| Channel list | `api/channels.json` | — | — |

---

## 🔧 Local Development

```bash
python scrape_fanqie_ranks.py                 # all channels
python scrape_fanqie_ranks.py --channel male  # male only
python scrape_fanqie_ranks.py --channel audio # audiobook heat only
python scripts/build_latest.py
python -m http.server 8000
```

Open `http://localhost:8000/index.html?ch=male` or `?ch=audio`.

---

## 📝 FAQ

**Q: Why does the audio channel scrape read ranks?**

Fanqie's public rank page only has new-book and read ranks for male/female. There is no dedicated audiobook chart. Read ranks are the closest heat signal because audiobooks share the same catalog.

---

## 📜 License

MIT
