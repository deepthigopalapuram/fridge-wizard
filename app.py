import pandas as pd
import streamlit as st

# -----------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------
st.set_page_config(page_title="WhatToCook", page_icon="🍳", layout="centered")

st.title("🍳 WhatToCook")
st.markdown(
    "Select the Indian vegetables you have available. Staples like **onions,"
    " garlic, rice, wheat flour, dal, chana, and rajma** are already assumed to"
    " be in your kitchen!"
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
        "title": "Capsicum Besan Sabzi (Stir Fry)",
        "ingredients": ["capsicum", "onion", "spices", "oil"],
        "time": "15 mins",
        "difficulty": "Easy",
        "instructions": "1. Slice capsicum and onions lengthwise.\n2. Sauté onions in oil, add sliced capsicum and spices, and cook for 5 minutes.\n3. Sprinkle roasted gram flour (besan) on top for an amazing crunch and aroma!",
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
    {
        "title": "Punjabi Rajma Curry",
        "ingredients": ["rajma", "onion", "tomatoes", "garlic", "spices"],
        "time": "35 mins",
        "difficulty": "Medium",
        "instructions": "1. Boil pre-soaked rajma until completely soft.\n2. Sauté garlic, onions, and tomatoes with rich Indian spices to make a thick gravy.\n3. Add boiled rajma, simmer together for 10 minutes, and serve hot with rice.",
    },
]


def find_matching_recipes(user_ingredients, selected_veg_set):
  """Finds recipes where the recipe ingredients are a subset of the user's available ingredients,

  AND the recipe actually uses at least one of the explicitly checked vegetables.
  """
  user_set = set([i.strip().lower() for i in user_ingredients])
  matched = []

  for recipe in RECIPES:
    recipe_set = set(recipe["ingredients"])
    # 1. User must have all ingredients for the recipe
    # 2. Recipe MUST contain at least one of the explicitly selected fresh vegetables
    if recipe_set.issubset(user_set) and (recipe_set & selected_veg_set):
      matched.append((len(recipe_set), recipe))

  matched.sort(key=lambda x: x[0], reverse=True)
  return [r[1] for r in matched]


# -----------------------------------------------------------
# USER INTERFACE
# -----------------------------------------------------------
st.subheader("🛒 What's in your Indian kitchen?")

# Indian vegetable quick-select checkboxes
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

# Custom text input for extra flexibility
custom_ingredients = st.text_input(
    "Type any other extra ingredients (e.g., tomatoes, oil, spices):",
    placeholder="e.g., tomatoes, oil, spices",
)

# Start with permanent staples
selected_list = [
    "onion",
    "garlic",
    "rice",
    "wheat flour",
    "dal",
    "chick peas",
    "rajma",
    "tomatoes",
    "oil",
    "spices",
]

# Track explicitly selected fresh vegetables
selected_veg_set = set()
any_veg_selected = False

if has_capsicum:
  selected_list.append("capsicum")
  selected_veg_set.add("capsicum")
  any_veg_selected = True
if has_palak:
  selected_list.append("palak")
  selected_veg_set.add("palak")
  any_veg_selected = True
if has_brinjal:
  selected_list.append("brinjal")
  selected_veg_set.add("brinjal")
  any_veg_selected = True
if has_methi:
  selected_list.append("methi")
  selected_veg_set.add("methi")
  any_veg_selected = True
if has_bottle_gourd:
  selected_list.append("bottle gourd")
  selected_veg_set.add("bottle gourd")
  any_veg_selected = True
if has_mint:
  selected_list.append("mint")
  selected_veg_set.add("mint")
  any_veg_selected = True
if has_bitter_gourd:
  selected_list.append("bitter gourd")
  selected_veg_set.add("bitter gourd")
  any_veg_selected = True
if has_potatoes:
  selected_list.append("potatoes")
  selected_veg_set.add("potatoes")
  any_veg_selected = True

if custom_ingredients:
  extra = [item.strip() for item in custom_ingredients.split(",")]
  if extra and extra[0] != "":
    selected_list.extend(extra)
    for item in extra:
      selected_veg_set.add(item.lower())
    any_veg_selected = True

st.markdown("---")

# -----------------------------------------------------------
# GENERATE RESULTS
# -----------------------------------------------------------
if st.button("✨ Generate Recipes", type="primary", use_container_width=True):
  if not any_veg_selected:
    st.error(
        "🛑 **FAST TILL YOU BUY STUFF!** 🧘‍♂️ Your fridge is completely empty"
        " of veggies. Go grab some sabzi before the Master Chef locks the"
        " kitchen!"
    )
  else:
    with st.spinner("Cooking up desi ideas..."):
      results = find_matching_recipes(selected_list, selected_veg_set)

    if not results:
      st.warning(
          "⚠️ **STRICT FASTING CONTINUES!** No matching recipes found that"
          " utilize those specific fresh veggies. Try checking a few more!"
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
