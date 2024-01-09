import discord
from config.conector_discord import ConectorDiscord

cliente_discord = ConectorDiscord()


async def canalcheckpoint(interaction: discord.Interaction, canal:discord.TextChannel):
    cliente_discord.canal_checkpoint_id = canal.id
    print(f"ID do canal enviado definido para {canal}.")
    print(f"ID do canal de checkpoint definido para {cliente_discord.canal_checkpoint_id}.")
    await interaction.response.send_message(f'ID do canal de checkpoint definido para {canal}.')


async def canalplanilha(interaction: discord.Interaction, canal:discord.TextChannel):
    cliente_discord.canal_planilha_id = canal.id
    await interaction.response.send_message(f'ID do canal da planilha definido para {canal}.')

def load_channel_commands(tree):
    tree.command(name='idcheckpoint', description='Define o ID do canal de checkpoint')(canalcheckpoint)
    tree.command(name='idplanilha', description='Define o ID do canal da planilha')(canalplanilha)
