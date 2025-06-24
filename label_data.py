import pandas as pd
import re
from unicodedata import normalize

# Load your scraped CSV
csv_file = 'telegram_data.csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Select 30-50 messages
messages = df['Message'].dropna().head(30).tolist()  # Adjust as needed

# Predefined lists for rule-based labeling (extend as needed)
locations = ['ቦሌ', 'አዲስ አበባ', 'መገናኛ', 'ልደታ']  # Common Ethiopian locations
products = ['ጠርሙስ', 'ቡና', 'ልብስ', 'ጫማ']  # Common products
price_indicators = ['ብር', 'birr', 'ETB']

def tokenize_amharic(text):
    # Normalize Unicode for Amharic
    text = normalize('NFC', text)
    # Simple tokenization (split on whitespace, can use advanced tokenizers)
    tokens = text.split()
    return tokens

def rule_based_label(tokens):
    labels = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        # Price detection
        if re.match(r'^\d+$', token) and i + 1 < len(tokens) and tokens[i + 1] in price_indicators:
            labels.append('B-PRICE')
            labels.append('I-PRICE')
            i += 2
            continue
        # Location detection
        if token in locations:
            labels.append('B-LOC')
            if i + 1 < len(tokens) and tokens[i + 1] in locations:  # Multi-word locations
                labels.append('I-LOC')
                i += 2
                continue
        # Product detection
        if token in products:
            labels.append('B-Product')
            if i + 1 < len(tokens) and tokens[i + 1] in products:  # Multi-word products
                labels.append('I-Product')
                i += 2
                continue
        # Default: Outside
        labels.append('O')
        i += 1
    return labels

def manual_label(tokens):
    labels = []
    print("\nLabeling tokens for message:", ' '.join(tokens))
    print("Options: B-Product, I-Product, B-LOC, I-LOC, B-PRICE, I-PRICE, O")
    for token in tokens:
        label = input(f"Enter label for '{token}': ")
        while label not in ['B-Product', 'I-Product', 'B-LOC', 'I-LOC', 'B-PRICE', 'I-PRICE', 'O']:
            print("Invalid label. Options: B-Product, I-Product, B-LOC, I-LOC, B-PRICE, I-PRICE, O")
            label = input(f"Enter label for '{token}': ")
        labels.append(label)
    return labels

# Output CoNLL file
with open('labeled_data.conll', 'w', encoding='utf-8') as f:
    for message in messages:
        tokens = tokenize_amharic(message)
        if not tokens:
            continue
        # Use rule-based labeling (comment out for manual labeling)
        labels = rule_based_label(tokens)
        # Uncomment below for manual labeling
        # labels = manual_label(tokens)
        
        # Ensure tokens and labels align
        if len(tokens) != len(labels):
            print(f"Warning: Token-label mismatch in message: {message}")
            continue
        
        # Write to CoNLL file
        for token, label in zip(tokens, labels):
            f.write(f"{token} {label}\n")
        f.write("\n")  # Blank line between messages

print("Labeling complete. Output saved to 'labeled_data.conll'")