"""
客户端示例 / Client Example
演示如何使用推送服务 / Demonstrates how to use the push service
"""

import requests
import time
import json
from datetime import datetime


class PushClient:
    """
    推送客户端类 / Push Client Class
    用于连接和使用推送服务 / Used to connect and use push service
    """
    
    def __init__(self, base_url='http://127.0.0.1:5000', subscriber_id=None):
        """
        初始化客户端 / Initialize client
        
        参数 / Args:
            base_url: 服务器地址 / Server URL
            subscriber_id: 订阅者ID / Subscriber ID
        """
        self.base_url = base_url
        self.subscriber_id = subscriber_id or f"client_{int(time.time())}"
        self.is_subscribed = False
        
    def subscribe(self, name=None, tags=None):
        """
        订阅服务 / Subscribe to service
        
        参数 / Args:
            name: 订阅者名称 / Subscriber name
            tags: 订阅标签 / Subscription tags
            
        返回 / Returns:
            bool: 是否成功 / Whether successful
        """
        url = f"{self.base_url}/api/subscribe"
        data = {
            'subscriber_id': self.subscriber_id,
            'name': name or self.subscriber_id,
            'tags': tags or []
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                self.is_subscribed = True
                print(f"✓ 订阅成功 / Subscription successful: {self.subscriber_id}")
                return True
            else:
                print(f"✗ 订阅失败 / Subscription failed: {response.json()}")
                return False
        except Exception as e:
            print(f"✗ 连接错误 / Connection error: {e}")
            return False
            
    def unsubscribe(self):
        """
        取消订阅 / Unsubscribe
        
        返回 / Returns:
            bool: 是否成功 / Whether successful
        """
        url = f"{self.base_url}/api/unsubscribe"
        data = {'subscriber_id': self.subscriber_id}
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                self.is_subscribed = False
                print(f"✓ 取消订阅成功 / Unsubscription successful")
                return True
            else:
                print(f"✗ 取消订阅失败 / Unsubscription failed: {response.json()}")
                return False
        except Exception as e:
            print(f"✗ 连接错误 / Connection error: {e}")
            return False
            
    def push(self, content, msg_type='text', priority=1, target=None):
        """
        推送消息 / Push message
        
        参数 / Args:
            content: 消息内容 / Message content
            msg_type: 消息类型 / Message type
            priority: 优先级 / Priority
            target: 目标订阅者 / Target subscriber
            
        返回 / Returns:
            dict或None / Dict or None
        """
        url = f"{self.base_url}/api/push"
        data = {
            'content': content,
            'type': msg_type,
            'priority': priority,
            'target': target
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ 消息已推送 / Message pushed: {result['message_id']}")
                return result
            else:
                print(f"✗ 推送失败 / Push failed: {response.json()}")
                return None
        except Exception as e:
            print(f"✗ 连接错误 / Connection error: {e}")
            return None
            
    def pull(self):
        """
        拉取消息 / Pull messages
        
        返回 / Returns:
            list: 消息列表 / List of messages
        """
        url = f"{self.base_url}/api/pull"
        data = {'subscriber_id': self.subscriber_id}
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                messages = result.get('messages', [])
                if messages:
                    print(f"✓ 拉取到 {len(messages)} 条消息 / Pulled {len(messages)} messages")
                return messages
            else:
                print(f"✗ 拉取失败 / Pull failed: {response.json()}")
                return []
        except Exception as e:
            print(f"✗ 连接错误 / Connection error: {e}")
            return []
            
    def heartbeat(self):
        """
        发送心跳 / Send heartbeat
        
        返回 / Returns:
            bool: 是否成功 / Whether successful
        """
        url = f"{self.base_url}/api/heartbeat"
        data = {'subscriber_id': self.subscriber_id}
        
        try:
            response = requests.post(url, json=data)
            return response.status_code == 200
        except Exception as e:
            return False
            
    def get_status(self):
        """
        获取服务状态 / Get service status
        
        返回 / Returns:
            dict或None / Dict or None
        """
        url = f"{self.base_url}/api/status"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"✗ 连接错误 / Connection error: {e}")
            return None


def demo_basic_usage():
    """基本使用演示 / Basic usage demonstration"""
    print("\n" + "="*60)
    print("推栏消息推送系统 - 基本使用演示")
    print("Push Notification System - Basic Usage Demo")
    print("="*60 + "\n")
    
    # 创建客户端 / Create clients
    print("1. 创建客户端 / Creating clients...")
    client1 = PushClient(subscriber_id="demo_client_1")
    client2 = PushClient(subscriber_id="demo_client_2")
    
    # 订阅服务 / Subscribe to service
    print("\n2. 订阅服务 / Subscribing to service...")
    client1.subscribe(name="客户端1 / Client 1", tags=["demo", "test"])
    client2.subscribe(name="客户端2 / Client 2", tags=["demo"])
    
    # 查看服务状态 / Check service status
    print("\n3. 查看服务状态 / Checking service status...")
    status = client1.get_status()
    if status:
        print(f"   服务状态 / Service status: {status['status']}")
        print(f"   活跃订阅者 / Active subscribers: {status['active_subscribers']}")
        print(f"   队列大小 / Queue size: {status['queue_size']}")
    
    # 推送广播消息 / Push broadcast message
    print("\n4. 推送广播消息 / Pushing broadcast message...")
    client1.push("欢迎使用推栏消息推送系统! / Welcome to Push Notification System!", priority=3)
    
    # 推送定向消息 / Push targeted message
    print("\n5. 推送定向消息 / Pushing targeted message...")
    client1.push(
        content="这是发给客户端2的消息 / This is a message for client 2",
        target="demo_client_2",
        priority=5
    )
    
    # 拉取消息 / Pull messages
    print("\n6. 拉取消息 / Pulling messages...")
    time.sleep(0.5)  # 等待消息处理 / Wait for message processing
    
    print("   客户端1拉取消息 / Client 1 pulling messages:")
    messages1 = client1.pull()
    for msg in messages1:
        print(f"     - [{msg['type']}] {msg['content']} (优先级/Priority: {msg['priority']})")
    
    print("   客户端2拉取消息 / Client 2 pulling messages:")
    messages2 = client2.pull()
    for msg in messages2:
        print(f"     - [{msg['type']}] {msg['content']} (优先级/Priority: {msg['priority']})")
    
    # 取消订阅 / Unsubscribe
    print("\n7. 取消订阅 / Unsubscribing...")
    client1.unsubscribe()
    client2.unsubscribe()
    
    print("\n" + "="*60)
    print("演示完成! / Demo completed!")
    print("="*60 + "\n")


def demo_advanced_usage():
    """高级使用演示 / Advanced usage demonstration"""
    print("\n" + "="*60)
    print("推栏消息推送系统 - 高级使用演示")
    print("Push Notification System - Advanced Usage Demo")
    print("="*60 + "\n")
    
    # 创建多个客户端 / Create multiple clients
    print("1. 创建多个客户端 / Creating multiple clients...")
    clients = [PushClient(subscriber_id=f"client_{i}") for i in range(3)]
    
    # 批量订阅 / Batch subscribe
    print("\n2. 批量订阅 / Batch subscribing...")
    for i, client in enumerate(clients):
        client.subscribe(name=f"客户端{i+1} / Client {i+1}")
    
    # 发送不同优先级的消息 / Send messages with different priorities
    print("\n3. 发送不同优先级的消息 / Sending messages with different priorities...")
    clients[0].push("低优先级消息 / Low priority message", priority=1)
    clients[0].push("中优先级消息 / Medium priority message", priority=3)
    clients[0].push("高优先级消息 / High priority message", priority=5)
    
    # 发送JSON格式消息 / Send JSON format message
    print("\n4. 发送JSON格式消息 / Sending JSON format message...")
    json_data = {
        "title": "系统通知 / System Notification",
        "body": "您有新的消息 / You have new messages",
        "timestamp": datetime.now().isoformat()
    }
    clients[0].push(json.dumps(json_data), msg_type='json', priority=4)
    
    # 所有客户端拉取消息 / All clients pull messages
    print("\n5. 所有客户端拉取消息 / All clients pulling messages...")
    time.sleep(0.5)
    for i, client in enumerate(clients):
        print(f"   客户端{i+1} / Client {i+1}:")
        messages = client.pull()
        for msg in messages:
            content = msg['content']
            if msg['type'] == 'json':
                try:
                    content = json.loads(content)
                    content = f"JSON: {content.get('title', 'N/A')}"
                except:
                    pass
            print(f"     - [{msg['priority']}] {content}")
    
    # 清理 / Cleanup
    print("\n6. 清理订阅 / Cleaning up subscriptions...")
    for client in clients:
        client.unsubscribe()
    
    print("\n" + "="*60)
    print("高级演示完成! / Advanced demo completed!")
    print("="*60 + "\n")


if __name__ == '__main__':
    import sys
    
    print("请确保推送服务已启动 (运行 push_service.py)")
    print("Please ensure push service is running (run push_service.py)")
    print("等待2秒... / Waiting 2 seconds...")
    time.sleep(2)
    
    try:
        # 运行基本演示 / Run basic demo
        demo_basic_usage()
        
        # 询问是否运行高级演示 / Ask if run advanced demo
        time.sleep(1)
        demo_advanced_usage()
        
    except KeyboardInterrupt:
        print("\n演示已中断 / Demo interrupted")
    except Exception as e:
        print(f"\n错误 / Error: {e}")
        import traceback
        traceback.print_exc()
