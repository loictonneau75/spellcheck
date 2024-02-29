from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.1"
DESCRITPION = "SpellCheck is a Python library designed to check and correct spelling errors in texts across multiple language"
LONG_DESCRIPTION = "SpellCheck is a Python library designed to check and correct spelling errors in texts across multiple languages using OpenAI's large language models (LLMs). It leverages the `langchain_openai.ChatOpenAI` interface to offer a seamless integration for developers looking to enhance their applications with advanced spell checking capabilities."

setup(
    name = "spellcheck",
    version = VERSION,
    author = "Loïc TONNEAU",
    author_email = "loictonneau@gmail.com",
    description = DESCRITPION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = ["langchain_openai", "langchain_core"],
    keywords = ["python", "langchain", "autocorrect", "llm", "openai", "language", "corrector", "grammar", "spelling"]
)