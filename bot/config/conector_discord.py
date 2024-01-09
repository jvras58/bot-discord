from datetime import datetime
from discord import app_commands
import discord

from funcoes.alertas import (
    alerta_checkpoint,
    verificar_checkpoints_nao_enviados,
)
from funcoes.comandos import processa_mensagens_anteriores #,processa_mensagem_canal_alvo
from funcoes.dados import dados #, envia_planilha

class ConectorDiscord(discord.Client):
    """
    Classe responsável por conectar ao Discord e gerenciar as configurações do bot.

    Padrão de projeto: Singleton
    """

    _instance = None
    
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.tree = app_commands.CommandTree(self)
        self.enviar_everyone: bool = True
        self.enviar_dm: bool = True
        self.ids_ignorados: list[str] = []
        self.canal_checkpoint_id: str = None
        self.canal_planilha_id: str = None
        self.alerta_checkpoint_horario: datetime = None
        self.verificar_checkpoint_horario: datetime = None
        self.dados = dados
        self.alerta_checkpoint = alerta_checkpoint
        self.verificar_checkpoints_nao_enviados = (
            verificar_checkpoints_nao_enviados
        )

    # TODO: self é a própria instância de ConectorDiscord por isso (conector_discord, cliente_discord) se passa como (self)
    async def on_ready(self):
        """
        Evento chamado quando o bot está pronto para ser usado.
        - processa_mensagens_anteriores(conector_discord= self, cliente_discord= self): função para processar mensagens anteriores do canal de checkpoint
        - alerta_checkpoint(conector_discord= self, cliente_discord= self): função para alertar sobre checkpoints
        - verificar_checkpoints_nao_enviados(cliente_discord = self, conector_discord= self, dados= self.dados): função para verificar checkpoints não enviados
        """
        await self.wait_until_ready()
        if not self.synced:
            # como não tem o guild_id, os comandos sempre demoram de 1~24 hrs para sincronizar
            await self.tree.sync()
            self.synced = True
        print(f'{self.user} conectado ao Discord!')
        #TODO: funcionando!!
        await processa_mensagens_anteriores(self, self)
        #TODO: funcionando!!
        self.loop.create_task(alerta_checkpoint(self, self))
        #FIXME: testar!!
        self.loop.create_task(verificar_checkpoints_nao_enviados(self, self, self.dados))
    
    #TODO: Analisar como fazer essa parte principal de ler os checkpoints no canal como é feito no codigo anterior
    # async def on_message(self, mensagem):
    #     """
    #     Evento chamado quando uma mensagem é enviada.
    #     """
    #     await self.wait_until_ready()

    #     # TODO: ESSA É A MAGICA QUE FAZ A LEITURA DAS MENSAGENS NO CANAL DO CHECKPOINT ELE COMEÇA A LER APARTIR QUE RECEBE O ID DO CANAL E ENVIA A PLANILHA NO CANAL DA PLANILHA QUANDO RECEBE O /CHECKPOINT
    #     if mensagem.channel.id == self.canal_checkpoint_id:
    #         await processa_mensagem_canal_alvo(mensagem)
    #     if (
    #         mensagem.channel.id == self.canal_planilha_id
    #         and mensagem.content.strip() == '/planilha'
    #     ):
    #         await envia_planilha(mensagem)
