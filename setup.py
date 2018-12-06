from setuptools import setup, find_packages

setup(name='metro_madrid_scraper',
      version='1.0',
      description='Metro scraper for Madrid',
      author='Javier López Barba',
      author_email='j.lopezbarb@gmail.com',
      url='https://github.com/jLopezbarb/metro-madrid-scraper',
      packages=find_packages(exclude=('tests', 'docs')),
     )
