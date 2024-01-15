import discord
from discord import app_commands

from funcoes.alertas import (
    alerta_checkpoint,
    verificar_checkpoints_nao_enviados,
)
from funcoes.comandos import (
    processa_mensagem_canal_alvo,
    processa_mensagens_anteriores,
)
from funcoes.dados import dados, envia_planilha

from sqlalchemy.orm import Session
from database.bot_models import Bot
from database.session import engine

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
        bot = self.session.query(Bot).first()
        if bot:
            self.enviar_everyone = bot.enviar_everyone
            self.enviar_dm = bot.enviar_dm
            self.ids_ignorados = bot.ids_ignorados
            self.canal_checkpoint_id = bot.canal_checkpoint_id
            self.canal_planilha_id = bot.canal_planilha_id
            self.alerta_checkpoint_horario = bot.alerta_checkpoint_horario
            self.verificar_checkpoint_horario = bot.verificar_checkpoint_horario
        else:
            self.enviar_everyone: bool = True
            self.enviar_dm: bool = True
            #TODO: LEMBRAR QUE ISSO AQUI É UMA LISTA OU SEJA DEVERIA SER ALGO ASSIM: self.ids_ignorados: list = [] 
            self.ids_ignorados = None
            self.canal_checkpoint_id = None
            self.canal_planilha_id = None
            #TODO: VERIFICAR QUAL O PROBLEMA DESSES PARAMETROS 
            self.alerta_checkpoint_horario = None
            self.verificar_checkpoint_horario = None
        self.dados = dados
        self.alerta_checkpoint = alerta_checkpoint
        self.verificar_checkpoints_nao_enviados = (
            verificar_checkpoints_nao_enviados
        )


    def save(self):
        bot = self.session.query(Bot).first()

        if not bot:
            bot = Bot()
            self.session.add(bot)

        bot.enviar_everyone = self.enviar_everyone
        bot.enviar_dm = self.enviar_dm
        #TODO: IDs ignorados SÃO UMA LISTA, NÃO UMA STRING MAS POR ENQUANTO VAMOS DEIXAR ASSIM!
        bot.ids_ignorados = self.ids_ignorados
        #bot.ids_ignorados = ','.join(str(id) for id in self.ids_ignorados)
        bot.canal_checkpoint_id = self.canal_checkpoint_id
        bot.canal_planilha_id = self.canal_planilha_id
        bot.alerta_checkpoint_horario = self.alerta_checkpoint_horario
        bot.verificar_checkpoint_horario = self.verificar_checkpoint_horario

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
        
        bot = self.session.query(Bot).first()
        if bot:
            bot.enviar_everyone = self.enviar_everyone
            bot.enviar_dm = self.enviar_dm
            bot.ids_ignorados = self.ids_ignorados
            bot.canal_checkpoint_id = self.canal_checkpoint_id
            bot.canal_planilha_id = self.canal_planilha_id
            bot.alerta_checkpoint_horario = self.alerta_checkpoint_horario
            bot.verificar_checkpoint_horario = self.verificar_checkpoint_horario
            self.session.commit()

        await processa_mensagens_anteriores(self, self)
        
        #TODO: VERIFICAR QUAL O PROBLEMA DESSAS FUNÇÕES DE ALERTA (NÃO ESTÃO CONSEGUINDO OBTER OS CANAIS DE CHECKPOINT SERA?) 
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
                print(f"Exceção ao chamar processa_mensagem_canal_alvo: {e}")
        if (
            mensagem.channel.id == self.canal_planilha_id
            and mensagem.content.strip() == '@checkpoint'
        ):
            await envia_planilha(mensagem)
