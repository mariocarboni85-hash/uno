"""
Collaborative Learning System - Sistema di apprendimento collaborativo tra agenti
"""

import time
import json
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import random


class LearningStrategy(Enum):
    """Strategie di apprendimento"""
    IMITATION = "imitation"  # Copia comportamento
    REINFORCEMENT = "reinforcement"  # Feedback-based
    COLLABORATIVE = "collaborative"  # Lavoro condiviso
    COMPETITIVE = "competitive"  # Competizione
    TRANSFER = "transfer"  # Transfer learning
    META = "meta"  # Meta-learning


class ExperienceType(Enum):
    """Tipi di esperienza"""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    OBSERVATION = "observation"
    TEACHING = "teaching"


@dataclass
class Experience:
    """Esperienza di apprendimento"""
    id: str
    agent_id: str
    timestamp: float
    experience_type: ExperienceType
    context: Dict[str, Any]
    action: str
    result: Any
    reward: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'timestamp': self.timestamp,
            'type': self.experience_type.value,
            'context': self.context,
            'action': self.action,
            'result': self.result,
            'reward': self.reward,
            'metadata': self.metadata
        }


@dataclass
class Skill:
    """Skill appreso"""
    name: str
    description: str
    proficiency: float  # 0.0 - 1.0
    learned_from: List[str] = field(default_factory=list)
    practice_count: int = 0
    success_rate: float = 0.0
    last_used: Optional[float] = None
    
    def improve(self, success: bool):
        """Migliora skill con pratica"""
        self.practice_count += 1
        alpha = 0.1  # Learning rate
        
        if success:
            self.proficiency = min(1.0, self.proficiency + alpha * (1.0 - self.proficiency))
            self.success_rate = (self.success_rate * (self.practice_count - 1) + 1.0) / self.practice_count
        else:
            self.proficiency = max(0.0, self.proficiency - alpha * 0.1)
            self.success_rate = (self.success_rate * (self.practice_count - 1)) / self.practice_count
        
        self.last_used = time.time()


@dataclass
class KnowledgeItem:
    """Item di conoscenza condivisa"""
    id: str
    source_agent: str
    content: Any
    confidence: float
    category: str
    created_at: float
    votes: int = 0
    validated: bool = False
    
    def vote(self, positive: bool = True):
        """Vota conoscenza"""
        self.votes += 1 if positive else -1
        # Update confidence based on votes
        self.confidence = min(1.0, max(0.0, 0.5 + self.votes * 0.1))


