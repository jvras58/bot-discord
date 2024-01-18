import discord

from app.config.conector_discord import ConectorDiscord
from app.funcoes.comandos import create_image


class BasicCommands:
    """
    Classe que define os comandos básicos do bot.
    """

    def __init__(self, cliente_discord: ConectorDiscord):
        """
        Inicializa a classe CanalCommands.

        Args:
            cliente (objeto): O cliente Discord.
        """
        self.cliente_discord = cliente_discord

    async def status(self, interaction: discord.Interaction):
        """
        Envia o status do bot como resposta a uma interação.

        Args:
            interaction (discord.Interaction): A interação do usuário com o bot.
        """
        await interaction.response.send_message(
            f'Meu Status é {self.cliente_discord.status}...', ephemeral=True
        )

    async def linkbot(self, interaction: discord.Interaction):
        """
        Envia o link de convite do bot como resposta a uma interação.

        Args:
            interaction (discord.Interaction): A interação do usuário com o bot.
        """
        bot_user = interaction.client.user
        imagem_buffer = await create_image(bot_user)

        link = 'https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot'.format(
            bot_user.id
        )

        file = discord.File(imagem_buffer, filename='image.png')

        embed = discord.Embed(
            title='Adicione-me ao seu servidor!',
            description=f'Para adicionar-me ao seu servidor, clique [aqui]({link})',
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url='attachment://image.png')

        await interaction.response.send_message(
            embed=embed, file=file, ephemeral=True
        )

    async def comousar(self, interaction: discord.Interaction):
        """
        Envia as instruções de como usar o bot na DM do usuário.

        Args:
            interaction (discord.Interaction): A interação do usuário com o bot.
        """
        await interaction.response.send_message(
            'Enviando como usar...', ephemeral=True
        )
        dm_channel = await interaction.user.create_dm()
        with open('comomeusar.md', 'rb') as file:
            await dm_channel.send(file=discord.File(file, 'comousar.md'))

    def load_basic_commands(self, tree):
        """
        Carrega os comandos básicos no objeto tree.

        Args:
            tree: O objeto tree onde os comandos serão carregados.
        """
        tree.command(name='status', description='Envia o status do bot')(
            self.status
        )
        tree.command(name='linkbot', description='Envia o link do bot')(
            self.linkbot
        )
        tree.command(
            name='comousar',
            description='Envia instruções de como usar o bot na dm',
        )(self.comousar)