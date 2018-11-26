import io
import multiprocessing
import os
import re

import requests
import unidecode as unidecode

from code import models

from bs4 import BeautifulSoup

from code.models import Coord

lines_url = 'https://www.metromadrid.es'


def scrap_skeleton(procedure, url):
    """ Skeleton method used for every web scrapper
    :param procedure: python function to call
    :type procedure: method
    :param url: web to scrap
    :type url: str
    :return: The procedure return
    """
    retries = 0
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}
        response = requests.get(url, headers)
        print(url)
        if response.status_code == 200:
            return procedure(response)
        else:
            print('Requests status code for {0} was {1}'.format(url, str(response.status_code)))
    except requests.exceptions.Timeout:
        print('Timeout exception on {0}'.format(url))
        if retries < 3:
            scrap_skeleton(procedure, url)
    except requests.exceptions.TooManyRedirects:
        print('It seems that {0} is not correct'.format(url))
    except requests.exceptions.RequestException as e:
        print(e)


def get_lines(response):
    soup = BeautifulSoup(response.content, 'lxml')
    lines_section = soup.find('section', {'id': 'block-metro-network-status-block'})
    lines_tags = lines_section.find_all('a', href=True)
    lines_urls = [tuple((get_stations, lines_url + a_tag['href'])) for a_tag in lines_tags]
    with multiprocessing.Pool(os.cpu_count()) as p:
        lines = p.starmap(scrap_skeleton, lines_urls)
    return lines


def get_stations(response):
    soup = BeautifulSoup(response.content, 'lxml')
    line_name = soup.find('title').text
    line_name = line_name[:line_name.find('|')].strip()
    stations_div = soup.find('div', {'id': 'line-main'})
    metro_type = set_metro_type(line_name)
    stations_info = [get_station_info(station, metro_type) for station in stations_div.find_all('li')]

    return models.Line(line_name, metro_type, stations_info)


def set_metro_type(line_name):
    if line_name.startswith('Línea'):
        metro_type = 'Metro'
    elif line_name.startswith('ML'):
        metro_type = 'Metro Ligero'
    else:
        metro_type = 'Ramal'
    return metro_type


def get_station_info(station_info_div, metro_type):
    station_name = station_info_div.select_one('a > p').text
    station_rate_zone = station_info_div.select_one('span.icon-tarifa').text
    station_services = []
    if station_info_div.select_one('div.box__info-linea--estaciones'):
        station_services_tags = station_info_div.select_one('div.box__info-linea--estaciones') \
            .find_all('div', {'class': ['text__info-estacion',
                                        'text__info-estacion--tit-icon']})
        station_services = [tag.text.strip() for tag in station_services_tags]
    coord = get_coords(station_name, metro_type)
    return models.Station(station_name, station_rate_zone, station_services, coord)


def get_coords(station_name, metro_type):
    if metro_type is 'Metro' or metro_type is 'Ramal':
        file = 'coord_files/metro.kml'
    else:
        file = 'coord_files/metro_ligero.kml'
    data = io.open(file, encoding='latin-1').read()
    coord_soup = BeautifulSoup(data, 'lxml')
    placemark = coord_soup.select('placemark')
    lat, long = None, None
    for place in placemark:
        xml_station = place.select_one('name').text
        station_name = station_name.replace('-', ' ')
        if is_same_station(xml_station, station_name):
            lat, long = place.select_one('coordinates').text.split(',')
            long = long.strip()
            break;
    return Coord(lat, long)


def is_same_station(xml_station, metro_station):
    cleaned_xml_station = re.sub('^\d*\w?', '', xml_station.strip()).strip().lower()
    cleaned_xml_station = cleaned_xml_station.replace('-', ' ')
    cleaned_xml_station = re.sub('avda\.', 'avenida',cleaned_xml_station)
    metro_station = set_correct_station(metro_station)
    return unidecode.unidecode(cleaned_xml_station) == unidecode.unidecode(metro_station.lower())


def set_correct_station(metro_station):
    if metro_station.lower() == 'feria de madrid':
        metro_station = 'campo de las naciones'
    elif metro_station.lower() == 'estadio metropolitano':
        metro_station = 'estadio olimpico'
    elif metro_station.lower() == 'parque de lisboa':
        metro_station = 'parque lisboa'
    elif metro_station.lower() == 'aeropuerto t 4':
        metro_station = 'aeropuerto t4'
    return metro_station
