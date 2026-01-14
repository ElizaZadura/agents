from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from models.spec_pack import SpecPack


@CrewBase
class MultiAgentEngineering():
    """MultiAgentEngineering crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'], # type: ignore[index]
            verbose=True
        )
    @agent
    def core_domain_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['core_domain_engineer'], # type: ignore[index]
            verbose=True
        )
    @agent
    def ui_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_engineer'], # type: ignore[index]
            verbose=True
        )

    @task
    def spec_intake_task(self) -> Task:
        return Task(
            config=self.tasks_config['spec_intake'], # type: ignore[index]
            output_pydantic=SpecPack
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MultiAgentEngineering crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical,
            verbose=True,
        )
