from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import csv

def extract_product_info(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraer el título con el nuevo selector
        title_element = soup.find("h1", class_="detalle-producto__nombre")
        title = title_element.text.strip() if title_element else "N/A"

        # Extraer información de la sección de detalles del producto
        detalle_producto = soup.select_one('div.detalle-producto__bullets')
        
        # Extraer ubicación
        ubicacion_element = detalle_producto.find('li', text='Ubicación')
        ubicacion_texto = ubicacion_element.find_next('li').text.strip() if ubicacion_element else "N/A"

        if ',' in ubicacion_texto:
            ubicacion_ciudad, ubicacion_pais = [part.strip().replace(".", "") for part in ubicacion_texto.split(',', 1)]
        else:
            ubicacion_ciudad = "N/A"
            ubicacion_pais = "N/A"

        # Extraer vendedor
        vendedor_element = detalle_producto.find('li', text='Vendido por')
        vendedor = vendedor_element.find_next('li').text.strip() if vendedor_element else "N/A"

        # Extraer horometro (horas de trabajo)
        horometro_element = detalle_producto.find('li', text='Horas de trabajo')
        horometro = horometro_element.find_next('li').text.strip() if horometro_element else "N/A"

        # Extraer año
        año_element = detalle_producto.find('li', text='Año')
        año_fabricacion = año_element.find_next('li').text.strip() if año_element else "N/A"

        # Extraer precio (mantenemos el selector original por si acaso)
        precio_element = soup.find("p", class_="precioNormal")
        #precio_element = soup.select_one('div.col-lg-4.col-md-5.col-sm-12.col-xs-12 div.precio p')
        precio = precio_element.text.strip().replace(",", "").replace(" USD + IGV", "") if precio_element else "N/A"

        return {
            'title': title,
            'vendedor': vendedor,
            'precio': precio,
            'ubicacion_pais': ubicacion_pais,
            'ubicacion_ciudad': ubicacion_ciudad,
            'horometro': horometro,
            'año_fabricacion': año_fabricacion,
            'link': link
        }
    except Exception as e:
        print(f"Error al procesar el link {link}: {str(e)}")
        return None

# El resto del código permanece igual
# Configurar el navegador
options = webdriver.FirefoxOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver = webdriver.Firefox(options=options)

# Navegar a la página principal
driver.get("https://www.be-market.com/tiendaonline/webapp/search?parametro=&pagina=1&pais:PER%C3%9A")

# Esperar a que la página cargue completamente
time.sleep(1)

# Extraer el número total de pestañoas (páginas)
try:
    element = driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div/div[2]/div[1]/div[2]/nav/ul/b[10]/li/span')
    total_paginas = int(element.text)
    print(f"Número total de páginas: {total_paginas}")
except Exception as e:
    print(f"Error al extraer el número de páginas: {str(e)}")
    driver.quit()
    exit()

# Definir el nombre del archivo CSV
csv_file = 'data.csv'

# Crear el archivo CSV y escribir los encabezados
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'vendedor', 'precio', 'ubicacion_pais', 'ubicacion_ciudad', 'horometro', 'año_fabricacion', 'link'])
    writer.writeheader()

# Iterar sobre todas las páginas
for page_num in range(1, total_paginas + 1):
    # Cambiar el número de página en la URL
    url = f"https://www.be-market.com/tiendaonline/webapp/search?parametro=&pagina={page_num}&pais:PER%C3%9A"
    driver.get(url)
    print(f"Procesando la página {page_num}/{total_paginas}")
    
    # Esperar a que la página cargue completamente
    time.sleep(1)
    
    # Extraer todos los links de productos en la página actual
    li_elements = driver.find_elements(By.CSS_SELECTOR, 'ul#DivItems li')
    page_links = []
    for li in li_elements:
        try:
            a_tag = li.find_element(By.CSS_SELECTOR, 'h3 a')
            href = a_tag.get_attribute('href')
            page_links.append(href)
        except:
            pass

    print(f"Se encontraron {len(page_links)} links en la página {page_num}")

    # Procesar cada link de la página actual
    for index, link in enumerate(page_links, start=1):
        print(f"Procesando el producto {index}/{len(page_links)} de la página {page_num}")
        product_data = extract_product_info(link)
        if product_data:
            with open(csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=product_data.keys())
                writer.writerow(product_data)
            print(f"Datos del producto {index} de la página {page_num} guardados en {csv_file}")

# Cerrar el navegador de Selenium
driver.quit()

print(f"Proceso completado. Todos los datos han sido guardados en {csv_file}")