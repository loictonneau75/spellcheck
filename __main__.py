from src.spellcheck import SpellCheck
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    sp = SpellCheck(os.getenv("OPENAI_API_KEY"),"fr")
    print(sp("coocou"))
