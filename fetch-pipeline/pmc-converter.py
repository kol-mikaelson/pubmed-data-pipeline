import pandas as pd
import requests

data = pd.read_csv("data/pmcdata/oa_comm_txt.incr.2025-05-14.filelist.csv")
print(data.head())
pmcids = list(data['AccessionID'])
print(pmcids)

base_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=wsai&email=purandhar@proton.me&format=json"

for pmcid in pmcids:
    url = f"{base_url}&ids={pmcid}"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to fetch data for PMCID {pmcid}, Status Code: {response.status_code}")
