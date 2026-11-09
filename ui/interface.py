import gradio as gr
import pandas as pd
import plotly.graph_objects as go

from ui.filters import (
    sdg_images,
    gri_images,
    filter_sdg,
    filter_gri,
    toggle_filters,
    quality_task_1_gallery, 
    quality_task_2_gallery, 
    quality_task_3_gallery,
    filter_quality_1,
    filter_quality_2,
    filter_quality_3,
    toggle_quality_filters,
    climate_images,
    gri_climate_images, 
    sdg13_images,
    gri_sdg13_images,
    filter_climate,
    filter_gri_climate,
    filter_sdg13,
    filter_gri_sdg13,
    toggle_climate
)

from ui.gradio_functions import (
    load_pdf,
    change_page,
    load_pdf_wrapper,
    change_page,
    highlight,
    upload_csv1,
    upload_csv2,
    run_sa_wrapper,
    set_task, 
    run_task,
    run_selected_tasks
)

PAPER_TITLE = (
    "UniTor ESG Insights: An Interactive Human-in-the-Loop System for "
    "Traceable Sustainability Report Analysis"
)
PAPER_DOI_URL = "https://doi.org/10.1145/3799682.3840253"
CIKM_URL = "https://cikm2026.diag.uniroma1.it/"
REPO_URL = "https://github.com/crux82/UniTorESGInsights"
MODELS_URL = "https://hf.co/collections/sag-uniroma2/unitoresginsights"
SPACE_URL = "https://huggingface.co/spaces/sag-uniroma2/UniTorESGInsights"
VIDEO_URL = "https://youtu.be/ErhCHIakyzg"
HF_ORG = "https://huggingface.co/sag-uniroma2"

ACM_REFERENCE = (
    "Seyed Alireza Mousavian Anaraki, Danilo Croce, Roberta Costa, Luigi Tiburzi, "
    "Armando Calabrese, and Roberto Basili. 2026. *UniTor ESG Insights: An Interactive "
    "Human-in-the-Loop System for Traceable Sustainability Report Analysis.* In Proceedings "
    "of the 35th ACM International Conference on Information and Knowledge Management "
    "(CIKM '26), November 07–11, 2026, Rome, Italy. ACM, New York, NY, USA. "
    f"[{PAPER_DOI_URL}]({PAPER_DOI_URL})"
)

BIBTEX = """@inproceedings{10.1145/3799682.3840253,
author = {Mousavian Anaraki, Seyed Alireza and Croce, Danilo and Costa, Roberta and Tiburzi, Luigi and Calabrese, Armando and Basili, Roberto},
title = {UniTor ESG Insights: An Interactive Human-in-the-Loop System for Traceable Sustainability Report Analysis},
year = {2026},
isbn = {9798400725395},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3799682.3840253},
doi = {10.1145/3799682.3840253},
abstract = {We present UniTor ESG Insights, an interactive system for traceable sustainability report analysis. Starting from PDF reports, the system extracts paragraph-level textual units, preserves page-level provenance, and applies a set of ESG classification modules for sustainability relevance detection, GRI--SDG topic alignment, disclosure quality assessment, qualitative/quantitative evidence identification, and climate-related analysis. The system targets ESG analysts, auditors, regulators, and corporate sustainability managers who need to inspect and aggregate evidence from long and partially structured reports. Unlike approaches that return only document-level labels or aggregate ESG scores, UniTor ESG Insights follows a bottom-up workflow in which predictions are generated at paragraph level and higher-level summaries remain linked to the underlying textual evidence. Users can inspect extracted paragraphs, filter predictions, correct intermediate outputs, re-upload refined data, visualize distributions, and export structured results. The demonstration shows an end-to-end scenario in which a user uploads a sustainability report, explores paragraph-level ESG predictions, analyzes disclosure quality and evidence characteristics, and generates traceable analytical views through a Gradio interface deployed on Hugging Face Spaces.},
booktitle = {Proceedings of the 35th ACM International Conference on Information and Knowledge Management},
pages = {9199–9203},
numpages = {5},
keywords = {esg analytics, sustainability reporting, human-in-the-loop systems, gri--sdg alignment, traceable decision support},
location = {Rome, Italy},
series = {CIKM '26}
}"""

