import streamlit as st
import random

# Konfigurasi Halaman & Tema Cyberpunk Visual
st.set_page_config(page_title="CodeQuest: The Digital Nexus", page_icon="🌐", layout="centered")

# Custom CSS untuk tampilan Gaming UI premium
st.markdown("""
<style>
    .reportview-container { background: #0a0e17; }
    .main { background-color: #0a0e17; color: #00ffcc; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3 { color: #ff007f !important; text-shadow: 0 0 10px #ff007f; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #ff007f , #00ffcc); }
    .css-1evm0ov { background-color: #121824; border: 1px solid #00ffcc; border-radius: 10px; padding: 20px; box-shadow: 0px 0px 15px rgba(0, 255, 204, 0.2); }
    .wordle-box { display: inline-block; width: 40px; height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; border-radius: 5px; margin: 2px; color: white; }
    .w-correct { background-color: #2e7d32; border: 2px solid #4caf50; }
    .w-present { background-color: #f57f17; border: 2px solid #fbc02d; }
    .w-absent { background-color: #37474f; border: 2px solid #78909c; }
</style>
""", unsafe_allow_html=True)

# Definisikan Bank Soal Tersegmentasi berdasarkan Tema/Faksi
THEME_DATABASE = {
    "Cyber Security & Hacking": [
        {"tipe": "PG", "soal": "Jenis malware yang mengunci data pengguna dan meminta tebusan uang disebut...", "opsi": ["Spyware", "Ransomware", "Trojan", "Worm"], "jawaban": "Ransomware"},
        {"tipe": "Wordle", "soal": "Tebak Istilah: Metode mengelabui pengguna untuk mencuri kredensial lewat link palsu.", "hint": "7 Huruf. Berawalan 'P' dan berakhir 'G'.", "jawaban": "PHISHING"},
        {"tipe": "PG", "soal": "Proses mengubah teks biasa menjadi teks rahasia yang tidak dapat dibaca disebut...", "opsi": ["Dekripsi", "Hashing", "Enkripsi", "Obfuscation"], "jawaban": "Enkripsi"}
    ],
    "AI & Data Science Necromancer": [
        {"tipe": "PG", "soal": "Manakah algoritma Machine Learning yang terinspirasi dari struktur jaringan saraf biologis manusia?", "opsi": ["Linear Regression", "Decision Tree", "Neural Network", "K-Means"], "jawaban": "Neural Network"},
        {"tipe": "Wordle", "soal": "Tebak Istilah: Proses melatih model dengan data agar memiliki kemampuan prediksi.", "hint": "8 Huruf. Berawalan 'T' dan berakhir 'G'.", "jawaban": "TRAINING"},
        {"tipe": "PG", "soal": "Tipe data atau nilai statistik yang berada jauh dari kumpulan data lainnya disebut...", "opsi": ["Mean", "Outlier", "Variance", "Missing Value"], "jawaban": "Outlier"}
    ],
    "Software Wizard & Logic": [
        {"tipe": "PG", "soal": "Manakah di bawah ini yang merupakan struktur data dengan prinsip FIFO (First In First Out)?", "opsi": ["Stack", "Queue", "Tree", "Graph"], "jawaban": "Queue"},
        {"tipe": "Wordle", "soal": "Tebak istilah: Sekumpulan instruksi terstruktur untuk menyelesaikan masalah.", "hint": "9 Huruf. Berawalan 'A' dan berakhir 'M'.", "jawaban": "ALGORITMA"},
        {"tipe": "Wordle", "soal": "Tebak istilah: Tipe data logika yang hanya bernilai True atau False.", "hint": "7 Huruf. Berawalan 'B' dan berakhir 'N'.", "jawaban": "BOOLEAN"}
    ]
}

# State Engine Initialization
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "theme" not in st.session_state:
    st.session_state.theme = None
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "wordle_feedback" not in st.session_state:
    st.session_state.wordle_feedback = ""

