import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.parse
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Rifa Los Güeros", layout="centered", page_icon="🎟️")

ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=2)
def cargar_datos(url):
    # Cargamos el archivo. skiprows=2 para saltar el logo/título y llegar a los encabezados.
    df = pd.read_excel(url, sheet_name="Registro", skiprows=2, engine='openpyxl')
    # Limpiamos nombres de columnas por si tienen espacios locos
    df.columns = [str(c).strip() for c in df.columns]
    return df

st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 03/04/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df = cargar_datos(URL_DRIVE)
    N = 100 
    info_boletos = {}
    
    # Identificamos las columnas por nombre exacto para que no falle si se mueven
    col_num = "Numero seleccionado"
    col_est = "Estatus"

    if col_num in df.columns and col_est in df.columns:
        for _, row in df.iterrows():
            celda_nums = str(row[col_num]).strip()
            val_estatus = str(row[col_est]).strip().lower()

            if celda_nums and celda_nums.lower() != 'nan':
                # Separar por comas (ej. "2, 4.0, 10")
                partes = celda_nums.split(',')
                for p in partes:
                    # Quitamos decimales y espacios
                    p_limpia = p.strip().split('.')[0]
                    num_solo = "".join(filter(str.isdigit, p_limpia))
                    
                    if num_solo:
                        num_id = int(num_solo)
                        if 1 <= num_id <= N:
                            info_boletos[num_id] = val_estatus
    else:
        st.error(f"No encontré las columnas '{col_num}' o '{col_est}'. Revisa los nombres en tu Excel.")

    # --- 2. DIBUJAR MAPA ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black' 
        
        estado = info_boletos.get(i, "")
        
        if "pagado" in estado:
            color, txt_c = '#28a745', 'white' # VERDE
        elif "pendiente" in estado:
            color, txt_c = '#ffc107', 'black' # AMARILLO
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    st.pyplot(fig)

    # --- 3. LEYENDA Y PAGOS ---
    st.markdown("""
        <div style="text-align: center; font-size: 0.9rem; border: 1px solid #ddd; padding: 10px; border-radius: 10px;">
            <span style="color: #28a745; font-size: 1.2rem;">●</span> <b>Pagado</b> | 
            <span style="color: #ffc107; font-size: 1.2rem;">●</span> <b>Pendiente</b> | 
            <span style="color: #bcbcbc; font-size: 1.2rem;">○</span> <b>Disponible</b><br>
            <b>Precio de Boleto: $170</b>
        </div>
    """, unsafe_allow_html=True)

    st.info("**🏦 DATOS DE PAGO:**\n- Banamex | Cuenta: 002180702288920746 | Rodrigo Antimo Mora")

    numero_wa = "525542006418" 
    mensaje_wa = "Hola Rodrigo! Ya realicé mi pago. Aquí te mando el comprobante."
    wa_link = f"https://wa.me/{numero_wa}?text={urllib.parse.quote(mensaje_wa)}"
    
    st.markdown(f'<a href="{wa_link}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:1.1rem;">MANDAR COMPROBANTE POR WHATSAPP ✅📱</div></a>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
