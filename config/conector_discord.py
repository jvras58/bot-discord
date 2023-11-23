
class ConectorDiscord:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.enviar_everyone: bool  = True
        self.enviar_dm: bool = True
        self.ids_ignorados:list[str] =[]
        self.canal_checkpoint_id:str = None 
        self.canal_planilha_id:str = None
        
