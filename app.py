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

# Callback function for data editor to instantly autosave changes into session state
def update_data_callback():
    edited_changes = st.session_state.get("data_editor", None)
    if edited_changes is not None:
        # Handle added rows
        if "added_rows" in edited_changes and edited_changes["added_rows"]:
            for new_row in edited_changes["added_rows"]:
                # Ensure default values if empty
                if not new_row.get("Date"):
                    new_row["Date"] = date.today()
                if not new_row.get("Item"):
                    new_row["Item"] = "New Item"
                if new_row.get("Sl No") is None or pd.isna(new_row.get("Sl No")):
                    max_sl = st.session_state.items_df["Sl No"].max() if len(st.session_state.items_df) > 0 else 0
                    new_row["Sl No"] = int(max_sl) + 1
                st.session_state.items_df = pd.concat([st.session_state.items_df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Handle edited rows
        if "edited_rows" in edited_changes and edited_changes["edited_rows"]:
            for idx_str, changes in edited_changes["edited_rows"].items():
                idx = int(idx_str)
                for col, val in changes.items():
                    if idx < len(st.session_state.items_df):
                        st.session_state.items_df.at[idx, col] = val

        # Handle deleted rows
        if "deleted_rows" in edited_changes and edited_changes["deleted_rows"]:
            st.session_state.items_df = st.session_state.items_df.drop(edited_changes["deleted_rows"]).reset_index(drop=True)

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

# Main Layout: Editable Data Editor with Autosave Callback
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
    key="data_editor",
    on_change=update_data_callback
)

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
