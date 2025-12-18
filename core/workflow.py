"""Workflow primitives shared across uno orchestrations.

This module defines a few lightweight data structures that allow us to
describe complex, multi-step procedures (like the vit-controlled meta
engineer flow) while keeping compatibility with the previous extremely
simple Workflow helper that existed in the project.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


@dataclass
class WorkflowContext:
    """Mutable context shared across workflow steps."""

    directive: str
    goal: str
    priority: str = "standard"
    vit_context: Optional[Dict[str, Any]] = None
    shared_memory: List[Dict[str, Any]] = field(default_factory=list)
    artifacts: Dict[str, Any] = field(default_factory=dict)
    breadcrumbs: List[str] = field(default_factory=list)


@dataclass
class WorkflowStep:
    """Single executable step within a workflow."""

    name: str
    description: str
    owner: str
    executor: Callable[["WorkflowStep", WorkflowContext], Dict[str, Any]]
    status: str = "pending"
    output: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


@dataclass
class WorkflowArtifact:
    """Structured summary produced by a workflow step."""

    step_name: str
    owner: str
    summary: str
    details: Dict[str, Any]
    tags: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class WorkflowRun:
    """High-level record describing an entire workflow execution."""

    run_id: str
    directive: str
    goal: str
    status: str
    artifacts: List[WorkflowArtifact]
    shared_memory: List[Dict[str, Any]]
    started_at: str
    finished_at: Optional[str] = None
    priority: str = "standard"


class Workflow:
    """Backward-compatible minimal workflow helper used by legacy code."""

    def __init__(self, steps: Optional[List[Callable[[], Any]]] = None):
        self.steps = steps or []

    def add_step(self, step: Callable[[], Any]):
        self.steps.append(step)

    def run(self):
        for step in self.steps:
            step()
