import json
import traceback

from model_configurations import get_model_configuration, get_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory
from typing import Dict, List, Any

gpt_chat_version = "gpt-4o"
gpt_config = get_model_configuration(gpt_chat_version)
calendarific_api_key = (
    get_configuration("CALENDARIFIC_API_KEY") or "GoVBey5KrDM8ehxPmwm5LKSG7gWYN3p0"
)

llm = AzureChatOpenAI(
    model=gpt_config["model_name"],
    deployment_name=gpt_config["deployment_name"],
    openai_api_key=gpt_config["api_key"],
    openai_api_version=gpt_config["api_version"],
    azure_endpoint=gpt_config["api_base"],
    temperature=gpt_config["temperature"],
)


def generate_hw01(question):
    prompt = "Please provide the anniversaries in Taiwan for the specified month and year in JSON format with keys 'date' and 'event'. Only return the JSON content."
    answer = hw01_helper(question, prompt)

    try:
        json_start = answer.content.find("```json")
        json_end = answer.content.rfind("```")
        if json_start != -1 and json_end != -1:
            json_content = answer.content[json_start + 7 : json_end].strip()
            parsed_answer = json.loads(json_content)

            if isinstance(parsed_answer, list):
                return json.dumps({"Result": [parsed_answer[0]]})
            else:
                return json.dumps({"error": "Unexpected response format"})
        else:
            return json.dumps({"error": "JSON content not found in response"})
    except Exception as e:
        return json.dumps({"error": str(e), "traceback": traceback.format_exc()})


def generate_hw02(question):
    response = hw02_helper(question)
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "get_anniversaries":
                function_args = tool_call["args"]
                country = function_args["country"]
                month = function_args["month"]
                year = function_args["year"]
                anniversaries = get_anniversaries(country, month, year)
                holidays = anniversaries.get("response").get("holidays")
                parsed_holidays = [
                    {"date": holiday["date"]["iso"], "name": holiday["name"]}
                    for holiday in holidays
                ]

                return json.dumps({"Result": parsed_holidays})


def generate_hw03(question2, question3):
    hw2_answer = generate_hw02(question2)

    holidays_data = json.loads(hw2_answer)
    holidays_list = holidays_data.get("Result", [])

    holidays_text = "Here are the holidays list:\n"
    for holiday in holidays_list:
        holidays_text += f"- {holiday['date']}: {holiday['name']}\n"

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Use the conversation history to provide context-aware responses.",
            ),
            ("human", "{input}"),
        ]
    )

    sessions: Dict[str, ChatMessageHistory] = {}

    def get_session_history(session_id: str) -> ChatMessageHistory:
        if session_id not in sessions:
            sessions[session_id] = ChatMessageHistory()
        return sessions[session_id]

    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    session_history = get_session_history("1")
    session_history.add_user_message(question2)
    session_history.add_ai_message(holidays_text)

    response = chain_with_history.invoke(
        {"input": question3}, config={"configurable": {"session_id": "1"}}
    )

    result_content = response.content
    add = "yes" in result_content.lower()
    reason = result_content

    return json.dumps({"Result": {"add": add, "reason": reason}})


def generate_hw04(question):
    import re

    image_path = "baseball.png"
    base64_image = local_image_to_data_url(image_path)

    messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "Please parse the data from the image to get the country name and point. Answer the question based on the specific country's point from the image. Only return the point.",
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
            ],
        },
    ]

    response = llm.invoke(messages)

    match = re.search(r"(\d+)", response.content)
    point = int(match.group(1)) if match else 0
    return json.dumps({"Result": {"score": point}})


def hw01_helper(question, prompt):
    """
    Generates a response from an Azure OpenAI model based on the given question and prompt.

    Args:
        question (str): The question to be answered by the model.
        prompt (str): The system message or context to guide the model's response.

    Returns:
        str: The response generated by the Azure OpenAI model.
    """
    system_message = SystemMessage(content=prompt)
    human_message = HumanMessage(
        content=[
            {"type": "text", "text": question},
        ]
    )
    response = llm.invoke([system_message, human_message])
    return response


def hw02_helper(question):
    """
    Sends a question to the Azure OpenAI Chat model and invokes a specified tool to fetch anniversaries.

    Args:
        question (str): The question to be sent to the Azure OpenAI Chat model.

    Returns:
        response: The response from the Azure OpenAI Chat model after invoking the specified tool.

    The tool used in this function is:
        - get_anniversaries: Fetches the anniversaries for a specified country in ISO-3166 format, month, and year using the Calendarific API.
    """
    human_message = HumanMessage(
        content=[
            {"type": "text", "text": question},
        ]
    )

    tool = {
        "type": "function",
        "function": {
            "name": "get_anniversaries",
            "description": "Fetches the anniversaries for a specified country in ISO-3166 format, month, and year using the Calendarific API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {"type": "string"},
                    "month": {"type": "integer"},
                    "year": {"type": "integer"},
                },
                "required": ["country", "month", "year"],
            },
        },
    }

    response = llm.invoke([human_message], tools=[tool])
    return response


def get_anniversaries(country, month, year):
    """
    Fetches the anniversaries for a specified country, month, and year using the Calendarific API.

    Args:
        country (str): The country code iso-3166 format (e.g., 'ID' for Indonesia).
        month (int): The month for which to fetch anniversaries (1-12).
        year (int): The year for which to fetch anniversaries.

    Returns:
        dict: A dictionary containing the response from the Calendarific API, which includes the anniversaries.
    """
    import requests

    url = f"https://calendarific.com/api/v2/holidays?api_key={calendarific_api_key}&country={country}&year={year}&month={month}"
    response = requests.get(url)
    return response.json()


def local_image_to_data_url(image_path: str) -> str:
    """
    Convert a local image to a base64 data URL.

    Args:
        image_path (str): The file path to the local image.

    Returns:
        str: The base64 encoded data URL of the image.
    """
    import base64

    """Convert a local image to base64 data URL."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Testing
# 1
# print(generate_hw01("2024年台灣10月紀念日有哪些?"))
# print("--------------------------------------------------")
# 2
# print(generate_hw02("2024年台灣10月紀念日有哪些"))
# print("--------------------------------------------------")
# 3
# question1 = "2024年台灣10月紀念日有哪些?"
# question2 = '根據先前的節日清單，這個節日是否有在該月份清單？{"date": "10-31", "name": "蔣公誕辰紀念日"}'
# print(generate_hw03(question1, question2))
# print("--------------------------------------------------")
# 4
# question = "請問中華台北的積分是多少?"
# print(generate_hw04(question))
# print("--------------------------------------------------")
