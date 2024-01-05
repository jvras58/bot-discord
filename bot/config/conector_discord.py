from datetime import datetime


class ConectorDiscord:
    """
    Classe responsável por conectar ao Discord e gerenciar as configurações do bot.

    Padrão de projeto: Singleton
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.enviar_everyone: bool = True
        self.enviar_dm: bool = True
        self.ids_ignorados: list[str] = []
        self.canal_checkpoint_id: str = None
        self.canal_planilha_id: str = None
        self.alerta_checkpoint_horario: datetime = None
        self.verificar_checkpoint_horario: datetime = None
