import streamlit as st
import pandas as pd
import os

# === PATHS ===
EXCEL_DIR = r"D:\OneDrive - Tata Power\High Registration Data\NITIN RANA\AI"
MEMO_DIR = r"D:\OneDrive - Tata Power\High Registration Data\memos for OSMT\New folder (2)\2022-23\Oct 22 onwards"

# === FIND THE FIRST EXCEL FILE IN THE FOLDER ===
def find_excel_file(folder):
    for file in os.listdir(folder):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            return os.path.join(folder, file)
    return None

# === STREAMLIT UI ===
st.set_page_config(page_title="Meter Info Lookup", layout="centered")
st.title("🔎 Meter Search & Memo Downloader")

meter_no = st.text_input("Enter Meter No.").strip()

if meter_no:
    excel_path = find_excel_file(EXCEL_DIR)

    if not excel_path:
        st.error("❌ No Excel file found in the folder.")
    else:
        try:
            df = pd.read_excel(excel_path, dtype=str)
            df.fillna("", inplace=True)

            matched = df[df['Meter No.'] == meter_no]

            if not matched.empty:
                row = matched.iloc[0]
                st.success("✅ Record Found")
                st.write("**SR Creation Date:**", row.get('SR Creation Date', 'Not Available'))
                st.write("**OSMT Request:**", row.get('OSMT Request', 'Not Available'))
                st.write("**Status:**", row.get('Status', 'Not Available'))

                # Look for PDF
                memo_filename = f"{meter_no}.pdf"
                memo_path = os.path.join(MEMO_DIR, memo_filename)

                if os.path.exists(memo_path):
                    with open(memo_path, "rb") as f:
                        st.download_button("📄 Download Memo PDF",
                                           data=f,
                                           file_name=memo_filename,
                                           mime="application/pdf")
                else:
                    st.warning("⚠️ Memo PDF not found for this Meter No.")
            else:
                st.error("❌ Meter No. not found in data.")
        except Exception as e:
            st.error(f"🚨 Error reading Excel: {e}")


