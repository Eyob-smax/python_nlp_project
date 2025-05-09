def tokenize(markup_cleaned_file):
    with open(markup_cleaned_file, 'r', encoding='utf-8') as file:
        text = file.read()
    tokenized_text = text.split(' ')
    return tokenized_text

__all__ = ['tokenize']