# 🔍 Python Website Uptime Monitor

A lightweight, free uptime monitoring system built with Python and GitHub Actions. Sends instant alerts to Discord, Slack, or Telegram when your site goes down — no paid services, no servers, no hassle.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![GitHub Actions](https://img.shields.io/badge/Runs%20on-GitHub%20Actions-2088FF) ![Free](https://img.shields.io/badge/Cost-Free-brightgreen)

---

## ✨ Features

- Automatically checks your site(s) every 15 minutes via GitHub Actions
- Sends instant alerts when a site goes down or recovers
- State-aware — no notification spam during long outages
- Credentials stored securely in GitHub Secrets (never in your code)
- Supports Discord, Slack, and Telegram
- 100% free to run

---

## 📁 Project Structure

```
your-repo/
├── monitor.py                   # Main monitoring script
├── requirements.txt             # Dependencies (just requests)
├── monitor_state.json           # Tracks last known site status
└── .github/
    └── workflows/
        └── uptime-monitor.yml   # GitHub Actions schedule
```

---

## 🚀 Quick Start

1. **Fork this repository**
2. **Add your webhook URL as a GitHub Secret**
   - Go to Settings → Secrets and variables → Actions → New repository secret
   - Name it `DISCORD_WEBHOOK_URL` and paste your Discord webhook URL
3. **Edit `monitor.py`** — update `URLS_TO_MONITOR` with your own URLs
4. **Push your changes** — GitHub Actions will handle the rest

The monitor runs automatically every 15 minutes. You can also trigger it manually from the Actions tab at any time.

---

## 🔔 Alert Platforms

Discord is configured by default. The [full blog post](https://www.procwire.com/2026/06/python-website-uptime-monitor.html) includes step-by-step instructions for switching to **Slack** or **Telegram** with just a few lines changed.

---

## 🧪 Testing It Works

Before waiting for a scheduled run, go to the **Actions** tab → **Website Uptime Monitor** → **Run workflow**. Watch the live console output to confirm everything is working.

To test alerts, temporarily change one of your URLs in `monitor.py` to `https://httpstat.us/500`, push the change, and run the workflow manually. You should receive a Discord alert within seconds. Then revert the URL.

---

## 💡 Real-World Uses for This Monitor
This type of Python uptime monitoring system can be used for much more than websites.

- Monitoring personal blogs
- Checking automation APIs
- Tracking Discord bot health endpoints
- Watching VPS landing pages
- Monitoring portfolio sites
- Checking internal tools for clients

Once you understand this workflow, you can automate monitoring for almost anything online.

---

## 📖 Full Guide

This repo accompanies the blog post [**"How to Build a Free Python Uptime Monitor with GitHub Actions"**](https://www.procwire.com/2026/06/python-website-uptime-monitor.html) — read it for a complete walkthrough of every file, concept, and configuration option.

---

## 📄 License

MIT — free to use, modify, and share.

---

If this saved you some time, consider leaving a ⭐ on the repo.
