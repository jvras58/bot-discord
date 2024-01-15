from typing import List
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from config.base_model import Base





class Bot(Base):
    """
    Representa a tabela configurações do bot no banco de dados.
    """

    __tablename__ = 'bot'

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    enviar_everyone: Mapped[bool] = mapped_column(nullable=True)
    enviar_dm: Mapped[bool] = mapped_column(nullable=True)
    #TODO: COMO EU SERIALIZO ESSA LISTA? ISSO É O SUFICIENTE? #acho que não precisa do JsonEncodedDict o Mapped[List[str]] já deve fazer o trabalho direito ou  json.dumps(lista)
    ids_ignorados: Mapped[str] = mapped_column(nullable=True)
    canal_checkpoint_id: Mapped[int] = mapped_column(nullable=True)
    canal_planilha_id: Mapped[int] = mapped_column(nullable=True)
    alerta_checkpoint_horario: Mapped[datetime] = mapped_column(nullable=True)
    verificar_checkpoint_horario: Mapped[datetime] = mapped_column(nullable=True)
