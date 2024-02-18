from os import getenv
import openai
import logging

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

openai.api_key  = getenv('OPENAI_API_KEY')

def get_completion(prompt: str, tool_name: str, model: str = "gpt-3.5-turbo-0125") -> dict:
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        top_p=0.1,
    )

    try:
        final_response = {"message": response.choices[0].message.content, "tool_name": tool_name}
    
    except openai.AuthenticationError as e:
        final_response = {"message": "Try another openai key.", "tool_name": tool_name}
        logging.error(e)

    except Exception as e:
        final_response = {"message": "Error: try again later.", "tool_name": tool_name}
        logging.error("Error: try again later.")
        logging.error(e)
    return final_response
