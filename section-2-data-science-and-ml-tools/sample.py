import openai
import time
import os
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
openai.api_key = os.getenv('OPENAI_API_KEY')


def get_chat_response(system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(model='gpt-4', messages=[{
            'role': 'system', 'content': system_prompt}, {'role': 'user',
            'content': user_prompt}])
        return response['choices'][0]['message']['content']
    except openai.error.RateLimitError:
        time.sleep(60)
        return get_chat_response(system_prompt, user_prompt)
    except openai.error.OpenAIError as e:
        print(f'Error: {e}')
        return None


def check_for_dynamic_objects():
    system_prompt = """
    You are an AI assistant that retrieves specific information for ETL connectors. Your task is to extract data based on the given parameters and return only the allowed value that closely matches the requested field or multiple fields.
    """
    user_prompt = """{
        "Connector": "SalesforceUpdated",
        "field": "supported and development environments for my application Updated",
        "description": "the available environments a user can interact with the connector in. If N/A then save PROD",
        "data_type": "JSON String array"
    }"""
    return get_chat_response(system_prompt, user_prompt, new_function_code)


if __name__ == '__main__':
    response = check_for_dynamic_objects()
    print(response)
