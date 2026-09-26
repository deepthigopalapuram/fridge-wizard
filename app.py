import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------------------------------------
# PAGE CONFIGURATION & CUSTOM HTML BRANDING INJECTION
# -----------------------------------------------------------
st.set_page_config(
    page_title="WhatToCook",
    page_icon="🍳",
    layout="centered",
)

# This custom JavaScript/HTML overrides the browser tab title and favicon directly
components.html(
    """
    <script>
        const docTitle = window.parent.document.querySelector("title");
        if (docTitle) {
            docTitle.text = "WhatToCook 🍳";
        }
        
        // Change the favicon dynamically
        const links = window.parent.document.querySelectorAll("link[rel*='icon']");
        links.forEach(link => {
            link.href = "https://abs.twimg.com/emoji/v2/72x72/1f373.png"; // Frying pan emoji image
        });
    </script>
""",
    height=0,
)

st.title("🍳 WhatToCook")
st.markdown(
    "Select the Indian vegetables you have available. Staples like **onions,"
    " garlic, rice, wheat flour, dal, chana, and rajma** are already assumed to"
    " be in your kitchen!"
)
