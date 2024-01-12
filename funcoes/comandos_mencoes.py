from datetime import datetime

import discord
from discord import app_commands
from sqlalchemy.orm import Session
from database.session import engine
from database.bot_models import Bot

class MentionsCommands:
    def __init__(self, cliente):
        self.cliente_discord = cliente
        self.session = Session(bind=engine)
#TODO: ainda não ta salvando os dados provavelmente por causa do bot = self.session.query(Bot).first() averiguar
    @app_commands.describe(horario='Horário do alerta: %H:%M')
    async def definir_alerta(
        self, interaction: discord.Interaction, horario: str
    ):
        horario = datetime.strptime(horario, '%H:%M').time()
        self.cliente_discord.alerta_checkpoint_horario = horario

        # Atualize o horário do alerta no objeto Bot
        bot = self.session.query(Bot).first()
        if bot:
            bot.alerta_checkpoint_horario = horario

            # Salve a alteração no banco de dados
            self.session.commit()

        await interaction.response.send_message(
            f'Alerta definido para {self.cliente_discord.alerta_checkpoint_horario}.',
            ephemeral=True,
        )

    async def offeveryone(self, interaction: discord.Interaction):
        # Responda à interação primeiro
        await interaction.response.send_message(
            'Desativando menções a todos...', ephemeral=True
        )
        self.cliente_discord.enviar_everyone = False

    async def oneveryone(self, interaction: discord.Interaction):
        # Responda à interação primeiro
        await interaction.response.send_message(
            'Ativando menções a todos...', ephemeral=True
        )
        self.cliente_discord.enviar_everyone = True

    def load_mentions_commands(self, tree):
        tree.command(
            name='horario_alerta', description='Define o horário do alerta'
        )(self.definir_alerta)
        tree.command(
            name='offeveryone', description='Desativa menções a todos'
        )(self.offeveryone)
        tree.command(name='oneveryone', description='Ativa menções a todos')(
            self.oneveryone
        )
