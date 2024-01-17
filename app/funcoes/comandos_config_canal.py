import discord
from config.config import get_settings
from discord import app_commands


class CanalCommands:
    def __init__(self, cliente):
        self.cliente_discord = cliente

    @app_commands.describe(canal='Canal de checkpoint')
    async def canalcheckpoint(
        self, interaction: discord.Interaction, canal: discord.TextChannel
    ):
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
        tree.command(
            name='canalcheckpoint',
            description='Define o ID do canal de checkpoint',
        )(self.canalcheckpoint)
        tree.command(
            name='canalplanilha',
            description='Define o ID do canal da planilha',
        )(self.canalplanilha)
