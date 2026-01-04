// 消息配置
const commonLogicText = '点击可以跳转到相应的评论列表页，点击返回则返回到消息首页。最多展示20个字，超出...显示。图片显示[图片]。';

const messageConfig = {
    comment: {
        title: '评论',
        systemText: '用户A 评论了你\n这篇文章写得真好，非常有深度，受益...',
        inAppText: '用户A 评论了你\n这篇文章写得真好，非常有深度，受益...',
        icon: '💬',
        listData: [
            { user: '用户A', content: '这篇文章写得真好，非常有深度，受益匪浅！[图片]', time: '刚刚' },
            { user: '用户B', content: '赞同楼上观点，期待更多分享。', time: '5分钟前' },
            { user: '用户C', content: '请问这个功能怎么实现呢？', time: '1小时前' },
            { user: '用户D', content: 'mark一下，回头细看。', time: '2小时前' }
        ],
        logic: {
            system: commonLogicText,
            inapp: commonLogicText
        }
    },
    at: {
        title: '@我',
        systemText: '用户B 提到了你\n今天天气晴朗@慧慧',
        inAppText: '用户B 提到了你\n今天天气晴朗@慧慧',
        icon: '@',
        listData: [
            { user: '用户B', content: '在群聊 "技术交流群" 中@了你：大家来看看这个方案。', time: '刚刚' },
            { user: '用户E', content: '在群聊 "项目组" 中@了你：周报记得提交。', time: '30分钟前' },
            { user: '用户F', content: '在评论区@了你：这里是不是写错了？', time: '昨天' }
        ],
        logic: {
            system: commonLogicText,
            inapp: commonLogicText
        }
    },
    like: {
        title: '点赞',
        systemText: '用户C 点赞了你',
        inAppText: '用户C 点赞了你',
        icon: '❤️',
        listData: [
            { user: '用户C', content: '赞了你的动态 "今天天气真不错"。', time: '刚刚' },
            { user: '用户G', content: '赞了你的评论 "确实如此"。', time: '10分钟前' },
            { user: '用户H', content: '赞了你的文章 "前端性能优化指南"。', time: '2小时前' },
            { user: '用户I', content: '赞了你的动态 "周末去爬山"。', time: '昨天' },
            { user: '用户J', content: '赞了你的动态 "周末去爬山"。', time: '昨天' }
        ],
        logic: {
            system: commonLogicText,
            inapp: commonLogicText
        }
    },
    follow: {
        title: '新粉丝',
        systemText: '用户D 关注了你',
        inAppText: '用户D 关注了你',
        icon: '👤',
        listData: [
            { user: '用户D', content: '关注了你，快去看看Ta的主页吧。', time: '刚刚' },
            { user: '用户K', content: '关注了你。', time: '昨天' },
            { user: '用户L', content: '关注了你。', time: '2天前' }
        ],
        logic: {
            system: commonLogicText,
            inapp: commonLogicText
        }
    }
};

let currentScenario = 'system';
let currentMessageType = null;

// 初始化
window.onload = function() {
    switchScenario('system');
};

function switchScenario(scenario) {
    currentScenario = scenario;
    closeList(true); // 切换场景时关闭列表页，并重置视图
    
    // 切换模拟器显示
    document.getElementById('scenario-system').style.display = scenario === 'system' ? 'flex' : 'none';
    document.getElementById('scenario-inapp').style.display = scenario === 'inapp' ? 'flex' : 'none'; // 改为 flex 以支持居中

    // 高亮当前场景块
    document.querySelectorAll('.scenario-block').forEach(block => block.classList.remove('active'));
    document.getElementById(`block-${scenario}`).classList.add('active');

    // 重置显示状态
    hideAllNotifications();
    
    // 更新逻辑说明
    document.getElementById('logic-title').innerText = scenario === 'system' ? '场景：未打开App' : '场景：打开App未在当前页面';
    document.getElementById('logic-content').innerText = scenario === 'system' 
        ? '当前模拟用户手机处于锁屏或桌面状态，App未运行或在后台。此时主要依赖系统级推送通道触达用户。'
        : '当前模拟用户正在使用App浏览其他内容。此时主要依赖App内长连接实时推送，实现轻量级互动。';
    
    // 清除按钮高亮
    document.querySelectorAll('.msg-btn').forEach(btn => btn.classList.remove('active'));
}

