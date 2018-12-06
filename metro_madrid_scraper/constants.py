import os


class CommonConstant:
    CPU_CORES = os.cpu_count()


class CoordScraperConst(CommonConstant):
    URL = 'https://datos.madrid.es'
    URN = "/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/" \
          "?vgnextoid=08055cde99be2410VgnVCM1000000b205a0aRCRD&" \
          "vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD"
    COORD_DIRECTORY = 'coord_files/'


class MetroScraperConst(CommonConstant):
    URL = 'https://www.metromadrid.es'
    HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/52.0.2743.82 Safari/537.36"}


class KmlSwitcher(CommonConstant):
    METRO_NAMES = {'feria de madrid': 'campo de las naciones',
                  'estadio metropolitano': 'estadio olimpico',
                  'parque de lisboa': 'Parque Lisboa',
                  'aeropuerto t 4': 'Aeropuerto T4',
                  'estación del arte': 'Atocha',
                  'vicente aleixandre': 'metropolitano',
                  'villaverde bajo-cruce': 'Villaverde Bajo Cruce',
                  'atocha-renfe': 'Atocha Renfe',
                  'aeropuerto t1-t2-t3': 'Aeropuerto T1 T2 T3',
                  'aeropuerto t-4': 'Aeropuerto T4'}
