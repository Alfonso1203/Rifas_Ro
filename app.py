import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Rodrigo 2026", layout="centered")

# --- 2. CONEXIÓN AL EXCEL ---
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx'

@st.cache_data(ttl=15)
def cargar_datos():
    # Lee 'Registro', salta 6 filas para empezar en los datos reales (Fila 7)
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", skiprows=6, engine='openpyxl')
    return df

# Título Principal
st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 27/03/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_full = cargar_datos()
    N = 100 
    info_boletos = {}
    
    # --- 3. PROCESAR ESTADOS PARA PINTAR EL MAPA ---
    for _, row in df_full.iterrows():
        try:
            # Columna E (índice 4): Números seleccionados
            # Columna F (índice 5): Estatus (Pagado/Pendiente)
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
        color, txt_c = 'white', 'black' # Disponible
        
        estado = info_boletos.get(i, "")
        
        if 'pagado' in estado:
            color, txt_c = '#28a745', 'white' # Verde
        elif 'pendiente' in estado:
            color, txt_c = '#ffc107', 'black' # Amarillo
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    st.pyplot(fig)

    st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>El mapa se tarda unos minutos en actualizarse ⏳</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # --- 5. SECCIÓN DE PAGO ---
    st.markdown("### 🏦 DATOS DE PAGO:")
    st.info("""
    - **Banco:** Banamex
    - **Cuenta:** 002180702288920746
    - **Nombre:** Rodrigo Antimo Mora
    """)

    # --- 6. BOTÓN WHATSAPP ---
    # REEMPLAZA LAS X CON TU NÚMERO
    numero_wa = "5542006418" 
    wa_link = f"https://wa.me/{numero_wa}?text=Hola,%20Rifalosgueros,%20ya%20realicé%20mi%20pago%20de%20la%20rifa."
    st.link_button("¿LISTO PARA APARTAR? 📱", wa_link, use_container_width=True)

    # --- 7. MENSAJE FINAL (Imagen f5df5a) ---
    st.warning("### 📸 ¡RECUERDA ENVIAR TU COMPROBANTE! ✨")
    
    # Mensaje adicional solicitado
    st.error("❗ UNA VEZ REALIZADO TU PAGO, TIENES 24 HRS PARA MANDAR TU COMPROBANTE, DE LO CONTRARIO EL NÚMERO SE LIBERARÁ.")

except Exception as e:
    st.error("Error al conectar con Google Sheets. Verifica los permisos de compartir.")
