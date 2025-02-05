from app.interview.model import InterviewContext

from .client import AIClient, MockAIDriver, OpenAIDriver
from .constants import prompts
from app.dependencies import ConfigDep


class BasicAgent:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    async def handle(self, context: InterviewContext, ai_client: AIClient) -> InterviewContext:
        if self.next_handler:
            return await self.next_handler.handle(context, ai_client)
        return context


class QuestionAgent(BasicAgent):
    async def handle(self, context: InterviewContext, ai_client: AIClient) -> InterviewContext:
        if not context.questions:
            prompt = prompts["question"].format(job_title=context.job_title)
            text = await ai_client.generate_text(prompt)
            context.questions = tuple(text.split("\n")[:3])
        return await super().handle(context, ai_client)


class EvaluationAgent(BasicAgent):
    async def handle(self, context: InterviewContext, ai_client: AIClient) -> InterviewContext:
        if not context.scores and context.responses:
            prompt = prompts["evaluation"].format(questions=context.questions, responses=context.responses)
            text = await ai_client.generate_text(prompt)
            context.scores = tuple(text.split("\n")[:3])
        return await super().handle(context, ai_client)


class ValidationAgent(BasicAgent):
    async def handle(self, context: InterviewContext, ai_client: AIClient) -> InterviewContext:
        if not context.feedback and context.scores:
            prompt = prompts["validation"].format(questions=context.questions, responses=context.responses, scores=context.scores)
            text = await ai_client.generate_text(prompt)
            context.scores = tuple(text.split("\n")[:3])
            context.feedback = text.split("\n")[3]
        return await super().handle(context, ai_client)


class Workflow():
    def __init__(self, ai_client: AIClient, agents: list):
        self.ai_client = ai_client
        self._handler = self.construct_handler_chain(agents)

    def construct_handler_chain(self, agents: list):
        handler_chain = None
        for agent in reversed(agents):
            agent.next_handler = handler_chain
            handler_chain = agent
        return handler_chain

    async def run(self, context) -> InterviewContext:
        return await self._handler.handle(context, self.ai_client)


async def get_workflow(config: ConfigDep) -> Workflow:
    agents = [QuestionAgent(), EvaluationAgent(), ValidationAgent()]
    return Workflow(OpenAIDriver(config.openai_api_key), agents)
