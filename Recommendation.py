import streamlit as st
import pandas as pd
import random

import streamlit as st


# Add a sidebar
st.sidebar.subheader("YOBOU Market")

# Add a link to the sidebar
st.sidebar.markdown("[Accéder à la plateforme E-commerce](http://www.yoboumarket.com)")

# Chargement des données de produits depuis un fichier Excel
data = pd.read_excel(r"data.xlsx")

# Titre de l'application

st.markdown('<h1 style="color: red;">Recommandation de paniers de produits de YOBOU Market</h1>', unsafe_allow_html=True)
st.subheader("Cette page vous permettra de composer des paniers de produits en fonction de vos catégories de préférences et de votre budget. Les données des produits sont chargées, puis filtrées en fonction des catégories que vous sélectionnez. Ensuite, vous entrez votre budget, et l'application recommande plusieurs paniers de produits qui respectent ce budget et contiennent une variété d'articles provenant des catégories sélectionnées. Les paniers sont composés en sélectionnant aléatoirement des produits de chaque catégorie tout en respectant le budget donné. Une fois recommandés, les détails des paniers, y compris les produits, leurs prix unitaires et quantités, ainsi que le total du panier, vous sont affichés.")
# Afficher toutes les catégories disponibles
categories = data['Catégorie'].unique()

# Sélectionner toutes les catégories par défaut
selected_categories = st.multiselect("Sélectionnez les catégories de produits:", categories, default=categories)

# Filtrer les produits en fonction des catégories sélectionnées
filtered_df = data[data['Catégorie'].isin(selected_categories)]



# Demander le budget de l'acheteur
budget = st.number_input("Entrez votre budget:", min_value=0.0, step=0.01)

# Fonction pour générer des paniers de produits
def recommander_paniers(data, budget, nb_paniers=5):
    paniers = []
    remaining_budget = budget

    # Générer plusieurs paniers
    for _ in range(nb_paniers):
        current_budget = remaining_budget
        current_panier = []

        # Sélectionner un produit de chaque catégorie jusqu'à ce que tous les produits soient utilisés
        for category in selected_categories:
            category_products = data[data['Catégorie'] == category]
            if not category_products.empty:
                chosen_product = category_products.sample()
                product_price = chosen_product['Prix'].iloc[0]
                if product_price <= current_budget:
                    max_quantity = min(int(current_budget / product_price), 2)  # Limiter la quantité à 10 au maximum
                    quantity = random.randint(1, max_quantity)
                    current_panier.append((chosen_product['Produit'].iloc[0], product_price, quantity))
                    current_budget -= product_price * quantity
                    data = data.drop(chosen_product.index)

        # Compléter le panier jusqu'à ce qu'il contienne au moins 5 éléments
        while len(current_panier) < 5 and len(data) > 0:
            chosen_product = data.sample()
            product_price = chosen_product['Prix'].iloc[0]
            if product_price <= current_budget:
                max_quantity = min(int(current_budget / product_price), 10)  # Limiter la quantité à 10 au maximum
                quantity = random.randint(1, max_quantity)
                current_panier.append((chosen_product['Produit'].iloc[0], product_price, quantity))
                current_budget -= product_price * quantity
                data = data.drop(chosen_product.index)
            else:
                break
        
        # Ajouter le panier généré à la liste des paniers
        paniers.append(current_panier)
    
    return paniers

# Recommender les paniers lorsque l'utilisateur clique sur le bouton
if st.button("Recommander des paniers"):
    paniers_recommandes = recommander_paniers(filtered_df, budget)
    st.subheader("Paniers recommandés:")

    # Afficher les paniers recommandés
    for i, panier in enumerate(paniers_recommandes):
        st.write(f"Panier {i+1}:")
        total_prix = sum([produit[1] * produit[2] for produit in panier])
        for produit in panier:
            st.write(f"- {produit[0]} (Prix unitaire: ${produit[1]:.2f}, Quantité: {produit[2]})")
        st.write(f"Total du panier: ${total_prix:.2f}")
