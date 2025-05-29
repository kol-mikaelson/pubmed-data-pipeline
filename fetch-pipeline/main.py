import requests
import time
import os

API_URL = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/pubtator?pmids="

def fetch_pubmed_data_to_files(pubmed_ids_file, output_dir):

    try:
        os.makedirs(output_dir, exist_ok=True)

        with open(pubmed_ids_file, 'r') as file:
            pubmed_ids = [line.strip() for line in file if line.strip()]

        for pmid in pubmed_ids:
            response = requests.get(f"{API_URL}{pmid}")

            if response.status_code == 200:
                output_file = os.path.join(output_dir, f"{pmid}.txt")
                with open(output_file, 'w') as f:
                    f.write(response.text)
            else:
                print(f"Failed to fetch data for PubMed ID {pmid}: {response.status_code}")

            time.sleep(0.5)  

        print(f"Data fetching complete. Results saved to {output_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "data/pubmed_ids.txt"  
    output_directory = "data/pubmed_responses_test"  
    fetch_pubmed_data_to_files(input_file, output_directory)

