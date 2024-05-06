import streamlit as st
import pandas as pd
import random

# Load data from Excel file
data = pd.read_excel(r"data.xlsx")

# Define CSS styles
main_title_style = """
    font-size: 32px;
    font-weight: bold;
    color: red;
    margin-bottom: 20px;
"""

subheader_style = """
    font-size: 20px;
    margin-top: 30px;
    margin-bottom: 10px;
"""

# Sidebar
st.sidebar.subheader("YOBOU Market")
st.sidebar.markdown("[Accéder à la plateforme E-commerce](http://www.yoboumarket.com)")

# Main title
st.markdown('<h1 style="{}">Recommandation de paniers de produits de YOBOU Market</h1>'.format(main_title_style), unsafe_allow_html=True)
st.markdown("""
    <p style="font-size: 16px; margin-bottom: 30px;">
    Cette page vous permettra de composer des paniers de produits en fonction de vos catégories de préférences et de votre budget. 
    Les données des produits sont chargées, puis filtrées en fonction des catégories que vous sélectionnez. 
    Ensuite, vous entrez votre budget, et l'application recommande plusieurs paniers de produits qui respectent ce budget et contiennent une variété d'articles provenant des catégories sélectionnées. 
    Les paniers sont composés en sélectionnant aléatoirement des produits de chaque catégorie tout en respectant le budget donné. 
    Une fois recommandés, les détails des paniers, y compris les produits, leurs prix unitaires et quantités, ainsi que le total du panier, vous sont affichés.
    </p>
""", unsafe_allow_html=True)

# Multiselect for selecting product categories
categories = data['Catégorie'].unique()
selected_categories = st.multiselect("Sélectionnez les catégories de produits:", categories, default=categories)
filtered_df = data[data['Catégorie'].isin(selected_categories)]

# Number input for budget
budget = st.number_input("Entrez votre budget:", min_value=0.0, step=0.01)

# Function to recommend baskets of products
def recommend_baskets(data, budget, num_baskets=5):
    baskets = []
    remaining_budget = budget

    for _ in range(num_baskets):
        current_budget = remaining_budget
        current_basket = []

        for category in selected_categories:
            category_products = data[data['Catégorie'] == category]
            if not category_products.empty:
                chosen_product = category_products.sample()
                product_price = chosen_product['Prix'].iloc[0]
                if product_price <= current_budget:
                    max_quantity = min(int(current_budget / product_price), 2)
                    quantity = random.randint(1, max_quantity)
                    current_basket.append((chosen_product['Produit'].iloc[0], product_price, quantity))
                    current_budget -= product_price * quantity
                    data = data.drop(chosen_product.index)

        while len(current_basket) < 5 and len(data) > 0:
            chosen_product = data.sample()
            product_price = chosen_product['Prix'].iloc[0]
            if product_price <= current_budget:
                max_quantity = min(int(current_budget / product_price), 10)
                quantity = random.randint(1, max_quantity)
                current_basket.append((chosen_product['Produit'].iloc[0], product_price, quantity))
                current_budget -= product_price * quantity
                data = data.drop(chosen_product.index)
            else:
                break
        
        baskets.append(current_basket)
    
    return baskets

# Recommend baskets when button is clicked
if st.button("Recommander des paniers"):
    recommended_baskets = recommend_baskets(filtered_df, budget)
    st.subheader("Paniers recommandés:")

    for i, basket in enumerate(recommended_baskets):
        st.write(f"Panier {i+1}:")
        total_price = sum([product[1] * product[2] for product in basket])
        for product in basket:
            st.write(f"- {product[0]} (Prix unitaire: ${product[1]:.2f}, Quantité: {product[2]})")
        st.write(f"Total du panier: ${total_price:.2f}")
