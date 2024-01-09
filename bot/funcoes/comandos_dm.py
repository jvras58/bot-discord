from datetime import datetime


import discord
from config.conector_discord import ConectorDiscord



cliente_discord = ConectorDiscord()


async def alerta_dm_horario(interaction: discord.Interaction, horario: str):
    horario = datetime.strptime(horario, "%H:%M").time()
    cliente_discord.verificar_checkpoint_horario = horario
    await interaction.response.send_message(f'Alerta definido para {cliente_discord.verificar_checkpoint_horario}.')

# versão que envia na dm as respostas
'''
async def alerta_dm_horario(interaction: discord.Interaction, horario: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Horario do alerta no horário sendo definido...', ephemeral=True
    )
    horario = datetime.strptime(horario, "%H:%M").time()
    cliente_discord.verificar_checkpoint_horario = horario
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'Alerta definido para {cliente_discord.verificar_checkpoint_horario}.')
''' 

async def offavisodm(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Desativando aviso de mensagem direta...', ephemeral=True
    )
    cliente_discord.enviar_dm = False

# versão que envia na dm as respostas
'''
async def offavisodm(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Desativando aviso de mensagem direta...', ephemeral=True
    )
    cliente_discord.enviar_dm = False
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Desativado aviso de mensagem direta.')
'''

async def onavisodm(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Ativando aviso de mensagem direta...', ephemeral=True
    )
    cliente_discord.enviar_dm = True

# versão que envia na dm as respostas
'''
async def onavisodm(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Ativando aviso de mensagem direta...', ephemeral=True
    )
    cliente_discord.enviar_dm = True
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Ativado aviso de mensagem direta.')
'''

#TODO: NECESSARIO TESTAR
#TODO: discord.User é um objeto que representa um usuário do Discord então na vez de passar diretamente um parametro id eu posso passar um objeto discord.User
async def idignore(interaction: discord.Interaction, id: str):
    cliente_discord.ids_ignorados = int(id)
    await interaction.response.send_message(f'ID de usuário {cliente_discord.ids_ignorados} adicionado à lista de ignorados.')

# versão que envia na dm as respostas
'''
async def idignore(interaction: discord.Interaction, id: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Adicionando ID de usuário à lista de ignorados...', ephemeral=True
    )
    cliente_discord.ids_ignorados = int(id)
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'ID de usuário {cliente_discord.ids_ignorados} adicionado à lista de ignorados.')
'''

#TODO: NECESSARIO TESTAR
async def readicionarids(interaction: discord.Interaction, id: str):
    cliente_discord.ids_ignorados.remove(int(id))
    await interaction.response.send_message(f'ID de usuário {id} removido da lista de ignorados.')

# versão que envia na dm as respostas
'''
async def readicionarids(interaction: discord.Interaction, id: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Removendo ID de usuário da lista de ignorados...', ephemeral=True
    )
    cliente_discord.ids_ignorados.remove(int(id))
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'ID de usuário {id} removido da lista de ignorados.')
    
'''

async def dm(interaction: discord.Interaction, user: discord.User, *, mensagem: str):
    try:
        if user:
            dm_channel = await user.create_dm()
            await dm_channel.send(mensagem)
            await interaction.response.send_message(f'Mensagem enviada para o usuário {user.name}.')
        else:
            await interaction.response.send_message('Não foi possível encontrar o usuário mencionado.')
    except discord.errors.HTTPException:
        await interaction.response.send_message('Não foi possível enviar a mensagem para o usuário mencionado.')

def load_dm_commands(tree):
    tree.command(name='horario_verificar', description='Define o horário do verficar checkpoint')(alerta_dm_horario)
    tree.command(name='offavisodm', description='Desativa aviso de mensagem direta')(offavisodm)
    tree.command(name='onavisodm', description='Ativa aviso de mensagem direta')(onavisodm)
    #TODO: NECESSARIO TESTAR
    tree.command(name='idignore', description='Adiciona um ID de usuário à lista de ignorados')(idignore)
    #TODO: NECESSARIO TESTAR
    tree.command(name='readicionarids', description='Remove um ID de usuário da lista de ignorados')(readicionarids)
    tree.command(name='dm', description='Envia o dm pelo bot')(dm)
