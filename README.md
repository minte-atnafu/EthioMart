EthioMart NER Project
Overview
The EthioMart Named Entity Recognition (NER) project aims to extract key entities (products, prices, and locations) from Amharic-language messages posted on Ethiopian e-commerce Telegram channels. These entities will support vendor analytics and a micro-lending scorecard for EthioMart. This repository contains scripts for data ingestion, preprocessing, and labeling, with plans for model fine-tuning, comparison, interpretability, and vendor analytics.
Current Progress

Task 1: Data Ingestion and Preprocessing - A Python script using telethon scrapes messages from Telegram channels, preprocesses Amharic text, and stores data in JSON format.
Task 2: Data Labeling - A sample of 30 messages is labeled in CoNLL format for NER, with recommendations for using doccano or Label Studio for efficient annotation.
Interim Report - A LaTeX-formatted report (interim_report.tex) summarizes progress for EthioMart stakeholders.

Repository Structure
├── media/                  # Directory for scraped images/documents
├── telegram_scraper.py     # Script for scraping and preprocessing Telegram messages
├── ner_labeled_data.conll  # Sample labeled dataset in CoNLL format
├── interim_report.tex      # LaTeX interim report for stakeholders
└── README.md               # Project documentation

Prerequisites

Python 3.8+
Telegram API credentials (API ID, API hash, phone number) from my.telegram.org
LaTeX environment with texlive-full and texlive-fonts-extra for compiling the interim report
Docker (optional, for doccano or Label Studio)

Python Dependencies
Install required Python packages:
pip install telethon unicodedata

LaTeX Dependencies
For compiling interim_report.tex:
sudo apt-get update
sudo apt-get install texlive-full texlive-fonts-extra

Setup

Clone the Repository:
git clone https://github.com/minte-atnafu/EthioMart
cd ethiomart-ner


Configure Telegram API:

Obtain API credentials from my.telegram.org.
Edit telegram_scraper.py to include your api_id, api_hash, and phone:api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'




Set Up Annotation Tools (Optional):

Doccano:docker pull doccano/doccano
docker run -d --name doccano -p 8000:8000 doccano/doccano

Access at http://localhost:8000 (default: admin/pass).
Label Studio:docker run -it -p 8080:8080 -v label_studio_data:/label_studio/data heartexlabs/label-studio:latest

Access at http://localhost:8080.



Usage
Task 1: Data Ingestion and Preprocessing

Run the Telegram scraper to collect messages:
python telegram_scraper.py


Outputs preprocessed_data.json with structured message data.
Media files (images/documents) are saved in the media/ directory.


The script:

Scrapes messages from five channels: t.me/EthioMart, t.me/AddisShopping, t.me/EthioCommerce, t.me/BoleMarket, t.me/ShopEthiopia.
Normalizes Amharic text (Unicode NFC), tokenizes, and cleans special characters.
Stores metadata (channel, timestamp, sender ID) and content (text tokens, media paths).



Task 2: Data Labeling

View the sample labeled dataset:
cat ner_labeled_data.conll


Contains 30 messages labeled with entities: B-Product, I-Product, B-LOC, I-LOC, B-PRICE, I-PRICE, O.


To label additional messages:

Import preprocessed_data.json into doccano or Label Studio.
Define NER labels (B-Product, etc.).
Export labeled data and convert to CoNLL format using a script like:import json
def jsonl_to_conll(jsonl_file, conll_file):
    with open(jsonl_file, 'r', encoding='utf-8') as f, open(conll_file, 'w', encoding='utf-8') as out:
        for line in f:
            data = json.loads(line)
            tokens = data['text'].split()
            labels = ['O'] * len(tokens)
            for label in data.get('labels', []):
                start, end, entity = label
                token_idx = len(data['text'][:start].split())
                labels[token_idx] = f'B-{entity}'
                for i in range(token_idx + 1, len(tokens)):
                    if len(' '.join(tokens[:i + 1])) <= end:
                        labels[i] = f'I-{entity}'
            for token, label in zip(tokens, labels):
                out.write(f'{token} {label}\n')
            out.write('\n')





Compile Interim Report
Compile the LaTeX report to PDF:
latexmk -pdf -interaction=nonstopmode interim_report.tex


Outputs interim_report.pdf summarizing data preparation and labeling progress.

Data Structure
preprocessed_data.json
[
  {
    "channel": "t.me/EthioMart",
    "message_id": 123,
    "timestamp": "2025-06-22T13:11:00+03:00",
    "sender_id": 456789,
    "text": "ቶምሲስ ብርጌስ ጫማ በ 1000 ብር በ አዲስ አበባ ይገኛል",
    "tokens": ["ቶምሲስ", "ብርጌስ", "ጫማ", "በ", "1000", "ብር", "በ", "አዲስ", "አበባ", "ይገኛል"],
    "media": "media/photo_123.jpg"
  },
  ...
]

ner_labeled_data.conll
ቶምሲስ B-Product
ብርጌስ I-Product
ጫማ I-Product
በ O
1000 B-PRICE
ብር I-PRICE
በ O
አዲስ B-LOC
አበባ I-LOC
ይገኛል O

ኤሌክትሪክ B-Product
ማጠቢያ I-Product
ማሽን I-Product
ዋጋ O
2500 B-PRICE
ብር I-PRICE
በ O
ቦሌ B-LOC
ለሽያጭ O
...

Future Steps

Task 3: Fine-tune NER models (XLM-RoBERTa, bert-tiny-amharic) using the labeled CoNLL dataset.
Task 4: Compare model performance (accuracy, speed, robustness).
Task 5: Implement SHAP and LIME for model interpretability.
Task 6: Develop a Vendor Analytics Engine to calculate metrics (posting frequency, average views, lending score) for the Vendor Scorecard.

Contributing
To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/new-feature).
Commit changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature/new-feature).
Open a pull request.

