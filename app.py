import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.parse
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Los Güeros", layout="centered", page_icon="🎟️")

# ID de tu Google Sheets
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=2)
def cargar_datos(url):
    # Lee desde la fila 3 (skiprows=2) para encontrar los encabezados
    df = pd.read_excel(url, sheet_name="Registro", skiprows=2, engine='openpyxl')
    return df

st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 03/04/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df = cargar_datos(URL_DRIVE)
    N = 100 
    info_boletos = {}
    
    # --- 2. LÓGICA DE PINTADO (COLUMNA D Y F) ---
    for _, row in df.iterrows():
        try:
            # Columna D (Índice 3): Numero seleccionado | Columna F (Índice 5): Estatus
            celda_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            val_estatus = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""

            if celda_nums and celda_nums.lower() != 'nan':
                # Dividimos por coma la cadena de números
                partes = celda_nums.split(',')
                for p in partes:
                    # Limpiamos espacios y posibles decimales accidentales del Excel (.0)
                    p_limpia = p.strip().split('.')[0]
                    if p_limpia.isdigit():
                        num_id = int(p_limpia)
                        if 1 <= num_id <= N:
                            info_boletos[num_id] = val_estatus
        except:
            continue

    # --- 3. DIBUJAR MAPA ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black' 
        
        estado = info_boletos.get(i, "")
        
        # Comparación de estatus flexible (insensible a mayúsculas)
        if "pagado" in estado:
            color, txt_c = '#28a745', 'white' # VERDE
        elif "pendiente" in estado:
            color, txt_c = '#ffc107', 'black' # AMARILLO
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    st.pyplot(fig)

    # --- 4. LEYENDA (SOLO PELOTITAS) ---
    st.markdown("""
        <div style="text-align: center; font-size: 0.9rem; border: 1px solid #ddd; padding: 10px; border-radius: 10px;">
            <span style="color: #28a745; font-size: 1.2rem;">●</span> <b>Pagado</b> | 
            <span style="color: #ffc107; font-size: 1.2rem;">●</span> <b>Pendiente</b> | 
            <span style="color: #bcbcbc; font-size: 1.2rem;">○</span> <b>Disponible</b><br>
            <b>Precio de Boleto: $170</b><br>
            <i style="color: gray;">El mapa se tarda unos minutos en actualizarse ⌛</i>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # --- 5. DATOS DE PAGO ---
    st.markdown("### 🏦 DATOS DE PAGO:")
    st.info("- **Banco:** Banamex\n- **Cuenta:** 002180702288920746\n- **Nombre:** Rodrigo Antimo Mora")

    # --- 6. BOTÓN WHATSAPP (LETRAS BLANCAS) ---
    numero_wa = "525542006418" 
    mensaje_wa = "Hola Rifa los gueros, Ya realice mi pago Aquí te mando el comprobante para registrar mis boletos"
    wa_link = f"https://wa.me/{numero_wa}?text={urllib.parse.quote(mensaje_wa)}"
    
    st.markdown(f'<a href="{wa_link}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:1.2rem;">MANDAR COMPROBANTE POR WHATSAPP ✅📱</div></a>', unsafe_allow_html=True)
    
    st.write("")
    st.warning("### 📸 ¡RECUERDA ENVIAR TU COMPROBANTE! ✨")
    st.error("❗ UNA VEZ REALIZADO TU PAGO, TIENES 24 HRS PARA MANDAR TU COMPROBANTE, DE LO CONTRARIO EL NÚMERO SE LIBERARÁ.")

except Exception as e:
    st.error(f"Error técnico: {e}")
