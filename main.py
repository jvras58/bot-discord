import discord
import emoji
import re
import pandas as pd

cliente_discord = discord.Client(intents=discord.Intents.all())

canal_alvo_id = 1158343397279543327

# Dicionário para armazenar as mensagens respondidas
mensagens_respondidas = {}

# DataFrame para armazenar os dados captados
dados = pd.DataFrame(columns=['ID do Usuário', 'Nome do Usuário', 'Emoji'])

@cliente_discord.event
async def on_ready():
    print('Logado como {0.user}'.format(cliente_discord))

@cliente_discord.event
async def on_message(mensagem):
    # Verifica se a mensagem não foi enviada pelo próprio bot
    if mensagem.author == cliente_discord.user:
        return

    # Verifica se o bot já respondeu a esta mensagem
    if mensagem.id in mensagens_respondidas:
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
                        await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji: {emojis[0]}')
                        # Adiciona a mensagem ao dicionário de mensagens respondidas
                        mensagens_respondidas[mensagem.id] = True
                        
                        # Adiciona os dados ao DataFrame
                        dados.loc[len(dados)] = [id_usuario, nome_usuario, emojis[0]]
                        
                        # Exporta os dados para uma planilha Excel
                        dados.to_excel('dados.xlsx', index=False)
                        
                        return

# Inicialização do cliente do Discord com o token de autenticação
cliente_discord.run('MTA3OTQyNjc5MDY4NDExNDk1NA.GhltlG.76_4XQfLHI8JO2T8wNoL5rLQj-Qi3gGQSfWHPc')
