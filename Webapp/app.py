import streamlit as st
import os
from generator import generate_html_from_csv

# --- Page Setup ---
st.set_page_config(page_title="Gig Grid Generator", page_icon="📅")

st.title("📅 Gig Grid HTML Generator")
st.info("Upload your CSV and I'll generate the HTML for your email or website.")

# --- 1. File Upload ---
uploaded_file = st.file_uploader("Drop your CSV file here", type="csv")

if uploaded_file:
    # We save the file temporarily so your generator.py can "open" it via path
    temp_filename = "temp_upload.csv"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # --- 2. Generation Logic ---
    if st.button("Generate HTML", type="primary"):
        try:
            # Your generator.py doing the heavy lifting:
            html_output = generate_html_from_csv(temp_filename)
            
            st.success("Successfully Generated!")

            # --- 3. Preview and Copy ---
            # st.code provides a built-in copy button in the top right!
            st.subheader("HTML Code")
            st.code(html_output, language="html")

            # --- 4. Download ---
            st.download_button(
                label="📥 Download .html File",
                data=html_output,
                file_name="gig_block.html",
                mime="text/html"
            )
            
            # Cleanup the temp file
            os.remove(temp_filename)

        except ValueError as e:
            st.error(f"Data Error: {e}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

else:
    st.write("Waiting for a CSV file...")