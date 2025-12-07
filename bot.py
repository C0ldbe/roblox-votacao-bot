import os
import discord
from discord.ext import commands
from fastapi import FastAPI
import uvicorn
import threading

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

votos = {
    "Opção 1": 0,
    "Opção 2": 0,
    "Opção 3": 0
}

message_id = None

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
app = FastAPI()


@app.post("/vote")
async def receive_vote(data: dict):
    global votos

    opcao = data.get("opcao")
    player = data.get("player")

    if opcao in votos:
        votos[opcao] += 1
        await atualizar_mensagem()

    return {"status": "ok"}


async def atualizar_mensagem():
    global message_id

    channel = bot.get_channel(CHANNEL_ID)
    msg = await channel.fetch_message(message_id)

    texto = (
        f"🟥 **Opção 1:** {votos['Opção 1']}\n"
        f"🟦 **Opção 2:** {votos['Opção 2']}\n"
        f"🟩 **Opção 3:** {votos['Opção 3']}"
    )

    embed = discord.Embed(
        title="📊 Votação em andamento",
        description=texto,
        color=0x2ECC71
    )

    await msg.edit(embed=embed)


@bot.event
async def on_ready():
    global message_id

    print(f"BOT ONLINE: {bot.user}")

    channel = bot.get_channel(CHANNEL_ID)

    embed = discord.Embed(
        title="📊 Votação em andamento",
        description="🟥 Opção 1: 0\n🟦 Opção 2: 0\n🟩 Opção 3: 0",
        color=0x2ECC71
    )

    msg = await channel.send(embed=embed)
    message_id = msg.id

    print("Mensagem inicial criada:", message_id)


def start_fastapi():
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)


threading.Thread(target=start_fastapi).start()


bot.run(TOKEN)
