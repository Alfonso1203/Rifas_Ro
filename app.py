import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Los Güeros", layout="centered", page_icon="🎟️")

# --- 2. CONEXIÓN AL EXCEL (CON TRUCO PARA FORZAR ACTUALIZACIÓN) ---
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
# Agregamos un parámetro de tiempo a la URL para evitar que Google Sheets nos de una versión vieja (caché)
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=10) # Reducimos el tiempo de caché a 10 segundos
def cargar_datos(url):
    # Lee 'Registro', salta 6 filas, empieza en fila 7
    df = pd.read_excel(url, sheet_name="Registro", skiprows=6, engine='openpyxl')
    return df

# Título Principal
st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 03/04/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    # Pasamos la URL con el timestamp para que siempre intente traer lo más nuevo
    df_full = cargar_datos(URL_DRIVE)
    N = 100 
    info_boletos = {}
    
    # --- 3. PROCESAR ESTADOS PARA PINTAR EL MAPA ---
    for _, row in df_full.iterrows():
        try:
            # Columna E (4): Números seleccionados
            # Columna F (5): Estatus (Pagado/Pendiente)
            if pd.notna(row.iloc[4]): 
                nums = str(row.iloc[4]).replace(" ", "").split(',')
                estado = str(row.iloc[5]).strip().lower() 
                
                for n in nums:
                    if n:
                        num_int = int(float(n))
                        info_boletos[num_int] = estado
        except:
            continue

    # --- 4. MAPA DE BOLETOS PINTADO ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black' 
        
        estado = info_boletos.get(i, "")
        
        if 'pagado' in estado:
            color, txt_c = '#28a745', 'white' 
        elif 'pendiente' in estado:
            color, txt_c = '#ffc107', 'black' 
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    st.pyplot(fig)

    # LEYENDA DE ACTUALIZACIÓN SOLICITADA
    st.markdown("<p style='text-align: center; color: #555;'><b>El mapa se tarda unos minutos en actualizarse</b></p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # --- 5. SECCIÓN DE PAGO (Se mantienen detalles) ---
    st.markdown("### 🏦 DATOS DE PAGO:")
    st.info("""
    - **Banco:** Banamex
    - **Cuenta:** 002180702288920746
    - **Nombre:** Rodrigo Antimo Mora
    """)

    # --- 6. BOTÓN WHATSAPP VERDE E ILUSTRATIVO ---
    # REEMPLAZA EL NÚMERO CON EL TUYO REAL
    numero_wa = "5542006418" 
    mensaje_wa = "Hola Rifa los gueros, Ya realice mi pago Aqui temando el comprobante para registrar mis boletos"
    import urllib.parse
    mensaje_codificado = urllib.parse.quote(mensaje_wa)
    wa_link = f"https://wa.me/{numero_wa}?text={mensaje_codificado}"
    
    # Estilo personalizado para botón verde WhatsApp
    st.markdown(f"""
        <a href="{wa_link}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 1.2rem;">
                MANDAR COMPROBANTE POR WHATSAPP ✅📱
            </div>
        </a>
    """, unsafe_allow_html=True)
    
    st.write("") # Espacio

    # --- 7. MENSAJES FINALES ---
    # Nota de comprobante con el concepto solicitado
    st.warning("### 📸 ¡RECUERDA ENVIAR TU COMPROBANTE! ✨\n\n**Nota:** En el concepto del pago favor de poner su **Nombre**.")
    
    # Mensaje de las 24 horas
    st.error("❗ UNA VEZ REALIZADO TU PAGO, TIENES 24 HRS PARA MANDAR TU COMPROBANTE, DE LO CONTRARIO EL NÚMERO SE LIBERARÁ.")

except Exception as e:
    st.error("Error al conectar con Google Sheets. Verifica que el archivo esté compartido como 'Cualquier persona con el enlace'.")
