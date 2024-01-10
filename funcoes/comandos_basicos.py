import discord
from config.conector_discord import ConectorDiscord


class BasicCommands:
    def __init__(self, cliente_discord: ConectorDiscord):
        self.cliente_discord = cliente_discord

    async def status(self,interaction: discord.Interaction):
        await interaction.response.send_message(
            f'Meu Status é {self.cliente_discord.status}...', ephemeral=True
        )

    async def linkbot(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            'Link Enviado...', ephemeral=True
        )
        link = 'https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot'.format(
            interaction.client.user.id
        )

        embed = discord.Embed(
            title = "Link de Autorização do Bot", 
            description = "Clique no link abaixo para adicionar o bot ao seu servidor!",  
            color = discord.Color.blue()
        )

        embed.add_field(name="Link", value=link, inline=False)

        dm_channel = await interaction.user.create_dm()
        await dm_channel.send(embed=embed)


    async def comousar(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            'Enviando como usar...', ephemeral=True
        )
        dm_channel = await interaction.user.create_dm()
        with open('comomeusar.md', 'rb') as file:
            await dm_channel.send(file=discord.File(file, 'comousar.md'))

    def load_basic_commands(self, tree):
        tree.command(name='status', description='Envia o status do bot na dm')(self.status)
        tree.command(name='linkbot', description='Envia o link do bot na dm')(self.linkbot)
        tree.command(name='comousar', description='Envia instruções de como usar o bot')(self.comousar)
