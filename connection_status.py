import requests

# Function that checks connection status and proceed for extracting data
def Connection_Status(url):
    page = requests.get(url,timeout=100, headers={'User-Agent': 'Mozilla/5.0'})
    connection_status_code = page.status_code
    return (page, connection_status_code)
