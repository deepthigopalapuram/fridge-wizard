import pandas as pd
import streamlit as st

# -----------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------
st.set_page_config(
    page_title="Fridge Leftovers Wizard", page_icon="🍳", layout="centered"
)

st.title("🍳 AI Recipe & Fridge Leftovers Wizard (Indian Edition)")
st.markdown(
    "Got Indian vegetables and staples lying around? Select or type them below to discover instant desi meal ideas!"
)

# -----------------------------------------------------------
# INDIAN RECIPE DATABASE / LOGIC
# -----------------------------------------------------------
RECIPES = [
    {
        "title": "Aloo Capsicum Masala",
        "ingredients": ["potatoes", "capsicum", "onion", "tomatoes", "spices"],
        "time": "20 mins",
        "difficulty": "Easy",
        "instructions": "1. Chop potatoes and capsicum into cubes.\n2. Sauté onions and tomatoes with Indian spices in oil.\n3. Add potatoes and capsicum, cover and cook until tender.",
    },
    {
        "title": "Palak Dal (Spinach Lentils)",
        "ingredients": ["palak", "dal", "onion", "tomatoes", "spices", "garlic"],
        "time": "25 mins",
        "difficulty": "Medium",
        "instructions": "1. Boil lentils (dal) with turmeric.\n2. In a separate pan, temper garlic, onions, tomatoes, and chopped palak.\n3. Mix the cooked dal into the spinach tempering and simmer.",
    },
    {
        "title": "Methi Paratha",
        "ingredients": ["methi", "wheat flour", "spices", "oil"],
        "time": "20 mins",
        "difficulty": "Easy",
        "instructions": "1. Wash and finely chop fresh methi leaves.\n2. Mix with wheat flour, salt, and spices, then knead into a soft dough.\n3. Roll into flatbreads (parathas) and cook on a hot tawa with oil or ghee.",
    },
    {
        "title": "Baingan Bharta (Roasted Brinjal Mash)",
        "ingredients": ["brinjal", "onion", "tomatoes", "spices", "garlic"],
        "time": "30 mins",
        "difficulty": "Medium",
        "instructions": "1. Roast the brinjal directly over a flame until soft, peel the skin, and mash it.\n2. Sauté chopped onions, garlic, and tomatoes with spices.\n3. Mix in the mashed brinjal and cook for 5 minutes.",
    },
    {
        "title": "Karela Fry (Bitter Gourd Stir Fry)",
        "ingredients": ["bitter gourd", "onion", "spices", "oil"],
        "time": "25 mins",
        "difficulty": "Medium",
        "instructions": "1. Slice bitter gourd thinly and rub with salt (optional to reduce bitterness).\n2. Heat oil in a pan, add sliced onions and spices.\n3. Fry the bitter gourd on medium heat until crispy and golden.",
    },
    {
        "title": "Bottle Gourd Curry (Lauki Sabzi)",
        "ingredients": ["bottle gourd", "onion", "tomatoes", "spices"],
        "time": "20 mins",
        "difficulty": "Easy",
        "instructions": "1. Peel and chop bottle gourd into small cubes.\n2. Sauté onions and tomatoes with basic Indian spices.\n3. Add bottle gourd pieces, cover, and cook until soft and juicy.",
    },
    {
        "title": "Pudina Rice (Mint Pulao)",
        "ingredients": ["rice", "mint", "onion", "spices", "oil"],
        "time": "20 mins",
        "difficulty": "Easy",
        "instructions": "1. Blend fresh mint leaves into a coarse paste.\n2. Sauté sliced onions and spices in oil, then add the mint paste.\n3. Toss in cooked rice and mix thoroughly on low heat.",
    },
]


def find_matching_recipes(user_ingredients):
  """Finds recipes where the recipe ingredients are a subset of the user's available ingredients."""
  user_set = set([i.strip().lower() for i in user_ingredients])
  matched = []

  for recipe in RECIPES:
    recipe_set = set(recipe["ingredients"])
    # Only show recipes where all required ingredients are present in the user's available list
    if recipe_set.issubset(user_set):
      matched.append((len(recipe_set), recipe))

  # Sort by most comprehensive match
  matched.sort(key=lambda x: x[0], reverse=True)
  return [r[1] for r in matched]


# -----------------------------------------------------------
# USER INTERFACE
# -----------------------------------------------------------
st.subheader("🛒 What's in your Indian kitchen?")

# Indian vegetable quick-select checkboxes
st.markdown("Select Indian vegetables and items you have:")
col1, col2, col3, col4 = st.columns(4)
with col1:
  has_capsicum = st.checkbox("Capsicum 🫑")
  has_palak = st.checkbox("Palak 🥬")
with col2:
  has_brinjal = st.checkbox("Brinjal 🍆")
  has_methi = st.checkbox("Methi 🌱")
with col3:
  has_bottle_gourd = st.checkbox("Bottle Gourd 🥒")
  has_mint = st.checkbox("Mint (Pudina) 🌿")
with col4:
  has_bitter_gourd = st.checkbox("Bitter Gourd (Karela) 🍈")
  has_potatoes = st.checkbox("Potatoes 🥔")

# Common staples quick-select
st.markdown("Common Staples & Basics:")
c_s1, c_s2, c_s3, c_s4 = st.columns(4)
with c_s1:
  has_onion = st.checkbox("Onion 🧅")
with c_s2:
  has_tomatoes = st.checkbox("Tomatoes 🍅")
with c_s3:
  has_garlic = st.checkbox("Garlic 🧄")
with c_s4:
  has_rice = st.checkbox("Rice 🍚")

# Custom text input for extra flexibility
custom_ingredients = st.text_input(
    "Or type any extra ingredients separated by commas:",
    placeholder="e.g., dal, wheat flour, spices, oil",
)

# Compile selected ingredients list
selected_list = []
if has_capsicum:
  selected_list.append("capsicum")
if has_palak:
  selected_list.append("palak")
if has_brinjal:
  selected_list.append("brinjal")
if has_methi:
  selected_list.append("methi")
if has_bottle_gourd:
  selected_list.append("bottle gourd")
if has_mint:
  selected_list.append("mint")
if has_bitter_gourd:
  selected_list.append("bitter gourd")
if has_potatoes:
  selected_list.append("potatoes")
if has_onion:
  selected_list.append("onion")
if has_tomatoes:
  selected_list.append("tomatoes")
if has_garlic:
  selected_list.append("garlic")
if has_rice:
  selected_list.append("rice")

if custom_ingredients:
  extra = [item.strip() for item in custom_ingredients.split(",")]
  selected_list.extend(extra)

st.markdown("---")

# -----------------------------------------------------------
# GENERATE RESULTS
# -----------------------------------------------------------
if st.button("✨ Generate Indian Recipes", type="primary", use_container_width=True):
  if not selected_list:
    st.warning(
        "Please select or type at least one ingredient to get recipe"
        " suggestions!"
    )
  else:
    with st.spinner("Cooking up desi ideas..."):
      results = find_matching_recipes(selected_list)

    if not results:
      st.info(
          "No exact recipe matches found for those specific items yet. Try"
          " adding staples like onions, tomatoes, or spices!"
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
