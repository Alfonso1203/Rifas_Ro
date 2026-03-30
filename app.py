import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.parse
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Rifa Rodrigo 2026", layout="centered")

# ID actualizado de tu Google Sheets
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=5) 
def cargar_datos():
    # Lee desde la fila 3 (skiprows=2) para encontrar Numero seleccionado (Col D) y Estatus (Col F)
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", skiprows=2, engine='openpyxl')
    return df

st.title("🎟️ BOLETOS RIFA 27/03/2026 🎟️")

try:
    df_full = cargar_datos()
    N = 100 
    info_boletos = {}
    
    # --- 2. LÓGICA DEL MAPA ---
    for index, row in df_full.iterrows():
        try:
            # Columna D (índice 3) y Columna F (índice 5)
            celda_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            estado = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""
            
            if celda_nums and celda_nums.lower() != 'nan':
                nums = celda_nums.split(',')
                for n in nums:
                    n_limpio = n.strip().split('.')[0]
                    if n_limpio.isdigit():
                        num_int = int(n_limpio)
                        info_boletos[num_int] = {
                            "nombre": str(row.iloc[1]), 
                            "apellido": str(row.iloc[2]), 
                            "estado": estado
                        }
        except:
            continue

    # --- 3. CREACIÓN DEL MAPA ---
    columnas = 15
    filas = int(np.ceil(100 / columnas))
    fig, ax = plt.subplots(figsize=(12, filas * 0.7 + 2))
    
    for i in range(1, 101):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black'
        
        info = info_boletos.get(i, {"estado": ""})
        est = info["estado"]
        
        if 'pagado' in est:
            color, txt_c = '#28a745', 'white' 
        elif 'pendiente' in est:
            color, txt_c = '#ffc107', 'black' 
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#333333', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    st.pyplot(fig)

    # --- 4. NUEVA LEYENDA SIMPLIFICADA ---
    st.markdown("""
        <div style="text-align: center; border: 1px solid #ddd; padding: 15px; border-radius: 10px;">
            <span style="color: #28a745; font-size: 1.5rem;">●</span> <b>Pagado</b> &nbsp;&nbsp;
            <span style="color: #ffc107; font-size: 1.5rem;">●</span> <b>Pendiente</b> &nbsp;&nbsp;
            <span style="color: #bcbcbc; font-size: 1.5rem;">○</span> <b>Disponible</b>
            <br><br>
            <b style="font-size: 1.2rem;">Precio del boleto: $170</b>
        </div>
    """, unsafe_allow_html=True)

    # --- 5. DETALLES AL SELECCIONAR ---
    st.markdown("### 🔍 Consultar detalle de boleto")
    num_consulta = st.number_input("Ingresa el número de boleto:", min_value=1, max_value=100, step=1)
    
    if num_consulta in info_boletos:
        det = info_boletos[num_consulta]
        st.write(f"👤 **Nombre:** {det['nombre']} {det['apellido']}")
        st.write(f"🎟️ **Número:** {num_consulta}")
        st.write(f"📌 **Estatus:** {det['estado'].capitalize()}")
    else:
        st.write("✨ Este boleto está **Disponible**")

    st.write("---")
    
    # --- 6. DATOS DE PAGO Y WHATSAPP ---
    col1, col2 = st.columns(2)
    with col1:
        st.info("**🏦 DATOS DE PAGO:**\n- Banamex\n- Cuenta: 002180702288920746\n- Rodrigo Antimo Mora")
    with col2:
        numero_tel = "525542006418" 
        link_wa = f"https://wa.me/{numero_tel}?text=Hola%20Rodrigo!%20Ya%20realice%20mi%20pago.%20Aqui%20te%20mando%20mi%20comprobante."
        st.link_button("Apartar por WhatsApp 📱", link_wa, use_container_width=True)

    st.warning("### 📸 ¡MANDA TU COMPROBANTE! ✨")

except Exception as e:
    st.error(f"Conectando con la base de datos... Error: {e}")
