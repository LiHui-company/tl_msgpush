"""
简单测试 / Simple Tests
验证核心功能 / Verify core functionality
"""

import sys
import time
from message import Message, MessageQueue
from subscriber import Subscriber, SubscriberManager


def test_message_creation():
    """测试消息创建 / Test message creation"""
    print("测试: 消息创建 / Testing: Message Creation")
    
    msg = Message("测试内容", msg_type='text', priority=3)
    assert msg.content == "测试内容"
    assert msg.msg_type == 'text'
    assert msg.priority == 3
    assert msg.status == 'pending'
    assert msg.id is not None
    
    print("  ✓ 消息创建成功 / Message creation successful")
    return True


def test_message_queue():
    """测试消息队列 / Test message queue"""
    print("测试: 消息队列 / Testing: Message Queue")
    
    queue = MessageQueue(max_size=10)
    
    # 添加不同优先级的消息
    msg1 = Message("低优先级", priority=1)
    msg2 = Message("高优先级", priority=5)
    msg3 = Message("中优先级", priority=3)
    
    queue.add(msg1)
    queue.add(msg2)
    queue.add(msg3)
    
    assert queue.size() == 3
    
    # 验证优先级排序
    next_msg = queue.get_next()
    assert next_msg.priority == 5  # 应该先获取高优先级消息
    
    print("  ✓ 消息队列功能正常 / Message queue working correctly")
    return True


def test_subscriber():
    """测试订阅者 / Test subscriber"""
    print("测试: 订阅者 / Testing: Subscriber")
    
    sub = Subscriber("test_001", name="测试订阅者", tags=["test"])
    assert sub.id == "test_001"
    assert sub.name == "测试订阅者"
    assert "test" in sub.tags
    assert sub.is_active
    
    # 测试心跳
    sub.update_heartbeat()
    assert sub.is_alive(timeout=60)
    
    print("  ✓ 订阅者功能正常 / Subscriber working correctly")
    return True


def test_subscriber_manager():
    """测试订阅者管理器 / Test subscriber manager"""
    print("测试: 订阅者管理器 / Testing: Subscriber Manager")
    
    manager = SubscriberManager(max_subscribers=5)
    
    # 注册订阅者
    sub1 = manager.register("client_1", name="客户端1")
    sub2 = manager.register("client_2", name="客户端2")
    
    assert manager.count() == 2
    assert sub1 is not None
    assert sub2 is not None
    
    # 获取订阅者
    retrieved = manager.get("client_1")
    assert retrieved.id == "client_1"
    
    # 注销订阅者
    success = manager.unregister("client_1")
    assert success
    assert manager.count() == 1
    
    print("  ✓ 订阅者管理器功能正常 / Subscriber manager working correctly")
    return True


def test_message_targeting():
    """测试消息定向 / Test message targeting"""
    print("测试: 消息定向 / Testing: Message Targeting")
    
    queue = MessageQueue()
    
    # 添加广播消息
    broadcast = Message("广播消息", target=None)
    queue.add(broadcast)
    
    # 添加定向消息
    targeted = Message("定向消息", target="client_1")
    queue.add(targeted)
    
    # 客户端1应该收到两条消息
    msgs_client1 = queue.get_for_subscriber("client_1")
    assert len(msgs_client1) == 2
    
    # 重新添加消息
    queue.add(Message("广播消息2", target=None))
    queue.add(Message("定向消息2", target="client_2"))
    
    # 客户端2应该只收到广播消息和定向给它的消息
    msgs_client2 = queue.get_for_subscriber("client_2")
    assert len(msgs_client2) == 2
    
    print("  ✓ 消息定向功能正常 / Message targeting working correctly")
    return True


def test_priority_ordering():
    """测试优先级排序 / Test priority ordering"""
    print("测试: 优先级排序 / Testing: Priority Ordering")
    
    queue = MessageQueue()
    
    # 添加多个不同优先级的消息
    for i in range(1, 6):
        queue.add(Message(f"消息{i}", priority=i))
    
    # 应该按优先级从高到低获取
    msg1 = queue.get_next()
    msg2 = queue.get_next()
    
    assert msg1.priority == 5
    assert msg2.priority == 4
    
    print("  ✓ 优先级排序正常 / Priority ordering working correctly")
    return True


def run_all_tests():
    """运行所有测试 / Run all tests"""
    print("\n" + "="*60)
    print("推栏消息推送系统 - 测试套件")
    print("Push Notification System - Test Suite")
    print("="*60 + "\n")
    
    tests = [
        test_message_creation,
        test_message_queue,
        test_subscriber,
        test_subscriber_manager,
        test_message_targeting,
        test_priority_ordering
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"  ✗ 测试失败 / Test failed")
        except Exception as e:
            failed += 1
            print(f"  ✗ 测试异常 / Test error: {e}")
            import traceback
            traceback.print_exc()
        print()
    
    print("="*60)
    print(f"测试结果 / Test Results:")
    print(f"  通过 / Passed: {passed}")
    print(f"  失败 / Failed: {failed}")
    print(f"  总计 / Total: {passed + failed}")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
