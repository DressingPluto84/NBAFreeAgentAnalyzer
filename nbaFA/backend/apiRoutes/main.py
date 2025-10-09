from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return "hello"

@app.get("/health")
def health():
    return "I am alive!!"

@app.post("/players")
def players(plays: str):
    pass

@app.get("/stats")
def stats():
    return stats