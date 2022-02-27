import asyncio
import logging

from fastapi import FastAPI

from src import bot

logger = logging.getLogger(__name__)
app = FastAPI()

@app.on_event("startup")
async def startup_event():
  asyncio.create_task(bot.bot.start('token'))


@app.get("/")
async def read_root():
  return {"detail": "helloworld"}
