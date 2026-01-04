// 消息配置
const chatConfig = {
    user: '慧慧',
    content: '今晚有空出来吃饭吗？就在公司附近那家新开的日料店，听说味道不错。',
    shortContent: '今晚有空出来吃饭吗？就在...',
    chatHistory: [
        { type: 'sent', content: '上次说的那个项目方案我发你邮箱了。' },
        { type: 'received', content: '好的，我稍后看下。' },
        { type: 'received', content: '今晚有空出来吃饭吗？就在公司附近那家新开的日料店，听说味道不错。' }
    ]
};

let currentScenario = 'system';
let messageTimestamps = []; // 用于频控

// 初始化
window.onload = function() {
    switchScenario('system');
};

function switchScenario(scenario) {
    currentScenario = scenario;
    closeChat(true); // 切换场景时关闭详情页，并重置视图
    
    // 切换模拟器显示
    document.getElementById('scenario-system').style.display = scenario === 'system' ? 'flex' : 'none';
    document.getElementById('scenario-inapp').style.display = scenario === 'inapp' ? 'flex' : 'none';

    // 高亮当前场景块
    document.querySelectorAll('.scenario-block').forEach(block => block.classList.remove('active'));
    document.getElementById(`block-${scenario}`).classList.add('active');

    // 重置显示状态
    hideAllNotifications();
    
    // 更新逻辑说明
    document.getElementById('logic-title').innerText = scenario === 'system' ? '场景：未打开App' : '场景：打开App未在当前页面';
    document.getElementById('logic-content').innerText = scenario === 'system' 
        ? '当前模拟用户手机处于锁屏或桌面状态。收到消息时展示完整内容的系统通知。点击通知进入聊天详情页，返回时跳转到消息列表页。'
        : '当前模拟用户正在使用App。系统会监测5秒内的消息频率：\n1. <3条：展示单条消息横幅。\n2. ≥3条：展示合并消息横幅 "你收到 n 条未读消息"。\n点击通知进入聊天详情页，返回时关闭详情页回到原页面。';
    
    // 清除频控记录
    messageTimestamps = [];
}

function triggerMessage(scenario) {
    // 如果点击的按钮不在当前场景，先切换场景
    if (currentScenario !== scenario) {
        switchScenario(scenario);
    }

    const now = Date.now();

    if (scenario === 'system') {
        showSystemNotification(`${chatConfig.user}：${chatConfig.content}`);
        document.getElementById('logic-content').innerText = '收到一条 Push（不折叠）。\n内容展示：用户昵称：消息内容（最多20字截断）。\n点击卡片 -> 进入聊天详情页。\n点击返回 -> 跳转到消息列表页面。';
    } else {
        // In-App 频控逻辑
        // 清理5秒前的时间戳
        messageTimestamps = messageTimestamps.filter(t => now - t <= 5000);
        // 添加当前时间戳
        messageTimestamps.push(now);
        
        const count = messageTimestamps.length;
        
        if (count < 3) {
            // 单条推送
            showInAppNotification(`${chatConfig.user}：${chatConfig.shortContent}`);
            document.getElementById('logic-content').innerText = `5秒内消息数：${count} (<3)\n展示单条推送样式。\n内容：${chatConfig.user}：${chatConfig.shortContent}`;
        } else {
            // 合并推送
            showInAppNotification(`你收到 ${count} 条未读消息`);
            document.getElementById('logic-content').innerText = `5秒内消息数：${count} (≥3)\n展示合并推送样式。\n内容：你收到 ${count} 条未读消息`;
        }
    }
}

function showSystemNotification(text) {
    const notif = document.getElementById('sys-notif');
    const content = document.getElementById('sys-notif-text');
    
    // 简单截断处理用于演示
    if (text.length > 20) {
        text = text.substring(0, 20) + '...';
    }

    content.innerText = text;
    notif.style.display = 'none'; // 重置动画
    setTimeout(() => {
        notif.style.display = 'block';
    }, 10);
}

function showInAppNotification(text) {
    const notif = document.getElementById('inapp-notif');
    const content = document.getElementById('inapp-notif-text');

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

function openChat(element) {
    // 添加消失动画
    if (element) {
        element.classList.add('anim-disappear');
    }

    // 等待动画结束后显示详情页
    setTimeout(() => {
        const chatView = document.getElementById('chat-detail-view');
        const chatContent = document.getElementById('chat-content');
        
        // 生成聊天内容
        let html = '';
        chatConfig.chatHistory.forEach(msg => {
            html += `<div class="chat-bubble ${msg.type}">${msg.content}</div>`;
        });
        chatContent.innerHTML = html;

        chatView.style.display = 'flex';
        
        // 动画结束后隐藏通知元素并移除动画类
        if (element) {
            element.style.display = 'none';
            element.classList.remove('anim-disappear');
        }
    }, 300);
}

function closeChat(reset = false) {
    document.getElementById('chat-detail-view').style.display = 'none';
    
    if (!reset) {
        if (currentScenario === 'system') {
            // 场景1：返回到消息列表页面
            document.getElementById('message-index-view').style.display = 'block';
            document.getElementById('scenario-system').style.display = 'none';
        } else {
            // 场景2：返回到之前App页面 (即露出底部的 tlsq.jpg)
            // 不需要做额外操作，因为 chat-detail-view 隐藏后自然露出下面的 scenario-inapp
        }
    }
}
