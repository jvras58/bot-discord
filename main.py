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


canal_alvo_id = 1158343397279543327  # chat teste 
canal_planilha_id = 1158543934021173258  # chat teste2 

# df para armazenar os dados pegos pelo bot
dados = pd.DataFrame(columns=['ID do Usuário', 'Nome do Usuário', 'Emoji', 'Data de Envio'])

def salvar_dados():
    """
    Função para salvar os dados em uma planilha Excel.
    """
    dados.to_excel('checkpoint.xlsx', index=False)

async def alerta_checkpoint():
    """
    Função assíncrona para enviar um alerta de checkpoint no canal alvo todos os dias às 10h.
    """
    await cliente_discord.wait_until_ready()
    canal = cliente_discord.get_channel(canal_alvo_id)
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        # teste para ver que horas são:
        # print(f"A hora atual é: {agora}")
        if agora.hour == 11 and agora.minute == 0:
            await canal.send("@everyone Lembre-se de responder ao #checkpoint!")
            await asyncio.sleep(60) # para ele não ficar spawnando a mensagem direto
        else:
            await asyncio.sleep(1)

@cliente_discord.event
async def on_ready():
    """
    Função para imprimir uma mensagem quando o bot estiver pronto.
    """
    print('Logado como {0.user}'.format(cliente_discord))
    # criar a tarefa pro bot ficar executando sempre o alert_checkpoint  
    cliente_discord.loop.create_task(alerta_checkpoint())

@cliente_discord.event
async def on_message(mensagem):
    """
    Função para lidar com mensagens recebidas.
    """
    if mensagem.author == cliente_discord.user:
        return
    
    if mensagem.content.startswith('/status'):
        await mensagem.channel.send(
            'Estou funcionando perfeitamente! Meu status é {0}'.format(
                cliente_discord.status))
        
    if mensagem.channel.id == canal_alvo_id:
        await processa_mensagem_canal_alvo(mensagem)
    elif mensagem.channel.id == canal_planilha_id and mensagem.content.strip() == '/checkpoint':
        await envia_planilha(mensagem)

async def processa_mensagem_canal_alvo(mensagem):
    """
    Função para processar mensagens recebidas no canal alvo.
    """
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
                    # print com a mensagem capturada para testes
                    await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji: {emojis[0]}')
                    
                    # O .loc é usado para acessar linhas e colunas por rótulo len(dados) retorna o número de linhas no DataFrame (então Adiciona uma nova linha ao DataFrame 'dados')
                    dados.loc[len(dados)] = [id_usuario, nome_usuario, emojis[0], data_envio_sem_fuso_horario]

                    # Converte a coluna 'Data de Envio' do DataFrame para string.
                    dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                    salvar_dados()

async def envia_planilha(mensagem):
    """
    Função para enviar a planilha quando o comando /checkpoint é recebido.
    """
    # Verifica se existe usando o os 
    if not os.path.exists('checkpoint.xlsx'):
        # se não existir avisa que não existe
        await mensagem.channel.send("Nenhum checkpoint identificado Por favor Gere um no Canal de #checkpoint! .")
    else:
        # se existir ele envia 
        # rb modo leitura / f arquivo aberto 
        with open('checkpoint.xlsx', 'rb') as f:
            await mensagem.channel.send("Aqui está o checkpoint de hoje:", file=discord.File(f, 'checkpoint.xlsx'))

while True:
    try:
        # Inicialização do cliente do Discord
        cliente_discord.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print(f"Erro encontrado: {e}. Reiniciando o bot.")
        time.sleep(5)  # Pausa por 5s



