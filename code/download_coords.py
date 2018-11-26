import os
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_coord_url = 'https://datos.madrid.es'


def download_coords():
    http = urllib3.PoolManager()
    response = http.request('GET', _coord_url + "/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/"
                                                "?vgnextoid=08055cde99be2410VgnVCM1000000b205a0aRCRD&"
                                                "vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD")
    soup = BeautifulSoup(response.data, 'html5lib')
    soup.find('li', {'class': 'asociada-item'}).find_all('li', {'class': 'asociada-item'})
    cleaned_div = [tag for tag in soup.find_all('li', {'class': 'asociada-item'}) if tag.select_one('p')]
    downloadable_file = [tuple((tag.select_one('ul').find('a', {'class': 'ico-kml'}, href=True)['href'],
                                tag.select_one('p').text.lower()))
                         for tag in cleaned_div if 'metro' in tag.select_one('p').text.lower()]
    [download_file(_coord_url+href[0], href[1]) for href in downloadable_file]


def download_file(url, file_name):
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)
    create_coord_dir()
    with open('coord_files/' + file_name.replace(' ', '_') + '.kml', 'wb') as out:
        while True:
            data = r.read()
            if not data:
                break
            out.write(data)


def create_coord_dir():
    if not os.path.exists('coord_files/'):
        os.makedirs('coord_files/')
