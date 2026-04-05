# Contributing to Financing

Thank you for your interest in contributing to Financing!

## Development Workflow

### Prerequisites
- Python 3.11+
- Node.js (for frontend)
- Virtual environment

### Getting Started
1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Run tests locally
6. Submit a pull request

## Testing

### Run Tests
```bash
# All tests
pytest

# Unit tests only
pytest tests/unit

# Integration tests only
pytest tests/integration

# Ports tests only
pytest tests/ports
```

### Code Quality
```bash
# Format code
black src tests scripts

# Lint code
ruff check src tests scripts

# Type check
mypy src
```

## Ports Management

This project uses a centralized port management system to avoid conflicts across multiple projects on the same host.

### Port Registry Files
- **PORTS.md**: Human-readable port documentation
- **ports.json**: Machine-readable port registry
- **ports.schema.json**: JSON Schema for validation

### Adding a New Service
1. Update `ports.json` with your service details:
   ```json
   {
     "id": "your-service",
     "name": "Your Service Name",
     "path": "your/path",
     "port": 12345,
     "fallbacks": [12346, 12347],
     "env_var": "YOUR_PORT",
     "owner": {"team": "your-team", "contact": "your.email@example.com"},
     "status": "active",
     "notes": "Description of your service"
   }
   ```

2. Validate locally:
   ```bash
   python3 -m scripts.ports_validate --file ./ports.json
   ```

3. Update `PORTS.md` to document your service

### Generating Local .env Files
When developing locally, generate your `.env.local` file from the port registry:

```bash
# Generate for a specific service by ID
python3 scripts/ports_generate_env.py --id frontend --out ./frontend/.env.local

# Generate with fallback support
python3 scripts/ports_generate_env.py --id frontend --out ./frontend/.env.local --allow-fallback
```

The generated file will have a header: `# GENERATED FROM ports.json - DO NOT COMMIT`

**Important**: Do not commit generated `.env.local` files. They are gitignored.

### Port Conflict Resolution
If you encounter a port conflict:
1. Check `ports.json` for the assigned port
2. Use `--allow-fallback` to use a fallback port
3. If no fallbacks are available, an ephemeral port will be auto-selected
4. Report persistent conflicts to the team

### Port Ownership
- Each port entry has an owner (team + contact)
- Contact the owner before modifying their port assignments
- Port changes require team approval

## Pull Request Process

1. Ensure your code passes all tests
2. Update documentation as needed
3. Keep your PR focused and small
4. Include a clear description of changes
5. Link related issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