function triggerMessage(scenario, type) {
    // 如果点击的按钮不在当前场景，先切换场景
    if (currentScenario !== scenario) {
        switchScenario(scenario);
    }

    currentMessageType = type;
    const config = messageConfig[type];
    
    // 更新逻辑说明
    document.getElementById('logic-title').innerText = `互动类型：${config.title}`;
    document.getElementById('logic-content').innerText = config.logic[scenario];

    // 高亮按钮
    document.querySelectorAll('.msg-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    // 展示对应场景的效果
    if (scenario === 'system') {
        showSystemNotification(config.systemText);
    } else {
        // In-App 场景下，所有类型均不显示 Header
        const showHeader = false;
        showInAppNotification(config.inAppText, config.icon, showHeader);
    }
}

function truncateText(text, maxLength = 20) {
    // 注意：这里的截断逻辑主要用于动态生成的文本，
    // 对于 messageConfig 中已经硬编码的文本，此函数可能不会改变什么，
    // 除非我们传入的是原始长文本。
    // 目前 messageConfig.comment 已经手动截断了。
    if (text.length > maxLength) {
        return text.substring(0, maxLength) + '...';
    }
    return text;
}

function showSystemNotification(text) {
    const notif = document.getElementById('sys-notif');
    const content = document.getElementById('sys-notif-text');
    
    // 系统通知始终显示完整内容（由 config 控制格式）
    content.innerText = text;
    notif.style.display = 'none'; // 重置动画
    setTimeout(() => {
        notif.style.display = 'block';
    }, 10);
}

function showInAppNotification(text, icon, showHeader = false) {
    // 使用顶部横幅样式
    const notif = document.getElementById('inapp-notif');
    const header = document.getElementById('inapp-notif-header');
    const content = document.getElementById('inapp-notif-text');

    // 控制 Header 显示
    header.style.display = showHeader ? 'flex' : 'none';

    content.innerText = text;
    
    notif.style.display = 'none'; // 重置动画
    setTimeout(() => {
        notif.style.display = 'block';
    }, 10);
}

function hideAllNotifications() {
    const sysNotif = document.getElementById('sys-notif');
    const inappNotif = document.getElementById('inapp-notif');
    
    sysNotif.style.display = 'none';
    sysNotif.classList.remove('anim-disappear');
    
    inappNotif.style.display = 'none';
    inappNotif.classList.remove('anim-disappear');

    document.getElementById('message-index-view').style.display = 'none';
}

function openList(element) {
    if (!currentMessageType) return;
    
    // 添加消失动画
    if (element) {
        element.classList.add('anim-disappear');
    }

    // 等待动画结束后显示列表页
    setTimeout(() => {
        const config = messageConfig[currentMessageType];
        const listView = document.getElementById('list-view');
        const listTitle = document.getElementById('list-title');
        const listContent = document.getElementById('list-content');

        listTitle.innerText = config.title;
        
        // 生成列表内容
        let html = '';
        config.listData.forEach(item => {
            html += `
                <div class="list-item">
                    <div class="list-avatar"></div>
                    <div class="list-info">
                        <div class="list-user">${item.user}</div>
                        <div class="list-text">${item.content}</div>
                        <div class="list-time">${item.time}</div>
                    </div>
                </div>
            `;
        });
        listContent.innerHTML = html;

        listView.style.display = 'flex';
        
        // 动画结束后隐藏通知元素并移除动画类，以便下次使用
        if (element) {
            element.style.display = 'none';
            element.classList.remove('anim-disappear');
        }
    }, 300); // 300ms 对应 CSS 动画时长
}

function closeList(reset = false) {
    document.getElementById('list-view').style.display = 'none';
    
    if (!reset && currentScenario === 'system') {
        // 如果是系统通知场景，返回时显示消息首页
        document.getElementById('message-index-view').style.display = 'block';
        // 隐藏系统通知层，避免重叠（虽然 z-index 较低，但为了逻辑清晰）
        document.getElementById('scenario-system').style.display = 'none';
    }
}
