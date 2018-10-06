"""Contains types for type hinting.

@since 0.1.0
"""

from typing import List, Tuple

Chromosome = List[int]
Eval = Tuple[Chromosome, float]
Parents = Tuple[Chromosome, Chromosome]