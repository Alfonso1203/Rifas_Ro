import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Rifa Los Güeros", layout="wide")

ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=2)
def cargar_datos():
    # Leemos el archivo completo para buscar los datos dinámicamente
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", engine='openpyxl')
    return df

st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 10/04/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_raw = cargar_datos()
    INICIO = 100
    FIN = 1000
    info_boletos = {}
    
    # --- LÓGICA DE PROCESAMIENTO (PUNTOS Y COMAS) ---
    for index, row in df_raw.iterrows():
        try:
            # Columna D (3): Números | Columna F (5): Estatus
            val_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            val_estatus = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""
            
            if val_nums and val_nums.lower() not in ['nan', 'numero seleccionado']:
                # Reemplazamos puntos por comas para estandarizar la separación
                lista_n = val_nums.replace('.', ',').split(',')
                for n in lista_n:
                    n_limpio = n.strip().split('.')[0]
                    if n_limpio.isdigit():
                        num_int = int(n_limpio)
                        if INICIO <= num_int <= FIN:
                            # Prioridad: Pagado se queda como pagado
                            if info_boletos.get(num_int) != "pagado":
                                info_boletos[num_int] = val_estatus
        except:
            continue

    # --- 2. CREACIÓN DEL MAPA (100 AL 1000) ---
    columnas = 20 # 20 columnas se ve bien para este rango
    total_numeros = (FIN - INICIO) + 1
    filas = int(np.ceil(total_numeros / columnas))
    
    fig, ax = plt.subplots(figsize=(15, filas * 0.6))
    
    for i in range(total_numeros):
        num_actual = INICIO + i
        f, c = i // columnas, i % columnas
        
        color, txt_c = 'none', 'white' 
        est = info_boletos.get(num_actual, "")
        
        if 'pagado' in est:
            color, txt_c = '#28a745', 'white' 
        elif 'pendiente' in est:
            color, txt_c = '#ffc107', 'black' 
        
        rect = plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#444444', linewidth=0.5)
        ax.add_patch(rect)
        ax.text(c + 0.45, -f + 0.4, str(num_actual), ha='center', va='center', 
                fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.2, columnas)
    ax.set_ylim(-filas + 0.2, 0.8)
    ax.axis('off')
    st.pyplot(fig, transparent=True)

    # --- 3. LEYENDA Y NOTAS ---
    st.markdown(f"""
        <div style="text-align: center; border: 1px solid #444; padding: 15px; border-radius: 10px; background-color: #121212; max-width: 600px; margin: 0 auto;">
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

    # --- 4. WHATSAPP Y PAGOS ---
    msg_wa = "Hola Rifas los gueros! Ya realice mi pago. Aquí te mando mi comprobante."
    link_wa = f"https://wa.me/5542006418?text={msg_wa.replace(' ', '%20')}"

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.info("**🏦 DATOS DE PAGO:**\n- Banamex\n- Cuenta: 002180702288920746\n- Rodrigo Antimo Mora")
    with c2:
        st.write("") 
        st.link_button("Apartar por WhatsApp 📱", link_wa, use_container_width=True)

    st.success("### 📸 ¡RECUERDA PONER TU NOMBRE COMPLETO EN EL CONCEPTO! ✨")

except Exception as e:
    st.error(f"Error: {e}")
