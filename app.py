import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.parse
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Rifa Rodrigo 2026", layout="wide", page_icon="🎟️")

# ID extraído de tu enlace
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=10) # Actualización cada 10 segundos
def cargar_datos():
    # Saltamos 2 filas para llegar a los encabezados en la fila 3
    # Usamos openpyxl para leer archivos .xlsx modernos
    try:
        df = pd.read_excel(URL_DRIVE, sheet_name="Registro", skiprows=2, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

# Título con la nueva fecha
st.markdown("<h1 style='text-align: center;'>🎟️ GRANDIOSA RIFA - 10/04/2026 🎟️</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Mapa de 1000 Boletos</h3>", unsafe_allow_html=True)

df_full = cargar_datos()

if df_full is not None:
    N = 1000 # Nuevo total de boletos
    info_boletos = {}
    
    # --- 2. LÓGICA DEL MAPA (LECTURA REFORZADA) ---
    for index, row in df_full.iterrows():
        try:
            # Forzamos que la celda sea tratada como Texto para evitar errores de formato
            # Columna D (índice 3): Números seleccionados | Columna F (índice 5): Estatus
            celda_raw = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""
            estado = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""
            
            if celda_raw and celda_raw.lower() != 'nan':
                # Procesamos números separados por comas
                nums = celda_raw.split(',')
                for n in nums:
                    # n_limpio: solo se queda con los números, eliminando apóstrofos, ".0" o espacios
                    n_limpio = "".join(filter(str.isdigit, n.strip().split('.')[0]))
                    if n_limpio:
                        num_int = int(n_limpio)
                        if 1 <= num_int <= N:
                            info_boletos[num_int] = estado
        except:
            continue

    # --- 3. CREACIÓN DEL MAPA DE 1000 BOLETOS ---
    # Diseño: 25 columnas x 40 filas = 1000 boletos
    columnas = 25
    filas = int(np.ceil(N / columnas))
    
    # Ajustamos el tamaño de la figura para que sea alta y legible (layout="wide")
    fig, ax = plt.subplots(figsize=(16, filas * 0.4 + 2))
    
    for i in range(1, N + 1):
        # Calculamos fila (f) y columna (c) invertida para que el 1 empiece arriba a la izquierda
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black' # Disponible por defecto
        
        est = info_boletos.get(i, "")
        
        if 'pagado' in est:
            color, txt_c = '#28a745', 'white' # VERDE
        elif 'pendiente' in est:
            color, txt_c = '#ffc107', 'black' # AMARILLO
        
        # Dibujamos el rectángulo del boleto
        ax.add_patch(plt.Rectangle((c, -f), 0.92, 0.85, facecolor=color, edgecolor='#bcbcbc', linewidth=0.3))
        # Ajustamos el tamaño de fuente (fontsize=6) para que quepan 1000 números
        ax.text(c + 0.46, -f + 0.42, str(i), ha='center', va='center', fontsize=6, fontweight='bold', color=txt_c)

    # Configuramos los límites y quitamos los ejes
    ax.set_xlim(-0.5, columnas); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    
    # Usamos container_width=True para que ocupe todo el ancho disponible
    st.pyplot(fig, use_container_width=True)

    # --- 4. LEYENDA SIMPLIFICADA (NUEVO PRECIO SI APLICA) ---
    st.markdown("""
        <div style="text-align: center; border: 1px solid #ddd; padding: 15px; border-radius: 10px; background-color: #f9f9f9;">
            <span style="color: #28a745; font-size: 1.8rem;">●</span> <b>Pagado</b> &nbsp;&nbsp;&nbsp;&nbsp;
            <span style="color: #ffc107; font-size: 1.8rem;">●</span> <b>Pendiente</b> &nbsp;&nbsp;&nbsp;&nbsp;
            <span style="color: #bcbcbc; font-size: 1.8rem;">○</span> <b>Disponible</b>
            <br><br>
            <b style="font-size: 1.3rem;">¡Participa y gana!</b><br>
            <i style="color: gray;">El mapa se actualiza automáticamente cada 10 segundos ⏳</i>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    
    # --- 5. DATOS DE PAGO Y WHATSAPP ---
    col1, col2 = st.columns(2)
    with col1:
        st.info("**🏦 DATOS DE PAGO:**\n- Banamex\n- Cuenta: 002180702288920746\n- Rodrigo Antimo Mora")
    with col2:
        numero_tel = "525542006418" 
        mensaje_wa = "Hola Rodrigo! Quiero apartar boletos para la rifa del 10/04/2026. Aquí está mi comprobante."
        link_wa = f"https://wa.me/{numero_tel}?text={urllib.parse.quote(mensaje_wa)}"
        # Botón grande y llamativo
        st.markdown(f'<a href="{link_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366; color:white; padding:18px; border-radius:12px; text-align:center; font-weight:bold; font-size:1.3rem;">Apartar por WhatsApp 📱✅</div></a>', unsafe_allow_html=True)

    st.warning("### 📸 ¡RECUERDA ENVIAR TU COMPROBANTE! ✨")
    st.error("❗ UNA VEZ REALIZADO TU PAGO, TIENES 24 HRS PARA MANDAR TU COMPROBANTE, DE LO CONTRARIO EL NÚMERO SE LIBERARÁ.")

else:
    st.warning("Esperando conexión con la base de datos... Por favor, asegúrate de que el archivo de Google Sheets tenga permisos de 'Cualquier persona con el enlace puede leer'.")
