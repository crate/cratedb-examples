# Building a PDF Knowledge Assistant: Step by Step

This guide outlines how to build a PDF Knowledge Assistant, covering:

- Setting up a project folder
- Installing dependencies
- Using two Python scripts (one for extracting data from PDFs, and one for creating a chatbot)

<details>
<summary>Click to see all the different steps</summary>

---

**Disclaimer**

This guide provides a basic example to help you get started with building a PDF Knowledge Assistant. It is intended as a starting point and does not cover advanced use cases, optimizations, or production-grade considerations. Be sure to customize and enhance the implementation based on your specific needs and requirements.

Important Note: This script uses OpenAI’s API for image descriptions and embedding generation. As such, the content of your PDFs (including text and images) may be sent to OpenAI’s servers for processing. Do not use this script for confidential or sensitive PDFs unless you are certain it complies with your data privacy and security requirements.

For processing sensitive data, consider using local or self-hosted Large Language Models (LLMs) such as:

- OpenLLM: A framework for running open-source LLMs locally.
- Hugging Face Transformers: Offers pre-trained models like BERT, GPT-2, and more.
- LLaMA (Large Language Model Meta AI): An efficient model designed for local use, available via Meta’s research initiative.
- Falcon: A highly performant open-source LLM optimized for inference and fine-tuning.
- Rasa: Focused on building local conversational AI.

By using local models, you can retain complete control over your data while still leveraging advanced capabilities for text and image processing.

---

## Project Setup

### Step 1: Create Project Folders and Virtual Environment

Run the following commands to create your project folder and set up a Python virtual environment:

```bash
mkdir -p pdf-knowledge-assistant/pdf-pdf_files
cd pdf-knowledge-assistant
python3 -m venv venv
source venv/bin/activate
```

Your terminal prompt should now start with (`venv`), indicating you’re inside the virtual environment.

### Step 2: Install Dependencies

#### Install the core packages:
```bash
pip install openai python-dotenv requests PyMuPDF spacy
```

#### Install Spacy - used for Keyword extraction
``` bash
python -m spacy download en_core_web_sm
```

#### Optional 
Streamlit (for a web-based UI):

``` bash 
pip install streamlit
```

### Step 3: What Each Package Does

| Package                   | Purpose                                                                                  |
|---------------------------|------------------------------------------------------------------------------------------|
| **openai**                | Enables embeddings and chat completions with OpenAI’s LLMs.                             |
| **python-dotenv**         | Loads environment variables from a `.env` file.                                         |
| **requests**              | Sends HTTP requests (e.g., for CrateDB or external services).                           |
| **PyMuPDF**               | Extracts text and images from PDFs.                                                     |
| **spacy**                 | Handles natural language tasks like keyword extraction.                                 |
| **streamlit**             | Quickly builds simple web-based UIs.                                                   |

- openai: Enables embeddings and chat completions with OpenAI’s LLMs.
- python-dotenv: Loads environment variables from a .env file.
- requests: Sends HTTP requests (e.g., for CrateDB or external services).
- PyMuPDF: Extracts text and images from PDFs.
- spacy: Handles natural language tasks like keyword extraction.
- streamlit: Quickly builds simple web-based UIs.

### Step 4: Obtain API Keys

You’ll need:

