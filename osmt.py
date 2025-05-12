import streamlit as st
import pandas as pd
import os

# === CONFIGURATION ===
ONEDRIVE_EXCEL_PATH = os.path.expanduser("~/OneDrive/YourFolderName/data.xlsx")  # Modify this
ONEDRIVE_MEMO_FOLDER = os.path.expanduser("~/OneDrive/YourFolderName/memos/")    # Modify this

# === UI ===
st.title("Meter Info and Memo Downloader")

meter_no = st.text_input("Enter Meter No.")

if meter_no:
    try:
        df = pd.read_excel(ONEDRIVE_EXCEL_PATH, dtype=str)
        df.fillna("", inplace=True)

        matched = df[df['Meter No.'] == meter_no]

        if not matched.empty:
            st.success("Record Found:")
            st.write("**SR Creation Date:**", matched.iloc[0]['SR Creation Date'])
            st.write("**OSMT Request:**", matched.iloc[0]['OSMT Request'])
            st.write("**Status:**", matched.iloc[0]['Status'])

            # Check for memo PDF
            memo_filename = f"{meter_no}.pdf"
            memo_path = os.path.join(ONEDRIVE_MEMO_FOLDER, memo_filename)

            if os.path.exists(memo_path):
                with open(memo_path, "rb") as f:
                    st.download_button(label="Download Memo PDF",
                                       data=f,
                                       file_name=memo_filename,
                                       mime="application/pdf")
            else:
                st.warning("Memo PDF not found for this Meter No.")
        else:
            st.error("Meter No. not found in data.")
    except Exception as e:
        st.error(f"Error reading data: {e}")
