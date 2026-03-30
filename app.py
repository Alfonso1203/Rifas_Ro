import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Rifa Los Güeros", layout="centered")

ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=5)
def cargar_datos():
    # Se salta 2 filas: los encabezados están en la fila 3
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", skiprows=2, engine='openpyxl')
    return df

st.title("🎟️ BOLETOS RIFA 03/04/2026 🎟️")

try:
    df_full = cargar_datos()
    N = 100 
    info_boletos = {}
    
    # --- 2. LÓGICA DE PINTADO (CORREGIDA) ---
    for index, row in df_full.iterrows():
        # Columna D (índice 3): Numero seleccionado | Columna F (índice 5): Estatus
        celda_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
        estado_crudo = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""
        
        if celda_nums and celda_nums.lower() != 'nan':
            # Separar números por coma (ej: "1,2,3")
            lista_n = celda_nums.split(',')
            for n in lista_n:
                n_limpio = n.strip().split('.')[0] # Quita espacios y posibles ".0"
                if n_limpio.isdigit():
                    num_int = int(n_limpio)
                    if 1 <= num_int <= N:
                        info_boletos[num_int] = estado_crudo

    # --- 3. CREACIÓN DEL MAPA ---
    columnas = 10
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.8))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'none', 'white' 
        
        est = info_boletos.get(i, "")
        
        # Prioridad de colores
        if 'pagado' in est:
            color, txt_c = '#28a745', 'white' # VERDE
        elif 'pendiente' in est:
            color, txt_c = '#ffc107', 'black' # AMARILLO
        
        rect = plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#555555', linewidth=0.8)
        ax.add_patch(rect)
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', 
                fontsize=9, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.2, columnas)
    ax.set_ylim(-filas + 0.2, 0.8)
    ax.axis('off')
    st.pyplot(fig, transparent=True)

    # --- 4. LEYENDA Y DATOS ---
    st.markdown(f"""
        <div style="text-align: center; border: 1px solid #444; padding: 15px; border-radius: 10px; background-color: #121212;">
            <span style="color: #28a745; font-size: 1.2rem;">●</span> <b>Pagado</b> &nbsp;&nbsp;
            <span style="color: #ffc107; font-size: 1.2rem;">●</span> <b>Pendiente</b> &nbsp;&nbsp;
            <span style="color: #ffffff; font-size: 1.2rem;">○</span> <b>Disponible</b>
            <br><br>
            <h3 style="margin:0; color: #ffffff;">Precio del boleto: $170</h3>
        </div>
    """, unsafe_allow_html=True)

    msg_wa = "Hola Rifas los gueros! Ya realice mi pago. Aquí te mando mi comprobante."
    link_wa = f"https://wa.me/5542006418?text={msg_wa.replace(' ', '%20')}"

    col_pago, col_btn = st.columns([1, 1])
    with col_pago:
        st.info("**🏦 DATOS DE PAGO:**\n- Banamex\n- Cuenta: 002180702288920746\n- Rodrigo Antimo Mora")
    with col_btn:
        st.write("") 
        st.link_button("Apartar por WhatsApp 📱", link_wa, use_container_width=True)

    st.success("### 📸 ¡MANDA TU COMPROBANTE! ✨")

except Exception as e:
    st.error(f"Error: {e}")
