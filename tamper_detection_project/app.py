import streamlit as st
import os
import mimetypes
from PIL import Image

from chunking import chunk_file
from image_processing import image_blocks
from video_processing import extract_frames
from audio_processing import extract_audio_segments

from video_timeline import build_video_timeline
from audio_timeline import build_audio_timeline

from hashing import select_hash, hash_chunk
from merkle import build_merkle_tree, get_merkle_root
from merkle_proof import generate_merkle_proof
from tamper_detection import detect_tampering
from visualization import visualize_tree

from image_visualization import highlight_tampered_blocks
from video_visualization import get_frame
from report_generator import generate_report

Image.MAX_IMAGE_PIXELS = None

st.set_page_config(
    page_title="Merkle Tamper Detection",
    page_icon="🔐",
    layout="wide"
)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("🔐 Merkle Tamper Detection")

    st.write("""
Detect **partial tampering** in multimedia files using:

• Adaptive hashing  
• Merkle tree verification  
• Image block analysis  
• Video frame verification  
• Audio segment hashing  
""")

    st.write("Developed by Sheena")


# ---------------- HEADER ---------------- #

st.title("🔐 Evidence-Grade Tamper Detection System")


# ---------------- ORIGINAL FILE ---------------- #

st.header("Upload Original File")

uploaded_file = st.file_uploader("Upload original file")

if uploaded_file:

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("File uploaded successfully")

    file_type, _ = mimetypes.guess_type(file_path)

    st.write("Detected Type:", file_type)

    algo = select_hash(file_type)

    st.write("Hash Algorithm:", algo)

    if file_type and "image" in file_type:

        chunks = image_blocks(file_path)
        st.image(file_path, caption="Uploaded Image", use_container_width=True)

    elif file_type and "video" in file_type:

        chunks = extract_frames(file_path)
        st.video(file_path)

    elif file_type and "audio" in file_type:

        chunks = extract_audio_segments(file_path)
        st.audio(file_path)

    else:

        chunks = chunk_file(file_path, chunk_size=262144)

    st.write("Chunks Created:", len(chunks))

    hashes = [hash_chunk(c, algo) for c in chunks]

    tree = build_merkle_tree(hashes)
    root = get_merkle_root(tree)

    st.subheader("Merkle Root")
    st.code(root)

    st.subheader("Merkle Tree")

    fig = visualize_tree(tree)
    st.pyplot(fig)

    st.subheader("Merkle Tree Stats")

    st.write("Total Chunks:", len(chunks))
    st.write("Tree Levels:", len(tree))
    st.write("Leaf Nodes:", len(tree[0]))

    st.session_state.original_hashes = hashes
    st.session_state.algo = algo
    st.session_state.file_type = file_type
    st.session_state.tree = tree
    st.session_state.root = root


# ---------------- VERIFY FILE ---------------- #

st.header("Verify File for Tampering")

verify_file = st.file_uploader("Upload file to verify")

if verify_file and "original_hashes" in st.session_state:

    verify_path = os.path.join(UPLOAD_FOLDER, verify_file.name)

    with open(verify_path, "wb") as f:
        f.write(verify_file.read())

    file_type = st.session_state.file_type
    algo = st.session_state.algo

    if file_type and "image" in file_type:
        new_chunks = image_blocks(verify_path)

    elif file_type and "video" in file_type:
        new_chunks = extract_frames(verify_path)

    elif file_type and "audio" in file_type:
        new_chunks = extract_audio_segments(verify_path)

    else:
        new_chunks = chunk_file(verify_path, chunk_size=262144)

    st.write("Original hashes:", len(st.session_state.original_hashes))
    st.write("New hashes:", len(new_chunks))

    modified = detect_tampering(
        st.session_state.original_hashes,
        new_chunks,
        algo
    )

    if len(modified) == 0:

        st.success("File integrity verified — NOT tampered")

    else:

        st.error("Tampering detected")
        st.write("Modified segments:", modified)

    # ---------------- IMAGE HEATMAP ---------------- #

    if file_type and "image" in file_type and len(modified) > 0:

        st.subheader("Tampered Area")

        heatmap = highlight_tampered_blocks(verify_path, modified)
        st.image(heatmap, use_container_width=True)

    # ---------------- VIDEO FRAMES ---------------- #

    if file_type and "video" in file_type and len(modified) > 0:

        st.subheader("Tampered Frames")

        for frame_no in modified[:5]:

            frame = get_frame(verify_path, frame_no)

            if frame is not None:
                st.image(frame, caption=f"Frame {frame_no}")

    # ---------------- VIDEO TIMELINE ---------------- #

    if file_type and "video" in file_type:

        st.subheader("Video Tamper Timeline")

        timeline = build_video_timeline(len(new_chunks), modified)

        for frame, status in timeline[:100]:

            if status == "OK":
                st.write(f"Frame {frame} ✓ OK")
            else:
                st.write(f"Frame {frame} ❌ TAMPERED")

    # ---------------- AUDIO TIMELINE ---------------- #

    if file_type and "audio" in file_type:

        st.subheader("Audio Tamper Timeline")

        timeline = build_audio_timeline(len(new_chunks), modified)

        for sec, status in timeline[:120]:

            if status == "OK":
                st.write(f"Second {sec} ✓ OK")
            else:
                st.write(f"Second {sec} ❌ TAMPERED")

    # ---------------- MERKLE PROOF ---------------- #

    tree = st.session_state.tree

    proof = generate_merkle_proof(tree, 0)

    st.subheader("Merkle Proof Example (Block 0)")
    st.write(proof)

    # ---------------- EVIDENCE REPORT ---------------- #

    report = generate_report(
        verify_file.name,
        algo,
        st.session_state.root,
        "NOT TAMPERED" if len(modified)==0 else "TAMPERED",
        proof
    )

    with open(report, "rb") as f:

        st.download_button(
            "Download Evidence Report",
            f,
            file_name="evidence_report.pdf"
        )