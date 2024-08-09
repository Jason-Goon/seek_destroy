import os
import shutil
import json
import git  # Ensure you have the GitPython package installed

# Configuration
TEMPLATE_REPO_URL = 'https://github.com/Jason-Goon/cafe.git'  # URL of the template repository
TEMPLATE_BRANCH = 'main'  # Branch to pull (default to 'main' if no specific branch is needed)
TEMPLATE_DIR = './template-repo'  # Local path to clone the template repository
OUTPUT_DIR = './output-sites'  # Directory to store the pitch sites

# Function to clone the template repository
def clone_template_repo():
    if os.path.exists(TEMPLATE_DIR):
        shutil.rmtree(TEMPLATE_DIR)
    repo = git.Repo.clone_from(TEMPLATE_REPO_URL, TEMPLATE_DIR, branch=TEMPLATE_BRANCH)
    print(f"Cloned template repository from {TEMPLATE_REPO_URL} to {TEMPLATE_DIR}")

# Function to replace placeholders in the template
def populate_template(json_data, template_file, output_file):
    with open(template_file, 'r') as file:
        content = file.read()

    # Replace placeholders with actual data or default values
    content = content.replace("{{PLACE_NAME}}", json_data.get('name', 'Cafe Name'))
    content = content.replace("{{ADDRESS}}", json_data.get('address', 'Address not available'))
    content = content.replace("{{EMAIL}}", json_data.get('gmail', 'email@example.com'))
    content = content.replace("{{DESCRIPTION}}", json_data.get('description', 'No description available'))
    content = content.replace("{{FACEBOOK_LINK}}", 'https://facebook.com')  # Placeholder value
    content = content.replace("{{INSTAGRAM_LINK}}", 'https://instagram.com')  # Placeholder value
    content = content.replace("{{OPERATING_HOURS}}", 'Mon-Sun: 9:00 AM - 5:00 PM')  # Placeholder value
    content = content.replace("{{MAP_EMBED_LINK}}", 'https://maps.google.com')  # Placeholder value

    # Write the modified content to the output file
    with open(output_file, 'w') as file:
        file.write(content)

# Main function to process the JSON data and create pitch sites
def main():
    json_file_path = input("Enter the path to your JSON file (default: ./JSON/jason.json): ") or './JSON/jason.json'
    
    # Clone the template repository
    clone_template_repo()
    
    # Load JSON data
    with open(json_file_path, 'r') as file:
        json_data_list = json.load(file)

    # Process each JSON object
    for json_data in json_data_list:
        site_name = json_data['name'].replace(' ', '_')
        output_site_dir = os.path.join(OUTPUT_DIR, f"pitch-site-{site_name}")
        
        # Check if the output directory already exists
        if os.path.exists(output_site_dir):
            print(f"Directory {output_site_dir} already exists. Skipping...")
            continue

        # Copy the entire template directory to a new location
        shutil.copytree(TEMPLATE_DIR, output_site_dir)
        
        # Populate the template with JSON data
        template_file = os.path.join(output_site_dir, 'src', 'index.html')
        populate_template(json_data, template_file, template_file)
        
        print(f"Pitch site created at {output_site_dir}")

if __name__ == "__main__":
    main()
