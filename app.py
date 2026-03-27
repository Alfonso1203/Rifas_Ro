import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rifa Rodrigo 2026", layout="centered")

# --- 2. CONEXIÓN AL EXCEL DE DRIVE ---
ID_ARCHIVO = "1lJKiR8B8_DbhTFVXXxdVoexMZ6pS3y6w"
URL_DRIVE = f'https://docs.google.com/spreadsheets/d/{ID_ARCHIVO}/export?format=xlsx'

@st.cache_data(ttl=30) # Se actualiza cada 30 segundos
def cargar_datos():
    # Saltamos 6 filas para llegar a los datos reales (Nombre en Col A, Apellido Col B, etc.)
    return pd.read_excel(URL_DRIVE, sheet_name="Registro", skiprows=6, engine='openpyxl')

st.title("🎟️ BOLETOS RIFA 27/03/2026 🎟️")

try:
    df = cargar_datos()
    N = 100 # Total de boletos
    info_boletos = {}
    
    # --- 3. PROCESAR INFORMACIÓN ---
    for _, row in df.iterrows():
        try:
            # Columna D (índice 3): Números seleccionados
            if pd.notna(row.iloc[3]): 
                nums = str(row.iloc[3]).replace(" ", "").split(',')
                nombre = str(row.iloc[0])   # Columna A
                apellido = str(row.iloc[1]) # Columna B
                estado = str(row.iloc[4]).strip().lower() # Columna E (Estatus)
                
                for n in nums:
                    if n:
                        num_int = int(float(n))
                        info_boletos[num_int] = {
                            "nombre": nombre, "apellido": apellido, "estado": estado
                        }
        except:
            continue

    # --- 4. DIBUJAR EL MAPA ---
    columnas = 15
    filas = int(np.ceil(N / columnas))
    fig, ax = plt.subplots(figsize=(10, filas * 0.7 + 1))
    
    for i in range(1, N + 1):
        f, c = (i - 1) // columnas, (i - 1) % columnas
        color, txt_c = 'white', 'black'
        
        info = info_boletos.get(i, {"estado": ""})
        if 'pagado' in info["estado"]:
            color, txt_c = '#28a745', 'white' # Verde
        elif 'pendiente' in info["estado"]:
            color, txt_c = '#ffc107', 'black' # Amarillo
        
        ax.add_patch(plt.Rectangle((c, -f), 0.9, 0.8, facecolor=color, edgecolor='#bcbcbc', linewidth=0.5))
        ax.text(c + 0.45, -f + 0.4, str(i), ha='center', va='center', fontsize=8, fontweight='bold', color=txt_c)

    ax.set_xlim(-0.5, 15); ax.set_ylim(-filas - 0.5, 1); ax.axis('off')
    st.pyplot(fig)

    # --- 5. INTERACTIVIDAD Y LEYENDA ---
    st.markdown("<p style='text-align: center; color: gray;'><i>Actualización automática desde Excel cada 30 seg ⏳</i></p>", unsafe_allow_html=True)
    
    st.markdown("### 🔍 Consultar dueño de boleto")
    num_buscado = st.number_input("Digita el número de boleto:", min_value=1, max_value=N, step=1)
    
    if num_buscado in info_boletos:
        b = info_boletos[num_buscado]
        st.success(f"👤 **Dueño:** {b['nombre']} {b['apellido']}  \n📌 **Estatus:** {b['estado'].capitalize()}")
    else:
        st.info("✨ Este boleto está **Disponible**")

    st.write("---")
    
    # --- 6. DATOS DE PAGO Y WHATSAPP ---
    c1, c2 = st.columns(2)
    with c1:
        st.info("**🏦 DATOS DE PAGO:**\n- Banamex\n- Cuenta: 002180702288920746\n- Rodrigo Antimo Mora")
    with c2:
        # ¡IMPORTANTE: Pon tu número real aquí!
        numero_wa = "52XXXXXXXXXX" 
        wa_link = f"https://wa.me/{numero_wa}?text=Hola%20Rodrigo,%20quiero%20el%20boleto%20numero..."
        st.link_button("Apartar por WhatsApp 📱", wa_link, use_container_width=True)

    st.warning("### 📸 ¡RECUERDA TU COMPROBANTE! ✨")

except Exception as e:
    st.error("Error al conectar con el Excel. Revisa que el archivo en Drive esté compartido como 'Cualquier persona con el enlace'.")
