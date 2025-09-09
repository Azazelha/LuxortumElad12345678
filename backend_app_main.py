from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Backend is running. Integrate your Python/ML/LLM code here."}