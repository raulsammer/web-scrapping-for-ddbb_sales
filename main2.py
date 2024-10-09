import requests
from bs4 import BeautifulSoup

url = 'https://maquinet.com/productos/maquinas-usadas.html?p=1'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, "html.parser")

regMaquinasWeb = soup.find_all("li", class_ = "item product product-item")


for one in range(len(regMaquinasWeb)):


    one = regMaquinasWeb[one]
    
    titleMaq = one.strong.a.text.strip()

    vendedorMaquina = one.find("div", class_ = "special-company").text.strip()
    vendedorMaquina= vendedorMaquina.replace("Empresa: ", "").strip()


    precio = one.find("span", class_="price").text.strip()
    precio = precio.replace("US$\xa0", "").replace(",", "")

    ubicacionVentaPais = one.find("div", class_ = "country-item").text

    horometro = one.find("div", class_="special-attr special-attr-hours").text
    horometro = horometro.replace(" hrs", "").replace(",", "").strip()

    ubicacionVentaCiudad = one.find("div", class_="special-attr special-attr-loc").text.strip()

    marcaFabricante = one.find("div", class_="special-attr special-attr-brand").text.strip()

    añoFabricacion = one.find("div", class_="special-attr special-attr-year").text.strip()
    añoFabricacion = añoFabricacion.replace("Año: ", "").strip()

    linkWebSiteMaquina = one.find("a", class_ = "product photo product-item-photo").get("href").strip()

    print("link:", linkWebSiteMaquina)
    print("Nombre de la máquina:", titleMaq, "\n")

"""    # Vendedor de la máquina (empresa)
    print("Vendedor:", vendedorMaquina)

    # Precio de la máquina
    print("Precio:", precio)

    # Ubicación del país de venta
    print("País de venta:", ubicacionVentaPais)

    # Horómetro (cantidad de horas)
    print("Horómetro:", horometro)

    # Ubicación de la ciudad de venta
    print("Ciudad de venta:", ubicacionVentaCiudad)

    # Marca del fabricante
    print("Marca del fabricante:", marcaFabricante)

    # Año de fabricación
    print("Año de fabricación:", añoFabricacion)"""

