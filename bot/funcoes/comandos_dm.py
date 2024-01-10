from datetime import datetime


import discord



class DmCommands:
    def __init__(self, cliente):
        self.cliente_discord = cliente

    async def alerta_dm_horario(self, interaction: discord.Interaction, horario: str):
        horario = datetime.strptime(horario, "%H:%M").time()
        self.cliente_discord.verificar_checkpoint_horario = horario
        await interaction.response.send_message(f'Alerta definido para {self.cliente_discord.verificar_checkpoint_horario}.')

    async def offavisodm(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            'Desativando aviso de mensagem direta...', ephemeral=True
        )
        self.cliente_discord.enviar_dm = False

    async def onavisodm(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            'Ativando aviso de mensagem direta...', ephemeral=True
        )
        self.cliente_discord.enviar_dm = True

    #TODO: discord.User é um objeto que representa um usuário do Discord então na vez de passar diretamente um parametro id eu posso passar um objeto discord.User
    #TODO: NECESSARIO TESTAR
    async def idignore(self, interaction: discord.Interaction, id: str):
        self.cliente_discord.ids_ignorados = int(id)
        await interaction.response.send_message(f'ID de usuário {self.cliente_discord.ids_ignorados} adicionado à lista de ignorados.')

    #TODO: NECESSARIO TESTAR
    async def readicionarids(self, interaction: discord.Interaction, id: str):
        self.cliente_discord.ids_ignorados.remove(int(id))
        await interaction.response.send_message(f'ID de usuário {id} removido da lista de ignorados.')

    async def dm(interaction: discord.Interaction, user: discord.User, *, mensagem: str):
        try:
            if user:
                dm_channel = await user.create_dm()
                await dm_channel.send(mensagem)
                await interaction.response.send_message(f'Mensagem enviada para o usuário {user.name}.')
            else:
                await interaction.response.send_message('Não foi possível encontrar o usuário mencionado.')
        except discord.errors.HTTPException:
            await interaction.response.send_message('Não foi possível enviar a mensagem para o usuário mencionado.')

    def load_dm_commands(self, tree):
        tree.command(name='horario_verificar', description='Define o horário do verficar checkpoint')(self.alerta_dm_horario)
        tree.command(name='offavisodm', description='Desativa aviso de mensagem direta')(self.offavisodm)
        tree.command(name='onavisodm', description='Ativa aviso de mensagem direta')(self.onavisodm)
        #TODO: NECESSARIO TESTAR
        tree.command(name='idignore', description='Adiciona um ID de usuário à lista de ignorados')(self.idignore)
        #TODO: NECESSARIO TESTAR
        tree.command(name='readicionarids', description='Remove um ID de usuário da lista de ignorados')(self.readicionarids)
        tree.command(name='dm', description='Envia o dm pelo bot')(self.dm)
