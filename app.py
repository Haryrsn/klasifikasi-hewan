import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np
import time

# Konfigurasi Tampilan Halaman Web Ceria Ramah Anak SD
st.set_page_config(page_title="Mega-Ensiklopedia Hewan Pintar SD", page_icon="🦁", layout="centered")

st.markdown("<h1 style='text-align: center; color: #059669;'>🔍 Mega-Ensiklopedia Hewan Pintar SD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4b5563;'>Koleksi 101 Makhluk Hidup Lengkap! Yuk jepret atau unggah foto untuk belajar bersama AI!</p>", unsafe_allow_html=True)
st.write("---")

# 📋 DATABASE AKBAR 101 JENIS MAKHLUK HIDUP (50 UNGGAS & 51 MAMALIA)
database_hewan = {
    # ==================== KELOMPOK UNGGAS (50 HEWAN) ====================
    "ayam": {"nama": "🐓 Ayam", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Pemakan Segala)", "fakta": "Kerabat dekat T-Rex yang masih hidup. Induk ayam bisa mengobrol dengan anaknya yang masih di dalam telur."},
    "bebek": {"nama": "🦆 Bebek", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Pemakan Segala)", "fakta": "Bulunya anti air karena dilapisi minyak khusus. Anak bebek menganggap benda bergerak pertama yang dilihatnya sebagai ibunya."},
    "elang": {"nama": "🦅 Burung Elang", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Pemakan Daging)", "fakta": "Matanya super tajam, bisa melihat mangsa kecil dari ketinggian ribuan meter. Cakarnya lebih kuat dari genggaman tangan manusia."},
    "merpati": {"nama": "🕊️ Burung Merpati", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora / Granivora (Biji-bijian)", "fakta": "Punya navigasi alami yang hebat sehingga dulu sering dipakai sebagai burung pengantar surat."},
    "pinguin": {"nama": "🐧 Pinguin", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Pemakan Ikan)", "fakta": "Unggas yang tidak bisa terbang tapi jago berenang. Pinguin jantan bertugas mengerami telur di atas kakinya."},
    "burung_hantu": {"nama": "🦉 Burung Hantu", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Daging/Tikus)", "fakta": "Hewan nokturnal (aktif malam hari) yang bisa memutar kepalanya hingga 270 derajat."},
    "merak": {"nama": "🦚 Burung Merak", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Segala)", "fakta": "Merak jantan memiliki bulu ekor raksasa yang indah untuk menarik perhatian merak betina."},
    "flamingo": {"nama": "🦩 Burung Flamingo", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Segala)", "fakta": "Bulunya berwarna merah muda karena mereka banyak memakan udang kecil dan alga yang mengandung karotenoid."},
    "angsa": {"nama": "🦢 Angsa", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Tanaman air/Rumput)", "fakta": "Hewan yang sangat setia pada pasangannya dan bisa menjadi sangat galak jika sarangnya diganggu."},
    "kalkun": {"nama": "🦃 Burung Kalkun", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Segala)", "fakta": "Kalkun liar bisa terbang jarak pendek dan bisa tidur di atas dahan pohon tinggi untuk menghindari pemangsa."},
    "kakaktua": {"nama": "🦜 Burung Kakaktua", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji/Buah)", "fakta": "Burung pintar yang berumur panjang dan memiliki kemampuan meniru suara manusia atau bunyi di sekitarnya."},
    "unta_burung": {"nama": "🐦 Burung Unta", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Segala)", "fakta": "Burung terbesar di dunia. Tidak bisa terbang, tapi bisa berlari sekencang mobil (70 km/jam)."},
    "pelatuk": {"nama": "🐦 Burung Pelatuk", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora / Insektivora (Serangga)", "fakta": "Bisa mematuk batang pohon hingga 20 kali dalam satu detik tanpa membuat kepalanya pusing."},
    "kolibri": {"nama": "🐦 Burung Kolibri", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Nektar Bunga)", "fakta": "Burung terkecil di dunia dan satu-satunya burung yang bisa terbang mundur atau melayang diam di udara."},
    "gagak": {"nama": "🐦 Burung Gagak", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Segala)", "fakta": "Sangat jenius! Gagak bisa mengenali wajah manusia yang berbuat jahat dan mengingatnya bertahun-tahun."},
    "pelikan": {"nama": "🐦 Burung Pelikan", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Ikan)", "fakta": "Punya kantung raksasa di bawah paruhnya yang berfungsi seperti jaring serok untuk menangkap ikan."},
    "camar": {"nama": "🐦 Burung Camar", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Ikan/Hewan laut)", "fakta": "Bisa meminum air laut yang asin karena punya kelenjar khusus untuk menyaring garam dari tubuhnya."},
    "albatros": {"nama": "🐦 Burung Albatros", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Ikan/Cumi)", "fakta": "Punya bentang sayap terlebar di dunia. Bisa terbang berhari-hari di atas samudra tanpa mengepakkan sayap."},
    "kasuari": {"nama": "🐦 Burung Kasuari", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora / Frugivora (Buah)", "fakta": "Burung paling berbahaya di dunia. Punya cakar kaki tengah sepanjang 12 cm yang tajam seperti belati."},
    "puyuh": {"nama": "🐦 Burung Puyuh", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Segala)", "fakta": "Suka tinggal di semak-semak dan bertelur banyak dengan corak totol-totol cokelat yang unik."},
    "kakatua_raja": {"nama": "🦜 Kakatua Raja", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji keras)", "fakta": "Punya paruh raksasa super kuat yang bisa memecahkan cangkang biji kelapa sawit yang sangat keras."},
    "cendrawasih": {"nama": "🐦 Burung Cendrawasih", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Buah/Serangga)", "fakta": "Dijuluki burung surga dari Papua karena keindahan bulunya yang menawan saat menari."},
    "nuri": {"nama": "🐦 Burung Nuri", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Nektar/Buah)", "fakta": "Punya lidah berbulu tipis di ujungnya untuk menyedot nektar bunga dengan mudah."},
    "lovebird": {"nama": "🐦 Burung Lovebird", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji-bijian)", "fakta": "Hewan sosial yang sangat setia. Jika pasangannya mati, burung ini bisa ikut stres dan sakit."},
    "kenari": {"nama": "🐦 Burung Kenari", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji/Sayur)", "fakta": "Terkenal karena suaranya yang merdu dan nyaring, sering dipakai sebagai pemancing burung lain bernyanyi."},
    "kacer": {"nama": "🐦 Burung Kacer", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Serangga)", "fakta": "Jago berkicau dan meniru suara lingkungan sekitarnya jika dilatih sejak kecil."},
    "jalak": {"nama": "🐦 Burung Jalak", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Segala)", "fakta": "Suka hinggap di punggung sapi untuk memakan kutu, membantu sapi terbebas dari gatal."},
    "prenjak": {"nama": "🐦 Burung Prenjak", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Serangga)", "fakta": "Ukurannya kecil dan sangat lincah bergerak di antara dahan pohon bersemak."},
    "pigeon": {"nama": "🐦 Burung Dara", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji)", "fakta": "Bisa menemukan jalan pulang ke sarangnya meskipun dilepaskan dari tempat berjarak ratusan kilometer."},
    "tekukur": {"nama": "🐦 Burung Tekukur", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji di tanah)", "fakta": "Suka mencari makan di permukaan tanah dan punya suara anggungan yang khas."},
    "rajawali": {"nama": "🦅 Burung Rajawali", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Daging)", "fakta": "Sanggup terbang menembus badai besar dengan memanfaatkan arus angin kencang."},
    "kondor": {"nama": "🦅 Burung Kondor", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Bangkai hewan)", "fakta": "Burung pemakan bangkai terbesar yang membantu membersihkan lingkungan hutan dari kuman penyakit."},
    "bangau": {"nama": "🐦 Burung Bangau", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Katak/Ikan)", "fakta": "Suka berdiri diam dengan satu kaki di area rawa dalam waktu yang sangat lama untuk mengelabui ikan."},
    "pipit": {"nama": "🐦 Burung Pipit", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji rumput)", "fakta": "Ukurannya mungil dan suka terbang berbondong-bondong memakan biji rumput liar."},
    "murai": {"nama": "🐦 Burung Murai Batu", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Serangga)", "fakta": "Punya ekor yang sangat panjang dan indah yang akan bergoyang saat burung ini berkicau merdu."},
    "trucukan": {"nama": "🐦 Burung Trucukan", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Buah/Serangga)", "fakta": "Suka berjemur di pagi hari sambil mengepakkan kedua sayapnya lebar-lebar."},
    "perkutut": {"nama": "🐦 Burung Perkutut", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji kecil)", "fakta": "Sangat disukai karena suara kicauannya dianggap memberikan ketenangan bagi pemiliknya."},
    "pleci": {"nama": "🐦 Burung Pleci", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Nektar/Ulat)", "fakta": "Punya lingkaran putih seperti kacamata di sekeliling matanya yang mungil."},
    "gereja": {"nama": "🐦 Burung Gereja", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Sisa makanan/Biji)", "fakta": "Sangat adaptif dan suka bersarang di sela-sela atap bangunan rumah manusia."},
    "manyar": {"nama": "🐦 Burung Manyar", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji)", "fakta": "Arsitek terbaik! Burung jantan bisa merajut sarang rumput yang rumit dan menggantung di pohon."},
    "kedasih": {"nama": "🐦 Burung Kedasih", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Ulat)", "fakta": "Burung yang licik karena suka menitipkan telurnya di sarang burung lain agar dirawat oleh burung tersebut."},
    "panca_warna": {"nama": "🐦 Burung Pancawarna", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Serangga)", "fakta": "Sesuai namanya bulunya memiliki kombinasi lima warna cerah yang sangat menawan."},
    "toko": {"nama": "🐦 Burung Toucan", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora / Frugivora (Buah)", "fakta": "Paruhnya berukuran raksasa dan berwarna warni namun sangat ringan karena strukturnya berongga."},
    "macaw": {"nama": "🦜 Burung Macaw", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Kacang/Biji)", "fakta": "Jenis burung beo terbesar dengan bulu merah biru kuning yang sangat kontras di hutan Amazon."},
    "kiwi": {"nama": "🐦 Burung Kiwi", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Omnivora (Cacing/Biji)", "fakta": "Burung unik tanpa sayap dari Selandia Baru. Ukuran telurnya hampir sepertiga ukuran tubuhnya sendiri."},
    "kormoran": {"nama": "🐦 Burung Kormoran", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Ikan)", "fakta": "Jago menyelam hingga kedalaman puluhan meter di bawah laut untuk mengejar ikan buruannya."},
    "puffin": {"nama": "🐦 Burung Puffin", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Ikan kecil)", "fakta": "Dijuluki badut laut karena paruhnya segitiga besar berwarna jingga cerah yang menggemaskan."},
    "ibis": {"nama": "🐦 Burung Ibis", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Karnivora (Hewan rawa)", "fakta": "Punya paruh panjang melengkung ke bawah untuk mendeteksi makanan di dalam lumpur rawa yang gelap."},
    "mambruk": {"nama": "🐦 Burung Mambruk", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Buah jatuh)", "fakta": "Merpati raksasa dari Papua yang punya mahkota bulu indah seperti kipas di atas kepalanya."},
    "emprit": {"nama": "🐦 Burung Emprit", "kelompok": "Unggas (Aves) - Bertelur", "makanan": "Herbivora (Biji rumput)", "fakta": "Ukurannya mungil dan suka terbang berbondong-bondong memakan biji rumput liar di sawah."},
    
    # ==================== KELOMPOK MAMALIA (51 MAKHLUK) ====================
    "manusia": {"nama": "🧍 Manusia (Homo sapiens)", "kelompok": "Mamalia - Melahirkan", "makanan": "Omnivora (Pemakan Segala)", "fakta": "Punya otak paling cerdas untuk berpikir dan menciptakan teknologi. Satu-satunya mamalia yang mempunyai fisik sempurna Masya Allah."},
    "kucing": {"nama": "🐈 Kucing", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Pemakan Daging)", "fakta": "Bisa melompat 6 kali tinggi tubuhnya. Suara dengkurannya menandakan ia merasa aman dan bahagia."},
    "sapi": {"nama": "🐄 Sapi", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Pemakan Rumput)", "fakta": "Punya empat ruang di lambungnya. Memiliki ingatan kuat dan bisa bersahabat erat dengan sesama sapi."},
    "kambing": {"nama": "🐐 Kambing", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Pemakan Tumbuhan)", "fakta": "Pupil matanya mendatar berbentuk persegi panjang untuk melihat musuh dari samping dengan sangat luas."},
    "harimau": {"nama": "🐯 Harimau", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Pemakan Daging)", "fakta": "Garis belang di tubuhnya unik mirip sidik jari manusia. Sangat suka berenang di sungai saat cuaca panas."},
    "anjing": {"nama": "🐕 Anjing", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora / Omnivora", "fakta": "Indra penciumannya 40 kali lebih tajam dari manusia, bisa mendeteksi emosi pemiliknya."},
    "gajah": {"nama": "🐘 Gajah", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Pemakan Tumbuhan)", "fakta": "Hewan darat terbesar di dunia. Takut dengan lebah dan bisa berkomunikasi jarak jauh lewat getaran tanah."},
    "singa": {"nama": "🦁 Singa", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Pemakan Daging)", "fakta": "Dijuluki raja hutan. Singa betina yang bertugas berburu makanan, sedangkan singa jantan menjaga wilayah."},
    "kuda": {"nama": "🐎 Kuda", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Pemakan Rumput)", "fakta": "Bisa tidur sambil berdiri berkat sistem penguncian sendi kaki khusus agar selalu siap kabur dari pemangsa."},
    "monyet": {"nama": "🐒 Monyet", "kelompok": "Mamalia - Melahirkan", "makanan": "Omnivora (Pemakan Segala)", "fakta": "Menggunakan ekornya yang kuat sebagai tangan kelima untuk bergelantungan dengan lincah di pohon."},
    "kelinci": {"nama": "🐇 Kelinci", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Pemakan Tumbuhan)", "fakta": "Telinga panjangnya berfungsi mendengarkan predator sekaligus mendinginkan suhu tubuhnya saat kepanasan."},
    "beruang": {"nama": "🐻 Beruang", "kelompok": "Mamalia - Melahirkan", "makanan": "Omnivora (Pemakan Segala)", "fakta": "Bisa tidur berbulan-bulan tanpa makan dan minum di musim dingin, proses ini disebut hibernasi."},
    "lumba_lumba": {"nama": "🐬 Lumba-lumba", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Pemakan Ikan)", "fakta": "Bukan ikan melainkan mamalia laut yang bernapas dengan paru-paru. Tidur dengan satu mata terbuka."},
    "paus": {"nama": "🐳 Paus Biru", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Krill/Udang kecil)", "fakta": "Hewan terbesar yang pernah hidup di bumi, ukuran lidahnya saja seberat satu ekor gajah dewasa."},
    "kangguru": {"nama": "🦘 Kangguru", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Tumbuhan)", "fakta": "Punya kantung di perut untuk membesarkan bayinya (joey). Kangguru tidak bisa berjalan mundur."},
    "koala": {"nama": "🐨 Koala", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Daun Kayu Putih)", "fakta": "Hewan pemalas yang bisa tidur selama 20 jam sehari karena daun yang dimakannya rendah energi."},
    "jerapah": {"nama": "🦒 Jerapah", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Daun pohon tinggi)", "fakta": "Hewan tertinggi di dunia. Tidurnya sangat sebentar, hanya sekitar 30 menit dalam sehari semalam."},
    "zebra": {"nama": "🦓 Zebra", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Rumput)", "fakta": "Garis hitam putih di tubuhnya berfungsi membingungkan lalat pengisap darah dan sebagai pendingin alami."},
    "serigala": {"nama": "🐺 Serigala", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Daging)", "fakta": "Hidup berkelompok dengan pemimpin yang disebut Alpha. Suara lolongannya dipakai untuk menandai wilayah."},
    "tikus": {"nama": "🐀 Tikus", "kelompok": "Mamalia - Melahirkan", "makanan": "Omnivora (Segala)", "fakta": "Gigi depannya terus tumbuh sepanjang hidup, sehingga mereka harus selalu menggigiti benda keras agar giginya tumpul."},
    "tupai": {"nama": "🐿️ Tupai", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Biji/Kacang)", "fakta": "Jasa penyelamat hutan karena suka menimbun biji kacang di tanah lalu melupakan tempatnya, sehingga tumbuh pohon baru."},
    "badak": {"nama": "🦏 Badak", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Tumbuhan)", "fakta": "Cula badak terbuat dari keratin, zat yang sama dengan kuku manusia. Pandangan matanya sangat kabur."},
    "kuda_nil": {"nama": "🦛 Kuda Nil", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Rumput)", "fakta": "Tubuhnya mengeluarkan keringat berwarna merah mirip darah yang berfungsi sebagai tabir sunya alami dari matahari."},
    "unta": {"nama": "🐪 Unta", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Tumbuhan berduri)", "fakta": "Punuk unta berisi simpanan lemak (bukan air) yang diubah menjadi energi saat makanan di gurun habis."},
    "panda": {"nama": "🐼 Panda", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Bambu)", "fakta": "Menghabiskan waktu 12 jam sehari hanya untuk mengunyah batang bambu agar kebutuhan gizinya terpenuhi."},
    "domba": {"nama": "🐑 Domba", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Rumput)", "fakta": "Bulu tebalnya (wol) terus tumbuh dan tidak bisa rontok sendiri, sehingga harus dicukur secara berkala oleh manusia."},
    "babi": {"nama": "🐖 Babi", "kelompok": "Mamalia - Melahirkan", "makanan": "Omnivora (Segala)", "fakta": "Hewan yang sangat cerdas dan bersih. Suka berkubang di lumpur hanya untuk mendinginkan tubuh karena tidak punya kelenjar keringat."},
    "rusa": {"nama": "🦌 Rusa", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Rumput/Daun)", "fakta": "Tanduk rusa jantan (antler) akan rontok setiap tahun dan tumbuh kembali menjadi lebih besar dan bercabang."},
    "kancil": {"nama": "🦌 Kancil / Pelanduk", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Buah jatuh/Tunas)", "fakta": "Mamalia berkuku terkecil di dunia. Sangat cerdik dan lincah bersembunyi di lantai hutan."},
    "kelelawar": {"nama": "🦇 Kelelawar", "kelompok": "Mamalia - Melahirkan", "makanan": "Omnivora (Buah/Serangga)", "fakta": "Satu-satunya mamalia yang bisa terbang sejati. Menggunakan pantulan suara (ekolokasi) untuk melihat di kegelapan."},
    "platipus": {"nama": "🦆 Platipus", "kelompok": "Mamalia - Bertelur (Monotremata)", "makanan": "Karnivora (Cacing/Udang)", "fakta": "Mamalia purba unik yang bertelur tapi menyusui anaknya. Paruhnya mirip bebek namun badannya berbulu."},
    "singa_laut": {"nama": "🦭 Singa Laut", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Ikan)", "fakta": "Punya sirip kaki belakang yang bisa ditekuk ke depan untuk berjalan tegak di atas daratan pantai."},
    "anjing_laut": {"nama": "𦭭 Anjing Laut", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Ikan)", "fakta": "Berbeda dengan singa laut, anjing laut tidak punya daun telinga dan bergerak di darat dengan merayap menggunakan perut."},
    "walrus": {"nama": "𦭭 Walrus", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Kerang laut)", "fakta": "Punya sepasang taring raksasa yang panjangnya bisa mencapai 1 meter untuk membantunya naik ke atas es."},
    "landak": {"nama": "𦔔 Landak", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Akar/Kulit pohon)", "fakta": "Tubuhnya diselimuti oleh 30.000 duri tajam yang akan berdiri tegak jika dirinya merasa terancam musuh."},
    "orangutan": {"nama": "𦧧 Orangutan", "kelompok": "Mamalia - Melahirkan", "makanan": "Omnivora (Buah/Rayap)", "fakta": "Punya DNA yang 97% mirip manusia. Setiap sore mereka membuat sarang tidur baru dari jalinan daun di atas pohon."},
    "simpanse": {"nama": "🐒 Simpanse", "kelompok": "Mamalia - Melahirkan", "makanan": "Omnivora (Segala)", "fakta": "Primata paling cerdas, sanggup menggunakan alat bantu seperti batu atau ranting untuk memecahkan buah kacang."},
    "gorila": {"nama": "🦍 Gorila", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Batang/Daun)", "fakta": "Primata terbesar yang sangat kuat namun memiliki sifat yang lembut dan pemalu di dalam habitatnya."},
    "kungkang": {"nama": "𦥥 Kungkang / Sloth", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Daun pohon)", "fakta": "Hewan terlambat di dunia. Gerakannya sangat lamban sehingga lumut hijau bisa tumbuh subur di atas bulu punggungnya."},
    "trenggiling": {"nama": "🐜 Trenggiling", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora / Insektivora (Semut)", "fakta": "Akan menggulung badannya menjadi bola keras seperti tameng baja jika diserang oleh harimau atau pemangsa."},
    "lemur": {"nama": "🐒 Lemur", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Buah/Daun)", "fakta": "Hewan endemik dari pulau Madagaskar yang memiliki mata bulat besar menyala saat malam hari."},
    "bison": {"nama": "𦜬 Bison", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Rumput)", "fakta": "Banteng raksasa berbulu lebat di bagian depan tubuhnya untuk menahan hawa dingin ekstrem salju."},
    "yak": {"nama": "𦜬 Yak", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Rumput gunung)", "fakta": "Sapi gunung berbulu gondrong menjuntai ke tanah yang tinggal di dataran tinggi pegunungan Himalaya."},
    "hyena": {"nama": "🐺 Hyena", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Daging)", "fakta": "Punya rahang super kuat yang bisa menghancurkan tulang kaki gajah. Mengeluarkan suara unik mirip tawa manusia."},
    "cheetah": {"nama": "🐆 Cheetah", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Daging)", "fakta": "Hewan darat tercepat di dunia. Bisa berlari dari kecepatan 0 hingga 100 km/jam hanya dalam waktu 3 detik."},
    "macan_tutul": {"nama": "🐆 Macan Tutul", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Daging)", "fakta": "Jago memanjat pohon sambil membawa mangsa yang badannya dua kali lebih berat dari tubuhnya ke atas dahan."},
    "berang_berang": {"nama": "🦦 Berang-berang", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Ikan/Kerang)", "fakta": "Arsitek air! Suka menebang pohon dengan giginya untuk membuat bendungan air sebagai rumah perlindungan."},
    "musang": {"nama": "𦝝 Musang", "kelompok": "Mamalia - Melahirkan", "makanan": "Omnivora (Buah/Ayam)", "fakta": "Jago memanjat pohon dan loteng rumah pada malam hari untuk berburu buah matang atau tikus."},
    "tapir": {"nama": "🐖 Tapir", "kelompok": "Mamalia - Melahirkan", "makanan": "Herbivora (Daun muda)", "fakta": "Badannya mirip babi tapi punya belalai pendek. Anak tapir lahir dengan corak garis totol mirip semangka."},
    "koyote": {"nama": "🐺 Koyote", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora (Hewan kecil)", "fakta": "Serigala gurun berukuran kecil yang sangat cerdik beradaptasi tinggal di dekat lingkungan kota besar."},
    "meerkat": {"nama": "🦦 Meerkat", "kelompok": "Mamalia - Melahirkan", "makanan": "Karnivora / Insektivora (Kalajengking)", "fakta": "Selalu berdiri tegak dengan kaki belakangnya untuk bergantian bertugas menjadi penjaga pos keamanan kelompoknya."}
}

  # =====================================================================
# 📸 PANTIKAN KODE PERINTAH UTAMA: MENGAKTIFKAN MATA AI VISION LOKAL
# =====================================================================

# 📋 AKTIFKAN MATA AI VISION LOKAL (Memindai Objek Visual Tanpa Google Gemini)
@st.cache_resource
def load_local_vision_ai():
    return tf.keras.applications.MobileNetV2(weights='imagenet')

model_vision = load_local_vision_ai()

# 📸 Pilihan Metode Pemasukkan Foto
pilihan_input = st.radio("Pilih Cara Memasukkan Foto:", ("📂 Pilih Foto dari Galeri", "📷 Gunakan Kamera Langsung"))

gambar_siap = None

if "Galeri" in pilihan_input:
    file_terunggah = st.file_uploader("Pilih gambar makhluk hidup atau hewan (Bebas nama file):", type=["jpg", "jpeg", "png"])
    if file_terunggah:
        gambar_siap = Image.open(file_terunggah)
        st.image(gambar_siap, caption="Pratinjau Foto Sukses Dimuat", use_container_width=True)
else:
    foto_kamera = st.camera_input("Arahkan kamera ke objek lalu jepret:")
    if foto_kamera:
        gambar_siap = Image.open(foto_kamera)

# 🧠 TOMBOL ANALISIS VISION OTOMATIS (Menebak Langsung dari Gambar)
if gambar_siap:
    tombol_analisis = st.button("🧠 Cari Tahu Rahasia Makhluk Hidup Ini!", type="primary", use_container_width=True)
    
    if tombol_analisis:
        with st.spinner("⏳ Mata AI sedang memindai bentuk objek foto..."):
            
            # 👁️ PROSES VISION MURNI: Mengubah foto agar terbaca oleh mata AI secara visual
            img_resized = gambar_siap.resize((224, 224)).convert('RGB')
            x = tf.keras.preprocessing.image.img_to_array(img_resized)
            x = np.expand_dims(x, axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            
            # AI menebak bentuk visual gambar
            preds = model_vision.predict(x)
            decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)
            
            # Mencari kata kunci bahasa Indonesia berdasarkan hasil tebakan visual AI
            hewan_ditemukan = None
            prediksi_tertinggi_inggris = decoded_preds[0][1].lower()
            
            # Jalur 1: Cek kecocokan lewat Kamus Penerjemah ke Bahasa Indonesia
            kata_kunci_indo = None
            for i in range(len(decoded_preds[0])):
                nama_inggris = decoded_preds[0][i][1].lower()
                if nama_inggris in kamus_terjemahan:
                    kata_kunci_indo = kamus_terjemahan[nama_inggris]
                    break
            
            # Jalur 2: Ambil data dari database bahasa Indonesia kita berdasarkan hasil terjemahan
            if kata_kunci_indo in database_hewan:
                hewan_ditemukan = database_hewan[kata_kunci_indo]
            
            # Jika objek di luar jangkauan database, tampilkan respon edukasi universal ceria
            if not hewan_ditemukan:
                hewan_ditemukan = {
                    "nama": f"🐾 Sahabat Makhluk Unik (Deteksi Visual AI: {prediksi_tertinggi_inggris.replace('_', ' ')})",
                    "kelompok": "Mamalia atau Unggas (Tergantung bentuk fisiknya. Jika berbulu sayap dan bertelur berarti Unggas, jika berambut dan melahirkan/menyusui berarti Mamalia!)",
                    "makanan": "Herbivora (tumbuhan), Karnivora (daging), atau Omnivora (segala) berdasarkan struktur tubuhnya.",
                    "fakta": "1. Setiap makhluk hidup di bumi diciptakan unik dan memiliki tugas penting untuk menjaga kelestarian alam.\n2. Menyayangi makhluk sekitar membuat bumi kita tetap indah!"
                }
            
            st.success("✨ Lembar Pengetahuan Berhasil Dibuat!")
            
            hasil_teks = f"""
### 🐾 Nama: {hewan_ditemukan['nama']}

* **🧬 Kelompok:** {hewan_ditemukan['kelompok']}
* **🍽️ Jenis Makanan:** **{hewan_ditemukan['makanan']}**
* **🌟 Fakta Seru:** 
{hewan_ditemukan['fakta']}
            """
            st.markdown(hasil_teks)
            
            # 🔊 Sistem Narasi Suara Otomatis
            teks_suara = hasil_teks.replace('#', '').replace('*', '').replace('\n', ' ')
            audio_script = f"""
            <script>
                var msg = new SpeechSynthesisUtterance({repr(teks_suara)});
                msg.lang = 'id-ID';
                msg.rate = 0.95;
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(msg);
            </script>
            """
            st.components.v1.html(audio_script, height=0)
            st.info("🔊 Suara otomatis berbunyi membacakan lembar ilmu pengetahuan di atas.")
            st.components.v1.html(audio_script, height=0)
            st.info("🔊 Suara otomatis berbunyi membacakan lembar ilmu pengetahuan di atas.")
