import gradio as gr

from ui.state import STATE


#Filter SDG
SDG_IMAGE_DIR = "assets/sdg_icons"

sdg_icons = {
    i: f"{SDG_IMAGE_DIR}/E_PRINT_{i:02d}.jpg"
    for i in range(1, 18)
}

sdg_images = [sdg_icons[i] for i in range(1, 18)]

def filter_sdg(evt: gr.SelectData):

    df = STATE.get("df")

    sdg_num = evt.index + 1
    pattern = f"SDG_{sdg_num}:"

    filtered = df[df["17 SDG Alignment"].astype(str).str.contains(pattern, na=False)]

    title = f"Showing results for SDG {sdg_num}"

    return filtered, title


#Filter GRI
GRI_IMAGE_DIR = "assets/gri_icons"

gri_topics = ["General", "Economic", "Environmental", "Social"]

gri_images = [
    f"{GRI_IMAGE_DIR}/General.PNG",
    f"{GRI_IMAGE_DIR}/Economic.PNG",
    f"{GRI_IMAGE_DIR}/Environmental.PNG",
    f"{GRI_IMAGE_DIR}/Social.PNG"
]

def filter_gri(evt: gr.SelectData):

    df = STATE.get("df")

    selected_idx = evt.index
    topic = gri_topics[selected_idx]   # Social / Economic / ...

    filtered = df[df["GRI Topic Alignment"].astype(str) == topic]

    title = f"Showing results for GRI Topic: {topic}"

    return filtered, title


# TOGGLE FILTERS
def toggle_filters(tasks):

    if tasks is None:
        tasks = []

    if isinstance(tasks, str):
        tasks = [tasks]

    show_sdg = "17 SDG Alignment" in tasks
    show_gri = "GRI Topic Alignment" in tasks

    return (
        gr.update(visible=show_sdg),
        gr.update(visible=show_gri)
    )


# Filter QUALITY Disclosure
QUALITY_IMAGE_DIR = "assets/quality_icons"

quality_icons = {
    "Informative": f"{QUALITY_IMAGE_DIR}/Informative.PNG",
    "Non-informative/Vague": f"{QUALITY_IMAGE_DIR}/Vague.PNG",

    "Qualitative": f"{QUALITY_IMAGE_DIR}/Qul.PNG",
    "Quantitative": f"{QUALITY_IMAGE_DIR}/Qun.PNG",

    "High Potential Greenwashing": f"{QUALITY_IMAGE_DIR}/HPG.PNG",
    "Low Potential Greenwashing": f"{QUALITY_IMAGE_DIR}/LPG.PNG"
}

quality_task_1_gallery = [quality_icons["Informative"], quality_icons["Non-informative/Vague"]]
quality_task_2_gallery = [quality_icons["Qualitative"], quality_icons["Quantitative"]]
quality_task_3_gallery = [quality_icons["High Potential Greenwashing"], quality_icons["Low Potential Greenwashing"]]

def filter_quality_1(evt: gr.SelectData):
    df = STATE.get("df")

    label = "Informative" if evt.index == 0 else "Non-informative/Vague"

    filtered = df[df["Informative & Non-Informative/Vague Sustainability Text Identification"].astype(str) == label]

    title = f"Showing results: {label}"
    return filtered, title

def filter_quality_2(evt: gr.SelectData):
    df = STATE.get("df")

    label = "Qualitative" if evt.index == 0 else "Quantitative"

    filtered = df[df["Qualitative & Quantitative Sustainability Text Identification"].astype(str) == label]

    title = f"Showing results: {label}"
    return filtered, title

def filter_quality_3(evt: gr.SelectData):
    df = STATE.get("df")

    label = "High Potential Greenwashing" if evt.index == 0 else "Low Potential Greenwashing"

    filtered = df[df["High Potential Greenwashing Detection"].astype(str) == label]

    title = f"Showing results: {label}"
    return filtered, title

# TOGGLE FILTERS
def toggle_quality_filters(tasks):

    if tasks is None:
        tasks = []

    if isinstance(tasks, str):
        tasks = [tasks]

    show_info = (
        "Informative & Non-Informative/Vague Sustainability Text Identification"
        in tasks
    )

    show_qq = (
        "Qualitative & Quantitative Sustainability Text Identification"
        in tasks
    )

    show_gw = (
        "High Potential Greenwashing Detection"
        in tasks
    )

    return (
        gr.update(visible=show_info),
        gr.update(visible=show_qq),
        gr.update(visible=show_gw)
    )


# Filter Climate
CLIMATE_DIR = "assets/climate_icons"

climate_icons = {
    "Climate": f"{CLIMATE_DIR}/C.PNG",
    "Non-Climate": f"{CLIMATE_DIR}/NC.PNG"
}

gri_climate_icons = {
    "GRI 101": f"{CLIMATE_DIR}/GRI101.PNG",
    "GRI 2": f"{CLIMATE_DIR}/GRI102.PNG",
    "GRI 201": f"{CLIMATE_DIR}/GRI201.PNG",
    "GRI 302": f"{CLIMATE_DIR}/GRI302.PNG",
    "GRI 303": f"{CLIMATE_DIR}/GRI303.PNG",
    "GRI 305": f"{CLIMATE_DIR}/GRI305.PNG",
    "GRI 306": f"{CLIMATE_DIR}/GRI306.PNG",
}

sdg13_icons = {
    "Climate Action (SDG13)": f"{CLIMATE_DIR}/CA.PNG",
    "Non-Climate Action": f"{CLIMATE_DIR}/NCA.PNG"
}

gri_sdg13_icons = {
    "Economical Aspect (GRI 201)": f"{CLIMATE_DIR}/EcCA.PNG",
    "Environmental Aspect (GRI 305)": f"{CLIMATE_DIR}/EnCA.PNG",
    "General Aspect (GRI 2)": f"{CLIMATE_DIR}/GCA.PNG"
}

climate_images = list(climate_icons.values())
gri_climate_images = list(gri_climate_icons.values())
sdg13_images = list(sdg13_icons.values())
gri_sdg13_images = list(gri_sdg13_icons.values())


def filter_climate(evt: gr.SelectData):

    df = STATE.get("df")

    label = list(climate_icons.keys())[evt.index]

    filtered = df[df["Climate Alignment"].astype(str) == label]

    return filtered, f"Showing: {label}"

def filter_gri_climate(evt: gr.SelectData):

    df = STATE.get("df")

    label = list(gri_climate_icons.keys())[evt.index]

    filtered = df[df["GRI Climate Alignment"].astype(str) == label]

    return filtered, f"Showing: {label}"

def filter_sdg13(evt: gr.SelectData):

    df = STATE.get("df")

    label = list(sdg13_icons.keys())[evt.index]

    filtered = df[df["Climate Action (SDG13) Alignment"].astype(str) == label]

    return filtered, f"Showing: {label}"

def filter_gri_sdg13(evt: gr.SelectData):

    df = STATE.get("df")

    label = list(gri_sdg13_icons.keys())[evt.index]

    filtered = df[df["GRI Climate Action (SDG13) Alignment"].astype(str) == label]

    return filtered, f"Showing: {label}"

# TOGGLE FILTERS
def toggle_climate(tasks):

    if tasks is None:
        tasks = []

    if isinstance(tasks, str):
        tasks = [tasks]

    return (
        gr.update(visible="Climate Alignment" in tasks),
        gr.update(visible="GRI Climate Alignment" in tasks),
        gr.update(visible="Climate Action (SDG13) Alignment" in tasks),
        gr.update(visible="GRI Climate Action (SDG13) Alignment" in tasks)
    )