from bs4 import BeautifulSoup
import requests
import csv

OUTPUT_PATH = "companies.csv"
URL = "https://stockanalysis.com/list/biggest-companies/"
    
with open(OUTPUT_PATH, 'w+', newline='') as csvfile:
    fieldnames = ["ticker", "company", "mkt_cap"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    html_content = requests.get(URL).content
    sp = BeautifulSoup(html_content, "html.parser")
    tbl = sp.find(id="main-table")
    tbody = tbl.find("tbody")

    for tr in tbody.find_all("tr"):
        tds = tr.find_all("td")        
        writer.writerow({'ticker': tds[1].text, "company": tds[2].text, "mkt_cap": tds[3].text})