
from supp.config import todo
from os import environ

from langchain_community.llms import Cohere, Ollama 
from langchain_community.chat_models import ChatCohere, ChatOllama
from langchain_openai import OpenAI, ChatOpenAI


def get_llm():

    if environ.get('COHERE_API_KEY'): 
        return Cohere(), ChatCohere()

    if environ.get('OPENAI_API_KEY'): 
        return OpenAI(), ChatOpenAI()

    if environ.get('OLLAMA_BASE_URL'): return Ollama(
        base_url=environ.get('OLLAMA_BASE_URL'), 
        model=environ.get('OLLAMA_MODEL'),
        temperature=0
    )


def get_app_prompt(app=None):
    return f'{todo["prompt"][:17]}{ app if app else "?"}> '


_BLUE = '\033[94m'
_RESET = '\033[0m'

def print_blue(text):
    print(f'{_BLUE}{text}{_RESET}')

