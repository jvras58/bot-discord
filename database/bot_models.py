from typing import List
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from config.base_model import Base
from config.jsonencodeddict import JsonEncodedDict




class Bot(Base):
    """
    Representa a tabela configurações do bot no banco de dados.
    """

    __tablename__ = 'bot'

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    enviar_everyone: Mapped[bool] = mapped_column()
    enviar_dm: Mapped[bool] = mapped_column()
    #TODO: COMO EU SERIALIZO ESSA LISTA? ISSO É O SUFICIENTE? #acho que não precisa do JsonEncodedDict o Mapped[List[str]] já deve fazer o trabalho direito ou  json.dumps(lista)
    ids_ignorados: Mapped[List[str]] = mapped_column(JsonEncodedDict)
    canal_checkpoint_id: Mapped[str] = mapped_column()
    canal_planilha_id: Mapped[str] = mapped_column()
    alerta_checkpoint_horario: Mapped[datetime] = mapped_column()
    verificar_checkpoint_horario: Mapped[datetime] = mapped_column()
