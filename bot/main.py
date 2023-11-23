import discord
import time
from funcoes.mensagens import on_ready as on_ready_mensagens, on_message as on_message_mensagens, envia_link_bot, processa_mensagem_canal_alvo
from funcoes.comandos import envia_dm, comousar, offeveryone, oneveryone, offavisodm, onavisodm, idignore, readicionarids, idcheckpoint, idplanilha
from config.conector_discord import ConectorDiscord
from config.config import get_settings
from funcoes.dados import dados,envia_planilha 
from funcoes.alertas import alerta_checkpoint,verificar_checkpoints_nao_enviados



cliente_discord = discord.Client(intents=discord.Intents.all())
conector_discord = ConectorDiscord()

@cliente_discord.event
async def on_ready():
    await on_ready_mensagens(cliente_discord, conector_discord, dados, alerta_checkpoint, verificar_checkpoints_nao_enviados)

@cliente_discord.event
async def on_message(mensagem):
    await on_message_mensagens(mensagem, cliente_discord, conector_discord, envia_link_bot, processa_mensagem_canal_alvo, envia_planilha, envia_dm, comousar, offeveryone, oneveryone, offavisodm, onavisodm, idignore, readicionarids, idcheckpoint, idplanilha)
while True:
    try:
        # Inicialização do cliente do Discord
        cliente_discord.run(get_settings().DISCORD_TOKEN)
    except Exception as e:
        print(f"Erro: {e}. Reiniciando o bot.")
        time.sleep(5)  # Pausa por 5s
