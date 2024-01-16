import json

import discord
from discord import app_commands
from sqlalchemy.orm import Session

from database.bot_models import Config_bot
from database.session import engine
from funcoes.alertas import (
    alerta_checkpoint,
    verificar_checkpoints_nao_enviados,
)
from funcoes.comandos import (
    processa_mensagem_canal_alvo,
    processa_mensagens_anteriores,
)
from funcoes.dados import dados, envia_planilha


class ConectorDiscord(discord.Client):
    """
    Classe responsável por conectar ao Discord e gerenciar as configurações do bot.

    Padrão de projeto: Singleton
    """

    _instance = None

    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False
        self.tree = app_commands.CommandTree(self)
        self.session = Session(bind=engine)
        config = self.session.query(Config_bot).first()
        if config:
            self.enviar_everyone = config.enviar_everyone
            self.enviar_dm = config.enviar_dm
            self.ids_ignorados = (
                json.loads(config.ids_ignorados)
                if config.ids_ignorados
                else []
            )
            self.canal_checkpoint_id = config.canal_checkpoint_id
            self.canal_planilha_id = config.canal_planilha_id
            self.alerta_checkpoint_horario = config.alerta_checkpoint_horario
            self.verificar_checkpoint_horario = (
                config.verificar_checkpoint_horario
            )
        else:
            self.enviar_everyone: bool = True
            self.enviar_dm: bool = True
            self.ids_ignorados = []
            self.canal_checkpoint_id = None
            self.canal_planilha_id = None
            self.alerta_checkpoint_horario = None
            self.verificar_checkpoint_horario = None

        self.dados = dados
        self.alerta_checkpoint = alerta_checkpoint
        self.verificar_checkpoints_nao_enviados = (
            verificar_checkpoints_nao_enviados
        )

    def save(self):
        config = self.session.query(Config_bot).first()

        if not config:
            config = Config_bot()
            self.session.add(config)

        config.enviar_everyone = self.enviar_everyone
        config.enviar_dm = self.enviar_dm
        config.ids_ignorados = (
            json.dumps(self.ids_ignorados) if self.ids_ignorados else None
        )
        config.canal_checkpoint_id = self.canal_checkpoint_id
        config.canal_planilha_id = self.canal_planilha_id
        config.alerta_checkpoint_horario = self.alerta_checkpoint_horario
        config.verificar_checkpoint_horario = self.verificar_checkpoint_horario

        self.session.commit()
        self.session.close()

    async def on_ready(self):
        """
        Evento chamado quando o bot está pronto para ser usado.
        """
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        print(f'{self.user} conectado ao Discord!')

        config = self.session.query(Config_bot).first()
        if config:
            config.enviar_everyone = self.enviar_everyone
            config.enviar_dm = self.enviar_dm
            config.ids_ignorados = self.ids_ignorados
            config.canal_checkpoint_id = self.canal_checkpoint_id
            config.canal_planilha_id = self.canal_planilha_id
            config.ids_ignorados = (
                json.dumps(self.ids_ignorados) if self.ids_ignorados else None
            )
            config.verificar_checkpoint_horario = (
                self.verificar_checkpoint_horario
            )
            self.session.commit()

        # TODO: talvez uma função de deixar ele desativado seja interresante pois esse comando só é necessario uma vez...
        await processa_mensagens_anteriores(self, self)

        # tasks
        self.loop.create_task(alerta_checkpoint(self, self))
        self.loop.create_task(
            verificar_checkpoints_nao_enviados(self, self, self.dados)
        )

    async def on_message(self, mensagem):
        await self.wait_until_ready()
        if mensagem.author == self.user:
            return

        if mensagem.channel.id == self.canal_checkpoint_id:
            try:
                await processa_mensagem_canal_alvo(mensagem)
            except Exception as e:
                print(f'Exceção ao chamar processa_mensagem_canal_alvo: {e}')
        if (
            mensagem.channel.id == self.canal_planilha_id
            and mensagem.content.strip() == '@checkpoint'
        ):
            await envia_planilha(mensagem)
