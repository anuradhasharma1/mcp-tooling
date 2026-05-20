from core.claude import Claude
from mcp_client import MCPClient
from anthropic.types import MessageParam


class Chat:
    def __init__(self, claude_service: Claude, clients: dict[str, MCPClient]):
        self.claude_service: Claude = claude_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[MessageParam] = []

    async def _process_query(self, query: str):
        self.messages.append(
            {
                "role": "user",
                "content": query,
            }
        )

    async def run(
        self,
        query: str,
    ) -> str:

        await self._process_query(query)

        response = self.claude_service.chat(
            messages=self.messages,
        )

        self.claude_service.add_assistant_message(
            self.messages,
            response,
        )

        return str(response)