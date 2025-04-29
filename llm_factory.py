# llm_factory.py
import os
from dotenv import load_dotenv

load_dotenv()                       # reads .env once on import

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()


def get_llm(*, temperature: float = 0):
    """
    Return a langchain `BaseChatModel` for the provider chosen in .env
    (OpenAI by default). Extend as you add more providers.
    """
    if PROVIDER == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            temperature=temperature,
        )

    if PROVIDER == "mistral":
        from langchain_mistralai.chat_models import ChatMistralAI

        return ChatMistralAI(
            api_key=os.getenv("MISTRAL_API_KEY"),
            model=os.getenv("MISTRAL_MODEL", "mistral-medium"),
            temperature=temperature,
        )

    raise ValueError(f"Unsupported LLM provider: {PROVIDER}")
