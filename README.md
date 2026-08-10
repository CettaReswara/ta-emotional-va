# ta-emotional-va
Tugas akhir Cetta Reswara Parahita (13521133). Laman penjelasan singkat dapat dilihat melalui https://digilib.itb.ac.id/gdl/view_data/pengembangan-model-prediksi-intensitas-dan-perubahan-valence-arousal-dari-dataset-teks-ecological-momentary-assessment-13521133.

## Struktur Repo

```
.
├── app.py                   # Entry point aplikasi demo
├── config.py                # Konfigurasi global aplikasi demo
├── data.py                  # Data aplikasi demo
├── state.py                 # State management aplikasi demo
├── ui.py                    # Komponen UI plikasi demo
├── inference/               # Pipeline inference untuk aplikasi demo
│   ├── model_loader.py        # Load model RoBERTa/DeBERTa terlatih
│   └── predictor.py           # Fungsi prediksi valence-arousal
├── pages_ui/                # Halaman aplikasi demo
│   ├── diary.py               # Halaman input mood diary
│   ├── detail.py              # Halaman detail entry
│   └── insight.py             # Halaman insight dan analisis
├── viz/                     # Visualisasi aplikasi demo
│   ├── circumplex.py          # Plot circumplex model
│   └── trajectory.py          # Plot trajectory emosi sepanjang waktu
├── notebook/                 # Notebook final model untuk tiap subtask
│   ├── subtask1.ipynb          # Prediksi valence-arousal dari teks
│   ├── subtask2a.ipynb         # Forecasting state-change valence-arousal
│   └── subtask2b.ipynb         # Forecasting dispositional-change valence-arousal
├── data/                     # Dataset training model
├── assets/                   # Model checkpoint terlatih. Untuk melalui `bit.ly/AssetsDemoTA13521133`
└── requirements.txt
```

## Setup

Aplikasi ini dijalankan menggunakan conda environment `ta`.

```bash
conda activate ta
pip install -r requirements.txt
```

Apabila environment `ta` belum tersedia, mohon persiapkan terlebih dahulu sebagai berikut:

```bash
conda create -n ta python=3.11
conda activate ta
pip install -r requirements.txt
```

## Dataset

Dataset yang dipakai berasal dari SemEval 2026 Task 2 dan tunduk pada ketentuan redistribusi resmi task tersebut.

Struktur folder `data/` mengikuti pembagian berikut:

```
data/
├── train_df/      # Data training tiap subtask
├── test_df/       # Data test tiap subtask
└── final_label/   # Label final untuk evaluasi
```

## Model Checkpoint

Checkpoint perlu diletakkan pada folder `assets/` untuk keperluan aplikasi demo. Checkpoint lengkap seluruh ensemble (seed 42, 123, 456 untuk masing masing RoBERTa dan DeBERTa) tersedia terpisah silakan hubungi penulis. Checkpoint minimal dapat diakses melalui link berikut untuk penggunaan terbatas pada aplikasi demo `bit.ly/AssetsDemoTA13521133`

## Menjalankan Notebook

Notebook di folder `notebook/` merepresentasikan hasil final eksperimen. Jalankan berurutan:

1. `subtask1.ipynb`: training dan evaluasi RoBERTa/DeBERTa
2. `subtask2a.ipynb`: forecasting state-change
3. `subtask2b.ipynb`: forecasting dispositional-change

**Rekomendasi runtime:** gunakan Colab Pro dengan GPU T4 untuk training. Ini mempercepat training RoBERTa/DeBERTa secara signifikan dibanding runtime gratis, dan lebih stabil untuk sesi training yang panjang.

Cara pilih runtime di Colab: `Runtime > Change runtime type > T4 GPU`

## Menjalankan Aplikasi Demo

```bash
conda activate ta
streamlit run app.py
```

Aplikasi ini merupakan demo interaktif dari pipeline yang dikembangkan, memungkinkan input entry mood baru, prediksi valence arousal secara live menggunakan model ensemble, dan visualisasi trajectory emosi melalui circumplex model.

## Referensi

Task: SemEval 2026 Task 2 (https://semeval2026task2.github.io/SemEval-2026-Task2/overview; https://aclanthology.org/2026.semeval-1.451/)
Penjelasan sistem: https://aclanthology.org/2026.semeval-1.348/
