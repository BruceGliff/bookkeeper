"""
"""

from dataclasses import dataclass


@dataclass
class Budget:
    period: int
    category: int
    amount: int
    pk: int = 0
