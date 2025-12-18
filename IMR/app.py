import streamlit as st
import pandas as pd
import uuid
from datetime import date

# ===============================
# KONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="Aplikasi Kasir & Transaksi Keuangan",
    layout="wide"
)

st.title("💰 Aplikasi Kasir & Transaksi Keuangan")

# ===============================
# PILIHAN DROPDOWN
# ===============================
transaction_types = ["Income", "Expense"]
categories = ["Sales", "Operational", "Marketing", "Salary", "Other"]
payment_methods = ["Cash", "Bank Transfer", "QRIS", "E-Wallet"]
counterparties = ["Customer", "Supplier", "Vendor", "Internal"]

# ===============================
# SESSION STATE
# ===============================
if "data_transaksi" not in st.session_state:
    st.session_state.data_transaksi = []

# ===============================
# FORM INPUT TRANSAKSI
# ===============================
st.subheader("📝 Input Transaksi")

with st.form("form_transaksi"):
    col1, col2 = st.columns(2)

    with col1:
        tanggal = st.date_input("Tanggal Transaksi", date.today())
        jenis = st.selectbox("Jenis Transaksi", transaction_types)
        kategori = st.selectbox("Kategori", categories)

    with col2:
        jumlah = st.number_input("Jumlah (Rp)", min_value=0.0, step=1000.0)
        metode = st.selectbox("Metode Pembayaran", payment_methods)
        pihak = st.selectbox("Pihak Terkait", counterparties)

    simpan = st.form_submit_button("Simpan")

# ===============================
# SIMPAN DATA
# ===============================
if simpan:
    transaksi = {
        "transaction_id": f"TX-{uuid.uuid4().hex[:6].upper()}",
        "date": tanggal,
        "transaction_type": jenis,
        "category": kategori,
        "amount": jumlah if jenis == "Income" else -jumlah,
        "payment_method": metode,
        "counterparty": pihak
    }

    st.session_state.data_transaksi.append(transaksi)
    st.success("✅ Transaksi berhasil disimpan")

# ===============================
# TAMPILKAN DATA
# ===============================
if st.session_state.data_transaksi:
    st.subheader("📊 Data Transaksi Keuangan")

    df = pd.DataFrame(st.session_state.data_transaksi)
    st.dataframe(df, use_container_width=True)

    # ===============================
    # RINGKASAN
    # ===============================
    total_income = df[df["amount"] > 0]["amount"].sum()
    total_expense = abs(df[df["amount"] < 0]["amount"].sum())
    profit = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"Rp {total_income:,.0f}")
    col2.metric("Total Expense", f"Rp {total_expense:,.0f}")
    col3.metric("Profit / Loss", f"Rp {profit:,.0f}")
else:
    st.info("Belum ada transaksi yang diinput.")
