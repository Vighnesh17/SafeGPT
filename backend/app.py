from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from .SafeGPT import SafeGPTProcessor

app = FastAPI()

# Set up static files and templates
templates = Jinja2Templates(directory='frontend/templates')
app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

# Initialize the SafeGPT processor with your OpenAI API key
api_key = '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'
processor = SafeGPTProcessor(api_key)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat")
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/privacy")
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@app.post("/api/process_prompt")
async def process_prompt(request: PromptRequest):
    try:
        response = processor.process_prompt(request.prompt)
        return {"response": response}
    except Exception as e:
        print(f"Error in process_prompt: {str(e)}")  # Add this line
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
