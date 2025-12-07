"""
Virtual Environment Simulator for Agent Design and Testing
Sistema completo di simulazione con fisica, rendering, sensori
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import json
from pathlib import Path
import time
from enum import Enum


class AgentType(Enum):
    """Tipi di agenti supportati"""
    GROUND_ROBOT = "ground_robot"
    DRONE = "drone"
    HUMANOID = "humanoid"
    VEHICLE = "vehicle"
    CUSTOM = "custom"


class SensorType(Enum):
    """Tipi di sensori disponibili"""
    CAMERA = "camera"
    LIDAR = "lidar"
    RADAR = "radar"
    GPS = "gps"
    IMU = "imu"
    SONAR = "sonar"
    PROXIMITY = "proximity"
    TACTILE = "tactile"


@dataclass
class Vector3D:
    """Vettore 3D per posizione/velocità/accelerazione"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def magnitude(self) -> float:
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector3D(self.x / mag, self.y / mag, self.z / mag)
        return Vector3D()
    
    def to_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])


@dataclass
class Quaternion:
    """Quaternione per rotazioni"""
    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def to_euler(self) -> Vector3D:
        """Convert to Euler angles (roll, pitch, yaw)"""
        # Roll (x-axis)
        sinr_cosp = 2 * (self.w * self.x + self.y * self.z)
        cosr_cosp = 1 - 2 * (self.x * self.x + self.y * self.y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)
        
        # Pitch (y-axis)
        sinp = 2 * (self.w * self.y - self.z * self.x)
        pitch = np.arcsin(np.clip(sinp, -1, 1))
        
        # Yaw (z-axis)
        siny_cosp = 2 * (self.w * self.z + self.x * self.y)
        cosy_cosp = 1 - 2 * (self.y * self.y + self.z * self.z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)
        
        return Vector3D(roll, pitch, yaw)


@dataclass
class PhysicsProperties:
    """Proprietà fisiche dell'agente"""
    mass: float = 1.0  # kg
    friction: float = 0.5
    restitution: float = 0.3  # bounce
    drag_coefficient: float = 0.1
    gravity_enabled: bool = True


@dataclass
class SensorData:
    """Dati da sensore"""
    sensor_type: SensorType
    timestamp: float
    data: Any
    position: Vector3D
    orientation: Quaternion


@dataclass
class AgentState:
    """Stato completo dell'agente"""
    position: Vector3D = field(default_factory=Vector3D)
    velocity: Vector3D = field(default_factory=Vector3D)
    acceleration: Vector3D = field(default_factory=Vector3D)
    orientation: Quaternion = field(default_factory=Quaternion)
    angular_velocity: Vector3D = field(default_factory=Vector3D)
    
    def copy(self):
        return AgentState(
            position=Vector3D(self.position.x, self.position.y, self.position.z),
            velocity=Vector3D(self.velocity.x, self.velocity.y, self.velocity.z),
            acceleration=Vector3D(self.acceleration.x, self.acceleration.y, self.acceleration.z),
            orientation=Quaternion(self.orientation.w, self.orientation.x, 
                                 self.orientation.y, self.orientation.z),
            angular_velocity=Vector3D(self.angular_velocity.x, 
                                     self.angular_velocity.y, self.angular_velocity.z)
        )


class Sensor:
    """Sensore generico"""
    
    def __init__(self, sensor_type: SensorType, position: Vector3D = None, 
                 config: Dict = None):
        self.sensor_type = sensor_type
        self.position = position or Vector3D()
        self.config = config or {}
        self.enabled = True
        
    def read(self, agent_state: AgentState, environment: 'VirtualEnvironment') -> SensorData:
        """Read sensor data - da implementare nelle sottoclassi"""
        return SensorData(
            sensor_type=self.sensor_type,
            timestamp=time.time(),
            data=None,
            position=self.position,
            orientation=Quaternion()
        )


