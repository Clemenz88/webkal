from fuzzywuzzy import process

def oversæt_fuzzy(navn, kandidater):
    match, score = process.extractOne(navn, kandidater)
    if score >= 70:
        return match
    return None