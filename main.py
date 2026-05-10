import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN DE HEADERS ---
# Usamos un User-Agent real para evitar bloqueos (Error 503)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def extraer_datos_amazon(busqueda):
    """
    Función para extraer productos, precios y ratings de Amazon.
    Prioriza la eficiencia mediante BeautifulSoup.
    """
    print(f"--- Iniciando búsqueda para: {busqueda} ---")
    url = f"https://www.amazon.com/s?k={busqueda}"
    
    try:
        respuesta = requests.get(url, headers=headers, timeout=10)
        if respuesta.status_code != 200:
            print(f"Error de servidor: {respuesta.status_code}")
            return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

    soup = BeautifulSoup(respuesta.content, "html.parser")
    lista_productos = []
    items = soup.select(".s-result-item[data-component-type='s-search-result']")
    
    for item in items:
        try:
            # Extracción de Título
            nombre = item.select_one("h2 span").text.strip()

            # Extracción y limpieza de Precio
            p_entero = item.select_one(".a-price-whole")
            p_decimal = item.select_one(".a-price-fraction")
            precio_final = float(f"{p_entero.text}{p_decimal.text}".replace(",", "")) if p_entero else 0.0

            # Extracción de Estrellas
            estrella_raw = item.select_one(".a-icon-alt")
            rating = float(estrella_raw.text.split(" ")[0]) if estrella_raw else 0.0

            # Lógica de respaldo para Reviews
            rev_elem = item.select_one(".a-size-base.s-underline-text") or \
                       item.select_one("span[aria-label*='valoraciones']") or \
                       item.select_one(".a-size-base.a-color-secondary")
            
            num_reviews = int("".join(filter(str.isdigit, rev_elem.text))) if rev_elem else 0

            lista_productos.append({
                "Producto": nombre,
                "Precio_USD": precio_final,
                "Rating": rating,
                "Reviews": num_reviews,
                "Fecha_Consulta": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
            })
        except:
            continue

    return pd.DataFrame(lista_productos)

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    query = "laptop"
    data_final = extraer_datos_amazon(query)

    if data_final is not None and not data_final.empty:
        print("¡Éxito! Guardando reporte...")
        data_final.to_csv(f"reporte_{query}.csv", index=False)
        print(data_final.head())
    else:
        print("No se obtuvieron datos.")
