import requests
import json
import re
import os

# --- CONFIGURACIÓN PRINCIPAL ---
# 1. URL de la agenda y nombre del archivo de salida HTML
URL_AGENDA = "https://thedaddy.click/schedule/schedule-generated.php"
NOMBRE_ARCHIVO_HTML = "agenda_deportiva.html"

# 2. URL base para los streams (el {channel_id} se reemplaza automáticamente)
BASE_STREAM_URL = "https://thedaddy.click/stream/stream-{channel_id}.php"

# --- DICCIONARIOS Y TEXTOS PARA LA TRADUCCIÓN COMPLETA ---
dias_traduccion = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado",
    "Sunday": "Domingo"
}
meses_traduccion = {
    "January": "Enero", "February": "Febrero", "March": "Marzo",
    "April": "Abril", "May": "Mayo", "June": "Junio",
    "July": "Julio", "August": "Agosto", "September": "Septiembre",
    "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}
frase_traducida = "Programación del Día - Horario UK (GMT)"

# --- CABECERAS PARA SIMULAR NAVEGADOR ---
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://thedaddy.click/schedule/",
    "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

# --- FUNCIONES AUXILIARES ---

def traducir_encabezado(texto_original):
    """Función para traducir completamente el encabezado."""
    texto_traducido = texto_original
    for eng, esp in dias_traduccion.items():
        texto_traducido = texto_traducido.replace(eng, esp)
    for eng, esp in meses_traduccion.items():
        texto_traducido = texto_traducido.replace(eng, esp)
    texto_traducido = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', texto_traducido)
    texto_traducido = texto_traducido.replace("- Schedule Time UK GMT", f"- {frase_traducida}")
    return texto_traducido

### NUEVO ###
def crear_id_ancla(texto):
    """Crea un ID seguro para URL a partir de un texto para usar en anclas HTML."""
    # Convierte a minúsculas, reemplaza espacios con guiones y elimina caracteres no válidos.
    id_seguro = texto.lower().replace(' ', '-').replace(':', '')
    id_seguro = re.sub(r'[^a-z0-9\-]', '', id_seguro)
    return id_seguro

### MODIFICADO ###
def generar_html(titulo_agenda, datos_deportes, orden_deportes):
    """Genera el contenido HTML completo a partir de los datos procesados."""
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo_agenda}</title>
    <style>
        body {{ font-family: "Segoe UI", sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; scroll-behavior: smooth; }}
        .container {{ max-width: 900px; margin: 0 auto; background-color: #ffffff; padding: 10px 20px 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a237e; text-align: center; border-bottom: 2px solid #e8eaf6; padding-bottom: 10px; margin-bottom: 20px;}}
        /* ### NUEVO ### Estilos para el índice de deportes */
        .sport-index {{ text-align: center; margin-bottom: 25px; padding: 10px 0; border-bottom: 1px solid #ddd; }}
        .sport-index a {{
            display: inline-block;
            margin: 4px 6px;
            padding: 5px 12px;
            background-color: #e8eaf6;
            color: #1a237e !important;
            text-decoration: none;
            font-weight: bold;
            border-radius: 15px;
            font-size: 0.9em;
            transition: background-color 0.2s, color 0.2s;
        }}
        .sport-index a:hover {{
            background-color: #3f51b5;
            color: white !important;
        }}
        /* --- Fin de nuevos estilos --- */
        .sport-title {{ background-color: #1a237e; color: white; padding: 10px 15px; font-size: 1.5em; font-weight: bold; border-radius: 5px; margin-top: 25px; margin-bottom: 10px; }}
        .event-card {{ border: 1px solid #ddd; border-radius: 5px; margin-bottom: 15px; padding: 15px; }}
        .event-header {{ display: flex; align-items: flex-start; margin-bottom: 10px; }}
        .event-time {{ background-color: #e8eaf6; color: #3f51b5; font-size: 0.9em; font-weight: bold; padding: 4px 8px; border-radius: 10px; white-space: nowrap; margin-right: 15px; }}
        .event-name {{ font-size: 1.1em; font-weight: bold; }}
        .channels-container {{ padding-left: 20px; }}
        .channels-title {{ font-size: 0.9em; font-weight: bold; margin-top: 10px; margin-bottom: 5px; color: #333; }}
        .channel-link {{ display: inline-block; color: white !important; text-decoration: none; font-size: 0.8em; font-weight: bold; padding: 5px 10px; border-radius: 3px; margin: 3px; transition: opacity 0.2s; }}
        .channel-link:hover {{ opacity: 0.85; }}
        .main-channel {{ background-color: #28a745; }}
        .other-channel {{ background-color: #dc3545; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{titulo_agenda}</h1>
"""
    # --- ### NUEVO ### ---
    # Generar el índice de deportes con enlaces de anclaje
    html += '        <div class="sport-index">\n'
    for sport_name in orden_deportes:
        anchor_id = crear_id_ancla(sport_name)
        html += f'            <a href="#{anchor_id}">{sport_name}</a>\n'
    html += '        </div>\n'
    # --- Fin de la sección del índice ---
    
    for sport_name in orden_deportes:
        events_list = datos_deportes.get(sport_name, [])
        
        # ### MODIFICADO ###: Añadir un ID al título del deporte para el anclaje
        anchor_id = crear_id_ancla(sport_name)
        html += f'<div id="{anchor_id}" class="sport-title">{sport_name}</div>\n'

        for event in events_list:
            html += '<div class="event-card">\n'
            time_str = event.get('time', '')
            event_name_escaped = event.get("event", "").replace('<', '<').replace('>', '>')
            html += f'    <div class="event-header">\n        <span class="event-time">{time_str}</span>\n        <span class="event-name">{event_name_escaped}</span>\n    </div>\n'
            canales_m = event.get('channels', [])
            canales_a = event.get('channels2', [])
            if isinstance(canales_m, dict): canales_m = list(canales_m.values())
            if isinstance(canales_a, dict): canales_a = list(canales_a.values())
            if canales_m or canales_a:
                html += '    <div class="channels-container">\n'
                if canales_m:
                    html += '        <div class="channels-title">Canales Principales:</div>\n'
                    for ch in canales_m:
                        if ch.get('channel_id') and ch.get('channel_name'):
                            url = BASE_STREAM_URL.format(channel_id=ch['channel_id'])
                            html += f'        <a href="{url}" target="_blank" class="channel-link main-channel">{ch["channel_name"]}</a>\n'
                if canales_a:
                    title = "Otras Opciones:" if canales_m else "Canales:"
                    html += f'        <div class="channels-title">{title}</div>\n'
                    for ch in canales_a:
                        if ch.get('channel_id') and ch.get('channel_name'):
                            url = BASE_STREAM_URL.format(channel_id=ch['channel_id'])
                            html += f'        <a href="{url}" target="_blank" class="channel-link other-channel">{ch["channel_name"]}</a>\n'
                html += '    </div>\n'
            html += '</div>\n'
    html += "    </div>\n</body>\n</html>"
    return html

# --- PROCESO PRINCIPAL ---
if __name__ == "__main__":
    print("--- INICIANDO PROCESO AUTOMÁTICO ---")
    
    try:
        # 1. DESCARGAR DATOS
        print(f"1. Descargando agenda de: {URL_AGENDA}")
        response = requests.get(URL_AGENDA, headers=headers, timeout=20)
        response.raise_for_status()
        contenido_original = response.text
        
        # 2. PROCESAR DATOS (TRADUCIR Y FILTRAR)
        print("2. Procesando y traduciendo datos...")
        datos = json.loads(contenido_original)
        clave_original = list(datos.keys())[0]
        clave_traducida = traducir_encabezado(clave_original)
        
        # Obtenemos las categorías y eliminamos "TV Shows" si existe
        categorias = datos[clave_original]
        if "TV Shows" in categorias:
            del categorias["TV Shows"]
            print("   - Sección 'TV Shows' eliminada.")
        
        # Consolidar datos para el HTML (agrupar por deporte principal)
        datos_consolidados = {}
        orden_final_deportes = []
        for key, events in categorias.items():
            main_sport = key.split(' - ')[0].strip().rstrip(':')
            if main_sport not in orden_final_deportes:
                orden_final_deportes.append(main_sport)
            if main_sport not in datos_consolidados:
                datos_consolidados[main_sport] = []
            datos_consolidados[main_sport].extend(events)
        print("   - Datos agrupados por deporte para el HTML.")

        # 3. GENERAR HTML
        print("3. Generando el archivo HTML...")
        contenido_html = generar_html(clave_traducida, datos_consolidados, orden_final_deportes)
        
        # 4. GUARDAR ARCHIVO HTML
        # ### MODIFICADO ###: He corregido la ruta del archivo para que sea más robusta.
        # En lugar de os.path.dirname(__file__), que puede fallar en algunos entornos,
        # usamos una ruta simple que guarda el archivo en el mismo directorio donde se ejecuta el script.
        ruta_completa = os.path.join(os.getcwd(), NOMBRE_ARCHIVO_HTML)
        with open(ruta_completa, "w", encoding="utf-8") as file_html:
            file_html.write(contenido_html)
        
        print(f"\n¡PROCESO COMPLETADO CON ÉXITO!")
        print(f"Archivo guardado en: {ruta_completa}")

    except requests.exceptions.RequestException as e:
        print(f"\nERROR: Ocurrió un error de red al intentar obtener la página: {e}")
    except (json.JSONDecodeError, IndexError) as e:
        print(f"\nERROR: El formato de los datos recibidos no es válido o está vacío: {e}")
    except Exception as e:
        print(f"\nERROR: Ocurrió un error inesperado durante el proceso: {e}")