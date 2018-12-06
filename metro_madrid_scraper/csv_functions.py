import csv
import os

headers = ['Estacion', 'Lineas', 'Zona tarifaria', 'Latitud', 'Longitud', 'Correspondencias', 'Conexiones']

csv_data = []
_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _get_services(lines):
    services = set()
    _create_csv_path()
    for line in lines:
        for station in line.stations:
            services |= set(station.services)
    [headers.append(service) for service in services]

def _create_csv_path():
    os.makedirs(os.path.join(_root_path, 'csv_result'), exist_ok=True)


def _get_csv_rows(lines):
    csv_data.append(headers)
    for line in lines:
        for station in line.stations:
            data = dict((el, False) for el in headers)
            data['Estacion'] = station.name
            data['Lineas'] = line.name
            data['Zona tarifaria'] = station.station_rate_zone
            data['Latitud'] = station.coord.lat
            data['Longitud'] = station.coord.long
            data['Correspondencias'] = station.get_correspondences()
            data['Conexiones'] = station.get_conections()
            for service in station.services:
                data[service] = True
            csv_data.append(list(data.values()))


def _write_csv():
    csv_path = os.path.abspath(os.path.join(os.path.join(_root_path, "csv_result"), "metro_madrid.csv"))
    with open(csv_path, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_data)
    csvFile.close()


def create_csv(lines):
    _get_services(lines)
    _get_csv_rows(lines)
    _write_csv()

