import re
import aiofiles
from bs4 import BeautifulSoup

async def remove_markup(filename):
    # Read file asynchronously
    async with aiofiles.open(filename, 'r', encoding='utf-8') as f:
        text_with_markup = await f.read()
    
    initial_total_length = len(text_with_markup)
    
    # Parse HTML
    soup = BeautifulSoup(text_with_markup, 'html.parser')
    
    # Get text content
    cleaned_text = soup.get_text()
    
    # Apply cleaning transformations
    cleaned_text = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = re.sub(
        r'\b(const|let|var|function|return|if|else|for|while|switch|case|break|true|false|null|undefined|async|await|import|export|class|new|this|try|catch|finally|throw)\b',
        '', cleaned_text)
    cleaned_text = re.sub(r'[{}[\]();:=<>!~&|,+*/%^)(-]', '', cleaned_text)
    cleaned_text = cleaned_text.strip()
    
    return {
        'initialLength': initial_total_length,
        'cleanedLength': len(cleaned_text),
        'cleanedText': cleaned_text
    }
