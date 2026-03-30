import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.parse
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Rodrigo 2026", layout="centered", page_icon="🎟️")

# --- 2. CONEXIÓN AL EXCEL ---
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w" # Tu ID de Drive
# Usamos el truco del tiempo para forzar la actualización
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=5) # Cache de 5 segundos para máxima frescura
def cargar_datos(url):
    # Saltamos las primeras filas de encabezados según image_23.png
    df = pd.read_excel(url, sheet_name="Registro", skiprows=2, engine='openpyxl')
    return df

# Título Principal (se mantiene)
st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 27/03/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_full = cargar_datos(URL_DRIVE)
    N = 100 # Total de boletos en tu mapa
    boletos_vendidos = set()
    
    # --- 3. PROCESAR NÚMEROS DE COLUMNA D (Modificación Solicitada) ---
    for _, row in df_full.iterrows():
        try:
            # Columna D (índice 3): Numero seleccionado
            celda_numeros = str(row.iloc[3])
            if celda_numeros and celda_numeros != 'nan':
                # Limpiamos y separamos por comas si hay varios números
                nums = celda_numeros.replace(" ", "").split(',')
                for n in nums:
                    if n:
                        # Convertimos a entero (manejando decimales como 1.0)
                        num_id = int(float(n))
                        if 1 <= num_id <= N:
                            boletos_vendidos.add(num_id)
        except:
            continue

    # --- 4. DIBUJAR MAPA PINTADO ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        # Modificación: Pintar en verde si el número está en 'boletos_vendidos'
        if i in boletos_vendidos:
            color = '#28a745' # Verde fuerte para vendidos
            txt_c = 'white'
        else:
            color = 'white' # Disponible
            txt_c = 'black'
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    st.pyplot(fig)

    # Leyenda (se mantiene)
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>El mapa se tarda unos minutos en actualizarse ⌛</p>", unsafe_allow_html=True)
    st.write("---")
    
    # --- 5. DATOS DE PAGO (sin cambios) ---
    st.markdown("### 🏦 DATOS DE PAGO:")
    st.info("- **Banco:** Banamex\n- **Cuenta:** 002180702288920746\n- **Rodrigo Antimo Mora**")

    # --- 6. BOTÓN WHATSAPP (Texto en blanco) ---
    numero_wa = "52XXXXXXXXXX" # Pon tu número real aquí
    mensaje_wa = "Hola Rodrigo, ya realicé mi pago Aquí temando el comprobante"
    wa_link = f"https://wa.me/{numero_wa}?text={urllib.parse.quote(mensaje_wa)}"
    
    # Estilo personalizado: Fondo verde con texto en blanco (color: white;)
    st.markdown(f'<a href="{wa_link}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366; color: white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:1.2rem; cursor:pointer;">MANDAR COMPROBANTE POR WHATSAPP ✅📱</div></a>', unsafe_allow_html=True)
    
    st.write("")

    # --- 7. MENSAJES FINALES (sin cambios) ---
    st.warning("### 📸 ¡RECUERDA ENVIAR TU COMPROBANTE! ✨")
    # Mensaje adicional sobre el nombre
    st.markdown("""
        <div style="background-color: #fcf8e3; color: #8a6d3b; padding: 10px; border-radius: 5px; font-weight: bold;">
            Nota: En el concepto del pago favor de poner su Nombre.
        </div>
    """, unsafe_allow_html=True)
    st.error("❗ UNA VEZ REALIZADO TU PAGO, TIENES 24 HRS PARA MANDAR TU COMPROBANTE, DE LO CONTRARIO EL NÚMERO SE LIBERARÁ.")

except Exception as e:
    st.error(f"Error técnico: Asegúrate de que el Drive esté compartido como 'Cualquier persona con el enlace'. {e}")
