import streamlit as st
import pandas as pd
import os

# === CONFIGURATION ===
EXCEL_PATH = r"D:\OneDrive - Tata Power\High Registration Data\NITIN RANA\AI\data.xlsx"
MEMO_FOLDER = r"D:\OneDrive - Tata Power\High Registration Data\memos for OSMT\New folder (2)\2022-23\Oct 22 onwards"

# === UI ===
st.set_page_config(page_title="Meter Search Tool", layout="centered")
st.title("Meter Info Lookup & Memo Downloader")

meter_no = st.text_input("🔍 Enter Meter No.")

if meter_no:
    try:
        df = pd.read_excel(EXCEL_PATH, dtype=str)
        df.fillna("", inplace=True)

        matched = df[df['Meter No.'] == meter_no]

        if not matched.empty:
            row = matched.iloc[0]
            st.success("✅ Record Found")
            st.write("**SR Creation Date:**", row.get('SR Creation Date', 'Not Available'))
            st.write("**OSMT Request:**", row.get('OSMT Request', 'Not Available'))
            st.write("**Status:**", row.get('Status', 'Not Available'))

            # Check for memo
            memo_filename = f"{meter_no}.pdf"
            memo_path = os.path.join(MEMO_FOLDER, memo_filename)

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
        st.error(f"🚨 Error: {e}")

