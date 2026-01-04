"""
配置文件 / Configuration File
推栏消息推送系统配置 / Push Notification System Configuration
"""

class Config:
    """系统配置类 / System Configuration Class"""
    
    # 服务器配置 / Server Configuration
    HOST = '127.0.0.1'
    PORT = 5000
    DEBUG = True
    
    # 消息队列配置 / Message Queue Configuration
    MAX_QUEUE_SIZE = 1000
    MESSAGE_RETENTION_TIME = 3600  # 秒 / seconds
    
    # 客户端配置 / Client Configuration
    MAX_SUBSCRIBERS = 100
    HEARTBEAT_INTERVAL = 30  # 秒 / seconds
    
    # 消息配置 / Message Configuration
    MAX_MESSAGE_SIZE = 10240  # 字节 / bytes
    SUPPORTED_MESSAGE_TYPES = ['text', 'json', 'binary']
