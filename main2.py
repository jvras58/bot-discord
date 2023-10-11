import discord
import emoji
import pandas as pd
import asyncio
import datetime
import os
import time
from dotenv import load_dotenv

load_dotenv()

cliente_discord = discord.Client(intents=discord.Intents.all())

canal_checkpoint_id = None
canal_planilha_id = None


dados = pd.DataFrame(columns=['ID do Usuário', 'Nome do Usuário', 'Emoji', 'Data de Envio'])

def salvar_dados():
    dados.to_excel('checkpoint.xlsx', index=False)

async def enviar_everyone_message(canal):
    if enviar_everyone:
        await canal.send("@everyone Lembre-se de responder ao #checkpoint!")

async def alerta_checkpoint():
    global enviar_everyone 

    await cliente_discord.wait_until_ready()
    canal = cliente_discord.get_channel(canal_checkpoint_id)
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        if agora.weekday() < 5 and agora.hour == 10 and agora.minute == 0:
            enviar_everyone_message(canal)
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(1)

async def verificar_checkpoints_nao_enviados():
    global enviar_dm, ids_ignorados
    await cliente_discord.wait_until_ready()
    canal_alvo = cliente_discord.get_channel(canal_checkpoint_id)
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        if  agora.weekday() < 5 and agora.hour == 12 and agora.minute == 0:
            usuarios_enviaram = dados['ID do Usuário'].tolist()
            membros = canal_alvo.guild.members
            for membro in membros:
                if membro.id not in usuarios_enviaram and membro.id not in ids_ignorados:
                    if enviar_dm:
                        await membro.send("Você não enviou o checkpoint hoje! Por favor, envie o checkpoint.")
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(1)

@cliente_discord.event
async def on_ready():
    print('Logado como {0.user}'.format(cliente_discord))
    cliente_discord.loop.create_task(alerta_checkpoint())
    cliente_discord.loop.create_task(verificar_checkpoints_nao_enviados())

@cliente_discord.event
async def on_message(mensagem):
    global enviar_everyone, enviar_dm, ids_ignorados, canal_checkpoint_id, canal_planilha_id

    if mensagem.author == cliente_discord.user:
        return

    if isinstance(mensagem.channel, discord.DMChannel):
        await process_dm_commands(mensagem)
        return

    await process_channel_commands(mensagem)

async def process_dm_commands(mensagem):
    global enviar_everyone, enviar_dm, ids_ignorados, canal_checkpoint_id, canal_planilha_id

    if mensagem.content.startswith('/linkbot'):
        await envia_link_bot(mensagem)
    elif mensagem.content.startswith('/status'):
        await mensagem.channel.send('Estou funcionando perfeitamente! Meu status é {0}'.format(cliente_discord.status))

async def process_channel_commands(mensagem):
    global enviar_everyone, enviar_dm, ids_ignorados, canal_checkpoint_id, canal_planilha_id

    if mensagem.content.startswith('/offeveryone'):
        enviar_everyone = False
        await mensagem.channel.send("O envio de mensagens @everyone foi desativado.")
    elif mensagem.content.startswith('/oneveryone'):
        enviar_everyone = True
        await mensagem.channel.send("O envio de mensagens @everyone foi reativado.")
    elif mensagem.content.startswith('/offavisodm'):
        enviar_dm = False
        await mensagem.channel.send("O envio de avisos por DM foi desativado.")
    elif mensagem.content.startswith('/onavisodm'):
        enviar_dm = True
        await mensagem.channel.send("O envio de avisos por DM foi reativado.")
    elif mensagem.content.startswith('/idignore'):
        await process_id_ignore_command(mensagem)
    elif mensagem.content.startswith('/readicionarids'):
        await process_readicionar_ids_command(mensagem)
    elif mensagem.content.startswith('/idcheckpoint'):
        await process_id_checkpoint_command(mensagem)
    elif mensagem.content.startswith('/idplanilha'):
        await process_id_planilha_command(mensagem)
    elif mensagem.content.startswith('/linkbot'):
        await envia_link_bot(mensagem)
    elif mensagem.content.startswith('/status'):
        await mensagem.channel.send('Estou funcionando perfeitamente! Meu status é {0}'.format(cliente_discord.status))
    elif mensagem.channel.id == canal_checkpoint_id:
        await processa_mensagem_canal_alvo(mensagem)
    elif mensagem.channel.id == canal_planilha_id and mensagem.content.strip() == '/checkpoint':
        await envia_planilha(mensagem)

