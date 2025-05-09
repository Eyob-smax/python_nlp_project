from pathlib import Path
from typing import Dict, List
from text_processing_tokenize import tokenize
from normalize import normalize
from stemmer import stemmer_algo
from stop_words import stopping_words
from markup import remove_markup

async def get_index(document: str) -> Dict[str, object]:
    markup_result = await remove_markup(document)
    initial_length = markup_result['initialLength']
    cleaned_length = markup_result['cleanedLength']
    cleaned_text = markup_result['cleanedText']
    
    pathfile = "./documents/markupFreeText.txt"
    Path(pathfile).write_text(cleaned_text, encoding='utf-8')
    
    tokenized_array =  tokenize(pathfile)
    normalized_array = await normalize(tokenized_array)
    remove_stop_words = await stopping_words(normalized_array)
    stemmed_array = await stemmer_algo(remove_stop_words)
    
    most_frequent = stemmed_array[0]['count']
    least_frequent = stemmed_array[-1]['count']
    
    index_string = construct_index(least_frequent, stemmed_array, most_frequent)
    
    return {
        'initialLength': initial_length,
        'totalReducedLength': initial_length - len(index_string),
        'finalLength': len(index_string),
        'indexString': index_string
    }

def analyse_statistics(
    stemmed_array: List[Dict[str, object]],
    initial_char_length: int,
    final_length_after_markup_removal: int
) -> None:
    print("📊 Analyzing Text Statistics...")
    print("--------------------------------------------------")
    print(f"✍️ Initial Character Length: {initial_char_length}")
    print(f"🧹 Final Length After Markup Removal: {final_length_after_markup_removal}")
    print(f"🔢 Total Words After Stemming: {len(stemmed_array)}")
    print("--------------------------------------------------")

    reduction = initial_char_length - final_length_after_markup_removal
    reduction_percentage = (reduction / initial_char_length) * 100

    print(f"📉 Reduction in Length: {reduction} characters")
    print(f"📊 Reduction Percentage: {reduction_percentage:.2f}%")
    print("✅ Analysis Complete.")

def construct_index(
    lower_cut_off: int,
    stemmed_array: List[Dict[str, object]],
    upper_cut_off: int
) -> str:
    stripped_string = " ".join(
        word['data'] for word in stemmed_array
        if lower_cut_off < word['count'] < upper_cut_off
    )
    return stripped_string

__all__ = ['get_index']