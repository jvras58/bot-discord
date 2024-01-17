from datetime import datetime
from unittest.mock import MagicMock

import pytest

from config.config import get_settings


@pytest.mark.asyncio
async def test_alerta_dm_horario(dm_commands, interaction, mock_horario):
    for id in get_settings().AUTHORIZATION_IDS.split(','):
        interaction.user.id = int(id)
    await dm_commands.alerta_dm_horario(interaction, mock_horario)
    interaction.response.send_message.assert_called_once_with(
        f'Alerta definido para {dm_commands.cliente_discord.verificar_checkpoint_horario}.',
        ephemeral=True,
    )
    assert (
        datetime.strptime(
            dm_commands.cliente_discord.verificar_checkpoint_horario, '%H:%M'
        ).time()
        == datetime.strptime(mock_horario, '%H:%M').time()
    )


@pytest.mark.asyncio
async def test_offavisodm(dm_commands, interaction):
    for id in get_settings().AUTHORIZATION_IDS.split(','):
        interaction.user.id = int(id)
    await dm_commands.offavisodm(interaction)
    interaction.response.send_message.assert_called_once_with(
        'Desativando aviso de mensagem direta...', ephemeral=True
    )
    assert dm_commands.cliente_discord.enviar_dm is False


@pytest.mark.asyncio
async def test_onavisodm(dm_commands, interaction):
    for id in get_settings().AUTHORIZATION_IDS.split(','):
        interaction.user.id = int(id)
    await dm_commands.onavisodm(interaction)
    interaction.response.send_message.assert_called_once_with(
        'Ativando aviso de mensagem direta...', ephemeral=True
    )
    assert dm_commands.cliente_discord.enviar_dm is True


@pytest.mark.asyncio
async def test_readicionarids(dm_commands, interaction, mock_id):
    for id in get_settings().AUTHORIZATION_IDS.split(','):
        interaction.user.id = int(id)

    dm_commands.cliente_discord.ids_ignorados = [int(mock_id)]
    await dm_commands.readicionarids(interaction, mock_id)
    interaction.response.send_message.assert_called_once_with(
        f'ID de usuário {mock_id} removido da lista de ignorados. Lista atual: []',
        ephemeral=True,
    )
    assert int(mock_id) not in dm_commands.cliente_discord.ids_ignorados


@pytest.mark.asyncio
async def test_dm(dm_commands, interaction, mock_user, mock_mensagem):
    dm_channel_mock = MagicMock()
    mock_user.create_dm.return_value = dm_channel_mock

    await dm_commands.dm(interaction, mock_user, mensagem=mock_mensagem)

    mock_user.create_dm.assert_called_once()
    interaction.response.send_message.assert_called_once_with(
        f'Mensagem enviada para o usuário {mock_user.name}.'
    )


@pytest.mark.asyncio
async def test_dm_user_not_found(dm_commands, interaction, mock_mensagem):
    mock_user = None

    await dm_commands.dm(interaction, mock_user, mensagem=mock_mensagem)

    interaction.response.send_message.assert_called_once_with(
        'Não foi possível encontrar o usuário mencionado.'
    )


def test_load_dm_commands(dm_commands):
    tree = MagicMock()
    dm_commands.load_dm_commands(tree)
    assert tree.command.call_count == 6
