# In main.py
import os
import json
from extract import extract_pdf_outline

# These paths are INSIDE the Docker container
INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

if __name__ == "__main__":
    # Loop through every file in the input directory
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            
            # Run the extraction function from our other file
            result = extract_pdf_outline(pdf_path)
            
            # Create the name for the output JSON file
            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            # Write the result to the new JSON file
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=4)
            
            print(f"✅ Processed {filename} -> {output_filename}")