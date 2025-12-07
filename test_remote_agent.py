"""
Test Remote Super Agent - Test completo sistema remoto
"""

import subprocess
import time
import sys
import threading
from remote_client import RemoteSuperAgentClient, RemoteAgentConfig


class RemoteAgentTester:
    """Tester per sistema remoto"""
    
    def __init__(self):
        self.server_process = None
        self.client = None
        
    def start_server(self):
        """Start server in background"""
        print("[*] Starting remote server...")
        
        # Start server process
        self.server_process = subprocess.Popen(
            [sys.executable, 'remote_server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        time.sleep(3)
        
        print("[OK] Server started")
        
    def stop_server(self):
        """Stop server"""
        if self.server_process:
            print("[*] Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
            print("[OK] Server stopped")
    
    def test_connection(self):
        """Test: Connection and authentication"""
        print("\n" + "=" * 80)
        print("TEST 1: CONNECTION & AUTHENTICATION")
        print("=" * 80)
        
        config = RemoteAgentConfig()
        self.client = RemoteSuperAgentClient(config)
        
        # Health check
        print("\n[*] Health check...")
        try:
            health = self.client.health_check()
            print(f"   Status: {health['status']}")
            assert health['status'] == 'healthy', "Server not healthy"
            print("   [OK] Server is healthy")
        except Exception as e:
            print(f"   [FAIL] {str(e)}")
            return False
        
        # Login
        print("\n[*] Testing login...")
        if self.client.login():
            print("   [OK] Login successful")
        else:
            print("   [FAIL] Login failed")
            return False
        
        return True
    
    def test_code_generation(self):
        """Test: Code generation"""
        print("\n" + "=" * 80)
        print("TEST 2: CODE GENERATION")
        print("=" * 80)
        
        descriptions = [
            "Function to reverse a string",
            "Class for binary search tree",
            "Algorithm for quick sort"
        ]
        
        for desc in descriptions:
            print(f"\n[*] Generating: {desc}")
            result = self.client.generate_code(desc)
            
            assert 'code' in result, "No code generated"
            assert result['quality_score'] > 0.8, "Quality too low"
            
            print(f"   Lines: {result['lines']}")
            print(f"   Quality: {result['quality_score']}")
            print("   [OK] Code generated")
        
        return True
    
    def test_code_analysis(self):
        """Test: Code analysis"""
        print("\n" + "=" * 80)
        print("TEST 3: CODE ANALYSIS")
        print("=" * 80)
        
        test_codes = [
            "def simple():\n    pass",
            "class MyClass:\n    def __init__(self):\n        self.value = 0",
            "for i in range(10):\n    print(i)"
        ]
        
        for i, code in enumerate(test_codes, 1):
            print(f"\n[*] Analyzing code sample {i}")
            result = self.client.analyze_code(code)
            
            assert 'lines' in result, "No analysis result"
            assert 'complexity' in result, "No complexity metric"
            
            print(f"   Lines: {result['lines']}")
            print(f"   Complexity: {result['complexity']}")
            print(f"   Quality: {result['quality_score']}")
            print("   [OK] Analysis complete")
        
        return True
    
    def test_refactoring(self):
        """Test: Code refactoring"""
        print("\n" + "=" * 80)
        print("TEST 4: CODE REFACTORING")
        print("=" * 80)
        
        code = """
def bad_function():
    x = 1
    x = x + 1
    x = x + 1
    return x
"""
        
        print("\n[*] Refactoring code...")
        result = self.client.refactor_code(code)
        
        assert 'refactored_code' in result, "No refactored code"
        assert 'improvements' in result, "No improvements listed"
        
        print(f"   Original lines: {result['original_lines']}")
        print(f"   Refactored lines: {result['refactored_lines']}")
        print(f"   Improvements: {len(result['improvements'])}")
        print("   [OK] Refactoring complete")
        
        return True
    
    def test_neural_prediction(self):
        """Test: Neural network prediction"""
        print("\n" + "=" * 80)
        print("TEST 5: NEURAL NETWORK PREDICTION")
        print("=" * 80)
        
        test_inputs = [
            [[1, 2, 3, 4, 5]],
            [[0.1, 0.2, 0.3]],
            [[10, 20, 30, 40]]
        ]
        
        for i, input_data in enumerate(test_inputs, 1):
            print(f"\n[*] Prediction {i}")
            result = self.client.neural_predict(input_data)
            
            assert 'predictions' in result, "No predictions"
            assert result['confidence'] > 0.5, "Confidence too low"
            
            print(f"   Confidence: {result['confidence']}")
            print(f"   Model: {result['model']}")
            print(f"   Latency: {result['latency_ms']}ms")
            print("   [OK] Prediction complete")
        
        return True
    
    def test_async_tasks(self):
        """Test: Asynchronous tasks"""
        print("\n" + "=" * 80)
        print("TEST 6: ASYNC TASK EXECUTION")
        print("=" * 80)
        
        # Create multiple tasks
        task_ids = []
        
        for i in range(3):
            print(f"\n[*] Creating task {i+1}")
            task_id = self.client.create_task(
                'generate_code',
                {'description': f'Test function {i+1}'}
            )
            task_ids.append(task_id)
            print(f"   Task ID: {task_id}")
        
        # Wait for completion
        print("\n[*] Waiting for tasks to complete...")
        for task_id in task_ids:
            result = self.client.wait_for_task(task_id, max_wait=10)
            assert result['status'] == 'completed', f"Task {task_id} failed"
            print(f"   Task {task_id}: {result['status']}")
        
        print("   [OK] All tasks completed")
        
        return True
    
    def test_task_management(self):
        """Test: Task listing and deletion"""
        print("\n" + "=" * 80)
        print("TEST 7: TASK MANAGEMENT")
        print("=" * 80)
        
        # List tasks
        print("\n[*] Listing tasks...")
        tasks = self.client.list_tasks()
        print(f"   Total tasks: {len(tasks)}")
        
        # Delete some tasks
        if tasks:
            print("\n[*] Deleting tasks...")
            deleted = 0
            for task in tasks[:3]:  # Delete first 3
                if self.client.delete_task(task['task_id']):
                    deleted += 1
            
            print(f"   Deleted: {deleted} tasks")
            print("   [OK] Task management complete")
        
        return True
    
    def test_statistics(self):
        """Test: Server statistics"""
        print("\n" + "=" * 80)
        print("TEST 8: SERVER STATISTICS")
        print("=" * 80)
        
        print("\n[*] Fetching statistics...")
        stats = self.client.get_stats()
        
        print(f"\n   Server Statistics:")
        print(f"   - Total requests: {stats['total_requests']}")
        print(f"   - Successful tasks: {stats['successful_tasks']}")
        print(f"   - Failed tasks: {stats['failed_tasks']}")
        print(f"   - Total tasks: {stats['total_tasks']}")
        print(f"   - Pending tasks: {stats['pending_tasks']}")
        print(f"   - Running tasks: {stats['running_tasks']}")
        print(f"   - Uptime: {stats['uptime']}")
        
        assert stats['total_requests'] > 0, "No requests recorded"
        print("\n   [OK] Statistics retrieved")
        
        return True
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "=" * 80)
        print("REMOTE SUPER AGENT - COMPLETE TEST SUITE")
        print("=" * 80)
        
        results = {}
        
        try:
            # Start server
            self.start_server()
            
            # Wait for server initialization
            time.sleep(2)
            
            # Run tests
            tests = [
                ("Connection & Authentication", self.test_connection),
                ("Code Generation", self.test_code_generation),
                ("Code Analysis", self.test_code_analysis),
                ("Code Refactoring", self.test_refactoring),
                ("Neural Prediction", self.test_neural_prediction),
                ("Async Tasks", self.test_async_tasks),
                ("Task Management", self.test_task_management),
                ("Server Statistics", self.test_statistics)
            ]
            
            for test_name, test_func in tests:
                try:
                    result = test_func()
                    results[test_name] = "PASS" if result else "FAIL"
                except Exception as e:
                    results[test_name] = f"FAIL: {str(e)}"
                    print(f"\n   [ERROR] {str(e)}")
            
        finally:
            # Stop server
            self.stop_server()
        
        # Print summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for r in results.values() if r == "PASS")
        total = len(results)
        
        for test_name, result in results.items():
            status = "[OK]" if result == "PASS" else "[FAIL]"
            print(f"{status} {test_name}: {result}")
        
        print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("\n[OK] ALL TESTS PASSED - Remote Super Agent is PRODUCTION READY!")
        else:
            print(f"\n[WARNING] {total-passed} tests failed")
        
        return passed == total


def main():
    """Main entry point"""
    tester = RemoteAgentTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
