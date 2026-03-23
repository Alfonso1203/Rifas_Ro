import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Rodrigo 2026", layout="centered")

# --- 2. CONFIGURACIÓN DE DATOS (GOOGLE DRIVE) ---
# Tu ID de archivo ya está integrado
ID_DE_TU_ARCHIVO = '1UXXSDdQCZ9jwYBByHJCxos7Z3QI-EDd1'
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_DE_TU_ARCHIVO}/export?format=xlsx'

# Tiempo de actualización: 30 segundos
@st.cache_data(ttl=30)  
def cargar_datos():
    return pd.read_excel(URL_DRIVE, sheet_name="Registro", engine='openpyxl')

# --- 3. TÍTULO ---
st.title("🎟️ BOLETOS RIFA 27/03/2026 🎟️")

try:
    df_full = cargar_datos()
    
    # Obtener el total de boletos (N) de la celda U3
    N = int(df_full.iloc[2, 20]) if pd.notna(df_full.iloc[2, 20]) else 100
    
    # Datos de los boletos empiezan en la fila 7
    df = df_full.iloc[6:].copy()
    
    # Diccionario para rastrear el estado de cada número
    estatus_boletos = {}
    for _, row in df.iterrows():
        if pd.notna(row.iloc[3]): # Columna D (Números)
            nums = str(row.iloc[3]).replace(" ", "").split(',')
            estado = str(row.iloc[4]).strip().lower() # Columna E (Estatus)
            for n in nums:
                try:
                    num_int = int(float(n))
                    estatus_boletos[num_int] = estado
                except:
                    continue

    # --- 4. CREACIÓN DEL MAPA VISUAL ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(12, filas * 0.7 + 2))
    fig.patch.set_facecolor('white')
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black' # Por defecto: Disponible
        
        est = estatus_boletos.get(i, "")
        if 'pagado' in est:
            color, txt_c = '#28a745', 'white' # Verde
        elif 'pendiente' in est:
            color, txt_c = '#ffc107', 'black' # Amarillo
        
        # Dibujar cuadro
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#333333', linewidth=0.5))
        # Poner número
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    # Leyenda del mapa
    y_l = -filas - 0.5
    ax.plot(2, y_l, 'o', color='#28a745', markersize=10); ax.text(2.6, y_l - 0.1, 'Pagado', fontsize=10, fontweight='bold')
    ax.plot(6, y_l, 'o', color='#ffc107', markersize=10); ax.text(6.6, y_l - 0.1, 'Pendiente', fontsize=10, fontweight='bold')
    ax.plot(10, y_l, 'o', color='white', markeredgecolor='black', markersize=10); ax.text(10.6, y_l - 0.1, 'Disponible', fontsize=10, fontweight='bold')

    ax.set_xlim(-0.5, 15)
    ax.set_ylim(-filas - 1.5, 1)
    ax.axis('off')
    
    # Mostrar el mapa (SOLO UNA VEZ)
    st.pyplot(fig)

    # --- 5. LEYENDA DE ESPERA ---
    st.markdown("<p style='text-align: center; color: gray;'><i>Una vez hecho tu pago, tus boletos se verán reflejados en unos minutos ⏳</i></p>", unsafe_allow_html=True)
    
    st.write("---")

    # --- 6. SECCIÓN DE PAGO Y CONTACTO (COLUMNAS) ---
    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **🏦 DATOS DE PAGO:**
        - **Banco:** Banamex
        - **Cuenta:** 002180702288920746
        - **Tipo:** Débito
        - **Nombre:** Rodrigo Antimo Mora
        """)

    with col2:
        # Reemplaza el número abajo con el tuyo real
        numero_tel = "525542006418" 
        mensaje_wa = "¡Hola Rodrigo! Ya realicé mi pago. Aquí te mando mi comprobante para registrar mis boletos."
        link_wa = f"https://wa.me/{numero_tel}?text={mensaje_wa.replace(' ', '%20')}"
        
        st.success("**💬 ¿LISTO PARA APARTAR?**")
        st.markdown("### Apartar mi boleto")
        st.link_button("Click aquí para ir a WhatsApp 📱", link_wa, use_container_width=True)

    # --- 7. RECORDATORIO FINAL ---
    st.write("") 
    st.warning("""
    ### 📸 ¡RECUERDA TU COMPROBANTE!
    Es muy importante que nos mandes una **foto o captura de tu comprobante de pago** por WhatsApp para poder registrar tus boletos oficialmente. 🎟️✨
    """)

except Exception as e:
    st.warning("Estamos actualizando el mapa con los últimos boletos. Vuelve a cargar en un momento.")
