"""Tests for agent.py."""

from unittest.mock import MagicMock, patch

import pytest

from harness_agent.agent import EXIT_COMMANDS, chat_loop, main


def test_exit_commands() -> None:
    """EXIT_COMMANDS should contain quit, exit, q."""
    assert "quit" in EXIT_COMMANDS
    assert "exit" in EXIT_COMMANDS
    assert "q" in EXIT_COMMANDS


@pytest.mark.asyncio
async def test_chat_loop_exit_command(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should exit when user inputs quit."""
    with patch("builtins.input", side_effect=["quit"]):
        await chat_loop()
        captured = capsys.readouterr()
        assert "再见" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_exit_uppercase(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should exit when user inputs QUIT."""
    with patch("builtins.input", side_effect=["QUIT"]):
        await chat_loop()
        captured = capsys.readouterr()
        assert "再见" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_exit_command_exit(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should exit when user inputs exit."""
    with patch("builtins.input", side_effect=["exit"]):
        await chat_loop()
        captured = capsys.readouterr()
        assert "再见" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_empty_input(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should skip empty inputs."""
    with patch("builtins.input", side_effect=["", "quit"]):
        await chat_loop()
        captured = capsys.readouterr()
        assert "再见" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_whitespace_input(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should skip whitespace-only inputs."""
    with patch("builtins.input", side_effect=["   ", "quit"]):
        await chat_loop()
        captured = capsys.readouterr()
        assert "再见" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_keyboard_interrupt(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should handle KeyboardInterrupt gracefully."""
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        await chat_loop()
        captured = capsys.readouterr()
        assert "再见" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_eof_error(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should handle EOFError gracefully."""
    with patch("builtins.input", side_effect=EOFError):
        await chat_loop()
        captured = capsys.readouterr()
        assert "再见" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_with_session_id(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should accept custom session_id."""
    with patch("builtins.input", side_effect=["quit"]):
        await chat_loop(session_id="test_session")
        captured = capsys.readouterr()
        assert "再见" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_welcome_message(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should display welcome message."""
    with patch("builtins.input", side_effect=["quit"]):
        await chat_loop()
        captured = capsys.readouterr()
        assert "Harness Agent Architect" in captured.out
        assert "quit/exit/q" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_with_conversation(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should handle conversation and display response."""
    mock_result = MagicMock()
    mock_result.final_output = "Test response"
    with (
        patch("builtins.input", side_effect=["test question", "quit"]),
        patch("harness_agent.agent.Runner.run", return_value=mock_result),
    ):
        await chat_loop()
        captured = capsys.readouterr()
        assert "Architect: Test response" in captured.out


@pytest.mark.asyncio
async def test_chat_loop_runner_exception(capsys: pytest.CaptureFixture) -> None:
    """chat_loop should handle Runner.run exceptions."""
    with (
        patch("builtins.input", side_effect=["test question", "quit"]),
        patch("harness_agent.agent.Runner.run", side_effect=Exception("API error")),
    ):
        await chat_loop()
        captured = capsys.readouterr()
        assert "错误" in captured.out
        assert "API error" in captured.out


@pytest.mark.asyncio
async def test_main(capsys: pytest.CaptureFixture) -> None:
    """main should run agent and print output."""
    mock_result = MagicMock()
    mock_result.final_output = "Test analysis result"
    with patch("harness_agent.agent.Runner.run", return_value=mock_result):
        await main()
        captured = capsys.readouterr()
        assert "Architect 分析结论" in captured.out
        assert "Test analysis result" in captured.out