class CameraSensor(Sensor):
    """Sensore camera RGB"""
    
    def __init__(self, position: Vector3D = None, resolution: Tuple[int, int] = (640, 480)):
        super().__init__(SensorType.CAMERA, position)
        self.resolution = resolution
        
    def read(self, agent_state: AgentState, environment: 'VirtualEnvironment') -> SensorData:
        # Simula acquisizione immagine
        image = np.random.randint(0, 256, (*self.resolution, 3), dtype=np.uint8)
        
        return SensorData(
            sensor_type=self.sensor_type,
            timestamp=time.time(),
            data={'image': image, 'resolution': self.resolution},
            position=agent_state.position + self.position,
            orientation=agent_state.orientation
        )


class LidarSensor(Sensor):
    """Sensore LIDAR"""
    
    def __init__(self, position: Vector3D = None, num_rays: int = 360, 
                 max_range: float = 10.0):
        super().__init__(SensorType.LIDAR, position)
        self.num_rays = num_rays
        self.max_range = max_range
        
    def read(self, agent_state: AgentState, environment: 'VirtualEnvironment') -> SensorData:
        # Simula scansione LIDAR
        angles = np.linspace(0, 2*np.pi, self.num_rays)
        distances = np.random.uniform(0.5, self.max_range, self.num_rays)
        
        # Point cloud
        points = []
        for angle, dist in zip(angles, distances):
            x = dist * np.cos(angle) + agent_state.position.x
            y = dist * np.sin(angle) + agent_state.position.y
            points.append([x, y, agent_state.position.z])
        
        return SensorData(
            sensor_type=self.sensor_type,
            timestamp=time.time(),
            data={'distances': distances, 'angles': angles, 'points': np.array(points)},
            position=agent_state.position + self.position,
            orientation=agent_state.orientation
        )


class IMUSensor(Sensor):
    """Inertial Measurement Unit"""
    
    def __init__(self, position: Vector3D = None):
        super().__init__(SensorType.IMU, position)
        
    def read(self, agent_state: AgentState, environment: 'VirtualEnvironment') -> SensorData:
        # Accelerometer, Gyroscope, Magnetometer
        return SensorData(
            sensor_type=self.sensor_type,
            timestamp=time.time(),
            data={
                'acceleration': agent_state.acceleration.to_array(),
                'angular_velocity': agent_state.angular_velocity.to_array(),
                'orientation': agent_state.orientation.to_euler().to_array()
            },
            position=agent_state.position,
            orientation=agent_state.orientation
        )


class VirtualAgent:
    """Agente virtuale con fisica e sensori"""
    
    def __init__(self, agent_id: str, agent_type: AgentType, 
                 initial_state: AgentState = None,
                 physics: PhysicsProperties = None):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.state = initial_state or AgentState()
        self.physics = physics or PhysicsProperties()
        
        self.sensors: Dict[str, Sensor] = {}
        self.actuators: Dict[str, Any] = {}
        
        self.state_history: List[AgentState] = []
        self.max_history = 1000
        
        self.color = np.random.rand(3)  # RGB color for rendering
        
    def add_sensor(self, name: str, sensor: Sensor):
        """Aggiungi sensore all'agente"""
        self.sensors[name] = sensor
        
    def remove_sensor(self, name: str):
        """Rimuovi sensore"""
        if name in self.sensors:
            del self.sensors[name]
            
    def read_sensors(self, environment: 'VirtualEnvironment') -> Dict[str, SensorData]:
        """Leggi tutti i sensori"""
        sensor_readings = {}
        for name, sensor in self.sensors.items():
            if sensor.enabled:
                sensor_readings[name] = sensor.read(self.state, environment)
        return sensor_readings
    
    def apply_force(self, force: Vector3D):
        """Applica forza all'agente"""
        # F = ma -> a = F/m
        self.state.acceleration = self.state.acceleration + (force * (1.0 / self.physics.mass))
        
    def apply_torque(self, torque: Vector3D):
        """Applica coppia (rotazione)"""
        self.state.angular_velocity = self.state.angular_velocity + torque
        
    def update(self, dt: float, environment: 'VirtualEnvironment'):
        """Update fisica agente"""
        # Gravity
        if self.physics.gravity_enabled and self.state.position.z > 0:
            gravity = Vector3D(0, 0, -9.81 * self.physics.mass)
            self.apply_force(gravity)
        
        # Drag force
        drag = self.state.velocity * (-self.physics.drag_coefficient)
        self.apply_force(drag)
        
        # Update velocity: v = v0 + a*dt
        self.state.velocity = self.state.velocity + (self.state.acceleration * dt)
        
        # Update position: p = p0 + v*dt
        self.state.position = self.state.position + (self.state.velocity * dt)
        
        # Ground collision
        if self.state.position.z < 0:
            self.state.position.z = 0
            self.state.velocity.z = -self.state.velocity.z * self.physics.restitution
            
            # Friction on ground
            friction_force = self.state.velocity * (-self.physics.friction)
            friction_force.z = 0
            self.apply_force(friction_force)
        
        # Reset acceleration
        self.state.acceleration = Vector3D()
        
        # Save history
        self.state_history.append(self.state.copy())
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
    
    def get_bounding_box(self) -> Tuple[Vector3D, Vector3D]:
        """Get bounding box (min, max)"""
        size = 1.0  # Default size
        half = size / 2
        return (
            Vector3D(self.state.position.x - half, 
                    self.state.position.y - half,
                    self.state.position.z),
            Vector3D(self.state.position.x + half,
                    self.state.position.y + half,
                    self.state.position.z + size)
        )


