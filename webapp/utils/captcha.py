"""Simple arithmetic captcha generation & validation."""
from __future__ import annotations
import random


def generate_captcha(min_n: int = 1, max_n: int = 9) -> tuple[str, str]:
    a = random.randint(min_n, max_n)
    b = random.randint(min_n, max_n)
    question = f"What is {a} + {b}?"
    answer = str(a + b)
    return question, answer


def validate_captcha(provided: str, expected: str) -> bool:
    return provided.strip() == expected.strip()
