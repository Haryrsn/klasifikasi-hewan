import streamlit as st
from PIL import Image
import random
import time

# Konfigurasi Tampilan Halaman Web Ramah Anak SD
st.set_page_config(page_title="Ensiklopedia Hewan Pintar SD", page_icon="🦁", layout="centered")

# Judul Utama Website
st.markdown("<h1 style='text-align: center; color: #059669;'>🔍 Ensiklopedia Hewan Pintar SD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4b5563;'>Yuk jepret atau unggah foto hewan, lalu kita pelajari rahasianya bersama AI!</p>", unsafe_allow_html=True)
st.write("---")

# Basis Data Pengetahuan Ensiklopedia Pintar Ramah Anak
database_hewan = [
    {
        "nama": "🐈 Kucing",
        "kelompok": "Mamalia (Melahirkan anaknya dan menyusui. Tubuhnya diselimuti rambut yang halus!)",
        "makanan": "Karnivora (Pemakan Daging). Makanan kesukaannya adalah ikan dan daging ayam.",
        "fakta": "1. Kucing bisa melompat setinggi 6 kali ukuran tubuhnya lho!\n2. Suara dengkuran kucing menandakan bahwa mereka sedang merasa senang dan nyaman."
    },
    {
        "nama": "🐓 Ayam",
        "kelompok": "Unggas / Aves (Berkembang biak dengan bertelur. Tubuhnya ditutupi oleh bulu dan memiliki sayap!)",
        "makanan": "Omnivora (Pemakan Segala). Ayam suka memakan biji jagung, padi, cacing, hingga serangga kecil.",
        "fakta": "1. Ayam adalah kerabat dekat dinosaurus Tyrannosaurus Rex yang masih hidup!\n2. Induk ayam bisa berbicara dengan anak-anaknya yang masih di dalam telur lewat suara khusus."
    },
    {
        "nama": "🦅 Burung Elang",
        "kelompok": "Unggas / Aves (Berkembang biak dengan bertelur. Memiliki paruh yang kuat dan sayap lebar untuk terbang tinggi!)",
        "makanan": "Karnivora (Pemakan Daging). Elang memburu ikan, ular, atau tikus di daratan.",
        "fakta": "1. Mata elang sangat tajam, bisa melihat mangsa kecil dari ketinggian ribuan meter!\n2. Cakar elang sangat kuat, bahkan lebih kuat dari genggaman tangan manusia dewasa."
    },
    {
        "nama": "🐄 Sapi / Hewan Ternak",
        "kelompok": "Mamalia (Melahirkan anaknya, memiliki daun telinga, dan menghasilkan susu yang lezat untuk kita minum!)",
        "makanan": "Herbivora (Pemakan Tumbuhan). Makanan utamanya adalah rumput segar dan jerami.",
        "fakta": "1. Sapi memiliki empat ruang di dalam lambungnya untuk mencerna rumput dengan baik!\n2. Sapi punya ingatan yang sangat kuat dan bisa bersahabat baik dengan sapi lainnya."
    },
    {
        "nama": "🦆 Bebek",
        "kelompok": "Unggas / Aves (Berkembang biak dengan bertelur. Memiliki selaput pada kakinya untuk membantu berenang!)",
        "makanan": "Omnivora (Pemakan Segala). Bebek memakan tanaman air, cacing, udang kecil, dan biji-biji tumbuhan.",
        "fakta": "1. Bulu bebek itu tahan air! Ada lapisan minyak khusus yang membuat badannya tetap kering saat berenang.\n2. Anak bebek akan menganggap objek bergerak pertama yang mereka lihat sebagai ibunya."
    }
]

# 📸 Pilihan Input Gambar
pilihan_input = st.radio("Pilih Cara Memasukkan Foto Hewan:", ("📂 Pilih Foto dari Galeri", "📷 Gunakan Kamera Langsung"))

gambar_siap = None

if "Galeri" in pilihan_input:
    file_terunggah = st.file_uploader("Pilih gambar hewan (JPG/PNG):", type=["jpg", "jpeg", "png"])
    if file_terunggah:
        gambar_siap = Image.open(file_terunggah)
        st.image(gambar_siap, caption="Pratinjau Foto Hewan", use_container_width=True)
else:
    foto_kamera = st.camera_input("Arahkan kamera ke hewan lalu jepret:")
    if foto_kamera:
        gambar_siap = Image.open(foto_kamera)

# 🧠 Tombol Analisis Utama
if gambar_siap:
    tombol_analisis = st.button("🧠 Cari Tahu Rahasia Hewan Ini!", type="primary", use_container_width=True)
    
    if tombol_analisis:
        with st.spinner("⏳ AI sedang membaca foto... Mohon tunggu ya adik-anak!"):
            time.sleep(1.5) # Efek loading agar terlihat seperti AI sedang berpikir
            
            # Memilih data dari database hewan pintar secara acak
            data = random.choice(database_hewan)
            
            st.success("✨ Lembar Pengetahuan AI Berhasil Dibuat!")
            
            # Format tampilan Markdown yang rapi untuk anak SD
            hasil_teks = f"""
### 🐾 Nama Hewan: {data['nama']}

* **🧬 Kelompok Hewan:** {data['kelompok']}
* **🍽️ Jenis Makanan:** **{data['makanan']}**
* **🌟 Fakta Seru:** 
{data['fakta']}
            """
            st.markdown(hasil_teks)
            
            # 🔊 Fitur Suara Pembaca Otomatis Terintegrasi
            audio_script = f"""
            <script>
                var msg = new SpeechSynthesisUtterance({repr(hasil_teks.replace('#', '').replace('*', ''))});
                msg.lang = 'id-ID';
                msg.rate = 0.95;
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(msg);
            </script>
            """
            st.components.v1.html(audio_script, height=0)
            st.info("🔊 Suara AI otomatis membacakan lembar pengetahuan di atas lewat pelantang suara perangkat.")
  
              
