import openai
import time
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

openai.api_key = os.getenv('OPENAI_API_KEY')

# Helper function to send OpenAI chat completion requests
def get_chat_response(system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.error.RateLimitError:
        time.sleep(60)  # Wait for 60 seconds before retrying
        return get_chat_response(system_prompt, user_prompt)
    except openai.error.OpenAIError as e:
        print(f"Error: {e}")
        return None

# Main function to check if dynamic objects exist for a connector
def check_for_dynamic_objects():
    system_prompt = """
    You are an AI assistant that retrieves specific information for ETL connectors. Your task is to extract data based on the given parameters and return only the allowed value that closely matches the requested field or multiple fields *Instructions**: - connector: {The name of the ETL Connector} - field: {The field to retrieve information from} - type: {The type of the data that needs to be returned. If the user specifies a JSON list return a JSON type array return all the possible values. If the user specifies JSON Object return an object} - description: {Description of what the field we are requesting} - Allowed Values: {A list of predefined field return values, if it is not specified, try to find any values} *Processing Steps**: 1. Look up the relevant {type} (e.g., ETL Connector) specified in the request. 2. Extract the {field} for that connector. 3. Compare the extracted value to the list of Allowed Values. 4. Return the closest match from the Allowed Values list. 5. Output only the allowed value without any additional explanation or formating. If it is JSON return just the JSON and nothing else 6. if multiple fields are passed in, return back both fields. 7. Return in a json object array format with a attribute field:{field}, and attribute value:{returned value} as the value returned and null if the value could not be found
    """
    
    user_prompt = '''{
        "Connector": "Salesforce",
        "field": "supported and development environments",
        "description": "the available environments a user can interact with the connector in. If N/A then save PROD",
        "data_type": "JSON String array"
    }'''

    return get_chat_response(system_prompt, user_prompt)

if __name__ == "__main__":
    response = check_for_dynamic_objects()
    print(response)
    