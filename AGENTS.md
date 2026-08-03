# Iron Ledger — Agent Context & Guidelines

> **Tagline:** *Every set. Every rep. Accounted for.*
> **Repository:** `iron-ledger`

---

## 1. Project Overview

**Iron Ledger** is a Python SDK and CLI tool designed to import, validate, and manage bodybuilding routines in the [Hevy](https://hevy.com) platform via the official Hevy API v1.

- **Primary Language:** Python 3.10+
- **Key Dependencies:** `requests`, `python-dotenv`, `pytest` (dev)
- **Target Audience:** Bodybuilders, powerlifters, and developers wanting programmatic workout routine management.

---

## 2. Core Philosophy & Design Principles

Adhere strictly to the following principles across all contributions:

- **SOLID & Clean Architecture:** Clear separation of concerns (API Client → Services → Domain Models → Importer → CLI).
- **Composition over Inheritance:** High modularity, zero rigid class hierarchies.
- **DRY & KISS & YAGNI:** Simplest implementation that works. No bloated DTOs, unnecessary Repositories, or over-engineered abstractions.
- **Boy Scout Rule:** Leave the codebase cleaner than you found it.
- **Explicit & Strongly Typed:** Type hints on all functions/methods (`dataclasses`, `typing`).
- **Fail Fast & Validate Early:** Program validation happens before making any network requests.

---

## 3. Project Structure & Architecture Map

```text
iron-ledger/
├── cli.py                          # CLI entry point (upload, --dry-run, --folder)
├── AGENTS.md                       # LLM & Developer guidelines (this file)
├── llms.txt                        # Concise project overview for LLMs
├── llms-full.txt                   # Complete project reference for LLMs
├── logo.png                        # Minimalist geometric logo
├── README.md                       # User-facing documentation
├── requirements.txt                # Production dependencies
│
├── iron_ledger/                    # Core Python Package
│   ├── __init__.py                 # Package metadata & version
│   ├── config.py                   # Environment configuration (load_config)
│   ├── constants.py                # API base URLs, Endpoints, RateLimits
│   ├── exceptions.py               # Custom exception hierarchy (IronLedgerError)
│   │
│   ├── api/                        # Hevy API Integration Layer
│   │   ├── __init__.py
│   │   ├── client.py               # HevyClient (HTTP, Auth, Retry, Pagination)
│   │   ├── routines.py             # RoutineService (GET/POST/PUT /v1/routines)
│   │   ├── folders.py              # FolderService (GET/POST /v1/routine_folders)
│   │   └── exercises.py            # ExerciseService (GET /v1/exercise_templates)
│   │
│   ├── domain/                     # Business Domain Layer
│   │   ├── __init__.py
│   │   ├── models.py               # Dataclasses: Routine, ExerciseSet, RoutineExercise, etc.
│   │   └── mapper.py               # ExerciseMatcher (3-pass fuzzy matching)
│   │
│   ├── importer/                   # Orchestration Layer
│   │   ├── __init__.py
│   │   ├── importer.py             # ProgramImporter (validate → folder → map → routine)
│   │   └── validator.py            # validate_program() (program schema & rules)
│   │
│   ├── workouts/                   # Workout Program Definitions
│   │   ├── __init__.py
│   │   ├── periodizacao_ab.py      # Periodização A/B (2-day program)
│   │   └── periodizacao_ab_ab_fullbody.py # Periodização 5 dias (AB-AB-FullBody)
│   │
│   └── utils/                      # Helper Utilities
│       ├── __init__.py
│       ├── logger.py               # Colored structured logging with checkmarks
│       └── retry.py                # Exponential backoff @with_retry decorator (429 handling)
│
└── tests/                          # Automated Tests
    ├── __init__.py
    ├── test_validator.py           # Program validation suite
    └── test_mapper.py              # Fuzzy exercise matcher suite
```

---

## 4. Git Commit Conventions (Conventional Commits + Gitmoji)

All commits in this repository MUST follow the **Conventional Commits** format paired with **Gitmoji**.

### Commit Format Structure

```text
<type>(<scope>): <gitmoji> <short summary>

[optional body]

[optional footer(s)]
```

### Commit Types & Corresponding Gitmojis

| Type | Scope Examples | Gitmoji | Description | Example |
| :--- | :--- | :---: | :--- | :--- |
| `feat` | `api`, `importer`, `cli`, `domain` | ✨ `:sparkles:` | New feature or capability | `feat(importer): ✨ add 5-day AB-AB-FullBody program` |
| `fix` | `mapper`, `client`, `validator` | 🐛 `:bug:` | Bug fix | `fix(mapper): 🐛 enforce 3-pass matching to prevent equipment mismatch` |
| `docs` | `readme`, `agents` | 📝 `:memo:` | Documentation updates | `docs(agents): 📝 add AGENTS.md and llms.txt context files` |
| `style` | `logger`, `formatting` | 💄 `:lipstick:` | Formatting, UI/logging tweaks | `style(logger): 💄 use colored output formatting` |
| `refactor` | `importer`, `client` | ♻️ `:recycle:` | Code restructuring without behavior change | `refactor(importer): ♻️ simplify folder ID extraction` |
| `test` | `validator`, `mapper` | ✅ `:white_check_mark:` | Adding or updating unit tests | `test(mapper): ✅ add tests for fuzzy exercise matching` |
| `chore` | `deps`, `config` | 🔧 `:wrench:` | Maintenance, configs, build scripts | `chore(deps): 🔧 update requirements.txt` |
| `init` | `repo` | 🎉 `:tada:` | Initial commit | `init(repo): 🎉 initialize Iron Ledger project structure` |

---

## 5. Development & Testing Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run unit tests
python -m pytest tests/ -v

# Run dry-run validation on a workout
python cli.py upload iron_ledger/workouts/periodizacao_ab_ab_fullbody.py --dry-run

# Run actual import into Hevy
python cli.py upload iron_ledger/workouts/periodizacao_ab_ab_fullbody.py --folder "Periodização AB-AB-FullBody (5 Dias)"
```

---

## 6. Guidelines for AI Agents

1. **Do not create bloated classes.** Use `@dataclass` and standalone functions where possible.
2. **Always validate before execution.** Never call the Hevy API without running `validate_program()` first.
3. **Handle Hevy API Rate Limits.** Wrap API methods with `@with_retry` decorator.
4. **Preserve English exercise template names in workouts** so fuzzy matching against Hevy API reaches 1.00 score. Keep notes and instructions in Portuguese as written by users.
5. **Write unit tests** whenever adding new validation rules or domain logic.
