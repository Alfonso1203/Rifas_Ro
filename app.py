import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Rifa Los Güeros", layout="wide")

# CSS para que los boletos se vean grandes y bien definidos en el celular
st.markdown("""
    <style>
    .ticket-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(45px, 1fr));
        gap: 5px;
        padding: 10px;
    }
    .ticket {
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        border: 1px solid #444;
        color: white;
    }
    .pagado { background-color: #28a745 !important; border-color: #1e7e34; }
    .pendiente { background-color: #ffc107 !important; color: black !important; border-color: #d39e00; }
    .disponible { background-color: transparent; border: 1px solid #555; }
    </style>
    """, unsafe_allow_html=True)

ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=2)
def cargar_datos():
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", engine='openpyxl')
    return df

st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 10/04/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_raw = cargar_datos()
    INICIO = 100
    FIN = 1000
    info_boletos = {}
    
    # --- PROCESAMIENTO DE DATOS ---
    for index, row in df_raw.iterrows():
        try:
            val_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            val_estatus = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""
            
            if val_nums and val_nums.lower() not in ['nan', 'numero seleccionado']:
                lista_n = val_nums.replace('.', ',').split(',')
                for n in lista_n:
                    n_limpio = n.strip().split('.')[0]
                    if n_limpio.isdigit():
                        num_int = int(n_limpio)
                        if INICIO <= num_int <= FIN:
                            if info_boletos.get(num_int) != "pagado":
                                info_boletos[num_int] = val_estatus
        except:
            continue

    # --- 2. MAPA INTERACTIVO Y GRANDE ---
    # Creamos el contenedor de la cuadrícula
    ticket_html = '<div class="ticket-container">'
    
    for i in range(INICIO, FIN + 1):
        est = info_boletos.get(i, "")
        clase = "disponible"
        if 'pagado' in est:
            clase = "pagado"
        elif 'pendiente' in est:
            clase = "pendiente"
            
        ticket_html += f'<div class="ticket {clase}">{i}</div>'
    
    ticket_html += '</div>'
    
    # Renderizar el mapa
    st.markdown(ticket_html, unsafe_allow_html=True)

    # --- 3. LEYENDA Y PRECIO ---
    st.markdown(f"""
        <div style="text-align: center; border: 1px solid #444; padding: 15px; border-radius: 10px; background-color: #121212; margin-top: 20px;">
            <span style="color: #28a745; font-size: 1.2rem;">●</span> <b>Pagado</b> &nbsp;&nbsp;
            <span style="color: #ffc107; font-size: 1.2rem;">●</span> <b>Pendiente</b> &nbsp;&nbsp;
            <span style="color: #ffffff; font-size: 1.2rem;">○</span> <b>Disponible</b>
            <br><br>
            <h3 style="margin:0; color: #ffffff;">Precio del boleto: $40</h3>
            <p style="font-size: 0.85rem; color: #888; margin-top: 5px;">
                ⌛ El mapa se tarda en actualizarse unos minutos ⌛
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- 4. BOTONES ---
    msg_wa = "Hola Rifas los gueros! Ya realice mi pago. Aquí te mando mi comprobante."
    link_wa = f"https://wa.me/5542006418?text={msg_wa.replace(' ', '%20')}"

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**🏦 DATOS DE PAGO:**\n- Banamex\n- Cuenta: 002180702288920746\n- Rodrigo Antimo Mora")
    with col2:
        st.write("") 
        st.link_button("Apartar por WhatsApp 📱", link_wa, use_container_width=True)

    st.success("### 📸 ¡RECUERDA PONER TU NOMBRE COMPLETO EN EL CONCEPTO! ✨")

except Exception as e:
    st.error(f"Error: {e}")
