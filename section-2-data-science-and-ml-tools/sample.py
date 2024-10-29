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
        response = openai.ChatCompletion.create(model='gpt-4', messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}])
        return response['choices'][0]['message']['content']
    except openai.error.RateLimitError:
        time.sleep(60)
        return get_chat_response(system_prompt, user_prompt)
    except openai.error.OpenAIError as e:
        print(f'Error: {e}')
        return None

def check_for_dynamic_objects():
    print('Updated function code executed.')
if __name__ == '__main__':
    response = check_for_dynamic_objects()
    print(response)