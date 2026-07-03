from groq import Groq
import json

import config.secrets

class LLM:
    client:str
    model = "llama-3.3-70b-versatile"

    def init_client():
        LLM.client = Groq(api_key=config.secrets.GROQ_API_KEY)

    def generate_text(query:str, rag:str = None):
        chat_completion = LLM.client.chat.completions.create(
            messages=[
                {
                "role": "system",
                    "content": (
                        "You are a system error explanation assistant.\n"
                        "You MUST return ONLY valid JSON. No markdown, no extra text.\n\n"
                        "Output format:\n"
                        "{\n"
                        '  "explanation": string,\n'
                        '  "solution": string\n'
                        "}\n\n"
                        "Rules:\n"
                        "- explanation: simple, non-technical, easy to understand\n"
                        "- solution: numbered step-by-step fixes\n"
                        "- If RAG context is provided, you may use it, but DO NOT depend on it.\n"
                        "- If RAG context is missing or empty (None/null/''), ignore it completely.\n"
                        "- Focus on the error message as the primary source of truth.\n"
                    )
                },
                {
                "role": "user",
                    "content": f"""
                        Error Query:
                        {query}

                        RAG Context (may be empty or None):
                        {rag if rag else "No RAG context available"}
                        """
                }
            ],

            # The language model which will generate the completion.
            model= LLM.model
        )

        result = chat_completion.choices[0].message.content

        try:
            result = json.loads(result)
            return result, True
        
        except json.JSONDecodeError:
            print("Could not parse LLM's output. Returning raw text")
            return result, False