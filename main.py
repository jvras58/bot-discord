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

canal_alvo_id = int(os.getenv('CANAL_ALVOCHECKPOINT_ID'))
canal_planilha_id = int(os.getenv('CANAL_PLANILHA_ID'))

# df para armazenar os dados pegos pelo bot
dados = pd.DataFrame(columns=['ID do Usuário', 'Nome do Usuário', 'Emoji', 'Data de Envio'])

def salvar_dados():
    """
    Função para salvar os dados em uma planilha Excel.
    """
    dados.to_excel('checkpoint.xlsx', index=False)

enviar_everyone = True
async def alerta_checkpoint():
    """
    Função assíncrona para enviar um alerta de checkpoint no canal alvo de segunda a sexta-feira às 10h.
    """
    global enviar_everyone 

    await cliente_discord.wait_until_ready()
    canal = cliente_discord.get_channel(canal_alvo_id)
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        # so dias de seg a sexta
        if agora.weekday() < 5 and agora.hour == 10 and agora.minute == 0:
            if enviar_everyone:  # Verifica se enviar_everyone é True antes de enviar a mensagem
                await canal.send("@everyone Lembre-se de responder ao #checkpoint!")
            await asyncio.sleep(60) # para ele não ficar spawnando a mensagem direto
        else:
            await asyncio.sleep(1)
            
async def verificar_checkpoints_nao_enviados():
    """
    Função assíncrona para verificar quem não enviou o checkpoint do dia e enviar uma mensagem privada (DM).
    """
    await cliente_discord.wait_until_ready()
    canal_alvo = cliente_discord.get_channel(canal_alvo_id)
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        if  agora.weekday() < 5 and agora.hour == 12 and agora.minute == 0:
            # Lista de usuários que já enviaram o checkpoint
            usuarios_enviaram = dados['ID do Usuário'].tolist()
            # Lista de membros do servidor
            membros = canal_alvo.guild.members
            for membro in membros:
                if membro.id not in usuarios_enviaram:
                    # Envia mensagem privada para usuários que não enviaram o checkpoint
                    await membro.send("Você não enviou o checkpoint hoje! Por favor, envie o checkpoint.")
            await asyncio.sleep(60)  # para evitar mensagens repetidas
        else:
            await asyncio.sleep(1)
            
@cliente_discord.event
async def on_ready():
    """
    Função para imprimir uma mensagem quando o bot estiver pronto.
    """
    print('Logado como {0.user}'.format(cliente_discord))
    # criar a tarefa pro bot ficar executando: 
    cliente_discord.loop.create_task(alerta_checkpoint())
    cliente_discord.loop.create_task(verificar_checkpoints_nao_enviados())



@cliente_discord.event
async def on_message(mensagem):
    """
    Função para lidar com mensagens recebidas.
    """
    global enviar_everyone 
    if mensagem.author == cliente_discord.user:
        return
    
    if mensagem.content.startswith('/offeveryone'):
        # Altere o valor de enviar_everyone para False quando o comando /offeveryone for recebido
        enviar_everyone = False
        await mensagem.channel.send("O envio de mensagens @everyone foi desativado.")
        
    elif mensagem.content.startswith('/oneveryone'):
        # Altere o valor de enviar_everyone para True quando o comando /oneveryone for recebido
        enviar_everyone = True
        await mensagem.channel.send("O envio de mensagens @everyone foi reativado.")
    
    if mensagem.content.startswith('/linkbot'):
        await envia_link_bot(mensagem)

    if mensagem.content.startswith('/status'):
        await mensagem.channel.send(
            'Estou funcionando perfeitamente! Meu status é {0}'.format(
                cliente_discord.status))
        
    if mensagem.channel.id == canal_alvo_id:
        await processa_mensagem_canal_alvo(mensagem)
    elif mensagem.channel.id == canal_planilha_id and mensagem.content.strip() == '/checkpoint':
        await envia_planilha(mensagem)


async def envia_link_bot(mensagem):
    """
    Função para enviar o link do bot quando o comando /linkbot é recebido.
    """
    link = f"https://discord.com/api/oauth2/authorize?client_id={cliente_discord.user.id}&permissions=0&scope=bot"
    await mensagem.channel.send(f"Aqui está o link: {link}")


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
                    # await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji: {emojis[0]}')
                    
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
        # apaga do arquivo local depois de enviado para não encher 
        os.remove('checkpoint.xlsx')
        
while True:
    try:
        # Inicialização do cliente do Discord
        cliente_discord.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print(f"Erro: {e}. Reiniciando o bot.")
        time.sleep(5)  # Pausa por 5s



