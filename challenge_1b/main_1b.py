# In main_1b.py
import os
import json
from analyze import analyze_documents_for_persona

# The container will process one collection at a time.
# We'll map the collection folder to the /app/data directory.
DATA_DIR = "/app/data" 

if __name__ == "__main__":
    # 1. Load the persona from its JSON file
    with open(os.path.join(DATA_DIR, "persona.json"), 'r') as f:
        persona_data = json.load(f)
    persona = persona_data.get("description", "")

    # 2. Load the job-to-be-done from its JSON file
    with open(os.path.join(DATA_DIR, "job_to_be_done.json"), 'r') as f:
        job_data = json.load(f)
    job = job_data.get("description", "")

    # 3. Find all the PDF files in the 'documents' subfolder
    docs_dir = os.path.join(DATA_DIR, "documents")
    pdf_files = [os.path.join(docs_dir, f) for f in os.listdir(docs_dir) if f.lower().endswith(".pdf")]

    # 4. Run the analysis if all inputs are present
    if pdf_files and persona and job:
        result = analyze_documents_for_persona(pdf_files, persona, job)

        # 5. Write the output to a new file in the same collection folder
        output_path = os.path.join(DATA_DIR, "output.json")
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=4)
        
        print(f"✅ Analysis complete. Output saved to {output_path}")
    else:
        print("❌ Error: Missing PDFs, persona.json, or job_to_be_done.json")