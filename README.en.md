# harness-agent

> PBH protocol-driven autonomous code repair agent — We don't tell AI how to think. We give it the best environment to work in.

## Quick Start

```bash
pip install -e ".[dev]"
make verify
```

## Commands

| Command | Description |
|---------|-------------|
| `make verify` | lint + tests + coverage |
| `make test` | run tests |
| `make lint` | code style check |
| `make fix` | auto-fix style issues |

## Project Structure

```
harness-agent/
├── src/harness_agent/   # Main code
├── tests/                # Tests
├── tasks/                # Task breakdown
├── docs/                 # Documentation
├── AGENTS.md             # AI collaboration protocol
├── Makefile
└── pyproject.toml
```

## AI Collaboration

This project follows the PBH protocol. AI assistants should read `AGENTS.md` for project rules and working guidelines.

## Ecosystem

This project is the third product of the PBH ecosystem, working alongside:

| Project | Description |
|---------|-------------|
| [PBH](https://github.com/renjianguojinqianfan/Project-Bootstrap-Harness) | Seeds AI collaboration protocols (AGENTS.md / make verify / progress.json) |
| [Harness-Lint](https://github.com/renjianguojinqianfan/harness-lint) | Detects typical AI coding defects with attribution-anchored reports |

Harness Agent's behavior is entirely driven by PBH-seeded protocol files — when project rules change, only AGENTS.md needs updating, not a single line of agent code.

## License

MIT