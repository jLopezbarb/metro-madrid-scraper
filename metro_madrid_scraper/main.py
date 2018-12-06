from metro_madrid_scraper.spiders.download_coords import *
from metro_madrid_scraper.csv_functions import *
from metro_madrid_scraper.coord_file_functions import *
from metro_madrid_scraper.spiders.metro_scrapper import *

# Download Coordenates files
download_coords_files()
# Get all the metro information
metro_info = get_metro_info()
metro_info = set_coords(metro_info)
# Create csv
create_csv(metro_info)


