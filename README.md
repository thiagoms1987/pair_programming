# Route Chain Pair Programming

## Introduction

This repository contains an API based on FastAPI and a web interface using Streamlit to interact with a router chain with prompts designed to act like a pair programmer.

### Libs

* OpenAI
* LangChain
* FastAPI
* Streamlit

### Reference
* (https://learn.deeplearning.ai/pair-programming-llm/lesson/5/technical-debt)
* (https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683)

### Requirements

* You need a OpenAI account. If you don't already have one, you can sign up at [https://chat.openai.com/auth/login]
* You need to add your `OPENAI_API_KEY` to the `.env` file to connect to the OpenAI API.

### Running locally

```bash
# clone this repo
git clone git@github.com:thiagoms1987/pair-programming.git
```

```
# Build and run docker image:

$docker build -t pair-programming .

$docker run -p 8000:8000 pair-programming -e OPENAI_API_KEY=my-key
```

## Documentation and testing API

```
http://127.0.0.1:8000/docs
```
```json
{
  "message": "message"
}
```
