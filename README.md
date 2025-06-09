# Telegram Ads Bot

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)

Skrip otomatis untuk mengirimkan pesan iklan atau promosi secara massal ke daftar grup atau channel Telegram Anda. Proyek ini dibuat untuk tujuan edukasi dan otomatisasi tugas-tugas pemasaran.

## ✨ Fitur Utama

-   **Pengiriman Massal**: Mengirimkan satu pesan ke banyak grup/channel sekaligus.
-   **Kustomisasi Pesan**: Mudah mengubah isi pesan iklan melalui file teks terpisah.
-   **Dukungan Media**: Mampu mengirimkan pesan teks bersama dengan gambar atau video.
-   **Manajemen Target**: Daftar target grup/channel dikelola dalam file terpisah agar mudah diubah.
--   **Jeda Otomatis**: Dilengkapi jeda (delay) antar pengiriman pesan untuk mengurangi risiko pembatasan akun oleh Telegram.

## ⚙️ Prasyarat

Sebelum memulai, pastikan Anda memiliki:

1.  **Python 3.7** atau versi yang lebih baru.
2.  **Akun Telegram**.
3.  **API ID** dan **API Hash** dari Telegram. Anda bisa mendapatkannya di [my.telegram.org](https://my.telegram.org).
    -   Login dengan nomor telepon Anda.
    -   Pilih "API development tools".
    -   Buat aplikasi baru (isi nama dan short name secara acak).
    -   Salin `api_id` dan `api_hash` yang muncul.

## 🚀 Instalasi

Ikuti langkah-langkah berikut untuk menjalankan skrip ini di komputer Anda.

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/setiaone-tech/Telegram_Ads.git](https://github.com/setiaone-tech/Telegram_Ads.git)
    ```

2.  **Masuk ke direktori proyek:**
    ```bash
    cd Telegram_Ads
    ```

3.  **Install semua dependensi yang dibutuhkan:**
    (Asumsi menggunakan library Telethon)
    ```bash
    pip install -r requirements.txt
    ```
    *Jika file `requirements.txt` tidak ada, install Telethon secara manual:*
    ```bash
    pip install telethon
    ```

## 📝 Konfigurasi

Sebelum menjalankan bot, Anda perlu melakukan beberapa konfigurasi:

1.  **Masukkan Kredensial API**
    Buka file utama (misalnya `main.py` atau `app.py`) dan cari bagian konfigurasi. Masukkan `API_ID` dan `API_HASH` yang sudah Anda dapatkan.

    ```python
    # Contoh di dalam file .py
    API_ID = 12345678
    API_HASH = 'abcdefghijklmnopqrstuvwxyz123456'
    SESSION_NAME = 'my_session'
    ```

2.  **Siapkan Pesan Iklan**
    -   Buka file `iklan.txt`.
    -   Tulis atau salin pesan iklan yang ingin Anda kirimkan ke dalam file ini.
    -   Jika Anda ingin mengirimkan gambar, pastikan nama file gambar (misal: `gambar.jpg`) sudah sesuai dengan yang ada di dalam skrip. Letakkan gambar di direktori yang sama dengan skrip.

3.  **Siapkan Daftar Target**
    -   Buka file `groups.txt`.
    -   Masukkan daftar username atau ID grup/channel yang menjadi target Anda, satu per baris.
    -   **Contoh isi `groups.txt`:**
        ```txt
        t.me/grupdiskusi_python
        t.me/belajar_desain_grafis
        -1001234567890 
        ```
    > **Catatan:** Untuk grup/channel publik, gunakan format `t.me/username`. Untuk grup/channel private, Anda perlu mendapatkan ID-nya (biasanya berupa angka negatif panjang) menggunakan bot lain seperti `@userinfobot`.

## ▶️ Cara Menjalankan

1.  **Sesi Pertama Kali:** Saat pertama kali menjalankan skrip, Telegram akan meminta Anda untuk login.
    ```bash
    python main.py
    ```
    -   Masukkan nomor telepon Anda.
    -   Masukkan kode verifikasi yang dikirimkan ke akun Telegram Anda.
    -   Jika Anda mengaktifkan 2FA (Two-Factor Authentication), masukkan juga password Anda.
    -   Setelah berhasil, sebuah file `my_session.session` akan dibuat. File ini berfungsi agar Anda tidak perlu login berulang kali.

2.  **Menjalankan Iklan:**
    Setelah file sesi dibuat, jalankan kembali skrip yang sama untuk mulai mengirimkan pesan.
    ```bash
    python main.py
    ```
    Bot akan membaca pesan dari `iklan.txt` dan mengirimkannya satu per satu ke target di `groups.txt`.

## ⚠️ Peringatan Penting

-   **Risiko Banned**: Penggunaan skrip otomasi untuk mengirim pesan massal melanggar Ketentuan Layanan Telegram dan dapat menyebabkan akun Anda dibatasi (mute) atau bahkan diblokir secara permanen.
-   **Gunakan Akun Kedua**: Sangat disarankan untuk menggunakan akun Telegram cadangan (bukan akun utama) untuk menjalankan skrip ini.
-   **Gunakan Dengan Bijak**: Jangan melakukan spam. Atur jeda waktu yang wajar antar pesan untuk menghormati pengguna lain dan mengurangi risiko. **Risiko ditanggung oleh pengguna.**

## 🤝 Kontribusi

Merasa ada yang bisa ditingkatkan? Silakan buat *Pull Request* atau buka *Issue*. Kontribusi dalam bentuk apapun sangat kami hargai!

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).
