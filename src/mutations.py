import random
from typing import List


DNA_BASES = ("A", "C", "G", "T")

def random_base(exclude=None):
    """Return a random DNA base, optionally excluding one base."""
    choices = [b for b in DNA_BASES if b != exclude]
    return random.choice(choices)

def mutate_seq(seq:List, n_mutations=5, seed=8):
    """
    Apply exactly n_mutations at random positions in the sequence.
    Each mutation changes only one base at a time:
      - substitution: replace 1 base
      - deletion: remove 1 base
      - insertion: insert 1 base
    Returns (mutated Seq, mutation log)
    """
    if seed is not None:
        random.seed(seed)

    mutated = str(seq)
    log = []

    for _ in range(n_mutations):
        if len(mutated) == 0:
            mtype = "insertion"
        else:
            mtype = random.choice(["substitution", "deletion", "insertion"])

        pos = random.randrange(len(mutated) + (1 if mtype == "insertion" else 0))

        if mtype == "substitution":
            old = mutated[pos]
            new = random_base(exclude=old)
            mutated = mutated[:pos] + new + mutated[pos+1:]
            log.append({"type": "substitution", "pos": pos, "old": old, "new": new})

        elif mtype == "deletion":
            deleted = mutated[pos]
            mutated = mutated[:pos] + mutated[pos+1:]
            log.append({"type": "deletion", "pos": pos, "deleted": deleted})

        else:  # insertion
            insert_base = random_base()
            mutated = mutated[:pos] + insert_base + mutated[pos:]
            log.append({"type": "insertion", "pos": pos, "inserted": insert_base})

    return mutated, log