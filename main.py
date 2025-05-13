
import requests
import time
import os

# Define the API URL
API_URL = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/pubtator?pmids="

def fetch_pubmed_data_to_files(pubmed_ids_file, output_dir):
    """
    Fetches data for a list of PubMed IDs from the API and stores the results as .txt files.
    Limits requests to 2 per second to comply with rate limiting.

    :param pubmed_ids_file: Path to the file containing PubMed IDs (one per line).
    :param output_dir: Directory where the API responses will be stored as .txt files.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Read PubMed IDs from the input file
        with open(pubmed_ids_file, 'r') as file:
            pubmed_ids = [line.strip() for line in file if line.strip()]

        for pmid in pubmed_ids:
            # Make the API call for each PubMed ID
            response = requests.get(f"{API_URL}{pmid}")

            if response.status_code == 200:
                # Write the response to a .txt file named after the PubMed ID
                output_file = os.path.join(output_dir, f"{pmid}.txt")
                with open(output_file, 'w') as f:
                    f.write(response.text)
            else:
                print(f"Failed to fetch data for PubMed ID {pmid}: {response.status_code}")

            # Limit requests to 2 per second
            time.sleep(0.5)  # 0.5 seconds = 2 requests per second

        print(f"Data fetching complete. Results saved to {output_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "data/pubmed_ids.txt"  # File containing PubMed IDs
    output_directory = "data/pubmed_responses"  # Directory to store .txt files
    fetch_pubmed_data_to_files(input_file, output_directory)

