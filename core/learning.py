"""
Advanced Learning System for SuperAgent
Self-improvement through experience and pattern recognition
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
from pathlib import Path
from collections import defaultdict
import math


class LearningMetrics:
    """Track and analyze performance metrics."""
    
    def __init__(self):
        self.metrics = {
            'accuracy': [],
            'speed': [],
            'success_rate': [],
            'tool_usage': defaultdict(int)
        }
    
    def record_execution(self, tool: str, success: bool, duration: float):
        """Record execution metrics."""
        self.metrics['tool_usage'][tool] += 1
        self.metrics['success_rate'].append(1 if success else 0)
        self.metrics['speed'].append(duration)
    
    def get_tool_reliability(self, tool: str) -> float:
        """Get reliability score for a tool (0-1)."""
        if tool not in self.metrics['tool_usage']:
            return 0.5  # Unknown
        
        # Calculate based on usage frequency and success
        usage = self.metrics['tool_usage'][tool]
        total_usage = sum(self.metrics['tool_usage'].values())
        usage_ratio = usage / total_usage if total_usage > 0 else 0
        
        return min(1.0, usage_ratio * 2)
    
    def get_overall_success_rate(self) -> float:
        """Calculate overall success rate."""
        if not self.metrics['success_rate']:
            return 0.0
        return sum(self.metrics['success_rate']) / len(self.metrics['success_rate'])
    
    def get_average_speed(self) -> float:
        """Get average execution speed."""
        if not self.metrics['speed']:
            return 0.0
        return sum(self.metrics['speed']) / len(self.metrics['speed'])


class PatternRecognizer:
    """Recognize patterns in agent behavior and outcomes."""
    
    def __init__(self):
        self.patterns = {}
        self.min_occurrences = 3
    
    def add_pattern(self, context: str, action: str, outcome: str):
        """Add a pattern observation."""
        key = f"{context}:{action}"
        if key not in self.patterns:
            self.patterns[key] = {'outcomes': [], 'count': 0}
        
        self.patterns[key]['outcomes'].append(outcome)
        self.patterns[key]['count'] += 1
    
    def predict_outcome(self, context: str, action: str) -> Optional[str]:
        """Predict outcome based on historical patterns."""
        key = f"{context}:{action}"
        if key not in self.patterns:
            return None
        
        pattern = self.patterns[key]
        if pattern['count'] < self.min_occurrences:
            return None
        
        # Return most common outcome
        from collections import Counter
        outcomes = Counter(pattern['outcomes'])
        return outcomes.most_common(1)[0][0]
    
    def get_confidence(self, context: str, action: str) -> float:
        """Get confidence in prediction (0-1)."""
        key = f"{context}:{action}"
        if key not in self.patterns or self.patterns[key]['count'] < self.min_occurrences:
            return 0.0
        
        pattern = self.patterns[key]
        from collections import Counter
        outcomes = Counter(pattern['outcomes'])
        most_common_count = outcomes.most_common(1)[0][1]
        
        return most_common_count / pattern['count']


class ExperienceMemory:
    """Store and retrieve past experiences."""
    
    def __init__(self, max_experiences: int = 1000):
        self.experiences = []
        self.max_experiences = max_experiences
        self.indexed_by_task = defaultdict(list)
        self.indexed_by_tool = defaultdict(list)
    
    def add_experience(self, task: str, tool: str, action: Dict, 
                      outcome: str, success: bool, duration: float,
                      context: Optional[Dict] = None):
        """Add a new experience."""
        experience = {
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'tool': tool,
            'action': action,
            'outcome': outcome,
            'success': success,
            'duration': duration,
            'context': context or {}
        }
        
        self.experiences.append(experience)
        self.indexed_by_task[task].append(experience)
        self.indexed_by_tool[tool].append(experience)
        
        # Keep only recent experiences
        if len(self.experiences) > self.max_experiences:
            old = self.experiences.pop(0)
            self.indexed_by_task[old['task']].remove(old)
            self.indexed_by_tool[old['tool']].remove(old)
    
    def find_similar_experiences(self, task: str, tool: Optional[str] = None, 
                                 limit: int = 5) -> List[Dict]:
        """Find similar past experiences."""
        candidates = self.indexed_by_task.get(task, [])
        
        if tool:
            candidates = [exp for exp in candidates if exp['tool'] == tool]
        
        # Sort by timestamp (most recent first)
        candidates.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return candidates[:limit]
    
    def get_success_rate_for_task(self, task: str, tool: Optional[str] = None) -> float:
        """Calculate success rate for specific task/tool combination."""
        experiences = self.find_similar_experiences(task, tool, limit=100)
        
        if not experiences:
            return 0.5  # Unknown
        
        successes = sum(1 for exp in experiences if exp['success'])
        return successes / len(experiences)
    
    def get_best_tool_for_task(self, task: str) -> Tuple[str, float]:
        """Determine best tool for a task based on experience."""
        experiences = self.indexed_by_task.get(task, [])
        
        if not experiences:
            return ("unknown", 0.0)
        
        tool_performance = defaultdict(lambda: {'successes': 0, 'total': 0})
        
        for exp in experiences:
            tool = exp['tool']
            tool_performance[tool]['total'] += 1
            if exp['success']:
                tool_performance[tool]['successes'] += 1
        
        # Find tool with highest success rate
        best_tool = None
        best_rate = 0.0
        
        for tool, perf in tool_performance.items():
            rate = perf['successes'] / perf['total']
            if rate > best_rate:
                best_rate = rate
                best_tool = tool
        
        return (best_tool or "unknown", best_rate)


class AdaptiveStrategy:
    """Adapt strategies based on learning."""
    
    def __init__(self):
        self.strategies = {}
        self.exploration_rate = 0.2  # 20% exploration, 80% exploitation
    
    def should_explore(self) -> bool:
        """Decide whether to explore new strategies or exploit known ones."""
        import random
        return random.random() < self.exploration_rate
    
    def adjust_exploration_rate(self, success_rate: float):
        """Adjust exploration rate based on current performance."""
        if success_rate > 0.8:
            # Performing well, explore less
            self.exploration_rate = max(0.1, self.exploration_rate * 0.9)
        elif success_rate < 0.5:
            # Performing poorly, explore more
            self.exploration_rate = min(0.4, self.exploration_rate * 1.1)
    
    def register_strategy(self, name: str, strategy: Dict):
        """Register a new strategy."""
        self.strategies[name] = {
            'config': strategy,
            'uses': 0,
            'successes': 0,
            'avg_duration': 0.0
        }
    
    def select_strategy(self, task_type: str) -> str:
        """Select best strategy for task type."""
        if not self.strategies or self.should_explore():
            return 'default'
        
        # Select strategy with best performance
        best_strategy = None
        best_score = -1
        
        for name, data in self.strategies.items():
            if data['uses'] == 0:
                continue
            
            success_rate = data['successes'] / data['uses']
            speed_bonus = 1.0 / (1.0 + data['avg_duration'])
            score = success_rate * 0.7 + speed_bonus * 0.3
            
            if score > best_score:
                best_score = score
                best_strategy = name
        
        return best_strategy or 'default'
    
    def update_strategy_performance(self, name: str, success: bool, duration: float):
        """Update strategy performance metrics."""
        if name not in self.strategies:
            return
        
        strategy = self.strategies[name]
        strategy['uses'] += 1
        if success:
            strategy['successes'] += 1
        
        # Update average duration
        n = strategy['uses']
        strategy['avg_duration'] = (strategy['avg_duration'] * (n-1) + duration) / n


class SelfLearningAgent:
    """Main self-learning system."""
    
    def __init__(self):
        self.metrics = LearningMetrics()
        self.patterns = PatternRecognizer()
        self.memory = ExperienceMemory()
        self.strategy = AdaptiveStrategy()
        self.learning_rate = 0.1
        self.improvement_threshold = 0.05
    
    def learn_from_execution(self, task: str, tool: str, action: Dict,
                            outcome: str, success: bool, duration: float,
                            context: Optional[Dict] = None):
        """Learn from a single execution."""
        # Record metrics
        self.metrics.record_execution(tool, success, duration)
        
        # Add to experience memory
        self.memory.add_experience(task, tool, action, outcome, success, duration, context)
        
        # Update pattern recognition
        task_type = context.get('task_type', 'general') if context else 'general'
        self.patterns.add_pattern(task_type, tool, 'success' if success else 'failure')
        
        # Adjust strategies
        overall_success = self.metrics.get_overall_success_rate()
        self.strategy.adjust_exploration_rate(overall_success)
    
    def get_recommendation(self, task: str, available_tools: List[str]) -> Dict[str, Any]:
        """Get intelligent recommendation for task execution."""
        recommendation = {
            'task': task,
            'recommended_tool': None,
            'confidence': 0.0,
            'predicted_outcome': None,
            'similar_experiences': [],
            'reasoning': []
        }
        
        # Find best tool based on experience
        best_tool, success_rate = self.memory.get_best_tool_for_task(task)
        
        if best_tool in available_tools:
            recommendation['recommended_tool'] = best_tool
            recommendation['confidence'] = success_rate
            recommendation['reasoning'].append(
                f"Tool '{best_tool}' has {success_rate:.1%} success rate for this task"
            )
        else:
            # Fall back to tool reliability
            tool_scores = {tool: self.metrics.get_tool_reliability(tool) 
                          for tool in available_tools}
            best_tool = max(tool_scores, key=lambda x: tool_scores[x])
            recommendation['recommended_tool'] = best_tool
            recommendation['confidence'] = tool_scores[best_tool]
            recommendation['reasoning'].append(
                f"Tool '{best_tool}' selected based on reliability score"
            )
        
        # Find similar past experiences
        similar = self.memory.find_similar_experiences(task, limit=3)
        recommendation['similar_experiences'] = [
            {
                'tool': exp['tool'],
                'success': exp['success'],
                'duration': exp['duration']
            }
            for exp in similar
        ]
        
        # Predict outcome
        task_type = self._classify_task(task)
        predicted = self.patterns.predict_outcome(task_type, recommendation['recommended_tool'])
        if predicted:
            recommendation['predicted_outcome'] = predicted
            confidence = self.patterns.get_confidence(task_type, recommendation['recommended_tool'])
            recommendation['reasoning'].append(
                f"Predicted outcome: {predicted} (confidence: {confidence:.1%})"
            )
        
        return recommendation
    
    def _classify_task(self, task: str) -> str:
        """Classify task type."""
        task_lower = task.lower()
        if 'file' in task_lower:
            return 'file_operation'
        elif 'web' in task_lower or 'search' in task_lower:
            return 'web_operation'
        elif 'shell' in task_lower or 'command' in task_lower:
            return 'shell_operation'
        return 'general'
    
    def get_learning_report(self) -> Dict[str, Any]:
        """Generate comprehensive learning report."""
        return {
            'overall_success_rate': self.metrics.get_overall_success_rate(),
            'average_speed': self.metrics.get_average_speed(),
            'total_experiences': len(self.memory.experiences),
            'patterns_learned': len(self.patterns.patterns),
            'exploration_rate': self.strategy.exploration_rate,
            'tool_usage': dict(self.metrics.metrics['tool_usage']),
            'most_reliable_tools': self._get_top_tools(3),
            'improvement_areas': self._identify_improvement_areas()
        }
    
    def _get_top_tools(self, n: int) -> List[Tuple[str, float]]:
        """Get top N most reliable tools."""
        tools = list(self.metrics.metrics['tool_usage'].keys())
        tool_scores = [(tool, self.metrics.get_tool_reliability(tool)) 
                      for tool in tools]
        tool_scores.sort(key=lambda x: x[1], reverse=True)
        return tool_scores[:n]
    
    def _identify_improvement_areas(self) -> List[str]:
        """Identify areas needing improvement."""
        areas = []
        
        success_rate = self.metrics.get_overall_success_rate()
        if success_rate < 0.6:
            areas.append("Overall success rate is low - need better tool selection")
        
        avg_speed = self.metrics.get_average_speed()
        if avg_speed > 5.0:
            areas.append("Average execution time is high - consider optimization")
        
        if len(self.memory.experiences) < 50:
            areas.append("Limited experience data - continue learning")
        
        return areas or ["Performance is good - maintain current strategies"]
    
    def save_learning_data(self, path: str):
        """Save all learning data to file."""
        data = {
            'metrics': {
                'success_rate': self.metrics.metrics['success_rate'],
                'speed': self.metrics.metrics['speed'],
                'tool_usage': dict(self.metrics.metrics['tool_usage'])
            },
            'patterns': self.patterns.patterns,
            'experiences': self.memory.experiences,
            'strategies': self.strategy.strategies,
            'config': {
                'learning_rate': self.learning_rate,
                'exploration_rate': self.strategy.exploration_rate
            }
        }
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def load_learning_data(self, path: str):
        """Load learning data from file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Restore metrics
            self.metrics.metrics['success_rate'] = data['metrics']['success_rate']
            self.metrics.metrics['speed'] = data['metrics']['speed']
            self.metrics.metrics['tool_usage'] = defaultdict(int, data['metrics']['tool_usage'])
            
            # Restore patterns
            self.patterns.patterns = data['patterns']
            
            # Restore experiences
            self.memory.experiences = data['experiences']
            # Rebuild indexes
            for exp in self.memory.experiences:
                self.memory.indexed_by_task[exp['task']].append(exp)
                self.memory.indexed_by_tool[exp['tool']].append(exp)
            
            # Restore strategies
            self.strategy.strategies = data['strategies']
            
            # Restore config
            if 'config' in data:
                self.learning_rate = data['config'].get('learning_rate', 0.1)
                self.strategy.exploration_rate = data['config'].get('exploration_rate', 0.2)
            
            return True
        except Exception as e:
            print(f"Error loading learning data: {e}")
            return False


# Global instance
_learning_agent = SelfLearningAgent()

def learn_from_execution(task: str, tool: str, action: Dict, outcome: str, 
                        success: bool, duration: float, context: Optional[Dict] = None):
    """Quick access to learning function."""
    _learning_agent.learn_from_execution(task, tool, action, outcome, success, duration, context)

def get_recommendation(task: str, available_tools: List[str]) -> Dict[str, Any]:
    """Quick access to recommendation function."""
    return _learning_agent.get_recommendation(task, available_tools)

def get_learning_report() -> Dict[str, Any]:
    """Quick access to learning report."""
    return _learning_agent.get_learning_report()
