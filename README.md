Adobe India Hackathon 2025 - Connecting the Dots
Team: [Om Singh | Govind Jee]

Solution Overview
This project provides a complete solution for Round 1 of the "Connecting the Dots" challenge. It's a two-stage system designed to first understand a document's structure and then analyze its content from a specific point of view.

Challenge 1A: Outline Extractor

A fast, Dockerized service that ingests raw PDFs and extracts a structured, hierarchical outline (e.g., Titles, Headings, Paragraphs) into a machine-readable JSON format.

Challenge 1B: Persona-Driven Intelligence

An intelligent analysis engine that uses the structured JSON from Challenge 1A. It analyzes the content from the perspective of a defined "persona" (e.g., a student, a researcher) to find and rank the most relevant sections based on that persona's interests.

The entire solution is designed to run efficiently on a CPU, completely offline, and within the specified resource constraints.

Project Structure
.
├── challenge_1a/
│   ├── input/                # Place source PDFs for 1a here
│   ├── output/               # Structured JSON from 1a appears here
│   ├── Dockerfile_1a
│   └── ... (1a source code)
├── challenge_1b/
│   ├── collection_1/
│   │   ├── persona.json      # Persona definition
│   │   └── output.json       # Final analysis for this collection
│   ├── collection_2/
│   ├── collection_3/
│   ├── src/
│   │   └── analyze.py        # Main analysis script for 1b
│   └── Dockerfile
└── README.md
Libraries and Models Used
Python 3.9: The core programming language.

PyMuPDF (fitz): Used for its high-speed and accurate parsing of PDF text and font properties, essential for structural analysis in Round 1A.

Sentence-Transformers: The core library for the semantic analysis in Round 1B.

all-MiniLM-L6-v2 Model: A pre-trained sentence-embedding model used for ranking. It was chosen for its excellent balance of performance, speed on a CPU, and small size (<1GB), perfectly fitting the hackathon's constraints.

Docker: Used for containerizing the applications to ensure a consistent and reproducible runtime environment.

How to Build and Run the Solution
This is a two-step process. You must run Challenge 1A first to generate the input needed for Challenge 1B.

Step 1: Run Challenge 1A (Extract PDF Structure)
This stage converts a PDF into a structured JSON file.

Place PDFs: Put the PDF files you want to analyze into the challenge_1a/input/ folder.

Build the Docker Image:

Bash

docker build -t adobe-hackathon-1a -f challenge_1a/Dockerfile_1a .
Run the Container:

Bash

docker run --rm \
-v "$(pwd)/challenge_1a/input:/app/input" \
-v "$(pwd)/challenge_1a/output:/app/output" \
adobe-hackathon-1a
The structured JSON output (e.g., challenge1a_output.json) will be created in the challenge_1a/output/ folder.

Step 2: Run Challenge 1B (Persona-Driven Analysis)
This stage uses the JSON file from Step 1 to perform a persona-based analysis.

Build the Docker Image:

Bash

docker build -t adobe-hackathon-1b -f challenge_1b/Dockerfile .
Run Analysis for each Collection:
Run the container for each collection. The command uses an environment variable (-e COLLECTION_NAME) to specify which persona to use. The output is saved directly into the corresponding collection folder.

For Collection 1:

Bash

docker run --rm \
-e COLLECTION_NAME=collection_1 \
-v "$(pwd)/challenge_1a/output:/app/input" \
-v "$(pwd)/challenge_1b:/app/collections" \
-v "$(pwd)/challenge_1b/src:/app/src" \
adobe-hackathon-1b python /app/src/analyze.py
For Collection 2:

Bash

docker run --rm \
-e COLLECTION_NAME=collection_2 \
-v "$(pwd)/challenge_1a/output:/app/input" \
-v "$(pwd)/challenge_1b:/app/collections" \
-v "$(pwd)/challenge_1b/src:/app/src" \
adobe-hackathon-1b python /app/src/analyze.py
For Collection 3:

Bash

docker run --rm \
-e COLLECTION_NAME=collection_3 \
-v "$(pwd)/challenge_1a/output:/app/input" \
-v "$(pwd)/challenge_1b:/app/collections" \
-v "$(pwd)/challenge_1b/src:/app/src" \
adobe-hackathon-1b python /app/src/analyze.py
After running, a final output.json file will be generated inside each collection folder.