import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import Chatbot

'''
This file defines a sample API created using FastAPI and hosted locally via uvicorn.
Pydantic is used to define a datamodel to which requests have to adhere to.
'''


class ChatbotRequest(BaseModel):
    request: str


app = FastAPI()
chatbot = Chatbot()


@app.get("/")
async def read_root():
    return {'message': 'No arguments provided!'}


@app.post('/prompt')
async def get_inference(req: ChatbotRequest):
    response = chatbot.query_engine(req.request)
    if len(response.source_nodes) > 0:
        metadata_keys = response.metadata.keys()
        next_key = next(iter(metadata_keys))
        return {'response': response.response, 'file': response.metadata[next_key]['file_name'],
                'page': response.metadata[next_key]['page_label']}
    else:
        return {'response': response}


if __name__ == "__main__":
    uvicorn.run('api:app', host='127.0.0.1', port=8000, reload=True)
