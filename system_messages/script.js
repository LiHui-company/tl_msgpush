// 消息配置
const commonLogicText = '点击可以跳转到相应的消息列表页，点击返回则返回到消息首页。最多展示20个字，超出...显示。';

const messageConfig = {
    sys_notice: {
        title: '系统通知',
        systemText: '系统维护通知：我们将于今晚凌晨2:00进行服务器升级，预计耗时2小时，请提前保存数据。',
        inAppText: '系统维护通知：我们将于今晚凌晨2:00进行服务器升级，预计耗时2小时，请提前保存数据。',
        icon: '📢',
        listData: [
            { user: '系统管理员', content: '系统维护通知：我们将于今晚凌晨2:00进行服务器升级，预计耗时2小时。', time: '刚刚' },
            { user: '系统管理员', content: '关于隐私政策更新的通知。', time: '3天前' },
            { user: '系统管理员', content: '版本 v2.0.1 更新日志。', time: '1周前' }
        ],
        logic: {
            system: commonLogicText,
            inapp: commonLogicText
        }
    },
    activity: {
        title: '活动通知',
        systemText: '双11大促开启！全场5折起，点击查看详情，错过再等一年！',
        inAppText: '双11大促开启！全场5折起，点击查看详情，错过再等一年！',
        icon: '🎉',
        listData: [
            { user: '活动助手', content: '双11大促开启！全场5折起，点击查看详情。', time: '刚刚' },
            { user: '活动助手', content: '周末狂欢，限时秒杀活动即将开始。', time: '昨天' },
            { user: '活动助手', content: '邀请好友赢取好礼，快来参与吧。', time: '2天前' }
        ],
        logic: {
            system: commonLogicText,
            inapp: commonLogicText
        }
    },
    security: {
        title: '安全提醒',
        systemText: '您的账户于 10:23 在新设备登录，如非本人操作请立即修改密码。',
        inAppText: '您的账户于 10:23 在新设备登录，如非本人操作请立即修改密码。',
        icon: '🛡️',
        listData: [
            { user: '安全中心', content: '您的账户于 10:23 在新设备登录 (IP: 192.168.1.1)。', time: '刚刚' },
            { user: '安全中心', content: '您的密码已成功修改。', time: '1个月前' }
        ],
        logic: {
            system: commonLogicText,
            inapp: commonLogicText
        }
    },
    account: {
        title: '账户通知',
        systemText: '您的会员权益即将到期，请及时续费以保留特权。',
        inAppText: '您的会员权益即将到期，请及时续费以保留特权。',
        icon: '💳',
        listData: [
            { user: '会员中心', content: '您的会员权益即将到期，请及时续费。', time: '刚刚' },
            { user: '积分助手', content: '您获得了 100 积分，快去兑换好礼吧。', time: '昨天' },
            { user: '成长体系', content: '恭喜您升级为 Lv5 用户！', time: '1周前' }
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
    if (text.length > maxLength) {
        return text.substring(0, maxLength) + '...';
    }
    return text;
}

function showSystemNotification(text) {
    const notif = document.getElementById('sys-notif');
    const content = document.getElementById('sys-notif-text');
    
    // 系统通知始终显示完整内容（由 config 控制格式）
    content.innerText = truncateText(text);
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

    content.innerText = truncateText(text);
    
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
