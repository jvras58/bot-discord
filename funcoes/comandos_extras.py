import random
import discord
from discord import app_commands

from funcoes.comandos import create_image


class ExtrasCommands:
    def __init__(self, cliente):
        self.cliente_discord = cliente

    
    @app_commands.describe(
        usuario1='Primeiro usuário a shippar',
        usuario2='Segundo usuário a shippar',
    )
    async def ship(
        self,
        interaction: discord.Interaction,
        usuario1: discord.User,
        usuario2: discord.User,
    ):
        porcentagem = random.randint(0, 100)
        metade1 = usuario1.name[: len(usuario1.name) // 2]
        metade2 = usuario2.name[len(usuario2.name) // 2 :]
        nomeship = metade1 + metade2

        buffer = await create_image(usuario1, usuario2, porcentagem)

        if porcentagem <= 35:
            mensagem_extra = (
                '😅 Não parece rolar uma química tão grande, mas quem sabe...?'
            )
        elif porcentagem <= 65:
            mensagem_extra = (
                '☺️ Essa combinação tem potencial, que tal um jantar romântico?'
            )
        else:
            mensagem_extra = '😍 Combinação perfeita! Quando será o casamento?'

        await interaction.response.send_message(
            f':hot_face: **Será que vamos ter um casal novo por aqui?** :hot_face: \n {self.cliente_discord.user}: {usuario1.mention} + {usuario2.mention} = ✨ `{nomeship}` ✨\n{mensagem_extra}',
            file=discord.File(fp=buffer, filename='file.png'),
        )
    
    def load_extras_commands(self, tree):
        tree.command(
            name='ship',
            description='Cheque se alguém é sua alma gêmea',
        )(self.ship)
