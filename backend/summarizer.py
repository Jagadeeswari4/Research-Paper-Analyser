import re
from builtins import len,any
def generate_summary(text, max_sentences=4):
    """Generate clean summary"""
    
    text = fix_text(text)
    text = re.sub(r'\s+', ' ', text)
    
    abstract_match = re.search(r'(?i)abstract\s*(.*?)(?=\n\s*[A-Z][A-Z\s]+:|Introduction|1\.|Keywords|$)', text, re.DOTALL)
    
    if abstract_match:
        abstract_text = abstract_match.group(1).strip()
        abstract_text = fix_text(abstract_text)
        abstract_text = re.sub(r'\s+', ' ', abstract_text)
        abstract_text = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', abstract_text)
        
        sentences = get_clean_sentences(abstract_text)
        if sentences:
            return '. '.join(sentences[:max_sentences])
    
    intro_match = re.search(r'(?i)introduction\s*(.*?)(?=\n\s*[A-Z][A-Z\s]+:|2\.|Related Work|Background|$)', text, re.DOTALL)
    if intro_match:
        intro_text = intro_match.group(1).strip()
        intro_text = fix_text(intro_text)
        intro_text = re.sub(r'\s+', ' ', intro_text)
        intro_text = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', intro_text)
        
        sentences = get_clean_sentences(intro_text)
        if sentences:
            return '. '.join(sentences[:max_sentences])
    
    sentences = get_clean_sentences(text)
    if sentences:
        return '. '.join(sentences[:max_sentences])
    
    return "Summary not available"

def fix_text(text):
    """Fix text issues"""
    text = re.sub(r'(\w+)-(\w+)', r'\1\2', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    fixes = [
        ('speechrecognition', 'speech recognition'),
        ('recognitionin', 'recognition in'),
        ('robotsanddiscuss', 'robots and discuss'),
        ('robustspeech', 'robust speech'),
        ('deployingrobust', 'deploying robust'),
        ('futuredirections', 'future directions'),
        ('multimodalinter', 'multimodal inter'),
        ('sysystems', 'systems'),
        ('recognotion', 'recognition'),
        ('rea-lly', 'really'),
        ('discussfuture', 'discuss future'),
        ('recog-', 'recognition '),
        ('speechrecog', 'speech recog'),
        ('robotsand', 'robots and'),
        ('outlinethechallenges', 'outline the challenges'),
    ]
    
    for wrong, correct in fixes:
        text = text.replace(wrong, correct)
    
    text = re.sub(r'(\w+)(recognition)', r'\1 recognition', text)
    text = re.sub(r'(\w+)(robots)', r'\1 robots', text)
    text = re.sub(r'(\w+)(discuss)', r'\1 discuss', text)
    text = re.sub(r'(\w+)(future)', r'\1 future', text)
    text = re.sub(r'(\w+)(speech)', r'\1 speech', text)
    
    return text

def get_clean_sentences(text):
    """Get clean sentences"""
    sentences = re.split(r'[.!?]+', text)
    
    clean_sentences = []
    for s in sentences:
        s = s.strip()
        if len(s) > 30 and s[0].isupper():
            bad_starters = ['and', 'with', 'of', 'for', 'in', 'on', 'at', 
                           'by', 'from', 'to', 'which', 'where', 'when',
                           'whose', 'whom', 'that', 'as', 'but', 'or', 
                           'yet', 'so', 'because', 'since', 'unless',
                           'although', 'while', 'whereas', 'however']
            if not any(s.lower().startswith(starter) for starter in bad_starters):
                clean_sentences.append(s)
    
    return clean_sentences