class LearningAgent:
    """Agente con capacità di apprendimento"""
    
    def __init__(self, agent_id: str, initial_skills: Optional[List[str]] = None):
        self.id = agent_id
        self.skills: Dict[str, Skill] = {}
        self.experiences: List[Experience] = []
        self.knowledge_base: Dict[str, Any] = {}
        
        self.learning_rate = 0.1
        self.exploration_rate = 0.2
        self.imitation_threshold = 0.7
        
        self.stats = {
            'total_experiences': 0,
            'successful_actions': 0,
            'failed_actions': 0,
            'skills_learned': 0,
            'knowledge_shared': 0,
            'collaborations': 0
        }
        
        # Initialize with basic skills
        if initial_skills:
            for skill_name in initial_skills:
                self.add_skill(skill_name, f"Initial skill: {skill_name}", 0.3)
    
    def add_skill(self, name: str, description: str, 
                 proficiency: float = 0.0, learned_from: Optional[str] = None):
        """Aggiungi skill"""
        if name not in self.skills:
            self.skills[name] = Skill(
                name=name,
                description=description,
                proficiency=proficiency,
                learned_from=[learned_from] if learned_from else []
            )
            self.stats['skills_learned'] += 1
    
    def learn_from_experience(self, experience: Experience):
        """Apprendi da esperienza"""
        self.experiences.append(experience)
        self.stats['total_experiences'] += 1
        
        # Update relevant skills
        if experience.experience_type == ExperienceType.SUCCESS:
            self.stats['successful_actions'] += 1
            # Extract skill from action
            skill_name = experience.action.split('_')[0]
            if skill_name in self.skills:
                self.skills[skill_name].improve(success=True)
        
        elif experience.experience_type == ExperienceType.FAILURE:
            self.stats['failed_actions'] += 1
            skill_name = experience.action.split('_')[0]
            if skill_name in self.skills:
                self.skills[skill_name].improve(success=False)
    
    def observe_agent(self, other_agent: 'LearningAgent', 
                     action: str, result: Any, success: bool) -> bool:
        """Osserva altro agente e impara"""
        # Check if worth imitating
        if success and random.random() < self.imitation_threshold:
            # Extract skill
            skill_name = action.split('_')[0]
            
            # Learn new skill or improve existing
            if skill_name not in self.skills:
                self.add_skill(
                    skill_name,
                    f"Learned by observing {other_agent.id}",
                    proficiency=0.3,
                    learned_from=other_agent.id
                )
            else:
                # Improve through observation
                self.skills[skill_name].improve(success=True)
            
            # Record observation experience
            exp = Experience(
                id=f"obs_{len(self.experiences)}",
                agent_id=self.id,
                timestamp=time.time(),
                experience_type=ExperienceType.OBSERVATION,
                context={'observed': other_agent.id},
                action=action,
                result=result,
                reward=0.5 if success else 0.0
            )
            self.learn_from_experience(exp)
            
            return True
        
        return False
    
    def teach_skill(self, student: 'LearningAgent', skill_name: str) -> bool:
        """Insegna skill ad altro agente"""
        if skill_name not in self.skills:
            return False
        
        skill = self.skills[skill_name]
        
        # Transfer skill with reduced proficiency
        transfer_proficiency = skill.proficiency * 0.7
        student.add_skill(
            skill_name,
            f"Taught by {self.id}: {skill.description}",
            proficiency=transfer_proficiency,
            learned_from=self.id
        )
        
        # Record teaching experience
        exp = Experience(
            id=f"teach_{len(self.experiences)}",
            agent_id=self.id,
            timestamp=time.time(),
            experience_type=ExperienceType.TEACHING,
            context={'student': student.id, 'skill': skill_name},
            action='teach',
            result='skill_transferred',
            reward=0.3
        )
        self.learn_from_experience(exp)
        self.stats['knowledge_shared'] += 1
        
        return True
    
    def collaborate(self, other_agent: 'LearningAgent', 
                   task: str) -> Tuple[bool, Any]:
        """Collabora con altro agente"""
        self.stats['collaborations'] += 1
        other_agent.stats['collaborations'] += 1
        
        # Combine skills
        my_skills = set(self.skills.keys())
        their_skills = set(other_agent.skills.keys())
        combined_skills = my_skills.union(their_skills)
        
        # Calculate success probability
        skill_name = task.split('_')[0]
        
        my_prof = self.skills.get(skill_name, Skill(skill_name, "", 0.0)).proficiency
        their_prof = other_agent.skills.get(skill_name, Skill(skill_name, "", 0.0)).proficiency
        
        # Collaboration bonus
        combined_proficiency = (my_prof + their_prof) / 2 * 1.2
        success_prob = min(0.95, combined_proficiency)
        
        success = random.random() < success_prob
        
        # Both agents learn from collaboration
        result = f"Collaboration on {task}: {'success' if success else 'failure'}"
        
        exp_self = Experience(
            id=f"collab_{len(self.experiences)}",
            agent_id=self.id,
            timestamp=time.time(),
            experience_type=ExperienceType.SUCCESS if success else ExperienceType.FAILURE,
            context={'collaborator': other_agent.id, 'task': task},
            action='collaborate',
            result=result,
            reward=1.0 if success else 0.2
        )
        self.learn_from_experience(exp_self)
        
        exp_other = Experience(
            id=f"collab_{len(other_agent.experiences)}",
            agent_id=other_agent.id,
            timestamp=time.time(),
            experience_type=ExperienceType.SUCCESS if success else ExperienceType.FAILURE,
            context={'collaborator': self.id, 'task': task},
            action='collaborate',
            result=result,
            reward=1.0 if success else 0.2
        )
        other_agent.learn_from_experience(exp_other)
        
        # Share knowledge from experience
        if success:
            # Both agents improve relevant skill
            if skill_name in self.skills:
                self.skills[skill_name].improve(success=True)
            if skill_name in other_agent.skills:
                other_agent.skills[skill_name].improve(success=True)
        
        return success, result
    
    def get_best_skill(self) -> Optional[Skill]:
        """Ottieni migliore skill"""
        if not self.skills:
            return None
        return max(self.skills.values(), key=lambda s: s.proficiency)
    
    def get_skills_summary(self) -> Dict[str, Any]:
        """Summary skills"""
        summary: Dict[str, Any] = {
            'total_skills': len(self.skills),
            'skills': {
                name: {
                    'proficiency': skill.proficiency,
                    'practice_count': skill.practice_count,
                    'success_rate': skill.success_rate
                }
                for name, skill in self.skills.items()
            }
        }

        best = self.get_best_skill()
        summary['best_skill'] = best.name if best is not None else None
        return summary
    
    def export_knowledge(self) -> Dict[str, Any]:
        """Esporta conoscenza"""
        return {
            'agent_id': self.id,
            'skills': {
                name: {
                    'name': skill.name,
                    'description': skill.description,
                    'proficiency': skill.proficiency,
                    'practice_count': skill.practice_count,
                    'success_rate': skill.success_rate
                }
                for name, skill in self.skills.items()
            },
            'experiences': [exp.to_dict() for exp in self.experiences[-10:]],  # Last 10
            'stats': self.stats
        }
    
    def import_knowledge(self, knowledge: Dict[str, Any], trust_factor: float = 0.5):
        """Importa conoscenza da altro agente"""
        # Import skills with reduced proficiency
        for skill_name, skill_data in knowledge.get('skills', {}).items():
            if skill_name not in self.skills:
                self.add_skill(
                    skill_name,
                    skill_data['description'],
                    proficiency=skill_data['proficiency'] * trust_factor,
                    learned_from=knowledge['agent_id']
                )


