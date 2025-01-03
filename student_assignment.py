import json
import traceback

from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

gpt_chat_version = "gpt-4o"
gpt_config = get_model_configuration(gpt_chat_version)


def generate_hw01(question):
    prompt = "Please provide the anniversaries in Taiwan for the specified month and year in JSON format with keys 'date' and 'event'. Only return the JSON content."
    answer = demo(question, prompt)
    
    try:
        # Extract JSON content from the response
        json_start = answer.content.find('```json')
        json_end = answer.content.rfind('```')
        if json_start != -1 and json_end != -1:
            json_content = answer.content[json_start + 7:json_end].strip()
            parsed_answer = json.loads(json_content)
            
            # Ensure the result is in the correct format
            if isinstance(parsed_answer, list):
                return json.dumps({"Result": parsed_answer})
            else:
                return json.dumps({"error": "Unexpected response format"})
        else:
            return json.dumps({"error": "JSON content not found in response"})
    except Exception as e:
        return json.dumps({"error": str(e), "traceback": traceback.format_exc()})


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

# Testing
# 1
# print(generate_hw01("2024年台灣10月紀念日有哪些?"))
# 2
# print(generate_hw02("2024年台灣10月紀念日有哪些"))
# 3
# question1 = '2024年台灣10月紀念日有哪些?'
# question2 = '根據先前的節日清單，這個節日是否有在該月份清單？{"date": "10-31", "name": "蔣公誕辰紀念日"}'
# print(generate_hw03(question1, question2))
# 4
# question = '請問中華台北的積分是多少?'
# print(generate_hw04(question))