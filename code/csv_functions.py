import csv

headers = ['Estacion', 'Lineas', 'Zona tarifaria', 'Latitud', 'Longitud']

csv_data = []


def _get_services(lines):
    services = set()
    for line in lines:
        for station in line.stations:
            services |= set(station.services)
    [headers.append(service) for service in services]


#TODO If station exist now it removes last occurence
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
            for service in station.services:
                data[service] = True
            csv_data.append(list(data.values()))


def _write_csv():
    with open('metro.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_data)
    csvFile.close()


def create_csv(lines):
    _get_services(lines)
    _get_csv_rows(lines)
    _write_csv()
