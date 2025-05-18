# Sentiment Analysis dengan Support Vector Machine (SVM)

Nama : Gevira Zahra Shofa

NIM :1227050050 

Kelas : Praktikum Pembelajaran Mesin E

## Tujuan

Menerapkan algoritma SVM untuk mengklasifikasikan sentimen (positif atau negatif) dari data ulasan teks.

## Langkah-langkah
+ Persiapan dan Preprocessing Data
  + Dataset dibaca dari file training.txt yang berisi dua kolom: label (liked) dan teks ulasan (text).
  + Dilakukan tokenisasi dan lemmatization menggunakan TextBlob.
  + Stopwords dan normalisasi kata diolah untuk persiapan vektorisasi.
+ Feature Extraction
  + Data teks diubah ke bentuk numerik menggunakan:
    + CountVectorizer: menghitung frekuensi kata.
    + TF-IDF Transformer: menghitung bobot kata berdasarkan frekuensi dan signifikansi.
+ Pembagian Data
  + Data dibagi menjadi training (80%) dan testing (20%) menggunakan train_test_split.
+ Modeling dengan SVM
  + Pipeline SVM dibuat dengan:
    + CountVectorizer → TF-IDF → SVC (Support Vector Classifier)
  + GridSearchCV digunakan untuk menemukan parameter terbaik (C, kernel, gamma) dengan 5-fold cross-validation.
+ Evaluasi
  + Evaluasi dilakukan menggunakan:
    + Classification Report (precision, recall, f1-score)
    + Akurasi Prediksi
  + Contoh prediksi:
    + "the vinci code is awesome" → positif
    + "the vinci code is bad" → negatif

## Hasil
+ Model berhasil melakukan klasifikasi sentimen dengan akurasi yang cukup baik (detail akurasi dan metrik bisa dilihat di output classification_report).
+ Hyperparameter terbaik ditemukan dengan kombinasi kernel = linear/rbf dan C/gamma tertentu melalui GridSearchCV.

## 📂 Struktur File
+ sentimen_analisis_svm.py – berisi seluruh proses dari preprocessing hingga evaluasi model.
+ sentimen_analisis_svm.ipynb – berisi seluruh proses dari preprocessing hingga evaluasi model.
+ Dataset: training.txt 
