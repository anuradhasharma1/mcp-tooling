import os
from openai import OpenAI


class Claude:
    def __init__(self, model: str):
        self.client = OpenAI(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            base_url=os.getenv("ANTHROPIC_BASE_URL")
        )

        self.model = model

    def add_user_message(self, messages: list, message):
        user_message = {
            "role": "user",
            "content": str(message),
        }
        messages.append(user_message)

    def add_assistant_message(self, messages: list, message):
        assistant_message = {
            "role": "assistant",
            "content": str(message),
        }
        messages.append(assistant_message)

    def text_from_message(self, message):
        return str(message)

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ):

        if system:
            messages.insert(
                0,
                {
                    "role": "system",
                    "content": system,
                },
            )

        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        if tools:
            params["tools"] = tools

        response = self.client.chat.completions.create(**params)

        return response.choices[0].message.content