import discord
from config.conector_discord import ConectorDiscord

cliente_discord = ConectorDiscord()


async def status(interaction: discord.Interaction):
    await interaction.response.send_message(
        f'Meu Status é {cliente_discord.status}...', ephemeral=True
    )

async def linkbot(interaction: discord.Interaction):
    await interaction.response.send_message(
        'Enviando link do bot...', ephemeral=True
    )
    link = 'https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot'.format(
        interaction.client.user.id
    )
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(link)

async def comousar(interaction: discord.Interaction):
    await interaction.response.send_message(
        'Enviando como usar...', ephemeral=True
    )
    dm_channel = await interaction.user.create_dm()
    with open('comomeusar.md', 'rb') as file:
        await dm_channel.send(file=discord.File(file, 'comousar.md'))

def load_basic_commands(tree):
    tree.command(name='status', description='Envia o status do bot na dm')(status)
    tree.command(name='linkbot', description='Envia o link do bot na dm')(linkbot)
    tree.command(name='comousar', description='Envia instruções de como usar o bot')(comousar)
