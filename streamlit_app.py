import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🧪 Simulador de Calidad del Agua - Modelo Streeter-Phelps")

with st.form("form_datos"):
    st.subheader("🔷 Datos del río")
    Qr = st.number_input("Caudal del río (L/s)", value=3000.0)
    Lr = st.number_input("DBO del río (mg/L)", value=10.0)
    ODr = st.number_input("OD del río (mg/L)", value=4.0)
    Vr = st.number_input("Velocidad del río (m/s)", value=0.9)
    Ar = st.number_input("Ancho del río (m)", value=10.0)
    Pr = st.number_input("Profundidad del río (m)", value=1.5)

    st.subheader("🔷 Datos del vertimiento")
    Qv = st.number_input("Caudal del vertimiento (L/s)", value=6.611)
    Lv = st.number_input("DBO del vertimiento (mg/L)", value=400.0)
    ODv = st.number_input("OD del vertimiento (mg/L)", value=3.0)

    st.subheader("🔷 Parámetros del modelo")
    Kd = st.number_input("Tasa de desoxigenación Kd (1/día)", value=0.2)
    Kr = st.number_input("Tasa de reaireación Kr (1/día)", value=0.5)
    ODsat = st.number_input("OD de saturación (mg/L)", value=8.0)

    st.subheader("🔷 Parámetros de simulación")
    distancia_max = st.number_input("Distancia máxima (m)", value=10000.0)
    paso_m = st.number_input("Paso entre puntos (m)", value=100.0)

    submitted = st.form_submit_button("Simular")

if submitted:
    Qt = Qr + Qv
    L0 = (Qr * Lr + Qv * Lv) / Qt
    OD0 = (Qr * ODr + Qv * ODv) / Qt
    velocidad_dia = Vr * 86400

    distancias = np.arange(0, distancia_max + paso_m, paso_m)
    tiempos = distancias / velocidad_dia
    OD = ODsat - ((Kd * L0) / (Kr - Kd)) * (np.exp(-Kd * tiempos) - np.exp(-Kr * tiempos))

    fig, ax = plt.subplots()
    ax.plot(distancias, OD, label="Oxígeno Disuelto", color="blue")
    ax.axhline(2, color='red', linestyle='--', label="Límite anóxico (2 mg/L)")
    ax.set_xlabel("Distancia río abajo (m)")
    ax.set_ylabel("Oxígeno Disuelto (mg/L)")
    ax.set_title("Simulación del OD en función de la distancia")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    st.success("✅ Simulación completada")
