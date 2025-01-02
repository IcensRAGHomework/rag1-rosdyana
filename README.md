[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/j1SuxzcN)
# Prompt Engineer Homework Questions

## Homework Content

Please complete the following assignment using the **LangChain** suite and implement the provided method `generate_hw01-04(question)`. Implemented in `student_assignment.py`.
#### Create `.env` file (for student use)

In this assignment, you will set up the necessary parameters in your local development environment to enable the program to run. To simplify the management of environment variables, create a file named `.env` in the project root directory and define the environment variables in it.

The main purpose of this `.env` file is to enable you to implement it on your own computer and provide the required parameters to the `model_configurations.py` file. When taking part in the assignment, we will provide specific parameter values ​​for you to fill in. The following is an example format of a .env file:


```makefile
AZURE_OPENAI_GPT4O_ENDPOINT=your_endpoint_here
AZURE_OPENAI_GPT4O_KEY=your_api_key_here
AZURE_OPENAI_GPT4O_DEPLOYMENT_CHAT=your_deployment_name_here
AZURE_OPENAI_GPT4O_VERSION=your_api_version_here
```
#### Things to note

- **Do not upload `.env` files to any version control system (such as GitHub)** to avoid leaking sensitive information.
- The `.env` file is for use in your local environment only and does not need to be included when submitting a job.

---

### Assignment 1

1. **Question**: `Please answer what are the anniversaries in specific months in Taiwan (please present it in JSON format)?`
2. **Example**: `What are the October anniversaries in Taiwan in 2024?`
3. **Method**: Implement `generate_hw01(question)` to answer the above questions.
4. **Output format**:
   - JSON The format is as follows：
     ```json
     {
         "Result": 
             {
                 "date": "2024-10-10",
                 "name": "國慶日"
             }
     }
     ```

---

### Assignment 2

1. **Question**: `Please answer what are the anniversaries in specific months in Taiwan (please present it in JSON format)?`
2. **Example**: `What are the October anniversaries in Taiwan in 2024?`
3. **Method**:
    - Use Function Calling to query the specified API.
    - Implement `generate_hw02(question)` to answer the above question.
4. **Specify API**:
    - Use [Calendarific API](https://calendarific.com/).
    - Steps:
        1. Visit the Calendarific website and register for an account.
        2. After logging in, enter the Dashboard and obtain your API Key.
5. **Output format**:
   - JSON The format is as follows：
     ```json
     {
         "Result": [
             {
                 "date": "2024-10-10",
                 "name": "國慶日"
             },
             {
                 "date": "2024-10-09",
                 "name": "重陽節"
             },
             {
                 "date": "2024-10-21",
                 "name": "華僑節"
             },
             {
                 "date": "2024-10-25",
                 "name": "台灣光復節"
             },
             {
                 "date": "2024-10-31",
                 "name": "萬聖節"
             }
         ]
     }
     ```
     
---

### Assignment 3

1. **Question**: `Based on the answer to Assignment 2, check whether a certain holiday is included in the holiday list for that month, and respond whether the holiday needs to be added`
2. **Example**: `According to the previous holiday list, is this holiday {"date": "10-31", "name": "蔣公誕辰紀念日"} included in the list of this month? `
3. **Method**:
    - Use RunnableWithMessageHistory to remember the previous answer.
    - Implement `generate_hw03(question2, question3)` to answer the above questions. PS.question2 is a question from homework 2
4. **Output format**:
    - add: This is a **Boolean** value indicating whether the festival needs to be added to the festival list. Determine whether the holiday exists in the list according to the question. If it does not exist, it is true; otherwise, it is false.
    - reason: Describe why the new holiday is needed or not, specify whether the holiday already exists in the list, and the contents of the current list.
    - The JSON format is as follows:
        ```json
        {
            "Result": 
                {
                    "add": true,
                    "reason": "The anniversary of Chiang Kai-shek's birth is not included in the list of October holidays. Existing holidays in October include National Day, Double Ninth Festival, Overseas Chinese Day, Taiwan Liberation Day and Halloween. Therefore, if the day is recognized as a holiday, it should be added to the list."
                }
        }
        ```

---

### Assignment 4

1. **Question**: `Please parse the provided image file baseball.png and answer the relevant questions in the image. `
2. **Example**: `How many points are there in Chinese Taipei`
3. **Method**:
    - Use the provided image file baseball.png as the input data source to analyze the image content and answer questions through the program.
    - Implement `generate_hw04(question)` to answer the above question.
4. **Output format**:
    - The JSON format is as follows:
        ```json
        {
            "Result": 
                {
                    "score": 5498
                }
        }
        ```

---

### Notes
- Method implementation must be done using the **LangChain** package.
- Make sure the format of the output is consistent with the example.
### Reference sources
- [Assignment 1](https://python.langchain.com/docs/how_to/few_shot_examples_chat/)
- [Job 2](https://python.langchain.com/api_reference/langchain/agents/langchain.agents.agent.AgentExecutor.html#langchain.agents.agent.AgentExecutor)
- [Assignment 2](https://python.langchain.com/api_reference/langchain/agents/langchain.agents.openai_functions_agent.base.create_openai_functions_agent.html)
- [Assignment 3](https://python.langchain.com/docs/how_to/agent_executor/)
- [Assignment 4](https://learn.microsoft.com/zh-tw/azure/ai-services/openai/how-to/gpt-with-vision?tabs=rest)