async def process_id_ignore_command(mensagem):
    global ids_ignorados
    ids_para_ignorar = mensagem.content.split()[1:]
    if ids_para_ignorar:
        ids_ignorados.extend(ids_para_ignorar)
        await mensagem.channel.send(f"Os seguintes IDs foram adicionados à lista de ignorados: {', '.join(ids_para_ignorar)}")
    else:
        await mensagem.channel.send("Por favor, forneça pelo menos um ID para ignorar. Exemplo: /idignore 11111111111111111")

async def process_readicionar_ids_command(mensagem):
    global ids_ignorados
    ids_para_readicionar = mensagem.content.split()[1:]
    if ids_para_readicionar:
        ids_ignorados = [id for id in ids_ignorados if id not in ids_para_readicionar]
        await mensagem.channel.send(f"Os seguintes IDs foram removidos da lista de ignorados: {', '.join(ids_para_readicionar)}")
    else:
        await mensagem.channel.send("Por favor, forneça pelo menos um ID para readicionar. Exemplo: /readicionarids 11111111111111111")

async def process_id_checkpoint_command(mensagem):
    global canal_checkpoint_id
    id_canal_checkpoint = mensagem.content.split()[1:]
    if id_canal_checkpoint:
        canal_checkpoint_id = int(id_canal_checkpoint[0])
        await mensagem.channel.send(f"O ID do canal de checkpoint foi definido como: {canal_checkpoint_id}")
    else:
        await mensagem.channel.send("Por favor, forneça um ID para o canal de checkpoint. Exemplo: /idcheckpoint 1158343397279543327")

async def process_id_planilha_command(mensagem):
    global canal_planilha_id
    id_canal_planilha = mensagem.content.split()[1:]
    if id_canal_planilha:
        canal_planilha_id = int(id_canal_planilha[0])
        await mensagem.channel.send(f"O ID do canal da planilha foi definido como: {canal_planilha_id}")
    else:
        await mensagem.channel.send("Por favor, forneça um ID para o canal da planilha. Exemplo: /idplanilha 1158543934021173258")



async def envia_link_bot(mensagem):
    link = f"https://discord.com/api/oauth2/authorize?client_id={cliente_discord.user.id}&permissions=0&scope=bot"
    await mensagem.channel.send(f"Aqui me adicione no seu servidor chefinho prometo ser uma boa menine: {link}")

async def processa_mensagem_canal_alvo(mensagem):
    linhas = mensagem.content.split('\n')
    if len(linhas) == 4:
        primeira_linha = linhas[0]
        if primeira_linha.startswith('- **Hj estou') or primeira_linha.startswith('Hj estou:') or primeira_linha.startswith('- Hj estou:'):
            partes = primeira_linha.split(':')
            if len(partes) > 1:
                texto = partes[1].strip()
                if texto.startswith('**'):
                    texto = texto[2:]
                emojis = [char for char in texto if emoji.emoji_count(char)]
                if emojis:
                    id_usuario = mensagem.author.id
                    nome_usuario = mensagem.author.name
                    data_envio = mensagem.created_at
                    data_envio_sem_fuso_horario = data_envio.replace(tzinfo=None)
                    await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji: {emojis[0]}')
                    dados.loc[len(dados)] = [id_usuario, nome_usuario, emojis[0], data_envio_sem_fuso_horario]
                    dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                    salvar_dados()

async def envia_planilha(mensagem):
    if not os.path.exists('checkpoint.xlsx'):
        await mensagem.channel.send("Nenhum checkpoint identificado. Por favor, gere um no canal de #checkpoint!")
    else:
        with open('checkpoint.xlsx', 'rb') as f:
            await mensagem.channel.send("Aqui está o checkpoint de hoje:", file=discord.File(f, 'checkpoint.xlsx'))
        os.remove('checkpoint.xlsx')

while True:
    try:
        cliente_discord.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print(f"Erro: {e}. Reiniciando o bot.")
        time.sleep(5)
