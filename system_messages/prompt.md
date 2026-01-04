# System Messages Page Prompt

**目标**：构建 `system_messages/index.html` 页面，结构与交互逻辑完全复用 `interactive_messages/index.html`，仅针对系统消息类型进行适配。

**UI 结构**：
1.  **左侧模拟器**：
    *   适配 Xiaomi 15 Pro 尺寸 (20:9)。
    *   包含 "未打开 App" (System Push) 和 "打开 App" (In-App) 两种场景视图。
    *   背景图复用：
        *   未打开 App：`../interactive_messages/assets/desktop.jpg`
        *   消息首页：`../interactive_messages/assets/msgidx.jpg`
        *   打开 App：`../interactive_messages/assets/tlsq.jpg`
2.  **右侧控制面板**：
    *   垂直分为两个场景区块。
    *   **区块 1：未打开 App 时**
        *   子按钮：系统通知、活动通知、安全提醒、账户通知。
    *   **区块 2：打开 App 未在当前页面**
        *   子按钮：系统通知、活动通知、安全提醒、账户通知。

**消息类型定义**：
1.  **系统通知** (System Notification)
    *   示例内容："系统维护通知：我们将于今晚凌晨2:00进行服务器升级..."
2.  **活动通知** (Activity Notification)
    *   示例内容："双11大促开启！全场5折起，点击查看详情..."
3.  **安全提醒** (Security Alert)
    *   示例内容："您的账户于 10:23 在新设备登录，如非本人操作请立即修改密码。"
4.  **账户通知** (Account Notification)
    *   示例内容："您的会员权益即将到期，请及时续费以保留特权。"

**交互逻辑**：
*   **通用逻辑**：
    *   点击控制面板按钮 -> 模拟器显示对应通知。
    *   点击通知 -> 通知消失动画 -> 进入列表页。
    *   列表页点击返回 -> 返回消息首页 (System场景) 或 关闭列表 (In-App场景)。
*   **展示样式**：
    *   **未打开 App**：显示完整系统通知样式 (Logo + 标题 + 时间 + 内容)。
    *   **打开 App**：显示顶部横幅 (Banner)。
        *   根据 `interactive_messages` 的最新规则，In-App 场景下通常简化 Header。在此页面中，为了保持一致性，我们可以设定：
            *   所有系统消息在 In-App 场景下**均不显示**推栏标题和时间，仅显示内容。
*   **内容格式**：
    *   支持换行 (`\n`)。
    *   过长文本截断 (20字 + `...`)。

**资源路径**：
*   由于本目录下没有 `assets` 文件夹，所有图片资源需引用 `../interactive_messages/assets/` 路径。

**代码结构要求**：
*   **JS 分离**：所有交互逻辑代码必须从 HTML 文件中剥离，存放在同级目录下的 `script.js` 文件中。
*   **引用**：在 `index.html` 底部通过 `<script src="script.js"></script>` 引入。
