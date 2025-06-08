
from rapidfuzz import process

def oversæt_fuzzy(navn, kandidater):
    match = process.extractOne(navn, kandidater, score_cutoff=70)
    if match:
        return match[0]
    return navn
