"""
Multi-Agent Ecosystem - Sistema per orchestrare ecosistemi di agenti collaborativi
"""

import time
import json
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import random
from pathlib import Path


class AgentRole(Enum):
    """Ruoli agenti nell'ecosistema"""
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    DEVELOPER = "developer"
    TESTER = "tester"
    ANALYST = "analyst"
    DESIGNER = "designer"
    OPTIMIZER = "optimizer"
    MONITOR = "monitor"
    COMMUNICATOR = "communicator"
    SECURITY = "security"


class AgentState(Enum):
    """Stati agente"""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority(Enum):
    """Priorità task"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class MessageType(Enum):
    """Tipi messaggio tra agenti"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    QUERY = "query"
    COMMAND = "command"
    BROADCAST = "broadcast"


@dataclass
class Message:
    """Messaggio tra agenti"""
    id: str
    type: MessageType
    sender: str
    receiver: str
    content: Any
    timestamp: float
    priority: TaskPriority = TaskPriority.MEDIUM
    requires_response: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type.value,
            'sender': self.sender,
            'receiver': self.receiver,
            'content': self.content,
            'timestamp': self.timestamp,
            'priority': self.priority.value,
            'requires_response': self.requires_response
        }


@dataclass
class Task:
    """Task nell'ecosistema"""
    id: str
    name: str
    description: str
    assigned_to: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.MEDIUM
    state: str = "pending"
    progress: float = 0.0
    result: Optional[Any] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'assigned_to': self.assigned_to,
            'dependencies': self.dependencies,
            'priority': self.priority.value,
            'state': self.state,
            'progress': self.progress,
            'result': self.result,
            'started_at': self.started_at,
            'completed_at': self.completed_at
        }


