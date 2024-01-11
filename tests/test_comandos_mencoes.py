from datetime import datetime
from unittest.mock import MagicMock

import pytest


@pytest.mark.asyncio
async def test_definir_alerta(mentions_commands, interaction, mock_horario):
    await mentions_commands.definir_alerta(interaction, mock_horario)
    interaction.response.send_message.assert_called_once_with(
        f'Alerta definido para {mentions_commands.cliente_discord.alerta_checkpoint_horario}.',
        ephemeral=True,
    )
    assert (
        mentions_commands.cliente_discord.alerta_checkpoint_horario
        == datetime.strptime(mock_horario, '%H:%M').time()
    )


@pytest.mark.asyncio
async def test_offeveryone(mentions_commands, interaction):
    await mentions_commands.offeveryone(interaction)
    interaction.response.send_message.assert_called_once_with(
        'Desativando menções a todos...', ephemeral=True
    )
    assert mentions_commands.cliente_discord.enviar_everyone is False


@pytest.mark.asyncio
async def test_oneveryone(mentions_commands, interaction):
    await mentions_commands.oneveryone(interaction)
    interaction.response.send_message.assert_called_once_with(
        'Ativando menções a todos...', ephemeral=True
    )
    assert mentions_commands.cliente_discord.enviar_everyone is True


def test_load_mentions_commands(mentions_commands):
    tree = MagicMock()
    mentions_commands.load_mentions_commands(tree)
    assert tree.command.call_count == 3