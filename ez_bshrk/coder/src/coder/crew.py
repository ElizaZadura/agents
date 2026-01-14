from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Coder():
    """Coder crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config['coder'], 
            verbose=True, 
            allow_code_execution=True, 
            code_execution_mode="safe", 
            max_execution_time=240,  # Increased from 30 to 240 seconds (4 minutes) to allow time for code writing, execution, and verification
            max_retry_limit=5
        )

    @task
    def coding_task(self) -> Task:
        return Task(config=self.tasks_config['coding_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)