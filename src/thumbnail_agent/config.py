from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI 
load_dotenv()

PROMPT_MODEL = "gpt-4o-mini"
CRITIC_MODEL = "gpt-4o"
IMAGE_MODEL = "gpt-image-2"


def get_prompt_llm():

    return ChatOpenAI(
        model=PROMPT_MODEL,
        temperature=0.7
    )


def get_critic_llm():

    return ChatOpenAI(
        model=CRITIC_MODEL,
        temperature=0
    )


def get_image_client():
    return OpenAI()