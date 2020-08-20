# Covid19-incisive

## Getting Started

Covid19-incisive is a web application that provides information about Corona Cases in the Country and also gives the cases at your location by tracking your IP. This also visualises the data. The next version is a dexterous Python application that predicts the end of Coronavirus cases in the states and in the country.

### Prerequisites

```
1. Django
2. BS4 (Beautiful Soup)
3. GeoIP2
4. Plotly
5. Django Dash Plotly
```

### Installing

1. Install Python
```
https://www.python.org/downloads/
```
2. Install Django
```
pip install django
```
3. Install bs4
```
pip install bs4
```
4. Install geoip2
```
pip install geoip2
```
5. Install plotly
```
pip install plotly
```
6. Install Django Dash Plotly
```
pip install django_plotly_dash
```
7. Install Channel and Redis
```
pip install channels daphne redis django-redis channels-redis
```

## Downloads
* Map GeoJson Data - https://un-mapped.carto.com/tables/states_india/public/map
* GeoIP2 Database - https://www.maxmind.com/en/geoip2-databases

## Deployment

* Run this code on local host using 127.0.0.1:8000/
* If hosting on the internet, then remove the ip definition from views.py

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [BS4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Beautiful Soup (A Web Scraping Tool)
* [GeoIP2](https://www.maxmind.com/en/geoip2-databases) - GeoIP databases
* [Plotly](https://plot.ly/python/) - Data Viusalization Library for Python
* [Dash Plotly](https://dash.plot.ly/) - Python Framework for Plotly
* [Django Plotly Dash](https://django-plotly-dash.readthedocs.io/en/latest/index.html) - Django Dash Plotly Integration
* [Tailwind CSS](https://tailwindcss.com/) - Fast UI
* [Tail Blocks](https://mertjf.github.io/tailblocks/) - Fast UI


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* Thank you Tailwind CSS and Tailblocks for speedy UI and to the developers of Django Dash Plotly integration library.
