import datetime
import os

def convertir_horario_a_html(archivo_entrada, archivo_salida):
    if not os.path.exists(archivo_entrada):
        print(f"El archivo {archivo_entrada} no existe.")
        return

    with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()

    # Obtener el día de la semana del primer elemento del archivo
    dia_semana = lineas[0].strip() if lineas else 'Desconocido'  # Día de la semana

    # Estructura HTML inicial
    contenido_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Horario de Deportes</title>
    <link rel="stylesheet" type="text/css" href="estilos.css">  <!-- Enlace al CSS externo -->
</head>
<body>
    <h1>Horario de Deportes ({dia_semana})</h1>
    <table>
        <tr>
            <th class="hora">Hora</th>
            <th class="partido">Partido</th>
            <th class="idioma">Idioma</th> <!-- Nueva columna para el idioma -->
            <th class="enlace">Enlace</th>
        </tr>
    '''

    # Procesar todas las líneas excepto la última
    for linea in lineas[:-1]:
        if "|" in linea:
            partes = linea.split("|")  
            if len(partes) >= 2:  
                detalles_partido = partes[0].strip()  
                enlace = partes[1].strip()  

                hora_partido = detalles_partido[:5].strip()  
                partido = detalles_partido[6:].strip()  

                # Determinar el idioma desde la línea
                idioma = 'Desconocido'  # Valor por defecto
                if 'ingles y español' in linea:
                    idioma = 'inglés y español'
                elif 'portugues' in linea:
                    idioma = 'portugués'
                elif 'español' in linea:
                    idioma = 'español'
                elif 'alemán' in linea:
                    idioma = 'alemán'
                elif 'italiano' in linea:
                    idioma = 'italiano'
                elif 'ingles' in linea:
                    idioma = 'inglés'  # Se agrega esta línea para detectar inglés

                # Agregar fila a HTML con hipervínculo
                contenido_html += f'''
                <tr>
                    <td class="hora">{hora_partido}</td>
                    <td class="partido">{partido}</td>
                    <td class="idioma">{idioma}</td> <!-- Llenar con el idioma -->
                    <td class="enlace"><a href="{enlace}" target="_blank">Ver partido</a></td>
                </tr>
                '''

    # Procesar la última línea
    ultima_linea = lineas[-1]
    if "|" in ultima_linea:
        partes = ultima_linea.split("|")  
        if len(partes) >= 2:  
            detalles_partido = partes[0].strip()  
            enlace = partes[1].strip()  

            hora_partido = detalles_partido[:5].strip()  
            partido = detalles_partido[6:].strip()  

            # Determinar el idioma para la última línea
            idioma = 'Desconocido'  # Valor por defecto
            if 'ingles y español' in ultima_linea:
                idioma = 'inglés y español'
            elif 'portugues' in ultima_linea:
                idioma = 'portugués'
            elif 'español' in ultima_linea:
                idioma = 'español'
            elif 'alemán' in ultima_linea:
                idioma = 'alemán'
            elif 'italiano' in ultima_linea:
                idioma = 'italiano'
            elif 'ingles' in ultima_linea:
                idioma = 'inglés'  # Se agrega esta línea para detectar inglés

            # Agregar la última fila a HTML
            contenido_html += f'''
            <tr>
                <td class="hora">{hora_partido}</td>
                <td class="partido">{partido}</td>
                <td class="idioma">{idioma}</td>
                <td class="enlace"><a href="{enlace}" target="_blank">Ver partido</a></td>
            </tr>
            '''

    # Estructura HTML final
    contenido_html += '''
    </table>
</body>
</html>
'''

    # Escribir en el archivo HTML de salida
    with open(archivo_salida, 'w', encoding='utf-8') as salida:
        salida.write(contenido_html)

# Obtener el día actual y asociarlo con el archivo correspondiente
import datetime

# Nombres de los archivos según los días de la semana
dias_semana = {
    0: 'lunes.txt',
    1: 'martes.txt',
    2: 'miércoles.txt',
    3: 'jueves.txt',
    4: 'viernes.txt',
    5: 'sábado.txt',
    6: 'domingo.txt'
}

# Obtener el día actual (0 = lunes, 6 = domingo)
dia_actual = datetime.datetime.now().weekday()
archivo_entrada = dias_semana[dia_actual]  # Seleccionar el archivo correspondiente
archivo_salida = 'horario.html'  # Nombre del archivo de salida

convertir_horario_a_html(archivo_entrada, archivo_salida)
print(f'Se ha generado el horario en HTML para el archivo {archivo_entrada}: {archivo_salida}')
