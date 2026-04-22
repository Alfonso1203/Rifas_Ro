import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Rifa Los Güeros", layout="wide")

# CSS para asegurar que el mapa sea legible en cualquier modo (Light/Dark)
st.markdown("""
    <style>
    .ticket-grid-bg {
        background-color: #0e1117;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .ticket-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
        gap: 8px;
    }
    .ticket {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
        font-weight: bold;
        font-size: 16px;
        color: white !important;
        border: 1px solid #444 !important;
        background-color: #1a1c23;
    }
    .pagado { background-color: #28a745 !important; border-color: #1e7e34 !important; }
    .pendiente { background-color: #ffc107 !important; color: black !important; border-color: #d39e00 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN CON TU EXCEL ---
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=2)
def cargar_datos():
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", engine='openpyxl')
    return df

st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 24/04/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_raw = cargar_datos()
    INICIO = 1
    FIN = 100
    info_boletos = {}
    
    # --- 3. LÓGICA PARA PINTAR LOS BOLETOS ---
    for index, row in df_raw.iterrows():
        try:
            val_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            val_estatus = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""
            
            if val_nums and val_nums.lower() not in ['nan', 'numero seleccionado']:
                lista_n = val_nums.replace('.', ',').split(',')
                for n in lista_n:
                    n_limpio = n.strip()
                    if n_limpio.isdigit():
                        num_int = int(n_limpio)
                        if INICIO <= num_int <= FIN:
                            if info_boletos.get(num_int) != "pagado":
                                info_boletos[num_int] = val_estatus
        except:
            continue

    # --- 4. GENERACIÓN DEL MAPA ---
    ticket_html = '<div class="ticket-grid-bg"><div class="ticket-container">'
    for i in range(INICIO, FIN + 1):
        est = info_boletos.get(i, "")
        clase = ""
        if 'pagado' in est:
            clase = "pagado"
        elif 'pendiente' in est:
            clase = "pendiente"
        ticket_html += f'<div class="ticket {clase}">{i}</div>'
    ticket_html += '</div></div>'
    st.markdown(ticket_html, unsafe_allow_html=True)

    # --- 5. LEYENDA Y PRECIO ---
    st.markdown("""
        <div style="text-align: center; border: 1px solid #444; padding: 15px; border-radius: 10px; background-color: #121212; color: white;">
            <span style="color: #28a745;">●</span> <b>Pagado</b> &nbsp;&nbsp;
            <span style="color: #ffc107;">●</span> <b>Pendiente</b> &nbsp;&nbsp;
            <span style="color: #ffffff;">○</span> <b>Disponible</b>
            <br><br>
            <h3 style="margin:0;">Precio del boleto: $170</h3>
            <p style="color: #bbbbbb; font-size: 0.9em; margin-top: 10px;">⌛ El mapa se tarda unos minutos en actualizarse ⌛</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 6. DATOS DE PAGO ACTUALIZADOS Y BOTÓN ---
    link_wa = "https://wa.me/5542006418?text=Hola%20Rifas%20los%20gueros!%20Ya%20realice%20mi%20pago."
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**🏦 DATOS DE PAGO:**\n- Bbva\n- Cuenta clave: 012 180 01580888896 1\n- Israel Sámano")
    with col2:
        st.write("") 
        st.link_button("Apartar por WhatsApp 📱", link_wa, use_container_width=True)

    st.success("### 📸 Recuerda poner tu nombre completo en el concepto del comprobante ✨")

except Exception as e:
    st.error(f"Error al cargar el mapa: {e}")
