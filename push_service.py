"""
推送服务模块 / Push Service Module
核心消息推送服务 / Core message push service
"""

from flask import Flask, request, jsonify
from message import Message, MessageQueue
from subscriber import SubscriberManager
from config import Config
import time


class PushService:
    """
    推送服务类 / Push Service Class
    管理消息推送的核心服务 / Core service for managing message push
    """
    
    def __init__(self):
        """初始化推送服务 / Initialize push service"""
        self.message_queue = MessageQueue(max_size=Config.MAX_QUEUE_SIZE)
        self.subscriber_manager = SubscriberManager(max_subscribers=Config.MAX_SUBSCRIBERS)
        self.app = Flask(__name__)
        self.setup_routes()
        self.stats = {
            'messages_sent': 0,
            'messages_failed': 0,
            'total_messages': 0
        }
        
    def setup_routes(self):
        """设置API路由 / Setup API routes"""
        
        @self.app.route('/api/status', methods=['GET'])
        def status():
            """获取服务状态 / Get service status"""
            return jsonify({
                'status': 'running',
                'queue_size': self.message_queue.size(),
                'active_subscribers': len(self.subscriber_manager.get_active()),
                'total_subscribers': self.subscriber_manager.count(),
                'stats': self.stats
            })
            
        @self.app.route('/api/subscribe', methods=['POST'])
        def subscribe():
            """订阅服务 / Subscribe to service"""
            data = request.json or {}
            subscriber_id = data.get('subscriber_id')
            name = data.get('name')
            tags = data.get('tags', [])
            
            if not subscriber_id:
                return jsonify({'error': '缺少订阅者ID / Missing subscriber_id'}), 400
            
            # 验证tags是列表 / Validate tags is a list
            if not isinstance(tags, list):
                tags = []
                
            subscriber = self.subscriber_manager.register(subscriber_id, name, tags)
            if subscriber is None:
                return jsonify({'error': '订阅者数量已达上限 / Subscriber limit reached'}), 503
                
            return jsonify({
                'message': '订阅成功 / Subscription successful',
                'subscriber': subscriber.to_dict()
            })
            
        @self.app.route('/api/unsubscribe', methods=['POST'])
        def unsubscribe():
            """取消订阅 / Unsubscribe from service"""
            data = request.json or {}
            subscriber_id = data.get('subscriber_id')
            
            if not subscriber_id:
                return jsonify({'error': '缺少订阅者ID / Missing subscriber_id'}), 400
                
            success = self.subscriber_manager.unregister(subscriber_id)
            if success:
                return jsonify({'message': '取消订阅成功 / Unsubscription successful'})
            else:
                return jsonify({'error': '订阅者不存在 / Subscriber not found'}), 404
                
        @self.app.route('/api/push', methods=['POST'])
        def push_message():
            """推送消息 / Push message"""
            data = request.json or {}
            content = data.get('content')
            msg_type = data.get('type', 'text')
            priority = data.get('priority', 1)
            target = data.get('target')
            
            if not content:
                return jsonify({'error': '缺少消息内容 / Missing content'}), 400
            
            # 验证并规范化优先级 / Validate and normalize priority
            try:
                priority = int(priority)
                if priority < 1 or priority > 5:
                    priority = 1
            except (TypeError, ValueError):
                priority = 1
            
            # 验证消息类型 / Validate message type
            if msg_type not in Config.SUPPORTED_MESSAGE_TYPES:
                msg_type = 'text'
                
            message = Message(content, msg_type, priority, target)
            self.message_queue.add(message)
            self.stats['total_messages'] += 1
            
            return jsonify({
                'message': '消息已加入队列 / Message queued',
                'message_id': message.id,
                'details': message.to_dict()
            })
            
        @self.app.route('/api/pull', methods=['POST'])
        def pull_messages():
            """拉取消息 / Pull messages"""
            data = request.json or {}
            subscriber_id = data.get('subscriber_id')
            
            if not subscriber_id:
                return jsonify({'error': '缺少订阅者ID / Missing subscriber_id'}), 400
                
            subscriber = self.subscriber_manager.get(subscriber_id)
            if not subscriber:
                return jsonify({'error': '订阅者不存在 / Subscriber not found'}), 404
                
            # 更新心跳 / Update heartbeat
            subscriber.update_heartbeat()
            
            # 获取消息 / Get messages
            messages = self.message_queue.get_for_subscriber(subscriber_id)
            
            return jsonify({
                'subscriber_id': subscriber_id,
                'count': len(messages),
                'messages': [msg.to_dict() for msg in messages]
            })
            
        @self.app.route('/api/heartbeat', methods=['POST'])
        def heartbeat():
            """心跳检测 / Heartbeat check"""
            data = request.json or {}
            subscriber_id = data.get('subscriber_id')
            
            if not subscriber_id:
                return jsonify({'error': '缺少订阅者ID / Missing subscriber_id'}), 400
                
            subscriber = self.subscriber_manager.get(subscriber_id)
            if not subscriber:
                return jsonify({'error': '订阅者不存在 / Subscriber not found'}), 404
                
            subscriber.update_heartbeat()
            return jsonify({'message': '心跳更新成功 / Heartbeat updated'})
            
        @self.app.route('/api/subscribers', methods=['GET'])
        def list_subscribers():
            """列出所有订阅者 / List all subscribers"""
            active_only = request.args.get('active_only', 'false').lower() == 'true'
            
            if active_only:
                subscribers = self.subscriber_manager.get_active()
            else:
                subscribers = self.subscriber_manager.get_all()
                
            return jsonify({
                'count': len(subscribers),
                'subscribers': [s.to_dict() for s in subscribers]
            })
            
    def start(self, host=None, port=None, debug=None):
        """
        启动服务 / Start service
        
        参数 / Args:
            host: 主机地址 / Host address
            port: 端口号 / Port number
            debug: 调试模式 / Debug mode
        """
        host = host or Config.HOST
        port = port or Config.PORT
        debug = debug if debug is not None else Config.DEBUG
        
        print(f"推送服务启动中... / Starting push service...")
        print(f"服务地址 / Service URL: http://{host}:{port}")
        print(f"API文档 / API Documentation: http://{host}:{port}/api/status")
        
        self.app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    service = PushService()
    service.start()
