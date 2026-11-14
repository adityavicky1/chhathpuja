import streamlit as st
import pandas as pd
from datetime import date

# Set page configuration
st.set_page_config(
    page_title="Item List & Amount Calculator",
    page_icon="📋",
    layout="wide"
)

# Initialize Session State for items if not already present
if "items_df" not in st.session_state:
    initial_data = [
        {"Sl No": 1, "Date": date.today(), "Item": "Apple", "Qty": 5.0, "UOM": "kg", "Rate": 120.0},
        {"Sl No": 2, "Date": date.today(), "Item": "Banana", "Qty": 2.0, "UOM": "dozen", "Rate": 50.0},
        {"Sl No": 3, "Date": date.today(), "Item": "Orange", "Qty": 30.0, "UOM": "pcs", "Rate": 10.0},
        {"Sl No": 4, "Date": date.today(), "Item": "Sweet Potato", "Qty": 4.0, "UOM": "kg", "Rate": 40.0},
        {"Sl No": 5, "Date": date.today(), "Item": "Radish", "Qty": 30.0, "UOM": "pcs", "Rate": 8.0},
        {"Sl No": 6, "Date": date.today(), "Item": "Turmeric", "Qty": 30.0, "UOM": "pcs", "Rate": 15.0},
        {"Sl No": 7, "Date": date.today(), "Item": "Ginger", "Qty": 30.0, "UOM": "pcs", "Rate": 20.0},
        {"Sl No": 8, "Date": date.today(), "Item": "Sugarcane", "Qty": 30.0, "UOM": "pcs", "Rate": 25.0},
        {"Sl No": 9, "Date": date.today(), "Item": "Coconut", "Qty": 4.0, "UOM": "pcs", "Rate": 30.0},
        {"Sl No": 10, "Date": date.today(), "Item": "Mahua", "Qty": 14.0, "UOM": "pcs", "Rate": 12.0},
        {"Sl No": 11, "Date": date.today(), "Item": "Guava", "Qty": 14.0, "UOM": "pcs", "Rate": 15.0},
        {"Sl No": 12, "Date": date.today(), "Item": "Water Chestnut", "Qty": 2.5, "UOM": "kg", "Rate": 60.0},
    ]
    st.session_state.items_df = pd.DataFrame(initial_data)

# App Header
st.title("📋 Inventory & Todo Item Ledger")
st.markdown("Manage your item list with auto-calculated amounts (`Qty × Rate`). Changes autosave immediately.")

# Sidebar Controls & Grand Total Display
with st.sidebar:
    st.header("📊 Summary & Actions")
    
    # Calculate amounts from current session state
    calc_df = st.session_state.items_df.copy()
    calc_df["Amount"] = pd.to_numeric(calc_df["Qty"], errors='coerce').fillna(0) * pd.to_numeric(calc_df["Rate"], errors='coerce').fillna(0)
    grand_total = calc_df["Amount"].sum()
    total_qty = pd.to_numeric(calc_df["Qty"], errors='coerce').fillna(0).sum()
    
    st.metric(label="Grand Total Amount", value=f"₹{grand_total:,.2f}")
    st.metric(label="Total Items Count", value=len(calc_df))
    st.metric(label="Total Quantity", value=f"{total_qty:,.2f}")
    
    st.divider()
    
    if st.button("🔄 Reset to Default List", use_container_width=True):
        st.session_state.items_df = pd.DataFrame([
            {"Sl No": 1, "Date": date.today(), "Item": "Apple", "Qty": 5.0, "UOM": "kg", "Rate": 120.0},
            {"Sl No": 2, "Date": date.today(), "Item": "Banana", "Qty": 2.0, "UOM": "dozen", "Rate": 50.0},
            {"Sl No": 3, "Date": date.today(), "Item": "Orange", "Qty": 30.0, "UOM": "pcs", "Rate": 10.0},
            {"Sl No": 4, "Date": date.today(), "Item": "Sweet Potato", "Qty": 4.0, "UOM": "kg", "Rate": 40.0},
            {"Sl No": 5, "Date": date.today(), "Item": "Radish", "Qty": 30.0, "UOM": "pcs", "Rate": 8.0},
            {"Sl No": 6, "Date": date.today(), "Item": "Turmeric", "Qty": 30.0, "UOM": "pcs", "Rate": 15.0},
            {"Sl No": 7, "Date": date.today(), "Item": "Ginger", "Qty": 30.0, "UOM": "pcs", "Rate": 20.0},
            {"Sl No": 8, "Date": date.today(), "Item": "Sugarcane", "Qty": 30.0, "UOM": "pcs", "Rate": 25.0},
            {"Sl No": 9, "Date": date.today(), "Item": "Coconut", "Qty": 4.0, "UOM": "pcs", "Rate": 30.0},
            {"Sl No": 10, "Date": date.today(), "Item": "Mahua", "Qty": 14.0, "UOM": "pcs", "Rate": 12.0},
            {"Sl No": 11, "Date": date.today(), "Item": "Guava", "Qty": 14.0, "UOM": "pcs", "Rate": 15.0},
            {"Sl No": 12, "Date": date.today(), "Item": "Water Chestnut", "Qty": 2.5, "UOM": "kg", "Rate": 60.0},
        ])
        st.rerun()

    st.markdown("### 🚀 Streamlit Deployment")
    st.markdown("""
    To deploy on Streamlit Community Cloud:
    1. Create a GitHub repo with `app.py` and `requirements.txt`:
       ```text
       streamlit
       pandas
       ```
    2. Deploy at [share.streamlit.io](https://share.streamlit.io)!
    """)

# Main Layout: Editable Data Editor storing back directly into session_state
st.subheader("Item Entries Editor")
st.markdown("Type directly into the table cells below. Changes are saved automatically upon clicking away or pressing Enter.")

edited_df = st.data_editor(
    st.session_state.items_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Sl No": st.column_config.NumberColumn("Sl No", format="%d", width="small"),
        "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
        "Item": st.column_config.TextColumn("Item Description", required=True),
        "Qty": st.column_config.NumberColumn("Qty", min_value=0.0, format="%.2f"),
        "UOM": st.column_config.TextColumn("UOM (kg, pcs...)"),
        "Rate": st.column_config.NumberColumn("Rate (₹)", min_value=0.0, format="₹%.2f")
    },
    key="data_editor"
)

# Update session state with the editor result so edits persist immediately
if not edited_df.equals(st.session_state.items_df):
    st.session_state.items_df = edited_df.copy()
    st.rerun()

# Calculate Amount column dynamically for display table
display_df = st.session_state.items_df.copy()
display_df["Qty"] = pd.to_numeric(display_df["Qty"], errors='coerce').fillna(0)
display_df["Rate"] = pd.to_numeric(display_df["Rate"], errors='coerce').fillna(0)
display_df["Amount"] = display_df["Qty"] * display_df["Rate"]

# Display Calculated Table with Amount Column
st.markdown("### Calculated Ledger View (Live)")
st.dataframe(
    display_df.style.format({
        "Qty": "{:,.2f}",
        "Rate": "₹{:,.2f}",
        "Amount": "₹{:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

# Bottom Grand Total Banner
st.success(f"### Grand Total Amount: ₹{display_df['Amount'].sum():,.2f}")
