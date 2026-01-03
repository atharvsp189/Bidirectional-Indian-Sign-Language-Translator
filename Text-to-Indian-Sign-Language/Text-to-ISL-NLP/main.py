import os
import json
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from googletrans import Translator


from payload import InputText
from code import take_input, clear_all
from  isl_nlp import get_isl_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins    = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

logging.info("Server Started - Text to Indian Sign Langauge NLP")

@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To Server' : f'{name}'}

@app.post('/api')
def get_final_response(data:InputText):
    logging.info("INPUT TEXT : ", InputText)
    text = data_dict = data.dict(by_alias=True)
    
    final_response = take_input(text['text'])
    clear_all()
    return {
        'final_response': final_response
    }


@app.post('/isl-text')
def get_isl(data: InputText):

    text = data_dict = data.dict(by_alias=True)
    logging.info("Translating to English Text to ISL")
    final_response = get_isl_text(text['text'])
    return {
        'final_response': final_response
    }

@app.post('/translate')
def get_isl(data: InputText):
    translator = Translator()
    translation = translator.translate(InputText, src='hi', dest='en')
    text = data_dict = data.dict(by_alias=True)
    print(data)
    final_response = get_isl_text(text['text'])
    return {
        'final_response': final_response
    }


@app.get('/Hindi')
def translate_to_hindi(hindi_text:str):
    logging.info("Translating Hindi to English")
    logging.info(f"Original Text (Hindi): {hindi_text}")

    translator = Translator()
    translation = translator.translate(hindi_text, src='hi', dest='en')
    # Display the translated text
    logging.info(f"Translated Text (English): {translation.text}")

    return {
        "translate" : translation.text
    }

@app.get('/ToMarathi/{marathi_text}')
def translate_to_marathi(marathi_text:str):
    logging.info("Translating Marathi to English")
    logging.info(f"Original Text (Hindi): {marathi_text}")
    print("Inside Marath")

    translator = Translator()
    translation = translator.translate(marathi_text, src='mr', dest='en')

    print(f"Original Text (Marath): {marathi_text}")
    print(f"Translated Text (English): {translation.text}")
    
    return translation


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=3002)