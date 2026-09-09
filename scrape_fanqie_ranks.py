import argparse
import json
import os
import sys
import time
from datetime import datetime

from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


from channels import CHANNEL_ORDER, get_channel, parse_channel_ids

START_CODE = 58344  # 0xE3E8
CHAR_SEQUENCE = [
    "D", "在", "主", "特", "家", "军", "然", "表", "场", "4", "要", "只", "v", "和", "?", "6", "别", "还", "g", "现", "儿", "岁", "?", "?", "此", "象", "月", "3", "出", "战", "工", "相", "o", "男", "直", "失", "世", "F", "都", "平", "文", "什", "V", "O", "将", "真", "T", "那", "当", "?", "会", "立", "些", "u", "是", "十", "张", "学", "气", "大", "爱", "两", "命", "全", "后", "东", "性", "通", "被", "1", "它", "乐", "接", "而", "感", "车", "山", "公", "了", "常", "以", "何", "可", "话", "先", "p", "i", "叫", "轻", "M", "士", "w", "着", "变", "尔", "快", "l", "个", "说", "少", "色", "里", "安", "花", "远", "7", "难", "师", "放", "t", "报", "认", "面", "道", "S", "?", "克", "地", "度", "I", "好", "机", "U", "民", "写", "把", "万", "同", "水", "新", "没", "书", "电", "吃", "像", "斯", "5", "为", "y", "白", "几", "日", "教", "看", "但", "第", "加", "候", "作", "上", "拉", "住", "有", "法", "r", "事", "应", "位", "利", "你", "声", "身", "国", "问", "马", "女", "他", "Y", "比", "父", "x", "A", "H", "N", "s", "X", "边", "美", "对", "所", "金", "活", "回", "意", "到", "z", "从", "j", "知", "又", "内", "因", "点", "Q", "三", "定", "8", "R", "b", "正", "或", "夫", "向", "德", "听", "更", "?", "得", "告", "并", "本", "q", "过", "记", "L", "让", "打", "f", "人", "就", "者", "去", "原", "满", "体", "做", "经", "K", "走", "如", "孩", "c", "G", "给", "使", "物", "?", "最", "笑", "部", "?", "员", "等", "受", "k", "行", "一", "条", "果", "动", "光", "门", "头", "见", "往", "自", "解", "成", "处", "天", "能", "于", "名", "其", "发", "总", "母", "的", "死", "手", "入", "路", "进", "心", "来", "h", "时", "力", "多", "开", "已", "许", "d", "至", "由", "很", "界", "n", "小", "与", "Z", "想", "代", "么", "分", "生", "口", "再", "妈", "望", "次", "西", "风", "种", "带", "J", "?", "实", "情", "才", "这", "?", "E", "我", "神", "格", "长", "觉", "间", "年", "眼", "无", "不", "亲", "关", "结", "0", "友", "信", "下", "却", "重", "己", "老", "2", "音", "字", "m", "呢", "明", "之", "前", "高", "P", "B", "目", "太", "e", "9", "起", "稜", "她", "也", "W", "用", "方", "子", "英", "每", "理", "便", "四", "数", "期", "中", "C", "外", "样", "a", "海", "们", "任"
]


def decode_text(text: str) -> str:
    if not text:
        return ""
    result = []
    for char in text:
        code = ord(char)
        idx = code - START_CODE
        if 0 <= idx < len(CHAR_SEQUENCE):
            result.append(CHAR_SEQUENCE[idx])
        else:
            result.append(char)
    return "".join(result)


