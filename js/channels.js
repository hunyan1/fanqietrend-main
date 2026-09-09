window.FanqieChannels = (() => {
    const femaleGenreGroups = [
        { name: '古风言情', categories: ['古风世情', '古言脑洞', '宫斗宅斗', '种田'] },
        { name: '现代言情', categories: ['现言脑洞', '豪门总裁', '职场婚恋', '青春甜宠'] },
        { name: '幻想言情', categories: ['玄幻言情', '科幻末世', '悬疑脑洞', '女频悬疑'] },
        { name: '快穿衍生', categories: ['快穿', '女频衍生'] },
        { name: '年代民国', categories: ['年代', '民国言情'] },
        { name: '娱乐星光', categories: ['星光璀璨'] },
        { name: '游戏体育', categories: ['游戏体育'] },
    ];

    const maleGenreGroups = [
        { name: '都市现实', categories: ['都市日常', '都市修真', '都市高武', '都市种田', '都市脑洞', '战神赘婿'] },
        { name: '玄幻仙侠', categories: ['西方奇幻', '东方仙侠', '传统玄幻', '玄幻脑洞'] },
        { name: '历史军事', categories: ['历史古代', '历史脑洞', '抗战谍战'] },
        { name: '脑洞悬疑', categories: ['悬疑脑洞', '悬疑灵异'] },
        { name: '科幻游戏', categories: ['科幻末世', '游戏体育'] },
        { name: '衍生同人', categories: ['动漫衍生', '男频衍生'] },
    ];

    const prefixGroups = (groups, prefix) => groups.map(group => ({
        name: `${prefix}${group.name}`,
        categories: group.categories.map(name => `${prefix}${name}`),
    }));

    const femaleKeywords = [
        '重生', '穿书', '快穿', '系统', '空间', '团宠', '萌宝', '幼崽', '女配', '炮灰',
        '反派', '权臣', '宅斗', '宫斗', '和离', '替嫁', '逃荒', '种田', '美食', '经商',
        '年代', '七零', '八零', '军婚', '豪门', '总裁', '真假千金', '先婚后爱', '追妻',
        '甜宠', '双洁', '强制爱', '无CP', '末世', '废土', '天灾', '囤货', '异能',
        '国运', '星际', '修仙', '玄学', '无限流', '悬疑', '直播', '综艺', '娱乐圈',
        '校园', '暗恋', '青梅竹马', '民国', '兽世', '远古', '基建',
    ];

    const maleKeywords = [
        '系统', '重生', '穿越', '无敌', '签到', '赘婿', '战神', '神医', '兵王', '都市',
        '修真', '仙侠', '玄幻', '末日', '末世', '高武', '种田', '囤货', '异能', '灵气复苏',
        '诸天', '无限流', '克苏鲁', '悬疑', '谍战', '抗战', '历史', '皇子', '权谋',
        '朝堂', '基建', '工业', '科技', '游戏', '电竞', '直播', '娱乐圈', '脑洞',
        '反派', '龙傲天', '退婚', '觉醒', '血脉', '宗门', '师尊', '丹药', '炼器',
        '灵根', '气运', '国运', '穿书', '快穿', '空间', '签到流', '模拟器', '御兽',
        '末日囤货', '废土', '机甲', '星际', '赛博', '灵异', '摸鱼',
    ];

    const list = [
        {
            id: 'female',
            name: '女频',
            subtitle: '女频新书榜追踪',
            rankLabel: '新书榜',
            dataDir: 'data',
            snapshotPrefix: 'fanqie_female_new_ranks_',
            latestFile: 'data/latest_ranks.json',
            datesFile: 'data/dates.json',
            marketFile: 'data/market_summary.json',
            trendsDir: 'data/trends',
            apiIndex: 'api/lastest.json',
            apiAll: 'api/lastest/all.json',
            genreGroups: femaleGenreGroups,
            keywords: femaleKeywords,
        },
        {
            id: 'male',
            name: '男频',
            subtitle: '男频新书榜追踪',
            rankLabel: '新书榜',
            dataDir: 'data/male',
            snapshotPrefix: 'fanqie_male_new_ranks_',
            latestFile: 'data/male/latest_ranks.json',
            datesFile: 'data/male/dates.json',
            marketFile: 'data/male/market_summary.json',
            trendsDir: 'data/male/trends',
            apiIndex: 'api/male/lastest.json',
            apiAll: 'api/male/lastest/all.json',
            genreGroups: maleGenreGroups,
            keywords: maleKeywords,
        },
        {
            id: 'audio',
            name: '听书',
            subtitle: '听书热播榜追踪',
            rankLabel: '阅读热榜',
            hint: '番茄网页暂无独立听书榜，本频道抓取男女频阅读榜作为热播信号。',
            dataDir: 'data/audio',
            snapshotPrefix: 'fanqie_audio_ranks_',
            latestFile: 'data/audio/latest_ranks.json',
            datesFile: 'data/audio/dates.json',
            marketFile: 'data/audio/market_summary.json',
            trendsDir: 'data/audio/trends',
            apiIndex: 'api/audio/lastest.json',
            apiAll: 'api/audio/lastest/all.json',
            genreGroups: prefixGroups(maleGenreGroups, '男频 · ').concat(prefixGroups(femaleGenreGroups, '女频 · ')),
            keywords: Array.from(new Set(maleKeywords.concat(femaleKeywords))),
        },
    ];

    const byId = Object.fromEntries(list.map(item => [item.id, item]));

    function get(id) {
        return byId[id] || null;
    }

    function current() {
        const params = new URLSearchParams(window.location.search);
        const fromUrl = params.get('ch');
        const fromStore = window.localStorage.getItem('fanqie_channel');
        const channel = get(fromUrl) || get(fromStore) || get('female');
        window.localStorage.setItem('fanqie_channel', channel.id);
        return channel;
    }

    function currentPage() {
        const file = (window.location.pathname.split('/').pop() || '').toLowerCase();
        if (file === 'trend.html' || file === 'book.html' || file === 'index.html') {
            return file;
        }
        return 'index.html';
    }

    function withChannel(href, channelId) {
        const id = channelId || current().id;
        const url = new URL(href, window.location.href);
        url.searchParams.set('ch', id);
        const file = (url.pathname.split('/').pop() || '').toLowerCase();
        const page = (file === 'trend.html' || file === 'book.html' || file === 'index.html')
            ? file
            : currentPage();
        return `${page}${url.search}${url.hash}`;
    }

    function snapshotUrl(channel, date) {
        return `${channel.dataDir}/${channel.snapshotPrefix}${String(date).replace(/-/g, '')}.json`;
    }

    function renderSwitch(container) {
        if (!container) return;
        const active = current();
        container.innerHTML = list.map(channel => `
            <a class="channel-btn${channel.id === active.id ? ' active' : ''}" href="${withChannel(currentPage(), channel.id)}">${channel.name}</a>
        `).join('');
    }

    function bindKeepChannelLinks() {
        const channel = current();
        document.querySelectorAll('[data-keep-channel]').forEach(link => {
            const href = link.getAttribute('href');
            if (!href || href.startsWith('http')) return;
            link.setAttribute('href', withChannel(href, channel.id));
        });
    }

    function applyPageMeta() {
        const channel = current();
        const subtitle = document.getElementById('sidebar-subtitle');
        if (subtitle) subtitle.textContent = channel.subtitle;
        const hint = document.getElementById('channel-hint');
        if (hint) {
            hint.textContent = channel.hint || '';
            hint.hidden = !channel.hint;
        }
        const page = currentPage();
        if (page === 'trend.html') {
            document.title = `类型风向标 · 番茄${channel.name}${channel.rankLabel}`;
        } else if (page === 'book.html') {
            document.title = `作品详情 · 番茄${channel.name}${channel.rankLabel}`;
        } else {
            document.title = `番茄${channel.name}${channel.rankLabel} · 风向标 | 每日趋势追踪`;
        }
        bindKeepChannelLinks();
        renderSwitch(document.getElementById('channel-switch'));
        renderSwitch(document.getElementById('channel-switch-top'));
        return channel;
    }

    return {
        list,
        get,
        current,
        withChannel,
        snapshotUrl,
        renderSwitch,
        bindKeepChannelLinks,
        applyPageMeta,
    };
})();