LINKS_LINE = (
    f"📄 [Paper (DOI)]({PAPER_DOI_URL}) &nbsp;·&nbsp; "
    f"💻 [GitHub repository]({REPO_URL}) &nbsp;·&nbsp; "
    f"🤗 [Models]({MODELS_URL}) &nbsp;·&nbsp; "
    f"▶️ [Demo video]({VIDEO_URL})"
)

DEMO_INTRO_MD = f"""
Companion demo for the paper **"{PAPER_TITLE}"**, published in the Proceedings of the
[35th ACM International Conference on Information and Knowledge Management (CIKM 2026)]({CIKM_URL}),
November 7–11, 2026, Rome, Italy.

{LINKS_LINE}
"""

ABOUT_DEMO_MD = f"""
**What this demo does.** It turns a PDF sustainability report into *paragraph-level ESG evidence*:
every prediction stays linked to its document, page and paragraph number, so each chart can be
traced back to the text behind it.

**Human in the loop.** At every step you can download the results as CSV, review or correct them,
and upload the corrected file again: all later steps then use your corrections.

**How to use it.** Follow Steps 1–5 from top to bottom. Open the ℹ️ boxes for a short description
of each step and of the model behind each task.

**More details:** code, setup instructions and all models are in the
[GitHub repository]({REPO_URL}) and the [model collection]({MODELS_URL}).
The hosted version of this demo is on [Hugging Face Spaces]({SPACE_URL}).

**Cite.** {ACM_REFERENCE}

```bibtex
{BIBTEX}
```
"""

CITE_FOOTER_MD = f"""
---
### 📚 If you find UniTor ESG Insights useful, please cite our paper

{ACM_REFERENCE}

```bibtex
{BIBTEX}
```

You can find more details, the source code and all fine-tuned models in the
[GitHub repository]({REPO_URL}) and the [Hugging Face collection]({MODELS_URL}).
"""

# Sample report for first-time visitors (public PDF).
SAMPLE_REPORT_URL = "https://assets.asics.com/system/libraries/4036/ASICS_sustainability_report_2024.pdf"

# Short "how to try" guide shown at the top, for visitors who did not attend the presentation.
HOW_TO_TRY_MD = f"""
> 🚀 **New to UniTor ESG Insights?** Start with the [ASICS Sustainability Report 2024]({SAMPLE_REPORT_URL})
> (download the PDF and upload it in Step 1). Identify sustainability-relevant paragraphs (Step 2), then run
> **SDG Alignment** (Step 3) and click an SDG icon to inspect the supporting evidence. You can also explore
> disclosure quality (Step 4) and climate-related predictions (Step 5), and download the results for human
> review and correction.
"""

# Note shown next to the PDF upload (public demo).
UPLOAD_NOTE_MD = (
    "🔒 *Please upload only **public or authorized** documents "
    "(e.g. published sustainability reports). Do not upload confidential or personal data.* "
    f"No report at hand? Try the [ASICS Sustainability Report 2024]({SAMPLE_REPORT_URL})."
)

# Shared note: each task is a separate model, trained on its own dataset and label set.
TASK_NOTE = (
    "\n\n> **Note.** Each task uses a separate model, trained on its own dataset and label set. "
    "Validation scores are therefore not directly comparable across tasks. You can select and run "
    "several tasks at the same time, but interpret each task's labels separately: labels from "
    "different models may not always agree on the same paragraph. Choose the tasks that match "
    "your analysis goal."
)

