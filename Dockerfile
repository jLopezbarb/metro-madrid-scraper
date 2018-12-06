FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app/
WORKDIR /usr/src/app/

RUN python setup.py install

VOLUME ["/usr/src/app/csv_result/"]

CMD [ "python", "./metro_madrid_scraper/main.py" ]