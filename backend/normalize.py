import re
from collections import defaultdict

async def normalize(tokens):
    freq_map = defaultdict(int)
    
    # Count word frequencies
    for word in tokens:
        if not word:
            continue
        freq_map[word] += 1
    
    # Process and filter words
    unique_list_of_words = [
        {'data': word.lower(), 'count': count}
        for word, count in freq_map.items()
        if re.fullmatch(r'^[A-Za-z]+$', word)
    ]
    
    # Sort by count in descending order
    unique_list_of_words.sort(key=lambda x: x['count'], reverse=True)
    
    return unique_list_of_words

# For Python module export
__all__ = ['normalize']