EXTRACT_JS = """
() => {
    const bookMap = new Map();
    const links = document.querySelectorAll('a[href^="/page/"]');
    links.forEach(link => {
        let container = link.parentElement;
        let depth = 0;
        while (container && depth < 6) {
            if (container.querySelector('img') && container.innerText.includes('在读')) {
                const href = link.getAttribute('href');
                if (!bookMap.has(href)) {
                    bookMap.set(href, container);
                }
                break;
            }
            container = container.parentElement;
            depth++;
        }
    });

    const cards = Array.from(bookMap.values());
    const results = [];
    for (const item of cards) {
        let imgNode = item.querySelector('img');
        let cover = imgNode ? imgNode.getAttribute('src') : "";

        let title = "";
        if (imgNode && imgNode.getAttribute('alt')) {
            title = imgNode.getAttribute('alt').trim();
        }
        if (!title) {
            let textTitleNode = item.querySelector('h4, .title, h1') || item.querySelector('a[href^="/page/"]');
            if (textTitleNode) {
                let text = textTitleNode.innerText.trim();
                if (text && !/^\\d+$/.test(text)) {
                    title = text;
                }
            }
        }
        if (!title) title = "未知";
        if (title.includes("榜单说明")) continue;

        let authorNode = item.querySelector('.author, .author-name') || item.querySelector('a[href^="/author-page/"]');
        let author = authorNode ? authorNode.innerText.trim() : "未知";

        let reads = "未知";
        const lines = item.innerText.split('\\n');
        for (let line of lines) {
            if (line.includes('在读')) {
                reads = line;
                break;
            }
        }

        let introNode = item.querySelector('.intro, .abstract, .desc');
        let intro = introNode ? introNode.innerText.trim() : "暂无简介";

        results.push({
            title: title,
            author: author,
            reads: reads,
            intro: intro,
            cover: cover,
            url: item.querySelector('a[href^="/page/"]').getAttribute('href')
        });
    }
    return results;
}
"""


def repo_root():
    return os.path.dirname(os.path.abspath(__file__))


def channel_paths(channel: dict, date_str: str):
    data_dir = os.path.join(repo_root(), channel["data_dir"])
    os.makedirs(data_dir, exist_ok=True)
    output_file = os.path.join(data_dir, channel["snapshot_template"].format(date=date_str))
    state_file = os.path.join(data_dir, f"task_state_{date_str}.json")
    return data_dir, output_file, state_file


def load_progress(output_file: str, state_file: str):
    completed_cats = []
    all_categories = []
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            try:
                completed_cats = json.load(f).get("completed", [])
            except Exception:
                pass
    if os.path.exists(output_file) and completed_cats:
        with open(output_file, "r", encoding="utf-8") as f:
            try:
                all_categories = json.load(f).get("categories", [])
            except Exception:
                pass
    return completed_cats, all_categories


def save_progress(output_file: str, state_file: str, all_categories: list, completed_cats: list):
    snapshot = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "categories": all_categories,
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump({"completed": completed_cats}, f, ensure_ascii=False)


def launch_browser(playwright):
    if os.environ.get("GITHUB_ACTIONS"):
        return playwright.chromium.launch(headless=True)
    return playwright.chromium.launch(headless=True, channel="chrome")


def new_page(browser):
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    return context, context.new_page()


def extract_categories(page, href_prefix: str):
    return page.evaluate(
        """
        (prefix) => Array.from(document.querySelectorAll('a'))
            .filter(a => a.getAttribute('href') && a.getAttribute('href').includes(prefix))
            .map(a => ({
                name: a.innerText.trim(),
                href: a.getAttribute('href')
            }))
            .filter(item => item.name && item.href)
        """,
        href_prefix,
    )


def normalize_books(books_data, limit: int):
    category_books = []
    for b in books_data[:limit]:
        title = decode_text(b.get("title", ""))
        author = decode_text(b.get("author", ""))
        reads_raw = decode_text(b.get("reads", ""))
        intro = decode_text(b.get("intro", "")).replace("\\n", " ")
        cover = b.get("cover", "")

        if "在读" in reads_raw:
            parts = reads_raw.split("在读")
            cleaned_reads = parts[1].replace(":", "").replace("：", "").strip() if len(parts) > 1 else reads_raw
        else:
            cleaned_reads = reads_raw

        category_books.append({
            "title": title,
            "author": author,
            "reads": cleaned_reads,
            "intro": intro,
            "cover": cover,
            "url": "https://fanqienovel.com" + b.get("url", ""),
        })
    return category_books


