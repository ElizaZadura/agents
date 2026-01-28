from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
import messages
from autogen_core import TRACE_LOGGER_NAME
import importlib
import logging
from autogen_core import AgentId
from dotenv import load_dotenv

load_dotenv(override=True)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(TRACE_LOGGER_NAME)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Creator(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
You are an Agent that creates new AI Agents.

You will be given a Python template. You must output a complete Python module that defines exactly one class named Agent.
Requirements:
- The file must be valid Python (must parse).
- The first line of your output MUST start at column 1 (no leading spaces).
- Do NOT output any prose or commentary.
- Do NOT output Markdown or code fences (no ```).
- The first non-empty line MUST begin with either: from, import, or class.

Agent requirements:
- class name: Agent
- inherits: RoutedAgent
- __init__(self, name: str) present and calls super().__init__(name)
- includes a system_message string for the delegate AssistantAgent
- decision bias: choose exactly ONE from:
  contrarian | risk-averse | numbers-first | narrative-first | adversarial | minimalist
  The bias MUST be stated explicitly in the system message and MUST affect how the agent evaluates ideas.
- System message must be operational rules (constraints/heuristics), not a persona biography.
- Avoid environmental topics. Mix business verticals across agents.

If you cannot comply with the formatting rules, output exactly:
raise SystemExit("FORMAT_ERROR")
"""



    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = AnthropicChatCompletionClient(model="claude-sonnet-4-5-20250929", temperature=1.0)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    def get_user_prompt(self):
        prompt = "Please generate a new Agent based strictly on this template. Stick to the class structure. \
            Respond only with the python code, no other text, and no markdown code blocks.\n\n\
            Be creative about taking the agent in a new direction, but don't change method signatures.\n\n\
            Here is the template:\n\n"
        with open("agent.py", "r", encoding="utf-8") as f:
            template = f.read()
        return prompt + template   
        

    @message_handler
    async def handle_my_message_type(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        filename = message.content
        agent_name = filename.split(".")[0]
        text_message = TextMessage(content=self.get_user_prompt(), source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.chat_message.content)
        print(f"** Creator has created python code for agent {agent_name} - about to register with Runtime")
        module = importlib.import_module(agent_name)
        await module.Agent.register(self.runtime, agent_name, lambda: module.Agent(agent_name))
        logger.info(f"** Agent {agent_name} is live")
        result = await self.send_message(messages.Message(content="Give me an idea"), AgentId(agent_name, "default"))
        return messages.Message(content=result.content)