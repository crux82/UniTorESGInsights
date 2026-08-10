import gradio as gr

# GRADIO UI

# =========================
# CUSTOM CSS
# =========================

app_css = """
/* =========================
HEADINGS ONLY
========================= */

h1, h2, h3 {
    color: #006c4b !important;
}
"""

# =========================
# THEME
# =========================

theme = gr.themes.Base(
    primary_hue="green"
).set(
    button_primary_background_fill="#006c4b",
    button_primary_background_fill_hover="#008a61",
    button_primary_text_color="white"
)
