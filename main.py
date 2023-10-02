# Importação da biblioteca discord
import discord

# Criação do cliente do Discord com as permissões necessárias
cliente_discord = discord.Client(intents=discord.Intents.all())

# ID do canal que o bot vai monitorar
canal_alvo_id = 1073372639877419139

# Evento chamado quando o cliente do Discord estiver pronto
@cliente_discord.event
async def on_ready():
    print('Logado como {0.user}'.format(cliente_discord))

# Evento chamado quando uma mensagem é recebida
@cliente_discord.event
async def on_message(mensagem):
    if mensagem.content.startswith('/status'):
        await mensagem.channel.send(
            'Estou funcionando perfeitamente! Meu status é {0}'.format(
                cliente_discord.status))

# Evento chamado quando é atendido o requisito 
@cliente_discord.event
async def on_message(mensagem):
    if mensagem.channel.id == canal_alvo_id:
        linhas = mensagem.content.split('\n')
        if len(linhas) == 4:
            for linha in linhas:
                if ': ' in linha:
                    emoji = linha.split(': ')[-1]
                    await mensagem.channel.send(f'O emoji é {emoji}')

# Inicialização do cliente do Discord com o token de autenticação
cliente_discord.run('MTA3OTQyNjc5MDY4NDExNDk1NA.GJRcML.Uen1zZ5Ljf7x_NBw69Ql8xbZWeArN7ZNlcPLzw')





























# # Importação da biblioteca discord
# import discord
# import re
# # Criação do cliente do Discord com as permissões necessárias
# cliente_discord = discord.Client(intents=discord.Intents.all())

# # ID do canal que o bot vai monitorar
# canal_alvo_id = 1073372639877419139

# # Evento chamado quando o cliente do Discord estiver pronto
# @cliente_discord.event
# async def on_ready():
#     print('Logado como {0.user}'.format(cliente_discord))

# # Evento chamado quando uma mensagem é recebida
# @cliente_discord.event
# async def on_message(mensagem):
#     if mensagem.content.startswith('/status'):
#         await mensagem.channel.send(
#             'Estou funcionando perfeitamente! Meu status é {0}'.format(
#                 cliente_discord.status))

#     if mensagem.channel.id == canal_alvo_id:
#         linhas = mensagem.content.split('\n')
#         if len(linhas) == 4:
#             prefixos = [
#                 '- **Hj estou**: ',
#                 '- **Ontem eu**: ',
#                 '- **Hj pretendo**: ',
#                 '- **Preciso de ajuda com**: '
#             ]
#             # Verificar se a estrutura completa é atendida
#             if all(linha.startswith(prefixo) for linha, prefixo in zip(linhas, prefixos)):
#                 await mensagem.channel.send('Esta mensagem segue o padrão!')
#                 # Encontrar e enviar emojis
#                 emojis = re.findall(r':\w+:', mensagem.content)
#                 if emojis:
#                     for em in emojis:
#                         await mensagem.channel.send(f'O emoji é {em}')
#             else:
#                 # Procurar somente por '- **Hj estou**: '
#                 for linha in linhas:
#                     if linha.startswith('- **Hj estou**: '):
#                         await mensagem.channel.send('Esta mensagem segue o padrão parcialmente.')


# # Inicialização do cliente do Discord com o token de autenticação
# cliente_discord.run('MTA3OTQyNjc5MDY4NDExNDk1NA.GJRcML.Uen1zZ5Ljf7x_NBw69Ql8xbZWeArN7ZNlcPLzw')
