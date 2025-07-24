import requests
from bs4 import BeautifulSoup
from datetime import datetime

palabras_clave = ["Stanley", "termo", "mate", "auriculares", "celular", "tecnología"]

def buscar_meli(query):
    url = f"https://www.mercadolibre.com.ar/{query.replace(' ', '-')}/_DisplayType_LF"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("li.ui-search-layout__item")[:3]
    resultados = []
    for item in items:
        titulo = item.select_one("h2") or item.select_one("h3")
        link = item.select_one("a")["href"] if item.select_one("a") else "#"
        if titulo:
            resultados.append((titulo.text.strip(), link))
    return resultados

def generar_html():
    hoy = datetime.now().strftime("%d/%m/%Y")
    html = f"""<!DOCTYPE html>
<html lang='es'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Cupones Mercado Libre</title>
  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'>
</head>
<body class='bg-yellow-50 text-gray-800'>
  <div class='max-w-3xl mx-auto py-8 px-4'>
    <h1 class='text-3xl font-bold text-yellow-600 mb-4'>🎯 Cupones del Día - Mercado Libre</h1>
    <p class='mb-6'>Ofertas en tecnología, termos, mates y Stanley. Actualizado: {hoy}</p>
    <div class='space-y-4'>
"""

    for palabra in palabras_clave:
        resultados = buscar_meli(palabra)
        if resultados:
            html += f"<div class='bg-white p-4 rounded-xl shadow'><h2 class='text-xl font-semibold mb-2'>🔎 {palabra.capitalize()}</h2>"
            for titulo, link in resultados:
                html += f"<p><a class='text-blue-600 underline' href='{link}' target='_blank'>{titulo}</a></p>"
            html += "</div>"

    html += "</div></div></body></html>"
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    generar_html()
