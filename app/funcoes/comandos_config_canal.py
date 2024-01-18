import discord
from discord import app_commands

from app.config.config import get_settings


class CanalCommands:
    """
    Classe responsável por definir os comandos relacionados à configuração de canais.
    """

    def __init__(self, cliente):
        """
        Inicializa a classe CanalCommands.

        Args:
            cliente (objeto): O cliente Discord.
        """
        self.cliente_discord = cliente

    @app_commands.describe(canal='Canal de checkpoint')
    async def canalcheckpoint(
        self, interaction: discord.Interaction, canal: discord.TextChannel
    ):
        """
        Define o ID do canal de checkpoint.

        Args:
            interaction (objeto): A interação do Discord.
            canal (objeto): O canal de checkpoint.
        """
        authorization_ids = [
            int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')
        ]

        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message(
                'Você não está autorizado a usar este comando.', ephemeral=True
            )
            return

        self.cliente_discord.canal_checkpoint_id = canal.id
        self.cliente_discord.save()
        await interaction.response.send_message(
            f'ID do canal de checkpoint definido para {canal}.', ephemeral=True
        )

    @app_commands.describe(canal='Canal de checkpoint')
    async def canalplanilha(
        self, interaction: discord.Interaction, canal: discord.TextChannel
    ):
        """
        Define o ID do canal da planilha.

        Args:
            interaction (objeto): A interação do Discord.
            canal (objeto): O canal da planilha.
        """
        authorization_ids = [
            int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')
        ]

        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message(
                'Você não está autorizado a usar este comando.', ephemeral=True
            )
            return

        self.cliente_discord.canal_planilha_id = canal.id
        self.cliente_discord.save()
        await interaction.response.send_message(
            f'ID do canal da planilha definido para {canal}.', ephemeral=True
        )

    def load_channel_commands(self, tree):
        """
        Carrega os comandos de canal.

        Args:
            tree (objeto): A árvore de comandos.
        """
        tree.command(
            name='canalcheckpoint',
            description='Define o ID do canal de checkpoint',
        )(self.canalcheckpoint)
        tree.command(
            name='canalplanilha',
            description='Define o ID do canal da planilha',
        )(self.canalplanilha)
