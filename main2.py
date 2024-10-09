import requests
from bs4 import BeautifulSoup

url = 'https://maquinet.com/productos/maquinas-usadas.html?p=1'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, "html.parser")

regMaquinasWeb = soup.find_all("li", class_ = "item product product-item")


for i in range(len(regMaquinasWeb)):

#iteracion para cada div
    i = regMaquinasWeb[i]
    
    titleMaq = i.strong.a.text.strip()

    vendedorMaquina = i.find("div", class_ = "special-company")
    if vendedorMaquina:
        vendedorMaquina = i.find("div", class_ = "special-company").text.strip()
        vendedorMaquina= vendedorMaquina.replace("Empresa: ", "").strip()
    else:
        vendedorMaquina = "No disponible"

    precio = i.find("span", class_="price").text.strip()
    precio = precio.replace("US$\xa0", "").replace(",", "")


    ubicacionVentaPais = i.find("div", class_ = "country-item")
    if ubicacionVentaPais:
        ubicacionVentaPais = i.find("div", class_ = "country-item").text.strip()
    else: 
        ubicacionVentaPais = "No disponible"

    horometro = i.find("div", class_="special-attr special-attr-hours").text
    horometro = horometro.replace(" hrs", "").replace(",", "").strip()

    ubicacionVentaCiudad = i.find("div", class_="special-attr special-attr-loc").text.strip()

    marcaFabricante = i.find("div", class_="special-attr special-attr-brand").text.strip()

    añoFabricacion = i.find("div", class_="special-attr special-attr-year").text.strip()
    añoFabricacion = añoFabricacion.replace("Año: ", "").strip()

    linkWebSiteMaquina = i.find("a", class_ = "product photo product-item-photo").get("href").strip()

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

