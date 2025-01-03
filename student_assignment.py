import json
import traceback

from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

gpt_chat_version = "gpt-4o"
gpt_config = get_model_configuration(gpt_chat_version)


def generate_hw01(question):
    prompt = "Please format the result as JSON with Result: { date, name }"
    answer = demo(question, prompt)

    # Strip the markdown code block and parse the JSON content
    json_content = answer.content.strip("```json\n").strip("```")
    parsed_answer = json.loads(json_content)

    # Transform the result from a list to a single object
    if (
        "Result" in parsed_answer
        and isinstance(parsed_answer["Result"], list)
        and len(parsed_answer["Result"]) > 0
    ):
        parsed_answer["Result"] = parsed_answer["Result"][0]

    return parsed_answer


def generate_hw02(question):
    pass


def generate_hw03(question2, question3):
    pass


def generate_hw04(question):
    pass


def demo(question, prompt):
    llm = AzureChatOpenAI(
        model=gpt_config["model_name"],
        deployment_name=gpt_config["deployment_name"],
        openai_api_key=gpt_config["api_key"],
        openai_api_version=gpt_config["api_version"],
        azure_endpoint=gpt_config["api_base"],
        temperature=gpt_config["temperature"],
    )
    system_message = SystemMessage(content=prompt)
    human_message = HumanMessage(
        content=[
            {"type": "text", "text": question},
        ]
    )
    response = llm.invoke([system_message, human_message])

    return response
