from bs4 import BeautifulSoup
import requests
import csv

OUTPUT_PATH = "companies.csv"
    
with open(OUTPUT_PATH, 'w+', newline='') as csvfile:
    fieldnames = ["ticker", "company", "mkt_cap"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    html_content = requests.get("https://stockanalysis.com/list/biggest-companies/").content
    sp = BeautifulSoup(html_content, "html.parser")
    tbl = sp.find(id="main-table")
    tbody = tbl.find("tbody").find_all("tr")

    for r in tbody:
        tds = r.find_all("td")        
        writer.writerow({'ticker': tds[1].text, "company": tds[2].text, "mkt_cap": tds[3].text})