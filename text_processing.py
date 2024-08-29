import spacy
from spacy.matcher import Matcher

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Matcher
matcher = Matcher(nlp.vocab)

# Define patterns for different information
patterns = {
    "Car Type": [
        [{"LOWER": {"in": ["hatchback", "suv", "sedan"]}}],
        [{"LOWER": {"in": ["hatch", "suv", "sed"]}}]  # Add variations
    ],
    "Fuel Type": [
        [{"LOWER": {"in": ["diesel", "petrol", "gasoline"]}}]  # Include common variants
    ],
    "Color": [
        [{"LOWER": {"in": ["white", "black", "red", "blue", "green", "yellow", "grey", "silver", "brown", "orange", "purple"]}}],
        [{"LOWER": {"in": ["color", "colour"]}}]  # Include color-related terms
    ],
    "Transmission Type": [
        [{"LOWER": {"in": ["manual", "automatic", "auto"]}}]  # Add variations
    ],
    "Return Policy": [
        [{"LOWER": {"in": ["return", "refund", "policy"]}}]
    ],
    "Money Back Guarantee": [
        [{"LOWER": "money-back"}],
        [{"LOWER": "guarantee"}]  # Add variations
    ],
    "Free RC Transfer": [
        [{"LOWER": {"in": ["rc", "transfer", "registration", "certificate"]}}]
    ],
    "Free RSA": [
        [{"LOWER": "rsa"}],
        [{"LOWER": {"in": ["roadside", "assistance"]}}]
    ],
    "Refurbishment Quality": [
        [{"LOWER": {"in": ["refurbishment", "quality"]}}],
        [{"LOWER": {"in": ["refurb", "condition"]}}]
    ],
    "Car Issues": [
        [{"LOWER": {"in": ["car", "issues", "problems", "faults"]}}]
    ],
    "Price Issues": [
        [{"LOWER": {"in": ["price", "issues", "cost", "price"]}}],
        [{"LOWER": {"in": ["price", "concern"]}}]
    ],
    "Customer Experience Issues": [
        [{"LOWER": {"in": ["customer", "experience", "wait", "salesperson"]}}],
        [{"LOWER": {"in": ["service", "behavior", "experience"]}}]
    ],
    "Price": [  # Add pattern for prices starting with "Rs"
        [{"LOWER": "rs"}, {"IS_DIGIT": True}, {"IS_PUNCT": True, "OP": "?"}]
    ]
}

for key, pattern in patterns.items():
    matcher.add(key, pattern)

def extract_customer_requirements(text):
    doc = nlp(text)
    matches = matcher(doc)
    
    extracted_info = {
        "Car Type": None,
        "Fuel Type": None,
        "Color": None,
        "Distance Travelled": None,  # Add pattern for distance if needed
        "Make Year": None,  # Add pattern for make year if needed
        "Transmission Type": None
    }
    
    for match_id, start, end in matches:
        span = doc[start:end]
        key = nlp.vocab.strings[match_id]
        if key in extracted_info:
            extracted_info[key] = span.text
    
    return extracted_info

def extract_company_policies(text):
    doc = nlp(text)
    matches = matcher(doc)
    
    extracted_info = {
        "Return Policy": None,
        "Money Back Guarantee": None,
        "Free RC Transfer": None,
        "Free RSA": None
    }
    
    for match_id, start, end in matches:
        span = doc[start:end]
        key = nlp.vocab.strings[match_id]
        if key in extracted_info:
            extracted_info[key] = span.text
    
    return extracted_info

def extract_customer_objections(text):
    doc = nlp(text)
    matches = matcher(doc)
    
    extracted_info = {
        "Refurbishment Quality": None,
        "Car Issues": None,
        "Price Issues": None,
        "Customer Experience Issues": None
    }
    
    for match_id, start, end in matches:
        span = doc[start:end]
        key = nlp.vocab.strings[match_id]
        if key in extracted_info:
            extracted_info[key] = span.text
    
    return extracted_info

def extract_information(text):
    customer_requirements = extract_customer_requirements(text)
    company_policies = extract_company_policies(text)
    customer_objections = extract_customer_objections(text)
    
    return {
        "Customer Requirements": customer_requirements,
        "Company Policies": company_policies,
        "Customer Objections": customer_objections
    }
