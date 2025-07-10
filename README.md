# 🧠 NEETify: Dashboard Interaktif Analisis NEET Pemuda Indonesia

![Status](https://img.shields.io/badge/status-aktif-brightgreen)
![Dibangun dengan](https://img.shields.io/badge/dibangun_dengan-Streamlit-orange?logo=streamlit)
![Python](https://img.shields.io/badge/python-3.10+-blue)

> **NEETify** adalah dashboard interaktif berbasis data yang dirancang untuk menganalisis dan mensimulasikan faktor-faktor yang memengaruhi NEET (Not in Education, Employment, or Training) pada pemuda usia 15–24 tahun di Indonesia.  
> Proyek ini disusun sebagai kontribusi untuk **Essay Insight Competition – INTELECTRA 2025**, Himpro Pasca Statistika IPB University.

---

## 📌 Latar Belakang

Tingkat NEET pemuda Indonesia tahun 2024 mencapai **20,31%**, dengan ketimpangan tinggi antarprovinsi.  
Permasalahan NEET berdampak besar pada ketimpangan sosial, pengangguran muda, serta pencapaian SDGs (khususnya SDG 4 & 8).  
Melalui pemodelan regresi **Generalized Least Squares (GLS)** dan visualisasi interaktif, **NEETify** membantu perumusan kebijakan yang lebih tepat sasaran dan berbasis wilayah.

---

## 🧭 Fitur Utama

✅ **Peta Interaktif** — Menampilkan distribusi NEET antarprovinsi dari tahun 2016–2024  
✅ **Tren Time Series** — Lihat grafik tren NEET per provinsi  
✅ **Simulasi Prediksi NEET** — Uji skenario kebijakan berdasarkan model GLS tiap wilayah  
✅ **Responsif & Ringan** — Dibangun menggunakan Streamlit, dapat diakses via web & mobile

---

## 📊 Data & Variabel yang Digunakan

Proyek ini menggunakan **data panel 34 provinsi di Indonesia (2016–2024)** yang bersumber dari **Badan Pusat Statistik (BPS)**.  
Berikut adalah daftar variabel independen yang digunakan dalam model regresi:

| Kode  | Variabel                                                                      |
|-------|-------------------------------------------------------------------------------|
| NEET  | Persentase penduduk usia 15–24 tahun yang tidak sekolah, tidak bekerja, atau pelatihan |
| PPM   | Persentase Penduduk Miskin                                                    |
| TPT   | Tingkat Pengangguran Terbuka                                                  |
| GR    | Gini Ratio (ketimpangan distribusi pendapatan)                                |
| APS1  | Angka Partisipasi Sekolah (usia 16–18 tahun)                                  |
| APS2  | Angka Partisipasi Sekolah (usia 19–23 tahun)                                  |
| TIK   | Proporsi penduduk muda dengan keterampilan komputer                           |
| PDRB  | Produk Domestik Regional Bruto per kapita                                     |
| LAJU  | Laju pertumbuhan penduduk                                                     |
| KP    | Kepadatan penduduk                                                            |
| PL    | Rasio jenis kelamin                                                           |

---

## 📈 Hasil Utama Model GLS (Per Wilayah)

Model GLS dibangun secara **regional** untuk menangkap karakteristik lokal. Berikut ringkasan hasil signifikan:

| Wilayah         | Variabel Meningkatkan NEET                  | Variabel Menurunkan NEET            |
|-----------------|----------------------------------------------|--------------------------------------|
| **Sumatera**     | PPM (+), TPT (+), PDRB (+)                   | —                                    |
| **Jawa**         | PPM (+), TPT (+)                             | TIK (–)                              |
| **Kalimantan**   | TPT (+), APS2 (+)                            | APS1 (–)                             |
| **Sulawesi**     | TPT (+), APS2 (+)                            | TIK (–), APS1 (–)                    |
| **Indonesia Timur** | TPT (+), PDRB (+)                        | Kepadatan Penduduk / KP (–)         |

📌 Catatan:
- Simbol (+) berarti hubungan positif terhadap peningkatan NEET.
- Simbol (–) berarti berperan menurunkan NEET.
- Variabel yang tidak signifikan dihilangkan dari simulasi pada dashboard.

---

## 📁 Struktur Folder

```bash
neetify/
│
├── .devcontainer/          # Konfigurasi untuk container development (opsional)
├── data/                   # Dataset NEET & indikator sosial ekonomi (2016–2024)
├── neet_dashboard.py       # Aplikasi Streamlit utama
├── requirements.txt        # Daftar dependensi Python
└── README.md               # Dokumentasi proyek
