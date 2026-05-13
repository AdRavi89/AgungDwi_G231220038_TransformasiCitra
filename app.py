import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="CV Pipeline - Local Mode", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'raw_images' not in st.session_state:
    st.session_state.raw_images = []
if 'gray_images' not in st.session_state:
    st.session_state.gray_images = []

# --- FUNGSI HELPER LOKAL ---
def load_local_images(folder_path):
    imgs = []
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    if not os.path.exists(folder_path):
        st.error(f"Folder '{folder_path}' tidak ditemukan!")
        return []

    # Mengambil list file dan filter hanya gambar
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
    
    if len(files) == 0:
        st.warning(f"Tidak ada gambar di dalam folder '{folder_path}'")
        return []

    # Ambil maksimal 25 gambar
    files = files[:25]
    
    for file_name in files:
        img_path = os.path.join(folder_path, file_name)
        # Baca gambar menggunakan OpenCV
        img = cv2.imread(img_path)
        if img is not None:
            imgs.append(img)
            
    return imgs

# --- UI SIDEBAR ---
with st.sidebar:
    st.header("Step 1: Load Data Lokal")
    folder_input = st.text_input("Nama Folder Gambar", value="images")
    st.info("Pastikan folder ini ada di direktori proyek Anda.")
    
    if st.button("📥 Load 25 Gambar dari Folder"):
        with st.spinner("Membaca file lokal..."):
            st.session_state.raw_images = load_local_images(folder_input)
            st.session_state.gray_images = [] # Reset grayscale
            if st.session_state.raw_images:
                st.success(f"Berhasil memuat {len(st.session_state.raw_images)} gambar.")

# --- MAIN CONTENT ---
st.title("🛠️ Computer Vision Pipeline: Transformasi Geometris (Local)")

# 1. DISPLAY ORIGINAL
if st.session_state.raw_images:
    st.subheader("1. Hasil Load Folder (Original RGB)")
    cols = st.columns(5)
    for idx, img in enumerate(st.session_state.raw_images):
        cols[idx % 5].image(img, channels="BGR", use_container_width=True, caption=f"Original {idx+1}")

    st.divider()
    st.header("Step 2: Pre-processing")
    if st.button("✨ Klik Ubah ke Grayscale"):
        st.session_state.gray_images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in st.session_state.raw_images]

# 2. DISPLAY GRAYSCALE & TRANSFORMASI
if st.session_state.gray_images:
    st.subheader("2. Hasil Grayscale (Frame Tersendiri)")
    cols_g = st.columns(5)
    for idx, img in enumerate(st.session_state.gray_images):
        cols_g[idx % 5].image(img, use_container_width=True, caption=f"Grayscale {idx+1}")

    st.divider()
    st.header("Step 3: Function Transformasi Geometris Citra")
    
    tabs = st.tabs([
        "Translasi", "Rotasi", "Scaling", "Shearing", 
        "Refleksi", "Affine", "Proyektif"
    ])

    def render_transformation(images, matrix, description):
        st.markdown(f"### Detail Transformasi")
        col_text, col_mat = st.columns([2, 1])
        with col_text:
            st.info(description)
        with col_mat:
            if matrix is not None:
                st.write("**Matriks Transformasi ($M$):**")
                st.code(matrix)
        
        st.write("**Hasil Visual:**")
        grid = st.columns(5)
        for i, im in enumerate(images):
            grid[i % 5].image(im, use_container_width=True, caption=f"Hasil {i+1}")

    # IMPLEMENTASI TIAP TAB
    with tabs[0]: # Translasi
        M = np.float32([[1, 0, 50], [0, 1, 30]])
        res = [cv2.warpAffine(img, M, (img.shape[1], img.shape[0])) for img in st.session_state.gray_images]
        render_transformation(res, M, "Menggeser citra secara horizontal (tx=50) dan vertikal (ty=30).")

    with tabs[1]: # Rotasi
        rows, cols = st.session_state.gray_images[0].shape
        M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
        res = [cv2.warpAffine(img, M, (cols, rows)) for img in st.session_state.gray_images]
        render_transformation(res, M, "Memutar citra sebesar 45 derajat terhadap titik pusat.")

    with tabs[2]: # Scaling
        res = [cv2.resize(img, None, fx=0.7, fy=0.7) for img in st.session_state.gray_images]
        render_transformation(res, None, "Mengecilkan citra menjadi 70% dari ukuran aslinya.")

    with tabs[3]: # Shearing
        M = np.float32([[1, 0.2, 0], [0, 1, 0]])
        res = [cv2.warpAffine(img, M, (int(img.shape[1]*1.2), img.shape[0])) for img in st.session_state.gray_images]
        render_transformation(res, M, "Memberikan efek kemiringan (skew) pada sumbu horizontal.")

    with tabs[4]: # Refleksi
        res = [cv2.flip(img, 1) for img in st.session_state.gray_images]
        render_transformation(res, None, "Mencerminkan citra secara horizontal (sumbu Y).")

    with tabs[5]: # Affine
        pts1 = np.float32([[50,50],[200,50],[50,200]])
        pts2 = np.float32([[10,100],[200,50],[100,250]])
        M = cv2.getAffineTransform(pts1,pts2)
        res = [cv2.warpAffine(img, M, (img.shape[1], img.shape[0])) for img in st.session_state.gray_images]
        render_transformation(res, M, "Transformasi linier yang menjaga garis sejajar tetap sejajar.")

    with tabs[6]: # Proyektif
        pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
        pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
        M = cv2.getPerspectiveTransform(pts1,pts2)
        res = [cv2.warpPerspective(img, M, (300,300)) for img in st.session_state.gray_images]
        render_transformation(res, M, "Transformasi perspektif untuk mengubah sudut pandang (3D mapping).")