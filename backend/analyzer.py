import re
from collections import Counter
from builtins import len,any,bool,int,enumerate,all

def analyze_paper(text):
    cleaned_text = fix_all_text(text)

    return {
        "title": extract_title(cleaned_text),
        "publication_year": extract_year(cleaned_text),
        "research_domain": detect_domain(cleaned_text),
        "abstract_summary": extract_abstract(cleaned_text),
        "keywords": extract_keywords(cleaned_text),
        "methodology": extract_methodology(cleaned_text),
        "algorithms_used": extract_algorithms(cleaned_text),
        "dataset_information": extract_dataset(cleaned_text),
        "results": extract_results(cleaned_text),
        "advantages": extract_advantages(cleaned_text),
        "future_scope": extract_future_scope(cleaned_text),
    }

def fix_merged_words(text):
    """Fix words that are merged together without spaces"""
    
    fixes = {
        'speechrecognition': 'speech recognition',
        'speechrecognation': 'speech recognition',
        'recognation': 'recognition',
        'recognotion': 'recognition',
        'recognitionin': 'recognition in',
        'recognitioninrobots': 'recognition in robots',
        'robotsand': 'robots and',
        'robotsanddiscuss': 'robots and discuss',
        'robustspeech': 'robust speech',
        'deployingrobust': 'deploying robust',
        'futuredirections': 'future directions',
        'multimodalinter': 'multimodal interaction',
        'sysystems': 'systems',
        'outlinethechallenges': 'outline the challenges',
        'discussfuture': 'discuss future',
        'humanrobot': 'human-robot',
        'cloudbased': 'cloud-based',
        'rosbased': 'ROS-based',
        'realworld': 'real-world',
        'weoutline': 'we outline',
        'anddiscuss': 'and discuss',
        'includingmultimodal': 'including multimodal',
        'interactionaction': 'interaction action',
        'interactionin': 'interaction in',
        'challengesof': 'challenges of',
        'languagebased': 'language-based',
        'realworldrobotic': 'real-world robotic',
        'roboticplat': 'robotic platforms',
        'formsin': 'forms in',
    }
    
    for wrong, correct in fixes.items():
        text = text.replace(wrong, correct)
        text = text.replace(wrong.title(), correct.title())
    
    # Do not guess word boundaries with broad regexes: they can corrupt valid
    # words such as "domain" and "information".  Use only known repairs.
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    return text

