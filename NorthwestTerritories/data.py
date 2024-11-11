# -*- coding: utf-8 -*-
import csv
from bs4 import BeautifulSoup

html = '''<table>
<thead><tr class="field-heading-row">
<th class="name-heading">            <a class="column-sort name-heading-link" href="/app/cros-rsel/search?btnSearch=&amp;page=1&amp;reference=&amp;search_name=aa&amp;sort=name">Name</a>
</th>
<th class="entity-type-translated-heading">            <a class="column-sort entity-type-translated-heading-link" href="/app/cros-rsel/search?btnSearch=&amp;page=1&amp;reference=&amp;search_name=aa&amp;sort=entity_type_translated">Entity Type</a>
</th>
<th class="fileno-heading">            <a class="column-sort fileno-heading-link" href="/app/cros-rsel/search?btnSearch=&amp;page=1&amp;reference=&amp;search_name=aa&amp;sort=fileno">File No.</a>
</th>
<th class="jurisdiction-heading">            <a class="column-sort jurisdiction-heading-link" href="/app/cros-rsel/search?btnSearch=&amp;page=1&amp;reference=&amp;search_name=aa&amp;sort=jurisdiction">Jurisdiction</a>
</th>
<th class="name-type-heading">            <a class="column-sort name-type-heading-link" href="/app/cros-rsel/search?btnSearch=&amp;page=1&amp;reference=&amp;search_name=aa&amp;sort=name_type">Name Type</a>
</th>
<th class="real-status-heading">
          Status
        </th>        <th class="controls"></th>
</tr></thead><tbody><tr class="odd company" data-rapid-context="company:800005">                <td class="name-view">
					<span class="notranslate entity-name"><span class="view company-name ">TUDJAAT CO-OPERATIVE LIMITED</span></span>
</td>
                <td class="entity-type-translated-view">  <span class="view company-entity-type-translated ">Co-operative Association</span>
</td>
                <td class="fileno-view"><span class="view company-fileno ">800005</span></td>
                <td class="jurisdiction-view">  <span class="view company-jurisdiction ">Northwest Territories</span>
</td>
                <td class="name-type-view">  <span class="view company-name-type "></span>
</td>
                <td class="real-status-view">  <span class="view company-real-status ">Nunavut Entity</span>
</td>
<td class="controls">          
            
                  <a class="button" href="https://www.justice.gov.nt.ca/app/cros-rsel/login?redirect_to=https%3A%2F%2Fwww.justice.gov.nt.ca%2Fapp%2Fcros-rsel%2Fcompanies%2F5%2F0">Login to view</a>
        
        </td></tr><tr class="even company" data-rapid-context="company:500152">                <td class="name-view">
					<span class="notranslate entity-name"><span class="view company-name ">SAMBAA K&#x27;E DEVELOPMENT CORPORATION LTD.</span></span>
</td>
                <td class="entity-type-translated-view">  <span class="view company-entity-type-translated ">Corporation</span>
</td>
                <td class="fileno-view"><span class="view company-fileno ">500152</span></td>
                <td class="jurisdiction-view">  <span class="view company-jurisdiction ">Northwest Territories</span>
</td>
                <td class="name-type-view">  <span class="view company-name-type "></span>
</td>
                <td class="real-status-view">  <span class="view company-real-status ">In Compliance</span>
</td>
<td class="controls">          
            
                  <a class="button" href="https://www.justice.gov.nt.ca/app/cros-rsel/login?redirect_to=https%3A%2F%2Fwww.justice.gov.nt.ca%2Fapp%2Fcros-rsel%2Fcompanies%2F1%2F0">Login to view</a>
        
        </td></tr><tr class="odd company" data-rapid-context="company:500551">                <td class="name-view">
					<span class="notranslate entity-name"><span class="view company-name ">AARCTIC TOURS LTD.</span></span>
</td>
                <td class="entity-type-translated-view">  <span class="view company-entity-type-translated ">Corporation</span>
</td>
                <td class="fileno-view"><span class="view company-fileno ">500551</span></td>
                <td class="jurisdiction-view">  <span class="view company-jurisdiction ">Northwest Territories</span>
</td>
                <td class="name-type-view">  <span class="view company-name-type "></span>
</td>
                <td class="real-status-view">  <span class="view company-real-status ">Dissolved</span>
</td>
<td class="controls">          
            
                  <a class="button" href="https://www.justice.gov.nt.ca/app/cros-rsel/login?redirect_to=https%3A%2F%2Fwww.justice.gov.nt.ca%2Fapp%2Fcros-rsel%2Fcompanies%2F1%2F0">Login to view</a>
        
        </td></tr>
</tbody></table>'''

soup = BeautifulSoup(html, 'html.parser')

# Extracting table headers
headers = [th.get_text(strip=True) for th in soup.select('thead th')]

# Extracting table rows without the 'Login to view' button
rows = []
for row in soup.select('tbody tr'):
    columns = [td.get_text(strip=True) for td in row.find_all('td')[:-1]]  # Exclude the last column (button)
    rows.append(columns)

# Save to CSV
with open('table_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write headers
    writer.writerow(headers[:-1])  # Exclude the last header as well
    
    # Write data rows
    for row in rows:
        writer.writerow(row)

print("Data saved to 'table_data.csv'")
