from collections import Counter
import re
from builtins import sum,len,any,round


def extract_keywords(text, num_keywords=8):
    """
    Extract most important keywords from research paper text
    
    Args:
        text (str): The text to extract keywords from
        num_keywords (int): Number of keywords to return (default: 8)
    
    Returns:
        list: List of extracted keywords
    """
    
    # Clean the text first
    text = clean_text(text)
    
    # Search in first 15000 characters (where keywords usually are)
    search_text = text[:15000].lower()
    
    # Remove citation numbers like [1], [2,3]
    search_text = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', search_text)
    
    # Remove ORCID and other IDs
    search_text = re.sub(r'\[\d{4}[-–]\d{4}[-–]\d{4}[-–]\d{4}\]', '', search_text)
    
    # Extract words (minimum 4 characters, only alphabetic)
    words = re.findall(r'\b[A-Za-z]{4,}\b', search_text)
    
    # Comprehensive stopwords list for academic text
    stopwords = {
        # Common English stopwords
        'a', 'an', 'the', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 'to', 'by',
        'in', 'of', 'with', 'without', 'about', 'after', 'before', 'between', 'among',
        'through', 'during', 'within', 'without', 'upon', 'toward', 'under', 'over',
        
        # Pronouns and demonstratives
        'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their',
        'we', 'our', 'us', 'you', 'your', 'he', 'him', 'his', 'she', 'her',
        'who', 'whom', 'whose', 'which', 'what', 'where', 'when', 'why', 'how',
        
        # Academic writing common words
        'paper', 'research', 'study', 'analysis', 'results', 'findings',
        'method', 'methods', 'approach', 'approaches', 'technique', 'techniques',
        'model', 'models', 'system', 'systems', 'data', 'information',
        'knowledge', 'understanding', 'insight', 'insights',
        'proposed', 'developed', 'presented', 'described', 'discussed',
        'shown', 'found', 'observed', 'noted', 'indicated', 'suggested',
        'demonstrated', 'evaluated', 'assessed', 'examined', 'investigated',
        'explored', 'analyzed', 'measured', 'calculated', 'estimated',
        
        # Transitional and connecting words
        'therefore', 'however', 'moreover', 'furthermore', 'additionally',
        'consequently', 'accordingly', 'thus', 'hence', 'thereby', 'thereafter',
        'nonetheless', 'nevertheless', 'conversely', 'similarly', 'likewise',
        'meanwhile', 'subsequently', 'ultimately', 'finally', 'overall',
        
        # Verbs commonly used in abstracts
        'using', 'based', 'used', 'use', 'using', 'utilized', 'applied',
        'performed', 'conducted', 'carried', 'implemented', 'designed',
        'tested', 'trained', 'validated', 'verified', 'confirmed',
        
        # Academic adverbs and adjectives
        'very', 'quite', 'rather', 'somewhat', 'relatively', 'comparatively',
        'substantially', 'significantly', 'considerably', 'remarkably',
        'particularly', 'especially', 'specifically', 'generally', 'typically',
        'commonly', 'frequently', 'often', 'usually', 'sometimes',
        'different', 'various', 'multiple', 'several', 'many', 'much',
        'more', 'most', 'least', 'less', 'greater', 'better', 'worse',
        
        # Numbers and quantifiers
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
        'first', 'second', 'third', 'fourth', 'fifth', 'last', 'next', 'previous',
        
        # Other common words
        'also', 'well', 'even', 'ever', 'never', 'always', 'often', 'sometimes',
        'currently', 'recently', 'previously', 'previously', 'early', 'late',
        'real', 'true', 'false', 'possible', 'potential', 'likely', 'unlikely',
        'important', 'essential', 'critical', 'crucial', 'vital', 'significant',
        'major', 'minor', 'main', 'primary', 'secondary', 'key', 'core', 'central',
        'preliminary', 'initial', 'final', 'ultimate', 'overall', 'general',
        'specific', 'particular', 'certain', 'clear', 'obvious', 'apparent',
        'further', 'additional', 'extra', 'supplementary', 'complementary',
        'related', 'associated', 'connected', 'linked', 'correlated',
        'common', 'typical', 'standard', 'conventional', 'traditional',
        'modern', 'contemporary', 'current', 'emerging', 'novel', 'new',
        'old', 'former', 'latter', 'previous', 'subsequent', 'following',
        
        # Months and days (sometimes appear in dates)
        'january', 'february', 'march', 'april', 'may', 'june', 'july',
        'august', 'september', 'october', 'november', 'december',
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
        
        # Common abbreviations
        'e', 'g', 'i', 'e', 'vs', 'cf', 'et', 'al', 'fig', 'figs', 'eq', 'eqs',
        'sec', 'secs', 'chap', 'chaps', 'app', 'apps', 'ref', 'refs',
        
        # Additional stopwords from your previous list
        'using', 'which', 'these', 'based', 'method', 'this', 'that', 'with',
        'from', 'have', 'were', 'will', 'analysis', 'study', 'results', 'proposed',
        'approach', 'experiments', 'section', 'also', 'used', 'for', 'are', 'but',
        'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out',
        'than', 'their', 'they', 'were', 'which', 'will', 'with', 'would',
        'about', 'after', 'because', 'been', 'before', 'between', 'both',
        'could', 'during', 'even', 'first', 'from', 'into', 'more', 'most',
        'such', 'than', 'that', 'then', 'these', 'they', 'this', 'those',
        'through', 'until', 'when', 'where', 'while', 'within', 'without',
        'among', 'other', 'many', 'much', 'some', 'however', 'therefore',
        'hence', 'thereby', 'thus', 'despite', 'although', 'though',
        'information', 'understanding', 'framework', 'methodology',
        'experimental', 'evaluation', 'performance', 'accuracy', 'precision',
        'recall', 'score', 'error', 'rate', 'time', 'cost', 'efficiency',
        'effective', 'efficient', 'reliable', 'robust', 'stable', 'consistent'
    }
    
    # Filter out stopwords and short words
    filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
    
    # Count frequencies
    keyword_counts = Counter(filtered_words)
    
    # Get most common keywords
    most_common = keyword_counts.most_common(num_keywords * 2)
    
    # Filter out words that appear only once
    keywords = [word for word, count in most_common if count > 1]
    
    # Return only the requested number
    return keywords[:num_keywords] if keywords else ["Keywords not found"]

