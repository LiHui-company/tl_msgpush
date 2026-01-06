"""
使用示例集合 / Usage Examples Collection
展示各种使用场景 / Demonstrate various use cases
"""

import requests
import json
import time


# 服务器地址 / Server URL
BASE_URL = "http://127.0.0.1:5000"


def example_1_basic_subscribe_and_push():
    """
    示例1: 基本订阅和推送
    Example 1: Basic subscribe and push
    """
    print("\n" + "="*60)
    print("示例1: 基本订阅和推送")
    print("Example 1: Basic Subscribe and Push")
    print("="*60)
    
    # 1. 订阅
    print("\n1. 订阅服务...")
    response = requests.post(f"{BASE_URL}/api/subscribe", json={
        "subscriber_id": "example_client_1",
        "name": "示例客户端1"
    })
    print(f"   状态: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    # 2. 推送消息
    print("\n2. 推送消息...")
    response = requests.post(f"{BASE_URL}/api/push", json={
        "content": "Hello from Example 1!",
        "type": "text",
        "priority": 3
    })
    print(f"   状态: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    # 3. 拉取消息
    print("\n3. 拉取消息...")
    time.sleep(0.5)
    response = requests.post(f"{BASE_URL}/api/pull", json={
        "subscriber_id": "example_client_1"
    })
    print(f"   状态: {response.status_code}")
    result = response.json()
    print(f"   收到 {result['count']} 条消息:")
    for msg in result['messages']:
        print(f"     - {msg['content']}")
    
    # 4. 取消订阅
    print("\n4. 取消订阅...")
    response = requests.post(f"{BASE_URL}/api/unsubscribe", json={
        "subscriber_id": "example_client_1"
    })
    print(f"   状态: {response.status_code}")


def example_2_targeted_messages():
    """
    示例2: 定向消息推送
    Example 2: Targeted message push
    """
    print("\n" + "="*60)
    print("示例2: 定向消息推送")
    print("Example 2: Targeted Message Push")
    print("="*60)
    
    # 订阅两个客户端
    print("\n1. 订阅两个客户端...")
    for i in [1, 2]:
        response = requests.post(f"{BASE_URL}/api/subscribe", json={
            "subscriber_id": f"targeted_client_{i}",
            "name": f"客户端{i}"
        })
        print(f"   客户端{i}: {response.status_code}")
    
    # 发送广播消息
    print("\n2. 发送广播消息...")
    response = requests.post(f"{BASE_URL}/api/push", json={
        "content": "这是广播消息，所有人都能收到",
        "priority": 2
    })
    print(f"   状态: {response.status_code}")
    
    # 发送定向消息
    print("\n3. 发送定向消息给客户端1...")
    response = requests.post(f"{BASE_URL}/api/push", json={
        "content": "这是给客户端1的专属消息",
        "target": "targeted_client_1",
        "priority": 4
    })
    print(f"   状态: {response.status_code}")
    
    # 两个客户端分别拉取消息
    print("\n4. 客户端拉取消息...")
    time.sleep(0.5)
    for i in [1, 2]:
        response = requests.post(f"{BASE_URL}/api/pull", json={
            "subscriber_id": f"targeted_client_{i}"
        })
        result = response.json()
        print(f"   客户端{i} 收到 {result['count']} 条消息:")
        for msg in result['messages']:
            print(f"     - {msg['content']}")
    
    # 清理
    for i in [1, 2]:
        requests.post(f"{BASE_URL}/api/unsubscribe", json={
            "subscriber_id": f"targeted_client_{i}"
        })


def example_3_priority_messages():
    """
    示例3: 优先级消息处理
    Example 3: Priority message handling
    """
    print("\n" + "="*60)
    print("示例3: 优先级消息处理")
    print("Example 3: Priority Message Handling")
    print("="*60)
    
    # 订阅
    print("\n1. 订阅服务...")
    response = requests.post(f"{BASE_URL}/api/subscribe", json={
        "subscriber_id": "priority_client",
        "name": "优先级测试客户端"
    })
    print(f"   状态: {response.status_code}")
    
    # 发送不同优先级的消息
    print("\n2. 发送不同优先级的消息...")
    priorities = [1, 3, 5, 2, 4]
    for p in priorities:
        response = requests.post(f"{BASE_URL}/api/push", json={
            "content": f"优先级 {p} 的消息",
            "priority": p
        })
        print(f"   发送优先级 {p}: {response.status_code}")
    
    # 拉取消息，应该按优先级排序
    print("\n3. 拉取消息 (应该按优先级从高到低)...")
    time.sleep(0.5)
    response = requests.post(f"{BASE_URL}/api/pull", json={
        "subscriber_id": "priority_client"
    })
    result = response.json()
    print(f"   收到 {result['count']} 条消息:")
    for msg in result['messages']:
        print(f"     - 优先级 {msg['priority']}: {msg['content']}")
    
    # 清理
    requests.post(f"{BASE_URL}/api/unsubscribe", json={
        "subscriber_id": "priority_client"
    })


def example_4_json_messages():
    """
    示例4: JSON消息
    Example 4: JSON messages
    """
    print("\n" + "="*60)
    print("示例4: JSON消息")
    print("Example 4: JSON Messages")
    print("="*60)
    
    # 订阅
    print("\n1. 订阅服务...")
    response = requests.post(f"{BASE_URL}/api/subscribe", json={
        "subscriber_id": "json_client",
        "name": "JSON测试客户端"
    })
    
    # 发送JSON消息
    print("\n2. 发送JSON消息...")
    json_data = {
        "event": "user_login",
        "user_id": 12345,
        "username": "张三",
        "timestamp": "2026-01-04T08:00:00Z",
        "metadata": {
            "ip": "192.168.1.100",
            "device": "mobile"
        }
    }
    response = requests.post(f"{BASE_URL}/api/push", json={
        "content": json.dumps(json_data, ensure_ascii=False),
        "type": "json",
        "priority": 3
    })
    print(f"   状态: {response.status_code}")
    
    # 拉取并解析JSON消息
    print("\n3. 拉取并解析JSON消息...")
    time.sleep(0.5)
    response = requests.post(f"{BASE_URL}/api/pull", json={
        "subscriber_id": "json_client"
    })
    result = response.json()
    for msg in result['messages']:
        if msg['type'] == 'json':
            data = json.loads(msg['content'])
            print(f"   事件类型: {data['event']}")
            print(f"   用户ID: {data['user_id']}")
            print(f"   用户名: {data['username']}")
            print(f"   设备: {data['metadata']['device']}")
    
    # 清理
    requests.post(f"{BASE_URL}/api/unsubscribe", json={
        "subscriber_id": "json_client"
    })


def example_5_heartbeat():
    """
    示例5: 心跳机制
    Example 5: Heartbeat mechanism
    """
    print("\n" + "="*60)
    print("示例5: 心跳机制")
    print("Example 5: Heartbeat Mechanism")
    print("="*60)
    
    # 订阅
    print("\n1. 订阅服务...")
    response = requests.post(f"{BASE_URL}/api/subscribe", json={
        "subscriber_id": "heartbeat_client",
        "name": "心跳测试客户端"
    })
    
    # 查看订阅者状态
    print("\n2. 查看订阅者列表...")
    response = requests.get(f"{BASE_URL}/api/subscribers?active_only=true")
    result = response.json()
    print(f"   活跃订阅者数量: {result['count']}")
    
    # 发送心跳
    print("\n3. 发送心跳...")
    for i in range(3):
        response = requests.post(f"{BASE_URL}/api/heartbeat", json={
            "subscriber_id": "heartbeat_client"
        })
        print(f"   心跳 {i+1}: {response.status_code}")
        time.sleep(1)
    
    # 再次查看订阅者状态
    print("\n4. 再次查看订阅者列表...")
    response = requests.get(f"{BASE_URL}/api/subscribers?active_only=true")
    result = response.json()
    print(f"   活跃订阅者数量: {result['count']}")
    if result['subscribers']:
        for sub in result['subscribers']:
            print(f"   - {sub['name']} (ID: {sub['id']})")
    
    # 清理
    requests.post(f"{BASE_URL}/api/unsubscribe", json={
        "subscriber_id": "heartbeat_client"
    })


def example_6_service_status():
    """
    示例6: 服务状态查询
    Example 6: Service status query
    """
    print("\n" + "="*60)
    print("示例6: 服务状态查询")
    print("Example 6: Service Status Query")
    print("="*60)
    
    print("\n查询服务状态...")
    response = requests.get(f"{BASE_URL}/api/status")
    
    if response.status_code == 200:
        status = response.json()
        print(f"\n服务状态详情:")
        print(f"  运行状态: {status['status']}")
        print(f"  队列大小: {status['queue_size']}")
        print(f"  活跃订阅者: {status['active_subscribers']}")
        print(f"  总订阅者数: {status['total_subscribers']}")
        print(f"  统计信息:")
        print(f"    - 已发送消息: {status['stats']['messages_sent']}")
        print(f"    - 失败消息: {status['stats']['messages_failed']}")
        print(f"    - 总消息数: {status['stats']['total_messages']}")
    else:
        print(f"查询失败: {response.status_code}")


def main():
    """运行所有示例 / Run all examples"""
    print("\n" + "="*60)
    print("推栏消息推送系统 - 使用示例集合")
    print("Push Notification System - Usage Examples")
    print("="*60)
    
    print("\n请确保推送服务正在运行...")
    print("Please ensure the push service is running...")
    time.sleep(2)
    
    try:
        # 检查服务是否运行
        response = requests.get(f"{BASE_URL}/api/status", timeout=2)
        if response.status_code != 200:
            print("错误: 服务未响应")
            return
    except Exception as e:
        print(f"错误: 无法连接到服务 - {e}")
        print("请先运行: python push_service.py")
        return
    
    # 运行所有示例
    examples = [
        example_1_basic_subscribe_and_push,
        example_2_targeted_messages,
        example_3_priority_messages,
        example_4_json_messages,
        example_5_heartbeat,
        example_6_service_status
    ]
    
    for example in examples:
        try:
            example()
            time.sleep(1)
        except Exception as e:
            print(f"\n错误: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("所有示例运行完成!")
    print("All examples completed!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