# Perhitungan Level berbasis XP
player_level = (st.session_state.xp // 20) + 1

# --- SCREEN 1: PILIHAN TEMA / DECK ---
if not st.session_state.game_started:
    st.title("🕹️ EDUTEKAL")
    st.subheader("Uji Logika, Kumpulkan XP, dan Naikkan Levelmu")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🛡️ Cyber Security")
        st.caption("Fokus pada celah keamanan, malware, dan enkripsi pertahanan siber.")
        if st.button("Pilih Cyber Security"):
            st.session_state.theme = "Cyber Security & Hacking"
            st.session_state.game_started = True
            questions = THEME_DATABASE[st.session_state.theme].copy()
            random.shuffle(questions)
            st.session_state.questions = questions
            st.rerun()
            
    with col2:
        st.markdown("### 🧠 AI & Data Science")
        st.caption("Jelajahi dunia statistik, neural networks, dan manipulasi masa depan.")
        if st.button("Pilih Data Science"):
            st.session_state.theme = "AI & Data Science Necromancer"
            st.session_state.game_started = True
            questions = THEME_DATABASE[st.session_state.theme].copy()
            random.shuffle(questions)
            st.session_state.questions = questions
            st.rerun()
            
    with col3:
        st.markdown("### 🔮 Software Wizard")
        st.caption("Kuasai algoritma murni, arsitektur kode dasar, dan logika komputasi.")
        if st.button("Pilih Software Wizard"):
            st.session_state.theme = "Software Wizard & Logic"
            st.session_state.game_started = True
            questions = THEME_DATABASE[st.session_state.theme].copy()
            random.shuffle(questions)
            st.session_state.questions = questions
            st.rerun()

# --- SCREEN 2: GAMEPLAY RUNNING ---
elif st.session_state.game_started and not st.session_state.game_over:
    # Cek Kondisi Kalah / Selesai
    if st.session_state.lives <= 0 or st.session_state.current_question >= len(st.session_state.questions):
        st.session_state.game_over = True
        st.rerun()

    # Tampilan Dasbor Status Atas
    st.title(f"⚡ Nexus Zone: {st.session_state.theme}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("PLAYER LEVEL", f"LVL {player_level}")
    c2.metric("EXP POINTS", f"✨ {st.session_state.xp} XP")
    c3.metric("INTEGRITY CORE (LIVES)", "❤️ " * st.session_state.lives if st.session_state.lives > 0 else "💥")
    
    # Progress Bar menuju level selanjutnya
    progress_val = (st.session_state.xp % 20) / 20
    st.progress(progress_val, text=f"Progress Ke Level Berikutnya: {int(progress_val*100)}%")
    st.write("---")

    q_idx = st.session_state.current_question
    q = st.session_state.questions[q_idx]

    st.markdown(f"### 🎯 Node Ke-{q_idx + 1} dari {len(st.session_state.questions)}")
    st.info(q["soal"])

    # Form Pertanyaan
    with st.form(key=f"nexus_node_{q_idx}"):
        if q["tipe"] == "PG":
            pilihan = st.radio("Dekripsi Node (Pilih Opsi):", q["opsi"])
            submit = st.form_submit_button("Injeksi Jawaban 🔓")
            
            if submit:
                if pilihan == q["jawaban"]:
                    st.success("🎉 CORE DECRYPTED! +10 XP Berhasil Diinjeksi.")
                    st.session_state.xp += 10
                else:
                    st.error(f"❌ DECRYPTION FAILED! Kunci asli adalah: {q['jawaban']}")
                    st.session_state.lives -= 1
                st.session_state.current_question += 1
                st.session_state.wordle_feedback = ""
                st.write("Klik tombol 'Lanjutkan Node' di bawah.")

        elif q["tipe"] == "Wordle":
            st.caption(f"💡 Petunjuk Enkripsi: {q['hint']}")
            tebakan = st.text_input("Ketik Kata Kunci (Caps Lock Otomatis):").strip().upper()
            submit = st.form_submit_button("Kirim Sinyal Kata 📤")

            if submit:
                if tebakan == q["jawaban"]:
                    st.success("🎉 EXCELLENT! Kata Kunci Sempurna. +20 XP Ekstra!")
                    st.session_state.xp += 20
                    st.session_state.current_question += 1
                    st.session_state.wordle_feedback = ""
                else:
                    # Logic Analisis Akurasi Karakter ala Wordle
                    feedback_html = ""
                    jawaban_asli = q["jawaban"]
                    
                    if len(tebakan) != len(jawaban_asli):
                        st.warning(f"Panjang kata tidak sesuai! Harus {len(jawaban_asli)} huruf.")
                    else:
                        for i in range(len(tebakan)):
                            if tebakan[i] == jawaban_asli[i]:
                                feedback_html += f"<div class='wordle-box w-correct'>{tebakan[i]}</div>"
                            elif tebakan[i] in jawaban_asli:
                                feedback_html += f"<div class='wordle-box w-present'>{tebakan[i]}</div>"
                            else:
                                feedback_html += f"<div class='wordle-box w-absent'>{tebakan[i]}</div>"
                        
                        st.session_state.wordle_feedback = feedback_html
                        st.session_state.lives -= 1
                        st.error("❌ SISTEM REJECTED! Analisis Grid Karakter Anda di bawah:")
                        
                        if st.session_state.lives <= 0:
                            st.session_state.current_question += 1

    # Tampilkan Grid Feedback Wordle jika ada kesalahan input
    if st.session_state.wordle_feedback:
        st.markdown("### 📊 Status Grid Akurasi Kata Anda:")
        st.markdown(st.session_state.session_state.wordle_feedback if hasattr(st.session_state, 'wordle_feedback') else st.session_state.wordle_feedback, unsafe_allow_html=True)
        st.caption("Warna Hijau = Huruf & Posisi Tepat | Jingga = Huruf Ada tapi Posisi Salah | Abu-abu = Huruf Salah")

    if st.button("Lanjutkan Node Berikutnya ➡️"):
        st.rerun()

# --- SCREEN 3: END OF THE GAME ---
else:
    st.header("🏁 CORE TERMINATED: RINGKASAN DATA PETUALANGAN")
    
    if st.session_state.lives > 0:
        st.balloons()
        st.success(f"🏆 SELAMAT! Anda Menembus Nexus! Level Akhir: {player_level} dengan Total {st.session_state.xp} XP!")
    else:
        st.error(f"💀 GAME OVER! Sistem Anda Mengalami Crash Akibat Kehabisan Nyawa Core. Skor Akhir: {st.session_state.xp} XP.")
    
    if st.button("Inisialisasi Ulang Simulasi 🔄"):
        st.session_state.game_started = False
        st.session_state.game_over = False
        st.session_state.xp = 0
        st.session_state.lives = 3
        st.session_state.current_question = 0
        st.session_state.wordle_feedback = ""
        st.rerun()