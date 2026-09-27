import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Konfigurasi Tampilan Halaman Web Ramah Anak SD
st.set_page_config(page_title="Ensiklopedia Hewan Pintar SD", page_icon="🦁", layout="centered")

# Judul Utama Website
st.markdown("<h1 style='text-align: center; color: #059669;'>🔍 Ensiklopedia Hewan Pintar SD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4b5563;'>Yuk jepret atau unggah foto hewan, lalu kita pelajari rahasianya bersama AI!</p>", unsafe_allow_html=True)
st.write("---")

# 🔑 Manajemen API Key Gemini (Input Aman di Layar)
with st.expander("🔑 Pengaturan Kunci AI (Guru/Pengajar)", expanded=True):
    api_key_input = st.text_input("Masukkan API Key Gemini Anda di sini:", type="password", help="Kunci AI gratis dari Google AI Studio")
    if api_key_input:
        genai.configure(api_key=api_key_input)

# 📸 Pilihan Input Gambar (Unggah File atau Kamera Langsung)
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
        if not api_key_input:
            st.error("⚠️ Mohon masukkan API Key Gemini Anda terlebih dahulu di kotak pengaturan atas!")
        else:
            with st.spinner("⏳ AI sedang membaca foto... Mohon tunggu ya adik-anak!"):
                try:
                    # Instruksi analisis ramah anak sekolah dasar
                    prompt = """
                    Analisis gambar hewan ini. Berikan jawaban dalam Bahasa Indonesia yang ceria dan mendidik untuk anak Sekolah Dasar (SD):
                    
                    1. 🐾 Nama Hewan: (Sebutkan nama umum hewan ini)
                    2. 🧬 Kelompok Hewan: (Jelaskan dengan bahasa sederhana apakah ini Mamalia or Unggas/Aves beserta cirinya seperti bertelur/melahirkan)
                    3. 🍽️ Jenis Makanan: (Tulis tebal apakah Herbivora, Karnivora, atau Omnivora, lalu sebutkan makanan kesukaannya)
                    4. 🌟 Fakta Seru: (Berikan 2 fakta unik hewan ini agar memotivasi anak-anak)
                    
                    Gunakan penulisan berpoin dan tambahkan banyak emoji agar menarik perhatian siswa.
                    """
                    
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content([prompt, gambar_siap])
                    
                    # Menampilkan Hasil ke Layar
                    st.success("✨ Lembar Pengetahuan AI Berhasil Dibuat!")
                    hasil_teks = response.text
                    st.markdown(hasil_teks)
                    
                    # 🔊 Fitur Suara Pembaca Otomatis Terintegrasi (Menggunakan HTML5 Speech)
                    audio_script = f"""
                    <script>
                        var msg = new SpeechSynthesisUtterance({repr(hasil_teks)});
                        msg.lang = 'id-ID';
                        msg.rate = 0.95;
                        window.speechSynthesis.cancel();
                        window.speechSynthesis.speak(msg);
                    </script>
                    """
                    st.components.v1.html(audio_script, height=0)
                    st.info("🔊 Suara AI otomatis berbunyi membacakan teks di atas lewat pelantang suara perangkat.")
                    
                except Exception as e:
                    st.error(f"😥 Ups, terjadi kendala koneksi AI. Silakan coba lagi. (Error: {str(e)})")