STEP_INFO = {
    1: "Upload a PDF sustainability report. The system splits it into paragraphs (more than 20 words), "
       "keeping the **document name, page number and paragraph number** for traceability. "
       "Use ⬅ / ➡ to browse page by page: each page image is shown next to its extracted paragraphs. "
       "You can download the extracted CSV, edit it, and upload it again before the next step.",
    2: "Each paragraph is classified as **Relevant** or **Irrelevant** to sustainability frameworks "
       "(integrated GRI and SDG). Only Relevant paragraphs are passed to the next steps. "
       "Download the results, correct any label if needed, and upload the modified CSV.\n\n"
       "*Technical name:* Sustainability Frameworks (GRI & SDG) Alignment (SFA) for "
       "Relevant/Irrelevant Classification.",
    3: "Relevant paragraphs are aligned with the **17 SDGs** and with the **GRI topic** series "
       "(General, Economic, Environmental, Social). After running, click an SDG or GRI icon to "
       "filter the table and see only the paragraphs behind it." + TASK_NOTE,
    4: "Characterises the quality of each disclosure: **informative vs. vague**, **qualitative vs. "
       "quantitative**, and a **weak-disclosure risk proxy** (shown as 'greenwashing potential'). "
       "The risk proxy signals low evidential support, *not* a verdict of greenwashing." + TASK_NOTE,
    5: "Climate-specific analysis with ClimateBERT-based models: **climate relevance**, "
       "**GRI climate topics**, and **SDG 13 Climate Action** alignment (overall and by GRI aspect). "
       "Click any icon to filter the paragraphs." + TASK_NOTE +
       "\n\n> **Example.** A paragraph can be labelled *Environmental* by the GRI topic model in Step 3 "
       "but *Non-Climate* by the climate model in this step. The two models answer different questions "
       "with different training data, so their labels complement each other rather than conflict. "
       "Use climate relevance for climate-specific screening, and GRI topics for the broader "
       "sustainability topic.",
}

