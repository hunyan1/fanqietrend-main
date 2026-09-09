"""番茄风向标频道配置：女频新书 / 男频新书 / 听书热播。

听书说明：番茄网页排行榜只有「阅读榜 / 新书榜 × 男频 / 女频」，
没有独立听书榜。听书内容与小说同源（TTS / 有声），本项目用
男女频阅读榜作为听书热播信号。
"""

BASE_URL = "https://fanqienovel.com"

FEMALE_GENRE_GROUPS = [
    {"name": "古风言情", "categories": ["古风世情", "古言脑洞", "宫斗宅斗", "种田"]},
    {"name": "现代言情", "categories": ["现言脑洞", "豪门总裁", "职场婚恋", "青春甜宠"]},
    {"name": "幻想言情", "categories": ["玄幻言情", "科幻末世", "悬疑脑洞", "女频悬疑"]},
    {"name": "快穿衍生", "categories": ["快穿", "女频衍生"]},
    {"name": "年代民国", "categories": ["年代", "民国言情"]},
    {"name": "娱乐星光", "categories": ["星光璀璨"]},
    {"name": "游戏体育", "categories": ["游戏体育"]},
]

MALE_GENRE_GROUPS = [
    {"name": "都市现实", "categories": ["都市日常", "都市修真", "都市高武", "都市种田", "都市脑洞", "战神赘婿"]},
    {"name": "玄幻仙侠", "categories": ["西方奇幻", "东方仙侠", "传统玄幻", "玄幻脑洞"]},
    {"name": "历史军事", "categories": ["历史古代", "历史脑洞", "抗战谍战"]},
    {"name": "脑洞悬疑", "categories": ["悬疑脑洞", "悬疑灵异"]},
    {"name": "科幻游戏", "categories": ["科幻末世", "游戏体育"]},
    {"name": "衍生同人", "categories": ["动漫衍生", "男频衍生"]},
]

FEMALE_KEYWORDS = [
    "重生", "穿书", "快穿", "系统", "空间", "团宠", "萌宝", "幼崽", "女配", "炮灰",
    "反派", "权臣", "宅斗", "宫斗", "和离", "替嫁", "逃荒", "种田", "美食", "经商",
    "年代", "七零", "八零", "军婚", "豪门", "总裁", "真假千金", "先婚后爱", "追妻",
    "甜宠", "双洁", "强制爱", "无CP", "末世", "废土", "天灾", "囤货", "异能",
    "国运", "星际", "修仙", "玄学", "无限流", "悬疑", "直播", "综艺", "娱乐圈",
    "校园", "暗恋", "青梅竹马", "民国", "兽世", "远古", "基建",
]

MALE_KEYWORDS = [
    "系统", "重生", "穿越", "无敌", "签到", "赘婿", "战神", "神医", "兵王", "都市",
    "修真", "仙侠", "玄幻", "末日", "末世", "高武", "种田", "囤货", "异能", "灵气复苏",
    "诸天", "无限流", "克苏鲁", "悬疑", "谍战", "抗战", "历史", "皇子", "权谋",
    "朝堂", "基建", "工业", "科技", "游戏", "电竞", "直播", "娱乐圈", "脑洞",
    "反派", "龙傲天", "退婚", "觉醒", "血脉", "宗门", "师尊", "丹药", "炼器",
    "灵根", "气运", "国运", "穿书", "快穿", "空间", "签到流", "模拟器", "御兽",
    "末日囤货", "废土", "机甲", "星际", "赛博", "灵异", "摸鱼",
]


def _prefix_groups(groups, prefix):
    return [
        {
            "name": f"{prefix}{group['name']}",
            "categories": [f"{prefix}{name}" for name in group["categories"]],
        }
        for group in groups
    ]


AUDIO_GENRE_GROUPS = _prefix_groups(MALE_GENRE_GROUPS, "男频 · ") + _prefix_groups(
    FEMALE_GENRE_GROUPS, "女频 · "
)

AUDIO_KEYWORDS = list(dict.fromkeys(MALE_KEYWORDS + FEMALE_KEYWORDS))

CHANNELS = {
    "female": {
        "id": "female",
        "name": "女频",
        "subtitle": "女频新书榜追踪",
        "rank_label": "新书榜",
        "audience": "读者",
        "prompt_scope": "番茄小说女频新书榜",
        "data_dir": "data",
        "snapshot_glob": "fanqie_female_new_ranks_*.json",
        "snapshot_template": "fanqie_female_new_ranks_{date}.json",
        "api_dir": "api/lastest",
        "api_index": "api/lastest.json",
        "genre_groups": FEMALE_GENRE_GROUPS,
        "keywords": FEMALE_KEYWORDS,
        "sources": [
            {
                "init_url": f"{BASE_URL}/rank/0_1_1139",
                "href_prefix": "/rank/0_1_",
                "name_prefix": "",
            }
        ],
    },
    "male": {
        "id": "male",
        "name": "男频",
        "subtitle": "男频新书榜追踪",
        "rank_label": "新书榜",
        "audience": "读者",
        "prompt_scope": "番茄小说男频新书榜",
        "data_dir": "data/male",
        "snapshot_glob": "fanqie_male_new_ranks_*.json",
        "snapshot_template": "fanqie_male_new_ranks_{date}.json",
        "api_dir": "api/male/lastest",
        "api_index": "api/male/lastest.json",
        "genre_groups": MALE_GENRE_GROUPS,
        "keywords": MALE_KEYWORDS,
        "sources": [
            {
                "init_url": f"{BASE_URL}/rank/1_1_1141",
                "href_prefix": "/rank/1_1_",
                "name_prefix": "",
            }
        ],
    },
    "audio": {
        "id": "audio",
        "name": "听书",
        "subtitle": "听书热播榜追踪",
        "rank_label": "阅读热榜",
        "audience": "听众",
        "prompt_scope": "番茄小说听书热播榜（网页阅读榜，听书与在读同源）",
        "hint": "番茄网页暂无独立听书榜，本频道抓取男女频阅读榜作为热播信号。",
        "data_dir": "data/audio",
        "snapshot_glob": "fanqie_audio_ranks_*.json",
        "snapshot_template": "fanqie_audio_ranks_{date}.json",
        "api_dir": "api/audio/lastest",
        "api_index": "api/audio/lastest.json",
        "genre_groups": AUDIO_GENRE_GROUPS,
        "keywords": AUDIO_KEYWORDS,
        "sources": [
            {
                "init_url": f"{BASE_URL}/rank/1_2_1141",
                "href_prefix": "/rank/1_2_",
                "name_prefix": "男频 · ",
            },
            {
                "init_url": f"{BASE_URL}/rank/0_2_1139",
                "href_prefix": "/rank/0_2_",
                "name_prefix": "女频 · ",
            },
        ],
    },
}

CHANNEL_ORDER = ["female", "male", "audio"]


def get_channel(channel_id: str) -> dict:
    if channel_id not in CHANNELS:
        raise KeyError(f"未知频道: {channel_id}")
    return CHANNELS[channel_id]


def parse_channel_ids(raw: str) -> list:
    """解析 CLI 的频道参数，默认全部。"""
    if not raw or raw.strip() in ("all", "*"):
        return list(CHANNEL_ORDER)
    ids = []
    for item in raw.split(","):
        cid = item.strip()
        if not cid:
            continue
        if cid not in CHANNELS:
            raise ValueError(f"未知频道: {cid}，可选: {', '.join(CHANNEL_ORDER)}")
        if cid not in ids:
            ids.append(cid)
    return ids or list(CHANNEL_ORDER)
