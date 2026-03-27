import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Rodrigo 2026", layout="centered")

# --- 2. CONEXIÓN AL EXCEL DE DRIVE ---
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx'

@st.cache_data(ttl=30) # Actualización cada 30 segundos
def cargar_datos():
    # Saltamos las primeras 6 filas para leer los datos reales
    return pd.read_excel(URL_DRIVE, sheet_name="Registro", skiprows=6, engine='openpyxl')

st.title("🎟️ BOLETOS RIFA 27/03/2026 🎟️")

try:
    df = cargar_datos()
    N = 100 
    estatus_boletos = {}
    
    # --- 3. PROCESAR INFORMACIÓN ---
    for _, row in df.iterrows():
        try:
            if pd.notna(row.iloc[3]): # Columna D: Números
                nums = str(row.iloc[3]).replace(" ", "").split(',')
                estado = str(row.iloc[4]).strip().lower() # Columna E: Estatus
                for n in nums:
                    if n:
                        num_int = int(float(n))
                        estatus_boletos[num_int] = estado
        except:
            continue

    # --- 4. DIBUJAR EL MAPA ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black'
        
        est = estatus_boletos.get(i, "")
        if 'pagado' in est:
            color, txt_c = '#28a745', 'white' # Verde
        elif 'pendiente' in est:
            color, txt_c = '#ffc107', 'black' # Amarillo
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    
    # Mostrar el mapa una sola vez
    st.pyplot(fig)

    # --- 5. LEYENDA DE ESPERA ---
    st.markdown("<p style='text-align: center; color: gray;'><i>Una vez hecho tu pago, tus boletos se verán reflejados en unos minutos ⏳</i></p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # --- 6. SECCIÓN DE PAGO Y WHATSAPP ---
    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **🏦 DATOS DE PAGO:**
        - **Banco:** Banamex
        - **Cuenta:** 002180702288920746
        - **Tipo:** Débito
        - **Nombre:** Rodrigo Antimo Mora
        """)

    with col2:
        # Pon tu número real aquí abajo
        numero_tel = "5542006418" 
        mensaje_wa = "¡Hola Rodrigo! Ya realicé mi pago. Aquí te mando mi comprobante para registrar mis boletos."
        link_wa = f"https://wa.me/{numero_tel}?text={mensaje_wa.replace(' ', '%20')}"
        
        st.success("**💬 ¿LISTO PARA APARTAR?**")
        st.markdown("### Apartar mi boleto")
        st.link_button("Click aquí para ir a WhatsApp 📱", link_wa, use_container_width=True)

    # --- 7. RECORDATORIO FINAL ---
    st.write("") 
    st.warning("""
    ### 📸 ¡RECUERDA TU COMPROBANTE!
    Es muy importante que nos mandes una **foto o captura de tu comprobante de pago** por WhatsApp para poder registrar tus boletos oficialmente. 🎟️✨
    """)

except Exception as e:
    st.warning("Estamos actualizando el mapa con los últimos boletos. Vuelve a cargar en un momento.")
