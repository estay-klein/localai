#!/bin/bash
# Load variables correctly
set -a
[ -f .env ] && source .env
set +a

# Launch Aider with the current active Gemini version
aider --model deepseek/deepseek-v4-pro \
      --editor-model ollama/deepseek-coder-v2:16b \
      --openai-api-base http://localhost:11435/v1 \
      --no-show-model-warnings