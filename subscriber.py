"""
订阅者模块 / Subscriber Module
管理消息订阅者 / Manage message subscribers
"""

import time
from datetime import datetime


class Subscriber:
    """
    订阅者类 / Subscriber Class
    表示一个消息订阅者/客户端 / Represents a message subscriber/client
    """
    
    def __init__(self, subscriber_id, name=None, tags=None):
        """
        初始化订阅者 / Initialize subscriber
        
        参数 / Args:
            subscriber_id: 订阅者唯一标识 / Unique subscriber ID
            name: 订阅者名称 / Subscriber name
            tags: 订阅标签列表 / Subscription tags list
        """
        self.id = subscriber_id
        self.name = name or subscriber_id
        self.tags = tags or []
        self.connected_at = datetime.now().isoformat()
        self.last_heartbeat = time.time()
        self.is_active = True
        
    def update_heartbeat(self):
        """更新心跳时间 / Update heartbeat time"""
        self.last_heartbeat = time.time()
        
    def is_alive(self, timeout=60):
        """
        检查订阅者是否存活 / Check if subscriber is alive
        
        参数 / Args:
            timeout: 超时时间(秒) / Timeout in seconds
            
        返回 / Returns:
            bool: 是否存活 / Whether alive
        """
        return (time.time() - self.last_heartbeat) < timeout
        
    def to_dict(self):
        """转换为字典 / Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'tags': self.tags,
            'connected_at': self.connected_at,
            'is_active': self.is_active,
            'last_heartbeat': self.last_heartbeat
        }
        
    def __repr__(self):
        return f"Subscriber(id={self.id}, name={self.name}, active={self.is_active})"


class SubscriberManager:
    """
    订阅者管理器 / Subscriber Manager
    管理所有订阅者的注册、注销和状态 / Manage subscriber registration, deregistration and status
    """
    
    def __init__(self, max_subscribers=100):
        """
        初始化订阅者管理器 / Initialize subscriber manager
        
        参数 / Args:
            max_subscribers: 最大订阅者数量 / Maximum number of subscribers
        """
        self.max_subscribers = max_subscribers
        self.subscribers = {}  # {subscriber_id: Subscriber}
        
    def register(self, subscriber_id, name=None, tags=None):
        """
        注册订阅者 / Register subscriber
        
        参数 / Args:
            subscriber_id: 订阅者ID / Subscriber ID
            name: 订阅者名称 / Subscriber name
            tags: 订阅标签 / Subscription tags
            
        返回 / Returns:
            Subscriber或None / Subscriber or None if limit reached
        """
        if len(self.subscribers) >= self.max_subscribers:
            return None
            
        subscriber = Subscriber(subscriber_id, name, tags)
        self.subscribers[subscriber_id] = subscriber
        return subscriber
        
    def unregister(self, subscriber_id):
        """
        注销订阅者 / Unregister subscriber
        
        参数 / Args:
            subscriber_id: 订阅者ID / Subscriber ID
            
        返回 / Returns:
            bool: 是否成功注销 / Whether successfully unregistered
        """
        if subscriber_id in self.subscribers:
            del self.subscribers[subscriber_id]
            return True
        return False
        
    def get(self, subscriber_id):
        """
        获取订阅者 / Get subscriber
        
        参数 / Args:
            subscriber_id: 订阅者ID / Subscriber ID
            
        返回 / Returns:
            Subscriber或None / Subscriber or None
        """
        return self.subscribers.get(subscriber_id)
        
    def get_all(self):
        """
        获取所有订阅者 / Get all subscribers
        
        返回 / Returns:
            list: 订阅者列表 / List of subscribers
        """
        return list(self.subscribers.values())
        
    def get_active(self, timeout=60):
        """
        获取所有活跃订阅者 / Get all active subscribers
        
        参数 / Args:
            timeout: 心跳超时时间(秒) / Heartbeat timeout in seconds
            
        返回 / Returns:
            list: 活跃订阅者列表 / List of active subscribers
        """
        return [s for s in self.subscribers.values() if s.is_alive(timeout)]
        
    def cleanup_inactive(self, timeout=60):
        """
        清理不活跃的订阅者 / Clean up inactive subscribers
        
        参数 / Args:
            timeout: 超时时间(秒) / Timeout in seconds
            
        返回 / Returns:
            int: 清理的订阅者数量 / Number of cleaned subscribers
        """
        inactive_ids = [
            sid for sid, sub in self.subscribers.items()
            if not sub.is_alive(timeout)
        ]
        
        for sid in inactive_ids:
            del self.subscribers[sid]
            
        return len(inactive_ids)
        
    def count(self):
        """返回订阅者数量 / Return subscriber count"""
        return len(self.subscribers)
