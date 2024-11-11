from DrissionPage import ChromiumPage
import time
# Initialize a ChromiumPage instance
page = ChromiumPage()

# Open a webpage
page.get('https://www.sos.ok.gov/corp/corpInquiryFind.aspx')


time.sleep(10000000)

# Close the page when done
page.close()