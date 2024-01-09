from datetime import datetime



import discord
from config.conector_discord import ConectorDiscord



cliente_discord = ConectorDiscord()


async def definir_alerta(interaction: discord.Interaction, horario: str):
    horario = datetime.strptime(horario, "%H:%M").time()
    cliente_discord.alerta_checkpoint_horario = horario
    await interaction.response.send_message(f'Alerta definido para {cliente_discord.alerta_checkpoint_horario}.',ephemeral=True)

# versão que envia na dm as respostas
'''
async def definir_alerta(interaction: discord.Interaction, horario: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Definindo alerta...', ephemeral=True
    )
    horario = datetime.strptime(horario, "%H:%M").time()
    cliente_discord.alerta_checkpoint_horario = horario
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'Alerta definido para {cliente_discord.alerta_checkpoint_horario}.')
'''

async def offeveryone(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Desativando menções a todos...', ephemeral=True
    )
    cliente_discord.enviar_everyone = False

# versão que envia na dm as respostas
'''
async def offeveryone(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Desativando menções a todos...', ephemeral=True
    )
    cliente_discord.enviar_everyone = False
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Desativado menções a todos.')
'''

async def oneveryone(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Ativando menções a todos...', ephemeral=True
    )
    cliente_discord.enviar_everyone = True

# versão que envia na dm as respostas
'''
async def oneveryone(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Ativando menções a todos...', ephemeral=True
    )
    cliente_discord.enviar_everyone = True
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Ativado menções a todos.')
'''