def fix_all_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)
    text = fix_merged_words(text)

    fixes = {
        "speechrecognition": "speech recognition",
        "recognation": "recognition",
        "recognotion": "recognition",
        "recognitionin": "recognition in",
        "robotsand": "robots and",
        "robustspeech": "robust speech",
        "futuredirections": "future directions",
        "multimodalinter": "multimodal interaction",
        "sysystems": "systems",
        "outlinethechallenges": "outline the challenges",
        "deployingrobust": "deploying robust",
        "discussfuture": "discuss future",
        "humanrobot": "human-robot",
        "cloudbased": "cloud-based",
        "rosbased": "ROS-based",
        "realworld": "real-world",
        "weoutline": "we outline",
        "anddiscuss": "and discuss",
    }

    for wrong, correct in fixes.items():
        text = re.sub(wrong, correct, text, flags=re.IGNORECASE)

    # Preserve newlines so title, author, and affiliation lines stay separate.
    text = re.sub(r"[ \t\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()

def _extract_title_legacy(text):
    """Extract ONLY the paper title - Remove author names, ORCID, numbers"""
    text = fix_all_text(text)
    lines = text.split('\n')
    
    skip_words = [
        "abstract", "introduction", "keywords", "references", 
        "conclusion", "acknowledgment", "appendix",
        "university", "institute", "college", "school", "department",
        "science tokyo", "eindhoven", "yokohama", "japan", "netherlands",
        "biomedical", "industrial design", "engineering", "technology",
        "author", "affiliation", "email", "corresponding",
        "all tools", "export", "edit", "create", "combine", "organize",
        "protect", "convert", "scan", "ocr",
        "use-case", "ccs concepts", "additional key words",
        "received", "accepted", "published", "conference",
        "proceedings", "volume", "issue", "pages", "copyright",
        "0000-0001", "0000-0002", "0000-0003", "0000-0004", "0000-0005"
    ]
    
    author_patterns = [
        r'[A-Z][a-z]+ [A-Z][a-z]+\[',
        r'[A-Z][a-z]+, [A-Z]\.',
        r'[A-Z]\. [A-Z][a-z]+',
        r'[A-Z][a-z]+ [A-Z][a-z]+,',
    ]
    
    for line in lines[:20]:
        line = re.sub(r"\s+", " ", line.strip())
        if not line:
            continue
        
        is_author = False
        for pattern in author_patterns:
            if re.search(pattern, line):
                is_author = True
                break
        if is_author:
            continue
        
        if re.search(r'\d{4}[-–]\d{4}[-–]\d{4}[-–]\d{4}', line):
            continue
        
        lower = line.lower()
        if any(word in lower for word in skip_words):
            continue
        
        if re.search(r"@|www\.|http|\.com|\.org|\.edu", lower):
            continue
        
        if re.fullmatch(r"[\d\s.,:/()-]+", line):
            continue
        
        if len(re.findall(r"[A-Za-z]", line)) < 4:
            continue
        
        if len(line) < 15 or len(line) > 300:
            continue
        
        if '?' in line or ':' in line:
            title = line
            title = re.sub(r'\[\d+\]', '', title)
            title = re.sub(r'\(\d+\)', '', title)
            title = re.sub(r'\d{4}[-–]\d{4}[-–]\d{4}[-–]\d{4}', '', title)
            title = re.sub(r'\s+', ' ', title).strip()
            if not re.search(r'[A-Z][a-z]+ [A-Z][a-z]+\[', title):
                return title
        
        if 'Casting' in line or 'Context' in line:
            title = line
            title = re.sub(r'\[\d+\]', '', title)
            title = re.sub(r'\(\d+\)', '', title)
            title = re.sub(r'\d{4}[-–]\d{4}[-–]\d{4}[-–]\d{4}', '', title)
            title = re.sub(r'\s+', ' ', title).strip()
            if not re.search(r'[A-Z][a-z]+ [A-Z][a-z]+\[', title):
                return title
        
        if re.search(r"[A-Z]", line) and len(re.findall(r"[A-Z]", line)) >= 2:
            if len(line) > 20:
                title = line
                title = re.sub(r'\[\d+\]', '', title)
                title = re.sub(r'\(\d+\)', '', title)
                title = re.sub(r'\d{4}[-–]\d{4}[-–]\d{4}[-–]\d{4}', '', title)
                title = re.sub(r'\s+', ' ', title).strip()
                if not re.search(r'[A-Z][a-z]+ [A-Z][a-z]+\[', title):
                    return title
    
    return "Title not found"

# ========== SIMPLIFIED AND IMPROVED extract_title() ==========
def extract_title(text):
    """Extract title using simpler but more effective approach."""
    # Clean text
    cleaned = fix_all_text(text)
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    
    # Patterns to skip (author names, affiliations, metadata)
    skip_patterns = [
        r'(?i)^(abstract|introduction|keywords|references|conclusion|acknowledgment|appendix)',
        r'(?i)^(university|college|institute|school|department)',
        r'(?i)^(dr\.|prof\.|mr\.|ms\.|mrs\.)',
        r'(?i)^(page|volume|issue|copyright|proceedings)',
        r'(?i)^(received|accepted|published|conference)',
        r'(?i)^(author|affiliation|email|corresponding)',
        r'@',
        r'\d{4}[-–]\d{4}[-–]\d{4}[-–]\d{4}',
        r'^\d+$',
    ]
    
    # Keywords that indicate a title (helps identify titles)
    title_keywords = [
        r'(?i)learning', r'(?i)recognition', r'(?i)speech', r'(?i)language',
        r'(?i)system', r'(?i)model', r'(?i)network', r'(?i)robot',
        r'(?i)analysis', r'(?i)detection', r'(?i)classification',
        r'(?i)generation', r'(?i)translation', r'(?i)prediction',
        r'(?i)optimization', r'(?i)recommendation', r'(?i)personalized',
        r'(?i)automation', r'(?i)intelligent', r'(?i)deep',
        r'(?i)convolutional', r'(?i)neural', r'(?i)transformer',
        r'(?i)bert', r'(?i)gpt', r'(?i)llm', r'(?i)cnn', r'(?i)rnn',
        r'(?i)lstm', r'(?i)attention', r'(?i)architecture',
    ]
    
    title_parts = []
    
    for line in lines[:50]:  # Check first 50 lines
        line = re.sub(r'\s+', ' ', line)
        
        # Skip if too short
        if len(line) < 10:
            continue
        
        # Skip if too long (likely not a title)
        if len(line) > 300:
            continue
        
        # Check skip patterns
        skip = False
        for pattern in skip_patterns:
            if re.search(pattern, line):
                skip = True
                break
        if skip:
            # If we already have title parts, stop
            if title_parts:
                break
            continue
        
        # Check if it has author indicators (multiple names with commas)
        if line.count(',') > 2:
            continue
        
        # Check if it has "and" between names
        if re.search(r'[A-Z][a-z]+\s+and\s+[A-Z][a-z]+', line):
            continue
        
        # Check for author initials pattern (e.g., "J. Smith")
        if re.search(r'[A-Z]\.\s+[A-Z][a-z]+', line):
            continue
        
        # Looks like a title - add it
        title_parts.append(line)
        
        # Stop if we have 3 parts
        if len(title_parts) >= 3:
            break
    
    # If no title found with the above method, try a more aggressive approach
    if not title_parts:
        for line in lines[:30]:
            line = re.sub(r'\s+', ' ', line)
            
            # Skip short lines
            if len(line) < 15:
                continue
            
            # Skip if it has author patterns
            if re.search(r'[A-Z]\.\s+[A-Z][a-z]+', line):
                continue
            if line.count(',') > 1:
                continue
            
            # Check if it has title keywords
            for keyword in title_keywords:
                if re.search(keyword, line):
                    title_parts.append(line)
                    break
            
            if title_parts:
                break
    
    if title_parts:
        title = ' '.join(title_parts)
        title = re.sub(r'\s+', ' ', title).strip()
        title = re.sub(r'[;,:]+$', '', title)
        # Remove any remaining author-like text
        title = re.sub(r'\b(Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.)\s+[A-Z][a-z]+', '', title)
        title = re.sub(r'[A-Z]\.\s+[A-Z][a-z]+', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        return title if len(title) > 15 else "Title not found"
    
    return "Title not found"

def extract_year(text):
    patterns = [
        r"published[:\s]*(19|20)\d{2}",
        r"publication[:\s]*(19|20)\d{2}",
        r"accepted[:\s]*(19|20)\d{2}",
        r"received[:\s]*(19|20)\d{2}",
        r"\b(19|20)\d{2}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            year = re.search(r"\b(19|20)\d{2}\b", match.group(0))
            if year:
                year_val = year.group(0)
                if 1950 <= int(year_val) <= 2026:
                    return year_val

    return "Year not found"

def detect_domain(text):
    text_lower = text.lower()[:12000]

    domains = {
        r"speech recognition|voice|audio|acoustic|asr|tts|whisper": "Speech Recognition / Audio Processing",
        r"robot|robotic|automation|autonomous|drone": "Robotics / Automation",
        r"healthcare|medical|clinical|disease|patient|diagnosis": "Healthcare / Medical AI",
        r"machine learning|deep learning|neural network|artificial intelligence|\bai\b": "Machine Learning / Artificial Intelligence",
        r"computer vision|image|object detection|segmentation|cnn|yolo": "Computer Vision",
        r"nlp|natural language|text mining|language model|bert|gpt": "Natural Language Processing",
        r"blockchain|crypto|smart contract": "Blockchain Technology",
        r"network|wireless|iot|sensor|5g": "Computer Networks / IoT",
        r"cyber|security|encryption|privacy|malware": "Cybersecurity",
        r"data science|analytics|big data|data mining": "Data Science",
        r"fake news|graph|anomaly|detection": "Fake News Detection / Graph Analysis",
    }

    for pattern, domain in domains.items():
        if re.search(pattern, text_lower):
            return domain

    return "Computer Science"

def extract_section(text, headings, stop_headings, sentence_count=4, fallback="Not found"):
    heading_pattern = "|".join(headings)
    stop_pattern = "|".join(stop_headings)

    pattern = rf"(?is)\b(?:{heading_pattern})\b\s*[:\-]?\s*(.*?)(?=\n\s*(?:{stop_pattern})\b|\Z)"
    match = re.search(pattern, text)

    if not match:
        return fallback

    content = clean_output(match.group(1))
    sentences = get_complete_sentences(content)

    if sentences:
        result = ". ".join(sentences[:sentence_count])
        if not result.endswith("."):
            result += "."
        return result

    return content[:700] if content else fallback

def extract_abstract(text):
    return extract_section(
        text,
        ["abstract", "summary"],
        ["keywords", "index terms", "introduction", "1 introduction"],
        4,
        "Abstract not found"
    )

def extract_methodology(text):
    return extract_section(
        text,
        ["methodology", "methods", "materials and methods", "experimental setup", "proposed method"],
        ["results", "evaluation", "discussion", "conclusion", "references"],
        4,
        "Methodology not clearly described"
    )

def extract_dataset(text):
    return extract_section(
        text,
        ["dataset", "data set", "data collection", "data", "experimental data"],
        ["methodology", "methods", "results", "evaluation", "discussion", "conclusion", "references"],
        3,
        "Dataset information not specified"
    )

def extract_results(text):
    return extract_section(
        text,
        ["results", "findings", "evaluation", "experimental results", "performance"],
        ["discussion", "conclusion", "future work", "references"],
        3,
        "Results not clearly presented"
    )

def extract_future_scope(text):
    return extract_section(
        text,
        ["future work", "future scope", "future research", "future directions", "future developments"],
        ["references", "acknowledgment", "appendix"],
        3,
        "Future scope not specified"
    )

def extract_algorithms(text):
    algorithms = []
    alg_list = [
        "CNN", "RNN", "LSTM", "GRU", "BERT", "GPT", "Transformer",
        "ResNet", "VGG", "YOLO", "GAN", "VAE", "SVM", "XGBoost",
        "Random Forest", "Decision Tree", "KNN", "PCA", "Autoencoder",
        "DNN", "ANN", "CTC", "GMM-HMM", "DNN-HMM", "Whisper",
        "Wav2Vec", "Attention", "Encoder-Decoder", "LF-MMI", "E2E",
        "GBAD", "MDL", "Graph"
    ]

    search_text = text[:20000]
    for alg in alg_list:
        if re.search(rf"\b{re.escape(alg)}\b", search_text, re.IGNORECASE):
            if alg not in algorithms:
                algorithms.append(alg)

    return " | ".join(algorithms[:8]) if algorithms else "Not specified"

def extract_advantages(text):
    search_text = clean_output(text[:25000])

    patterns = [
        r"(?i)(?:outperforms|improves|enhances|achieves|provides|offers|demonstrates|shows)[^.]*\.",
        r"(?i)(?:advantage|benefit|strength)[^.]*\.",
        r"(?i)(?:results show|findings indicate|experiments demonstrate)[^.]*\.",
    ]

    advantages = []

    for pattern in patterns:
        for match in re.findall(pattern, search_text):
            sentence = clean_output(match)
            if len(sentence) > 35 and sentence not in advantages:
                advantages.append(sentence)
                if len(advantages) >= 4:
                    break
        if len(advantages) >= 4:
            break

    if advantages:
        return " | ".join(advantages[:4])
    return "Advantages not clearly stated"

def extract_keywords(text):
    search_text = text[:15000].lower()
    search_text = re.sub(r"\[[^\]]*\]", " ", search_text)

    words = re.findall(r"\b[a-zA-Z]{4,}\b", search_text)

    stopwords = {
        "paper", "research", "study", "analysis", "result", "results",
        "method", "methods", "approach", "system", "model", "models",
        "data", "using", "used", "based", "this", "that", "with",
        "from", "were", "will", "have", "been", "which", "their",
        "there", "these", "those", "also", "such", "more", "most",
        "section", "figure", "table", "proposed", "performance",
        "accuracy", "information", "different", "various", "where",
        "when", "while", "within", "without", "between", "among",
        "through", "during", "across", "along", "below", "above"
    }

    words = [word for word in words if word not in stopwords]
    counts = Counter(words).most_common(12)
    keywords = [word for word, count in counts if count > 1]

    return keywords[:8] if keywords else ["Keywords not found"]

def get_complete_sentences(text):
    parts = re.split(r"[.!?]+", text)
    sentences = []

    for part in parts:
        sentence = clean_output(part)
        if len(sentence) > 30 and re.match(r"^[A-Z]", sentence):
            sentences.append(sentence)

    return sentences

def clean_output(text):
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()