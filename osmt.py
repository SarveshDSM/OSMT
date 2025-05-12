import streamlit as st
import pandas as pd
import os

# === CONFIGURATION ===
CSV_PATH = "data.csv"         # CSV should be in the same folder as app.py
PDF_FOLDER = "C:\\"           # PDFs are stored in the E drive, named by Meter No.

# === Streamlit UI ===
st.set_page_config(page_title="Meter No. Lookup", layout="centered")
st.title("🔎 Meter Info & Memo Downloader")

meter_no = st.text_input("Enter Meter No.").strip()

if meter_no:
    try:
        # Load local CSV
        df = pd.read_csv(CSV_PATH, dtype=str)
        df.fillna("", inplace=True)

        if 'Meter No.' not in df.columns:
            st.error("❌ 'Meter No.' column not found in the CSV file.")
        else:
            matched = df[df['Meter No.'] == meter_no]

            if not matched.empty:
                row = matched.iloc[0]
                st.success("✅ Record Found")
                st.write("**SR Creation Date:**", row.get('SR Creation Date', 'N/A'))
                st.write("**OSMT Request:**", row.get('OSMT Request', 'N/A'))
                st.write("**Status:**", row.get('Status', 'N/A'))

                # Debug: Check what file path we are looking for
                memo_path = os.path.join(PDF_FOLDER, f"{meter_no}.pdf")
                st.write("🔍 Looking for file:", memo_path)

                # Optional: List all files in E:\ drive for visual confirmation
                try:
                    all_files = os.listdir(PDF_FOLDER)
                    st.write("📁 Files in E:\\:", all_files)
                except Exception as e:
                    st.error(f"❌ Error listing E:\\: {e}")

                # Check if PDF exists at E:\<meter_no>.pdf
                if os.path.exists(memo_path):
                    with open(memo_path, "rb") as f:
                        st.download_button("📄 Download Memo PDF",
                                           data=f,
                                           file_name=f"{meter_no}.pdf",
                                           mime="application/pdf")
                else:
                    st.warning("⚠️ Memo PDF not found in E drive.")
            else:
                st.error("❌ Meter No. not found in the data.")
    except Exception as e:
        st.error(f"🚨 Error reading CSV file: {e}")