1.	OpenAI API key – [Developer quickstart](https://platform.openai.com/docs/quickstart)
2.	CrateDB credentials – For embedding storage in [CrateDB Cloud](https://cratedb.com/docs/cloud/en/latest/tutorials/quick-start.html). 
3.	Other service-specific keys – Based on additional integrations.

Store keys in a `.env` file:

``` bash 
CRATEDB_URL=your_cratedb_url
CRATEDB_USERNAME=your_cratedb_username
CRATEDB_PASSWORD=your_cratedb_password
OPENAI_API_KEY=your_openai_api_key
AZURE_API_KEY=your_azure_api_key
```

Ensure `.env` is included in `.gitignore` to avoid committing sensitive information.


### Step 5: Build the extract_data.py script

<details>
<summary>Click to see all the different steps</summary>


#### Overview

This script processes PDFs to extract content, generate embeddings, and store the data in a CrateDB database. It is designed to handle both text and images while ensuring the data is clean, contextualized, and searchable.

##### Key Steps:

1. **Connect to Database**:
   - Ensures the necessary table exists in CrateDB.
2. **Extract Content**:
   - Retrieves text and images from PDF files.
3. **Clean and Chunk**:
   - Cleans extracted text and splits it into smaller, manageable chunks.
4. **Generate Embeddings**:
   - Converts text chunks and image descriptions into vector embeddings using OpenAI models.
5. **Store Data**:
   - Saves the processed data, including embeddings, metadata, and content, into CrateDB.

---

##### Workflow

Core Processing Steps:

- **Text Extraction**:
  - Uses PyMuPDF to read text from each page of the PDF.

- **Chunking**:
  - Splits extracted text into smaller chunks while preserving context (e.g., sentence-aware chunking).

- **Image Extraction**:
  - Identifies and retrieves images from PDF pages.
  - Optionally generates detailed descriptions for these images using GPT models.

- **Embedding Generation**:
  - Sends text and image descriptions to OpenAI to generate vector embeddings, enabling similarity-based searches.

- **Storage**:
  - Inserts data into CrateDB, including:
    - **Content**: Text or image descriptions.
    - **Metadata**: Page numbers and document names.
    - **Embeddings**: Vectors for semantic search.

This step-by-step process ensures that the PDF content is indexed and searchable for efficient retrieval in future queries.

This script processes PDFs—text and images—and stores the extracted data in a database. 

####  Import Libraries and Set Up Environment Variables
Load environment variables from a .env file to keep sensitive data secure.

``` python
import os
import re
import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv
from base64 import b64encode
from requests.auth import HTTPBasicAuth
from openai import OpenAI

# Load environment variables
load_dotenv()

CRATEDB_URL = os.getenv("CRATEDB_URL")
CRATEDB_USERNAME = os.getenv("CRATEDB_USERNAME")
CRATEDB_PASSWORD = os.getenv("CRATEDB_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_DIR = os.getenv("PDF_DIR", "./pdf_files")
COLLECTION_NAME = "pdf_data"

# Instantiate OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)
```

Environment Variables Required:

- CRATEDB_URL: URL formatted connection string for CrateDB.
- CRATEDB_USERNAME / CRATEDB_PASSWORD: Credentials for CrateDB.
- OPENAI_API_KEY: OpenAI API key.
- PDF_DIR: Directory containing the PDFs to process.


#### CrateDB Helpers

##### Define CrateDB general Query Helper
A utility function to send queries to CrateDB:

``` python
def execute_cratedb_query(query, args=None):
    data = {"stmt": query}
    if args:
        data["args"] = args
    response = requests.post(
        CRATEDB_URL, json=data, auth=HTTPBasicAuth(CRATEDB_USERNAME, CRATEDB_PASSWORD)
    )
    if response.status_code != 200:
        print(f"CrateDB query failed: {response.text}")
        return None
    return response.json()
```

##### Create the database table
Define a function to create the database table for storing the data if it doesn’t exist:

``` python
def create_table():
    query = f"""
    CREATE TABLE IF NOT EXISTS {COLLECTION_NAME} (
        id TEXT PRIMARY KEY,
        document_name TEXT,
        page_number INT,
        content_type TEXT,
        content TEXT INDEX USING FULLTEXT WITH (analyzer = 'standard'),
        content_embedding FLOAT_VECTOR(1536)
    )
    """
    execute_cratedb_query(query)
    execute_cratedb_query(f"REFRESH TABLE {COLLECTION_NAME}")
    print(f"Table {COLLECTION_NAME} is ready.")
```

| Column Name       | Description                                       |
|-------------------|---------------------------------------------------|
| **id**            | Unique identifier for the chunk.                 |
| **document_name** | Name of the PDF file.                            |
| **page_number**   | Page number where the content is found.          |
| **content_type**  | Type of content ("text" or "image").             |
| **content**       | Extracted text or image description.             |
| **content_embedding** | Vector embedding for the content.               |

##### Helper to store extracted data in CrateDB

``` python 
def store_in_cratedb(
    content_id, document_name, page_number, content_type, content, embedding
):
    """
    Stores extracted text or image data in CrateDB.

    Parameters:
    - content_id (str): Unique identifier for the content.
    - document_name (str): Name of the source PDF file.
    - page_number (int): Page number of the content.
    - content_type (str): Type of content ("text" or "image").
    - content (str): The actual text or image description.
    - embedding (list): The vector embedding of the content.

    Notes:
    - Insert the data into the specified CrateDB table.
    - Content and embeddings are indexed for efficient retrieval.
    """
    query = f"""
    INSERT INTO {COLLECTION_NAME} (id, document_name, page_number, content_type, content, content_embedding)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    execute_cratedb_query(
        query,
        [content_id, document_name, page_number, content_type, content, embedding],
    )
    print(f"Stored content: {content_id}")
```

#### Extraction helpers

These functions ensure that text is cleaned and broken into manageable chunks, and irrelevant headers/footers are removed. Here’s the complete implementation:

##### Extract Text with Header/Footer Removal
This function identifies repetitive headers/footers and removes them before cleaning and chunking the remaining text.

``` python
def extract_text_with_cleaning(doc):
    """
    Extracts and cleans text from a PDF, removing repetitive headers/footers.

    Parameters:
    - doc (fitz.Document): A PyMuPDF document object.

    Returns:
    - list: A list of dictionaries with "page" (page number) and "text" (cleaned chunk).

    Process:
    1. Identifies repeating headers/footers by analyzing all pages.
    2. Remove identified headers/footers from each page.
    3. Split the remaining text into sentence-aware chunks.
    4. Returns the cleaned and chunked text with metadata.
    """
    all_chunks = []
    header_candidates = []

    # Identify potential headers/footers
    for page in doc:
        text_lines = page.get_text("text").splitlines()
        if len(text_lines) > 2:
            header_candidates.append(text_lines[0])  # Add first line as header
            header_candidates.append(text_lines[-1])  # Add last line as footer

    # Find common headers/footers across pages
    common_headers = {
        k
        for k, v in dict.fromkeys(header_candidates).items()
        if header_candidates.count(k) > 2
    }

    # Process each page
    for page_num, page in enumerate(doc):
        text_lines = page.get_text("text").splitlines()
        clean_lines = [line for line in text_lines if line not in common_headers]
        cleaned_text = clean_text("\n".join(clean_lines))
        chunks = sentence_aware_chunking(cleaned_text)

        # Store chunks with metadata
        for chunk in chunks:
            if len(chunk) > 50:  # Only include meaningful chunks
                all_chunks.append({"page": page_num + 1, "text": chunk})
    return all_chunks

```

##### Clean Text

This function removes unnecessary elements such as URLs, emails, and phone numbers.
``` python
def clean_text(text):
    """
    Cleans raw text by removing unnecessary elements.

    Parameters:
    - text (str): The raw text to clean.

    Returns:
    - str: The cleaned and normalized text.

    Cleaning Steps:
    - Removes URLs, email addresses, and phone numbers.
    - Replaces multiple spaces with a single space.
    """
    text = re.sub(r"https?://\S+|www\.\S+", "", text)  # Remove URLs
    text = re.sub(r"\S+@\S+\.\S+", "", text)  # Remove emails
    text = re.sub(r"\+?\d[\d\s\-\(\)]{8,}\d", "", text)  # Remove phone numbers
    text = re.sub(r"\s{2,}", " ", text)  # Replace multiple spaces
    return text.strip()
```

##### Sentence-Aware Chunking

This function ensures text is split into chunks while preserving sentence boundaries. Chunks have a maximum size and optional overlap.
``` python
def sentence_aware_chunking(text, max_chunk_size=500, overlap=50):
    """
    Splits text into manageable chunks, preserving sentence boundaries.

    Parameters:
    - text (str): The input text to chunk.
    - max_chunk_size (int): Maximum size of each chunk (in characters).
    - overlap (int): Number of overlapping characters between consecutive chunks.

    Returns:
    - list: A list of text chunks.

    Notes:
    - Ensures sentences are not split across chunks for better context retention.
    - Useful for generating embeddings and storing in CrateDB.
    """
    sentences = re.split(r"(?<=[.!?]) +", text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

```

##### Extract text near images

Extracts a snippet of text near a specified position on the page, providing contextual sentences around an image or other content for enhanced understanding.
``` python 
def extract_surrounding_text(page_text, position=0, max_length=300):
    """
    Extracts nearby text to provide context for an image.

    Parameters:
    - page_text (str): The full text of the page containing the image.
    - position (int): Approximate index of the image on the page.
    - max_length (int): Maximum number of characters to include in the snippet.

    Returns:
    - str: A snippet of text surrounding the image's position.

    Notes:
    - Captures sentences around the image's position for better contextualization.
    """
    lines = re.split(r"(?<=[.!?])\s+", page_text)  # Split into sentences
    start = max(0, position - 1)
    end = min(len(lines), position + 2)  # Capture sentences around the position

    # Combine and trim to max_length
    surrounding_snippet = " ".join(lines[start:end])
    return surrounding_snippet[:max_length].strip()
```

##### Encode image to base64

``` python
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")
```

#### Generate embeddings (Text and Images)

##### Function to generate text embeddings
Generates vector embeddings for a given text chunk and stores it with associated metadata in CrateDB.

``` python 
def get_text_embedding_openai(text, model="text-embedding-3-small"):
    """
    Generates a vector embedding for the given text using OpenAI's embedding model.

    Parameters:
    - text (str): The text content to embed.
    - model (str): OpenAI embedding model (default: "text-embedding-3-small").

    Returns:
    - list: A list of floats representing the embedding vector.
    - None: If the embedding generation fails (e.g., invalid input, API error).

    Notes:
    - The embedding helps in similarity searches for text retrieval.
    """
    try:
        text = text.replace("\n", " ")  # Clean up newlines
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding for text: {text[:50]}... Error: {e}")
        return None
```

``` python
def generate_text_embedding(text, document_name, page_num, idx):
    """
    Generates an embedding for a text chunk and stores it in CrateDB.

    Parameters:
    - text (str): The text content to embed.
    - document_name (str): Name of the source document.
    - page_num (int): Page number where the text is located.
    - idx (int): Index of the chunk in the page.
    """
    embedding = get_text_embedding_openai(text)
    if embedding:
        content_id = f"text_{document_name}_{page_num}_{idx}"
        store_in_cratedb(content_id, document_name, page_num, "text", text, embedding)
        print(f"Stored text embedding: {content_id}")
```

##### Functions to generate image embeddings

Creates a detailed natural language description of an image using OpenAI’s GPT-4 Turbo model.

``` python
def generate_image_description(image_bytes, max_tokens=150):
    """
    Generates a detailed description of an image using OpenAI's GPT-4 Turbo.

    Parameters:
    - image_bytes (bytes): The binary data of the image.
    - max_tokens (int): Maximum tokens for the generated description.

    Returns:
    - str: A detailed description of the image.
    - "Image description unavailable": If the description generation fails.

    Process:
    1. Encode the image to Base64.
    2. Sends the encoded image to OpenAI GPT-4 Turbo.
    3. Extracts and returns the generated description.
    """
    try:
        # Encode the image to base64
        encoded_image = b64encode(image_bytes).decode("utf-8")

        # Call GPT-4-Turbo with vision capabilities
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at describing images in detail. Provide rich and concise descriptions of the key visual elements of any image.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image in detail."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            },
                        },
                    ],
                },
            ],
            max_tokens=max_tokens,
            temperature=0.5,
        )

        # Extract and return the description
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error generating image description: {e}")
        return "Image description unavailable."
```

Combines an image description and its surrounding context to generate embeddings and stores them in CrateDB.
``` python
def generate_image_embedding(image_bytes, surrounding_text, document_name, page_num, img_index):
    """
    Generates a description for an image, creates an embedding, and stores it in CrateDB.

    Parameters:
    - image_bytes (bytes): The binary data of the image.
    - surrounding_text (str): Contextual text near the image.
    - document_name (str): Name of the source document.
    - page_num (int): Page number where the image is located.
    - img_index (int): Index of the image on the page.
    """
    # Generate image description
    image_description = generate_image_description(image_bytes)

    # Combine description with surrounding text
    combined_description = f"{image_description} Context: {surrounding_text}"

    # Generate embedding
    embedding = get_text_embedding_openai(combined_description)
    if embedding:
        content_id = f"image_{document_name}_{page_num}_{img_index}"
        store_in_cratedb(
            content_id, document_name, page_num, "image", combined_description, embedding
        )
        print(f"Stored image embedding: {content_id}")
```

#### Process PDFs (with Text and Images)

The `process_pdf` function handles:
- Text extraction, cleaning, and embedding generation.
- Image extraction, description generation, and storage of embeddings.
- Combining image descriptions with nearby text for richer context.

``` python
def process_pdf(pdf_path):
    """
    Processes a PDF file by extracting text and images, generating embeddings,
    and storing the data in CrateDB.

    Parameters:
    - pdf_path (str): The file path of the PDF to process.
    """
    print(f"Processing {pdf_path}")
    doc = fitz.open(pdf_path)
    document_name = os.path.basename(pdf_path)

    # Extract and process text with improved chunking
    extracted_chunks = extract_text_with_cleaning(doc)
    for idx, chunk_data in enumerate(extracted_chunks):
        page_num = chunk_data["page"]
        chunk_text = chunk_data["text"]

        # Generate text embedding
        generate_text_embedding(chunk_text, document_name, page_num, idx)

    # Process images with clean, minimal surrounding context
    for page_num, page in enumerate(doc):
        full_page_text = page.get_text("text")
        cleaned_page_text = clean_text(full_page_text)

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Extract surrounding text for context
            surrounding_text = extract_surrounding_text(
                cleaned_page_text, position=img_index
            )

            # Generate image embedding
            generate_image_embedding(
                image_bytes, surrounding_text, document_name, page_num + 1, img_index
            )

```

#### Tying everything together in main

The `main` function ties everything together by:

1. Ensuring the database table is ready (create_table).
2. Iterating over all PDFs in the directory to process them (process_local_pdfs).

``` python
def process_local_pdfs():
    """
    Processes all PDFs in the specified directory.

    Process:
    1. Iterates through PDF files in the directory.
    2. Calls `process_pdf` for each file to extract and store data.

    Notes:
    - Skips the directory if no PDF files are found.
    """
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    if not pdf_files:
        print("No PDF files found in the directory.")
        return
    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        process_pdf(pdf_path)
```

``` python
if __name__ == "__main__":
    # Step 1: Create or refresh the database table
    create_table()

    # Step 2: Process all PDFs in the specified directory
    process_local_pdfs()
```
</details>

#### Full `extract_data.py` script

<details>
<summary>Click to expand the full script</summary>

```python
# Import Libraries and Set Up Environment Variables
import os
import re
import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv
from base64 import b64encode
from requests.auth import HTTPBasicAuth
from openai import OpenAI

# Load environment variables
load_dotenv()

CRATEDB_URL = os.getenv("CRATEDB_URL")
CRATEDB_USERNAME = os.getenv("CRATEDB_USERNAME")
CRATEDB_PASSWORD = os.getenv("CRATEDB_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_DIR = os.getenv("PDF_DIR", "./pdf_files")
COLLECTION_NAME = "pdf_data"

# Instantiate OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Database Helpers
def execute_cratedb_query(query, args=None):
    data = {"stmt": query}
    if args:
        data["args"] = args
    response = requests.post(
        CRATEDB_URL, json=data, auth=HTTPBasicAuth(CRATEDB_USERNAME, CRATEDB_PASSWORD)
    )
    if response.status_code != 200:
        print(f"CrateDB query failed: {response.text}")
        return None
    return response.json()

def create_table():
    query = f"""
    CREATE TABLE IF NOT EXISTS {COLLECTION_NAME} (
        id TEXT PRIMARY KEY,
        document_name TEXT,
        page_number INT,
        content_type TEXT,
        content TEXT INDEX USING FULLTEXT WITH (analyzer = 'standard'),
        content_embedding FLOAT_VECTOR(1536)
    )
    """
    execute_cratedb_query(query)
    execute_cratedb_query(f"REFRESH TABLE {COLLECTION_NAME}")
    print(f"Table {COLLECTION_NAME} is ready.")

def store_in_cratedb(content_id, document_name, page_number, content_type, content, embedding):
    query = f"""
    INSERT INTO {COLLECTION_NAME} (id, document_name, page_number, content_type, content, content_embedding)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    execute_cratedb_query(query, [content_id, document_name, page_number, content_type, content, embedding])
    print(f"Stored content: {content_id}")

# Text Processing
def clean_text(text):
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"\S+@\S+\.\S+", "", text)
    text = re.sub(r"\+?\d[\d\s\-$begin:math:text$$end:math:text$]{8,}\d", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()

def sentence_aware_chunking(text, max_chunk_size=500, overlap=50):
    sentences = re.split(r"(?<=[.!?]) +", text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def extract_text_with_cleaning(doc):
    all_chunks = []
    header_candidates = []

    for page in doc:
        text_lines = page.get_text("text").splitlines()
        if len(text_lines) > 2:
            header_candidates.append(text_lines[0])
            header_candidates.append(text_lines[-1])

    common_headers = {k for k in set(header_candidates) if header_candidates.count(k) > 2}

    for page_num, page in enumerate(doc):
        text_lines = page.get_text("text").splitlines()
        clean_lines = [line for line in text_lines if line not in common_headers]
        cleaned_text = clean_text("\n".join(clean_lines))
        chunks = sentence_aware_chunking(cleaned_text)
        for chunk in chunks:
            if len(chunk) > 50:
                all_chunks.append({"page": page_num + 1, "text": chunk})
    return all_chunks

# Embedding Generation
def get_text_embedding_openai(text, model="text-embedding-3-small"):
    try:
        text = text.replace("\n", " ")
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def generate_text_embedding(text, document_name, page_num, idx):
    embedding = get_text_embedding_openai(text)
    if embedding:
        content_id = f"text_{document_name}_{page_num}_{idx}"
        store_in_cratedb(content_id, document_name, page_num, "text", text, embedding)

def generate_image_description(image_bytes, max_tokens=150):
    try:
        encoded_image = b64encode(image_bytes).decode("utf-8")
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Describe this image in detail."},
                {"role": "user", "content": f"data:image/png;base64,{encoded_image}"}
            ],
            max_tokens=max_tokens,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating image description: {e}")
        return "Image description unavailable."

def generate_image_embedding(image_bytes, surrounding_text, document_name, page_num, img_index):
    image_description = generate_image_description(image_bytes)
    combined_description = f"{image_description} Context: {surrounding_text}"
    embedding = get_text_embedding_openai(combined_description)
    if embedding:
        content_id = f"image_{document_name}_{page_num}_{img_index}"
        store_in_cratedb(content_id, document_name, page_num, "image", combined_description, embedding)

# PDF Processing
def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    document_name = os.path.basename(pdf_path)
    extracted_chunks = extract_text_with_cleaning(doc)
    for idx, chunk_data in enumerate(extracted_chunks):
        page_num = chunk_data["page"]
        chunk_text = chunk_data["text"]
        generate_text_embedding(chunk_text, document_name, page_num, idx)

    for page_num, page in enumerate(doc):
        full_page_text = page.get_text("text")
        cleaned_page_text = clean_text(full_page_text)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            surrounding_text = extract_surrounding_text(cleaned_page_text, img_index)
            generate_image_embedding(image_bytes, surrounding_text, document_name, page_num + 1, img_index)

def process_local_pdfs():
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    if not pdf_files:
        print("No PDF files found.")
        return
    for pdf_file in pdf_files:
        process_pdf(os.path.join(PDF_DIR, pdf_file))

if __name__ == "__main__":
    create_table()
    process_local_pdfs()
```
</details>

### Step 6 Start extracting PDFs

Place a PDF in the directory `pdf-knowledge-assistant/pdf-pdf_files` for example [How-to-Build-AI-driven-Knowledge-Assistants.pdf](https://cratedb.com/resources/white-papers/lp-wp-ai-driven-knowledge-assistants).

Execute the just created `extract_data.py` script. Check your database for the creation of the **pdf_data** table and the ingestion of the rows. 


### Step 7: Build the chatbot.py script for Document Retrieval and QA

<details>
<summary>Click to see all the different steps</summary>

#### Overview

This guide walks you through creating a chatbot capable of querying a CrateDB database, performing a hybrid search, and using OpenAI to generate concise answers based on PDF data.

---

##### Workflow

Chatbot Workflow:

1. Load Configurations: Load environment variables and setup.
2. Keyword Extraction: Extract meaningful keywords from the user query using spaCy.
3. Hybrid Search: Perform KNN and BM25 searches on CrateDB.
4. Answer Generation: Use OpenAI’s GPT models to generate concise answers from retrieved context.
5. Interactive Interface: Provide a user-friendly interface for asking questions.

#### Import Libraries and Load Environment Variables

First, we import the required libraries and load the environment variables for CrateDB and OpenAI configurations.

``` python
import os
import re
import requests
import spacy
from dotenv import load_dotenv
from openai import OpenAI
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()

CRATEDB_URL = os.getenv("CRATEDB_URL")
CRATEDB_USERNAME = os.getenv("CRATEDB_USERNAME")
CRATEDB_PASSWORD = os.getenv("CRATEDB_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = "pdf_data"
RESULTS_LIMIT = 3  # Number of results to return

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Instantiate OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Debug flag for debugging intermediate steps
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ANSI escape codes for formatting
GREEN = "\033[92m"
RESET = "\033[0m"
```

- If you want or need to debug you can add the following to 
Set `DEBUG=True` in the .env file to enable detailed output during development.

#### CrateDB Helpers

#### Execute queries in CrateDB
``` python
def execute_cratedb_query(query, args=None):
    data = {"stmt": query}
    if args:
        data["args"] = args

    response = requests.post(
        CRATEDB_URL, json=data, auth=HTTPBasicAuth(CRATEDB_USERNAME, CRATEDB_PASSWORD)
    )

    if response.status_code != 200:
        print(f"CrateDB query failed: {response.text}") if DEBUG else None
        return None
    return response.json()
```

#### Keyword extraction

We use spaCy to extract meaningful keywords (nouns, verbs, and proper nouns) from the user query. Tokenizes the input question and filters words based on Part-Of-Speech (POS) tags. This is used for the BM25 (Full-Text Search) to match only keywords.

``` python
def extract_keywords_pos(question):
    """
    Extracts meaningful keywords from the question using POS tagging.
    """
    doc = nlp(question)
    keywords = [token.text for token in doc if token.pos_ in {"NOUN", "PROPN", "VERB"}]
    return " ".join(keywords)
```

#### Hybrid Search

##### Generate Embedding for user question

Converts the user query into a vector embedding using OpenAI’s embedding model.

``` python
def get_text_embedding(text, model="text-embedding-ada-002"):
    """
    Generates a vector embedding for a given text using OpenAI's embedding model.
    """
    try:
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}") if DEBUG else None
        return None
```

##### Perform KNN Vector Search on CrateDB

Searches for the top matching content based on vector similarity.

``` python
def knn_search(query_embedding, collection_name, results_limit=RESULTS_LIMIT):
    """
    Searches the vector index in CrateDB using a KNN algorithm.
    Parameters:
    - query_embedding: Vector embedding of the query
    - collection_name: Name of the database collection
    - results_limit: Number of results to return
    """
    embedding_string = ",".join(map(str, query_embedding))
    if DEBUG:
        print(
            f"\n### KNN Search Query Embedding (first 10): {query_embedding[:10]} ###\n"
        )

    query = f"""
    SELECT id, document_name, page_number, content_type, content, _score
    FROM {collection_name}
    WHERE knn_match(content_embedding, ARRAY[{embedding_string}], {results_limit})
    ORDER BY _score DESC
    LIMIT {results_limit}
    """
    response = execute_cratedb_query(query)
    if response and "rows" in response:
        if DEBUG:
            print(f"\n### KNN Search Results ({len(response['rows'])} rows): ###")
            for row in response["rows"]:
                print(f"Page {row[2]} (Score: {row[-1]}): {row[4][:200]}...")
        return response["rows"]
    return []
```

##### Perform BM25 Search

Performs a keyword-based full-text search using BM25.

``` python
def full_text_search(keywords, collection_name, results_limit=RESULTS_LIMIT):
    """
    Searches the full-text index in CrateDB using BM25 (Best Matching 25) algorithm.

    Parameters:
    - keywords (str): The extracted keywords from the user's query.
    - collection_name (str): The name of the database collection to search.
    - results_limit (int): The maximum number of results to return.

    Returns:
    - list: A list of rows containing the matching records, including their scores and metadata.
    - Empty list: If no results are found or if the query fails.

    Debugging:
    - Prints the BM25 search query and results when DEBUG is enabled.
    """
    if DEBUG:
        print(f'\n### BM25 Search Query: "{keywords}" ###\n')

    query = f"""
    SELECT id, document_name, page_number, content_type, content, _score AS bm25_score
    FROM {collection_name}
    WHERE MATCH(content, '{keywords}')
    ORDER BY bm25_score DESC
    LIMIT {results_limit}
    """
    response = execute_cratedb_query(query)
    return response["rows"] if response and "rows" in response else []
```

##### Combine KNN and BM25 Results - Hybrid-Search

Combines KNN vector search and BM25 full-text search to retrieve the most relevant results.

``` python
def perform_hybrid_search(
    question, alpha=0.8, collection_name=COLLECTION_NAME, results_limit=RESULTS_LIMIT
):
    """
    Parameters:
    - question (str): The user's input question.
    - alpha (float): Weight for KNN scores in the hybrid scoring formula.
    - collection_name (str): The name of the database collection to search.
    - results_limit (int): The maximum number of results to return.

    Returns:
    - list: A list of rows containing the combined results, sorted by hybrid scores.

    Process:
    1. Generates a query embedding and extracts keywords.
    2. Performs KNN search and BM25 search independently.
    3. Normalizes scores and combines results with weighted averaging.
    4. Return the top results sorted by hybrid scores.
    """
    query_embedding = get_text_embedding(question)
    keywords = extract_keywords_pos(question)

    if DEBUG:
        print(f"\nExtracted Keywords for BM25: {keywords}\n")

    knn_results = knn_search(query_embedding, collection_name, results_limit)
    bm25_results = full_text_search(keywords, collection_name, results_limit)

    # Normalize and merge results
    knn_max = max(row[-1] for row in knn_results) if knn_results else 1
    bm25_max = max(row[-1] for row in bm25_results) if bm25_results else 1

    def normalize(score, max_score):
        return score / max_score if max_score > 0 else 0

    merged = {}
    for row in knn_results:
        merged[row[0]] = {"score": normalize(row[-1], knn_max) * alpha, "data": row}
    for row in bm25_results:
        if row[0] in merged:
            merged[row[0]]["score"] += normalize(row[-1], bm25_max) * (1 - alpha)
        else:
            merged[row[0]] = {
                "score": normalize(row[-1], bm25_max) * (1 - alpha),
                "data": row,
            }

    results = sorted(merged.values(), key=lambda x: x["score"], reverse=True)
    return [result["data"] for result in results[:results_limit]]
```

#### Answer Generation

``` python
def generate_answer(question, context):
    """
    Generates a concise and clear answer to the user's question based on the provided context.

    Parameters:
    - question (str): The user's input question.
    - context (str): The retrieved context containing relevant information.

    Returns:
    - str: A text response generated by OpenAI's GPT-3.5-turbo.
    - "I'm sorry, I couldn't generate an answer.": If the generation fails.

    Notes:
    - The function uses a structured prompt to guide the language model's response. Changing the prompt will have an effect on the answers provided by the chatbot.
    - Includes sources in the prompt to provide traceability in the answer.
    """
    prompt = f"""
    You are a skilled technical assistant. Use the following document context to answer the question concisely and clearly. Focus on the most relevant information. Avoid redundancy, but provide a full explanation. Include references to figures or images if mentioned:

    Context:
    {context}

    Question:
    {question}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating answer: {e}") if DEBUG else None
        return "I'm sorry, I couldn't generate an answer."
```

#### Build the Chatbot Pipeline

Processes a user query through the chatbot pipeline:
1. Performs hybrid search to retrieve relevant results.
2. Filters and formats the retrieved context with scores and metadata.
3. Generates a detailed answer using OpenAI's language model.

``` python
def chatbot_query(question):
    """
    Parameters:
    - question (str): The user's input question.

    Returns:
    - str: A formatted response containing the answer and references to sources.

    Debugging:
    - Prints intermediate steps (e.g., search results, context) when DEBUG is enabled.
    """
    results = perform_hybrid_search(question)
    if not results:
        return "No relevant documents found."

    print(f"DEBUG: Results structure: {results}") if DEBUG else None

    unique_context = set()
    hybrid_results_with_scores = []

    for result in results:
        print(f"DEBUG: Single result: {result}") if DEBUG else None
        # Dynamically unpack, focusing only on relevant fields
        _, doc_name, page_num, content_type, content, score, *_ = result

        # Convert score to float safely
        try:
            score = float(score)
        except ValueError:
            score = 0.0  # Default if score conversion fails

        # Prepare the context snippet
        context_snippet = f"Page {page_num} (Document: {doc_name}, Type: {content_type}, Score: {score:.4f})"

        if content not in unique_context:  # Avoid duplicates
            unique_context.add(content)
            hybrid_results_with_scores.append(context_snippet)

    # Combine context for LLM
    context = "\n".join(hybrid_results_with_scores)
    if DEBUG:
        print(f"\n### Retrieved Context with Scores ###\n{context}\n")

    # Generate the answer using the LLM
    answer = generate_answer(question, context)

    # Format the response with the answer in green
    formatted_response = f"{GREEN}{answer}{RESET}\n\nSources:\n" + "\n".join(
        hybrid_results_with_scores
    )
    return formatted_response
```

#### Chatbot interface

Provides an interactive command-line interface for the chatbot.

``` python
def chatbot_interface():
    """

    Process:
    1. Prompts the user to input a question.
    2. Calls `chatbot_query` to process the query and generate a response.
    3. Displays the answer and sources in a formatted style (answer in green).
    4. Exits gracefully when the user types "exit".

    Notes:
    - Designed for iterative question-answering with minimal latency.
    """
    print("\nWelcome to the PDF Data Chatbot!")
    while True:
        user_query = input("Ask a question (type 'exit' to quit): ").strip()
        if user_query.lower() == "exit":
            print("Goodbye!")
            break
        response = chatbot_query(user_query)
        print(f"\nAnswer:\n{response}\n")
```

#### Main function

``` python
if __name__ == "__main__":
    chatbot_interface()
```
</details>

#### Full `chatbot.py` script

<details>
<summary>Click to expand the full script</summary>

``` python
import os
import re
import requests
import spacy
from dotenv import load_dotenv
from openai import OpenAI
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()

CRATEDB_URL = os.getenv("CRATEDB_URL")
CRATEDB_USERNAME = os.getenv("CRATEDB_USERNAME")
CRATEDB_PASSWORD = os.getenv("CRATEDB_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = "pdf_data"
RESULTS_LIMIT = 3  # Number of results to return

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Instantiate OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Debug flag for debugging intermediate steps
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ANSI escape codes for formatting
GREEN = "\033[92m"
RESET = "\033[0m"


def execute_cratedb_query(query, args=None):
    data = {"stmt": query}
    if args:
        data["args"] = args

    response = requests.post(
        CRATEDB_URL, json=data, auth=HTTPBasicAuth(CRATEDB_USERNAME, CRATEDB_PASSWORD)
    )

    if response.status_code != 200:
        print(f"CrateDB query failed: {response.text}") if DEBUG else None
        return None
    return response.json()


def extract_keywords_pos(question):
    """
    Extract meaningful keywords from the question using POS tagging.
    """
    doc = nlp(question)
    keywords = [token.text for token in doc if token.pos_ in {"NOUN", "PROPN", "VERB"}]
    return " ".join(keywords)


def get_text_embedding(text, model="text-embedding-ada-002"):
    """
    Generates a vector embedding for a given text using OpenAI's embedding model.
    """
    try:
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}") if DEBUG else None
        return None

def knn_search(query_embedding, collection_name, results_limit=RESULTS_LIMIT):
    """
    Searches the vector index in CrateDB using a KNN algorithm.
    Parameters:
    - query_embedding: Vector embedding of the query
    - collection_name: Name of the database collection
    - results_limit: Number of results to return
    """
    embedding_string = ",".join(map(str, query_embedding))
    if DEBUG:
        print(
            f"\n### KNN Search Query Embedding (first 10): {query_embedding[:10]} ###\n"
        )

    query = f"""
    SELECT id, document_name, page_number, content_type, content, _score
    FROM {collection_name}
    WHERE knn_match(content_embedding, ARRAY[{embedding_string}], {results_limit})
    ORDER BY _score DESC
    LIMIT {results_limit}
    """
    response = execute_cratedb_query(query)
    if response and "rows" in response:
        if DEBUG:
            print(f"\n### KNN Search Results ({len(response['rows'])} rows): ###")
            for row in response["rows"]:
                print(f"Page {row[2]} (Score: {row[-1]}): {row[4][:200]}...")
        return response["rows"]
    return []

def full_text_search(keywords, collection_name, results_limit=RESULTS_LIMIT):
    """
    Searches the full-text index in CrateDB using BM25 (Best Matching 25) algorithm.

    Parameters:
    - keywords (str): The extracted keywords from the user's query.
    - collection_name (str): The name of the database collection to search.
    - results_limit (int): The maximum number of results to return.

    Returns:
    - list: A list of rows containing the matching records, including their scores and metadata.
    - Empty list: If no results are found or if the query fails.

    Debugging:
    - Prints the BM25 search query and results when DEBUG is enabled.
    """
    if DEBUG:
        print(f'\n### BM25 Search Query: "{keywords}" ###\n')

    query = f"""
    SELECT id, document_name, page_number, content_type, content, _score AS bm25_score
    FROM {collection_name}
    WHERE MATCH(content, '{keywords}')
    ORDER BY bm25_score DESC
    LIMIT {results_limit}
    """
    response = execute_cratedb_query(query)
    return response["rows"] if response and "rows" in response else []

def perform_hybrid_search(
    question, alpha=0.8, collection_name=COLLECTION_NAME, results_limit=RESULTS_LIMIT
):
    """
    Parameters:
    - question (str): The user's input question.
    - alpha (float): Weight for KNN scores in the hybrid scoring formula.
    - collection_name (str): The name of the database collection to search.
    - results_limit (int): The maximum number of results to return.

    Returns:
    - list: A list of rows containing the combined results, sorted by hybrid scores.

    Process:
    1. Generates a query embedding and extracts keywords.
    2. Performs KNN search and BM25 search independently.
    3. Normalizes scores and combines results with weighted averaging.
    4. Return the top results sorted by hybrid scores.
    """
    query_embedding = get_text_embedding(question)
    keywords = extract_keywords_pos(question)

    if DEBUG:
        print(f"\nExtracted Keywords for BM25: {keywords}\n")

    knn_results = knn_search(query_embedding, collection_name, results_limit)
    bm25_results = full_text_search(keywords, collection_name, results_limit)

    # Normalize and merge results
    knn_max = max(row[-1] for row in knn_results) if knn_results else 1
    bm25_max = max(row[-1] for row in bm25_results) if bm25_results else 1

    def normalize(score, max_score):
        return score / max_score if max_score > 0 else 0

    merged = {}
    for row in knn_results:
        merged[row[0]] = {"score": normalize(row[-1], knn_max) * alpha, "data": row}
    for row in bm25_results:
        if row[0] in merged:
            merged[row[0]]["score"] += normalize(row[-1], bm25_max) * (1 - alpha)
        else:
            merged[row[0]] = {
                "score": normalize(row[-1], bm25_max) * (1 - alpha),
                "data": row,
            }

    results = sorted(merged.values(), key=lambda x: x["score"], reverse=True)
    return [result["data"] for result in results[:results_limit]]

def generate_answer(question, context):
    """
    Generates a concise and clear answer to the user's question based on the provided context.

    Parameters:
    - question (str): The user's input question.
    - context (str): The retrieved context containing relevant information.

    Returns:
    - str: A text response generated by OpenAI's GPT-3.5-turbo.
    - "I'm sorry, I couldn't generate an answer.": If the generation fails.

    Notes:
    - The function uses a structured prompt to guide the language model's response. Changing the prompt will have an effect on the answers provided by the chatbot.
    - Includes sources in the prompt to provide traceability in the answer.
    """
    prompt = f"""
    You are a skilled technical assistant. Use the following document context to answer the question concisely and clearly. Focus on the most relevant information. Avoid redundancy, but provide a full explanation. Include references to figures or images if mentioned:

    Context:
    {context}

    Question:
    {question}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating answer: {e}") if DEBUG else None
        return "I'm sorry, I couldn't generate an answer."


def chatbot_query(question):
    """
    Parameters:
    - question (str): The user's input question.

    Returns:
    - str: A formatted response containing the answer and references to sources.

    Debugging:
    - Prints intermediate steps (e.g., search results, context) when DEBUG is enabled.
    """
    results = perform_hybrid_search(question)
    if not results:
        return "No relevant documents found."

    print(f"DEBUG: Results structure: {results}") if DEBUG else None

    unique_context = set()
    hybrid_results_with_scores = []

    for result in results:
        print(f"DEBUG: Single result: {result}") if DEBUG else None
        # Dynamically unpack, focusing only on relevant fields
        _, doc_name, page_num, content_type, content, score, *_ = result

        # Convert score to float safely
        try:
            score = float(score)
        except ValueError:
            score = 0.0  # Default if score conversion fails

        # Prepare the context snippet
        context_snippet = f"Page {page_num} (Document: {doc_name}, Type: {content_type}, Score: {score:.4f})"

        if content not in unique_context:  # Avoid duplicates
            unique_context.add(content)
            hybrid_results_with_scores.append(context_snippet)

    # Combine context for LLM
    context = "\n".join(hybrid_results_with_scores)
    if DEBUG:
        print(f"\n### Retrieved Context with Scores ###\n{context}\n")

    # Generate the answer using the LLM
    answer = generate_answer(question, context)

    # Format the response with the answer in green
    formatted_response = f"{GREEN}{answer}{RESET}\n\nSources:\n" + "\n".join(
        hybrid_results_with_scores
    )
    return formatted_response


def chatbot_interface():
    """

    Process:
    1. Prompts the user to input a question.
    2. Calls `chatbot_query` to process the query and generate a response.
    3. Displays the answer and sources in a formatted style (answer in green).
    4. Exits gracefully when the user types "exit".

    Notes:
    - Designed for iterative question-answering with minimal latency.
    """
    print("\nWelcome to the PDF Data Chatbot!")
    while True:
        user_query = input("Ask a question (type 'exit' to quit): ").strip()
        if user_query.lower() == "exit":
            print("Goodbye!")
            break
        response = chatbot_query(user_query)
        print(f"\nAnswer:\n{response}\n")

if __name__ == "__main__":
    chatbot_interface()        
```

</details>

### Step 8 Using the chatbot

When you combine all the pieces needed for the chatbot in a file named `chatbot.py`, you can start testing the functionality.

Execute the just created `chatbot.py` script. Like this:

``` bash
python chatbot.py
```

This will start the chatbot and give you a prompt like:

``` bash 
Welcome to the PDF Data Chatbot!
Ask a question (type 'exit' to quit): 
```

Then you can start asking questions like: `What is needed to build a knowledge assistant?`

``` bash 
Answer:
To build a knowledge assistant, you will need to refer to the document "How-to-Build-AI-driven-Knowledge-Assistants.pdf." Key information can be found on pages 4, 10, and 14 of the document. These pages likely contain details on the necessary steps, technologies, and processes involved in creating a knowledge assistant. It is essential to review these sections thoroughly to understand the requirements for building a knowledge assistant effectively.

Sources:
Page 10 (Document: How-to-Build-AI-driven-Knowledge-Assistants.pdf, Type: image, Score: 0.3408)
Page 4 (Document: How-to-Build-AI-driven-Knowledge-Assistants.pdf, Type: text, Score: 0.3396)
Page 14 (Document: How-to-Build-AI-driven-Knowledge-Assistants.pdf, Type: text, Score: 0.3394)
```

As you can see, the answer is nicely formulated, and 3 chunks (can be controlled by `RESULTS_LIMIT = 3`) of both text and image were matched. 

### Step 9 Building a UI on top of the chatbot

As a last step, we could build a simple web UI using Streamlit. Streamlit is an open-source Python framework that makes it easy to build and share beautiful, custom web applications for data analysis, machine learning, and AI workflows. With Streamlit, you can transform your Python scripts into interactive web apps with just a few lines of code—no web development experience is required.

Use the following code as an easy starting point. Safe this in a file `chatbot-UI.py` in the same directory as the `chatbot.py`.

<details>
<summary>Click to see the code</summary>

``` python
import streamlit as st
from chatbot import chatbot_query  # Import the chatbot function

# Configure the Streamlit page
st.set_page_config(
    page_title="Document QA Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"  # Sidebar minimized
)

# Add custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e8eaed;
        color: #000000;
    }
    .bot-message {
        background-color: #2b313e;
        color: #ffffff;
    }
    .source-info {
        font-size: 0.8rem;
        color: #b4b4b4;
        margin-top: 0.5rem;
        border-top: 1px solid #555;
        padding-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("📚 Document QA Chatbot")
st.markdown("Ask questions about your documents and get AI-powered answers with source references.")

# Chat input
user_query = st.chat_input("Ask a question...")

if user_query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Show a loading spinner while processing the response
    with st.spinner("Thinking..."):
        try:
            # Get chatbot response
            raw_response = chatbot_query(user_query)

            # Clean and parse response
            cleaned_response = raw_response.replace("\033[92m", "").replace("\033[0m", "").strip()
            
            # Add a single blank line before sources
            if "Sources:" in cleaned_response:
                cleaned_response = cleaned_response.replace("Sources:", "<br><strong>Sources:</strong>")
            
            # Append assistant response as a single message
            st.session_state.messages.append({"role": "assistant", "content": cleaned_response})

        except Exception as e:
            # Handle errors gracefully
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"An error occurred: {e}"
            })

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.container():
            st.markdown(f"""
                <div class="chat-message user-message">
                    <div><strong>You:</strong> {message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(f"""
                <div class="chat-message bot-message">
                    <div><strong>Assistant:</strong> {message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

# Add a clear chat button in the sidebar
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
```

This line **from chatbot import chatbot_query** is crucial as this tells Streamlit to import the `chatbot_query` from the `chatbot.py` script. 

</details>

### Step 10 Run the chatbot with UI

Start the streamlit application by executing the following:

``` bash
streamlit run chatbot-UI.py
```

This produces the following output:
``` bash
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.17:8501
```

If you are running this locally, then this will open the page in a browser automatically. Otherwise, open a browser tab and navigate to the URL shown in:
`Network URL: `

## Recap

In this guide, we explored how to build a PDF Knowledge Assistant step by step. Starting from extracting data from PDFs and indexing it in a database to creating an interactive chatbot that retrieves relevant information and provides concise, AI-powered answers. We also enhanced the experience by building a simple web-based UI using Streamlit, making it easier to interact with the assistant.

This implementation serves as a foundation for building AI-driven knowledge systems. Stay tuned for the next chapter in this blog series, where we’ll focus on Making a Production-Ready AI Knowledge Assistant, diving into scaling, optimizing, and securing your assistant for real-world deployment!

</details>

</details>
