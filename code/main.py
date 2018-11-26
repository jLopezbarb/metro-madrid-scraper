from code.download_coords import download_coords
from code import metro_scrapper as ms, csv_functions

# Download Coordenates files
download_coords()
# Get all the metro information
metro_info = ms.scrap_skeleton(ms.get_lines, ms.lines_url)
# Create csv
csv_functions.create_csv(metro_info)


