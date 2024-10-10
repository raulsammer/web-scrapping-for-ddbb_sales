import requests
from bs4 import BeautifulSoup

# Función para obtener el contenido de la página web
def webView():
    url = 'https://maquinet.com/productos/maquinas-usadas.html?p=1'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    
    return soup.find_all("li", class_="item product product-item")

# Listas para almacenar los datos
titlesMaq = []
vendedoresMaquina = []
precios = []
ubicacionesVentaPais = []
horometros = []
ubicacionesVentaCiudad = []
marcasFabricante = []
añosFabricacion = []
linksWebSiteMaquina = []

# Función para extraer y guardar los datos en las listas
def scrappingData(regMaquinasWeb):
    for maquina in regMaquinasWeb:
        # Nombre de la máquina
        titleMaq = maquina.strong.a.text.strip()
        titlesMaq.append(titleMaq)
        
        # Vendedor de la máquina
        vendedorMaquina = maquina.find("div", class_="special-company")
        if vendedorMaquina:
            vendedorMaquina = vendedorMaquina.text.strip().replace("Empresa: ", "")
            vendedoresMaquina.append(vendedorMaquina)
        else:
            vendedoresMaquina.append("No disponible")
        
        # Precio de la máquina
        precio = maquina.find("span", class_="price").text.strip()
        precio = precio.replace("US$\xa0", "").replace(",", "")
        precios.append(precio)
        
        # Ubicación del país de venta
        ubicacionVentaPais = maquina.find("div", class_="country-item")
        if ubicacionVentaPais:
            ubicacionVentaPais = ubicacionVentaPais.text.strip()
            ubicacionesVentaPais.append(ubicacionVentaPais)
        else:
            ubicacionesVentaPais.append("No disponible")
        
        # Horómetro (cantidad de horas)
        horometro = maquina.find("div", class_="special-attr special-attr-hours")
        if horometro:
            horometro = horometro.text.replace(" hrs", "").replace(",", "").strip()
            horometros.append(horometro)
        else:
            horometros.append("No disponible")
        
        # Ubicación de la ciudad de venta
        ubicacionVentaCiudad = maquina.find("div", class_="special-attr special-attr-loc")
        if ubicacionVentaCiudad:
            ubicacionVentaCiudad = ubicacionVentaCiudad.text.strip()
            ubicacionesVentaCiudad.append(ubicacionVentaCiudad)
        else:
            ubicacionesVentaCiudad.append("No disponible")
        
        # Marca del fabricante
        marcaFabricante = maquina.find("div", class_="special-attr special-attr-brand")
        if marcaFabricante:
            marcaFabricante = marcaFabricante.text.strip()
            marcasFabricante.append(marcaFabricante)
        else:
            marcasFabricante.append("No disponible")
        
        # Año de fabricación
        añoFabricacion = maquina.find("div", class_="special-attr special-attr-year")
        if añoFabricacion:
            añoFabricacion = añoFabricacion.text.replace("Año: ", "").strip()
            añosFabricacion.append(añoFabricacion)
        else:
            añosFabricacion.append("No disponible")
        
        # Enlace al sitio web de la máquina
        linkWebSiteMaquina = maquina.find("a", class_="product photo product-item-photo").get("href").strip()
        linksWebSiteMaquina.append(linkWebSiteMaquina)

# Llamada a la función para obtener las máquinas
maquinas = webView()

# Llamada a la función para hacer scraping y guardar los datos
scrappingData(maquinas)

# Imprimir el contenido de las listas como verificación
print("Nombres de las máquinas:", titlesMaq)
print("Vendedores:", vendedoresMaquina)
print("Precios:", precios)
print("Países de venta:", ubicacionesVentaPais)
print("Horómetros:", horometros)
print("Ciudades de venta:", ubicacionesVentaCiudad)
print("Marcas:", marcasFabricante)
print("Años de fabricación:", añosFabricacion)
print("Enlaces:", linksWebSiteMaquina)
