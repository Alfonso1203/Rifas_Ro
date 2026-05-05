import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Rifa Los Güeros", layout="wide")

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
        grid-template-columns: repeat(auto-fill, minmax(45px, 1fr));
        gap: 6px;
    }
    .ticket {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
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

st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 18/05/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_raw = cargar_datos()
    INICIO = 1
    FIN = 400 
    info_boletos = {}
    
    # --- 3. LÓGICA DE PINTADO CORREGIDA ---
    for index, row in df_raw.iterrows():
        try:
            # Columna D: Números | Columna F: Estatus
            val_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            val_estatus = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""
            
            if val_nums and val_nums.lower() not in ['nan', 'numero seleccionado']:
                # Reemplazamos puntos por comas para que siempre funcione
                lista_n = val_nums.replace('.', ',').split(',')
                for n in lista_n:
                    n_limpio = n.strip()
                    if n_limpio.isdigit():
                        num_int = int(n_limpio)
                        if INICIO <= num_int <= FIN:
                            # Prioridad al estado "pagado"
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

    # --- 5. SECCIÓN DE PRECIO Y LEYENDA ---
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="color: #28a745;">●</span> <b>Pagado</b> &nbsp;&nbsp;
            <span style="color: #ffc107;">●</span> <b>Pendiente</b> &nbsp;&nbsp;
            <span style="color: #ffffff;">○</span> <b>Disponible</b>
            <br><br>
            <h1 style="margin:0; font-size: 2.5rem;">Precio del boleto: $65</h1>
            <p style="color: #bbbbbb; font-size: 1rem; margin-top: 10px;">⌛ El mapa se tarda unos minutos en actualizarse ⌛</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 6. DATOS DE PAGO Y BOTÓN ---
    col1, col2 = st.columns([1.5, 2])
    with col1:
        st.info("""
        **🏦 DATOS DE PAGO:**
        * Bbva
        * Cuenta clave: 012 180 01580888896 1
        * Israel Sámano
        """)
    with col2:
        st.write("")
        st.write("")
        link_wa = "https://wa.me/5542006418?text=Hola%20Rifas%20los%20gueros!%20Ya%20realice%20mi%20pago."
        st.link_button("Apartar por WhatsApp 📱", link_wa, use_container_width=True)

    st.success("### 📸 Recuerda poner tu nombre completo en el concepto del comprobante ✨")

except Exception as e:
    st.error(f"Error al cargar el mapa: {e}")
