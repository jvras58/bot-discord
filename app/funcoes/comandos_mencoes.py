from datetime import datetime

import discord
from discord import app_commands

from app.config.config import get_settings


class MentionsCommands:
    """
    Classe que define os comandos relacionados a mensagens no canal.
    """

    def __init__(self, cliente):
        """
        Inicializa a classe CanalCommands.

        Args:
            cliente (objeto): O cliente Discord.
        """
        self.cliente_discord = cliente

    @app_commands.describe(horario='Horário do alerta: %H:%M')
    async def definir_alerta(
        self, interaction: discord.Interaction, horario: str
    ):
        """
        Verifica se o usuário está autorizado a usar o comando e, em seguida,
        Define um alerta para ser disparado em um determinado horário.
        Salva as alterações no cliente Discord.

        Args:
            interaction (discord.Interaction): A interação do usuário com o comando.
            horario (str): O horário do alerta no formato '%H:%M'.
        """
        authorization_ids = [
            int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')
        ]

        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message(
                'Você não está autorizado a usar este comando.', ephemeral=True
            )
            return

        horario = datetime.strptime(horario, '%H:%M').time()

        # Converta a hora e os minutos para uma string no formato 'HH:MM'
        horario_str = horario.strftime('%H:%M')

        # Salve a hora e os minutos como uma string
        self.cliente_discord.alerta_checkpoint_horario = horario_str
        self.cliente_discord.save()
        await interaction.response.send_message(
            f'Alerta definido para {self.cliente_discord.alerta_checkpoint_horario}.',
            ephemeral=True,
        )

    async def offeveryone(self, interaction: discord.Interaction):
        """
        Desativa o aviso de everyone no canal.

        Verifica se o usuário está autorizado a usar o comando e, em seguida,
        desativa o aviso de mensagem direta. Salva as alterações no cliente Discord.

        Args:
            interaction (discord.Interaction): A interação do usuário com o comando.
        """
        authorization_ids = [
            int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')
        ]

        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message(
                'Você não está autorizado a usar este comando.', ephemeral=True
            )
            return

        # Responda à interação primeiro
        await interaction.response.send_message(
            'Desativando menções a todos...', ephemeral=True
        )
        self.cliente_discord.enviar_everyone = False
        self.cliente_discord.save()

    async def oneveryone(self, interaction: discord.Interaction):
        """
        ativa o aviso de everyone no canal.

        Verifica se o usuário está autorizado a usar o comando e, em seguida,
        ativa o aviso de mensagem direta. Salva as alterações no cliente Discord.

        Args:
            interaction (discord.Interaction): A interação do usuário com o comando.
        """
        authorization_ids = [
            int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')
        ]

        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message(
                'Você não está autorizado a usar este comando.', ephemeral=True
            )
            return

        # Responda à interação primeiro
        await interaction.response.send_message(
            'Ativando menções a todos...', ephemeral=True
        )
        self.cliente_discord.enviar_everyone = True
        self.cliente_discord.save()

    def load_mentions_commands(self, tree):
        """
        Carrega os comandos relacionados a mensagens no canal no objeto tree.

        Args:
            tree: O objeto tree onde os comandos serão carregados.
        """
        tree.command(
            name='horario_alerta', description='Define o horário do alerta'
        )(self.definir_alerta)
        tree.command(
            name='offeveryone', description='Desativa menções a todos'
        )(self.offeveryone)
        tree.command(name='oneveryone', description='Ativa menções a todos')(
            self.oneveryone
        )
