from fuzzywuzzy import process

def oversæt_fuzzy(navn, kandidater):
    navn = navn.lower()
    result = process.extractOne(navn, kandidater, score_cutoff=70)
    return result[0] if result else navn