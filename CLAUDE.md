# SmartCash Project

## Project Overview
Django-based SmartCash application - Personal portfolio project for demonstrating skills to potential employers. Not intended for production deployment or enterprise scale.

## Environment Setup
- **IDE**: PyCharm
- **Python Version**: 3.13.2 (via venv)
- **Framework**: Django 5.2.3
- **Virtual Environment**: `.venv` (Windows-style structure)

## Installed Packages
- Django: 5.2.3
- asgiref: 3.8.1
- sqlparse: 0.5.3
- tzdata: 2025.2
- pip: 25.0.1

## Project Structure
- `SmartCash/` - Main Django project directory
  - `settings.py` - Django settings
  - `urls.py` - URL configuration
  - `wsgi.py` - WSGI configuration
  - `asgi.py` - ASGI configuration
- `templates/` - HTML templates directory
- `manage.py` - Django management script
- `.env` - Environment variables

## Commands
To activate the virtual environment in WSL:
```bash
source .venv/Scripts/activate
```

Or use Python/pip directly:
```bash
.venv/Scripts/python.exe manage.py runserver
.venv/Scripts/pip.exe install <package>
```

## Development Notes
- Running on Windows Subsystem for Linux (WSL2)
- Git repository initialized
- Using Windows-style virtual environment paths

## Important Guidelines
- **ALWAYS follow best practices** - Never choose simple solutions over best practices. Always implement industry-standard patterns, security measures, and code quality standards
- **NEVER use mock data** - Always use real data and actual implementations
- **Use context7** for up-to-date documentation when planning or writing code for **non-Piraeus Bank API related tasks**
- **For Piraeus Bank API integration**: Use the documentation files below (context7 does not have Piraeus Bank API information)

## Piraeus Bank API Documentation

### Technical API Specifications (Use First)
- **`docs/piraeus-bank-api/oauth-swagger.yaml`** - Complete OAuth2 API specification with endpoints, parameters, and schemas

### Implementation Guides (Use for Context)
- **`docs/piraeus-bank-api/oauth-flows-guide.md`** - OAuth2 flows, environment configs, SCA patterns, and integration guidance
- **`docs/piraeus-bank-api/error-handling-guide.md`** - Error codes, retry strategies, and SCA error handling flows

### Detailed Implementation Examples (Use for Complex Integration)
- **`docs/piraeus-bank-api/psd2-ais-quickstart.md`** - PSD2 AIS API step-by-step implementation guide
- **`docs/piraeus-bank-api/psd2-pis-quickstart.md`** - PSD2 PIS API payment initiation guide
- **`docs/piraeus-bank-api/psd2-ais-examples.md`** - PSD2 AIS API detailed implementation examples
- **`docs/piraeus-bank-api/psd2-pis-examples.md`** - PSD2 PIS API detailed payment examples
- **`docs/piraeus-bank-api/sandbox-reference.md`** - PSD2 APIs sandbox environment testing guide
- **`docs/piraeus-bank-api/pb-apis-sandbox-reference.md`** - PB APIs (v1.1/v1.2) sandbox testing guide

### Complete Error Reference (Use for Troubleshooting)
- **`docs/piraeus-bank-api/error-codes.md`** - Complete error code reference tables by API endpoint

## Documentation Usage Guidelines

**For OAuth2 Authentication:**
1. **Start with** `oauth-swagger.yaml` for exact API specification
2. **Use** `oauth-flows-guide.md` for environment setup and flow sequences
3. **Reference** `error-handling-guide.md` for SCA and error handling patterns

**For PSD2 API Integration:**
1. **Start with** respective quickstart guides for step-by-step implementation
2. **Use** detailed examples for complex scenarios
3. **Reference** sandbox guides for testing environment setup
