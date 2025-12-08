### TAHAP 1: Setup Database di Supabase

Sebelum mengutak-atik kode, kita siapkan dulu "rumah" untuk datanya.

1.  Buka [Supabase.com](https://supabase.com/) dan **Sign In** (bisa pakai GitHub).
2.  Klik **New Project**.
3.  Isi **Name** (misal: `mirai-db`) dan buat **Database Password** (PENTING: Simpan password ini, jangan sampai lupa\!).
4.  Pilih **Region** yang dekat (misal: Singapore).
5.  Klik **Create New Project** dan tunggu beberapa menit sampai setup selesai.
6.  Setelah selesai, masuk ke menu **Project Settings** (ikon gerigi di kiri bawah) -\> **Database**.
7.  Cari bagian **Connection String**.
8.  Klik tab **URI**.
9.  Copy string tersebut. Bentuknya akan seperti ini:
    `postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres`
    *(Nanti kita akan pakai ini di Render).*

-----

### TAHAP 2: Persiapan Kode Django (Localhost)

Kita perlu menginstal beberapa *library* agar Django bisa berjalan di production (Render) dan membaca database Supabase.

**1. Install Library Tambahan**
Buka terminal di folder proyek `mirAI` kamu, lalu jalankan:

```bash
pip install gunicorn psycopg2-binary dj-database-url whitenoise
```

  * `gunicorn`: Server untuk production (pengganti `runserver`).
  * `psycopg2-binary`: Driver agar Python bisa ngobrol sama PostgreSQL.
  * `dj-database-url`: Helper untuk membaca konfigurasi database dari URL Supabase.
  * `whitenoise`: Agar Render bisa menampilkan file statis (CSS/JS/Gambar) dengan benar.

**2. Update `settings.py`**
Buka file `settings.py` kamu dan lakukan perubahan berikut:

**A. Import di paling atas:**

```python
import os
import dj_database_url
```

**B. Allowed Hosts:**

```python
# Izinkan semua host (untuk render)
ALLOWED_HOSTS = ['*'] 
```

**C. Middleware (Untuk Whitenoise):**
Cari `MIDDLEWARE` dan tambahkan `whitenoise` **setelah** `SecurityMiddleware`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # TAMBAHKAN INI
    # ... middleware lainnya ...
]
```

**D. Konfigurasi Database:**
Ubah bagian `DATABASES` menjadi seperti ini. Ini artinya: "Kalau ada setting database di Render, pakai itu. Kalau tidak ada (di laptop), pakai SQLite bawaan".

```python
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}
```

**E. Static Files (PENTING):**
Tambahkan konfigurasi ini di bagian paling bawah `settings.py` agar CSS tidak *broken*:

```python
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**3. Buat file `requirements.txt` baru**
Simpan daftar library yang baru diinstall tadi:

```bash
pip freeze > requirements.txt
```

**4. Buat Script `build.sh`**
Buat file baru bernama `build.sh` di root folder (sejajar dengan `manage.py`). File ini memerintahkan Render apa yang harus dilakukan saat deploy.

Isi file `build.sh`:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Kumpulkan file static (css/js)
python manage.py collectstatic --no-input

# Jalankan migrasi database (membuat tabel di Supabase)
python manage.py migrate
```

**5. Push ke GitHub**
Simpan semua perubahan, commit, dan push ke repo GitHub kamu.

-----

### TAHAP 3: Migrasi Data (Opsional tapi Direkomendasikan)

Jika kamu ingin **memindahkan data film/user** yang sudah ada di laptop (SQLite/Postgres Lokal) ke Supabase, cara termudah bagi pemula Django adalah menggunakan `dumpdata` dan `loaddata`.

1.  **Di Laptop (Dump Data):**
    Jalankan perintah ini untuk mengambil semua isi database lokalmu menjadi file JSON:

    ```bash
    python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json
    ```

2.  **Commit file `data.json`** ini ke GitHub agar ikut ter-upload ke Render (atau nanti bisa dijalankan manual via koneksi remote, tapi upload paling gampang).

-----

### TAHAP 4: Deploy ke Render

1.  Buka [Render.com](https://render.com) dan Login.

2.  Klik **New +** dan pilih **Web Service**.

3.  Pilih opsi **Build and deploy from a Git repository**.

4.  Cari repo `mirAI-django` kamu dan klik **Connect**.

5.  Isi konfigurasi berikut:

      * **Name:** `mirai-app` (atau terserah).
      * **Region:** Singapore (biar dekat).
      * **Branch:** `main` (atau `master`).
      * **Runtime:** Python 3.
      * **Build Command:** `./build.sh`
      * **Start Command:** `gunicorn nama_folder_project_kamu.wsgi:application`
        *(Ganti `nama_folder_project_kamu` dengan nama folder yang di dalamnya ada file `settings.py`. Biasanya sama dengan nama repo atau nama project django, misal `mirAI.wsgi:application`)*.
      * **Instance Type:** Free.

6.  **Environment Variables (PENTING SEKALI)**
    Scroll ke bawah ke bagian "Environment Variables", klik **Add Environment Variable**:

      * **Key:** `DATABASE_URL`
        **Value:** Paste URI dari Supabase tadi. **JANGAN LUPA** ganti `[YOUR-PASSWORD]` dengan password database yang kamu buat di Tahap 1.
      * **Key:** `SECRET_KEY`
        **Value:** Isi dengan string acak yang panjang (bisa copy dari `settings.py` tapi sebaiknya diganti biar aman).
      * **Key:** `PYTHON_VERSION`
        **Value:** `3.9.0` (atau sesuaikan dengan versi python di laptopmu, misal `3.10.0`).

7.  Klik **Create Web Service**.

-----

### TAHAP 5: Memasukkan Data Lama (Load Data)

Render akan mulai proses deploy. Ia akan menjalankan `build.sh` yang otomatis melakukan `migrate` (membuat tabel kosong di Supabase).

Jika deploy sudah **Success** (warna hijau), website kamu sudah live tapi databasenya masih kosong. Untuk mengisi data dari laptop tadi (`data.json`):

1.  Di Dashboard Render, buka tab **Shell** (ini seperti terminal di server).
2.  Tunggu sampai terminal terhubung.
3.  Jalankan perintah ini untuk mengisi database Supabase dengan data json kamu:
    ```bash
    python manage.py loaddata data.json
    ```
4.  Buat superuser baru agar bisa login admin:
    ```bash
    python manage.py createsuperuser
    ```

Selesai\! Sekarang web kamu sudah online di Render, menggunakan database PostgreSQL di Supabase, dan data lama kamu sudah terpindahkan.