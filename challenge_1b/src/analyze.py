# import json
# import os

# # --- File Paths ---
# # This tells the script where to find the input files inside the Docker container
# # The output from Challenge 1a will be in the /app/input directory
# INPUT_JSON_PATH = '/app/input/challenge1a_output.json'
# # The persona file will be in the /app/data directory
# PERSONA_PATH = '/app/data/persona.json'
# # This is where we will save our final analysis
# OUTPUT_PATH = '/app/output/challenge1b_output.json'

# def analyze_document():
#     """
#     This function performs the persona-based analysis.
#     """
#     print("✅ Starting analysis...")

#     # --- 1. Load the Persona ---
#     try:
#         with open(PERSONA_PATH, 'r') as f:
#             persona = json.load(f)
#             # Get the list of topics the persona is interested in
#             interests = persona.get("interests", [])
#             print(f"Persona '{persona.get('persona')}' is interested in: {interests}")
#     except FileNotFoundError:
#         print(f"❌ ERROR: Persona file not found at {PERSONA_PATH}")
#         return

#     # --- 2. Load the Structured Document (from Challenge 1a) ---
#     try:
#         with open(INPUT_JSON_PATH, 'r') as f:
#             document_structure = json.load(f)
#     except FileNotFoundError:
#         print(f"❌ ERROR: Input JSON from Challenge 1a not found at {INPUT_JSON_PATH}")
#         return

#     # --- 3. Analyze and Find Relevant Sections ---
#     print("🔎 Finding relevant sections based on persona's interests...")
#     relevant_sections = []
#     # Loop through all the elements (sections, paragraphs, etc.) in the document
#     for item in document_structure.get("elements", []):
#         # Check if the item has a 'Path' which is like a section title
#         path = item.get("Path", "")
#         # Check if any of the persona's interests are in the section title
#         if any(interest in path.lower() for interest in interests):
#             # If it's a match, get the text and add it to our list
#             text = item.get("Text", "No text available.")
#             relevant_sections.append({
#                 "section_title": path,
#                 "text": text
#             })
#             print(f"  -> Found relevant section: {path}")

#     # --- 4. Prepare the Final Output ---
#     final_output = {
#         "persona_analysis": {
#             "persona": persona.get("persona"),
#             "summary": f"Found {len(relevant_sections)} sections relevant to the persona's interests.",
#             "relevant_content": relevant_sections
#         }
#     }

#     # --- 5. Save the Output to a JSON file ---
#     # Ensure the output directory exists
#     os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
#     with open(OUTPUT_PATH,3 'w') as f:
#         json.dump(final_output, f, indent=4)

#     print(f"✅ Analysis complete. Output saved to {OUTPUT_PATH}")


# if __name__ == "__main__":
#     analyze_document()
import json
import os

# Get the collection name from an environment variable passed by Docker
# This makes our script reusable for collection_1, collection_2, etc.
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "collection_1")

# --- File Paths inside the Docker Container ---
# The JSON from Challenge 1a will be mounted here
INPUT_JSON_PATH = '/app/input/challenge1a_output.json'

# The path to the persona file will change based on the collection we are processing
PERSONA_PATH = f'/app/collections/{COLLECTION_NAME}/persona.json'

# The path where the final output will be saved
OUTPUT_PATH = f'/app/collections/{COLLECTION_NAME}/output.json'


def analyze_document():
    """
    Performs persona-based analysis using the output from Challenge 1a.
    """
    print(f"✅ Starting analysis for '{COLLECTION_NAME}'...")

    # 1. Load the Persona
    try:
        with open(PERSONA_PATH, 'r') as f:
            persona_data = json.load(f)
        interests = persona_data.get("interests", [])
        persona_name = persona_data.get("persona", "Unknown")
        print(f" Persona '{persona_name}' is interested in: {interests}")
    except FileNotFoundError:
        print(f"❌ ERROR: Persona file not found at {PERSONA_PATH}. Make sure it exists.")
        return

    # 2. Load the Structured Document from Challenge 1a
    try:
        with open(INPUT_JSON_PATH, 'r') as f:
            document_structure = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: Input JSON from Challenge 1a not found at {INPUT_JSON_PATH}.")
        print(" Ensure you have run Challenge 1a first and its output is available.")
        return

    # 3. Find Relevant Sections based on Persona's Interests
    print("🔎 Finding relevant sections...")
    relevant_content = []
    for element in document_structure.get("elements", []):
        # The 'Path' field often contains section titles or headings
        path = element.get("Path", "").lower()
        text = element.get("Text")
        if text and any(interest.lower() in path for interest in interests):
            relevant_content.append({
                "section_title": element.get("Path"),
                "text": text
            })
            print(f"  -> Found match in section: {element.get('Path')}")

    # 4. Create Final Output JSON
    final_output = {
        "persona_analysis": {
            "persona_used": persona_name,
            "collection": COLLECTION_NAME,
            "summary": f"Found {len(relevant_content)} sections relevant to the persona's interests.",
            "relevant_extracts": relevant_content
        }
    }

    # 5. Save the Output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(final_output, f, indent=4)

    print(f"✅ Analysis complete. Output saved to {OUTPUT_PATH} (locally in {COLLECTION_NAME}/output.json)")


if __name__ == "__main__":
    analyze_document()