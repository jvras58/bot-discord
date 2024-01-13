import discord
from discord import app_commands


class CanalCommands:
    def __init__(self, cliente):
        self.cliente_discord = cliente

    @app_commands.describe(canal='Canal de checkpoint')
    async def canalcheckpoint(
        self, interaction: discord.Interaction, canal: discord.TextChannel
    ):
        self.cliente_discord.canal_checkpoint_id = canal.id
        self.cliente_discord.save()
        # print(f"ID do canal enviado definido para {canal}.")
        # print(f"ID do canal de checkpoint definido para {self.cliente_discord.canal_checkpoint_id}.")
        await interaction.response.send_message(
            f'ID do canal de checkpoint definido para {canal}.'
        )

    @app_commands.describe(canal='Canal de checkpoint')
    async def canalplanilha(
        self, interaction: discord.Interaction, canal: discord.TextChannel
    ):
        self.cliente_discord.canal_planilha_id = canal.id
        self.cliente_discord.save()
        await interaction.response.send_message(
            f'ID do canal da planilha definido para {canal}.'
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
