import spacy

nlp = spacy.load("en_core_web_sm")

# Define categories
CATEGORIES = {
    'terrorism': 'Terrorism/protest/political unrest/riot',
    'uplifting': 'Positive/Uplifting',
    'disaster': 'Natural Disasters',
    'others': 'Others'
}

# Function to classify the article content
def classify_article(content):
    doc = nlp(content)
    # Simple keyword-based classification (can be enhanced with ML models)
    if "terrorism" in doc.text.lower() or "protest" in doc.text.lower():
        return CATEGORIES['terrorism']
    elif "happy" in doc.text.lower() or "inspiration" in doc.text.lower():
        return CATEGORIES['uplifting']
    elif "earthquake" in doc.text.lower() or "flood" in doc.text.lower():
        return CATEGORIES['disaster']
    else:
        return CATEGORIES['others']
