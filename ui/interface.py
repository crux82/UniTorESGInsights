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

        # =========================
        # STAGE 1: PDF → CSV
        # =========================
        gr.Markdown("## Step 1: Upload PDF and Extract Data")

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
        gr.Markdown("## Step 2: Sustainability Frameworks (GRI & SDG) Alignment (SFA) for Relevant/Irrelevant Classification Task")

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
        gr.Markdown("## Step 5: More Specific Climate Analysis")

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

        toggle_containers = [
            sdg_container, gri_container,
            quality1_container, quality2_container, quality3_container,
            climate1_container, climate2_container, climate3_container, climate4_container
        ]

        def _hide_all_toggle_containers():
            return [gr.update(visible=False) for _ in toggle_containers]

        demo.load(_hide_all_toggle_containers, outputs=toggle_containers)

        return demo