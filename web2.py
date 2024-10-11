import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.be-market.com/tiendaonline/webapp/search?parametro=&pagina=1&pais:PER%C3%9A'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

titlesMaq = []
vendedoresMaquina = []
precios = []
ubicacionesVentaPais = []
horometros = []
ubicacionesVentaCiudad = []
marcasFabricante = []
añosFabricacion = []
linksWebSiteMaquina = []

regMaquinaWeb = soup.find_all('li', class_='columnas__item', attrs={'ng-repeat': 'producto in productos'})

print(len(regMaquinaWeb))


