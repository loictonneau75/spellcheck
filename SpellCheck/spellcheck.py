from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re


class SpellCheck:
    """
    Implements a spell checking and correction mechanism utilizing OpenAI's large language models (LLMs).
    This class provides functionality to check and correct spelling in text for a specified language using
    predefined models from OpenAI and a custom prompt template for generating queries to the model.

    Attributes:
        allowed_models (List[str]): Specifies the models that are permitted for use in spell checking. Currently,
            this is limited to "gpt-3.5-turbo" but can be expanded.
        YES (str): A constant value representing an affirmative response in the language checking logic.
        NO (str): A constant value representing a negative response in the language checking logic.

    Args:
        api_key (str): The API key required to access OpenAI's GPT models.
        language (str): The language code that determines the spell checking language. The implementation
            of `_get_language` method must validate this language against supported languages.
        model (str, optional): Specifies which OpenAI model to use for spell checking. Defaults to "gpt-3.5-turbo".
        temperature (float, optional): Controls the randomness in the model's response. Must be between 0 and 1.
            Defaults to 0.3.
        max (int, optional): Sets the maximum number of tokens to generate. Must be between 10 and 10,000.
            Defaults to 1000.
    """
    #todo: utiliser le webscrapping pour completer la liste
    allowed_models: list[str] = ["gpt-3.5-turbo", ]
    regex = r'^sk-[A-Za-z0-9]{20}T3BlbkFJT3BlbkFJ[A-Za-z0-9]{20}$'
    YES = "oui"
    NO = "non"

    def __init__(self, api_key: str, language: str, model: str = "gpt-3.5-turbo", temperature: float = 0.3, max: int = 1000) -> None:
        self.llm = self._create_llm(model, temperature, max, api_key)
        self.selected_language = self._get_language(language)
        self.prompt = self._prompt()


    def _create_llm(self, model: str, temperature: float, max: int, api_key: str) -> ChatOpenAI | ValueError:
        """
        Initializes and returns an instance of `ChatOpenAI` for spell checking, configured with the specified model
        parameters and API key.

        Args:
            model (str): The name of the OpenAI model to use for spell checking.
            temperature (float): The sampling temperature to use when generating responses from the model. Controls the
                randomness of the output, with a range from 0 (completely deterministic) to 1 (maximally random).
            max (int): The maximum number of tokens the model is allowed to generate in response to the input text.
            api_key (str): The API key for authenticating requests to OpenAI.

        Returns:
            ChatOpenAI: An instance of `ChatOpenAI` configured for spell checking.

        Raises:
            ValueError: If the specified model is not in the list of allowed models, if the temperature is not within
                the valid range [0, 1], if the maximum token count is outside the allowed range [10, 10000],
                or if the API key is not valid.
        """
        if model not in self.allowed_models:
            raise ValueError(f"Le modèle doit être parmi les suivants: {self.allowed_models}")
        if not (isinstance(temperature, float) and 0 <= temperature <= 1 and round(temperature, 1) == temperature):
            raise ValueError("La température doit être un float à 1 chiffre après la virgule et comprise entre 0 et 1.")
        if not (isinstance(max, int) and 10 <= max <= 10000):
            raise ValueError("Max doit être un entier compris entre 10 et 10 000.")
        if not (isinstance(api_key, str)) and not re.match(self.regex, api_key):
            raise ValueError("Votre clé API ne semble pas valide")
        return ChatOpenAI(
            model_name=model,
            temperature=temperature,
            max_tokens=max,
            verbose=True,
            api_key=api_key
        )

    def _get_language(self, language: str):
        """
        Validates the provided language and returns its corresponding language name in French if supported.

        This method simulates a chat interaction using a fixed prompt to determine if the language is supported and
        known. It relies on a simplistic AI-based logic to map language codes to French names.

        Args:
            language (str): The language code to validate and translate.

        Returns:
            str: The French name of the language if supported and recognized.

        Raises:
            ValueError: If the language is not supported or the language code is not recognized.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Tu dois dire si la langue fournie existe ou non, tu dois egalement reecrire la lanque en francais si tu la connais"),
                ("user","lih"),
                ("ai", f"{self.NO},undefined"),
                ("user","french"),
                ("ai",f"{self.YES},francais"),
                ("user","eng"),
                ("ai", f"{self.YES},anglais"),
                ("user", "{language}")
            ]
        )
        parser = StrOutputParser()
        chain = prompt | self.llm | parser
        output: list = chain.invoke({"language": language}).split(",")
        if output[0] == self.YES:
            return output[1]
        else: 
            raise ValueError(f"La langue fournie n'existe pas ou n'est pas prise en charge.\n value = {language} type = {type(language)}")

    def _prompt(self):
        """
        Generates and returns a chat prompt template for initiating spell checking interactions with the OpenAI model.

        This method crafts a prompt template that is used to guide the spell checking process, incorporating the selected
        language and setting up the context for correcting spelling errors in user-provided text.

        Returns:
            ChatPromptTemplate: A template object containing predefined messages and placeholders for dynamic content,
            specifically tailored for spell checking tasks.
        """
        return ChatPromptTemplate.from_messages(
           [
               ("system", "Tu es un assistant servant à me corriger les fautes d'orthographe en {language} dans des mots/textes."),
               ("user", "la phrase a corriger est : tomtae"),
               ("ai", "La phrase corrigée est : Tomate"),
               ("user", "la phrase a corriger est : bonojur commet allez vous"),
               ("ai", "La phrase corrigée est : Bonjour comment allez-vous ?"),
               ("user", "La phrase a corriger est : Je vais bien et toi ?"),
               ("ai", "La phrase corrigée est : Je vais bien et toi "),
               ("user", "la phrase a corriger est : {text}")
           ]
       )

    def __call__(self, text: str):
        """
        Processes the input text through the spell checking pipeline and returns the corrected text.

        This method acts as the primary interface for the `SpellCheck` class, taking user input text and processing it
        for spelling corrections in the specified language. It leverages the configured `ChatOpenAI` instance and the
        generated prompt template to interact with the OpenAI model and parse its output for corrections.

        Args:
            text (str): The text input by the user to be spell checked.

        Returns:
            str: The corrected version of the input text, as generated by the OpenAI model based on the spell checking
            interaction template.
        """
        parser = StrOutputParser()
        chain = self.prompt | self.llm | parser
        output:str = chain.invoke(
            {
                "language": self.selected_language,
                "text": text
            }
        )
        if output.startswith("La phrase corrigée est : "):
            output = output.replace("La phrase corrigée est : ", "")
        if output.startswith("Le mot corrigé est : "):
            output = output.replace("Le mot corrigé est : ", "")
        if output.startswith("Il n'y a pas de faute dans le mot \""):
            output= output.replace("Il n'y a pas de faute dans le mot \"", "")
            output = output.replace("\".","")
        if output.startswith("Il n'y a pas de faute dans la phrase \""):
            output= output.replace("Il n'y a pas de faute dans la phrase \"", "")
            output = output.replace("\".","")
        return output