class Agent:
    """Agente base nell'ecosistema"""
    
    def __init__(self, agent_id: str, role: AgentRole, 
                 capabilities: Optional[List[str]] = None,
                 max_concurrent_tasks: int = 3):
        self.id = agent_id
        self.role = role
        self.capabilities = capabilities or []
        self.state = AgentState.IDLE
        self.max_concurrent_tasks = max_concurrent_tasks
        
        self.current_tasks: List[Task] = []
        self.completed_tasks: List[str] = []
        self.inbox: List[Message] = []
        self.knowledge_base: Dict[str, Any] = {}
        
        self.stats = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'messages_sent': 0,
            'messages_received': 0,
            'total_work_time': 0.0
        }
    
    def can_handle_task(self, task: Task) -> bool:
        """Check se l'agente può gestire il task"""
        if len(self.current_tasks) >= self.max_concurrent_tasks:
            return False
        
        # Check capabilities
        required_cap = task.name.split('_')[0].lower()
        return required_cap in [cap.lower() for cap in self.capabilities]
    
    def assign_task(self, task: Task):
        """Assegna task all'agente"""
        task.assigned_to = self.id
        task.state = "assigned"
        self.current_tasks.append(task)
        self.state = AgentState.WORKING
    
    def work_on_tasks(self, ecosystem: 'MultiAgentEcosystem', time_delta: float = 1.0) -> List[Task]:
        """Lavora sui task assegnati"""
        completed = []
        
        for task in self.current_tasks[:]:
            if task.state == "assigned":
                task.state = "in_progress"
                task.started_at = time.time()
            
            if task.state == "in_progress":
                # Simulate work progress
                work_amount = time_delta * 0.1  # 10% per step
                task.progress = min(1.0, task.progress + work_amount)
                
                # Complete task
                if task.progress >= 1.0:
                    task.state = "completed"
                    task.completed_at = time.time()
                    task.result = self._execute_task(task, ecosystem)
                    
                    self.current_tasks.remove(task)
                    self.completed_tasks.append(task.id)
                    self.stats['tasks_completed'] += 1
                    completed.append(task)
        
        if not self.current_tasks:
            self.state = AgentState.IDLE
        
        return completed
    
    def _execute_task(self, task: Task, ecosystem: 'MultiAgentEcosystem') -> Any:
        """Esegui task specifico"""
        # Role-specific execution
        if self.role == AgentRole.RESEARCHER:
            return {
                'type': 'research',
                'findings': f"Research completed for: {task.name}",
                'data': {'confidence': 0.85, 'sources': 3}
            }
        elif self.role == AgentRole.DEVELOPER:
            return {
                'type': 'code',
                'code': f"def {task.name}():\n    # Implementation\n    pass",
                'tests': ['test_basic', 'test_edge_cases']
            }
        elif self.role == AgentRole.TESTER:
            return {
                'type': 'test_results',
                'passed': 8,
                'failed': 2,
                'coverage': 0.85
            }
        elif self.role == AgentRole.ANALYST:
            return {
                'type': 'analysis',
                'metrics': {'performance': 0.92, 'quality': 0.88},
                'recommendations': ['optimize_query', 'add_caching']
            }
        else:
            return {'status': 'completed', 'task': task.name}
    
    def send_message(self, ecosystem: 'MultiAgentEcosystem', 
                    receiver: str, message_type: MessageType,
                    content: Any, priority: TaskPriority = TaskPriority.MEDIUM):
        """Invia messaggio ad altro agente"""
        msg = Message(
            id=f"msg_{self.id}_{len(ecosystem.messages)}",
            type=message_type,
            sender=self.id,
            receiver=receiver,
            content=content,
            timestamp=time.time(),
            priority=priority
        )
        
        ecosystem.deliver_message(msg)
        self.stats['messages_sent'] += 1
    
    def receive_message(self, message: Message):
        """Ricevi messaggio"""
        self.inbox.append(message)
        self.stats['messages_received'] += 1
    
    def process_messages(self, ecosystem: 'MultiAgentEcosystem'):
        """Processa messaggi inbox"""
        for msg in self.inbox[:]:
            self._handle_message(msg, ecosystem)
            self.inbox.remove(msg)
    
    def _handle_message(self, msg: Message, ecosystem: 'MultiAgentEcosystem'):
        """Gestisci messaggio"""
        if msg.type == MessageType.REQUEST:
            # Respond to request
            response_content = f"Response to: {msg.content}"
            self.send_message(
                ecosystem, msg.sender, MessageType.RESPONSE,
                response_content
            )
        elif msg.type == MessageType.QUERY:
            # Answer query from knowledge base
            answer = self.knowledge_base.get(str(msg.content), "Unknown")
            self.send_message(
                ecosystem, msg.sender, MessageType.RESPONSE, answer
            )
    
    def share_knowledge(self, key: str, value: Any):
        """Aggiungi conoscenza al knowledge base"""
        self.knowledge_base[key] = value
    
    def get_status(self) -> Dict[str, Any]:
        """Status agente"""
        return {
            'id': self.id,
            'role': self.role.value,
            'state': self.state.value,
            'current_tasks': len(self.current_tasks),
            'completed_tasks': len(self.completed_tasks),
            'inbox_size': len(self.inbox),
            'stats': self.stats
        }


