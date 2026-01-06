"""
消息模块 / Message Module
定义消息结构和消息处理 / Define message structure and handling
"""

import time
import uuid
from datetime import datetime


class Message:
    """
    消息类 / Message Class
    表示系统中的一条推送消息 / Represents a push message in the system
    """
    
    def __init__(self, content, msg_type='text', priority=1, target=None):
        """
        初始化消息 / Initialize message
        
        参数 / Args:
            content: 消息内容 / Message content
            msg_type: 消息类型 / Message type (text, json, binary)
            priority: 优先级 / Priority (1-5, 5 is highest)
            target: 目标订阅者 / Target subscriber (None for broadcast)
        """
        # 验证优先级 / Validate priority
        if not isinstance(priority, int) or priority < 1 or priority > 5:
            priority = 1
            
        # 验证消息类型 / Validate message type
        if msg_type not in ['text', 'json', 'binary']:
            msg_type = 'text'
            
        self.id = str(uuid.uuid4())
        self.content = content
        self.msg_type = msg_type
        self.priority = priority
        self.target = target
        self.timestamp = datetime.now().isoformat()
        self.created_at = time.time()
        self.status = 'pending'  # pending, sent, failed
        
    def to_dict(self):
        """转换为字典 / Convert to dictionary"""
        return {
            'id': self.id,
            'content': self.content,
            'type': self.msg_type,
            'priority': self.priority,
            'target': self.target,
            'timestamp': self.timestamp,
            'status': self.status
        }
    
    def __repr__(self):
        return f"Message(id={self.id}, type={self.msg_type}, priority={self.priority})"


class MessageQueue:
    """
    消息队列类 / Message Queue Class
    管理待推送的消息 / Manage pending messages
    """
    
    def __init__(self, max_size=1000):
        """
        初始化消息队列 / Initialize message queue
        
        参数 / Args:
            max_size: 队列最大容量 / Maximum queue capacity
        """
        self.max_size = max_size
        self.queue = []
        
    def add(self, message):
        """
        添加消息到队列 / Add message to queue
        
        参数 / Args:
            message: Message对象 / Message object
            
        返回 / Returns:
            bool: 是否成功添加 / Whether successfully added
        """
        if len(self.queue) >= self.max_size:
            # 移除最旧的低优先级消息 / Remove oldest low-priority message
            self._remove_lowest_priority()
            
        self.queue.append(message)
        # 按优先级排序 / Sort by priority
        self.queue.sort(key=lambda x: (-x.priority, x.created_at))
        return True
        
    def get_next(self):
        """
        获取下一条消息 / Get next message
        
        返回 / Returns:
            Message或None / Message or None
        """
        if self.queue:
            return self.queue.pop(0)
        return None
        
    def get_for_subscriber(self, subscriber_id):
        """
        获取特定订阅者的消息 / Get messages for specific subscriber
        
        参数 / Args:
            subscriber_id: 订阅者ID / Subscriber ID
            
        返回 / Returns:
            list: 消息列表 / List of messages
        """
        messages = []
        remaining = []
        
        for msg in self.queue:
            if msg.target is None or msg.target == subscriber_id:
                messages.append(msg)
            else:
                remaining.append(msg)
                
        self.queue = remaining
        return messages
        
    def _remove_lowest_priority(self):
        """移除最低优先级的消息 / Remove lowest priority message"""
        if self.queue:
            self.queue.sort(key=lambda x: (x.priority, -x.created_at))
            self.queue.pop(0)
            
    def size(self):
        """返回队列大小 / Return queue size"""
        return len(self.queue)
        
    def clear(self):
        """清空队列 / Clear queue"""
        self.queue.clear()
