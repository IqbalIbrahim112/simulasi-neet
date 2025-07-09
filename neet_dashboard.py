import streamlit as st
import pandas as pd
import plotly.express as px
import json
import math

st.set_page_config(
    layout="wide",
    page_title="Dashboard NEET Rate Indonesia",
    page_icon="🇮🇩",
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .stHeading {
        font-size: 2.5em;
        color: #2e3b4e;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stSubheader {
        font-size: 1.8em;
        color: #4f8bf9;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 1.2em !important;
        color: #555555 !important;
    }
    .metric-value {
        font-size: 2.5em !important;
        font-weight: bold !important;
        color: #007bff !important;
    }
    .stSlider label, .stNumberInput label {
        font-weight: bold;
        color: #333333;
        font-size: 1.05em;
    }
    .non-significant-var {
        color: #888888;
        font-style: italic;
        margin-top: 1.5em;
        margin-bottom: 1.5em;
    }
    .conclusion-box {
        background-color: #f0f2f6;
        border-left: 6px solid #4CAF50;
        margin: 1.5em 0;
        padding: 1em 1.5em;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .conclusion-box p, .conclusion-box ul, .conclusion-box li {
        font-size: 1.0em;
        line-height: 1.6;
        color: #333333;
    }
    .conclusion-box strong {
        color: #007bff;
    }
    .conclusion-box ul {
        margin-left: 1em;
        padding-left: 0.5em;
    }

    .dynamic-conclusion-box {
        background-color: #e6f7ff;
        border-left: 6px solid #2196F3;
        margin: 1em 0;
        padding: 0.8em 1.2em;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .dynamic-conclusion-box p {
        font-size: 0.95em;
        line-height: 1.5;
        color: #333333;
    }
    .dynamic-conclusion-box strong {
        color: #1a73e8;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='stHeading'>📊 NEETify: Dashboard Interaktif NEET Rate Indonesia (2016–2024)</h1>", unsafe_allow_html=True)
st.markdown("---")

try:
    @st.cache_data
    def load_data(file_path):
        return pd.read_csv(file_path)

    neet = load_data("data/neet_data_34prov.csv")
    model = load_data("data/model_params_region.csv")

except FileNotFoundError:
    st.error("Error: File 'neet_data_34prov.csv' dan 'model_params_region.csv' tidak ditemukan. Pastikan file ada di folder 'data/' di direktori yang sama dengan aplikasi Anda.")
    st.stop()

neet['provinsi'] = neet['provinsi'].str.upper().str.strip().str.replace(" ", "")

mapping = {
    "DI.ACEH": "ACEH",
    "DAERAHISTIMEWAYOGYAKARTA": "YOGYAKARTA",
    "DKIJAKARTA": "JAKARTARAYA",
    "KEPULAUANBANGKABELITUNG": "BANGKABELITUNG"
}
neet['provinsi'] = neet['provinsi'].replace(mapping)

model.columns = model.columns.str.strip()

if "Region" in model.columns:
    model['Wilayah'] = model['Region'].str.upper().str.strip().str.replace(" ", "_")
    model = model.drop(columns=['Region'])
elif "Wilayah" in model.columns:
    model['Wilayah'] = model['Wilayah'].str.upper().str.strip().str.replace(" ", "_")


if "provinsi" in model.columns:
    model['provinsi'] = model['provinsi'].str.upper().str.strip().replace(" ", "")
    model['provinsi'] = model['provinsi'].replace(mapping)

region_map = {
    "SUMATERA": [
        "ACEH", "SUMATERAUTARA", "SUMATERABARAT", "RIAU", "KEPULAUANRIAU",
        "JAMBI", "SUMATERASELATAN", "BENGKULU", "LAMPUNG", "BANGKABELITUNG"
    ],
    "JAWA": [
        "JAKARTARAYA",
        "JAWABARAT", "JAWATENGAH", "YOGYAKARTA", "JAWATIMUR", "BANTEN"
    ],
    "KALIMANTAN": [
        "KALIMANTANBARAT", "KALIMANTANTENGAH", "KALIMANTANSELATAN",
        "KALIMANTANTIMUR", "KALIMANTANUTARA"
    ],
    "SULAWESI": [
        "SULAWESIUTARA", "GORONTALO", "SULAWESITENGAH", "SULAWESIBARAT",
        "SULAWESISELATAN",
        "SULAWESITENGGARA"
    ],
    "INDONESIA_TIMUR": [
        "BALI", "NUSATENGGARABARAT", "NUSATENGGARATIMUR",
        "MALUKU", "MALUKUUTARA", "PAPUA", "PAPUABARAT"
    ]
}

def assign_region(prov):
    for region, prov_list in region_map.items():
        if prov in prov_list:
            return region
    return None

neet["Wilayah"] = neet["provinsi"].apply(assign_region)


st.sidebar.header("⚙️ Kontrol Dashboard")

if neet.empty:
    st.sidebar.error("Data NEET kosong. Tidak dapat menampilkan kontrol.")
    st.stop()

st.sidebar.subheader("Pilih Tahun Peta:")
tahun = st.sidebar.slider(
    "Geser untuk memilih tahun",
    int(neet['tahun'].min()),
    int(neet['tahun'].max()),
    int(neet['tahun'].max()),
    key="tahun_slider"
)

data_now = neet[neet['tahun'] == tahun].copy()

if data_now.empty:
    st.warning(f"Tidak ada data untuk tahun {tahun}. Silakan pilih tahun lain.")


if tahun == neet['tahun'].min():
    data_now["perubahan"] = None
    data_now["tooltip"] = data_now.apply(
        lambda row: f"{row['provinsi']}<br>NEET: {row['neet_rate']:.2f}%", axis=1
    )
    data_now.rename(columns={"neet_rate": "neet_rate_now"}, inplace=True)
    data_merge = data_now
else:
    data_prev = neet[neet['tahun'] == tahun - 1].copy()
    data_prev.rename(columns={"neet_rate": "neet_rate_prev"}, inplace=True)
    data_now.rename(columns={"neet_rate": "neet_rate_now"}, inplace=True)
    data_merge = pd.merge(data_now, data_prev[["provinsi", "neet_rate_prev"]], on="provinsi", how="left")
    data_merge["perubahan"] = ((data_merge["neet_rate_now"] - data_merge["neet_rate_prev"]) / data_merge["neet_rate_prev"]) * 100

    def format_arrow(val):
        if pd.isna(val):
            return "-"
        return f"▲ {val:.2f}%" if val > 0 else f"▼ {abs(val):.2f}%"

    data_merge["tooltip"] = data_merge.apply(
        lambda row: f"{row['provinsi']}<br>NEET: {row['neet_rate_now']:.2f}%<br>Perubahan: {format_arrow(row['perubahan'])}",
        axis=1
    )

try:
    @st.cache_data
    def load_geojson(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    geojson = load_geojson("data/gadm41_IDN_1.json")
except FileNotFoundError:
    st.error("Error: File 'gadm41_IDN_1.json' tidak ditemukan. Pastikan file ada di folder 'data/' di direktori yang sama dengan aplikasi Anda.")
    st.stop()

for feature in geojson['features']:
    if 'NAME_1' in feature['properties']:
        normalized_name = feature['properties']['NAME_1'].upper().strip().replace(" ", "")
        for k, v in mapping.items():
            if normalized_name == k:
                normalized_name = v
                break
        feature['properties']['Propinsi'] = normalized_name

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h3 class='stSubheader'>🗺️ Peta NEET Rate Indonesia</h3>", unsafe_allow_html=True)
    if data_merge.empty:
        st.info("Pilih tahun yang memiliki data untuk menampilkan peta.")
    else:
        fig = px.choropleth(
            data_merge,
            geojson=geojson,
            locations="provinsi",
            featureidkey="properties.Propinsi",
            color="neet_rate_now",
            hover_name="provinsi",
            hover_data={"tooltip": True, "provinsi": False, "neet_rate_now": False},
            color_continuous_scale="YlOrRd",
            labels={'neet_rate_now': 'NEET Rate'},
            range_color=(data_merge['neet_rate_now'].min() * 0.9, data_merge['neet_rate_now'].max() * 1.1)
        )

        fig.update_traces(hovertemplate="%{customdata[0]}")
        fig.update_geos(fitbounds="locations", visible=False, showland=True, landcolor="white")
        fig.update_layout(
            title=f"NEET Rate per Provinsi - {tahun}",
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=0, r=0, t=40, b=0),
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<h3 class='stSubheader'>📈 Tren NEET Rate per Provinsi</h3>", unsafe_allow_html=True)
    prov_chart_options = sorted(neet["provinsi"].unique())
    if not prov_chart_options:
        st.info("Tidak ada data provinsi yang tersedia untuk menampilkan tren.")
    else:
        display_chart_options = [p.replace('RAYA', ' Raya').title() for p in prov_chart_options]
        prov_chart_display = st.selectbox("Pilih Provinsi untuk Melihat Tren", display_chart_options, key="trend_province_selector")
        prov_chart = prov_chart_display.upper().replace(' ', '') if prov_chart_display else None

        if prov_chart:
            data_tren = neet[neet["provinsi"] == prov_chart]
            if not data_tren.empty:
                fig_line = px.line(
                    data_tren,
                    x="tahun",
                    y="neet_rate",
                    markers=True,
                    title=f"Tren NEET di {prov_chart_display}",
                    labels={"neet_rate": "NEET Rate", "tahun": "Tahun"},
                    height=350
                )
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info(f"Data tren untuk provinsi '{prov_chart_display}' tidak ditemukan. Mungkin data tidak lengkap.")

st.divider()

st.markdown("<h3 class='stSubheader'>🧮 Simulasi Prediksi NEET Rate Berdasarkan Wilayah</h3>", unsafe_allow_html=True)

all_potential_vars = ['PPM', 'TPT', 'GR', 'APS1', 'APS2', 'TIK', 'PDRB', 'LAJU', 'KP', 'PL']
required_p_value_cols = [f"p_{var}" for var in all_potential_vars]

var_descriptions = {
    "PPM": "Persentase Penduduk Miskin",
    "TPT": "Tingkat Pengangguran Terbuka",
    "GR": "Gini Ratio (indikator ketimpangan pendapatan)",
    "APS1": "Angka Partisipasi Sekolah (16-18 tahun)",
    "APS2": "Angka Partisipasi Sekolah (19-23 tahun)",
    "TIK": "Keterampilan Teknologi Informasi dan Komputer (misal: persentase pengguna internet)",
    "PDRB": "Produk Domestik Regional Bruto (per kapita)",
    "RLS": "Rata-Rata Lama Sekolah",
    "KP": "Kepadatan Penduduk",
    "PL": "Proporsi Laki-laki dan Perempuan",
    "LAJU": "Laju Pertumbuhan Penduduk",
}


missing_model_cols = [col for col in ["Wilayah", "intercept"] + all_potential_vars + required_p_value_cols if col not in model.columns]

if missing_model_cols:
    st.error("❗ File 'model_params_region.csv' tidak memiliki semua kolom yang diperlukan untuk simulasi.")
    st.info(f"Kolom yang hilang: {', '.join(missing_model_cols)}. Pastikan file model Anda berisi kolom 'Wilayah', 'intercept', semua nama variabel, dan p-value yang sesuai (e.g., p_PPM, p_TPT, dll).")
else:
    region_options = sorted(model["Wilayah"].dropna().unique())
    if not region_options:
        st.info("Tidak ada data wilayah yang tersedia dalam model untuk simulasi.")
    else:
        st.sidebar.subheader("Simulasi Prediksi NEET:")
        region_pilih = st.sidebar.selectbox("Pilih Wilayah untuk Simulasi", region_options, key="sim_region_selector")

        if region_pilih is None:
            st.info("Pilih Wilayah terlebih dahulu di sidebar untuk menjalankan simulasi.")
        else:
            model_region = model[model["Wilayah"] == region_pilih]

            if model_region.empty:
                st.warning(f"Model untuk wilayah '{region_pilih}' belum tersedia. Pilih wilayah lain.")
            else:
                param_region = model_region.iloc[0]

                model_actual_vars = []
                for var in all_potential_vars:
                    if pd.notna(param_region.get(var)):
                        model_actual_vars.append(var)

                variabel_signifikan = set()
                variabel_tidak_signifikan_names = []
                significance_threshold = 0.1
                
                for var in model_actual_vars:
                    p_value_col = f"p_{var}"
                    if pd.notna(param_region.get(p_value_col)) and param_region[p_value_col] < significance_threshold:
                        variabel_signifikan.add(var)
                    else:
                        variabel_tidak_signifikan_names.append(var)

                st.markdown(f"**Rumus Regresi untuk Wilayah {region_pilih.title().replace('_', ' ')}:**")
                rumus = f"\\text{{NEET}} = {param_region['intercept']:.2f}"
                for var in model_actual_vars:
                    coef = param_region.get(var)
                    rumus += f" + ({coef:.4f} \\times \\text{{{var}}})"
                st.latex(rumus)

                if variabel_tidak_signifikan_names:
                    bolded_non_significant_vars = [f"**{v}** ({var_descriptions.get(v, v)})" for v in variabel_tidak_signifikan_names]
                    st.info(f"Catatan: Variabel berikut tidak signifikan ($p \\ge {significance_threshold}$) dan **inputnya tidak dapat diubah**, namun **tetap memengaruhi prediksi NEET** dengan koefisien aslinya: {', '.join(bolded_non_significant_vars)}.")

                st.sidebar.markdown("---")
                st.sidebar.subheader(f"Variabel Input untuk {region_pilih.title().replace('_', ' ')}:")

                provinsi_opsi = sorted(neet[neet["Wilayah"] == region_pilih]["provinsi"].unique())

                if not provinsi_opsi:
                    st.warning(f"Tidak ada provinsi yang ditemukan dalam data untuk wilayah '{region_pilih}' untuk simulasi. Pastikan pemetaan wilayah sudah benar.")
                    prov_pilih = None
                else:
                    display_prov_options = [p.replace('RAYA', ' Raya').title() for p in provinsi_opsi]
                    
                    prov_pilih_display = None
                    if 'sim_province_selector' in st.session_state and st.session_state['sim_province_selector'] in display_prov_options:
                        prov_pilih_display = st.session_state['sim_province_selector']
                    elif display_prov_options:
                        prov_pilih_display = display_prov_options[0]

                    default_index = 0
                    if prov_pilih_display in display_prov_options:
                        default_index = display_prov_options.index(prov_pilih_display)

                    prov_pilih_display = st.sidebar.selectbox(
                        "Pilih Provinsi dalam Wilayah",
                        display_prov_options,
                        index=default_index,
                        key="sim_province_selector"
                    )

                    prov_pilih = prov_pilih_display.upper().replace(' ', '') if prov_pilih_display else None


                if prov_pilih is None:
                    st.sidebar.info("Pilih Provinsi di sidebar terlebih dahulu.")
                else:
                    data_input = neet[(neet["provinsi"] == prov_pilih) & (neet["tahun"] == neet["tahun"].max())]
                    default_vals = data_input.iloc[0] if not data_input.empty else {}

                    inputs = {}
                    st.markdown(f"**Input Variabel untuk {prov_pilih_display}:**")
                    cols_input = st.columns(3)
                    input_idx = 0

                    for var in model_actual_vars:
                        col_to_use = cols_input[input_idx % 3]
                        input_idx += 1

                        default_val = default_vals.get(var)
                        if pd.isna(default_val):
                            if var in ['PPM', 'TPT', 'APS1', 'APS2', 'TIK', 'LAJU']:
                                default_val = 50.0
                            elif var == 'GR':
                                default_val = 0.4
                            elif var == 'PDRB':
                                default_val = 100000.0
                            elif var in ['KP', 'PL']:
                                default_val = 100.0
                            else:
                                default_val = 10.0

                        input_key = f"{var}_{region_pilih}_{prov_pilih}_sim"
                        
                        is_disabled = var not in variabel_signifikan

                        with col_to_use:
                            display_label = var_descriptions.get(var, var)
                            
                            if var in ['PPM', 'TPT', 'APS1', 'APS2', 'TIK', 'LAJU']:
                                inputs[var] = st.slider(display_label, 0.0, 100.0, float(default_val), key=input_key, format="%.2f", disabled=is_disabled)
                            elif var == 'GR':
                                inputs[var] = st.slider(display_label, 0.0, 1.0, float(default_val), key=input_key, format="%.3f", disabled=is_disabled)
                            elif var == 'PDRB':
                                inputs[var] = st.number_input(display_label, min_value=0.0, max_value=1_000_000_000_000.0, value=float(default_val), key=input_key, format="%.2f", disabled=is_disabled)
                            elif var == 'KP':
                                min_kp = neet['KP'].min() if not neet.empty else 0
                                max_kp = neet['KP'].max() if not neet.empty else 120
                                inputs[var] = st.number_input(display_label, min_value=float(min_kp), max_value=float(max_kp), value=float(default_val), key=input_key, format="%.2f", disabled=is_disabled)
                            elif var == 'PL':
                                min_pl = neet['PL'].min() if not neet.empty else 0.0
                                max_pl = neet['PL'].max() if not neet.empty else 150.0
                                inputs[var] = st.number_input(display_label, min_value=float(min_pl), max_value=float(max_pl), value=float(default_val), key=input_key, format="%.2f", disabled=is_disabled)
                            else:
                                inputs[var] = st.number_input(display_label, value=float(default_val), key=input_key, format="%.2f", disabled=is_disabled)


                    prediksi_neet = param_region['intercept']
                    for var in model_actual_vars:
                        coef_to_use = param_region.get(var)
                        if pd.isna(coef_to_use):
                            coef_to_use = 0.0

                        input_value = inputs.get(var, 0.0)
                        if pd.isna(input_value):
                            input_value = 0.0

                        prediksi_neet += coef_to_use * input_value

                    st.markdown("---")
                    current_prediction_value = f"{prediksi_neet:.2f}%"

                    st.metric(
                        label=f"🎯 Prediksi NEET Rate untuk {prov_pilih_display} (Wilayah {region_pilih.title().replace('_', ' ')})",
                        value=current_prediction_value,
                        help=f"Prediksi berdasarkan model regresi regional. Variabel dengan p-value kurang dari {significance_threshold} dianggap signifikan dan memengaruhi hasil. Variabel yang tidak signifikan atau tidak relevan memiliki input yang dinonaktifkan tetapi tetap memengaruhi prediksi dengan koefisien aslinya."
                    )
                    st.success("Prediksi berhasil dihitung! Sesuaikan input variabel di atas untuk melihat perubahan.")

                    if 'previous_inputs' not in st.session_state:
                        st.session_state['previous_inputs'] = {}
                        st.session_state['previous_prediction'] = None
                        st.session_state['initial_run'] = True
                    else:
                        st.session_state['initial_run'] = False

                    current_prediction_str = f"{prediksi_neet:.2f}%"
                    current_inputs = inputs.copy()

                    if not st.session_state['initial_run']:
                        old_prediction = st.session_state.get('previous_prediction')
                        old_inputs = st.session_state.get('previous_inputs', {})

                        try:
                            old_prediction_float = float(str(old_prediction).replace('%',''))
                        except (ValueError, TypeError):
                            old_prediction_float = None

                        changed_vars_info = []
                        if old_prediction_float is not None and not math.isnan(old_prediction_float):
                            delta_neet_rate = prediksi_neet - old_prediction_float

                            for var in model_actual_vars:
                                if var in variabel_signifikan:
                                    old_val = old_inputs.get(var)
                                    new_val = current_inputs.get(var)

                                    if old_val is not None and new_val is not None and abs(old_val - new_val) > 1e-6:
                                        change_amount = new_val - old_val
                                        change_type = "peningkatan" if change_amount > 0 else "penurunan"
                                        
                                        desc = var_descriptions.get(var, var)
                                        changed_vars_info.append(
                                            f"<strong>{var}</strong> ({desc}) dari {old_val:.2f} menjadi {new_val:.2f} (terjadi {change_type} {abs(change_amount):.2f} unit)."
                                        )
                            
                            if changed_vars_info:
                                st.markdown("<div class='dynamic-conclusion-box'>", unsafe_allow_html=True)
                                st.markdown("<h5>✨ Dampak Perubahan Input Anda:</h5>", unsafe_allow_html=True)
                                st.markdown(f"<p>Anda telah melakukan perubahan pada:<br><ul>{''.join([f'<li>{info}</li>' for info in changed_vars_info])}</ul></p>", unsafe_allow_html=True)
                                
                                overall_dampak_word = "meningkat" if delta_neet_rate > 0 else "menurun"
                                if abs(delta_neet_rate) < 0.01:
                                    st.markdown(f"<p>Prediksi NEET rate <strong>tetap tidak berubah secara signifikan</strong>.</p>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<p>Secara keseluruhan, prediksi NEET rate <strong>{overall_dampak_word}</strong> sebesar <strong>{abs(delta_neet_rate):.2f}%</strong> dari {old_prediction_float:.2f}% menjadi {prediksi_neet:.2f}%.</p>", unsafe_allow_html=True)
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                            elif not st.session_state['initial_run'] and (old_prediction_float is None or math.isnan(old_prediction_float)):
                                st.info("Prediksi sebelumnya tidak valid untuk perbandingan perubahan. Silakan interaksi lebih lanjut.")
                            elif not st.session_state['initial_run']:
                                st.info("Tidak ada perubahan yang signifikan pada input yang dapat diubah saat ini.")

                    st.session_state['previous_inputs'] = current_inputs
                    st.session_state['previous_prediction'] = current_prediction_str


st.divider()
st.markdown("<h3 class='stSubheader'>📝 Kesimpulan Model Wilayah</h3>", unsafe_allow_html=True)

with st.expander("Klik untuk melihat Ringkasan Model Regresi", expanded=True):
    if 'region_pilih' not in locals() or region_pilih is None:
        st.info("Pilih Wilayah di sidebar untuk melihat kesimpulan modelnya.")
    elif model_region.empty:
        st.info(f"Model untuk wilayah '{region_pilih.title().replace('_', ' ')}' belum tersedia, sehingga kesimpulan tidak dapat dibuat.")
    else:
        param_region_conclusion = model_region.iloc[0]
        
        signifikan_conclusion = []
        tidak_signifikan_dihitung_conclusion = []
        tidak_relevan_diabaikan_conclusion = []

        significance_threshold_conclusion = 0.1

        for var in all_potential_vars:
            coef_val = param_region_conclusion.get(var)
            p_val = param_region_conclusion.get(f"p_{var}")

            if pd.isna(coef_val):
                tidak_relevan_diabaikan_conclusion.append(var)
            elif pd.notna(p_val) and p_val < significance_threshold_conclusion:
                signifikan_conclusion.append(var)
            else:
                tidak_signifikan_dihitung_conclusion.append(var)
        
        region_nama_bersih = region_pilih.title().replace('_', ' ')
        kesimpulan_text = f"<p>Analisis ini didasarkan pada model regresi linear spesifik untuk <strong>Wilayah {region_nama_bersih}</strong>.</p>"

        intercept_val = param_region_conclusion['intercept']
        kesimpulan_text += f"<p>Intersep model sebesar <strong>{intercept_val:.2f}%</strong>, menunjukkan bahwa tingkat NEET dasar di wilayah ini adalah sekitar {intercept_val:.2f}% ketika seluruh variabel prediktor bernilai nol (atau pada tingkat rata-rata data).</p>"

        if signifikan_conclusion:
            kesimpulan_text += "<p><u>Variabel signifikan (p &lt; 0.1):</u></p><ul>"
            for var in sorted(signifikan_conclusion):
                coef = param_region_conclusion.get(var)
                p_value = param_region_conclusion.get(f"p_{var}")
                dampak_word = "menurunkan" if coef < 0 else "meningkatkan"
                desc = var_descriptions.get(var, var)
                kesimpulan_text += f"<li><strong>{var}</strong> ({desc}): Koefisien {coef:.4f}, p-value {p_value:.4f}. Ini berarti peningkatan satu unit pada {var} cenderung {dampak_word} NEET rate sebesar {abs(coef):.4f}%. Variabel ini menunjukkan hubungan yang kuat dan konsisten secara statistik.</li>"
            kesimpulan_text += "</ul>"
        else:
            kesimpulan_text += "<p>Tidak ada variabel yang secara statistik signifikan ($p < 0.1$) ditemukan memengaruhi NEET rate di wilayah ini berdasarkan model yang digunakan. Ini berarti hubungan yang teramati tidak cukup kuat untuk dianggap bukan kebetulan.</p>"

        if tidak_signifikan_dihitung_conclusion:
            kesimpulan_text += "<p><u>Variabel tidak signifikan tetapi tetap dihitung dalam model:</u></p><ul>"
            for var in sorted(tidak_signifikan_dihitung_conclusion):
                coef = param_region_conclusion.get(var)
                p_value = param_region_conclusion.get(f"p_{var}")
                p_info = f"p-value: {p_value:.4f}" if pd.notna(p_value) else "p-value tidak tersedia"
                desc = var_descriptions.get(var, var)
                kesimpulan_text += f"<li><strong>{var}</strong> ({desc}): Koefisien {coef:.4f}, {p_info}. Hubungan antara {var} dengan NEET rate tidak menunjukkan bukti statistik yang kuat untuk dianggap signifikan.</li>"
            kesimpulan_text += "</ul>Variabel-variabel ini mungkin memiliki pengaruh, namun belum dapat dikonfirmasi secara konsisten oleh model.<br>"

        if tidak_relevan_diabaikan_conclusion:
            bolded_irrelevant_vars = [f"<strong>{v}</strong> ({var_descriptions.get(v, v)})" for v in sorted(tidak_relevan_diabaikan_conclusion)]
            kesimpulan_text += f"<p><u>Variabel yang tidak digunakan dalam model ini:</u> {', '.join(bolded_irrelevant_vars)}.<br>Koefisien tidak tersedia, sehingga variabel ini tidak memengaruhi prediksi NEET rate untuk wilayah ini.</p>"
        
        st.markdown(f"<div class='conclusion-box'>{kesimpulan_text}</div>", unsafe_allow_html=True)


st.info("✨ Dashboard ini dibuat dengan Streamlit dan data publik.")
