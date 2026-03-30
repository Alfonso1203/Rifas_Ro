import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Rifa Los Güeros", layout="centered")

ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
# Forzamos la descarga del archivo fresco
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=2)
def cargar_datos():
    # Eliminamos skiprows para analizar el archivo completo primero
    df = pd.read_excel(URL_DRIVE, sheet_name="Registro", engine='openpyxl')
    return df

st.title("🎟️ BOLETOS RIFA 03/04/2026 🎟️")

try:
    df_raw = cargar_datos()
    
    # --- LIMPIEZA DINÁMICA ---
    # Buscamos la fila donde realmente empiezan los datos (donde 'Estatus' no sea nulo)
    # O simplemente filtramos las filas que tengan datos en la columna de números (Columna D / Índice 3)
    
    N = 100 
    info_boletos = {}
    
    # Iteramos sobre todas las filas del archivo
    for index, row in df_raw.iterrows():
        try:
            # Intentamos obtener valores de las columnas D (3) y F (5)
            # Usamos iloc para evitar problemas si el encabezado no se leyó bien
            val_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            val_estatus = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""
            
            # Si la celda contiene números y no es el encabezado "Numero seleccionado"
            if val_nums and val_nums.lower() not in ['nan', 'numero seleccionado']:
                # Separar números por comas
                lista_n = val_nums.split(',')
                for n in lista_n:
                    # Limpiar el número (quitar .0 o espacios)
                    n_limpio = n.strip().split('.')[0]
                    if n_limpio.isdigit():
                        num_int = int(n_limpio)
                        if 1 <= num_int <= N:
                            # Prioridad: Si ya es 'pagado', no lo cambies a 'pendiente'
                            nuevo_estado = val_estatus
                            estado_actual = info_boletos.get(num_int, "")
                            if estado_actual != "pagado":
                                info_boletos[num_int] = nuevo_estado
        except:
            continue

    # --- 2. CREACIÓN DEL MAPA ---
    columnas = 10
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.8))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'none', 'white' 
        
        est = info_boletos.get(i, "")
        
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

    # --- 3. LEYENDA Y DATOS DE PAGO ---
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
    st.error(f"Error al procesar el Excel: {e}")
