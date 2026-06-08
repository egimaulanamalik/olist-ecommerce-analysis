import streamlit as st
import pandas as pd

DATA_PATH = '/Users/egi/Documents/Portfolio/olist-ecommerce-analysis/data/cleaned/'
RAW_PATH  = '/Users/egi/Documents/Portfolio/olist-ecommerce-analysis/data/'

try:
    master = pd.read_csv(DATA_PATH + "master_orders.csv",
                         parse_dates=['order_purchase_timestamp'])
    st.success(f"master loaded - {master.shape}")
except Exception as e:
    st.error(f"master failed: {e}")
    
try:
    products = pd.read_csv(DATA_PATH + "products_cleaned.csv")
    st.success(f"products loaded - {products.shape}")
except Exception as e:
    st.error(f"products failed: {e}")

try:
    order_items = pd.read_csv(RAW_PATH + "olist_order_items_dataset.csv")
    st.success(f"order items loaded - {order_items.shape}")
except Exception as e:
    st.error(f"order_items failed: {e}")

try:
    sellers = pd.read_csv(RAW_PATH + "olist_sellers_dataset.csv")
    st.success(f"sellers loaded - {sellers.shape}")
except Exception as e:
    st.error(f"sellers failed: {e}")
    
try:
    payments = pd.read_csv(RAW_PATH + "olist_order_payments_dataset.csv")
    st.success(f"payments loaded - {payments.shape}")
except Exception as e:
    st.error(f"payments failed: {e}")