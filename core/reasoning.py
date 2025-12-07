"""
Advanced Reasoning System for SuperAgent
Multi-step reasoning, logical deduction, problem decomposition
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
import re


class ReasoningType(Enum):
    """Types of reasoning strategies."""
    DEDUCTIVE = "deductive"  # General to specific
    INDUCTIVE = "inductive"  # Specific to general
    ABDUCTIVE = "abductive"  # Best explanation
    ANALOGICAL = "analogical"  # By similarity
    CAUSAL = "causal"  # Cause and effect
    FORWARD = "forward"  # Goal-driven
    BACKWARD = "backward"  # Data-driven


class ReasoningStep:
    """A single step in reasoning chain."""
    
    def __init__(self, step_type: str, input_data: Any, output: Any, 
                 confidence: float, reasoning: str):
        self.step_type = step_type
        self.input_data = input_data
        self.output = output
        self.confidence = confidence
        self.reasoning = reasoning
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'step_type': self.step_type,
            'input': str(self.input_data),
            'output': str(self.output),
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'timestamp': self.timestamp
        }


class ReasoningChain:
    """Chain of reasoning steps."""
    
    def __init__(self, problem: str):
        self.problem = problem
        self.steps: List[ReasoningStep] = []
        self.conclusion: Optional[str] = None
        self.overall_confidence = 1.0
    
    def add_step(self, step: ReasoningStep):
        """Add reasoning step and update confidence."""
        self.steps.append(step)
        # Confidence decreases with chain length (uncertainty propagation)
        self.overall_confidence *= step.confidence
    
    def get_chain_summary(self) -> str:
        """Get human-readable summary of reasoning chain."""
        summary = [f"Problem: {self.problem}\n"]
        summary.append("Reasoning Chain:")
        
        for i, step in enumerate(self.steps, 1):
            summary.append(f"\n{i}. {step.step_type.upper()}")
            summary.append(f"   Input: {step.input_data}")
            summary.append(f"   → {step.reasoning}")
            summary.append(f"   Output: {step.output}")
            summary.append(f"   Confidence: {step.confidence:.1%}")
        
        if self.conclusion:
            summary.append(f"\nConclusion: {self.conclusion}")
        summary.append(f"Overall Confidence: {self.overall_confidence:.1%}")
        
        return "\n".join(summary)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'problem': self.problem,
            'steps': [step.to_dict() for step in self.steps],
            'conclusion': self.conclusion,
            'confidence': self.overall_confidence
        }


class ProblemDecomposer:
    """Decompose complex problems into smaller subproblems."""
    
    def decompose(self, problem: str) -> List[Dict[str, Any]]:
        """
        Break down problem into manageable subproblems.
        
        Returns:
            List of subproblems with metadata
        """
        subproblems = []
        
        # Detect conjunctions (and, then, after, also)
        if any(word in problem.lower() for word in [' and ', ' then ', ' after ', ' also ']):
            # Split by conjunctions
            parts = re.split(r'\s+(?:and|then|after|also)\s+', problem, flags=re.IGNORECASE)
            for i, part in enumerate(parts):
                subproblems.append({
                    'id': i + 1,
                    'description': part.strip(),
                    'type': 'sequential' if 'then' in problem.lower() or 'after' in problem.lower() else 'parallel',
                    'dependencies': [i] if i > 0 and 'then' in problem.lower() else []
                })
        
        # Detect if-then conditions
        elif 'if' in problem.lower() and 'then' in problem.lower():
            match = re.search(r'if\s+(.+?)\s+then\s+(.+)', problem, re.IGNORECASE)
            if match:
                condition, action = match.groups()
                subproblems.append({
                    'id': 1,
                    'description': f"Check condition: {condition}",
                    'type': 'condition',
                    'dependencies': []
                })
                subproblems.append({
                    'id': 2,
                    'description': f"If true: {action}",
                    'type': 'conditional_action',
                    'dependencies': [1]
                })
        
        # Single complex problem - break by verbs
        elif len(problem.split()) > 10:
            # Identify main verbs/actions
            verbs = self._extract_actions(problem)
            for i, verb in enumerate(verbs):
                subproblems.append({
                    'id': i + 1,
                    'description': verb,
                    'type': 'action',
                    'dependencies': []
                })
        
        # Simple problem
        else:
            subproblems.append({
                'id': 1,
                'description': problem,
                'type': 'simple',
                'dependencies': []
            })
        
        return subproblems
    
    def _extract_actions(self, text: str) -> List[str]:
        """Extract action verbs from text."""
        action_verbs = ['read', 'write', 'create', 'delete', 'search', 'find', 
                       'analyze', 'compute', 'execute', 'run', 'fetch', 'send']
        actions = []
        
        for verb in action_verbs:
            if verb in text.lower():
                # Extract surrounding context
                pattern = rf'\b\w*{verb}\w*\s+[\w\s]{{0,30}}'
                matches = re.findall(pattern, text, re.IGNORECASE)
                actions.extend(matches)
        
        return actions[:5]  # Limit to 5 actions


class LogicalReasoner:
    """Perform logical reasoning operations."""
    
    def __init__(self):
        self.rules = []
        self.facts = set()
    
    def add_rule(self, premise: str, conclusion: str, confidence: float = 1.0):
        """Add logical rule: IF premise THEN conclusion."""
        self.rules.append({
            'premise': premise,
            'conclusion': conclusion,
            'confidence': confidence
        })
    
    def add_fact(self, fact: str):
        """Add known fact."""
        self.facts.add(fact)
    
    def deduce(self, goal: str) -> Tuple[bool, float, List[str]]:
        """
        Deduce if goal is true using rules and facts.
        
        Returns:
            (is_true, confidence, reasoning_path)
        """
        reasoning_path = []
        
        # Direct fact check
        if goal in self.facts:
            return True, 1.0, [f"Direct fact: {goal}"]
        
        # Apply rules
        for rule in self.rules:
            if rule['conclusion'] == goal:
                # Check if premise is true
                if rule['premise'] in self.facts:
                    reasoning_path.append(f"Rule: IF {rule['premise']} THEN {rule['conclusion']}")
                    reasoning_path.append(f"Fact: {rule['premise']} is true")
                    reasoning_path.append(f"Therefore: {goal} is true")
                    return True, rule['confidence'], reasoning_path
                
                # Recursive deduction for premise
                premise_true, conf, path = self.deduce(rule['premise'])
                if premise_true:
                    reasoning_path.extend(path)
                    reasoning_path.append(f"Rule: IF {rule['premise']} THEN {rule['conclusion']}")
                    reasoning_path.append(f"Therefore: {goal} is true")
                    return True, conf * rule['confidence'], reasoning_path
        
        return False, 0.0, [f"Cannot deduce: {goal}"]
    
    def abductive_reasoning(self, observation: str) -> List[Tuple[str, float]]:
        """
        Find best explanations for observation.
        
        Returns:
            List of (explanation, confidence) tuples
        """
        explanations = []
        
        for rule in self.rules:
            if rule['conclusion'] == observation:
                # This premise could explain the observation
                explanations.append((rule['premise'], rule['confidence']))
        
        # Sort by confidence
        explanations.sort(key=lambda x: x[1], reverse=True)
        return explanations


class CausalReasoner:
    """Reason about cause and effect relationships."""
    
    def __init__(self):
        self.causal_graph = {}  # cause -> [effects]
    
    def add_causal_link(self, cause: str, effect: str, strength: float = 1.0):
        """Add cause-effect relationship."""
        if cause not in self.causal_graph:
            self.causal_graph[cause] = []
        self.causal_graph[cause].append({
            'effect': effect,
            'strength': strength
        })
    
    def predict_effects(self, cause: str) -> List[Tuple[str, float]]:
        """Predict effects given a cause."""
        if cause not in self.causal_graph:
            return []
        
        return [(link['effect'], link['strength']) 
                for link in self.causal_graph[cause]]
    
    def find_causes(self, effect: str) -> List[Tuple[str, float]]:
        """Find possible causes for an effect."""
        causes = []
        
        for cause, links in self.causal_graph.items():
            for link in links:
                if link['effect'] == effect:
                    causes.append((cause, link['strength']))
        
        return causes
    
    def causal_chain(self, start: str, end: str, max_depth: int = 5) -> List[List[str]]:
        """Find causal chains from start to end."""
        chains = []
        
        def search(current: str, target: str, path: List[str], depth: int):
            if depth > max_depth:
                return
            
            if current == target:
                chains.append(path + [current])
                return
            
            effects = self.predict_effects(current)
            for effect, _ in effects:
                if effect not in path:  # Avoid cycles
                    search(effect, target, path + [current], depth + 1)
        
        search(start, end, [], 0)
        return chains


class AdvancedReasoner:
    """Main advanced reasoning system."""
    
    def __init__(self):
        self.decomposer = ProblemDecomposer()
        self.logical = LogicalReasoner()
        self.causal = CausalReasoner()
        self.reasoning_history = []
    
    def reason(self, problem: str, strategy: ReasoningType = ReasoningType.FORWARD,
              context: Optional[Dict[str, Any]] = None) -> ReasoningChain:
        """
        Perform advanced reasoning on problem.
        
        Args:
            problem: Problem to solve
            strategy: Reasoning strategy to use
            context: Additional context information
            
        Returns:
            ReasoningChain with steps and conclusion
        """
        chain = ReasoningChain(problem)
        
        # Step 1: Problem decomposition
        subproblems = self.decomposer.decompose(problem)
        chain.add_step(ReasoningStep(
            step_type="decomposition",
            input_data=problem,
            output=f"{len(subproblems)} subproblems identified",
            confidence=0.95,
            reasoning=f"Broke down complex problem into {len(subproblems)} manageable parts"
        ))
        
        # Step 2: Analyze subproblems
        for subproblem in subproblems:
            analysis = self._analyze_subproblem(subproblem, context)
            chain.add_step(ReasoningStep(
                step_type="analysis",
                input_data=subproblem['description'],
                output=analysis['solution_approach'],
                confidence=analysis['confidence'],
                reasoning=analysis['reasoning']
            ))
        
        # Step 3: Synthesize solution
        solution = self._synthesize_solution(subproblems, chain)
        chain.add_step(ReasoningStep(
            step_type="synthesis",
            input_data="All subproblem solutions",
            output=solution,
            confidence=0.85,
            reasoning="Combined individual solutions into complete solution"
        ))
        
        chain.conclusion = solution
        
        # Store in history
        self.reasoning_history.append(chain)
        
        return chain
    
    def _analyze_subproblem(self, subproblem: Dict, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze individual subproblem."""
        description = subproblem['description'].lower()
        
        # Identify action type
        if any(word in description for word in ['read', 'load', 'get', 'fetch']):
            approach = "Data retrieval operation"
            tool = "files or browser"
            confidence = 0.9
        elif any(word in description for word in ['write', 'save', 'create', 'store']):
            approach = "Data storage operation"
            tool = "files"
            confidence = 0.9
        elif any(word in description for word in ['search', 'find', 'query']):
            approach = "Search operation"
            tool = "browser"
            confidence = 0.85
        elif any(word in description for word in ['execute', 'run', 'command']):
            approach = "Command execution"
            tool = "shell"
            confidence = 0.8
        elif any(word in description for word in ['analyze', 'compute', 'calculate']):
            approach = "Computational analysis"
            tool = "brain or custom code"
            confidence = 0.75
        else:
            approach = "General task"
            tool = "multiple tools"
            confidence = 0.6
        
        return {
            'solution_approach': f"{approach} using {tool}",
            'confidence': confidence,
            'reasoning': f"Identified as {approach} based on keywords"
        }
    
    def _synthesize_solution(self, subproblems: List[Dict], chain: ReasoningChain) -> str:
        """Synthesize complete solution from subproblems."""
        if len(subproblems) == 1:
            return f"Execute: {subproblems[0]['description']}"
        
        # Check for sequential dependencies
        has_dependencies = any(subproblem['dependencies'] for subproblem in subproblems)
        
        if has_dependencies:
            solution = "Execute steps in sequence:\n"
            for i, subproblem in enumerate(subproblems, 1):
                solution += f"{i}. {subproblem['description']}\n"
        else:
            solution = "Execute steps in parallel:\n"
            for i, subproblem in enumerate(subproblems, 1):
                solution += f"- {subproblem['description']}\n"
        
        return solution.strip()
    
    def explain_reasoning(self, problem: str) -> str:
        """Provide detailed explanation of reasoning process."""
        chain = self.reason(problem)
        return chain.get_chain_summary()
    
    def what_if_analysis(self, scenario: str, changes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform what-if analysis.
        
        Args:
            scenario: Base scenario
            changes: Changes to apply
            
        Returns:
            Predicted outcomes
        """
        results = {
            'scenario': scenario,
            'changes': changes,
            'predicted_outcomes': [],
            'confidence': 0.7
        }
        
        # Analyze each change
        for change_type, change_value in changes.items():
            # Use causal reasoning
            effects = self.causal.predict_effects(change_type)
            
            for effect, strength in effects:
                results['predicted_outcomes'].append({
                    'effect': effect,
                    'likelihood': strength,
                    'reasoning': f"{change_type} causes {effect} with strength {strength}"
                })
        
        return results
    
    def compare_options(self, options: List[Dict[str, Any]], 
                       criteria: List[str]) -> Dict[str, Any]:
        """
        Compare multiple options against criteria.
        
        Args:
            options: List of options to compare
            criteria: Evaluation criteria
            
        Returns:
            Comparison results with recommendation
        """
        scores = []
        
        for option in options:
            score = 0
            details = []
            
            for criterion in criteria:
                # Simple scoring based on keyword match
                criterion_lower = criterion.lower()
                option_str = str(option).lower()
                
                if criterion_lower in option_str:
                    points = 1.0
                    score += points
                    details.append(f"Matches {criterion}: +{points}")
                else:
                    details.append(f"Doesn't match {criterion}: +0")
            
            scores.append({
                'option': option,
                'score': score,
                'max_score': len(criteria),
                'percentage': (score / len(criteria) * 100) if criteria else 0,
                'details': details
            })
        
        # Sort by score
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'comparisons': scores,
            'recommendation': scores[0]['option'] if scores else None,
            'reasoning': f"Scored highest with {scores[0]['percentage']:.0f}% match" if scores else "No clear winner"
        }
    
    def analogy_reasoning(self, source: str, target: str) -> Dict[str, Any]:
        """Reason by analogy from source to target."""
        return {
            'source': source,
            'target': target,
            'mapping': f"If {source} works in one context, {target} may work in similar context",
            'confidence': 0.6,
            'reasoning': "Analogical reasoning based on structural similarity"
        }
    
    def get_reasoning_stats(self) -> Dict[str, Any]:
        """Get statistics about reasoning performance."""
        if not self.reasoning_history:
            return {'total_reasonings': 0}
        
        total = len(self.reasoning_history)
        avg_steps = sum(len(chain.steps) for chain in self.reasoning_history) / total
        avg_confidence = sum(chain.overall_confidence for chain in self.reasoning_history) / total
        
        return {
            'total_reasonings': total,
            'average_steps': avg_steps,
            'average_confidence': avg_confidence,
            'reasoning_types': list(set(step.step_type for chain in self.reasoning_history for step in chain.steps))
        }


# Global instance
_reasoner = AdvancedReasoner()

def reason(problem: str, strategy: ReasoningType = ReasoningType.FORWARD) -> ReasoningChain:
    """Quick access to reasoning."""
    return _reasoner.reason(problem, strategy)

def explain_reasoning(problem: str) -> str:
    """Quick explanation."""
    return _reasoner.explain_reasoning(problem)

def compare_options(options: List[Dict], criteria: List[str]) -> Dict:
    """Quick option comparison."""
    return _reasoner.compare_options(options, criteria)
