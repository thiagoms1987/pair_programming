import time
import logging
from fastapi import FastAPI, Body, HTTPException, Request
from fastapi.responses import JSONResponse
from utils_tools import agent
from models import Input, Output, EXAMPLE_INPUT
import uvicorn

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

app = FastAPI()

@app.get("/healthz")
async def healthz():
    '''Healthz'''
    try:
        return {"status": "ok"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=err)

@app.post("/chat")
async def get_help(
        request: Input = Body(Input(), example=EXAMPLE_INPUT)
                ) -> Output or dict:
    """
    Help to create a code, improve, debug, create documentation or create tests from a code.

    Inputs:
        - query_str: string. Ex.: "debug: "def sum_two_numbers(x:float, y:float) -> float: return x+y".
    Returns:
        {"message":"The code is correct."}
    """
    message = request.message
    try:
        start = time.time()
        result = agent(message)
        end = time.time()
        execution_time = (end - start)

        return {
            "result": result["message"], "execution_time": execution_time
        }
        
    except Exception as err:
        logging.error(err)
        return {"result": "Failed", "error": "Try again latter."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