def scrape_source(page, source: dict, completed_cats: list, all_categories: list,
                  output_file: str, state_file: str, limit: int, sleep_sec: int):
    init_url = source["init_url"]
    href_prefix = source["href_prefix"]
    name_prefix = source.get("name_prefix", "")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 正在初始化并访问基础榜单页：{init_url}")
    page.goto(init_url, wait_until="load", timeout=15000)
    page.wait_for_selector('a[href^="/page/"]', timeout=5000)

    categories = extract_categories(page, href_prefix)
    print(f"✅ 成功提取到 {len(categories)} 个分类标签（前缀 {href_prefix}）")

    for cat in categories:
        raw_name = cat["name"]
        cat_name = f"{name_prefix}{raw_name}" if name_prefix else raw_name
        cat_href = cat["href"]

        if cat_name in completed_cats:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏭️ 跳过今日已经完成抓取的类别：{cat_name}")
            continue

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 模拟点击执行类别切换 -> {cat_name}")
        try:
            page.locator(f"a[href='{cat_href}']").first.click()
            time.sleep(2)
            page.wait_for_selector('a[href^="/page/"]', timeout=5000)
        except Exception as e:
            print(f"切换分类出错或加载超时 {cat_name}: {e}")

        for _ in range(3):
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            time.sleep(1.5)

        try:
            books_data = page.evaluate(EXTRACT_JS)
        except Exception as e:
            print(f"执行JS抽取失败 {cat_name}: {e}")
            books_data = []

        category_books = normalize_books(books_data, limit)
        all_categories.append({
            "name": cat_name,
            "books": category_books,
        })
        completed_cats.append(cat_name)
        save_progress(output_file, state_file, all_categories, completed_cats)
        print(f"成功抓取 {cat_name} 类别的前 {len(category_books)} 本书，且进度已存档。等待 {sleep_sec} 秒防拦截...")
        time.sleep(sleep_sec)

    return completed_cats, all_categories


def run_channel(channel_id: str, limit=30, sleep_sec=5):
    channel = get_channel(channel_id)
    date_str = datetime.now().strftime("%Y%m%d")
    _, output_file, state_file = channel_paths(channel, date_str)
    completed_cats, all_categories = load_progress(output_file, state_file)

    print(f"\n===== 开始抓取频道：{channel['name']} {channel['rank_label']} =====")
    if channel.get("hint"):
        print(f"ℹ️  {channel['hint']}")

    with sync_playwright() as p:
        browser = launch_browser(p)
        context, page = new_page(browser)
        try:
            for source in channel["sources"]:
                completed_cats, all_categories = scrape_source(
                    page, source, completed_cats, all_categories,
                    output_file, state_file, limit, sleep_sec,
                )
        finally:
            context.close()
            browser.close()

    print(f"✅ {channel['name']} 当日任务完毕。数据源：{output_file}")
    return output_file


def run_scraper(limit=30, sleep_sec=5, channel_ids=None):
    ids = channel_ids or list(CHANNEL_ORDER)
    outputs = []
    for channel_id in ids:
        outputs.append(run_channel(channel_id, limit=limit, sleep_sec=sleep_sec))
    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="抓取番茄女频 / 男频 / 听书榜单")
    parser.add_argument(
        "--channel",
        default="all",
        help="要抓取的频道：female,male,audio 或 all",
    )
    parser.add_argument("--limit", type=int, default=30, help="每个分类抓取的书籍数量")
    parser.add_argument("--sleep", type=int, default=5, help="分类切换间隔秒数")
    args = parser.parse_args()

    channels = parse_channel_ids(args.channel)
    print("开始执行番茄风向标抓取计划，频道：", "、".join(channels))
    run_scraper(limit=args.limit, sleep_sec=args.sleep, channel_ids=channels)
