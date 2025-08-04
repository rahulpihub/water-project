import streamlit as st
import pandas as pd
import numpy as np
import math

st.set_page_config(page_title="Wall & Bulk Decay Calculator", layout="wide")

# Apply secondary background color
st.markdown("""
    <style>
        [data-testid="stSidebar"], .stSidebar, .css-1d391kg {
            background-color: #2DA5BB !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Chlorine Decay Coefficient Calculator")

# Constants
initial_chlorine = 2.0
final_chlorine = 0.96
pipe_material_factor = 0.8

# Reservoir dataset
reservoirs_by_region = {
    "Chennai / Tiruvallur": [
        "Poondi Dam (Poondi Reservoir) – Tiruvallur District",
        "Thervoy Kandigai Dam – Tiruvallur District"
    ],
    "Coimbatore / Pollachi": [
        "Aliyar Reservoir – Coimbatore (Pollachi) District",
        "Amaravathi Dam & Reservoir – Tiruppur District (west of Coimbatore)",
        "Sholayar Dam (Upper Sholayar) – Coimbatore District",
        "Lower Nirar Dam – Coimbatore District"
    ],
    "Salem District": [
        "Mettur Dam (Stanley Reservoir) – Salem District"
    ],
    "Erode District": [
        "Bhavanisagar Dam (Lower Bhavani) – Erode District",
        "Varattupallam Dam – Erode District",
        "Kunderipallam Dam – Erode District"
    ],
    "Dharmapuri District": [
        "Chinnar (Panchapalli) Dam – Dharmapuri District",
        "Nagavathi Dam – Dharmapuri District",
        "Kesarigulihalla Dam – Dharmapuri District",
        "Maruthupandiyar/Dharmapuri related – including Thoppaiyar, Thumblahalli – Dharmapuri District"
    ],
    "Krishnagiri District": [
        "Krishnagiri Dam – Krishnagiri District",
        "Barur Dam – Krishnagiri District",
        "Pambar Dam – Krishnagiri District",
        "Shoolagiri Chinnar Dam – Krishnagiri District"
    ],
    "Dindigul District": [
        "Kodaganar Dam – Dindigul District",
        "Nanganjiyar Dam – Dindigul District",
        "Varadhamanadhi Dam – Dindigul District",
        "Marudhanadhi Dam – Dindigul District",
        "Pallar Porundalar (Ponnaniar) Dam – Dindigul District"
    ],
    "Theni District": [
        "Vaigai Dam (Vaigai Reservoir) – Theni District",
        "Manjalar Dam – Theni District",
        "Sothupparai Dam – Theni District",
        "Periyar Forebay – Theni District",
        "Eravangalar Dam – Theni District",
        "Shanmuganadhi Dam – Theni District"
    ],
    "Tirunelveli District": [
        "Papanasam Dam – Tirunelveli District",
        "Chittar I & II Dams – Tirunelveli District",
        "Gundar Dam – Tirunelveli District",
        "Karuppanadhi Dam – Tirunelveli District",
        "Nambiar Dam – Tirunelveli District",
        "Servalar Dam – Tirunelveli District",
        "Vadakku Paichaiyar Dam – Tirunelveli District"
    ],
    "Viluppuram District": [
        "Manimukthanadhi Dam – Viluppuram District",
        "Vidur Dam – Viluppuram District"
    ],
    "Vellore District": [
        "Mordhana Dam (Koundanyanadhi) – Vellore District"
    ],
    "Tiruppur District": [
        "Nallathangal Odai Dam – Tiruppur District",
        "Uppar (Erode) Dam – Tiruppur District",
        "Thirumurthi Dam – Tiruppur District"
    ],
    "Perambalur District": [
        "Visvakudi Dam – Perambalur District",
        "Kottarai Dam – Perambalur District"
    ],
    "Kanniyakumari District": [
        "Pechiparai Dam – Kanyakumari District",
        "Lower Kodayar Dam – Kanyakumari District",
        "Perunchani Dam – Kanyakumari District",
        "Puthen Dam – Kanyakumari District",
        "Poigaiyar Dam – Kanyakumari District",
        "Kuttiyar Dam – Kanyakumari District"
    ],
    "Nilgiris District": [
        "Avalanche Dam – Nilgiris District",
        "Emerald Dam – Nilgiris District",
        "Glenmorgan – Nilgiris District",
        "Moyar Forebay – Nilgiris District",
        "Pykara Dam – Nilgiris District",
        "Upper Bhavani Dam – Nilgiris District"
    ]
}

# Utility functions
def contact_time(length_m, velocity):
    return length_m / velocity / 3600 if velocity > 0 else None

def base_decay(C0, C, t):
    try:
        return -math.log(C / C0) / t if all([C0 > 0, C > 0, t and t > 0]) else None
    except:
        return None

def adjust_bulk_decay(k_b, iron, nitrate, manganese):
    if k_b is None:
        return None
    return k_b + (iron * 0.1) + (nitrate * 0.05) + (manganese * 0.08)

def apply_correction_factors(k_w_base, ph, iron, nitrite, manganese, h2s):
    f_ph = 1 + 0.02 * (ph - 7)
    f_iron = 1 + 0.15 * iron
    f_manganese = 1 + 0.12 * manganese
    f_nitrite = 1 + 0.1 * nitrite
    f_h2s = 1 + 0.2 * h2s
    correction_factor = f_ph * f_iron * f_manganese * f_nitrite * f_h2s
    return k_w_base * correction_factor

# Sidebar mode selection
st.sidebar.title("Mode")
input_mode = st.sidebar.radio("Choose input mode", ["Upload Dataset", "Manual Input"])

# ------------------------------
# Mode 1: Upload Dataset
# ------------------------------
if input_mode == "Upload Dataset":
    decay_mode = st.sidebar.radio("Select Decay Type", ["Wall Decay", "Bulk Decay"])

    # Reservoir Selection (button logic)
    st.sidebar.markdown("### Reservoir Selection")
    selected_region = None
    for region in reservoirs_by_region.keys():
        if st.sidebar.button(region):
            selected_region = region

    # Show reservoirs on main page
    if selected_region:
        st.subheader(f"Reservoirs in {selected_region}")
        for reservoir in reservoirs_by_region[selected_region]:
            st.write(f"- {reservoir}")

    uploaded_file = st.file_uploader("Upload your dataset as CSV", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, encoding='cp1252')
        except:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

        df.columns = df.columns.str.strip().str.lower()
        st.subheader("Uploaded Data Preview")
        st.dataframe(df)

        if 'velocity m/s' not in df.columns:
            st.error("Your dataset must include a 'Velocity m/s' column.")
        else:
            if decay_mode == "Wall Decay":
                try:
                    df['pipe diameter (m)'] = df['diameter (mm)'] / 1000
                    df['initial chlorine'] = initial_chlorine
                    df['contact time (hrs)'] = df.apply(lambda row: contact_time(row['length (m)'], row['velocity m/s']), axis=1)
                    df['ln_ratio'] = np.log(df['final chlorine (ppm)'] / df['initial chlorine'])
                    df['k_w_base'] = - (df['pipe diameter (m)'] / (4 * df['contact time (hrs)'])) * df['ln_ratio']
                    df['k_w_adjusted'] = df['k_w_base'] * pipe_material_factor

                    if {'ph', 'iron', 'nitrite', 'manganese', 'hydrogen sulfide'}.issubset(df.columns):
                        df['f_ph'] = 1 + 0.02 * (df['ph'] - 7)
                        df['f_iron'] = 1 + 0.15 * df['iron']
                        df['f_manganese'] = 1 + 0.12 * df['manganese']
                        df['f_nitrite'] = 1 + 0.1 * df['nitrite']
                        df['f_h2s'] = 1 + 0.2 * df['hydrogen sulfide']
                        df['correction factor'] = df['f_ph'] * df['f_iron'] * df['f_manganese'] * df['f_nitrite'] * df['f_h2s']
                        df['final k_w'] = df['k_w_adjusted'] * df['correction factor']
                    else:
                        df['final k_w'] = df['k_w_adjusted']

                    df_result = df.drop(columns=['pipe diameter (m)', 'initial chlorine', 'ln_ratio', 'k_w_base', 'k_w_adjusted',
                                                 'f_ph', 'f_iron', 'f_manganese', 'f_nitrite', 'f_h2s', 'correction factor'], errors='ignore')
                    st.subheader("Wall Decay Results")
                    st.dataframe(df_result)
                    st.download_button("Download Wall Decay Results", df_result.to_csv(index=False), "wall_decay_results.csv", "text/csv")
                except Exception as e:
                    st.error(f"Error in Wall Decay: {e}")

            elif decay_mode == "Bulk Decay":
                try:
                    results = []
                    for _, row in df.iterrows():
                        t = contact_time(row['length (m)'], row['velocity m/s'])
                        k_b = base_decay(initial_chlorine, final_chlorine, t)
                        k_b_adj = adjust_bulk_decay(k_b, row['iron'], row['nitrite'], row['manganese'])
                        results.append({**row, "contact time (hrs)": t, "base decay coefficient (k_b)": k_b,
                                        "adjusted decay coefficient (k_b)": k_b_adj})
                    df_bulk = pd.DataFrame(results)
                    st.subheader("Bulk Decay Results")
                    st.dataframe(df_bulk)
                    st.download_button("Download Bulk Decay Results", df_bulk.to_csv(index=False), "bulk_decay_results.csv", "text/csv")
                except Exception as e:
                    st.error(f"Error in Bulk Decay: {e}")

# ------------------------------
# Mode 2: Manual Input
# ------------------------------
elif input_mode == "Manual Input":
    st.sidebar.markdown("### Enter General Parameters")
    decay_choice = st.sidebar.radio("Choose Decay Type", ["Wall Decay", "Bulk Decay"])

    # Reservoir Selection (button logic same as Upload Dataset)
    st.sidebar.markdown("### Reservoir Selection")
    selected_region_manual = None
    for region in reservoirs_by_region.keys():
        if st.sidebar.button(region):
            selected_region_manual = region

    # Show reservoirs on main page
    if selected_region_manual:
        st.subheader(f"Reservoirs in {selected_region_manual}")
        for reservoir in reservoirs_by_region[selected_region_manual]:
            st.write(f"- {reservoir}")

    st.markdown("## ✍️ Manual Entry Mode")
    st.markdown("Use the fields below to input values manually for decay calculation.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Pipe Parameters")
        c1, c2 = st.columns(2)
        with c1:
            length = st.number_input("Pipe Length (m)", min_value=0.0, step=1.0)
        with c2:
            diameter = st.number_input("Pipe Diameter (mm)", min_value=1.0, step=1.0)

        c11, c12 = st.columns(2)
        with c11:
            pipe_material = st.selectbox("Type of Pipe Material", ["AC", "PVC", "HDPE", "CI"])
        with c12:
            pipe_age = st.number_input("Age of Pipe (years)", min_value=1, step=1)

        c3, c4 = st.columns(2)
        with c3:
            velocity = st.number_input("Velocity (m/s)", min_value=0.01, step=0.01)
        with c4:
            final_chlorine_input = st.number_input("Final Chlorine (PPM)", min_value=0.0, value=0.96)

        st.markdown("### Water Chemistry")
        c5, c6 = st.columns(2)
        with c5:
            ph = st.number_input("pH", min_value=0.0, value=7.0)
        with c6:
            iron = st.number_input("Iron", min_value=0.0)

        temp_unit = st.selectbox("Select Temperature Unit", ["Celsius", "Fahrenheit"])
        if temp_unit == "Celsius":
            temperature = st.number_input("Temperature (°C)", min_value=-50.0, value=25.0)
        else:
            temperature = st.number_input("Temperature (°F)", min_value=-58.0, value=77.0)
        if temp_unit == "Fahrenheit":
            temperature_celsius = (temperature - 32) * 5.0 / 9.0
        else:
            temperature_celsius = temperature

        c7, c8 = st.columns(2)
        with c7:
            nitrite = st.number_input("Nitrite", min_value=0.0)
        with c8:
            manganese = st.number_input("Manganese", min_value=0.0)

        c9, c10 = st.columns(2)
        with c9:
            h2s = st.number_input("Hydrogen Sulfide", min_value=0.0)

        st.markdown("### Run Calculation")
        if decay_choice == "Wall Decay":
            if st.button("🔍 Calculate Wall Decay"):
                try:
                    diameter_m = diameter / 1000
                    t = contact_time(length, velocity)
                    ln_ratio = math.log(final_chlorine_input / initial_chlorine)
                    k_w_base = - (diameter_m / (4 * t)) * ln_ratio
                    k_w_adjusted = k_w_base * pipe_material_factor
                    final_k_w = apply_correction_factors(k_w_adjusted, ph, iron, nitrite, manganese, h2s)
                    st.success("✅ Wall Decay Coefficient Calculated:")
                    st.write(f"**Contact Time:** {t:.4f} hrs")
                    st.write(f"**Final k_w:** {final_k_w:.6f} per hr")
                except Exception as e:
                    st.error(f"Error in Wall Decay: {e}")

        elif decay_choice == "Bulk Decay":
            if st.button("🔍 Calculate Bulk Decay"):
                try:
                    t = contact_time(length, velocity)
                    k_b = base_decay(initial_chlorine, final_chlorine, t)
                    adjusted_k_b = adjust_bulk_decay(k_b, iron, nitrite, manganese)
                    st.success("✅ Bulk Decay Coefficient Calculated:")
                    st.write(f"**Contact Time:** {t:.4f} hrs")
                    st.write(f"**Adjusted k_b:** {adjusted_k_b:.6f} per hr")
                except Exception as e:
                    st.error(f"Error in Bulk Decay: {e}")
