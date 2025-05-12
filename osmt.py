import streamlit as st
import pandas as pd
import os

# === CONFIGURATION ===
CSV_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/data.csv"  # ← Replace with your actual GitHub raw CSV URL
MEMO_FOLDER = r"E:\data\memos"  # ← Optional local folder for memo PDFs (update or leave blank if not used)

# === Streamlit UI ===
st.set_page_config(page_title="Meter No. Lookup", layout="centered")
st.title("🔎 Meter Info & Memo Downloader")

st.markdown("Enter a Meter Number to search its details from the CSV stored on GitHub.")

meter_no = st.text_input("Enter Meter No.").strip()

if meter_no:
    try:
        # Read CSV file directly from GitHub
        df = pd.read_csv(CSV_URL, dtype=str)
        df.fillna("", inplace=True)

        # Validate column
        if 'Meter No.' not in df.columns:
            st.error("❌ 'Meter No.' column not found in the CSV file.")
        else:
            # Filter for matching Meter No.
            matched = df[df['Meter No.'] == meter_no]

            if not matched.empty:
                row = matched.iloc[0]
                st.success("✅ Record Found")
                st.write("**SR Creation Date:**", row.get('SR Creation Date', 'N/A'))
                st.write("**OSMT Request:**", row.get('OSMT Request', 'N/A'))
                st.write("**Status:**", row.get('Status', 'N/A'))

                # Check for memo PDF (optional)
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
                        st.warning("⚠️ Memo PDF not found for this Meter No. in local folder.")
            else:
                st.error("❌ Meter No. not found in the data.")
    except Exception as e:
        st.error(f"🚨 Error reading CSV file: {e}")




