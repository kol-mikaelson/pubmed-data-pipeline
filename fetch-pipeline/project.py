from pycaprio import Pycaprio
import os
from concurrent.futures import ThreadPoolExecutor

client = Pycaprio("http://localhost:8080/", authentication=("remote", "remoteuser"))

# List projects
project_name = "finalnerproject1234"
existing_projects = client.api.projects()
try:
    new_project = client.api.create_project(project_name)
except Exception as e:
    print(f"An error occurred while creating the project: {e}")
    new_project = None


from pycaprio.mappings import InceptionFormat, DocumentState

# Function to process a single file
def process_file(file_path, filename):
    if os.path.getsize(file_path) == 0:
        print(f"Ignored empty file: {filename}")
        return
    with open(file_path, 'rb') as document_file:
        try:
            new_document = client.api.create_document(
                new_project, 
                filename, 
                document_file, 
                document_format="conll2002",
            )
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")

# Import all files from a given directory in CONLL 2002 format using multi-threading
directory_path = "data/conll_out_title/"
with ThreadPoolExecutor() as executor:
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            executor.submit(process_file, file_path, filename)