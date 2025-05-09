import re
from collections import defaultdict

async def normalize(tokens):
    freq_map = defaultdict(int)
    
    for word in tokens:
        if not word:
            continue
        freq_map[word] += 1
    
    unique_list_of_words = [
        {'data': word.lower(), 'count': count}
        for word, count in freq_map.items()
        if re.fullmatch(r'^[A-Za-z]+$', word)
    ]
    
    unique_list_of_words.sort(key=lambda x: x['count'], reverse=True)
    
    return unique_list_of_words

__all__ = ['normalize']