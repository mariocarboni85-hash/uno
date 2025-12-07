"""
Scheduler and Task Automation Tool
Handles scheduled tasks, cron-like functionality, task queues
"""
import time
import threading
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional, Any
from queue import Queue, PriorityQueue
import json


class Task:
    """Represents a scheduled task."""
    
    def __init__(self, name: str, func: Callable, args: tuple = (),
                 kwargs: Optional[dict] = None, priority: int = 5):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.priority = priority
        self.created_at = datetime.now()
        self.executed_at = None
        self.status = 'pending'  # pending, running, completed, failed
        self.result = None
        self.error = None
    
    def execute(self):
        """Execute the task."""
        try:
            self.status = 'running'
            self.executed_at = datetime.now()
            self.result = self.func(*self.args, **self.kwargs)
            self.status = 'completed'
            return self.result
        except Exception as e:
            self.status = 'failed'
            self.error = str(e)
            return None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary."""
        return {
            'name': self.name,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'result': str(self.result) if self.result else None,
            'error': self.error
        }


class ScheduledTask:
    """Represents a recurring scheduled task."""
    
    def __init__(self, name: str, func: Callable, schedule: Dict,
                 args: tuple = (), kwargs: Optional[dict] = None):
        self.name = name
        self.func = func
        self.schedule = schedule  # {'interval': 60} or {'cron': '*/5 * * * *'}
        self.args = args
        self.kwargs = kwargs or {}
        self.next_run = None
        self.last_run = None
        self.run_count = 0
        self.enabled = True
        
        self._calculate_next_run()
    
    def _calculate_next_run(self):
        """Calculate next run time."""
        if 'interval' in self.schedule:
            # Simple interval in seconds
            interval = self.schedule['interval']
            if self.last_run:
                self.next_run = self.last_run + timedelta(seconds=interval)
            else:
                self.next_run = datetime.now() + timedelta(seconds=interval)
        
        elif 'cron' in self.schedule:
            # Simple cron parsing (minute hour day month weekday)
            # For now, just support */N patterns for minutes
            cron = self.schedule['cron']
            if cron.startswith('*/'):
                minutes = int(cron.split()[0].replace('*/', ''))
                if self.last_run:
                    self.next_run = self.last_run + timedelta(minutes=minutes)
                else:
                    self.next_run = datetime.now() + timedelta(minutes=minutes)
            else:
                # Default to 5 minutes if can't parse
                self.next_run = datetime.now() + timedelta(minutes=5)
        
        elif 'time' in self.schedule:
            # Specific time (e.g., '14:30')
            target_time = datetime.strptime(self.schedule['time'], '%H:%M').time()
            now = datetime.now()
            next_run = datetime.combine(now.date(), target_time)
            
            if next_run <= now:
                next_run += timedelta(days=1)
            
            self.next_run = next_run
    
    def should_run(self) -> bool:
        """Check if task should run now."""
        if not self.enabled:
            return False
        
        if self.next_run is None:
            return False
        
        return datetime.now() >= self.next_run
    
    def execute(self):
        """Execute the task."""
        try:
            result = self.func(*self.args, **self.kwargs)
            self.last_run = datetime.now()
            self.run_count += 1
            self._calculate_next_run()
            return result
        except Exception as e:
            self.last_run = datetime.now()
            self._calculate_next_run()
            raise e


class TaskQueue:
    """Priority task queue with threading."""
    
    def __init__(self, num_workers: int = 2):
        self.queue = PriorityQueue()
        self.num_workers = num_workers
        self.workers = []
        self.running = False
        self.completed_tasks = []
    
    def start(self):
        """Start worker threads."""
        if self.running:
            return
        
        self.running = True
        
        for i in range(self.num_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def stop(self):
        """Stop worker threads."""
        self.running = False
    
    def _worker(self):
        """Worker thread function."""
        while self.running:
            try:
                # Get task from queue (priority, timestamp, task)
                priority, timestamp, task = self.queue.get(timeout=1)
                
                # Execute task
                task.execute()
                
                # Store completed task
                self.completed_tasks.append(task)
                
                self.queue.task_done()
            except:
                continue
    
    def add_task(self, task: Task):
        """Add task to queue."""
        # Lower priority number = higher priority
        timestamp = time.time()
        self.queue.put((task.priority, timestamp, task))
    
    def get_status(self) -> Dict:
        """Get queue status."""
        return {
            'queue_size': self.queue.qsize(),
            'workers': self.num_workers,
            'running': self.running,
            'completed': len(self.completed_tasks)
        }


class Scheduler:
    """Advanced task scheduler."""
    
    def __init__(self):
        self.tasks = {}  # name -> ScheduledTask
        self.running = False
        self.scheduler_thread = None
        self.task_queue = TaskQueue(num_workers=2)
    
    def add_task(self, name: str, func: Callable, schedule: Dict,
                args: tuple = (), kwargs: Optional[dict] = None):
        """
        Add scheduled task.
        
        Schedule examples:
        - {'interval': 60} - Every 60 seconds
        - {'cron': '*/5 * * * *'} - Every 5 minutes
        - {'time': '14:30'} - Daily at 14:30
        """
        task = ScheduledTask(name, func, schedule, args, kwargs)
        self.tasks[name] = task
    
    def remove_task(self, name: str) -> bool:
        """Remove task by name."""
        if name in self.tasks:
            del self.tasks[name]
            return True
        return False
    
    def enable_task(self, name: str):
        """Enable a task."""
        if name in self.tasks:
            self.tasks[name].enabled = True
    
    def disable_task(self, name: str):
        """Disable a task."""
        if name in self.tasks:
            self.tasks[name].enabled = False
    
    def start(self):
        """Start scheduler."""
        if self.running:
            return
        
        self.running = True
        self.task_queue.start()
        self.scheduler_thread = threading.Thread(target=self._run, daemon=True)
        self.scheduler_thread.start()
    
    def stop(self):
        """Stop scheduler."""
        self.running = False
        self.task_queue.stop()
    
    def _run(self):
        """Main scheduler loop."""
        while self.running:
            # Check all tasks
            for name, task in self.tasks.items():
                if task.should_run():
                    # Create a task for the queue
                    queue_task = Task(
                        name=name,
                        func=task.func,
                        args=task.args,
                        kwargs=task.kwargs
                    )
                    self.task_queue.add_task(queue_task)
                    
                    # Update last run
                    task.last_run = datetime.now()
                    task.run_count += 1
                    task._calculate_next_run()
            
            # Sleep for a bit
            time.sleep(1)
    
    def get_tasks(self) -> List[Dict]:
        """Get all tasks info."""
        tasks_info = []
        
        for name, task in self.tasks.items():
            tasks_info.append({
                'name': name,
                'enabled': task.enabled,
                'next_run': task.next_run.isoformat() if task.next_run else None,
                'last_run': task.last_run.isoformat() if task.last_run else None,
                'run_count': task.run_count,
                'schedule': task.schedule
            })
        
        return tasks_info
    
    def get_status(self) -> Dict:
        """Get scheduler status."""
        return {
            'running': self.running,
            'total_tasks': len(self.tasks),
            'enabled_tasks': sum(1 for t in self.tasks.values() if t.enabled),
            'queue_status': self.task_queue.get_status()
        }


class TimerManager:
    """Manage one-time timers."""
    
    def __init__(self):
        self.timers = {}
    
    def set_timer(self, name: str, func: Callable, delay: float,
                 args: tuple = (), kwargs: Optional[dict] = None):
        """
        Set a one-time timer.
        
        Args:
            name: Timer name
            func: Function to call
            delay: Delay in seconds
            args: Function arguments
            kwargs: Function keyword arguments
        """
        def timer_func():
            time.sleep(delay)
            func(*args, **(kwargs or {}))
            if name in self.timers:
                del self.timers[name]
        
        timer_thread = threading.Thread(target=timer_func, daemon=True)
        timer_thread.start()
        
        self.timers[name] = {
            'thread': timer_thread,
            'started_at': datetime.now(),
            'delay': delay
        }
    
    def cancel_timer(self, name: str) -> bool:
        """Cancel a timer."""
        if name in self.timers:
            # Note: Can't actually stop a sleeping thread in Python
            # But we can remove it from our tracking
            del self.timers[name]
            return True
        return False
    
    def get_timers(self) -> List[Dict]:
        """Get active timers."""
        timers_info = []
        
        for name, timer in self.timers.items():
            elapsed = (datetime.now() - timer['started_at']).total_seconds()
            remaining = max(0, timer['delay'] - elapsed)
            
            timers_info.append({
                'name': name,
                'delay': timer['delay'],
                'elapsed': elapsed,
                'remaining': remaining
            })
        
        return timers_info


# Global instances
_scheduler = Scheduler()
_timer_manager = TimerManager()

def schedule_task(name: str, func: Callable, schedule: Dict,
                 args: tuple = (), kwargs: Optional[dict] = None):
    """Add task to global scheduler."""
    _scheduler.add_task(name, func, schedule, args, kwargs)

def start_scheduler():
    """Start global scheduler."""
    _scheduler.start()

def stop_scheduler():
    """Stop global scheduler."""
    _scheduler.stop()

def set_timer(name: str, func: Callable, delay: float):
    """Set a timer."""
    _timer_manager.set_timer(name, func, delay)

def get_scheduled_tasks() -> List[Dict]:
    """Get all scheduled tasks."""
    return _scheduler.get_tasks()
