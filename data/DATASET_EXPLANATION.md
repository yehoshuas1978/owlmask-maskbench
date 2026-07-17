# OwlMask Benchmarking Dataset Explanation

This document outlines the structure, methodology, and categories of the synthetic test datasets generated for evaluating the OwlMask PII masking engine.

## Overview

The datasets are stored in `texts-to-mask-{lang}.txt` files within the `data` directory. Each file contains **10,000 synthetic records** tailored to a specific language:
- **Hebrew (`-he.txt`)**
- **English (`-en.txt`)**
- **German (`-de.txt`)**

To ensure robust evaluation, the dataset is highly diverse. It utilizes randomly generated names, cities, streets, phone numbers, IPs, MAC addresses, IBANs, and national IDs mixed into over 38 structural templates per language.

Each record in the `.txt` files is separated by a `---` delimiter to safely support multi-line text strings.

## Categories of Text

Each 10,000-record file is divided into five distinct testing categories, designed to test different capabilities and vulnerabilities of the masking engine.

### 1. Core PII & Mixed Language (2,000 Records)
These are standard, straightforward sentences you would expect to see in regular logs, tickets, or reports.
- **Purpose**: Establishes a baseline accuracy for standard PII patterns (names next to "Name:" or "ID:").
- **Features**: Includes mixed-language scenarios (e.g., English names dropped into a Hebrew sentence) and standard false positive tests.
- **False Positives Included**:
  - Ambiguous words that sound like names (e.g., "Grace", "May", "Hope", "שמחה", "אור").
  - 9-digit inventory part numbers that perfectly mimic Teudat Zehut (Israeli ID) or SSN formatting, testing the engine's ability to use context to *ignore* them.

### 2. Implicit / No-Label Context (1,000 Records)
These records contain PII dropped directly into conversational text without any identifying labels.
- **Purpose**: Tests the engine's semantic/NLP understanding. If an engine relies heavily on regular expressions looking for keywords like "ID Number" or "Phone:", it will fail here.
- **Example**: *"I left the package with John Smith at 12 Main St. Call (555) 123-4567 if there are issues."*

### 3. Advanced Edge Cases (3,000 Records)
These records actively attempt to break the masking engine by using hostile formatting, encoding, and syntax.
- **Purpose**: Torture-testing parser resilience and tokenization logic.
- **Features**:
  - **Multi-line Strings**: Text spanning several lines with `\n` characters (e.g., standard email signatures).
  - **Punctuation Hugging**: PII tightly wrapped in brackets or quotes without spaces `[{John Smith}], ({123456789})`.
  - **Emojis**: PII placed directly adjacent to emojis `📞054-1234567`.
  - **HTML/XML Tags**: PII nested inside markup `<div>Customer: <strong>John Smith</strong></div>`.
  - **URL Encoding**: PII passed as web query parameters `?user=John%20Smith&phone=123-4567`.
  - **Tabs & Capitalization**: Tab-delimited text and aggressive ALL CAPS usage.

### 4. Longform Internet Texts / Needle in a Haystack (1,000 Records)
These records consist of thick, multi-sentence paragraphs modeled after standard industry boilerplate.
- **Purpose**: Tests the engine's ability to isolate a tiny piece of sensitive data buried deep within a wall of formal text.
- **Domains Covered**:
  - **Law/Contracts**: Real estate leases and Terms of Service agreements.
  - **Medical**: Health articles (modeled after CDC/Wikipedia) discussing conditions alongside specific patient examples.
  - **Banking/Privacy**: GDPR privacy declarations and transaction logs.
  - **Insurance**: Comprehensive auto/life insurance policy documentation.

### 5. Expanded Domain Coverage (3,000 Records)
These records expand the dataset to cover highly specific, high-risk domains that expose unique types of PII.
- **Domains Covered**:
  - **Human Resources (HR)**: Resumes, references, and candidate profiles.
  - **IT / Cybersecurity**: 500 Server Errors, JSON Web Tokens (JWT), and IP address logs.
  - **E-Commerce**: Shipping notifications, addresses, and courier tracking details.
  - **Education**: Parent-teacher correspondence and student ID tracking.
  - **Government**: Tax assessments, Social Security/Tax IDs, and penalty dates.
  - **Travel**: Flight confirmations, departure dates, and passport numbers.

## Legacy Encoding Tests

In addition to the main UTF-8 files, two smaller 100-record files were generated to test how the engine handles non-UTF8 legacy file encodings:
- `texts-to-mask-he-iso8859-8.txt` (ISO-8859-8 Hebrew)
- `texts-to-mask-de-iso8859-1.txt` (ISO-8859-1 / Latin-1 German)
