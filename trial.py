from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re
import pandas as pd

# Will add for taking urls from the xlsx sheet later.
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = "FDA Enforcement URLs.xlsx"
path = dir_path + '\\' + file_name

f = open("sample.txt","w+")

df = pd.read_excel(path, headers = 0)
urls = df['url'].to_list()
for url in urls:
    print(url)
    print(url, file = f)
    if 'Product-Tabs' in url:
        pass
    elif '#' in url:
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

            # For filtering only the products.
            if 'PRODUCT ' in product and 'CODE' in product:

                # Initializing the variables to store the required information.
                ids = []
                recall_firm = ""
                manufacturing_firm = ""
                
                # To capture the IDs.
                splits = product.split('PRODUCT')[1].split("CODE")[0]
                if 'Recall' in splits:
                    splits = splits.split('Recall')
                elif 'recall' in splits:
                    splits = splits.split('recall')
                elif 'Safety Alert' in splits:
                    splits = splits.split('Safety Alert')
                elif 'Unit' in splits:
                    splits = splits.split('Unit')

                # Observed that every ID has either ';' or '.' at the end. So splitting based on that.
                for i in range(1, len(splits)):
                    if i == len(splits) - 1:
                        ids.append(splits[i].split('.')[0].split(';')[0])
                    else:
                        ids.append((splits[i].split(';')[0]).split('.')[0].split(':')[0].split('b')[0].split('c')[0])

                # Capture all IDs in the required format. TO take all cases into consideration used two if's. 
                for i in range(len(ids)):
                    if '#' in ids[i]:
                        ids[i] = ids[i].split('#')[1]
                    if ' ' in ids[i]:
                        ids[i] = ids[i][1:]

                # if len(ids) == 0:
                #     splits = product.split('PRODUCT')[1].split('CODE')[0]
                #     ids = re.findall(r'([A-Z](-[0-9]+)+)', splits)
                #     for i in range(len(ids)):
                #         ids[i] = ids[i][0]
                #     ids.extend(re.findall(r'[A-Z][0-9]+-[0-9]+', splits))

                # Always the name of the firm is between the two strings in the function split.
                temp = ''
                if 'RECALLING FIRM' in product:
                    temp = product.split('RECALLING FIRM')[1].split('REASON')[0]
                elif 'RESPONSIBLE FIRM' in product:
                    temp = product.split('RESPONSIBLE FIRM')[1].split('REASON')[0]
                else:
                    pass

                if '/MANUFACTURER' in temp:
                    temp = temp.split('/MANUFACTURER')[1]
                elif 'FIRM/MANUFACTURER' in temp:
                    temp = temp.split('FIRM/MANUFACTURER')[1]

                # If 'Firm:' is present in this part it means the recalling firm and manufacturing firms are different else we have only recalling firm information.
                flag = False
                if 'Manufacturing Firm:' in temp:
                    temp1 = temp.split('Manufacturing Firm:')
                    flag = True
                elif 'Manufacturer:' in temp:
                    temp1 = temp.split('Manufacturer:')
                    flag = True
                else:
                    if ':' in temp:
                        temp1 = temp.split(':')
                        recall_firm = temp1[1].split(', by')[0].split(',by')[0]
                    else:
                        recall_firm = temp.split(', by')[0].split(',by')[0]
                if flag:
                    if 'Firm:' in temp1[0]:
                        temp2 = temp1[0].split(', by')[0].split(',by')[0].split('Firm:')
                        if len(temp2) == 2:
                            recall_firm = temp2[1]
                    else:
                        recall_firm = temp1[0].split(', by')[0].split(',by')[0]
                    
                    if '. Firm initiated recall is complete.' in temp1[1]:
                        manufacturing_firm = temp1[1].split('. Firm initiated recall is complete.')[0]
                    elif 'Firm initiated recall is ongoing.' in temp1[1]:
                        manufacturing_firm = temp1[1].split('Firm initiated recall is ongoing.')[0]
                    elif 'Firm initiated recall isongoing.' in temp1[1]:
                        manufacturing_firm = temp1[1].split('Firm initiated recall isongoing.')[0]

                # Printing to test. Will convert it into csv in the end after making rows instead of separate variables using pandas.
                print(ids, recall_firm, manufacturing_firm)
                print(ids, recall_firm, manufacturing_firm, file = f)

            else:
                pass

    else:
        pass