import sqlite3

# Example usage
def query_pubmed_data(db_file, pubmed_id):
    """
    Queries the SQLite database for a specific PubtheMed ID.

    :param db_file: Path to the SQLite database file.
    :param pubmed_id: The PubMed ID to query.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT xml_data FROM pubmed_data WHERE pubmed_id = ?", (pubmed_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        print(f"XML Data for PubMed ID {pubmed_id}:\n{result[0]}")
        return result[0]
    else:
        print(f"No data found for PubMed ID {pubmed_id}")
        return "0"
        
        



    
    



if __name__ == "__main__":
     data = query_pubmed_data("data/pubmed_data.db", "16602100") # Replace with a valid PubMed ID
     if data != "0":
         with open("output.txt", "w") as file:
             file.write(data)
         print("Data saved to output.txt")
