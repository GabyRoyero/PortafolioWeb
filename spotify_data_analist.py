from openpyxl.chart import BarChart, Reference
from openpyxl import Workbook
import matplotlib.pyplot as plt
import pandas as pd

# Leer archivo CSV
ruta_csv = r"C:\Users\gabyr\OneDrive\Desktop\Programación\Proyectos_cv\spotify_songs.csv"
datos = pd.read_csv(ruta_csv)
print(datos.head())

# Ordenar por popularidad (de mayor a menor)
datos_ordenados = datos.sort_values(by="Popularidad", ascending=False)

# Gráfico de barras - Popularidad
plt.figure(figsize=(10, 6))
plt.bar(datos_ordenados["Titulo"], datos_ordenados["Popularidad"], color="purple")
plt.title("Popularidad de Canciones de TWICE")
plt.xlabel("Canciones")
plt.ylabel("Popularidad")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Canción con mayor popularidad
cancion_top = datos.loc[datos["Popularidad"].idxmax()]
print("🎶 Canción más popular:")
print(cancion_top)

# Duración promedio
duracion_promedio = datos["Duracion"].mean()
print(f"⏰ Duración promedio: {round(duracion_promedio, 2)} minutos")

# Canciones con popularidad mayor a 95
canciones_populares = datos[datos["Popularidad"] > 95]
print(f"🔥 Canciones con popularidad mayor a 95: {len(canciones_populares)}")
print(canciones_populares[["Titulo", "Popularidad"]])

# Gráfico de torta - Proporción de canciones populares
labels = ["Mayor a 95", "Menor o igual a 95"]
sizes = [len(canciones_populares), len(datos) - len(canciones_populares)]
colors = ["purple", "pink"]
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%")
plt.title("Proporción de Canciones Populares")
plt.show()

# Crear informe Excel con varias hojas
ruta_excel = "informe_spotify.xlsx"
with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
    pd.DataFrame([cancion_top]).to_excel(writer, sheet_name="Cancion_Mas_Popular", index=False)
    pd.DataFrame({"Duracion_Promedio": [round(duracion_promedio, 2)]}).to_excel(writer, sheet_name="Estadisticas_Generales", index=False)
    canciones_populares.to_excel(writer, sheet_name="Canciones_Populares", index=False)

print("✅ Informe generado con éxito")

# Crear Gráfico de Barras en Excel
wb = Workbook()
ws = wb.active
ws.title = "Canciones_Populares"
ws.append(["Titulo", "Popularidad"])

for row in canciones_populares.itertuples():
    ws.append([row.Titulo, row.Popularidad])

chart = BarChart()
data = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=len(canciones_populares) + 1)
categories = Reference(ws, min_col=1, min_row=2, max_row=len(canciones_populares) + 1)
chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)
chart.title = "Popularidad de Canciones"
chart.x_axis.title = "Canciones"
chart.y_axis.title = "Popularidad"
ws.add_chart(chart, "E5")

wb.save(ruta_excel)
print("✅ Informe con gráfico generado con éxito")
