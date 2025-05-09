import re
from typing import List, Dict

async def stemmer_algo(array_without_stop_words: List[Dict[str, object]]) -> List[Dict[str, object]]:
    stemmed_array = [{'data': stem_word(word['data']), 'count': word['count']} 
                    for word in array_without_stop_words]
    return stemmed_array

def stem_word(word: str) -> str:
    exceptions = {
        "sky", "news", "how", "new", "now", "know", "able", "age", "ago", "air",
        "all", "and", "any", "are", "art", "ask", "ate", "bad", "bag", "ban",
        # ... (rest of your exceptions list)
        "fish", "aircraft", "series", "species"
    }

    if word in exceptions:
        return word

    prefixes = [
        "over", "under", "after", "inter", "super", "trans", "hyper", "semi",
        "anti", "multi", "mis", "dis", "non", "pre", "re", "un", "in", "im",
        "il", "ir"
    ]

    suffixes = [
        "s", "es", "ies", "ed", "ing", "ly", "er", "or", "ness", "ment",
        "tion", "ation", "ity", "able", "ible", "ship", "hood", "dom", "ism",
        "ist", "ity", "al", "ial", "ing", "ance", "ence", "ful", "less", "ous",
        "ization", "ational", "fulness", "iveness"
    ]

    if word.endswith("ss") or word.endswith("us"):
        return word

    # Handle prefixes
    for prefix in prefixes:
        if word.startswith(prefix) and len(word) > len(prefix) + 2:
            stem = word[len(prefix):]
            if len(stem) >= 2 and re.fullmatch(r'[a-z]{2,}', stem):
                if stem not in exceptions:
                    word = stem
                    break

    # Handle suffixes
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            stem = word[:-len(suffix)]
            if len(stem) >= 2 and re.fullmatch(r'[a-z]{2,}', stem):
                if stem not in exceptions:
                    word = stem
                    break

    # Handle double letters
    if re.search(r'([a-z])\1$', word):
        word = word[:-1]

    # Handle 'i' ending
    if word.endswith("i") and len(word) > 3:
        word = word[:-1] + "y"

    if len(word) < 3 or word in exceptions:
        return word

    return word

# For Python module export
__all__ = ['stemmer_algo']