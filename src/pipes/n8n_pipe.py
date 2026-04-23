"""
title: n8n Pipe Function
author: Cole Medin
author_url: https://www.youtube.com/@ColeMedin
version: 0.1.0

This module defines a Pipe class that utilizes N8N for an Agent.
A "Pipe" is a component that can be inserted into an AI agent's workflow to
call external services (in this case, an n8n workflow) and process the response.

The pipe receives a conversation body, extracts the last user message, sends it
to a configured n8n webhook, and appends the workflow's output as an assistant
message. It also emits status events for real‑time progress indication.
"""

from typing import Optional, Callable, Awaitable
from pydantic import BaseModel, Field
import os
import time
import requests


class Pipe:
    """
    Pipe implementation for integrating n8n workflows into an AI agent.

    The pipe is configured via a `Valves` model (configuration parameters).
    It expects an n8n webhook URL and a bearer token for authentication.
    When invoked, it sends the last user message to the webhook and returns
    the workflow's response.

    Attributes:
        type (str): Always "pipe" (identifies this as a pipe component).
        id (str): Unique identifier "n8n_pipe".
        name (str): Human‑readable name "N8N Pipe".
        valves (Valves): Configuration instance with defaults.
        last_emit_time (float): Timestamp of the last status emission.
    """

    class Valves(BaseModel):
        """
        Configuration parameters for the n8n pipe (valves = knobs to adjust).

        Fields:
            n8n_url (str): Full URL of the n8n webhook.
                Example: "https://n8n.example.com/webhook/your‑webhook‑id"
            n8n_bearer_token (str): Bearer token for authenticating to n8n.
            input_field (str): JSON field name where the user message is placed
                in the payload sent to n8n (default: "chatInput").
            response_field (str): JSON field name from which the response is
                extracted in n8n's reply (default: "output").
            emit_interval (float): Minimum seconds between status emissions
                (default: 2.0). Prevents flooding the UI with progress events.
            enable_status_indicator (bool): Whether to emit status events
                (default: True). Set to False to silence progress updates.
        """
        n8n_url: str = Field(
            default="https://n8n.[your domain].com/webhook/[your webhook URL]",
            description="Full URL of the n8n webhook (including /webhook/ path)"
        )
        n8n_bearer_token: str = Field(
            default="...",
            description="Bearer token for n8n authentication"
        )
        input_field: str = Field(
            default="chatInput",
            description="JSON field name for the user message in the request payload"
        )
        response_field: str = Field(
            default="output",
            description="JSON field name for the workflow response in n8n's reply"
        )
        emit_interval: float = Field(
            default=2.0,
            description="Interval in seconds between status emissions"
        )
        enable_status_indicator: bool = Field(
            default=True,
            description="Enable or disable status indicator emissions"
        )

    def __init__(self):
        """Initialize the pipe with default configuration."""
        self.type = "pipe"
        self.id = "n8n_pipe"
        self.name = "N8N Pipe"
        self.valves = self.Valves()
        self.last_emit_time = 0
        pass

    async def emit_status(
        self,
        __event_emitter__: Callable[[dict], Awaitable[None]],
        level: str,
        message: str,
        done: bool,
    ):
        """
        Emit a status event to the UI (if enabled and enough time has passed).

        Args:
            __event_emitter__: Async callback that sends events to the frontend.
                If None, no emission occurs.
            level: Severity level ("info", "error", etc.).
            message: Human‑readable status description.
            done: Whether the operation is complete (final status).
        """
        current_time = time.time()
        if (
            __event_emitter__
            and self.valves.enable_status_indicator
            and (
                current_time - self.last_emit_time >= self.valves.emit_interval or done
            )
        ):
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "status": "complete" if done else "in_progress",
                        "level": level,
                        "description": message,
                        "done": done,
                    },
                }
            )
            self.last_emit_time = current_time

    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
        __event_call__: Callable[[dict], Awaitable[dict]] = None,
    ) -> Optional[dict]:
        """
        Main pipe entry point. Called by the agent when the pipe is activated.

        Workflow:
          1. Emit a "calling n8n" status.
          2. Extract the last user message from the conversation body.
          3. Build a JSON payload with the message and a session ID.
          4. POST the payload to the n8n webhook (authenticated with bearer token).
          5. Extract the response from the n8n reply.
          6. Append the response as an assistant message to the conversation.
          7. Emit a completion status and return the response.

        Args:
            body: The conversation body (contains "messages" list).
            __user__: Optional user metadata (e.g., user ID for session tracking).
            __event_emitter__: Callback for emitting status events.
            __event_call__: Unused in this pipe (reserved for future extensions).

        Returns:
            The n8n response as a string, or a dict with an "error" key on failure.
        """
        await self.emit_status(
            __event_emitter__, "info", "/Calling N8N Workflow...", False
        )

        messages = body.get("messages", [])

        # Verify a message is available
        if messages:
            question = messages[-1]["content"]
            try:
                # Invoke N8N workflow
                headers = {
                    "Authorization": f"Bearer {self.valves.n8n_bearer_token}",
                    "Content-Type": "application/json",
                }
                # Create a session ID from user ID and first message (truncated)
                payload = {"sessionId": f"{__user__['id']} - {messages[0]['content'].split('Prompt: ')[-1][:100]}"}
                payload[self.valves.input_field] = question
                response = requests.post(
                    self.valves.n8n_url, json=payload, headers=headers
                )
                if response.status_code == 200:
                    n8n_response = response.json()[self.valves.response_field]
                else:
                    raise Exception(f"Error: {response.status_code} - {response.text}")

                # Set assistant message with chain reply
                body["messages"].append({"role": "assistant", "content": n8n_response})
            except Exception as e:
                await self.emit_status(
                    __event_emitter__,
                    "error",
                    f"Error during sequence execution: {str(e)}",
                    True,
                )
                return {"error": str(e)}
        # If no message is available alert user
        else:
            await self.emit_status(
                __event_emitter__,
                "error",
                "No messages found in the request body",
                True,
            )
            body["messages"].append(
                {
                    "role": "assistant",
                    "content": "No messages found in the request body",
                }
            )

        await self.emit_status(__event_emitter__, "info", "Complete", True)
        return n8n_response
