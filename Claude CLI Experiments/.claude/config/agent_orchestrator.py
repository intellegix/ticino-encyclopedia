#!/usr/bin/env python3
"""
Multiagent Orchestrator with Perplexity Research Integration
Coordinates specialized agents with research capabilities
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class AgentType(Enum):
    """Available specialized agent types"""
    ORCHESTRATOR = "orchestrator"
    ARCHITECT = "architect"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    DEVOPS = "devops"
    TESTING = "testing"
    RESEARCH = "research"


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class AgentTask:
    """Represents a task for an agent"""
    task_id: str
    agent_type: AgentType
    description: str
    priority: TaskPriority
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    requires_research: bool = False
    research_query: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None


@dataclass
class WorkflowPhase:
    """Represents a development phase"""
    phase_name: str
    description: str
    tasks: List[AgentTask]
    parallel_execution: bool = True
    required_for_next: bool = True


class AgentOrchestrator:
    """
    Orchestrates multiple specialized agents with research integration
    """

    def __init__(self):
        self.tasks: Dict[str, AgentTask] = {}
        self.phases: List[WorkflowPhase] = []
        self.current_phase: Optional[WorkflowPhase] = None

    def create_standard_workflow(
        self,
        project_description: str,
        architecture_type: str = "layered"
    ) -> List[WorkflowPhase]:
        """
        Create standard 5-phase development workflow

        Args:
            project_description: High-level project requirements
            architecture_type: Architecture pattern (layered, microservices, etc.)

        Returns:
            List of workflow phases
        """
        phases = []

        # Phase 1: Requirements and Architecture
        phase1 = WorkflowPhase(
            phase_name="Requirements & Architecture",
            description="Analyze requirements and design system architecture",
            tasks=[
                AgentTask(
                    task_id="research_requirements",
                    agent_type=AgentType.RESEARCH,
                    description=f"Research best practices for: {project_description}",
                    priority=TaskPriority.CRITICAL,
                    requires_research=True,
                    research_query=f"Latest best practices and architectural patterns for {project_description}"
                ),
                AgentTask(
                    task_id="arch_design",
                    agent_type=AgentType.ARCHITECT,
                    description=f"Design {architecture_type} architecture with ADRs",
                    priority=TaskPriority.CRITICAL,
                    dependencies=["research_requirements"]
                ),
                AgentTask(
                    task_id="research_tech_stack",
                    agent_type=AgentType.RESEARCH,
                    description="Research optimal technology stack",
                    priority=TaskPriority.HIGH,
                    requires_research=True,
                    research_query=f"Best technology stack for {project_description} using {architecture_type} architecture 2024"
                ),
                AgentTask(
                    task_id="db_schema_design",
                    agent_type=AgentType.DATABASE,
                    description="Design database schema and ERD",
                    priority=TaskPriority.HIGH,
                    dependencies=["arch_design"]
                ),
                AgentTask(
                    task_id="api_contract_design",
                    agent_type=AgentType.ARCHITECT,
                    description="Define API contracts (OpenAPI/Swagger)",
                    priority=TaskPriority.HIGH,
                    dependencies=["arch_design", "db_schema_design"]
                )
            ],
            parallel_execution=False,
            required_for_next=True
        )
        phases.append(phase1)

        # Phase 2: Parallel Development
        phase2 = WorkflowPhase(
            phase_name="Parallel Development",
            description="Frontend, Backend, and Database implementation",
            tasks=[
                AgentTask(
                    task_id="research_frontend_patterns",
                    agent_type=AgentType.RESEARCH,
                    description="Research modern frontend patterns and libraries",
                    priority=TaskPriority.MEDIUM,
                    requires_research=True,
                    research_query="Latest frontend development patterns, state management, and UI libraries 2024"
                ),
                AgentTask(
                    task_id="frontend_implementation",
                    agent_type=AgentType.FRONTEND,
                    description="Implement frontend components and state management",
                    priority=TaskPriority.HIGH,
                    dependencies=["api_contract_design", "research_frontend_patterns"]
                ),
                AgentTask(
                    task_id="research_backend_patterns",
                    agent_type=AgentType.RESEARCH,
                    description="Research backend security and optimization patterns",
                    priority=TaskPriority.MEDIUM,
                    requires_research=True,
                    research_query="Backend API security best practices, authentication, and performance optimization 2024"
                ),
                AgentTask(
                    task_id="backend_implementation",
                    agent_type=AgentType.BACKEND,
                    description="Implement API endpoints and business logic",
                    priority=TaskPriority.HIGH,
                    dependencies=["api_contract_design", "research_backend_patterns"]
                ),
                AgentTask(
                    task_id="research_db_optimization",
                    agent_type=AgentType.RESEARCH,
                    description="Research database optimization techniques",
                    priority=TaskPriority.MEDIUM,
                    requires_research=True,
                    research_query="Database indexing, query optimization, and scaling strategies 2024"
                ),
                AgentTask(
                    task_id="database_implementation",
                    agent_type=AgentType.DATABASE,
                    description="Create migrations, indexes, and seed data",
                    priority=TaskPriority.HIGH,
                    dependencies=["db_schema_design", "research_db_optimization"]
                )
            ],
            parallel_execution=True,
            required_for_next=True
        )
        phases.append(phase2)

        # Phase 3: Testing & Quality Assurance
        phase3 = WorkflowPhase(
            phase_name="Testing & QA",
            description="Comprehensive testing and quality validation",
            tasks=[
                AgentTask(
                    task_id="research_testing_strategies",
                    agent_type=AgentType.RESEARCH,
                    description="Research modern testing frameworks and strategies",
                    priority=TaskPriority.MEDIUM,
                    requires_research=True,
                    research_query="Comprehensive testing strategies: unit, integration, e2e testing frameworks 2024"
                ),
                AgentTask(
                    task_id="unit_testing",
                    agent_type=AgentType.TESTING,
                    description="Create unit tests (>80% coverage)",
                    priority=TaskPriority.CRITICAL,
                    dependencies=["frontend_implementation", "backend_implementation", "research_testing_strategies"]
                ),
                AgentTask(
                    task_id="integration_testing",
                    agent_type=AgentType.TESTING,
                    description="Create integration tests for APIs and database",
                    priority=TaskPriority.HIGH,
                    dependencies=["unit_testing"]
                ),
                AgentTask(
                    task_id="e2e_testing",
                    agent_type=AgentType.TESTING,
                    description="Create end-to-end tests for critical flows",
                    priority=TaskPriority.HIGH,
                    dependencies=["integration_testing"]
                ),
                AgentTask(
                    task_id="security_testing",
                    agent_type=AgentType.TESTING,
                    description="Security testing (OWASP Top 10)",
                    priority=TaskPriority.CRITICAL,
                    dependencies=["e2e_testing"]
                )
            ],
            parallel_execution=False,
            required_for_next=True
        )
        phases.append(phase3)

        # Phase 4: DevOps & Deployment
        phase4 = WorkflowPhase(
            phase_name="DevOps & Deployment",
            description="CI/CD, infrastructure, and deployment",
            tasks=[
                AgentTask(
                    task_id="research_devops_practices",
                    agent_type=AgentType.RESEARCH,
                    description="Research modern DevOps and deployment strategies",
                    priority=TaskPriority.MEDIUM,
                    requires_research=True,
                    research_query="Modern CI/CD pipelines, container orchestration, and infrastructure as code best practices 2024"
                ),
                AgentTask(
                    task_id="cicd_pipeline",
                    agent_type=AgentType.DEVOPS,
                    description="Configure CI/CD pipeline",
                    priority=TaskPriority.CRITICAL,
                    dependencies=["security_testing", "research_devops_practices"]
                ),
                AgentTask(
                    task_id="containerization",
                    agent_type=AgentType.DEVOPS,
                    description="Create Docker and Kubernetes configurations",
                    priority=TaskPriority.HIGH,
                    dependencies=["cicd_pipeline"]
                ),
                AgentTask(
                    task_id="infrastructure",
                    agent_type=AgentType.DEVOPS,
                    description="Setup IaC (Terraform/Pulumi)",
                    priority=TaskPriority.HIGH,
                    dependencies=["containerization"]
                ),
                AgentTask(
                    task_id="monitoring",
                    agent_type=AgentType.DEVOPS,
                    description="Setup monitoring and logging",
                    priority=TaskPriority.MEDIUM,
                    dependencies=["infrastructure"]
                )
            ],
            parallel_execution=False,
            required_for_next=False
        )
        phases.append(phase4)

        # Phase 5: Monitoring & Optimization
        phase5 = WorkflowPhase(
            phase_name="Monitoring & Optimization",
            description="Production monitoring and continuous optimization",
            tasks=[
                AgentTask(
                    task_id="research_monitoring",
                    agent_type=AgentType.RESEARCH,
                    description="Research application monitoring and observability",
                    priority=TaskPriority.LOW,
                    requires_research=True,
                    research_query="Application performance monitoring, observability, and alerting best practices 2024"
                ),
                AgentTask(
                    task_id="performance_monitoring",
                    agent_type=AgentType.DEVOPS,
                    description="Configure APM and alerting",
                    priority=TaskPriority.MEDIUM,
                    dependencies=["monitoring", "research_monitoring"]
                ),
                AgentTask(
                    task_id="optimization_review",
                    agent_type=AgentType.ARCHITECT,
                    description="Performance optimization review",
                    priority=TaskPriority.LOW,
                    dependencies=["performance_monitoring"]
                )
            ],
            parallel_execution=True,
            required_for_next=False
        )
        phases.append(phase5)

        self.phases = phases
        return phases

    def generate_execution_plan(self) -> Dict[str, Any]:
        """
        Generate detailed execution plan for all phases

        Returns:
            Structured execution plan with task ordering
        """
        plan = {
            "total_phases": len(self.phases),
            "total_tasks": sum(len(p.tasks) for p in self.phases),
            "estimated_parallel_gains": self._calculate_parallel_efficiency(),
            "phases": []
        }

        for phase_idx, phase in enumerate(self.phases, 1):
            phase_plan = {
                "phase_number": phase_idx,
                "phase_name": phase.phase_name,
                "description": phase.description,
                "parallel_execution": phase.parallel_execution,
                "required_for_next": phase.required_for_next,
                "tasks": []
            }

            # Group tasks by dependencies for parallel execution
            if phase.parallel_execution:
                task_groups = self._group_tasks_by_dependencies(phase.tasks)
                for group_idx, task_group in enumerate(task_groups, 1):
                    phase_plan["tasks"].append({
                        "execution_group": group_idx,
                        "parallel": True,
                        "tasks": [self._task_to_dict(t) for t in task_group]
                    })
            else:
                phase_plan["tasks"] = [
                    {
                        "execution_group": idx,
                        "parallel": False,
                        "tasks": [self._task_to_dict(task)]
                    }
                    for idx, task in enumerate(phase.tasks, 1)
                ]

            plan["phases"].append(phase_plan)

        return plan

    def _group_tasks_by_dependencies(
        self,
        tasks: List[AgentTask]
    ) -> List[List[AgentTask]]:
        """Group tasks into parallel execution groups based on dependencies"""
        groups = []
        remaining_tasks = tasks.copy()
        completed_task_ids = set()

        while remaining_tasks:
            # Find tasks with no unfulfilled dependencies
            current_group = []
            for task in remaining_tasks:
                if all(dep in completed_task_ids for dep in task.dependencies):
                    current_group.append(task)

            if not current_group:
                # Circular dependency or error - add remaining tasks
                current_group = remaining_tasks.copy()

            groups.append(current_group)

            # Update completed and remaining
            for task in current_group:
                completed_task_ids.add(task.task_id)
                remaining_tasks.remove(task)

        return groups

    def _calculate_parallel_efficiency(self) -> str:
        """Calculate estimated efficiency gains from parallel execution"""
        total_tasks = sum(len(p.tasks) for p in self.phases)
        parallel_phases = sum(1 for p in self.phases if p.parallel_execution)

        if parallel_phases > 0:
            efficiency = min(400, (parallel_phases / len(self.phases)) * 400)
            return f"{efficiency:.0f}% faster through parallel execution"

        return "Sequential execution (no parallelization)"

    def _task_to_dict(self, task: AgentTask) -> Dict[str, Any]:
        """Convert AgentTask to dictionary"""
        return {
            "task_id": task.task_id,
            "agent_type": task.agent_type.value,
            "description": task.description,
            "priority": task.priority.value,
            "status": task.status.value,
            "dependencies": task.dependencies,
            "requires_research": task.requires_research,
            "research_query": task.research_query
        }

    def get_next_tasks(self) -> List[AgentTask]:
        """
        Get next tasks ready for execution

        Returns:
            List of tasks ready to execute (dependencies met)
        """
        if not self.current_phase:
            self.current_phase = self.phases[0] if self.phases else None

        if not self.current_phase:
            return []

        completed_ids = {
            tid for tid, task in self.tasks.items()
            if task.status == TaskStatus.COMPLETED
        }

        ready_tasks = [
            task for task in self.current_phase.tasks
            if task.status == TaskStatus.PENDING
            and all(dep in completed_ids for dep in task.dependencies)
        ]

        return ready_tasks

    def mark_task_complete(
        self,
        task_id: str,
        result: Optional[Dict[str, Any]] = None
    ) -> None:
        """Mark a task as completed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.COMPLETED
            self.tasks[task_id].result = result
            self.tasks[task_id].completed_at = datetime.now().isoformat()

    def mark_task_failed(self, task_id: str, error: str) -> None:
        """Mark a task as failed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.FAILED
            self.tasks[task_id].error = error

    async def execute_research_task(
        self,
        task: AgentTask,
        wait_time: int = 150
    ) -> Dict[str, Any]:
        """
        Execute a Perplexity research task

        Args:
            task: AgentTask with research_query specified
            wait_time: Seconds to wait for research (default: 150)

        Returns:
            Research results dictionary
        """
        import subprocess
        from pathlib import Path

        if not task.research_query:
            return {"success": False, "error": "No research query specified"}

        # Run the simple_research.py script
        script_path = Path(__file__).parent.parent / "simple_research.py"
        result_path = Path(__file__).parent.parent / "sessions" / "screenshots" / "research_result.txt"

        try:
            # Execute research script
            process = subprocess.run(
                [
                    "../../.venv/Scripts/python.exe",
                    str(script_path),
                    task.research_query,
                    str(wait_time)
                ],
                capture_output=True,
                text=True,
                timeout=wait_time + 60
            )

            # Read the results
            if result_path.exists():
                with open(result_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                return {
                    "success": True,
                    "query": task.research_query,
                    "content": content,
                    "content_length": len(content),
                    "result_file": str(result_path)
                }
            else:
                return {
                    "success": False,
                    "error": "Research completed but no results file found"
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Research timed out after {wait_time + 60} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Research execution failed: {str(e)}"
            }

    def export_plan(self, output_file: str) -> None:
        """Export execution plan to JSON file"""
        plan = self.generate_execution_plan()
        with open(output_file, 'w') as f:
            json.dump(plan, f, indent=2)


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Multiagent Orchestrator with Research Integration"
    )
    parser.add_argument(
        "--project",
        type=str,
        required=True,
        help="Project description"
    )
    parser.add_argument(
        "--architecture",
        type=str,
        default="layered",
        choices=["layered", "microservices", "monolithic", "hexagonal", "event-driven"],
        help="Architecture pattern"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".claude/execution_plan.json",
        help="Output file for execution plan"
    )

    args = parser.parse_args()

    orchestrator = AgentOrchestrator()
    orchestrator.create_standard_workflow(
        project_description=args.project,
        architecture_type=args.architecture
    )

    plan = orchestrator.generate_execution_plan()
    print(json.dumps(plan, indent=2))

    if args.output:
        orchestrator.export_plan(args.output)
        print(f"\nExecution plan saved to: {args.output}")


if __name__ == "__main__":
    main()
