import pandas as pd
import streamlit as st

# -----------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------
st.set_page_config(
    page_title="Fridge Leftovers Wizard", page_icon="🍳", layout="centered"
)

st.title("🍳 AI Recipe & Fridge Leftovers Wizard")
st.markdown(
    "Got random ingredients lying around? Select or type them below to discover instant meal ideas!"
)

# -----------------------------------------------------------
# RECIPE DATABASE / LOGIC (Simple rule-based matching engine)
# -----------------------------------------------------------
RECIPES = [
    {
        "title": "Quick Egg Fried Rice",
        "ingredients": ["eggs", "rice", "onion", "garlic", "soy sauce"],
        "time": "15 mins",
        "difficulty": "Easy",
        "instructions": "1. Heat oil in a pan and sauté chopped onions and garlic.\n2. Crack in eggs and scramble.\n3. Add leftover cooked rice and soy sauce, toss well on high heat until hot.",
    },
    {
        "title": "Cheesy Tomato Omelet",
        "ingredients": ["eggs", "tomatoes", "cheese", "onion"],
        "time": "10 mins",
        "difficulty": "Easy",
        "instructions": "1. Whisk eggs in a bowl with a pinch of salt.\n2. Pour into a hot buttered pan, add diced tomatoes, onions, and shredded cheese.\n3. Fold in half and serve hot.",
    },
    {
        "title": "Garlic Butter Pasta",
        "ingredients": ["pasta", "garlic", "butter", "cheese"],
        "time": "12 mins",
        "difficulty": "Easy",
        "instructions": "1. Boil pasta until al dente.\n2. In a separate pan, melt butter and sauté minced garlic until fragrant.\n3. Toss pasta in garlic butter and top with cheese.",
    },
    {
        "title": "Potato & Onion Stir Fry (Aloo Fry)",
        "ingredients": ["potatoes", "onion", "oil", "spices"],
        "time": "20 mins",
        "difficulty": "Easy",
        "instructions": "1. Slice potatoes thinly and chop onions.\n2. Heat oil in a pan, add spices, and shallow-fry potatoes and onions on medium heat until crispy.",
    },
    {
        "title": "Paneer Bhurji",
        "ingredients": ["paneer", "onion", "tomatoes", "spices"],
        "time": "15 mins",
        "difficulty": "Easy",
        "instructions": "1. Sauté chopped onions and tomatoes in a pan with spices.\n2. Crumble paneer into the mix and stir well for 5 minutes.",
    },
]


def find_matching_recipes(user_ingredients):
    """Finds recipes matching at least one of the user's available ingredients."""
    user_set = set([i.strip().lower() for i in user_ingredients])
    matched = []

    for recipe in RECIPES:
        recipe_set = set(recipe["ingredients"])
        # Check if there is an intersection between user ingredients and recipe ingredients
        common = user_set.intersection(recipe_set)
        if common:
            score = len(common)
            matched.append((score, recipe))

    # Sort by how many ingredients match best
    matched.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in matched]


# -----------------------------------------------------------
# USER INTERFACE
# -----------------------------------------------------------
st.subheader("🛒 What's in your kitchen?")

# Common ingredient quick-select chips/checkboxes
st.markdown("Select common items you have:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    has_eggs = st.checkbox("Eggs 🥚")
    has_pasta = st.checkbox("Pasta 🍝")
with col2:
    has_rice = st.checkbox("Rice 🍚")
    has_potatoes = st.checkbox("Potatoes 🥔")
with col3:
    has_onion = st.checkbox("Onion 🧅")
    has_cheese = st.checkbox("Cheese 🧀")
with col4:
    has_tomatoes = st.checkbox("Tomatoes 🍅")
    has_paneer = st.checkbox("Paneer 🧀")

# Custom text input for extra flexibility
custom_ingredients = st.text_input(
    "Or type any extra ingredients separated by commas:",
    placeholder="e.g., garlic, butter, mushrooms",
)

# Compile selected ingredients list
selected_list = []
if has_eggs:
    selected_list.append("eggs")
if has_pasta:
    selected_list.append("pasta")
if has_rice:
    selected_list.append("rice")
if has_potatoes:
    selected_list.append("potatoes")
if has_onion:
    selected_list.append("onion")
if has_cheese:
    selected_list.append("cheese")
if has_tomatoes:
    selected_list.append("tomatoes")
if has_paneer:
    selected_list.append("paneer")

if custom_ingredients:
    extra = [item.strip() for item in custom_ingredients.split(",")]
    selected_list.extend(extra)

st.markdown("---")

# -----------------------------------------------------------
# GENERATE RESULTS
# -----------------------------------------------------------
if st.button("✨ Generate Recipes", type="primary", use_container_width=True):
    if not selected_list:
        st.warning(
            "Please select or type at least one ingredient to get recipe suggestions!"
        )
    else:
        with st.spinner("Cooking up ideas..."):
            results = find_matching_recipes(selected_list)

        if not results:
            st.info(
                "No exact recipe matches found for those specific items, but try adding staples like rice, eggs, or onions!"
            )
        else:
            st.success(f"Found {len(results)} delicious meal idea(s) for you!")
            for recipe in results:
                with st.container(border=True):
                    st.subheader(recipe["title"])
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"⏱️ **Prep Time:** {recipe['time']}")
                    with c2:
                        st.markdown(f"📊 **Difficulty:** {recipe['difficulty']}")

                    st.markdown(
                        f"🥗 **Required Ingredients:** {', '.join(recipe['ingredients'])}"
                    )
                    st.markdown("**Instructions:**")
                    st.text(recipe["instructions"])
