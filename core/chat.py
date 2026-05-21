from core.claude import Claude
from mcp_client import MCPClient
from anthropic.types import MessageParam


class Chat:
    def __init__(self, claude_service: Claude, clients: dict[str, MCPClient]):
        self.claude_service: Claude = claude_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[MessageParam] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def _get_all_tools(self) -> list:
        tools = []
        for client in self.clients.values():
            client_tools = await client.list_tools()
            for tool in client_tools:
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    }
                })
        return tools

    async def _find_client_for_tool(self, tool_name: str) -> MCPClient | None:
        for client in self.clients.values():
            tools = await client.list_tools()
            if any(t.name == tool_name for t in tools):
                return client
        return None

    async def run(self, query: str) -> str:
        await self._process_query(query)
        tools = await self._get_all_tools()

        while True:
            response = self.claude_service.chat(
                messages=self.messages,
                tools=tools if tools else None,
            )

          
            if not response.choices[0].message.tool_calls:
                final_text = response.choices[0].message.content
                self.claude_service.add_assistant_message(self.messages, final_text)
                return str(final_text)

            # Handle tool calls
            tool_calls = response.choices[0].message.tool_calls

            # Add assistant's tool call message to history
            self.messages.append({
                "role": "assistant",
                "content": response.choices[0].message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    }
                    for tc in tool_calls
                ]
            })

            # Execute each tool and add results
            for tc in tool_calls:
                import json
                tool_name = tc.function.name
                tool_input = json.loads(tc.function.arguments)

                client = await self._find_client_for_tool(tool_name)
                if client:
                    result = await client.call_tool(tool_name, tool_input)
                    tool_result = result.content[0].text if result.content else "No result"
                else:
                    tool_result = f"Tool {tool_name} not found"

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": tool_result,
                })