from groq import Groq

class LLMWrapper:
    """
    A wrapper around Groq-hosted LLaMA3 for generating answers.
    """
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key) #

    def generate_answer(self, prompt: str) -> str:
        """
        Generate an answer from the LLaMA3 model.
        """
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specializing in card management services."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500,
        )

        return response.choices[0].message.content.strip()




# utils/llm_wrapper.py (Updated for OpenAI GPT-4)

# """
# LLMWrapper: Encapsulates OpenAI GPT-4 model for answer generation.
# """

# import openai
# from groq import Groq
# import os

# class LLMWrapper:
#     """
#     A wrapper around OpenAI's GPT-4 for generating answers.
#     """
#     def __init__(self):
#         openai.api_key = os.getenv("OPENAI_API_KEY")  # Read API Key from environment

#         #groq_api_key = os.getenv("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")
#         client = Groq(api_key="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")

#     def generate_answer(self, prompt: str) -> str:
#         """
#         Generate an answer given a text prompt using OpenAI GPT-4.
#         """
#         # response = openai.ChatCompletion.create(
#         #     model="gpt-4",
#         #     messages=[
#         #         {"role": "system", "content": "You are a helpful assistant specializing in card management services."},
#         #         {"role": "user", "content": prompt}
#         #     ],
#         #     temperature=0.2,
#         #     max_tokens=500,
#         # )
        
#         chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Explain the importance of fast language models"
#             }
#         ],
#         temperature=0.2,
#         max_tokens=500,
 
#         model="llama3-70b-8192"
#     )
        
        
#     return response['choices'][0]['message']['content'].strip()
