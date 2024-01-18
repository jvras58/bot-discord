import asyncio
from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from app.config.conector_discord import ConectorDiscord
from app.funcoes.comandos_basicos import BasicCommands
from app.funcoes.comandos_config_canal import CanalCommands
from app.funcoes.comandos_dm import DmCommands
from app.funcoes.comandos_mencoes import MentionsCommands


@pytest.fixture
def mock_canal():
    """
    Fixture que cria um canal de texto falso para uso nos testes.

    Retorna uma instância de MockTextChannel que simula um canal de texto do Discord.
    """

    class MockTextChannel(discord.TextChannel):
        def __str__(self):
            return 'mock channel'

    state = MagicMock()
    guild = MagicMock()
    data = MagicMock()
    return MockTextChannel(state=state, guild=guild, data=data)


@pytest.fixture
def cliente_discord():
    """
    Fixture que retorna uma instância do ConectorDiscord para ser usada nos testes.
    """
    return ConectorDiscord()


@pytest.fixture
def basic_commands(cliente_discord):
    """
    Fixture que retorna uma instância da classe BasicCommands,
    inicializada com o cliente_discord fornecido como argumento.
    """
    return BasicCommands(cliente_discord)


@pytest.fixture
def mentions_commands(cliente_discord):
    """
    Fixture que retorna uma instância da classe mentions_commands,
    inicializada com o cliente_discord fornecido como argumento.
    """
    return MentionsCommands(cliente_discord)


@pytest.fixture
def dm_commands(cliente_discord):
    """
    Fixture que retorna uma instância da classe dm_commands,
    inicializada com o cliente_discord fornecido como argumento.
    """
    return DmCommands(cliente_discord)


@pytest.fixture
def canal_commands(cliente_discord):
    """
    Fixture que retorna uma instância da classe canal_commands,
    inicializada com o cliente_discord fornecido como argumento.
    """
    return CanalCommands(cliente_discord)


@pytest.fixture
def mock_horario():
    return '12:34'


@pytest.fixture
def mock_id():
    return '1234567890'


@pytest.fixture
def mock_mensagem():
    return 'Esta é uma mensagem de teste'


@pytest.fixture
def mock_user():
    """
    Fixture para criar um usuário fictício para testes.

    Retorna um objeto MagicMock que simula um usuário.
    O usuário possui um atributo 'name' definido como 'mock_user'.
    Além disso, a função 'create_dm' é substituída por uma função assíncrona que retorna um objeto MagicMock
    simulando um canal de mensagem direta (DM). A função 'send' desse canal é substituída por uma função
    assíncrona que retorna um objeto Future, que é resolvido imediatamente com o valor None.

    Retorna:
        MagicMock: Objeto simulando um usuário fictício para testes.
    """
    user = MagicMock()
    user.name = 'mock_user'

    async def create_dm():
        dm_channel = MagicMock()
        dm_channel.send = MagicMock(return_value=asyncio.Future())
        dm_channel.send.return_value.set_result(None)
        return dm_channel

    user.create_dm = MagicMock(side_effect=create_dm)
    return user


@pytest.fixture
def interaction():
    """
    Fixture que simula uma interação com o usuário.

    Retorna um objeto MagicMock que simula uma interação com o usuário.
    Esse objeto possui os seguintes atributos e métodos:
    - response.send_message: um método assíncrono que simula o envio de uma mensagem de resposta.
    - user.create_dm: um método assíncrono que simula a criação de uma mensagem direta com o usuário.

    Exemplo de uso:
    interaction = interaction()
    interaction.response.send_message("Olá, mundo!")
    interaction.user.create_dm()
    """
    interaction = AsyncMock()
    interaction.response.send_message = AsyncMock()
    interaction.user.create_dm = AsyncMock()
    return interaction


@pytest.fixture
def interaction_channel():
    """
    Fixture que simula um canal de interação para testes.

    Retorna um objeto MagicMock que simula uma interação com o bot.
    O objeto possui um método send_message() que é um objeto AsyncMock,
    simulando o envio de uma mensagem de resposta.
    O objeto também possui um atributo channel que é um objeto MagicMock,
    simulando um canal de interação.

    Retorna:
        MagicMock: Objeto que simula uma interação com o bot.
    """
    interaction = MagicMock()
    interaction.response.send_message = AsyncMock()
    interaction.channel = MagicMock()
    return interaction