class Obstacle:
    """Ostacolo nell'ambiente"""
    
    def __init__(self, position: Vector3D, size: Vector3D, obstacle_type: str = "box"):
        self.position = position
        self.size = size
        self.obstacle_type = obstacle_type
        
    def check_collision(self, point: Vector3D) -> bool:
        """Check if point collides with obstacle"""
        return (abs(point.x - self.position.x) < self.size.x / 2 and
                abs(point.y - self.position.y) < self.size.y / 2 and
                abs(point.z - self.position.z) < self.size.z / 2)


class VirtualEnvironment:
    """Ambiente virtuale di simulazione"""
    
    def __init__(self, name: str = "Default Environment", 
                 size: Vector3D = None,
                 gravity: float = 9.81):
        self.name = name
        self.size = size or Vector3D(100, 100, 50)
        self.gravity = gravity
        
        self.agents: Dict[str, VirtualAgent] = {}
        self.obstacles: List[Obstacle] = []
        
        self.time = 0.0
        self.dt = 0.01  # 100 Hz simulation
        
        self.running = False
        
    def add_agent(self, agent: VirtualAgent):
        """Aggiungi agente all'ambiente"""
        self.agents[agent.agent_id] = agent
        
    def remove_agent(self, agent_id: str):
        """Rimuovi agente"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            
    def add_obstacle(self, obstacle: Obstacle):
        """Aggiungi ostacolo"""
        self.obstacles.append(obstacle)
        
    def step(self):
        """Single simulation step"""
        # Update all agents
        for agent in self.agents.values():
            agent.update(self.dt, self)
        
        # Check collisions between agents
        agent_list = list(self.agents.values())
        for i, agent1 in enumerate(agent_list):
            for agent2 in agent_list[i+1:]:
                self._check_agent_collision(agent1, agent2)
        
        # Check collisions with obstacles
        for agent in self.agents.values():
            for obstacle in self.obstacles:
                if obstacle.check_collision(agent.state.position):
                    self._handle_obstacle_collision(agent, obstacle)
        
        self.time += self.dt
        
    def run(self, duration: float):
        """Run simulation for specified duration"""
        self.running = True
        start_time = self.time
        
        while self.running and (self.time - start_time) < duration:
            self.step()
            
    def _check_agent_collision(self, agent1: VirtualAgent, agent2: VirtualAgent):
        """Check collision between two agents"""
        distance = (agent1.state.position - agent2.state.position).magnitude()
        min_distance = 1.0  # Minimum safe distance
        
        if distance < min_distance:
            # Simple elastic collision
            direction = (agent2.state.position - agent1.state.position).normalize()
            
            # Separate agents
            overlap = min_distance - distance
            agent1.state.position = agent1.state.position + (direction * (-overlap / 2))
            agent2.state.position = agent2.state.position + (direction * (overlap / 2))
            
    def _handle_obstacle_collision(self, agent: VirtualAgent, obstacle: Obstacle):
        """Handle collision with obstacle"""
        # Simple bounce back
        direction = (agent.state.position - obstacle.position).normalize()
        agent.state.velocity = direction * agent.state.velocity.magnitude() * 0.5
        
    def get_environment_state(self) -> Dict[str, Any]:
        """Get complete environment state"""
        return {
            'time': self.time,
            'agents': {
                agent_id: {
                    'position': [agent.state.position.x, agent.state.position.y, agent.state.position.z],
                    'velocity': [agent.state.velocity.x, agent.state.velocity.y, agent.state.velocity.z],
                    'type': agent.agent_type.value
                }
                for agent_id, agent in self.agents.items()
            },
            'obstacles': [
                {
                    'position': [obs.position.x, obs.position.y, obs.position.z],
                    'size': [obs.size.x, obs.size.y, obs.size.z],
                    'type': obs.obstacle_type
                }
                for obs in self.obstacles
            ]
        }


class AgentDesigner:
    """Designer per costruire agenti custom"""
    
    def __init__(self):
        self.templates = {
            AgentType.GROUND_ROBOT: self._create_ground_robot_template,
            AgentType.DRONE: self._create_drone_template,
            AgentType.HUMANOID: self._create_humanoid_template,
            AgentType.VEHICLE: self._create_vehicle_template,
        }
        
    def create_agent(self, agent_id: str, agent_type: AgentType,
                    position: Vector3D = None,
                    custom_sensors: List[Tuple[str, Sensor]] = None) -> VirtualAgent:
        """Create agent from template"""
        
        initial_state = AgentState(position=position or Vector3D())
        
        if agent_type in self.templates:
            agent = self.templates[agent_type](agent_id, initial_state)
        else:
            agent = VirtualAgent(agent_id, AgentType.CUSTOM, initial_state)
        
        # Add custom sensors
        if custom_sensors:
            for name, sensor in custom_sensors:
                agent.add_sensor(name, sensor)
        
        return agent
    
    def _create_ground_robot_template(self, agent_id: str, 
                                     initial_state: AgentState) -> VirtualAgent:
        """Ground robot with wheels"""
        physics = PhysicsProperties(
            mass=5.0,
            friction=0.7,
            restitution=0.1,
            drag_coefficient=0.2
        )
        
        agent = VirtualAgent(agent_id, AgentType.GROUND_ROBOT, initial_state, physics)
        
        # Default sensors
        agent.add_sensor("front_camera", CameraSensor(Vector3D(0.5, 0, 0.3)))
        agent.add_sensor("lidar", LidarSensor(Vector3D(0, 0, 0.5), num_rays=360))
        agent.add_sensor("imu", IMUSensor())
        
        return agent
    
    def _create_drone_template(self, agent_id: str, 
                              initial_state: AgentState) -> VirtualAgent:
        """Flying drone"""
        physics = PhysicsProperties(
            mass=1.5,
            friction=0.1,
            restitution=0.2,
            drag_coefficient=0.3,
            gravity_enabled=True
        )
        
        agent = VirtualAgent(agent_id, AgentType.DRONE, initial_state, physics)
        
        # Drone sensors
        agent.add_sensor("down_camera", CameraSensor(Vector3D(0, 0, -0.2)))
        agent.add_sensor("lidar", LidarSensor(Vector3D(0, 0, 0), num_rays=180))
        agent.add_sensor("imu", IMUSensor())
        
        return agent
    
    def _create_humanoid_template(self, agent_id: str,
                                  initial_state: AgentState) -> VirtualAgent:
        """Humanoid robot"""
        physics = PhysicsProperties(
            mass=75.0,
            friction=0.8,
            restitution=0.05,
            drag_coefficient=0.1
        )
        
        agent = VirtualAgent(agent_id, AgentType.HUMANOID, initial_state, physics)
        
        # Humanoid sensors
        agent.add_sensor("head_camera", CameraSensor(Vector3D(0, 0, 1.7)))
        agent.add_sensor("imu", IMUSensor(Vector3D(0, 0, 0.8)))
        
        return agent
    
    def _create_vehicle_template(self, agent_id: str,
                                initial_state: AgentState) -> VirtualAgent:
        """Wheeled vehicle"""
        physics = PhysicsProperties(
            mass=1500.0,
            friction=0.6,
            restitution=0.2,
            drag_coefficient=0.4
        )
        
        agent = VirtualAgent(agent_id, AgentType.VEHICLE, initial_state, physics)
        
        # Vehicle sensors
        agent.add_sensor("front_camera", CameraSensor(Vector3D(2.0, 0, 1.5)))
        agent.add_sensor("lidar", LidarSensor(Vector3D(0, 0, 2.0), num_rays=360))
        agent.add_sensor("imu", IMUSensor())
        
        return agent


class SimulationAnalyzer:
    """Analizzatore per simulazioni"""
    
    def __init__(self):
        self.metrics = {}
        
    def analyze_agent_performance(self, agent: VirtualAgent) -> Dict[str, Any]:
        """Analyze agent performance from history"""
        if len(agent.state_history) < 2:
            return {}
        
        # Extract trajectories
        positions = [state.position for state in agent.state_history]
        velocities = [state.velocity for state in agent.state_history]
        
        # Calculate metrics
        total_distance = sum(
            (positions[i+1] - positions[i]).magnitude()
            for i in range(len(positions)-1)
        )
        
        avg_velocity = np.mean([v.magnitude() for v in velocities])
        max_velocity = max([v.magnitude() for v in velocities])
        
        # Height statistics
        heights = [p.z for p in positions]
        avg_height = np.mean(heights)
        max_height = max(heights)
        
        return {
            'total_distance': total_distance,
            'average_velocity': avg_velocity,
            'max_velocity': max_velocity,
            'average_height': avg_height,
            'max_height': max_height,
            'trajectory_length': len(positions)
        }
    
    def analyze_environment(self, environment: VirtualEnvironment) -> Dict[str, Any]:
        """Analyze complete environment"""
        return {
            'simulation_time': environment.time,
            'num_agents': len(environment.agents),
            'num_obstacles': len(environment.obstacles),
            'timestep': environment.dt,
            'agents': {
                agent_id: self.analyze_agent_performance(agent)
                for agent_id, agent in environment.agents.items()
            }
        }


def create_test_environment() -> VirtualEnvironment:
    """Create test environment with agents and obstacles"""
    env = VirtualEnvironment("Test Environment", Vector3D(50, 50, 20))
    
    # Add obstacles
    env.add_obstacle(Obstacle(Vector3D(10, 10, 0), Vector3D(2, 2, 2)))
    env.add_obstacle(Obstacle(Vector3D(-10, -10, 0), Vector3D(3, 3, 1)))
    env.add_obstacle(Obstacle(Vector3D(15, -15, 0), Vector3D(1, 1, 3)))
    
    # Create designer
    designer = AgentDesigner()
    
    # Add ground robot
    robot = designer.create_agent(
        "robot_1",
        AgentType.GROUND_ROBOT,
        position=Vector3D(0, 0, 0.5)
    )
    env.add_agent(robot)
    
    # Add drone
    drone = designer.create_agent(
        "drone_1",
        AgentType.DRONE,
        position=Vector3D(5, 5, 5)
    )
    env.add_agent(drone)
    
    return env


if __name__ == "__main__":
    print("Virtual Environment Simulator for Agent Design")
    print("=" * 80)
    
    # Create environment
    env = create_test_environment()
    
    print(f"\n[*] Environment: {env.name}")
    print(f"   Size: {env.size.x} x {env.size.y} x {env.size.z}")
    print(f"   Agents: {len(env.agents)}")
    print(f"   Obstacles: {len(env.obstacles)}")
    
    # Run simulation
    print(f"\n[*] Running simulation for 5 seconds...")
    env.run(duration=5.0)
    
    # Analyze
    analyzer = SimulationAnalyzer()
    results = analyzer.analyze_environment(env)
    
    print(f"\n[*] Simulation Results:")
    print(f"   Total time: {results['simulation_time']:.2f}s")
    print(f"   Timesteps: {int(results['simulation_time'] / env.dt)}")
    
    for agent_id, metrics in results['agents'].items():
        print(f"\n   Agent: {agent_id}")
        print(f"      Distance: {metrics['total_distance']:.2f}m")
        print(f"      Avg velocity: {metrics['average_velocity']:.2f}m/s")
        print(f"      Max velocity: {metrics['max_velocity']:.2f}m/s")
    
    print("\n[OK] Virtual Environment ready!")
