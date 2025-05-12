import requests
import time
import sqlite3

# Define the API URL
API_URL = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/pubtator?pmids="

def fetch_pubmed_data_to_db(pubmed_ids_file, db_file):
    """
    Fetches data for a list of PubMed IDs from the API and stores the results in an SQLite database.
    Limits requests to 2 per second to comply with rate limiting.

    :param pubmed_ids_file: Path to the file containing PubMed IDs (one per line).
    :param db_file: Path to the SQLite database file where the API responses will be stored.
    """
    try:
        # Connect to SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create a table to store PubMed data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pubmed_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pubmed_id TEXT UNIQUE,
                xml_data TEXT
            )
        """)
        conn.commit()

        # Read PubMed IDs from the input file
        with open(pubmed_ids_file, 'r') as file:
            pubmed_ids = [line.strip() for line in file if line.strip()]

        for pmid in pubmed_ids:
            # Make the API call for each PubMed ID
            response = requests.get(f"{API_URL}{pmid}")
            
            if response.status_code == 200:
                # Insert the PubMed ID and XML data into the database
                try:
                    cursor.execute("""
                        INSERT INTO pubmed_data (pubmed_id, xml_data)
                        VALUES (?, ?)
                    """, (pmid, response.text))
                    conn.commit()
                except sqlite3.IntegrityError:
                    print(f"PubMed ID {pmid} already exists in the database. Skipping.")
            else:
                print(f"Failed to fetch data for PubMed ID {pmid}: {response.status_code}")

            # Limit requests to 2 per second
            time.sleep(0.5)  # 0.5 seconds = 2 requests per second

        print(f"Data fetching complete. Results saved to {db_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    input_file = "pubmed_ids.txt"  # File containing PubMed IDs
    database_file = "pubmed_data.db"  # SQLite database file
    fetch_pubmed_data_to_db(input_file, database_file)
