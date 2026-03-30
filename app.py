import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import urllib.parse

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Los Güeros", layout="centered", page_icon="🎟️")

# --- 2. CONEXIÓN AL EXCEL (FORZAR ACTUALIZACIÓN) ---
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=10)
def cargar_datos(url):
    # Lee 'Registro', empieza en los datos reales (Fila 7)
    df = pd.read_excel(url, sheet_name="Registro", skiprows=6, engine='openpyxl')
    return df

# Título Principal
st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 03/04/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_full = cargar_datos(URL_DRIVE)
    N = 100 
    info_boletos = {}
    
    # --- 3. PROCESAR ESTADOS PARA PINTAR EL MAPA ---
    for _, row in df_full.iterrows():
        try:
            # Columna E (índice 4): Números seleccionados
            # Columna F (índice 5): Estatus (Pagado/Pendiente)
            if pd.notna(row.iloc[4]): 
                nums = str(row.iloc[4]).replace(" ", "").split(',')
                estado = str(row.iloc[5]).strip().lower() 
                
                for n in nums:
                    if n:
                        num_int = int(float(n))
                        info_boletos[num_int] = estado
        except:
            continue

    # --- 4. MAPA DE BOLETOS ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black' # Blanco - Disponible
        
        estado = info_boletos.get(i, "")
        
        if 'pagado' in estado:
            color, txt_c = '#28a745', 'white' # Verde - Pagado
        elif 'pendiente' in estado:
            color, txt_c = '#ffc107', 'black' # Amarillo - Pendiente
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    st.pyplot(fig)

    # --- 5. LEYENDA Y ACTUALIZACIÓN ---
    st.markdown("""
        <div style="text-align: center; font-size: 0.9rem; line-height: 1.6;">
            <span style="color: #28a745;">●</span> <b>Verde:</b> Pagado | 
            <span style="color: #ffc107;">●</span> <b>Amarillo:</b> Pendiente | 
            <span style="color: #bcbcbc;">○</span> <b>Blanco:</b> Disponible<br>
            <b>Precio de Boleto: $170</b><br>
            <i style="color: gray;">El mapa se tarda unos minutos en actualizarse ⌛</i>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # --- 6. DATOS DE PAGO ---
    st.markdown("### 🏦 DATOS DE PAGO:")
    st.info("""
    - **Banco:** Banamex
    - **Cuenta:** 002180702288920746
    - **Nombre:** Rodrigo Antimo Mora
    """)

    # --- 7. BOTÓN WHATSAPP VERDE ---
    numero_wa = "5542006418" # Coloca tu número aquí
    mensaje_wa = "Hola Rifa los gueros, Ya realice mi pago Aqui temando el comprobante para registrar mis boletos"
    mensaje_codificado = urllib.parse.quote(mensaje_wa)
    wa_link = f"https://wa.me/{numero_wa}?text={mensaje_codificado}"
    
    st.markdown(f"""
        <a href="{wa_link}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 1.2rem;">
                MANDAR COMPROBANTE POR WHATSAPP ✅📱
            </div>
        </a>
    """, unsafe_allow_html=True)
    
    st.write("")

    # --- 8. MENSAJES FINALES ---
    st.warning("### 📸 ¡RECUERDA ENVIAR TU COMPROBANTE! ✨\n\n**Nota:** En el concepto del pago favor de poner su **Nombre**.")
    
    st.error("❗ UNA VEZ REALIZADO TU PAGO, TIENES 24 HRS PARA MANDAR TU COMPROBANTE, DE LO CONTRARIO EL NÚMERO SE LIBERARÁ.")

except Exception as e:
    st.error("Error al conectar con Google Sheets. Verifica los permisos de compartir.")
