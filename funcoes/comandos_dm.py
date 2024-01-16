from datetime import datetime

import discord
from discord import app_commands
import json
from datetime import datetime, date
from config.config import get_settings

class DmCommands:
    def __init__(self, cliente):
        self.cliente_discord = cliente

    @app_commands.describe(horario='Horário do alerta: %H:%M')
    async def alerta_dm_horario(
        self, interaction: discord.Interaction, horario: str
    ):
        authorization_ids = [int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')]
        
        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message('Você não está autorizado a usar este comando.', ephemeral=True)
            return
        
        horario = datetime.strptime(horario, '%H:%M').time()
        
        # Converta o objeto time para datetime
        horario_datetime = datetime.combine(date.today(), horario)
        
        # Salve apenas a hora e os minutos
        self.cliente_discord.verificar_checkpoint_horario = horario_datetime
        self.cliente_discord.save()
        await interaction.response.send_message(
            f'Alerta definido para {self.cliente_discord.verificar_checkpoint_horario.hour}:{self.cliente_discord.verificar_checkpoint_horario.minute}.',
            ephemeral=True,
        )

    async def offavisodm(self, interaction: discord.Interaction):
        authorization_ids = [int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')]
        
        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message('Você não está autorizado a usar este comando.', ephemeral=True)
            return
            
        await interaction.response.send_message(
            'Desativando aviso de mensagem direta...', ephemeral=True
        )
        self.cliente_discord.enviar_dm = False
        self.cliente_discord.save()

    async def onavisodm(self, interaction: discord.Interaction):
        authorization_ids = [int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')]
        
        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message('Você não está autorizado a usar este comando.', ephemeral=True)
            return
            
        await interaction.response.send_message(
            'Ativando aviso de mensagem direta...', ephemeral=True
        )
        self.cliente_discord.enviar_dm = True
        self.cliente_discord.save()

    # TODO: discord.User é um objeto que representa um usuário do Discord então na vez de passar diretamente um parametro id eu posso passar um objeto discord.User
    @app_commands.describe(id='identificador do usuário a ser ignorado')
    async def idignore(self, interaction: discord.Interaction, id: str):
        authorization_ids = [int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')]
        
        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message('Você não está autorizado a usar este comando.', ephemeral=True)
            return
        
        if isinstance(self.cliente_discord.ids_ignorados, str):
            self.cliente_discord.ids_ignorados = json.loads(self.cliente_discord.ids_ignorados)  # Converte a string JSON de volta em uma lista
        self.cliente_discord.ids_ignorados.append(int(id))
        self.cliente_discord.save()
        ids_ignorados_json = json.dumps(self.cliente_discord.ids_ignorados)
        await interaction.response.send_message(
            f'ID de usuário {id} adicionado à lista de ignorados. Lista atual: {ids_ignorados_json}', ephemeral=True
        )

    @app_commands.describe(id='identificador do usuário a ser ree-adicionado')
    async def readicionarids(self, interaction: discord.Interaction, id: str):
        authorization_ids = [int(id) for id in get_settings().AUTHORIZATION_IDS.split(',')]
        
        if interaction.user.id not in authorization_ids:
            await interaction.response.send_message('Você não está autorizado a usar este comando.', ephemeral=True)
            return
        
        self.cliente_discord.ids_ignorados.remove(int(id))  # Remove o ID da lista
        self.cliente_discord.save()
        ids_ignorados_json = json.dumps(self.cliente_discord.ids_ignorados)  # Converte a lista em JSON
        await interaction.response.send_message(
            f'ID de usuário {id} removido da lista de ignorados. Lista atual: {ids_ignorados_json}', ephemeral=True
        )

    @app_commands.describe(
        user='usuario a ser enviado a mensagem',
        mensagem='mensagem a ser enviada',
    )
    async def dm(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        *,
        mensagem: str,
    ):
        try:
            if user:
                dm_channel = await user.create_dm()
                await dm_channel.send(mensagem)
                await interaction.response.send_message(
                    f'Mensagem enviada para o usuário {user.name}.'
                )
            else:
                await interaction.response.send_message(
                    'Não foi possível encontrar o usuário mencionado.'
                )
        except discord.errors.HTTPException:
            await interaction.response.send_message(
                'Não foi possível enviar a mensagem para o usuário mencionado.'
            )

    def load_dm_commands(self, tree):
        tree.command(
            name='horario_verificar',
            description='Define o horário do verficar checkpoint',
        )(self.alerta_dm_horario)
        tree.command(
            name='offavisodm', description='Desativa aviso de mensagem direta'
        )(self.offavisodm)
        tree.command(
            name='onavisodm', description='Ativa aviso de mensagem direta'
        )(self.onavisodm)
        tree.command(
            name='idignore',
            description='Adiciona um ID de usuário à lista de ignorados',
        )(self.idignore)
        tree.command(
            name='readicionarids',
            description='Remove um ID de usuário da lista de ignorados',
        )(self.readicionarids)
        tree.command(name='dm', description='Envia o dm pelo bot')(self.dm)
