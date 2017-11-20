import requests
import shutil
from bs4 import BeautifulSoup

for page_number in range(1, 42):
    print('Page %s' % page_number)
    url = 'https://www.dndbeyond.com/monsters?page=%s' % page_number
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html5lib")
    monsters_list = soup.find_all('div', {'data-type': 'monsters'})
    for monster in monsters_list:
        name = monster.find('a', {'class': 'link'}).contents[0]
        image_div = monster.find('div', {'class': 'row monster-icon'}).find('a')
        if not image_div:
            print('%s has no picture' % name)
            continue
        image_link = image_div['href']
        print('%s %s' % (name, image_link))
        try:
            response = requests.get(image_link, stream=True)
            with open('%s.jpg' % name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        except Exception as e:
            print(e)