def clean_text(text):
    """
    Clean the text before keyword extraction
    
    Args:
        text (str): Raw text to clean
    
    Returns:
        str: Cleaned text
    """
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep words
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra spaces again
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def extract_keywords_from_abstract(text, num_keywords=5):
    """
    Extract keywords specifically from abstract section
    
    Args:
        text (str): Full text
        num_keywords (int): Number of keywords to return
    
    Returns:
        list: Keywords from abstract
    """
    
    # Try to find abstract section
    abstract_match = re.search(r'(?i)abstract\s*(.*?)(?=\n\s*[A-Z][A-Z\s]+:|Introduction|1\.|Keywords|$)', text, re.DOTALL)
    
    if abstract_match:
        abstract_text = abstract_match.group(1).strip()
        return extract_keywords(abstract_text, num_keywords)
    
    return []

def extract_keywords_from_title(text, num_keywords=3):
    """
    Extract keywords specifically from title
    
    Args:
        text (str): Full text
        num_keywords (int): Number of keywords to return
    
    Returns:
        list: Keywords from title
    """
    
    # Try to find title (first 10 lines)
    lines = text.split('\n')
    for line in lines[:10]:
        line = line.strip()
        if len(line) > 20 and len(line) < 300:
            skip_words = ['abstract', 'introduction', 'keywords', 'references', 
                         'fig', 'table', 'figure', 'acknowledgment', 'author', 
                         'affiliation', 'university', 'institute', 'email']
            if not any(word in line.lower() for word in skip_words):
                if re.search(r'[A-Z]', line):
                    return extract_keywords(line, num_keywords)
    
    return []

def get_keywords_with_weights(text, num_keywords=8):
    """
    Extract keywords with importance weights
    
    Args:
        text (str): Full text
        num_keywords (int): Number of keywords to return
    
    Returns:
        list: List of (keyword, weight) tuples
    """
    
    # Clean text
    text = clean_text(text)
    search_text = text[:15000].lower()
    search_text = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', search_text)
    
    # Extract words
    words = re.findall(r'\b[A-Za-z]{4,}\b', search_text)
    
    # Stopwords (same as above)
    stopwords = {
        'paper', 'research', 'study', 'analysis', 'results', 'findings',
        'method', 'methods', 'approach', 'approaches', 'technique', 'techniques',
        'model', 'models', 'system', 'systems', 'data', 'information',
        'proposed', 'developed', 'presented', 'described', 'discussed',
        'shown', 'found', 'observed', 'noted', 'indicated', 'suggested',
        'using', 'based', 'used', 'use', 'using', 'utilized', 'applied',
        'therefore', 'however', 'moreover', 'furthermore', 'additionally',
        'also', 'well', 'even', 'ever', 'never', 'always', 'often',
        'one', 'two', 'three', 'four', 'five', 'first', 'second', 'third',
        'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them',
        'we', 'our', 'us', 'you', 'your', 'he', 'him', 'his', 'she', 'her',
        'who', 'whom', 'whose', 'which', 'what', 'where', 'when', 'why'
    }
    
    # Filter words
    filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
    
    # Count frequencies
    keyword_counts = Counter(filtered_words)
    
    # Get total count for normalization
    total_words = sum(keyword_counts.values())
    
    # Calculate weights (tf-idf like)
    weighted_keywords = []
    for word, count in keyword_counts.items():
        weight = count / total_words if total_words > 0 else 0
        weighted_keywords.append((word, weight))
    
    # Sort by weight
    weighted_keywords.sort(key=lambda x: x[1], reverse=True)
    
    # Filter out words with very low weight
    weighted_keywords = [(w, round(wt, 4)) for w, wt in weighted_keywords[:num_keywords] if wt > 0.01]
    
    return weighted_keywords if weighted_keywords else [("Keywords not found", 0)]