class SharedKnowledgeBase:
    """Knowledge base condiviso tra agenti"""
    
    def __init__(self):
        self.knowledge: Dict[str, KnowledgeItem] = {}
        self.categories: Set[str] = set()
        self.contributions: Dict[str, int] = {}  # agent_id -> count
        
    def add_knowledge(self, source_agent: str, content: Any,
                     category: str, confidence: float = 0.5) -> str:
        """Aggiungi conoscenza"""
        knowledge_id = f"k_{len(self.knowledge)}_{source_agent}"
        
        item = KnowledgeItem(
            id=knowledge_id,
            source_agent=source_agent,
            content=content,
            confidence=confidence,
            category=category,
            created_at=time.time()
        )
        
        self.knowledge[knowledge_id] = item
        self.categories.add(category)
        
        if source_agent not in self.contributions:
            self.contributions[source_agent] = 0
        self.contributions[source_agent] += 1
        
        return knowledge_id
    
    def query_knowledge(self, category: Optional[str] = None,
                       min_confidence: float = 0.5) -> List[KnowledgeItem]:
        """Query knowledge base"""
        results = []
        
        for item in self.knowledge.values():
            if item.confidence >= min_confidence:
                if category is None or item.category == category:
                    results.append(item)
        
        # Sort by confidence and votes
        results.sort(key=lambda x: (x.confidence, x.votes), reverse=True)
        return results
    
    def vote_knowledge(self, knowledge_id: str, positive: bool = True):
        """Vota conoscenza"""
        if knowledge_id in self.knowledge:
            self.knowledge[knowledge_id].vote(positive)
    
    def validate_knowledge(self, knowledge_id: str):
        """Valida conoscenza"""
        if knowledge_id in self.knowledge:
            self.knowledge[knowledge_id].validated = True
            self.knowledge[knowledge_id].confidence = min(1.0, 
                                                          self.knowledge[knowledge_id].confidence + 0.2)
    
    def get_stats(self) -> Dict[str, Any]:
        """Statistiche knowledge base"""
        validated_count = sum(1 for k in self.knowledge.values() if k.validated)
        
        return {
            'total_items': len(self.knowledge),
            'categories': len(self.categories),
            'validated_items': validated_count,
            'top_contributors': sorted(
                self.contributions.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }


class CollaborativeLearningEnvironment:
    """Ambiente di apprendimento collaborativo"""
    
    def __init__(self, name: str):
        self.name = name
        self.agents: Dict[str, LearningAgent] = {}
        self.shared_knowledge = SharedKnowledgeBase()
        self.interaction_history: List[Dict[str, Any]] = []
        
        self.stats = {
            'total_interactions': 0,
            'successful_collaborations': 0,
            'teaching_events': 0,
            'observations': 0,
            'knowledge_transfers': 0
        }
    
    def add_agent(self, agent: LearningAgent):
        """Aggiungi agente all'ambiente"""
        self.agents[agent.id] = agent
    
    def create_agent(self, agent_id: str, initial_skills: Optional[List[str]] = None) -> LearningAgent:
        """Crea e aggiungi agente"""
        agent = LearningAgent(agent_id, initial_skills)
        self.add_agent(agent)
        return agent
    
    def facilitate_teaching(self, teacher_id: str, student_id: str, 
                          skill_name: str) -> bool:
        """Facilita insegnamento tra agenti"""
        if teacher_id not in self.agents or student_id not in self.agents:
            return False
        
        teacher = self.agents[teacher_id]
        student = self.agents[student_id]
        
        success = teacher.teach_skill(student, skill_name)
        
        if success:
            self.stats['teaching_events'] += 1
            self.stats['knowledge_transfers'] += 1
            
            self.interaction_history.append({
                'type': 'teaching',
                'teacher': teacher_id,
                'student': student_id,
                'skill': skill_name,
                'timestamp': time.time(),
                'success': success
            })
        
        return success
    
    def facilitate_collaboration(self, agent1_id: str, agent2_id: str,
                                task: str) -> Tuple[bool, Any]:
        """Facilita collaborazione tra agenti"""
        if agent1_id not in self.agents or agent2_id not in self.agents:
            return False, "Agents not found"
        
        agent1 = self.agents[agent1_id]
        agent2 = self.agents[agent2_id]
        
        success, result = agent1.collaborate(agent2, task)
        
        self.stats['total_interactions'] += 1
        if success:
            self.stats['successful_collaborations'] += 1
        
        self.interaction_history.append({
            'type': 'collaboration',
            'agents': [agent1_id, agent2_id],
            'task': task,
            'timestamp': time.time(),
            'success': success,
            'result': result
        })
        
        return success, result
    
    def facilitate_observation(self, observer_id: str, observed_id: str,
                             action: str, result: Any, success: bool):
        """Facilita osservazione tra agenti"""
        if observer_id not in self.agents or observed_id not in self.agents:
            return
        
        observer = self.agents[observer_id]
        observed = self.agents[observed_id]
        
        learned = observer.observe_agent(observed, action, result, success)
        
        if learned:
            self.stats['observations'] += 1
            
            self.interaction_history.append({
                'type': 'observation',
                'observer': observer_id,
                'observed': observed_id,
                'action': action,
                'timestamp': time.time(),
                'learned': learned
            })
    
    def share_agent_knowledge(self, source_agent_id: str, 
                            category: str = "general"):
        """Condividi conoscenza di agente nel knowledge base"""
        if source_agent_id not in self.agents:
            return
        
        agent = self.agents[source_agent_id]
        knowledge = agent.export_knowledge()
        
        # Add to shared knowledge base
        self.shared_knowledge.add_knowledge(
            source_agent_id,
            knowledge,
            category,
            confidence=0.7
        )
        
        self.stats['knowledge_transfers'] += 1
    
    def distribute_knowledge(self, category: Optional[str] = None,
                           trust_factor: float = 0.5):
        """Distribuisci conoscenza a tutti gli agenti"""
        knowledge_items = self.shared_knowledge.query_knowledge(category)
        
        for agent in self.agents.values():
            for item in knowledge_items:
                if item.source_agent != agent.id:  # Don't import own knowledge
                    agent.import_knowledge(item.content, trust_factor)
    
    def run_collaborative_session(self, num_interactions: int = 50):
        """Esegui sessione collaborativa"""
        agent_ids = list(self.agents.keys())
        
        if len(agent_ids) < 2:
            return
        
        for _ in range(num_interactions):
            # Random interaction type
            interaction_type = random.choice(['teach', 'collaborate', 'observe'])
            
            # Pick random agents
            agent1_id = random.choice(agent_ids)
            agent2_id = random.choice([a for a in agent_ids if a != agent1_id])
            
            if interaction_type == 'teach':
                # Random skill from agent1
                agent1 = self.agents[agent1_id]
                if agent1.skills:
                    skill = random.choice(list(agent1.skills.keys()))
                    self.facilitate_teaching(agent1_id, agent2_id, skill)
            
            elif interaction_type == 'collaborate':
                # Random task
                tasks = ['code_feature', 'analyze_data', 'design_system', 
                        'test_code', 'optimize_performance']
                task = random.choice(tasks)
                self.facilitate_collaboration(agent1_id, agent2_id, task)
            
            elif interaction_type == 'observe':
                # Agent2 observes agent1
                actions = ['code_implement', 'test_validate', 'analyze_metrics',
                          'design_interface', 'optimize_query']
                action = random.choice(actions)
                success = random.random() < 0.7
                result = "success" if success else "failure"
                self.facilitate_observation(agent2_id, agent1_id, action, result, success)
        
        # Share knowledge at end
        for agent_id in agent_ids:
            self.share_agent_knowledge(agent_id)
        
        # Distribute knowledge
        self.distribute_knowledge(trust_factor=0.6)
    
    def get_environment_stats(self) -> Dict[str, Any]:
        """Statistiche ambiente"""
        agent_stats = {
            agent_id: agent.stats
            for agent_id, agent in self.agents.items()
        }
        
        return {
            'environment': self.name,
            'total_agents': len(self.agents),
            'environment_stats': self.stats,
            'agent_stats': agent_stats,
            'knowledge_base': self.shared_knowledge.get_stats(),
            'recent_interactions': self.interaction_history[-10:]
        }
    
    def get_learning_progress(self) -> Dict[str, Any]:
        """Progress di apprendimento agenti"""
        progress = {}
        
        for agent_id, agent in self.agents.items():
            total_proficiency = sum(s.proficiency for s in agent.skills.values())
            avg_proficiency = total_proficiency / len(agent.skills) if agent.skills else 0.0
            
            progress[agent_id] = {
                'total_skills': len(agent.skills),
                'avg_proficiency': avg_proficiency,
                'total_experiences': len(agent.experiences),
                'success_rate': (agent.stats['successful_actions'] / 
                               max(1, agent.stats['successful_actions'] + agent.stats['failed_actions']))
            }
        
        return progress


if __name__ == "__main__":
    print("Collaborative Learning System")
    print("=" * 80)
    
    # Create environment
    env = CollaborativeLearningEnvironment("LearningLab")
    
    # Create agents with different initial skills
    agent1 = env.create_agent("agent_1", ["code", "test"])
    agent2 = env.create_agent("agent_2", ["design", "analyze"])
    agent3 = env.create_agent("agent_3", ["optimize", "monitor"])
    
    print(f"\n[*] Created {len(env.agents)} agents")
    
    # Teaching
    print("\n[*] Teaching skills...")
    env.facilitate_teaching("agent_1", "agent_2", "code")
    
    # Collaboration
    print("[*] Collaborative tasks...")
    success, result = env.facilitate_collaboration("agent_1", "agent_2", "code_feature")
    print(f"   Collaboration: {result}")
    
    # Run session
    print("\n[*] Running collaborative session...")
    env.run_collaborative_session(num_interactions=30)
    
    # Stats
    print("\n[OK] Environment statistics:")
    stats = env.get_environment_stats()
    print(f"   Interactions: {stats['environment_stats']['total_interactions']}")
    print(f"   Collaborations: {stats['environment_stats']['successful_collaborations']}")
    print(f"   Teaching events: {stats['environment_stats']['teaching_events']}")
    
    print("\n[OK] Collaborative learning system initialized!")
