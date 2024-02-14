from utils import get_completion
from models import SearchInput

from os import getenv
import openai
from langchain.agents import tool
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.schema.agent import AgentFinish
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.prompts import ChatPromptTemplate
import logging

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

openai.api_key  = getenv('OPENAI_API_KEY')

@tool(args_schema=SearchInput)
def generate_code(header: str) -> dict:
    """Useful when you need to write a python code from a user request.""" 
    
    prompt_template = f"""
    I need to write a code in python to solve this problem, can you help me?

    {header}

    Please comment each line in detail, \n
    and explain in detail what you did, and why.
    """

    final_response = get_completion(prompt_template, "generate_code")
    return final_response

@tool(args_schema=SearchInput)
def code_improve(header: str) -> dict:
    """Useful when you need to improve your code.""" 
    
    prompt_template = f"""
    I don't think this code is the best way to do it in Python, can you help me?

    The code will be enclosed in "" in the following text.
    {header}

    Please explain, in detail, what you did to improve it.
    """

    final_response = get_completion(prompt_template, "code_improve")
    return final_response

@tool(args_schema=SearchInput)
def generate_code_variations(header: str) -> dict:
    """Useful when you need to explore new ways of writing code and understand the differences.""" 
    
    prompt_template = f"""
    I don't think this code is the best way to do it in Python, can you help me?

    The code will be enclosed in "" in the following text.
    {header}

    Please explore multiple ways of solving the problem, explain each,
    and tell me which is the most Pythonic.
    """

    final_response = get_completion(prompt_template, "generate_code_variations")
    return final_response

@tool(args_schema=SearchInput)
def code_simplification(header: str) -> dict:
    """Useful when you need to simplify the code and understand how to do it.""" 
    
    prompt_template = f"""
    Can you please simplify this code in Python? \n
    You are an expert in Pythonic code.

    The code will be enclosed in "" in the following text.
    {header}

    Please comment each line in detail, \n
    and explain in detail what you did to modify it, and why.
    """

    final_response = get_completion(prompt_template, "code_simplification")
    return final_response

@tool(args_schema=SearchInput)
def generate_tests(header: str) -> dict:
    """Useful when you need to create tests.""" 
    
    prompt_template = f"""
    Can you please create good test cases for this Python code using pytest?

    The code will be enclosed in "" in the following text.
    {header}

    Explain in detail what these test cases are designed to achieve.
    Reply with the complete code and explanation.
    """

    final_response = get_completion(prompt_template, "generate_tests")
    return final_response

@tool(args_schema=SearchInput)
def optimize_code(header: str) -> dict:
    """Useful when you need to optimize your code.""" 
    
    prompt_template = f"""
    Can you please make this code more efficient?

    The code will be enclosed in "" in the following text.
    {header}

    Explain in detail what you changed and why.
    """

    final_response = get_completion(prompt_template, "optimize_code")
    return final_response

@tool(args_schema=SearchInput)
def debug_code(header: str) -> dict:
    """Useful when you need to debug your code.""" 
    
    prompt_template = f"""
    Can you please help me to debug this code?

    The code will be enclosed in "" in the following text.
    {header}

    Explain in detail what you found and why it was a bug.
    """

    final_response = get_completion(prompt_template, "debug_code")
    return final_response

@tool(args_schema=SearchInput)
def generate_documentation(header: str) -> dict:
    """Useful when you need to generate documentation about your code.""" 
    
    prompt_template = f"""
    Please write technical documentation for this code and \n
    make it easy for a non python developer to understand:

    The code will be enclosed in "" in the following text.
    {header}

    Output the results in markdown
    """

    final_response = get_completion(prompt_template, "generate_documentation")
    return final_response

def route(result):
    if isinstance(result, AgentFinish):
        return result.return_values['output']
    else:
        tools = {
            "code_improve": code_improve,
            "generate_code": generate_code,
            "code_variations": generate_code_variations,
            "code_simplification": code_simplification,
            "generate_tests": generate_tests,
            "optimize_code": optimize_code,
            "debug_code": debug_code,
            "generate_documentation": generate_documentation,
        }
        return tools[result.tool].run(result.tool_input)

def agent(task: str) -> dict:

    functions = [
    convert_to_openai_function(f) for f in [
        code_improve, generate_code, generate_code_variations, code_simplification, 
        generate_tests, optimize_code, debug_code, generate_documentation
        ]
    ]

    model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key = getenv('OPENAI_API_KEY')).bind(functions=functions)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a personal and very powerful Python assistant."),
        ("user", "{input}"),
    ])

    try:
        chain = prompt | model | OpenAIFunctionsAgentOutputParser() | route
        response = chain.invoke({"input": task})

        logging.info(f"The used Tool was {response['tool_name']}")
        logging.info("Answer generated.")
        logging.info(response.get("message"))

    except TypeError as e:
        response = {"message":"Error, try again later."}

        logging.error(response["message"])
        logging.error(e)
        return response

    except Exception as e:
        response = {"message":"Error, try again later."}
        
        logging.error(response["message"])
        logging.error(e)
        return response
    return response
