from unittest.mock import AsyncMock, MagicMock

import pytest

from config.conector_discord import ConectorDiscord
from funcoes.comandos_basicos import BasicCommands
from funcoes.comandos_config_canal import CanalCommands
from funcoes.comandos_dm import DmCommands
from funcoes.comandos_mencoes import MentionsCommands


@pytest.fixture
def cliente_discord():
    return ConectorDiscord()


@pytest.fixture
def basic_commands(cliente_discord):
    return BasicCommands(cliente_discord)


@pytest.fixture
def mentions_commands(cliente_discord):
    return MentionsCommands(cliente_discord)


@pytest.fixture
def dm_commands(cliente_discord):
    return DmCommands(cliente_discord)


@pytest.fixture
def canal_commands(cliente_discord):
    return CanalCommands(cliente_discord)


@pytest.fixture
def interaction():
    interaction = MagicMock()
    interaction.response.send_message = AsyncMock()
    interaction.user.create_dm = AsyncMock()
    return interaction


@pytest.fixture
def interaction_channel():
    interaction = MagicMock()
    interaction.response.send_message = AsyncMock()
    interaction.channel = MagicMock()
    return interaction
