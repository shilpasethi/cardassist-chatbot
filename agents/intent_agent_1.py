import os
from dotenv import load_dotenv
from utils.llm_wrapper import LLMWrapper 

# Load environment variables (including GROQ_API_KEY)
load_dotenv()


class IntentAgent:
    """
    IntentAgent: Classifies user input into intents using an LLM with ReAct prompting
    and autonomously decides which tool to call based on the detected intent.
    """

    def __init__(self, groq_key, api_agent, knowledge_agent, temperature: float = 0.0):
        """
        Initialize the IntentAgent with the LLMWrapper for intent classification.

        :param api_agent: APIAgent instance for card operations.
        :param knowledge_agent: KnowledgeAgent instance for knowledge retrieval.
        :param temperature: Sampling temperature for the model.
        """
        # Initialize LLMWrapper
        self.llm = LLMWrapper(api_key=groq_key)

        # Define available tools
        self.tools = {
            "activate": api_agent.activate_card,
            "deactivate": api_agent.deactivate_card,
            "knowledge": knowledge_agent.answer_question,
        }

    def get_intent(self, user_input: str) -> str:
        """
        Determine the intent of the user input by querying the LLM using a ReAct-style prompt.

        :param user_input: The user's raw input string.
        :return: One of "activate", "deactivate", or "knowledge".
        """
        # Craft a ReAct-style prompt for the LLM
        prompt = (
            "You are an intent classification assistant\n"
            "For the given user input, think step-by-step (Thought), choose an Action from CLASSIFY_INTENT[activate/deactivate/knowledge],"
            " and then provide the final classification in the Answer step.\n"
            "Respond strictly in this format (no additional text):\n"
            "Thought: <your reasoning>\n"
            "Action: CLASSIFY_INTENT[<intent>]\n"
            "Answer: <intent>\n"
            f"User Input: \"{user_input}\"\n"
        )

        # Call the LLMWrapper to generate an answer
        response = self.llm.generate_answer(prompt)

        # Parse the Answer line from the LLM's response
        intent = None
        for line in response.splitlines()[::-1]:
            if line.lower().startswith("answer:"):
                intent = line.split(":", 1)[1].strip().lower()
                break

        # Validate and fallback
        if intent not in self.tools:
            intent = "knowledge"

        return intent

    def decide_and_execute(self, user_input: str) -> str:
        """
        Decide which tool to call based on the user input and execute it.

        :param user_input: The user's raw input string.
        :return: The result of the tool execution.
        """
        # Determine the intent
        intent = self.get_intent(user_input)
        print(f"Detected intent: {intent}")

        # Execute the corresponding tool
        tool = self.tools.get(intent)
        print(f"Tool to execute: {tool}")
        if not tool:
            return "I'm sorry, I couldn't determine the appropriate action for your request."

        return tool(user_input)