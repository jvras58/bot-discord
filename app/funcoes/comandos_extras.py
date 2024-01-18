import random
from collections import defaultdict

import discord
from discord import app_commands
from funcoes.comandos import create_image


class ExtrasCommands:
    """
    Classe que define os comandos extras.
    """

    def __init__(self, cliente):
        """
        Inicializa a classe CanalCommands.

        Args:
            cliente (objeto): O cliente Discord.
        """
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
        namoro: bool,
    ):
        """
        Ship 2 users e gerar um nome de ship e porcentagem.

        Args:
            interaction (discord.Interaction): A interação do usuário com o comando.
            usuario1 (discord.User): usuario 1
            usuario2 (discord.User): usuario 2.
            namoro (bool): Indica se o ship é para um relacionamento amoroso.

        """
        porcentagem = random.randint(0, 100)
        metade1 = usuario1.name[: len(usuario1.name) // 2]
        metade2 = usuario2.name[len(usuario2.name) // 2 :]
        nomeship = metade1 + metade2

        buffer = await create_image(usuario1, usuario2, porcentagem)

        if namoro:
            if porcentagem <= 35:
                mensagem_extra = '😅 Não parece rolar uma química tão grande, mas quem sabe...?'
            elif porcentagem <= 65:
                mensagem_extra = '☺️ Essa combinação tem potencial, que tal um jantar romântico?'
            else:
                mensagem_extra = (
                    '😍 Combinação perfeita! Quando será o casamento?'
                )
        else:
            if porcentagem <= 35:
                mensagem_extra = (
                    '😅 Parece que vocês não têm muitos interesses em comum...'
                )
            elif porcentagem <= 65:
                mensagem_extra = '☺️ Essa combinação tem potencial!!'
            else:
                mensagem_extra = '😍 Vocês são melhores amigos!'

        await interaction.response.send_message(
            f':hot_face: **Será que vamos ter um match novo por aqui?** :hot_face: \n {self.cliente_discord.user}: {usuario1.mention} + {usuario2.mention} = ✨ `{nomeship}` ✨\n{mensagem_extra}',
            file=discord.File(fp=buffer, filename='file.png'),
        )

    async def ranking(self, interaction: discord.Interaction):
        """
        Retorna o ranking de usuários com base no número de checkpoints enviados.

        Args:
        interaction (discord.Interaction): A interação do usuário com o comando.
        """
        # Extrai o canal do checkpoint
        canal_alvo = self.cliente_discord.get_channel(
            self.cliente_discord.canal_checkpoint_id
        )

        # Cria um dicionário para armazenar o número de checkpoints enviados por cada usuário
        ranking = defaultdict(int)

        # Itera sobre as mensagens no canal
        async for mensagem in canal_alvo.history(limit=50000):
            # Verifica se a mensagem foi enviada pelo próprio bot
            if mensagem.author == self.cliente_discord.user:
                continue

            # Incrementa o contador para o usuário que enviou a mensagem
            ranking[mensagem.author.id] += 1

        # Classifica o dicionário pelo número de checkpoints enviados
        ranking_ordenado = sorted(
            ranking.items(), key=lambda item: item[1], reverse=True
        )

        # Envia o ranking no chat
        for i, (id_usuario, num_checkpoints) in enumerate(ranking_ordenado, 1):
            await interaction.response.send_message(
                f'{i}. <@{id_usuario}>: {num_checkpoints} checkpoints'
            )

    def load_extras_commands(self, tree):
        """
        Carrega os comandos extras no objeto tree.

        Args:
            tree: O objeto tree onde os comandos serão carregados.
        """
        tree.command(
            name='ship',
            description='Cheque se alguém é sua alma gêmea',
        )(self.ship)
        tree.command(
            name='ranking',
            description='Mostra o ranking de usuários que mais enviaram checkpoints',
        )(self.ranking)
