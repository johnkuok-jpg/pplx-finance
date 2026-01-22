#!/usr/bin/env python3
"""
Streamlit Web App for Modifying Invoice Banking Information
"""
import streamlit as st
import fitz  # PyMuPDF
import io

def modify_invoice_pdf(pdf_bytes, bank_info):
    """
    Modify the invoice PDF by replacing banking information

    Args:
        pdf_bytes: PDF file as bytes
        bank_info: Dictionary with new banking information

    Returns:
        Modified PDF as bytes
    """
    # Open the PDF from bytes
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    # Search for "Bank name" across all pages
    bank_name_rect = None
    target_page = None

    for page_num in range(len(doc)):
        page = doc[page_num]
        bank_name_search = page.search_for("Bank name")

        if bank_name_search:
            # Found "Bank name" on this page
            # Try to find it in the lower part of the page (y > 600)
            # or just use the first occurrence if none in lower part
            for rect in bank_name_search:
                if rect.y0 > 600:
                    bank_name_rect = rect
                    target_page = page
                    break

            # If we didn't find it in lower part, use first occurrence
            if not bank_name_rect and bank_name_search:
                bank_name_rect = bank_name_search[0]
                target_page = page
                break

    if not bank_name_rect or not target_page:
        return None, "Could not find 'Bank name' in the PDF"

    page = target_page

    # Delete from slightly above the Bank name line to catch all old text
    delete_from_y = bank_name_rect.y0 - 5
    page_height = page.rect.height
    deletion_rect = fitz.Rect(35, delete_from_y, 450, page_height - 20)

    # Add redaction and apply
    page.add_redact_annot(deletion_rect, fill=(1, 1, 1))
    page.apply_redactions()

    # Add new banking information
    y_start = delete_from_y + 12
    x_label = 34
    x_value = 152
    line_height = 12.5
    fontsize = 9
    fontname = "helv"

    # Create list of bank info to add
    bank_info_list = [
        ("Bank name", bank_info["bank_name"]),
        ("Account Name", bank_info["account_name"]),
        ("Account Type", bank_info["account_type"]),
        ("ACH Routing/ABA", bank_info["routing_number"]),
        ("Acct #", bank_info["account_number"]),
        ("Swift/IBAN", bank_info["swift_code"])
    ]

    # Insert new text
    y_pos = y_start
    for label, value in bank_info_list:
        if value:  # Only add if value is provided
            page.insert_text(
                (x_label, y_pos),
                label,
                fontsize=fontsize,
                fontname=fontname,
                color=(0, 0, 0)
            )
            page.insert_text(
                (x_value, y_pos),
                value,
                fontsize=fontsize,
                fontname=fontname,
                color=(0, 0, 0)
            )
            y_pos += line_height

    # Save to bytes
    output_bytes = io.BytesIO()
    doc.save(output_bytes, garbage=4, deflate=True, clean=True)
    doc.close()

    output_bytes.seek(0)
    return output_bytes.getvalue(), None


# Streamlit App
def main():
    st.set_page_config(
        page_title="Invoice Banking Info Updater",
        page_icon="💳",
        layout="centered"
    )

    st.title("💳 Invoice Banking Information Updater")
    st.markdown("Upload a Stripe-formatted invoice PDF and update the banking details")

    # File uploader
    uploaded_file = st.file_uploader(
        "Drag and drop your invoice PDF here",
        type=['pdf'],
        help="Upload a Stripe invoice PDF to modify"
    )

    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")

        # Create two columns for input fields
        st.subheader("Enter New Banking Information")

        col1, col2 = st.columns(2)

        with col1:
            bank_name = st.text_input("Bank Name", value="Silicon Valley Bank")
            account_name = st.text_input("Account Name", value="Perplexity AI, Inc.")
            account_type = st.text_input("Account Type", value="Checking")

        with col2:
            routing_number = st.text_input("ACH Routing/ABA", value="121140399")
            account_number = st.text_input("Account Number", value="3304334669")
            swift_code = st.text_input("Swift/IBAN", value="SVBKUS6S")

        # Update button
        if st.button("🔄 Update Invoice", type="primary", use_container_width=True):
            if not account_name or not account_number:
                st.error("Please fill in at least Account Name and Account Number")
            else:
                with st.spinner("Modifying invoice..."):
                    # Read the uploaded PDF
                    pdf_bytes = uploaded_file.read()

                    # Prepare bank info dictionary
                    bank_info = {
                        "bank_name": bank_name,
                        "account_name": account_name,
                        "account_type": account_type,
                        "routing_number": routing_number,
                        "account_number": account_number,
                        "swift_code": swift_code
                    }

                    # Modify the PDF
                    modified_pdf, error = modify_invoice_pdf(pdf_bytes, bank_info)

                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.success("✅ Invoice updated successfully!")

                        # Generate download filename
                        original_name = uploaded_file.name.replace('.pdf', '')
                        download_name = f"{original_name}-Modified.pdf"

                        # Download button
                        st.download_button(
                            label="📥 Download Modified Invoice",
                            data=modified_pdf,
                            file_name=download_name,
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )

    else:
        st.info("👆 Upload a PDF invoice to get started")

    # Instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        ### Instructions
        1. **Upload** your Stripe invoice PDF using the file uploader above
        2. **Enter** the new banking information in the form fields
        3. **Click** the "Update Invoice" button
        4. **Download** your modified invoice

        ### Requirements
        - The PDF must be a Stripe-formatted invoice
        - The PDF must contain a "Bank name" section in the banking details
        - All old banking information will be removed and replaced with your new details

        ### Privacy
        - All processing happens in your browser session
        - Files are not stored on any server
        - Your data is never saved or transmitted
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>Built with Streamlit | "
        "Secure & Private</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
