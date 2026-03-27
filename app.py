import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Rodrigo 2026", layout="centered")

# --- 2. CONEXIÓN AL EXCEL DE DRIVE ---
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx'

@st.cache_data(ttl=15) # Actualización rápida cada 15 segundos
def cargar_datos():
    # Saltamos 6 filas para empezar en los encabezados reales (Fila 7)
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", skiprows=6, engine='openpyxl')
    return df

st.title("🎟️ BOLETOS RIFA 27/03/2026 🎟️")

try:
    df_full = cargar_datos()
    N = 100 
    info_boletos = {}
    
    # --- 3. PROCESAR COLORES (Lógica corregida) ---
    for _, row in df_full.iterrows():
        try:
            # Columna E (índice 4): Números seleccionados
            # Columna F (índice 5): Estatus
            if pd.notna(row.iloc[4]): 
                nums = str(row.iloc[4]).replace(" ", "").split(',')
                estado = str(row.iloc[5]).strip().lower() 
                
                for n in nums:
                    if n:
                        num_int = int(float(n))
                        info_boletos[num_int] = estado
        except:
            continue

    # --- 4. DIBUJAR EL MAPA PINTADO ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black' # Disponible
        
        estado = info_boletos.get(i, "")
        
        if 'pagado' in estado:
            color, txt_c = '#28a745', 'white' # Verde fuerte para pagados
        elif 'pendiente' in estado:
            color, txt_c = '#ffc107', 'black' # Amarillo para pendientes
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    st.pyplot(fig)

    st.markdown("<p style='text-align: center; color: gray;'><i>Actualización automática cada 15 seg ⏳</i></p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # --- 5. DATOS DE PAGO Y BOTÓN ---
    c1, c2 = st.columns(2)
    with c1:
        st.info("""
        **🏦 DATOS DE PAGO:**
        - Banco: Banamex
        - Cuenta: 002180702288920746
        - Rodrigo Antimo Mora
        """)
    with c2:
        wa_link = "https://wa.me/5542006418?text=Hola%20Rodrigo,%20quiero%20apartar%20un%20boleto"
        st.link_button("¿LISTO PARA APARTAR? 📱", wa_link, use_container_width=True)

    st.warning("### 📸 ¡RECUERDA ENVIAR TU COMPROBANTE! ✨")

except Exception as e:
    st.error("Error al cargar datos. Verifica que el Excel esté compartido como 'Cualquier persona con el enlace'.")
