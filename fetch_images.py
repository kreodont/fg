import requests
url = 'https://www.dndbeyond.com/monsters'
result = requests.get(url)
print(result.text)