import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

def generate_distractors(word: str, count: int = 3) -> list[str]:
    """Generate a list of distractor words by altering the input word."""
    word = word.lower()
    candidates = set()

    # Vowel swaps
    for i, c in enumerate(word):
        if c in VOWELS: 
            for v in VOWELS:
                if v != c: 
                    candidates.add(word[:i] + v + word[i+1:])

    # Drop a letter
    for i in range(len(word)):
        candidates.add(word[:i] + word[i+1:])
    
    # Double a letter
    for i in range(len(word)):
        candidates.add(word[:i] + word[i] + word[i:])

    # Remove a double letter
    for i in range(len(word) - 1):
        if word[i] == word[i + 1]:
            candidates.add(word[:i] + word[i+1:])
    
    # Common phonetic substitutions
    PHONETIC_SWAPS = {
        'ph': 'f',
        'f': 'ph',
        'c': 'k',
        'k': 'c',
        's': 'z',
        'z': 's',
        'j': 'g',
        'g': 'j',
        'q': 'k',
        'x': 'ks',
        'ks': 'x',
        'ei': 'ie',
        'ie': 'ei',
        's': 'c',
        'c': 'ck',
        'ck': 'c'
    }

    for src, tgt in PHONETIC_SWAPS.items():
        if src in word:
            candidates.add(word.replace(src, tgt, 1))

    # Cleanup
    candidates.discard(word)
    candidates = {c for c in candidates if len(c) >= 3}

    # Gurantee output
    candidates = list(candidates)
    random.shuffle(candidates)

    if len(candidates) < count: 
        # Fallback: random mutations
        while len(candidates) < count:
            i = random.randint(0, len(word) - 1)
            candidates.append(word[:i] + random.choice(VOWELS) + word[i+1:])

    return candidates[:count]