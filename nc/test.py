from bs4 import BeautifulSoup

# Sample HTML content
html_content = '''
<header>
    <h2 class="section-title">
        Business Corporation <br>
    </h2>
</header>
'''

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extract text from the h2 tag with class 'section-title'
section_title = soup.find('h2', class_='section-title').get_text(strip=True)

# Print the extracted text
print(section_title)
