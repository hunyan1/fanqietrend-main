# 🏆 番茄风向标 · Fanqie Rank Tracker

[![English](https://img.shields.io/badge/lang-English-blue)](README_EN.md)

> 女频新书 / 男频新书 / 听书热播，每日自动追踪排行数据并结合 AI 生成趋势分析，部署为在线看板。

---

## ✨ 功能概览

| 功能 | 说明 |
|------|------|
| 🕷️ 三频道抓取 | 每日定时抓取女频新书榜、男频新书榜、听书热播榜（男女频阅读榜）各分类 Top 30 |
| 📊 趋势对比 | 自动对比相邻两天数据：新上榜 / 掉榜 / 排名变化 / 阅读量增长 |
| 🤖 AI 风向分析 | 接入 OpenAI 兼容 API，按频道、按分类生成市场趋势速评 |
| 🧭 类型风向标 | 独立趋势页聚合多日数据，用 AI 总结综合赛道、热门分类和高频题材 |
| 🖥️ 精美看板 | 暗色编辑风格仪表盘，带频道切换、瀑布流书籍卡片 |
| 📱 移动适配 | 完整的移动端适配，侧边栏抽屉式菜单 |
| 🔌 数据接口 | 按频道生成静态 `lastest` JSON 接口 |
| ⚡ 全自动化 | GitHub Actions + GitHub Pages，零服务器运维 |

---

## 📡 三个频道

番茄网页排行榜的路由是 `/rank/{性别}_{榜单}_{分类}`：

| 频道 | URL 前缀 | 抓什么 | 看板入口 |
|------|----------|--------|----------|
| 女频 | `/rank/0_1_*` | 女频新书榜 | `index.html?ch=female` |
| 男频 | `/rank/1_1_*` | 男频新书榜 | `index.html?ch=male` |
| 听书 | `/rank/1_2_*` + `/rank/0_2_*` | 男女频阅读榜 | `index.html?ch=audio` |

> **听书说明：** 番茄网页没有独立「听书榜」。听书与小说同源（TTS / 有声），本项目用阅读榜作为热播信号，分类名前会带 `男频 · ` / `女频 · ` 前缀。

历史女频数据仍放在 `data/fanqie_female_new_ranks_*.json`，男频和听书分别写入 `data/male/`、`data/audio/`。

---

## 🚀 食用指南

### 前置条件

- **Python 3.9+**
- **Git**
- 一个 GitHub 账号
- （可选）一个 OpenAI 兼容 API 的密钥，用于 AI 分析

### 第一步：Fork 仓库

点击 GitHub 页面右上角的 **Fork** 按钮，将项目 Fork 到你自己的账号下。

### 第二步：开启 GitHub Pages

1. 进入你 Fork 后的仓库 → **Settings** → **Pages**
2. Source 选择 **Deploy from a branch**
3. Branch 选择 `main`，目录选择 `/ (root)`
4. 点击 **Save**

稍等几分钟，你的看板就会上线：`https://<你的用户名>.github.io/<仓库名>/`

### 第三步：配置 Secrets（可选，开启 AI 分析）

进入仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**，添加以下三个 Secret：

| Secret 名称 | 说明 | 示例 |
|---|---|---|
| `API_BASE_URL` | OpenAI 兼容 API 的地址 | `https://api.openai.com/v1` |
| `API_KEY` | API 密钥 | `sk-xxxxxxxxxxxxx` |
| `API_MODEL` | 模型名称 | `gpt-4o-mini` |

> **💡 提示：** 任何 OpenAI 兼容接口均可使用（如 Moonshot / DeepSeek / 自建服务等）。如果不配置这三个 Secret，系统将自动使用基于规则的摘要替代 AI 分析，**不影响核心功能**。

### 第四步：手动触发首次运行

1. 进入仓库 → **Actions** → 左侧选择 **Daily Fanqie Rank Scraper**
2. 点击右上角 **Run workflow** → **Run workflow**
3. 等待 Workflow 运行完成（三个频道大约 8–15 分钟）

运行成功后，`data/`、`data/male/`、`data/audio/` 会生成数据文件，打开 GitHub Pages 链接即可看到看板。侧边栏可切换女频 / 男频 / 听书。

### 第五步：坐等自动更新

GitHub Actions 已配置为 **每天 UTC 00:17（北京时间 08:17）** 自动运行。之后无需任何手动操作，数据和看板会每天自动更新。

看板右上角的 **风向标** 可进入 `trend.html`，先查看当下火热综合赛道、具体热门分类和高频题材，再按具体类型查看近 7 / 14 / 30 日或全部周期的趋势分析。全站热点会优先使用 AI 总结，未配置 API 或生成失败时使用规则统计文案兜底。

---

## 🔌 最新数据接口

构建脚本会同步生成 GitHub Pages 可直接访问的静态 JSON 接口：

| 频道 | 类型索引 | 全量数据 | 单类型 |
|---|---|---|---|
| 女频 | `api/lastest.json` | `api/lastest/all.json` | `api/lastest/<类型>.json` |
| 男频 | `api/male/lastest.json` | `api/male/lastest/all.json` | `api/male/lastest/<类型>.json` |
| 听书 | `api/audio/lastest.json` | `api/audio/lastest/all.json` | `api/audio/lastest/<类型>.json` |
| 频道列表 | `api/channels.json` | — | — |

示例：

```bash
curl https://<你的用户名>.github.io/<仓库名>/api/channels.json
curl https://<你的用户名>.github.io/<仓库名>/api/lastest/all.json
curl https://<你的用户名>.github.io/<仓库名>/api/male/lastest/all.json
curl https://<你的用户名>.github.io/<仓库名>/api/audio/lastest/all.json
```

---

## 🔧 本地开发

```bash
# 1. 克隆仓库
git clone https://github.com/<你的用户名>/fanqietrend-main.git
cd fanqietrend-main

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
playwright install chromium

# 4. 运行爬虫（默认三个频道；可只抓一个）
python scrape_fanqie_ranks.py                 # 女频 + 男频 + 听书
python scrape_fanqie_ranks.py --channel male  # 只抓男频
python scrape_fanqie_ranks.py --channel audio # 只抓听书热播

# 5. 构建看板数据（可选，带 AI 分析需设置环境变量）
pip install openai
export API_BASE_URL="https://your-api-endpoint/v1"
export API_KEY="your-api-key"
export API_MODEL="your-model-name"
python scripts/build_latest.py
python scripts/build_latest.py --channel female

# 6. 本地预览前端
python -m http.server 8000
# 打开 http://localhost:8000
# 男频：http://localhost:8000/index.html?ch=male
# 听书：http://localhost:8000/index.html?ch=audio
```

---

## 📁 项目结构

```
fanqietrend-main/
├── .github/workflows/
│   └── scrape.yml              # GitHub Actions 自动化工作流
├── css/
│   └── style.css
├── js/
│   ├── channels.js             # 女频 / 男频 / 听书频道配置
│   ├── app.js
│   ├── trend.js
│   └── book.js
├── scripts/
│   └── build_latest.py         # 按频道构建趋势 + AI 分析
├── channels.py                 # 爬虫 / 构建共用的频道配置
├── data/
│   ├── fanqie_female_new_ranks_YYYYMMDD.json
│   ├── latest_ranks.json
│   ├── market_summary.json
│   └── trends/
├── data/male/                  # 男频快照与趋势
├── data/audio/                 # 听书热播快照与趋势
├── api/
│   ├── channels.json
│   ├── lastest/                # 女频接口
│   ├── male/lastest/           # 男频接口
│   └── audio/lastest/          # 听书接口
├── index.html
├── trend.html
├── scrape_fanqie_ranks.py
└── README.md
```

---

## ⚙️ 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                   GitHub Actions (每日 08:17)                │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Playwright   │───▶│  build_latest │───▶│  git commit  │  │
│  │  女/男/听书   │    │  三频道趋势   │    │  自动提交     │  │
│  │  榜单抓取     │    │  + AI 分析    │    │  到 main     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                    GitHub Pages 自动部署
                    用户访问在线看板 🌐
```

---

## 📝 常见问题

<details>
<summary><b>Q: Workflow 运行失败怎么办？</b></summary>

检查 Actions 日志中的错误信息。常见原因：
- 番茄小说页面结构变更 → 需要更新爬虫选择器
- Playwright 安装超时 → 尝试重新运行
- 某个频道超时 → 可单独重跑：`python scrape_fanqie_ranks.py --channel male`

</details>

<details>
<summary><b>Q: 不配置 AI Secret 也能用吗？</b></summary>

可以！系统会自动 fallback 到基于规则的摘要（如"新增3本上榜；《XX》排名上升+5位"）。只是没有 AI 自然语言分析而已。

</details>

<details>
<summary><b>Q: 听书频道为什么抓的是阅读榜？</b></summary>

番茄网页排行榜只有「阅读榜 / 新书榜 × 男频 / 女频」，没有独立听书榜。听书内容与小说同源，阅读榜更能反映热播。分类名会带 `男频 · ` / `女频 · ` 前缀，方便区分。

</details>

---

## 📜 License

MIT

---

<p align="center">
  <sub>Made with ☕ and 🤖 — 数据每日自动更新，无需手动维护</sub>
</p>
