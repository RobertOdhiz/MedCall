from ibm_watsonx_ai import APIClient, Credentials
from langchain_ibm import ChatWatsonx
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()

model = "meta-llama/llama-3-3-70b-instruct"
service_url = os.getenv("WATSONX_URL")
space_id = os.getenv("WATSONX_SPACE_ID")
version = os.getenv("WATSONX_VERSION")


def get_client(agent_service_id: str) -> APIClient:
    credentials = Credentials(
        url=service_url,
        # token=os.getenv("WATSONX_IAM"),
        api_key=os.getenv("WATSONX_API_KEY"),
    )
    client = APIClient(credentials)
    client.default_space_id = space_id
    return client


def create_chat_model(client: APIClient):
    parameters = {
        "frequency_penalty": 0,
        "max_tokens": 2000,
        "presence_penalty": 0,
        "temperature": 0,
        "top_p": 1
    }
    return ChatWatsonx(
        model_id=model,
        url=service_url,
        space_id=space_id,
        params=parameters,
        watsonx_client=client
    )


def analyze_symptoms(messages: List[Dict[str, str]]) -> str:
    agent_service_id = os.getenv("SYMPTOM_CHECKER_ID")
    client = get_client(agent_service_id)
    model = create_chat_model(client)
    response = model.invoke(messages)
    return response.content


def log_patient_info(messages: List[Dict[str, str]]) -> str:
    agent_service_id = os.getenv("PATIENT_LOGGER_ID")
    client = get_client(agent_service_id)
    model = create_chat_model(client)
    response = model.invoke(messages)
    return response.content


def evaluate_emergency(messages: List[Dict[str, str]]) -> str:
    agent_service_id = os.getenv("EMERGENCY_ESCALATION_ID")
    client = get_client(agent_service_id)
    model = create_chat_model(client)
    response = model.invoke(messages)
    return response.content


def summarize_models_responses(messages: List[Dict[str, str]]) -> str:
    agent_service_id = os.getenv("NLP_SUMMARY_ID")
    client = get_client(agent_service_id)
    model = create_chat_model(client)
    response = model.invoke(messages)
    return response.content