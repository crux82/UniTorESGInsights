from ui.interface import build_interface
from ui.theme import theme, app_css

demo = build_interface()

demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    theme=theme,
    css=app_css,
    ssr_mode=False
)
