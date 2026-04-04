import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Rifa Los Güeros - 1000 Boletos", layout="wide")

ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=2)
def cargar_datos():
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", engine='openpyxl')
    return df

# Título con nueva fecha
st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 10/04/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_raw = cargar_datos()
    N = 1000 # Actualizado a 1000 boletos
    info_boletos = {}
    
    for index, row in df_raw.iterrows():
        try:
            val_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            val_estatus = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""
            
            if val_nums and val_nums.lower() not in ['nan', 'numero seleccionado']:
                lista_n = val_nums.split(',')
                for n in lista_n:
                    n_limpio = n.strip().split('.')[0]
                    if n_limpio.isdigit():
                        num_int = int(n_limpio)
                        if 1 <= num_int <= N:
                            estado_actual = info_boletos.get(num_int, "")
                            if estado_actual != "pagado":
                                info_boletos[num_int] = val_estatus
        except:
            continue

    # --- 2. CREACIÓN DEL MAPA (OPTIMIZADO PARA 1000) ---
    columnas = 25 # Más columnas para que no sea eterno el scroll
    filas = int(np.ceil(N / columnas))
    
    # Ajustamos el tamaño de la figura para que quepan los 1000
    fig, ax = plt.subplots(figsize=(15, filas * 0.5))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'none', 'white' 
        
        est = info_boletos.get(i, "")
        
        if 'pagado' in est:
            color, txt_c = '#28a745', 'white' 
        elif 'pendiente' in est:
            color, txt_c = '#ffc107', 'black' 
        
        rect = plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#444444', linewidth=0.5)
        ax.add_patch(rect)
        
        # El tamaño de fuente se reduce un poco para que quepan números de 3-4 dígitos
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', 
                fontsize=7, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.2, columnas)
    ax.set_ylim(-filas + 0.2, 0.8)
    ax.axis('off')
    st.pyplot(fig, transparent=True)

    # --- 3. LEYENDA, PRECIO ($40) Y NOTA ---
    st.markdown(f"""
        <div style="text-align: center; border: 1px solid #444; padding: 15px; border-radius: 10px; background-color: #121212; max-width: 600px; margin: 0 auto;">
            <span style="color: #28a745; font-size: 1.2rem;">●</span> <b>Pagado</b> &nbsp;&nbsp;
            <span style="color: #ffc107; font-size: 1.2rem;">●</span> <b>Pendiente</b> &nbsp;&nbsp;
            <span style="color: #ffffff; font-size: 1.2rem;">○</span> <b>Disponible</b>
            <br><br>
            <h3 style="margin:0; color: #ffffff;">Precio del boleto: $40</h3>
            <p style="font-size: 0.85rem; color: #888; margin-top: 5px;">
                ⌛ El mapa se tarda en actualizarse unos minutos
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- 4. BOTONES Y DATOS ---
    msg_wa = "Hola Rifas los gueros! Ya realice mi pago. Aquí te mando mi comprobante."
    link_wa = f"https://wa.me/5542006418?text={msg_wa.replace(' ', '%20')}"

    st.write("")
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.info("**🏦 DATOS DE PAGO:**\n- Banamex\n- Cuenta: 002180702288920746\n- Rodrigo Antimo Mora")
    
    with col_der:
        st.write("") 
        st.link_button("Apartar por WhatsApp 📱", link_wa, use_container_width=True)

    st.success("### 📸 ¡RECUERDA MANDAR TU COMPROBANTE Y EN EL CONCEPTO TU NOMBRE COMPLETO! ✨")

except Exception as e:
    st.error(f"Error: {e}")