# Per-task info: model repo id, short description, labels, base model, indicative macro F1
# (validation scores of each released model, from Table 1 of the paper; they come from
# different datasets and are not directly comparable across tasks).
TASK_INFO = {
    "SA": {
        "name": "Sustainability Framework Alignment",
        "model": "SA_MODEL",
        "desc": "Binary classification model for detecting whether a paragraph is aligned with "
                "sustainability reporting integrated GRI and SDG frameworks.",
        "labels": "Relevant · Irrelevant",
        "base": "BERT (bert-base-cased)",
        "f1": "0.968",
    },
    "17 SDG Alignment": {
        "name": "SDG Alignment",
        "model": "SDG_MODEL",
        "desc": "Assigns each relevant paragraph to the Sustainable Development Goal (one of the 17 SDGs) "
                "it is most aligned with.",
        "labels": "SDG 1 … SDG 17",
        "base": "BERT (bert-base-cased)",
        "f1": "0.860",
    },
    "GRI Topic Alignment": {
        "name": "GRI Topic Alignment",
        "model": "GRITopics_MODEL",
        "desc": "Assigns each relevant paragraph to a GRI Standards topic series.",
        "labels": "General · Economic (GRI 200) · Environmental (GRI 300) · Social (GRI 400)",
        "base": "BERT",
        "f1": "0.736",
    },
    "Informative & Non-Informative/Vague Sustainability Text Identification": {
        "name": "Informative vs. Non-Informative/Vague",
        "model": "INFVague_MODEL",
        "desc": "Detects whether a sustainability paragraph gives specific, informative content "
                "or stays generic and vague.",
        "labels": "Informative · Non-informative/Vague",
        "base": "BERT",
        "f1": "0.675",
    },
    "Qualitative & Quantitative Sustainability Text Identification": {
        "name": "Qualitative vs. Quantitative",
        "model": "QQ_MODEL",
        "desc": "Detects whether a sustainability paragraph provides quantitative evidence "
                "(numbers, measurable indicators) or only qualitative statements.",
        "labels": "Qualitative · Quantitative",
        "base": "BERT",
        "f1": "0.857",
    },
    "High Potential Greenwashing Detection": {
        "name": "Weak-Disclosure Risk Proxy (High/Low Potential Greenwashing)",
        "model": "HPGW_MODEL",
        "desc": "Flags paragraphs with weak evidential support as a risk signal for further review. "
                "It reflects disclosure quality and linguistic evidence, not actual greenwashing behaviour.\n\n"
                "This is an **independent binary classifier**: it predicts the label directly from the "
                "paragraph text and does **not** combine the outputs of the other models in this demo. "
                "Its training labels were derived by combining the annotations of the same taxonomy "
                "(Relevant/Irrelevant, Informative/Non-informative, Qualitative/Quantitative):\n\n"
                "- **High Potential Greenwashing (weak disclosure):** *Relevant + Informative + Qualitative* "
                "or *Relevant + Non-informative* paragraphs, i.e. descriptive or less evidentially "
                "supported disclosures.\n"
                "- **Low Potential Greenwashing:** *Relevant + Informative + Quantitative* paragraphs, "
                "i.e. disclosures supported by measurable evidence.\n\n"
                "The label signals **weak evidential support that may require further review**; "
                "qualitative disclosures are not necessarily examples of greenwashing.",
        "labels": "High Potential Greenwashing · Low Potential Greenwashing",
        "base": "BERT",
        "f1": "0.793",
    },
    "Climate Alignment": {
        "name": "Climate Relevance",
        "model": "Climate_MODEL",
        "desc": "Detects whether a paragraph is about climate-related topics.",
        "labels": "Climate · Non-Climate",
        "base": "ClimateBERT",
        "f1": "0.930",
    },
    "GRI Climate Alignment": {
        "name": "GRI Climate Category Alignment",
        "model": "GRIClimate_MODEL",
        "desc": "Aligns climate-related paragraphs with GRI climate-relevant standards.",
        "labels": "GRI 101 Biodiversity · GRI 2 General · GRI 201 Economic · GRI 302 Energy · "
                  "GRI 303 Water · GRI 305 Emissions · GRI 306 Waste",
        "base": "ClimateBERT",
        "f1": "0.755",
    },
    "Climate Action (SDG13) Alignment": {
        "name": "Climate Action (SDG 13) Alignment",
        "model": "ClimateActionSDG13_MODEL",
        "desc": "Detects whether a paragraph is aligned with SDG 13 Climate Action.",
        "labels": "Climate Action (SDG13) · Non-Climate Action",
        "base": "ClimateBERT",
        "f1": "0.915",
    },
    "GRI Climate Action (SDG13) Alignment": {
        "name": "Climate Action GRI Topic Alignment",
        "model": "GRISDG13_MODEL",
        "desc": "Links SDG 13 Climate Action content to the GRI aspect it relates to.",
        "labels": "General Aspect (GRI 2) · Economic Aspect (GRI 201) · Environmental Aspect (GRI 305)",
        "base": "ClimateBERT",
        "f1": "0.910",
    },
}


def task_info_md(task):
    t = TASK_INFO[task]
    url = f"{HF_ORG}/{t['model']}"
    return (
        f"**{t['name']}** ([{t['model']}]({url}))\n\n"
        f"**Task description.** {t['desc']}\n\n"
        f"- **Labels:** {t['labels']}\n"
        f"- **Base model:** {t['base']}, fine-tuned\n"
        f"- **Validation macro F1 (indicative):** {t['f1']}\n\n"
        f"Model card: [{url}]({url}) · details in the [GitHub repository]({REPO_URL})"
    )


def info_box(label, md_text):
    """Collapsible info box: closed by default, click to open, click again to close."""
    with gr.Accordion(label, open=False):
        gr.Markdown(md_text)


def step_info(step, tasks):
    """One closed info box per step: the step explanation + one box per task model."""
    with gr.Accordion(f"ℹ️ About Step {step}", open=False):
        gr.Markdown(STEP_INFO[step])
        for task in tasks:
            with gr.Accordion(f"🤖 {TASK_INFO[task]['name']} — {TASK_INFO[task]['model']}", open=False):
                gr.Markdown(task_info_md(task))



