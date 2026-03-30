import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.parse
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Rifa Los Güeros", layout="centered", page_icon="🎟️")

# ID de tu enlace: 1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx&t={int(time.time())}'

@st.cache_data(ttl=2)
def cargar_datos(url):
    # skiprows=2 para que la fila 3 del Excel sea el encabezado real
    df = pd.read_excel(url, sheet_name="Registro", skiprows=2, engine='openpyxl')
    return df

st.markdown("<h1 style='text-align: center;'>🎟️ BOLETOS RIFA 03/04/2026 🎟️</h1>", unsafe_allow_html=True)

try:
    df_full = cargar_datos(URL_DRIVE)
    N = 100 
    info_boletos = {}
    
    # --- 2. LÓGICA DE PINTADO (COLUMNA D Y F) ---
    for _, row in df_full.iterrows():
        try:
            # Columna D (3): Numero seleccionado | Columna F (5): Estatus
            celda_nums = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
            val_estatus = str(row.iloc[5]).strip().lower() if pd.notna(row.iloc[5]) else ""

            if celda_nums and celda_nums.lower() != 'nan':
                # Separamos por comas por si hay varios números en una celda
                partes = celda_nums.split(',')
                for p in partes:
                    # Limpiamos decimales .0 y espacios
                    p_limpia = p.strip().split('.')[0]
                    # Solo nos quedamos con los dígitos
                    num_solo = "".join(filter(str.isdigit, p_limpia))
                    
                    if num_solo:
                        num_id = int(num_solo)
                        if 1 <= num_id <= N:
                            # Guardamos el estatus para este número
                            info_boletos[num_id] = val_estatus
        except:
            continue

    # --- 3. DIBUJAR MAPA ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black' # Por defecto blanco
        
        estado = info_boletos.get(i, "")
        
        # Validación de colores
        if 'pagado' in estado:
            color, txt_c = '#28a745', 'white' # VERDE
        elif 'pendiente' in estado:
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
            <b>Precio de Boleto: $170</b>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # --- 5. PAGOS Y WHATSAPP (LETRAS BLANCAS) ---
    col1, col2 = st.columns(2)
    with col1:
        st.info("**🏦 DATOS DE PAGO:**\n- Banamex\n- Cuenta: 002180702288920746\n- Rodrigo Antimo Mora")
    
    with col2:
        numero_wa = "525542006418" 
        mensaje_wa = "Hola Rodrigo! Ya realicé mi pago. Aquí te mando el comprobante."
        wa_link = f"https://wa.me/{numero_wa}?text={urllib.parse.quote(mensaje_wa)}"
        # Botón con letras blancas
        st.markdown(f'<a href="{wa_link}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:1.1rem; cursor:pointer;">MANDAR COMPROBANTE ✅📱</div></a>', unsafe_allow_html=True)

    st.warning("### 📸 ¡MANDA TU COMPROBANTE! ✨")
    st.error("❗ UNA VEZ REALIZADO TU PAGO, TIENES 24 HRS PARA MANDAR TU COMPROBANTE.")

except Exception as e:
    st.error(f"Conectando con la base de datos... Error: {e}")
