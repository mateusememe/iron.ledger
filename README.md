<p align="center">
  <img src="logo.png" alt="Iron Ledger" width="120" />
</p>

<h1 align="center">Iron Ledger</h1>

<p align="center">
  <em>Every set. Every rep. Accounted for.</em>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#philosophy">Philosophy</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#roadmap">Roadmap</a>
</p>

---

Import bodybuilding routines into [Hevy](https://hevy.com) with a clean and maintainable workflow.

**Iron Ledger** is a lightweight Python SDK that converts structured workout definitions into Hevy routines using the [official API](https://api.hevyapp.com/docs). Designed with simplicity, maintainability, and long-term evolution in mind.

## Features

- **Import complete workout programs** — define once, upload anywhere
- **Automatic exercise mapping** — fuzzy matching against Hevy's exercise library
- **Routine folder creation** — organize programs into folders
- **Validation before upload** — catch errors before hitting the API
- **Retry on API failures** — exponential backoff on `429` responses
- **Idempotent imports** — safe to re-run
- **Structured logging** — clear, colored output with progress indicators
- **Minimal configuration** — just one env var

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root (see [`.env.example`](.env.example)):

```env
HEVY_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Get your API key at [hevy.com/settings?developer](https://hevy.com/settings?developer).

> **Note:** The Hevy API requires a Hevy Pro subscription.

## Usage

### Upload default program

```bash
python cli.py upload
```

### Upload a specific workout file

```bash
python cli.py upload iron_ledger/workouts/periodizacao_ab.py
```

### Upload into a named folder

```bash
python cli.py upload --folder "Periodização A/B"
```

### Dry run (validate without uploading)

```bash
python cli.py upload --dry-run
```

## Defining Workouts

Workout programs are plain Python dictionaries. No YAML, no JSON, no magic:

```python
PROGRAM = {
    "name": "My Program",
    "workouts": [
        {
            "title": "Workout A",
            "notes": "Upper body focus",
            "exercises": [
                {
                    "name": "Bench Press (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Control the descent",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 60},
                        {"type": "normal", "reps": 10, "weight_kg": 60},
                        {"type": "normal", "reps": 8,  "weight_kg": 65},
                        {"type": "failure", "reps": 6, "weight_kg": 70},
                    ]
                },
            ]
        },
    ]
}
```

See [`iron_ledger/workouts/periodizacao_ab.py`](iron_ledger/workouts/periodizacao_ab.py) for a complete example.

## Philosophy

This project intentionally favors:

- **SOLID** — single responsibility, open for extension
- **DRY** — no duplicated logic
- **KISS** — simplest solution that works
- **Clean Architecture** — clear separation of concerns
- **Composition over inheritance** — flexible, testable design
- **Explicit code** — no hidden behavior
- **Readability first** — code is read far more than written

No unnecessary abstractions. No hidden magic. No framework dependency.

## Architecture

```
CLI
 ↓
Importer
 ↓
Validator
 ↓
Exercise Mapper
 ↓
Hevy API Client
 ↓
Hevy
```

### Project Structure

```
iron-ledger/
├── cli.py                          # CLI entry point
├── iron_ledger/
│   ├── config.py                   # Environment configuration
│   ├── constants.py                # API constants
│   ├── exceptions.py               # Custom exceptions
│   ├── api/
│   │   ├── client.py               # HTTP client with auth
│   │   ├── routines.py             # Routine operations
│   │   ├── folders.py              # Folder operations
│   │   └── exercises.py            # Exercise template operations
│   ├── domain/
│   │   ├── models.py               # Data models (dataclasses)
│   │   └── mapper.py               # Fuzzy exercise matching
│   ├── importer/
│   │   ├── importer.py             # Import orchestrator
│   │   └── validator.py            # Program validation
│   ├── workouts/
│   │   └── periodizacao_ab.py      # Example: Periodization A/B
│   └── utils/
│       ├── logger.py               # Structured logging
│       └── retry.py                # Retry with backoff
└── tests/
    ├── test_validator.py
    └── test_mapper.py
```

### Exercise Mapping

Instead of hardcoded `if` chains, Iron Ledger uses intelligent fuzzy matching:

```
ExerciseMatcher
      ↓
  normalize()     → lowercase, strip equipment suffixes
      ↓
    score()       → SequenceMatcher similarity ratio
      ↓
  best_match()    → highest scoring template
      ↓
  template_id
```

Any exercise name from any program will be matched to the closest Hevy template automatically.

### Retry Strategy

API rate limits (`429`) are handled transparently:

```
Request failed (429)
      ↓
  Retry 1 → wait 1s
      ↓
  Retry 2 → wait 2s
      ↓
  Retry 3 → wait 4s
      ↓
  ...exponential backoff
```

## Running Tests

```bash
pytest tests/ -v
```

## Roadmap

- [ ] YAML importer
- [ ] JSON importer
- [ ] CSV importer
- [ ] Excel importer
- [ ] Progression calculator
- [ ] Exercise fuzzy matching improvements
- [ ] Dry-run mode with diff preview
- [ ] Interactive CLI
- [ ] Docker image
- [ ] GitHub Action
- [ ] PyPI package (`pip install iron-ledger`)

## License

[MIT](LICENSE)

---

<p align="center">
  <strong>Iron Ledger</strong> — Built with discipline. No shortcuts.
</p>