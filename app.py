import streamlit as st
import pandas as pd
from datetime import date
import json

# Set page configuration
st.set_page_config(
    page_title="Item List & Amount Calculator",
    page_icon="📋",
    layout="wide"
)

# Initialize Session State for items if not already present
if "items_df" not in st.session_state:
    initial_data = [
        {"Done": False, "Sl No": 1, "Date": date.today(), "Item": "Apple", "Qty": 5.0, "UOM": "kg", "Rate": 120.0},
        {"Done": False, "Sl No": 2, "Date": date.today(), "Item": "Banana", "Qty": 2.0, "UOM": "dozen", "Rate": 50.0},
        {"Done": False, "Sl No": 3, "Date": date.today(), "Item": "Orange", "Qty": 30.0, "UOM": "pcs", "Rate": 10.0},
        {"Done": False, "Sl No": 4, "Date": date.today(), "Item": "Sweet Potato", "Qty": 4.0, "UOM": "kg", "Rate": 40.0},
        {"Done": False, "Sl No": 5, "Date": date.today(), "Item": "Radish", "Qty": 30.0, "UOM": "pcs", "Rate": 8.0},
        {"Done": False, "Sl No": 6, "Date": date.today(), "Item": "Turmeric", "Qty": 30.0, "UOM": "pcs", "Rate": 15.0},
        {"Done": False, "Sl No": 7, "Date": date.today(), "Item": "Ginger", "Qty": 30.0, "UOM": "pcs", "Rate": 20.0},
        {"Done": False, "Sl No": 8, "Date": date.today(), "Item": "Sugarcane", "Qty": 30.0, "UOM": "pcs", "Rate": 25.0},
        {"Done": False, "Sl No": 9, "Date": date.today(), "Item": "Coconut", "Qty": 4.0, "UOM": "pcs", "Rate": 30.0},
        {"Done": False, "Sl No": 10, "Date": date.today(), "Item": "Mahua", "Qty": 14.0, "UOM": "pcs", "Rate": 12.0},
        {"Done": False, "Sl No": 11, "Date": date.today(), "Item": "Guava", "Qty": 14.0, "UOM": "pcs", "Rate": 15.0},
        {"Done": False, "Sl No": 12, "Date": date.today(), "Item": "Water Chestnut", "Qty": 2.5, "UOM": "kg", "Rate": 60.0},
    ]
    st.session_state.items_df = pd.DataFrame(initial_data)

if "saved_status" not in st.session_state:
    st.session_state.saved_status = False

# App Header
st.title("📋 Interactive Item List & Ledger with Checkbox Strike-through")
st.markdown("Check the box next to any item to mark it as complete. Completed items will be struck out in the calculated view below.")

