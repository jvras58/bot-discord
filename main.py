import discord
import emoji
import pandas as pd
import asyncio
import datetime

# Inicializando o cliente do Discord com todas as intenções
cliente_discord = discord.Client(intents=discord.Intents.all())


canal_alvo_id = 1158343397279543327  # chat teste 
canal_planilha_id = 1158543934021173258  # chat teste2 

# DataFrame para armazenar os dados captados
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
        if agora.hour == 10 and agora.minute == 0:
            await canal.send("@everyone Lembre-se de responder ao #checkpoint!")
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(1)

@cliente_discord.event
async def on_ready():
    """
    Função para imprimir uma mensagem quando o bot estiver pronto.
    """
    print('Logado como {0.user}'.format(cliente_discord))

@cliente_discord.event
async def on_message(mensagem):
    """
    Função para lidar com mensagens recebidas.
    """
    if mensagem.author == cliente_discord.user:
        return

    if mensagem.channel.id == canal_alvo_id:
        linhas = mensagem.content.split('\n')
        if len(linhas) == 4:
            primeira_linha = linhas[0]
            if primeira_linha.startswith('- **Hj estou') or primeira_linha.startswith('Hj estou:') or primeira_linha.startswith('- Hj estou:'):
                partes = primeira_linha.split(':')
                if len(partes) > 1:
                    texto = partes[1].strip()
                    if texto.startswith('**'):
                        texto = texto[2:]
                    # Extrai todos os emojis da string usando a função emoji.emoji_count()
                    emojis = [char for char in texto if emoji.emoji_count(char)]
                    # Envia apenas o primeiro emoji encontrado
                    if emojis:
                        # Obtem o identificador e o nome do usuário
                        id_usuario = mensagem.author.id
                        nome_usuario = mensagem.author.name
                        data_envio = mensagem.created_at
                        data_envio_sem_fuso_horario = data_envio.replace(tzinfo=None)
                        await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji: {emojis[0]}')
                        
                        # Adiciona os dados ao DataFrame
                        dados.loc[len(dados)] = [id_usuario, nome_usuario, emojis[0], data_envio_sem_fuso_horario]
                        
                        # Converte a coluna 'Data de Envio' para uma string
                        dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                        salvar_dados()

    elif mensagem.channel.id == canal_planilha_id and mensagem.content.strip() == '/checkpoint':
        with open('checkpoint.xlsx', 'rb') as f:
            await mensagem.channel.send("Aqui esta o checkpoint de hoje:", file=discord.File(f, 'checkpoint.xlsx'))

# Inicialização do cliente do Discord com o token de autenticação
cliente_discord.run('')
