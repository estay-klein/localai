"""
Pipes module for LocalAI Stack.
Contains pipe implementations for integrating with external services (n8n, etc.).
"""

from .n8n_pipe import Pipe

__all__ = ["Pipe"]