# Contributing to Trello MCP Server

Thanks for your interest in contributing! This document provides guidelines and steps for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a branch for your changes

```bash
git checkout -b feature/your-feature-name
```

4. Install dependencies

```bash
uv sync --extra dev
cp .env.example .env  # Fill in your Trello API key and token
```

## Development Workflow

### Running Tests

```bash
uv run pytest --cov
```

### Linting and Formatting

```bash
uv run ruff check .
uv run ruff format --check .
```

Pre-commit hooks are configured to run these checks automatically:

```bash
uv run pre-commit install
```

### Code Style

- Follow existing code patterns and conventions
- Keep functions focused and concise
- Add tests for new functionality
- Maintain test coverage above 80%

## Submitting Changes

1. Commit your changes with a clear, descriptive message
2. Push to your fork
3. Open a Pull Request against the `main` branch
4. Describe what your PR does and why

## Reporting Issues

- Use GitHub Issues to report bugs or suggest features
- Include steps to reproduce for bug reports
- Check existing issues before opening a new one

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