class MultiAgentEcosystem:
    """Ecosistema multi-agente"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.messages: List[Message] = []
        self.global_knowledge: Dict[str, Any] = {}
        
        self.stats = {
            'total_agents': 0,
            'total_tasks': 0,
            'tasks_completed': 0,
            'messages_exchanged': 0,
            'simulation_time': 0.0
        }
        
        self.created_at = time.time()
        self.running = False
    
    def add_agent(self, agent: Agent):
        """Aggiungi agente all'ecosistema"""
        self.agents[agent.id] = agent
        self.stats['total_agents'] += 1
    
    def create_agent(self, agent_id: str, role: AgentRole, 
                    capabilities: Optional[List[str]] = None) -> Agent:
        """Crea e aggiungi agente"""
        agent = Agent(agent_id, role, capabilities)
        self.add_agent(agent)
        return agent
    
    def add_task(self, task: Task):
        """Aggiungi task all'ecosistema"""
        self.tasks[task.id] = task
        self.stats['total_tasks'] += 1
    
    def create_task(self, task_id: str, name: str, description: str,
                   dependencies: Optional[List[str]] = None,
                   priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        """Crea e aggiungi task"""
        task = Task(
            id=task_id,
            name=name,
            description=description,
            dependencies=dependencies or [],
            priority=priority
        )
        self.add_task(task)
        return task
    
    def assign_tasks(self):
        """Assegna task agli agenti disponibili"""
        # Get pending tasks sorted by priority
        pending = [t for t in self.tasks.values() if t.state == "pending"]
        pending.sort(key=lambda t: t.priority.value, reverse=True)
        
        for task in pending:
            # Check dependencies
            if not self._dependencies_met(task):
                continue
            
            # Find suitable agent
            for agent in self.agents.values():
                if agent.can_handle_task(task):
                    agent.assign_task(task)
                    break
    
    def _dependencies_met(self, task: Task) -> bool:
        """Check se le dipendenze del task sono soddisfatte"""
        for dep_id in task.dependencies:
            dep_task = self.tasks.get(dep_id)
            if not dep_task or dep_task.state != "completed":
                return False
        return True
    
    def deliver_message(self, message: Message):
        """Consegna messaggio al destinatario"""
        self.messages.append(message)
        self.stats['messages_exchanged'] += 1
        
        if message.receiver in self.agents:
            self.agents[message.receiver].receive_message(message)
        elif message.receiver == "broadcast":
            # Broadcast a tutti gli agenti
            for agent in self.agents.values():
                if agent.id != message.sender:
                    agent.receive_message(message)
    
    def step(self, time_delta: float = 1.0):
        """Esegui step di simulazione"""
        # Assign pending tasks
        self.assign_tasks()
        
        # Agents work on tasks
        all_completed = []
        for agent in self.agents.values():
            completed = agent.work_on_tasks(self, time_delta)
            all_completed.extend(completed)
        
        # Process messages
        for agent in self.agents.values():
            agent.process_messages(self)
        
        # Update stats
        self.stats['simulation_time'] += time_delta
        self.stats['tasks_completed'] = len([t for t in self.tasks.values() if t.state == "completed"])
        
        return all_completed
    
    def run(self, max_steps: int = 100, time_delta: float = 1.0) -> Dict[str, Any]:
        """Esegui simulazione completa"""
        self.running = True
        step_count = 0
        
        while step_count < max_steps and self.running:
            completed = self.step(time_delta)
            step_count += 1
            
            # Check if all tasks completed
            pending = [t for t in self.tasks.values() if t.state != "completed"]
            if not pending:
                break
        
        self.running = False
        
        return {
            'steps': step_count,
            'tasks_completed': self.stats['tasks_completed'],
            'total_tasks': self.stats['total_tasks'],
            'messages_exchanged': self.stats['messages_exchanged'],
            'simulation_time': self.stats['simulation_time']
        }
    
    def get_agent_by_role(self, role: AgentRole) -> Optional[Agent]:
        """Ottieni primo agente con ruolo specifico"""
        for agent in self.agents.values():
            if agent.role == role:
                return agent
        return None
    
    def get_agents_by_role(self, role: AgentRole) -> List[Agent]:
        """Ottieni tutti gli agenti con ruolo specifico"""
        return [a for a in self.agents.values() if a.role == role]
    
    def broadcast_knowledge(self, key: str, value: Any):
        """Condividi conoscenza con tutti gli agenti"""
        self.global_knowledge[key] = value
        for agent in self.agents.values():
            agent.share_knowledge(key, value)
    
    def get_status(self) -> Dict[str, Any]:
        """Status completo ecosistema"""
        return {
            'name': self.name,
            'description': self.description,
            'agents': {aid: a.get_status() for aid, a in self.agents.items()},
            'tasks': {tid: t.to_dict() for tid, t in self.tasks.items()},
            'stats': self.stats,
            'running': self.running
        }
    
    def visualize_network(self) -> str:
        """Visualizza network agenti"""
        lines = [f"\n{self.name} - Agent Network"]
        lines.append("=" * 60)
        
        # Group by role
        by_role: Dict[AgentRole, List[Agent]] = {}
        for agent in self.agents.values():
            if agent.role not in by_role:
                by_role[agent.role] = []
            by_role[agent.role].append(agent)
        
        for role, agents in by_role.items():
            lines.append(f"\n{role.value.upper()}: ({len(agents)} agents)")
            for agent in agents:
                status_icon = "●" if agent.state == AgentState.WORKING else "○"
                lines.append(f"  {status_icon} {agent.id} - {len(agent.current_tasks)} tasks")
        
        return "\n".join(lines)


class EcosystemTemplate:
    """Template per ecosistemi predefiniti"""
    
    @staticmethod
    def software_development_team(name: str = "DevTeam") -> MultiAgentEcosystem:
        """Team sviluppo software"""
        eco = MultiAgentEcosystem(name, "Software development ecosystem")
        
        # Create agents
        eco.create_agent("coordinator_1", AgentRole.COORDINATOR, 
                        ["planning", "coordination", "management"])
        eco.create_agent("researcher_1", AgentRole.RESEARCHER,
                        ["research", "analysis", "documentation"])
        eco.create_agent("developer_1", AgentRole.DEVELOPER,
                        ["code", "implementation", "refactoring"])
        eco.create_agent("developer_2", AgentRole.DEVELOPER,
                        ["code", "implementation", "debugging"])
        eco.create_agent("tester_1", AgentRole.TESTER,
                        ["test", "validation", "qa"])
        eco.create_agent("security_1", AgentRole.SECURITY,
                        ["security", "audit", "compliance"])
        
        return eco
    
    @staticmethod
    def research_lab(name: str = "ResearchLab") -> MultiAgentEcosystem:
        """Laboratorio ricerca"""
        eco = MultiAgentEcosystem(name, "Research laboratory ecosystem")
        
        eco.create_agent("lead_researcher", AgentRole.COORDINATOR,
                        ["research", "planning", "coordination"])
        eco.create_agent("researcher_1", AgentRole.RESEARCHER,
                        ["research", "experimentation", "analysis"])
        eco.create_agent("researcher_2", AgentRole.RESEARCHER,
                        ["research", "data_collection", "modeling"])
        eco.create_agent("analyst_1", AgentRole.ANALYST,
                        ["analysis", "statistics", "visualization"])
        eco.create_agent("designer_1", AgentRole.DESIGNER,
                        ["design", "visualization", "presentation"])
        
        return eco
    
    @staticmethod
    def data_processing_pipeline(name: str = "DataPipeline") -> MultiAgentEcosystem:
        """Pipeline elaborazione dati"""
        eco = MultiAgentEcosystem(name, "Data processing pipeline")
        
        eco.create_agent("collector_1", AgentRole.RESEARCHER,
                        ["collect", "extract", "crawl"])
        eco.create_agent("processor_1", AgentRole.DEVELOPER,
                        ["process", "transform", "clean"])
        eco.create_agent("analyzer_1", AgentRole.ANALYST,
                        ["analyze", "model", "predict"])
        eco.create_agent("validator_1", AgentRole.TESTER,
                        ["validate", "verify", "check"])
        eco.create_agent("optimizer_1", AgentRole.OPTIMIZER,
                        ["optimize", "tune", "improve"])
        
        return eco
    
    @staticmethod
    def autonomous_trading_system(name: str = "TradingSystem") -> MultiAgentEcosystem:
        """Sistema trading autonomo"""
        eco = MultiAgentEcosystem(name, "Autonomous trading system")
        
        eco.create_agent("market_monitor", AgentRole.MONITOR,
                        ["monitor", "track", "alert"])
        eco.create_agent("data_analyst", AgentRole.ANALYST,
                        ["analyze", "predict", "model"])
        eco.create_agent("strategy_dev", AgentRole.DEVELOPER,
                        ["strategy", "algorithm", "backtest"])
        eco.create_agent("risk_manager", AgentRole.SECURITY,
                        ["risk", "compliance", "audit"])
        eco.create_agent("executor", AgentRole.COORDINATOR,
                        ["execute", "coordinate", "manage"])
        
        return eco
    
    @staticmethod
    def content_creation_studio(name: str = "ContentStudio") -> MultiAgentEcosystem:
        """Studio creazione contenuti"""
        eco = MultiAgentEcosystem(name, "Content creation studio")
        
        eco.create_agent("creative_director", AgentRole.COORDINATOR,
                        ["planning", "coordination", "creative"])
        eco.create_agent("writer_1", AgentRole.DEVELOPER,
                        ["write", "edit", "content"])
        eco.create_agent("designer_1", AgentRole.DESIGNER,
                        ["design", "graphics", "layout"])
        eco.create_agent("researcher_1", AgentRole.RESEARCHER,
                        ["research", "fact-check", "sources"])
        eco.create_agent("optimizer_1", AgentRole.OPTIMIZER,
                        ["seo", "optimize", "analytics"])
        
        return eco


class EcosystemManager:
    """Manager per gestire multipli ecosistemi"""
    
    def __init__(self):
        self.ecosystems: Dict[str, MultiAgentEcosystem] = {}
        self.templates = EcosystemTemplate()
    
    def create_ecosystem(self, name: str, description: str = "") -> MultiAgentEcosystem:
        """Crea nuovo ecosistema"""
        eco = MultiAgentEcosystem(name, description)
        self.ecosystems[name] = eco
        return eco
    
    def create_from_template(self, template_name: str, 
                           custom_name: Optional[str] = None) -> MultiAgentEcosystem:
        """Crea ecosistema da template"""
        templates = {
            'software_dev': self.templates.software_development_team,
            'research_lab': self.templates.research_lab,
            'data_pipeline': self.templates.data_processing_pipeline,
            'trading_system': self.templates.autonomous_trading_system,
            'content_studio': self.templates.content_creation_studio
        }
        
        if template_name not in templates:
            raise ValueError(f"Template {template_name} not found")
        
        eco = templates[template_name](custom_name or template_name)
        self.ecosystems[eco.name] = eco
        return eco
    
    def get_ecosystem(self, name: str) -> Optional[MultiAgentEcosystem]:
        """Ottieni ecosistema"""
        return self.ecosystems.get(name)
    
    def list_ecosystems(self) -> List[str]:
        """Lista ecosistemi"""
        return list(self.ecosystems.keys())
    
    def run_ecosystem(self, name: str, max_steps: int = 100) -> Dict[str, Any]:
        """Esegui ecosistema"""
        eco = self.get_ecosystem(name)
        if not eco:
            raise ValueError(f"Ecosystem {name} not found")
        
        return eco.run(max_steps)
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Statistiche tutti gli ecosistemi"""
        return {
            'total_ecosystems': len(self.ecosystems),
            'ecosystems': {
                name: eco.stats
                for name, eco in self.ecosystems.items()
            }
        }


if __name__ == "__main__":
    print("Multi-Agent Ecosystem System")
    print("=" * 80)
    
    # Create manager
    manager = EcosystemManager()
    
    # Create software dev team
    print("\n[*] Creating Software Development Team...")
    dev_team = manager.create_from_template('software_dev', 'MyDevTeam')
    
    # Add tasks
    print("[*] Adding tasks...")
    dev_team.create_task("research_1", "research_requirements", "Research project requirements")
    dev_team.create_task("code_1", "code_implementation", "Implement features", 
                        dependencies=["research_1"])
    dev_team.create_task("test_1", "test_features", "Test implementation",
                        dependencies=["code_1"])
    
    # Visualize
    print(dev_team.visualize_network())
    
    # Run simulation
    print("\n[*] Running simulation...")
    result = dev_team.run(max_steps=50)
    
    print(f"\n[OK] Simulation completed in {result['steps']} steps")
    print(f"   Tasks completed: {result['tasks_completed']}/{result['total_tasks']}")
    print(f"   Messages exchanged: {result['messages_exchanged']}")
    
    print("\n[OK] Multi-Agent Ecosystem system initialized!")
