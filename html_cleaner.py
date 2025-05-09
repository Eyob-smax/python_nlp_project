from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import re
import os
import ssl
from pathlib import Path
import string

# ======================
# INITIAL SETUP
# ======================

def configure_ssl():
    """Handle SSL certificate issues for NLTK downloads"""
    try:
        _create_unverified_https_context = ssl._create_unverified_context
        ssl._create_default_https_context = _create_unverified_https_context
    except AttributeError:
        pass

def setup_nltk_resources():
    """Ensure all required NLTK data packages are available"""
    required_resources = {
        'punkt': 'tokenizers/punkt',
        'punkt_tab': 'tokenizers/punkt_tab',
        'stopwords': 'corpora/stopwords',
        'wordnet': 'corpora/wordnet',
        'omw-1.4': 'corpora/omw-1.4'
    }

    for package, path in required_resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            print(f"⏳ Downloading NLTK '{package}' resource...")
            try:
                nltk.download(package, quiet=False)
            except Exception as e:
                print(f"❌ Failed to download '{package}': {str(e)}")
                print(f"Please try manually: python -m nltk.downloader {package}")
                exit(1)

# ======================
# TEXT PROCESSING FUNCTIONS
# ======================

def clean_html(file_path):
    """Remove all HTML/JS/CSS markup and return clean text"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        print("\n=== HTML CLEANING ===")
        print("Removing scripts, styles, and markup...")
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove unwanted elements
        for tag in soup(["script", "style", "noscript", "iframe", "meta", "link", "header", "footer"]):
            tag.decompose()
        
        # Remove all attributes and comments
        for tag in soup.find_all():
            tag.attrs = {}
        
        # Get clean text with improved whitespace handling
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove special chars
        clean_text = re.sub(r'\s+', ' ', text).strip()
        
        print(f"Original length: {len(html)} characters")
        print(f"Cleaned length: {len(clean_text)} characters")
        return clean_text
    except Exception as e:
        raise RuntimeError(f"HTML cleaning failed: {str(e)}")

def normalize_text(text):
    """Normalize text (lowercase, remove punctuation/numbers)"""
    print("\n=== TEXT NORMALIZATION ===")
    print("Converting to lowercase, removing punctuation/numbers...")
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    print(f"Normalized length: {len(text)} characters")
    return text

def tokenize_text(text):
    """Tokenize text into words"""
    print("\n=== TOKENIZATION ===")
    tokens = word_tokenize(text)
    print(f"Generated {len(tokens)} tokens")
    print("Sample tokens:", tokens[:10])
    return tokens

def remove_stopwords(tokens):
    """Remove stopwords from tokens"""
    print("\n=== STOPWORD REMOVAL ===")
    stop_words = set(stopwords.words('english'))
    initial_count = len(tokens)
    filtered = [word for word in tokens if word not in stop_words]
    
    print(f"Removed {initial_count - len(filtered)} stopwords")
    print(f"Remaining tokens: {len(filtered)}")
    print("Sample remaining:", filtered[:10])
    return filtered

def stem_words(tokens):
    """Apply Porter stemming to tokens"""
    print("\n=== STEMMING ===")
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(word) for word in tokens]
    print("Sample stemmed tokens:", stemmed[:10])
    return stemmed

def lemmatize_words(tokens):
    """Apply WordNet lemmatization to tokens"""
    print("\n=== LEMMATIZATION ===")
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    print("Sample lemmatized tokens:", lemmatized[:10])
    return lemmatized

# ======================
# MAIN EXECUTION
# ======================

def main():
    # Initial configuration
    configure_ssl()
    setup_nltk_resources()
    
    # File handling
    documents_dir = Path('documents')
    input_file = documents_dir / 'test.html'
    
    if not input_file.exists():
        print(f"❌ Error: Missing input file at {input_file.resolve()}")
        print("Please create the 'documents' folder and add 'test.html'")
        return
    
    try:
        print("\n🔍 Starting text processing pipeline 🔍")
        
        # 1. HTML Cleaning
        clean_text = clean_html(input_file)
        print("\n=== CLEANED TEXT (TRUNCATED) ===")
        print(clean_text[:200] + ("..." if len(clean_text) > 200 else ""))
        
        # 2. Normalization
        normalized_text = normalize_text(clean_text)
        
        # 3. Tokenization
        tokens = tokenize_text(normalized_text)
        
        # 4. Stopword Removal
        filtered_tokens = remove_stopwords(tokens)
        
        # 5. Stemming/Lemmatization
        print("\n=== CHOOSING STEMMING OR LEMMATIZATION ===")
        choice = input("Use lemmatization? (y/n, default=y): ").lower()
        if choice.startswith('n'):
            processed_tokens = stem_words(filtered_tokens)
            method = "stemmed"
        else:
            processed_tokens = lemmatize_words(filtered_tokens)
            method = "lemmatized"
        
        # Final output
        print("\n=== FINAL PROCESSED TOKENS ===")
        print(f"Total {method} tokens: {len(processed_tokens)}")
        print("Sample tokens:", processed_tokens[:20])
        
        # Save results
        output_file = documents_dir / 'processed_output.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== {method.upper()} TOKENS ===\n")
            f.write("\n".join(processed_tokens))
        
        print(f"\n✅ Results saved to {output_file.resolve()}")
        
    except Exception as e:
        print(f"\n❌ Processing Error: {str(e)}")

if __name__ == '__main__':
    main()