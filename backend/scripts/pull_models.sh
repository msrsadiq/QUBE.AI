# backend/scripts/pull_models.sh

#!/bin/sh
echo "Pulling Ollama models..."

# Pull recommended models for testing
ollama pull llama2
ollama pull codellama
ollama pull mistral
ollama pull phi

echo "Models pulled successfully!"

# Keep container running
tail -f /dev/null

---