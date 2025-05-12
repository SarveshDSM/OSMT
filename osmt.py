import streamlit as st
import pandas as pd
import os

# === CONFIGURATION ===
CSV_PATH = "data.csv"  # This assumes data.csv is in the same folder as app.py
MEMO_FOLDER = r"E:\data\memos"  # Optional folder for PDF memos

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

                # Optional: PDF download
                if MEMO_FOLDER:
                    memo_filename = f"{meter_no}.pdf"
                    memo_path = os.path.join(MEMO_FOLDER, memo_filename)

                    if os.path.exists(memo_path):
                        with open(memo_path, "rb") as f:
                            st.download_button("📄 Download Memo PDF",
                                               data=f,
                                               file_name=memo_filename,
                                               mime="application/pdf")
                    else:
                        st.warning("⚠️ Memo PDF not found in local folder.")
            else:
                st.error("❌ Meter No. not found in the data.")
    except Exception as e:
        st.error(f"🚨 Error reading CSV file: {e}")




