import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Rodrigo 2026", layout="centered", page_icon="🎟️")

# --- 2. CONEXIÓN AL EXCEL (Solo lectura) ---
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w" # Tu ID de Drive
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx'

@st.cache_data(ttl=15) # Se actualiza cada 15 segundos
def cargar_datos():
    # Lee 'Registro', salta 6 filas, empieza en fila 7
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", skiprows=6, engine='openpyxl')
    return df

# --- TÍTULO PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 27/03/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_full = cargar_datos()
    N = 100 # Total de boletos
    info_boletos = {}
    
    # --- 3. PROCESAR ESTADOS ---
    for _, row in df_full.iterrows():
        try:
            # Columna E (4): Números seleccionados
            # Columna F (5): Estatus
            if pd.notna(row.iloc[4]): 
                nums = str(row.iloc[4]).replace(" ", "").split(',')
                estado = str(row.iloc[5]).strip().lower() # pagado o pendiente
                
                for n in nums:
                    if n:
                        num_int = int(float(n))
                        info_boletos[num_int] = estado
        except:
            continue

    # --- 4. DIBUJAR MAPA (Corregido y pintado) ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black' # Disponible por defecto
        
        estado = info_boletos.get(i, "")
        
        if 'pagado' in estado:
            color, txt_c = '#28a745', 'white' # Verde fuerte (Pagado)
        elif 'pendiente' in estado:
            color, txt_c = '#ffc107', 'black' # Amarillo (Pendiente)
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    
    # Mostramos el mapa
    st.pyplot(fig)

    # Nota de actualización
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>Actualización automática cada 15 seg ⏳</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # --- 5. SECCIÓN DE PAGO (Imagen 18) ---
    st.markdown("## 🏦 DATOS DE PAGO:")
    
    # Recreamos el recuadro azul de la imagen
    st.info("""
    - **Banco:** Banamex
    - **Cuenta:** 002180702288920746
    - **Nombre:** Rodrigo Antimo Mora
    """)

    # --- 6. SECCIÓN DE WHATSAPP (Imagen 18) ---
    # ¡IMPORTANTE: Reemplaza con tu número real!
    NUMERO_WA = "5542006418" 
    wa_link = f"https://wa.me/{NUMERO_WA}?text=Hola%20Rodrigo,%20quiero%20apartar%20un%20boleto"
    
    st.link_button("¿LISTO PARA APARTAR? 📱", wa_link, use_container_width=True)
    
    # Nota final de comprobante
    st.warning("### 📸 ¡RECUERDA ENVIAR TU COMPROBANTE! ✨")

except Exception as e:
    st.error("No se pudieron cargar los boletos. Asegúrate de que el Google Sheet esté compartido como 'Cualquier persona con el enlace'.")
