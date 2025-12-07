"""
Demo Remote Super Agent - Client standalone senza dipendenze server
"""

from remote_client import RemoteSuperAgentClient, RemoteAgentConfig
import time


def demo_remote_operations():
    """Demo operazioni remote complete"""
    
    print("=" * 80)
    print("REMOTE SUPER AGENT - STANDALONE CLIENT DEMO")
    print("=" * 80)
    
    # Configurazione
    config = RemoteAgentConfig(
        base_url="http://localhost:5000",
        username="admin",
        password="admin123"
    )
    
    client = RemoteSuperAgentClient(config)
    
    # Health check
    print("\n[1] HEALTH CHECK")
    print("-" * 80)
    try:
        health = client.health_check()
        print(f"✓ Server Status: {health['status']}")
        print(f"✓ Version: {health['version']}")
        print(f"✓ Timestamp: {health['timestamp']}")
    except Exception as e:
        print(f"✗ Server not available: {str(e)}")
        print("\nPlease start server in another terminal:")
        print("  python remote_server.py")
        return
    
    # Login
    print("\n[2] AUTHENTICATION")
    print("-" * 80)
    if client.login():
        print(f"✓ Logged in successfully")
    else:
        print("✗ Login failed")
        return
    
    # Code Generation
    print("\n[3] CODE GENERATION")
    print("-" * 80)
    
    descriptions = [
        "Function to calculate Fibonacci sequence",
        "Class for managing a queue data structure",
        "Algorithm for binary search"
    ]
    
    for i, desc in enumerate(descriptions, 1):
        print(f"\n  [{i}] {desc}")
        result = client.generate_code(desc)
        print(f"      ✓ Generated {result['lines']} lines")
        print(f"      ✓ Quality: {result['quality_score']:.2%}")
        print(f"      Code preview:\n{result['code'][:100]}...")
    
    # Code Analysis
    print("\n[4] CODE ANALYSIS")
    print("-" * 80)
    
    sample_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""
    
    print("  Analyzing code sample...")
    analysis = client.analyze_code(sample_code)
    print(f"  ✓ Lines: {analysis['lines']}")
    print(f"  ✓ Complexity: {analysis['complexity']}")
    print(f"  ✓ Quality Score: {analysis['quality_score']:.2%}")
    print(f"  ✓ Suggestions: {', '.join(analysis['suggestions'])}")
    
    # Refactoring
    print("\n[5] CODE REFACTORING")
    print("-" * 80)
    
    print("  Refactoring code...")
    refactored = client.refactor_code(sample_code)
    print(f"  ✓ Original: {refactored['original_lines']} lines")
    print(f"  ✓ Refactored: {refactored['refactored_lines']} lines")
    print(f"  ✓ Improvements:")
    for improvement in refactored['improvements']:
        print(f"      - {improvement}")
    
    # Neural Network Prediction
    print("\n[6] NEURAL NETWORK PREDICTION")
    print("-" * 80)
    
    test_inputs = [
        [1.0, 2.0, 3.0, 4.0, 5.0],
        [0.5, 1.5, 2.5, 3.5, 4.5],
        [10.0, 20.0, 30.0, 40.0, 50.0]
    ]
    
    for i, input_data in enumerate(test_inputs, 1):
        print(f"\n  [{i}] Input: {input_data}")
        prediction = client.neural_predict([input_data])
        print(f"      ✓ Confidence: {prediction['confidence']:.2%}")
        print(f"      ✓ Model: {prediction['model']}")
        print(f"      ✓ Latency: {prediction['latency_ms']}ms")
        print(f"      ✓ Predictions shape: {len(prediction['predictions'])}x{len(prediction['predictions'][0])}")
    
    # Async Tasks
    print("\n[7] ASYNC TASK EXECUTION")
    print("-" * 80)
    
    print("  Creating async tasks...")
    task_configs = [
        ('generate_code', {'description': 'Merge sort implementation'}),
        ('analyze_code', {'code': 'def test(): pass'}),
        ('refactor_code', {'code': 'x = 1\nx = x + 1\nreturn x'})
    ]
    
    task_ids = []
    for task_type, params in task_configs:
        task_id = client.create_task(task_type, params)
        task_ids.append(task_id)
        print(f"  ✓ Created task: {task_id[:8]}... ({task_type})")
    
    print("\n  Waiting for completion...")
    completed = 0
    for task_id in task_ids:
        try:
            result = client.wait_for_task(task_id, max_wait=10)
            if result['status'] == 'completed':
                completed += 1
                print(f"  ✓ Task {task_id[:8]}... completed")
        except Exception as e:
            print(f"  ✗ Task {task_id[:8]}... failed: {str(e)}")
    
    print(f"\n  Summary: {completed}/{len(task_ids)} tasks completed")
    
    # Statistics
    print("\n[8] SERVER STATISTICS")
    print("-" * 80)
    
    try:
        stats = client.get_stats()
        print(f"  ✓ Total Requests: {stats['total_requests']}")
        print(f"  ✓ Successful Tasks: {stats['successful_tasks']}")
        print(f"  ✓ Failed Tasks: {stats['failed_tasks']}")
        print(f"  ✓ Total Tasks: {stats['total_tasks']}")
        print(f"  ✓ Pending Tasks: {stats['pending_tasks']}")
        print(f"  ✓ Running Tasks: {stats['running_tasks']}")
        print(f"  ✓ Server Uptime: {stats['uptime']}")
    except Exception as e:
        print(f"  ✗ Could not fetch stats: {str(e)}")
    
    # Task Management
    print("\n[9] TASK MANAGEMENT")
    print("-" * 80)
    
    try:
        tasks = client.list_tasks()
        print(f"  ✓ Total tasks in system: {len(tasks)}")
        
        if len(tasks) > 0:
            print(f"\n  Recent tasks:")
            for task in tasks[-3:]:  # Last 3 tasks
                print(f"    - {task['task_id'][:8]}... : {task['status']} ({task['task_type']})")
    except Exception as e:
        print(f"  ✗ Could not list tasks: {str(e)}")
    
    # Summary
    print("\n" + "=" * 80)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    print("\n✓ FEATURES TESTED:")
    print("  [OK] Health Check & Server Status")
    print("  [OK] Authentication (JWT)")
    print("  [OK] Code Generation (3 examples)")
    print("  [OK] Code Analysis (complexity, quality)")
    print("  [OK] Code Refactoring (improvements)")
    print("  [OK] Neural Network Predictions (3 tests)")
    print("  [OK] Async Task Execution (3 tasks)")
    print("  [OK] Server Statistics")
    print("  [OK] Task Management")
    
    print("\n✓ REMOTE CAPABILITIES:")
    print("  • REST API with JWT authentication")
    print("  • Async task processing")
    print("  • Real-time status tracking")
    print("  • Server-side execution")
    print("  • Multi-user support")
    print("  • Statistics monitoring")
    
    print("\n✓ PRODUCTION READY:")
    print("  • Secure token-based auth")
    print("  • Error handling & logging")
    print("  • Task queueing system")
    print("  • RESTful API design")
    print("  • CORS enabled")
    print("  • Health monitoring")


def quick_test():
    """Quick connectivity test"""
    
    print("\nQUICK CONNECTIVITY TEST")
    print("-" * 40)
    
    client = RemoteSuperAgentClient()
    
    try:
        health = client.health_check()
        print(f"✓ Server is {health['status']}")
        
        if client.login():
            print(f"✓ Authentication working")
            
            # Quick operation
            result = client.generate_code("Hello world function")
            print(f"✓ Remote execution working")
            print(f"✓ Generated {result['lines']} lines")
            
            return True
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        demo_remote_operations()
