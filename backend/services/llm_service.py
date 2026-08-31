import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_answer(query: str, context_chunks: list[str]) -> str:
    """Generate an answer using a local Ollama LLM."""

    if not context_chunks:
        return "I could not find relevant information in the document."

    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI document assistant.

Answer the user's question using ONLY the provided document context.

If the answer is not available in the context, say:
"I could not find this information in the document."

Do not invent or assume information.

Document context:
{context}

User question:
{query}

Answer:
""".strip()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

    except requests.ConnectionError:
        return "Unable to connect to Ollama. Please make sure Ollama is running."

    except requests.Timeout:
        return "The AI model took too long to respond. Please try again."

    except requests.RequestException:
        return "The AI service is currently unavailable. Please try again."

    return response.json()["response"].strip()