import discord
import emoji
import re
import pandas as pd
import asyncio
import datetime

cliente_discord = discord.Client(intents=discord.Intents.all())

canal_alvo_id = 1158343397279543327

# DataFrame para armazenar os dados captados
dados = pd.DataFrame(columns=['ID do Usuário', 'Nome do Usuário', 'Emoji', 'Data de Envio'])

def salvar_dados():
    # Exporta os dados para uma planilha Excel
    dados.to_excel('dados.xlsx', index=False)

#parte para testa se da pra ficar enviando mensagem para o usuarios lembrarem de enviar a mensagem do checkpoint do dia (a pedidos de tony)
async def alerta_checkpoint():
    await cliente_discord.wait_until_ready()
    canal = cliente_discord.get_channel(canal_alvo_id)
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        # ver como isso funciona de verdade pois acho dificil funcionar de primeira kk 
        if agora.hour == 10 and agora.minute == 0:  # Altere para o horário desejado
            await canal.send("@everyone Lembre-se de responder ao #checkpoint!")
            await asyncio.sleep(60)  # Espera um minuto para que o bot não envie várias mensagens
        else:
            await asyncio.sleep(1)  # Espera um segundo antes de verificar novamente

@cliente_discord.event
async def on_ready():
    print('Logado como {0.user}'.format(cliente_discord))

@cliente_discord.event
async def on_message(mensagem):
    # Verifica se a mensagem não foi enviada pelo próprio bot
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
                        # Obtém o identificador e o nome do usuário
                        id_usuario = mensagem.author.id
                        nome_usuario = mensagem.author.name
                        data_envio = mensagem.created_at  # Obtém a data de envio da mensagem
                        data_envio_sem_fuso_horario = data_envio.replace(tzinfo=None)  # Remove as informações de fuso horário
                        await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji: {emojis[0]}')
                        
                        # Adiciona os dados ao DataFrame
                        dados.loc[len(dados)] = [id_usuario, nome_usuario, emojis[0], data_envio_sem_fuso_horario]
                        
                        # Converte a coluna 'Data de Envio' para uma string
                        dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                        # Salva os dados na planilha
                        salvar_dados()

# Inicialização do cliente do Discord com o token de autenticação
cliente_discord.run('')
