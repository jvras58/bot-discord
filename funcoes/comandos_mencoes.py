from datetime import datetime

import discord
from discord import app_commands


class MentionsCommands:
    def __init__(self, cliente):
        self.cliente_discord = cliente

    #TODO: CONSEGUIMOS INSERIR HORARIO DENTRO DO BANCO PROVAVELMENTE TODOS OS OUTROS AINDA NÃO ESTÃO PEGANDO POR ISSO DEFINIR O CANAL DE CHECKPOINT É O HORARIO AINDA NÃO VAI FAZER O @EVERYONE FUNCIONAR TEMOS QUE FAZER O ALERTA CHECKPOINT PEGAR O NOVO FORMATO DE HORARIO DO BANCO É VERIFICAR TBMM
    @app_commands.describe(horario='Horário do alerta: %H:%M')
    async def definir_alerta(
        self, interaction: discord.Interaction, horario: str
    ):
        horario = datetime.strptime(horario, '%H:%M').time()
        
        # Crie um objeto datetime.datetime com a data atual
        datetime_obj = datetime.now()

        # Substitua a hora, minuto e segundo do objeto datetime.datetime
        datetime_obj = datetime_obj.replace(hour=horario.hour, minute=horario.minute, second=horario.second)

        self.cliente_discord.alerta_checkpoint_horario = datetime_obj
        self.cliente_discord.save()
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
