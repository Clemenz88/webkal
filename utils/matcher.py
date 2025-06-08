from fuzzywuzzy import process

def oversæt_fuzzy(navn, kandidater):
    match, score = process.extractOne(navn, kandidater)
    return match if score >= 70 else navn