def _empty_plot():
    return go.Figure()


def _empty_df():
    return pd.DataFrame()


def build_interface():
    with gr.Blocks() as demo:

        gr.Markdown("# UniTor ESG Insights: An Interactive Human-in-the-Loop System for Traceable Sustainability Report Analysis")

        # gr.Image(
        #    value="assets/logo.png",
        #    label="UniTor ESG Insights System",
        #    interactive=False,
        #    #width=600
        #)

        gr.Image(
            value="assets/workflow.png",
            label="Human-in-the-Loop Interactive Workflow Overview. SDG logo and icons © United Nations.",
            interactive=False,
            #width=600
        )

        # --- paper / repository / citation info under the workflow figure ---
        gr.Markdown(DEMO_INTRO_MD)
        gr.Markdown(HOW_TO_TRY_MD)
        info_box("📄 About this demo · paper · repository · how to cite", ABOUT_DEMO_MD)

        # =========================
        # STAGE 1: PDF → CSV
        # =========================
        gr.Markdown("## Step 1: Upload PDF and Extract Data")
        step_info(1, [])

        gr.Markdown(UPLOAD_NOTE_MD)
        file = gr.File(label="Upload PDF")
        load_btn = gr.Button("Load PDF", variant="primary")

        extracted_download = gr.File(label="Download Extracted CSV")

        upload_csv_1 = gr.File(label="(Optional) Upload Custom CSV")

        with gr.Row():
            prev = gr.Button("⬅", variant="primary")
            next = gr.Button("➡", variant="primary")

        with gr.Row():
            img = gr.Image()
            table = gr.Dataframe(value=_empty_df(), interactive=True)

        text = gr.Markdown()

        # =========================
        # STAGE 2: SA
        # =========================
        gr.Markdown("## Step 2: Identify Sustainability-Relevant Paragraphs")
        step_info(2, ["SA"])

        sa_btn = gr.Button("Run SFA", variant="primary")

        sa_download = gr.File(label="Download SFA Results")

        chart1 = gr.Plot(value=_empty_plot(), label="Distribution")

        upload_csv_2 = gr.File(label="(Optional) Upload Modified SFA CSV")

        # =========================
        # CONNECTIONS
        # =========================
        # --- STEP 1 ---
        load_btn.click(load_pdf_wrapper, file, [img, table, extracted_download])

        next.click(lambda: change_page(1), outputs=[img, table])
        prev.click(lambda: change_page(-1), outputs=[img, table])

        table.select(highlight, outputs=text)

        # Optional CSV override (Stage 1)
        upload_csv_1.upload(upload_csv1, upload_csv_1, table)

        # --- STEP 2 ---
        sa_btn.click(
            run_sa_wrapper,
            outputs=[sa_download, table, chart1]
        )

        # Optional CSV override (Stage 2)
        upload_csv_2.upload(upload_csv2, upload_csv_2, table)

        # =========================
        # STAGE 3: SDG / GRI
        # =========================
        gr.Markdown("## Step 3: SDG/GRI Classification (Topic Alignment)")
        step_info(3, ["17 SDG Alignment", "GRI Topic Alignment"])

        task_selector_1 = gr.Dropdown(
            choices=[
                "17 SDG Alignment",
                "GRI Topic Alignment"
            ],
            multiselect=True,
            label="Select Tasks"
        )

        run_tasks_btn_1 = gr.Button("Run", variant="primary")

        chart_tasks_1 = gr.Plot(value=_empty_plot())
        download_1 = gr.File(label="Download Results")


        # ---------- SDG FILTER ----------
        # NOTE: starts visible=True (not False) -- see the demo.load()
        # workaround below for why.
        with gr.Column(visible=True) as sdg_container:
            gr.Markdown("### SDG Filter. SDG logo and icons © United Nations. Used in accordance with the [UN SDG Guidelines](https://www.un.org/sustainabledevelopment/wp-content/uploads/2019/01/SDG_Guidelines_AUG_2019_Final.pdf) "
                        "for informational, non-commercial purposes. No endorsement by the United Nations is implied.")

            sdg_gallery = gr.Gallery(
                value=sdg_images,
                columns=6,
                allow_preview=False
            )

        sdg_result_table = gr.Dataframe(value=_empty_df(), interactive=True)

        sdg_gallery.select(
            fn=filter_sdg,
            outputs=[sdg_result_table, text]
        )


        # ---------- GRI FILTER ----------
        with gr.Column(visible=True) as gri_container:
            gr.Markdown("### GRI Topic Filter")

            gri_gallery = gr.Gallery(
                value=gri_images,
                columns=4,
                allow_preview=False
            )

        gri_result_table = gr.Dataframe(value=_empty_df(), interactive=True)

        gri_gallery.select(
            fn=filter_gri,
            outputs=[gri_result_table, text]
        )


        # ---------- TOGGLE FILTERS ----------
        task_selector_1.change(
            fn=toggle_filters,
            inputs=task_selector_1,
            outputs=[sdg_container, gri_container]
        )


        # ---------- RUN STEP 3 ----------
        run_tasks_btn_1.click(
            run_selected_tasks,
            inputs=task_selector_1,
            outputs=[download_1, table, chart_tasks_1]
        )

        # =========================
        # STAGE 4: DISCLOSURE QUALITY
        # =========================
        gr.Markdown("## Step 4: Disclosure Quality Analysis")
        step_info(4, [
            "Informative & Non-Informative/Vague Sustainability Text Identification",
            "Qualitative & Quantitative Sustainability Text Identification",
            "High Potential Greenwashing Detection",
        ])

        task_selector_2 = gr.Dropdown(
            choices=[
                "Informative & Non-Informative/Vague Sustainability Text Identification",
                "Qualitative & Quantitative Sustainability Text Identification",
                "High Potential Greenwashing Detection"
            ],
            multiselect=True,
            label="Select Tasks"
        )

        run_tasks_btn_2 = gr.Button("Run", variant="primary")

        chart_tasks_2 = gr.Plot(value=_empty_plot())
        download_2 = gr.File(label="Download Results")

        # ---------- Quality Filter ----------
        with gr.Row():

            # ---------- INFORMATIVE / VAGUE ----------
            with gr.Column(visible=True) as quality1_container:
                gr.Markdown("### Informative vs Non-Informative/Vague")
        
                quality1_gallery = gr.Gallery(
                    value=quality_task_1_gallery,
                    columns=2,
                    allow_preview=False
                )
        
            # ---------- QUALITATIVE / QUANTITATIVE ----------
            with gr.Column(visible=True) as quality2_container:
        
                gr.Markdown("### Qualitative vs Quantitative")
        
                quality2_gallery = gr.Gallery(
                    value=quality_task_2_gallery,
                    columns=2,
                    allow_preview=False
                )
        
            # ---------- GREENWASHING ----------
            with gr.Column(visible=True) as quality3_container:
        
                gr.Markdown("### Greenwashing Potential")
        
                quality3_gallery = gr.Gallery(
                    value=quality_task_3_gallery,
                    columns=2,
                    allow_preview=False
                )

        quality_result_table = gr.Dataframe(value=_empty_df(), interactive=True)
        
        # ---------- Gallery Events ----------
        quality1_gallery.select(
            fn=filter_quality_1,
            outputs=[quality_result_table, text]
        )

        quality2_gallery.select(
            fn=filter_quality_2,
            outputs=[quality_result_table, text]
        )

        quality3_gallery.select(
            fn=filter_quality_3,
            outputs=[quality_result_table, text]
        )

        # ---------- TOGGLE FILTERS ----------
        task_selector_2.change(
            fn=toggle_quality_filters,
            inputs=task_selector_2,
            outputs=[
                quality1_container,
                quality2_container,
                quality3_container
            ]
        )

        # ---------- RUN STEP 4 ----------
        run_tasks_btn_2.click(
            run_selected_tasks,
            inputs=task_selector_2,
            outputs=[download_2, table, chart_tasks_2]
        )
            
        # =========================
        # STAGE 5: CLIMATE ANALYSIS
        # =========================
        gr.Markdown("## Step 5: Climate-Specific Analysis")
        step_info(5, [
            "Climate Alignment",
            "GRI Climate Alignment",
            "Climate Action (SDG13) Alignment",
            "GRI Climate Action (SDG13) Alignment",
        ])

        task_selector_3 = gr.Dropdown(
            choices=[
                "Climate Alignment",
                "GRI Climate Alignment",
                "GRI Climate Action (SDG13) Alignment",
                "Climate Action (SDG13) Alignment"
            ],
            multiselect=True,
            label="Select Tasks"
        )

        run_tasks_btn_3 = gr.Button("Run", variant="primary")

        chart_tasks_3 = gr.Plot(value=_empty_plot())
        download_3 = gr.File(label="Download Results")

        # ---------- Climate Filter ----------
        with gr.Row():

            # ---------- Climate Alignment ----------
            with gr.Column(visible=True) as climate1_container:
                gr.Markdown("### Climate Alignment")
        
                climate1_gallery = gr.Gallery(
                    value=climate_images,
                    columns=2,
                    #height=130,
                    allow_preview=False
                )
        
            # ---------- GRI Climate Alignment ----------
            with gr.Column(visible=True) as climate2_container:
                gr.Markdown("### GRI Climate Alignment")
        
                climate2_gallery = gr.Gallery(
                    value=gri_climate_images,
                    columns=4,
                    #height=130,
                    allow_preview=False
                )

        # shared table ROW 1
        climate_table_1 = gr.Dataframe(value=_empty_df(), interactive=True)

        with gr.Row():

            # ---------- Climate Action SDG13 ----------
            with gr.Column(visible=True) as climate3_container:
                gr.Markdown("### Climate Action (SDG13)")
        
                climate3_gallery = gr.Gallery(
                    value=sdg13_images,
                    columns=2,
                    #height=130,
                    allow_preview=False
                )
        
            # ---------- GRI SDG13 ----------
            with gr.Column(visible=True) as climate4_container:
                gr.Markdown("### GRI Climate Action (SDG13)")
        
                climate4_gallery = gr.Gallery(
                    value=gri_sdg13_images,
                    columns=3,
                    #height=130,
                    allow_preview=False
                )

        # shared table ROW 2
        climate_table_2 = gr.Dataframe(value=_empty_df(), interactive=True)

        # ---------- Gallery Events ----------
        climate1_gallery.select(
            fn=filter_climate,
            outputs=[climate_table_1, text]
        )
        
        climate2_gallery.select(
            fn=filter_gri_climate,
            outputs=[climate_table_1, text]
        )
        
        climate3_gallery.select(
            fn=filter_sdg13,
            outputs=[climate_table_2, text]
        )
        
        climate4_gallery.select(
            fn=filter_gri_sdg13,
            outputs=[climate_table_2, text]
        )

        # ---------- CONNECT TO DROPDOWN ----------
        task_selector_3.change(
            fn=toggle_climate,
            inputs=task_selector_3,
            outputs=[
                climate1_container,
                climate2_container,
                climate3_container,
                climate4_container
            ]
        )

        # ---------- RUN STEP 5 ----------
        run_tasks_btn_3.click(
            run_selected_tasks,
            inputs=task_selector_3,
            outputs=[download_3, table, chart_tasks_3]
        )

        # --- citation footer ---
        gr.Markdown(CITE_FOOTER_MD)

        toggle_containers = [
            sdg_container, gri_container,
            quality1_container, quality2_container, quality3_container,
            climate1_container, climate2_container, climate3_container, climate4_container
        ]

        def _hide_all_toggle_containers():
            return [gr.update(visible=False) for _ in toggle_containers]

        demo.load(_hide_all_toggle_containers, outputs=toggle_containers)

        return demo