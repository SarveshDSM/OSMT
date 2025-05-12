import streamlit as st
import pandas as pd
import os

# === SET YOUR LOCAL DESKTOP PATHS ===
EXCEL_DIR = r"E:\data.csv"  # Your Excel file path
MEMO_DIR = r"C:\Users\YourUsername\Desktop\MeterApp\memos"  # Your Memo folder path

# === Find the Excel file (this is adapted for your case) ===
def find_excel_file(file_path):
    if os.path.exists(file_path):
        return file_path
    return None

# === Streamlit UI ===
st.set_page_config(page_title="Meter No. Lookup", layout="centered")
st.title("🔎 Meter Info & Memo Downloader")

meter_no = st.text_input("Enter Meter No.").strip()

if meter_no:
    excel_path = find_excel_file(EXCEL_DIR)

    if not excel_path or not os.path.exists(excel_path):
        st.error(f"❌ Excel file not found in: {EXCEL_DIR}")
    else:
        try:
            # Read the Excel file
            df = pd.read_excel(excel_path, dtype=str)
            df.fillna("", inplace=True)

            # Find the row matching the entered Meter No.
            matched = df[df['Meter No.'] == meter_no]

            if not matched.empty:
                row = matched.iloc[0]
                st.success("✅ Record Found")
                st.write("**SR Creation Date:**", row.get('SR Creation Date', 'N/A'))
                st.write("**OSMT Request:**", row.get('OSMT Request', 'N/A'))
                st.write("**Status:**", row.get('Status', 'N/A'))

                # Check for corresponding memo PDF
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
                st.error("❌ Meter No. not found in the Excel data.")
        except Exception as e:
            st.error(f"🚨 Error reading Excel file: {e}")