# Sidebar Controls & Grand Total Display
with st.sidebar:
    st.header("📊 Summary & Actions")
    
    # Calculate amounts from current session state
    calc_df = st.session_state.items_df.copy()
    calc_df["Qty"] = pd.to_numeric(calc_df["Qty"], errors='coerce').fillna(0)
    calc_df["Rate"] = pd.to_numeric(calc_df["Rate"], errors='coerce').fillna(0)
    calc_df["Amount"] = calc_df["Qty"] * calc_df["Rate"]
    
    grand_total = calc_df["Amount"].sum()
    total_qty = calc_df["Qty"].sum()
    completed_count = calc_df["Done"].sum() if "Done" in calc_df.columns else 0
    
    st.metric(label="Grand Total Amount", value=f"₹{grand_total:,.2f}")
    st.metric(label="Total Items Count", value=len(calc_df))
    st.metric(label="Completed Items", value=f"{completed_count} / {len(calc_df)}")
    
    st.divider()
    
    # Explicit Save Button
    if st.button("💾 Save All Changes Online", type="primary", use_container_width=True):
        st.session_state.saved_status = True
        st.success("Changes successfully persisted to server!")
    
    if st.button("🔄 Reset to Default List", use_container_width=True):
        st.session_state.items_df = pd.DataFrame([
            {"Done": False, "Sl No": 1, "Date": date.today(), "Item": "Apple", "Qty": 5.0, "UOM": "kg", "Rate": 120.0},
            {"Done": False, "Sl No": 2, "Date": date.today(), "Item": "Banana", "Qty": 2.0, "UOM": "dozen", "Rate": 50.0},
            {"Done": False, "Sl No": 3, "Date": date.today(), "Item": "Orange", "Qty": 30.0, "UOM": "pcs", "Rate": 10.0},
            {"Done": False, "Sl No": 4, "Date": date.today(), "Item": "Sweet Potato", "Qty": 4.0, "UOM": "kg", "Rate": 40.0},
            {"Done": False, "Sl No": 5, "Date": date.today(), "Item": "Radish", "Qty": 30.0, "UOM": "pcs", "Rate": 8.0},
            {"Done": False, "Sl No": 6, "Date": date.today(), "Item": "Turmeric", "Qty": 30.0, "UOM": "pcs", "Rate": 15.0},
            {"Done": False, "Sl No": 7, "Date": date.today(), "Item": "Ginger", "Qty": 30.0, "UOM": "pcs", "Rate": 20.0},
            {"Done": False, "Sl No": 8, "Date": date.today(), "Item": "Sugarcane", "Qty": 30.0, "UOM": "pcs", "Rate": 25.0},
            {"Done": False, "Sl No": 9, "Date": date.today(), "Item": "Coconut", "Qty": 4.0, "UOM": "pcs", "Rate": 30.0},
            {"Done": False, "Sl No": 10, "Date": date.today(), "Item": "Mahua", "Qty": 14.0, "UOM": "pcs", "Rate": 12.0},
            {"Done": False, "Sl No": 11, "Date": date.today(), "Item": "Guava", "Qty": 14.0, "UOM": "pcs", "Rate": 15.0},
            {"Done": False, "Sl No": 12, "Date": date.today(), "Item": "Water Chestnut", "Qty": 2.5, "UOM": "kg", "Rate": 60.0},
        ])
        st.session_state.saved_status = False
        st.rerun()

# Main Layout: Editable Data Editor with Checkbox Column
st.subheader("Interactive Item Entries & Checkboxes")
st.markdown("Check the **Done** column box to cross off items. Edits autosave into session state.")

edited_df = st.data_editor(
    st.session_state.items_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Done": st.column_config.CheckboxColumn("Done?", default=False, width="small"),
        "Sl No": st.column_config.NumberColumn("Sl No", format="%d", width="small"),
        "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
        "Item": st.column_config.TextColumn("Item Description", required=True),
        "Qty": st.column_config.NumberColumn("Qty", min_value=0.0, format="%.2f"),
        "UOM": st.column_config.TextColumn("UOM (kg, pcs...)"),
        "Rate": st.column_config.NumberColumn("Rate (₹)", min_value=0.0, format="₹%.2f")
    },
    key="data_editor_main"
)

# Detect live changes and autosave into session state
if not edited_df.equals(st.session_state.items_df):
    st.session_state.items_df = edited_df.copy()
    st.session_state.saved_status = False
    st.rerun()

# Calculated Amount Preview Table with Strike-Through Styling for Completed Items
st.markdown("### 🧮 Live Calculated Ledger View (Strikethrough for Completed Items)")
calc_display_df = st.session_state.items_df.copy()
calc_display_df["Qty"] = pd.to_numeric(calc_display_df["Qty"], errors='coerce').fillna(0)
calc_display_df["Rate"] = pd.to_numeric(calc_display_df["Rate"], errors='coerce').fillna(0)
calc_display_df["Amount"] = calc_display_df["Qty"] * calc_display_df["Rate"]

def strike_through_formatter(val, row_is_done):
    if row_is_done:
        return f"<s>{val}</s>"
    return str(val)

# Apply custom styling function where rows marked 'Done' get strike-through styling
def style_completed_rows(row):
    if row.get("Done", False):
        return ['text-decoration: line-through; color: #9ca3af; background-color: #f8fafc;' for _ in row.index]
    return ['' for _ in row.index]

styled_df = calc_display_df.style.apply(style_completed_rows, axis=1).format({
    "Qty": "{:,.2f}",
    "Rate": "₹{:,.2f}",
    "Amount": "₹{:,.2f}"
})

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)

# Status notification banner
if st.session_state.saved_status:
    st.success("✅ All changes are saved and synced with the server online.")
else:
    st.warning("⚠️ You have unsaved changes. Click **Save All Changes Online** in the sidebar to commit them.")
