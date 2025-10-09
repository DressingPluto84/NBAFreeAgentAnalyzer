from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class PlayerRequest(BaseModel):
    players: List[str]

@app.get("/")
def main():
    return "hello"

@app.get("/health")
def health():
    return "I am alive!!"

@app.post("/players")
def players(request: PlayerRequest):
    player_names = request.players
    print(player_names)

@app.get("/stats")
def stats():
    return ""