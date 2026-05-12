"""Tests for cli.py."""

from unittest.mock import AsyncMock, patch

from typer.testing import CliRunner

from harness_agent.cli import app

runner = CliRunner()


def test_hello_default() -> None:
    """hello should print greeting with default name."""
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_hello_with_name() -> None:
    """hello should print greeting with provided name."""
    result = runner.invoke(app, ["hello", "Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output


def test_version_flag() -> None:
    """--version should print version and exit."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_version_short_flag() -> None:
    """-v should print version and exit."""
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_chat_command() -> None:
    """chat should start interactive session."""
    with patch("harness_agent.cli.chat_loop", new_callable=AsyncMock) as mock_chat:
        result = runner.invoke(app, ["chat"])
        assert result.exit_code == 0
        assert "Starting chat session" in result.output
        mock_chat.assert_called_once_with("default")


def test_chat_command_with_session_id() -> None:
    """chat should accept custom session_id."""
    with patch("harness_agent.cli.chat_loop", new_callable=AsyncMock) as mock_chat:
        result = runner.invoke(app, ["chat", "my_session"])
        assert result.exit_code == 0
        assert "my_session" in result.output
        mock_chat.assert_called_once_with("my_session")
