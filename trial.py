from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url = "http://web.archive.org/web/20150322152114/http:/www.fda.gov/Safety/Recalls/EnforcementReports/2004/ucm120330.htm#"

# Takes the url and downloads the HTML data.
client = urlopen(url)

# read function can be used only once so we save the data into a var.
page_html = client.read()

# Closes the client once the data is HTML code is copied into the var.
client.close()

# Does the parsing of the HTML code. 
page_soup = bs(page_html, "html.parser")

# Collected all the dat in the form of a string.
data = page_soup.findAll("div", {"class":"middle-column"})

# Created a list of all the <p> tags within the data.
products = data[0].findAll("p")

for product in products:

    product = product.text

    if '# ' in product:

        splits = product.split('# ')
        ids = []
        recall_firm = ""
        manufacturing_firm = ""

        for i in range(1, len(splits)):
            if i == len(splits) - 1:
                ids.append(splits[i].split('.')[0])
            else:
                ids.append(splits[i].split(';')[0])
        
        if '.' in ids[len(ids) - 2]:
            ids.pop()
            ids[len(ids) - 1] = ids[len(ids) - 1].split('.')[0]

        temp = product.split('RECALLING FIRM/MANUFACTURER')[1].split('REASON')[0]

        if 'Firm:' in temp:
            temp1 = temp.split(':')
            recall_firm = temp1[1].split(', by')[0].split(',by')[0]
            manufacturing_firm = temp1[2].split('. Firm initiated recall is complete.')[0]

        else:
            recall_firm = temp.split(', by')[0].split(',by')[0]

        print(ids, recall_firm, manufacturing_firm)

    else:
        pass