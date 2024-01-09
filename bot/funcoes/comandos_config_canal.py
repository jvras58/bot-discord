import discord
from config.conector_discord import ConectorDiscord

cliente_discord = ConectorDiscord()


async def idcheckpoint(interaction: discord.Interaction, canal:discord.TextChannel):
    cliente_discord.canal_checkpoint_id = canal.id
    print(f"ID do canal enviado definido para {canal}.")
    print(f"ID do canal de checkpoint definido para {cliente_discord.canal_checkpoint_id}.")
    await interaction.response.send_message(f'ID do canal de checkpoint definido para {canal}.')


async def idplanilha(interaction: discord.Interaction, canal:discord.TextChannel):
    cliente_discord.canal_planilha_id = canal.id
    await interaction.response.send_message(f'ID do canal da planilha definido para {canal}.')
