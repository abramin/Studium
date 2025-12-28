#!/usr/bin/env python3
"""
Validation script to check the project setup.
This can be run before building Docker images or starting the application.
"""

import ast
import sys
from pathlib import Path


def validate_python_syntax():
    """Validate Python files have correct syntax."""
    print("🔍 Validating Python syntax...")
    python_files = [
        "app/main.py",
        "app/config.py",
        "app/database.py",
        "app/celery_worker.py",
        "app/__init__.py",
        "tests/test_api.py",
    ]
    
    errors = []
    for filepath in python_files:
        try:
            with open(filepath, 'r') as f:
                ast.parse(f.read())
            print(f"  ✓ {filepath}")
        except SyntaxError as e:
            errors.append(f"Syntax error in {filepath}: {e}")
            print(f"  ✗ {filepath}: {e}")
    
    return len(errors) == 0, errors


def validate_yaml():
    """Validate YAML files."""
    print("\n🔍 Validating YAML files...")
    try:
        import yaml
        with open("docker-compose.yml", 'r') as f:
            yaml.safe_load(f)
        print("  ✓ docker-compose.yml")
        return True, []
    except Exception as e:
        error = f"Invalid YAML in docker-compose.yml: {e}"
        print(f"  ✗ {error}")
        return False, [error]


def validate_toml():
    """Validate TOML files."""
    print("\n🔍 Validating TOML files...")
    try:
        import tomllib
        with open("pyproject.toml", 'rb') as f:
            tomllib.load(f)
        print("  ✓ pyproject.toml")
        return True, []
    except Exception as e:
        error = f"Invalid TOML in pyproject.toml: {e}"
        print(f"  ✗ {error}")
        return False, [error]


def validate_required_files():
    """Check all required files exist."""
    print("\n🔍 Checking required files...")
    required_files = [
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "app/main.py",
        "app/config.py",
        "app/database.py",
        "app/celery_worker.py",
        "init-db.sql",
    ]
    
    missing = []
    for filepath in required_files:
        if Path(filepath).exists():
            print(f"  ✓ {filepath}")
        else:
            missing.append(filepath)
            print(f"  ✗ {filepath} - MISSING")
    
    return len(missing) == 0, missing


def validate_directory_structure():
    """Check directory structure."""
    print("\n🔍 Checking directory structure...")
    required_dirs = [
        "app",
        "app/ingestion",
        "app/retrieval",
        "app/tutor",
        "app/quiz",
        "app/mastery",
        "app/eval",
        "tests",
        "docs",
    ]
    
    missing = []
    for dirpath in required_dirs:
        if Path(dirpath).is_dir():
            print(f"  ✓ {dirpath}/")
        else:
            missing.append(dirpath)
            print(f"  ✗ {dirpath}/ - MISSING")
    
    return len(missing) == 0, missing


def main():
    """Run all validations."""
    print("=" * 60)
    print("Studium Project Setup Validation")
    print("=" * 60)
    
    all_passed = True
    all_errors = []
    
    # Run validations
    checks = [
        validate_required_files,
        validate_directory_structure,
        validate_python_syntax,
        validate_yaml,
        validate_toml,
    ]
    
    for check in checks:
        passed, errors = check()
        if not passed:
            all_passed = False
            all_errors.extend(errors)
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All validations passed!")
        print("\nNext steps:")
        print("  1. Copy .env.example to .env and configure")
        print("  2. Run: docker compose up -d")
        print("  3. Visit: http://localhost:8000/docs")
        return 0
    else:
        print("❌ Some validations failed:")
        for error in all_errors:
            print(f"  - {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
