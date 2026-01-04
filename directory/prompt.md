# Directory Page Prompt

**目标**：创建一个功能导航目录页面 `directory/index.html`，作为各个功能模块的入口。

**页面结构**：
1.  **头部 (Header)**：显示项目名称 "TL_MSPUSH 目录"。
2.  **导航 (Navigation)**：提供跳转到 "封面" 和当前 "目录" 的链接。
3.  **内容区 (Container)**：
    *   标题：显示 "功能导航"。
    *   **菜单网格 (Menu Grid)**：使用网格布局展示功能入口。

**功能入口列表**：
1.  **聊天消息**：
    *   链接：`../chat_messages/index.html`
    *   图标/文本：💬 聊天消息
2.  **互动消息**：
    *   链接：`../interactive_messages/index.html`
    *   图标/文本：🔔 互动消息
3.  **系统消息**：
    *   链接：`../system_messages/index.html`
    *   图标/文本：⚙️ 系统消息
4.  **订阅号消息**：
    *   链接：`../subscription_messages/index.html`
    *   图标/文本：📰 订阅号消息

**样式要求**：
*   引用通用的 CSS 文件 `../css/style.css`。
*   使用 `.menu-grid` 和 `.menu-item` 类来实现网格布局和按钮样式。
