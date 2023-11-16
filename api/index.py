from  fastapi import  FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"message": "Hello, World\n We are in love with code."}