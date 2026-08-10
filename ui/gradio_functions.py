import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gradio as gr

from ui.state import STATE
from ui.charts import BASE_COLORS, get_shades

from pdf_processing.pdf_utils import (
    process_pdf,
    pdf_to_images
)

from models.model_loader import get_model
from models.predictor import (
    predict,
    predict_with_model
)

from configs.sdg_labels import SDG_LABELS

# =========================
# LOAD PDF
# =========================
def load_pdf(file):
    path = file.name
    STATE["pdf"] = path

    csv_path = "extracted.csv"
    process_pdf(path, csv_path)

    df = pd.read_csv(csv_path)
    STATE["df"] = df
    STATE["images"] = pdf_to_images(path)
    STATE["page"] = 0

    return STATE["images"][0], df[df["Page_num"] == 1]


# =========================
# PAGE NAVIGATION
# =========================
def change_page(step):
    STATE["page"] = max(0, min(STATE["page"] + step, len(STATE["images"]) - 1))
    df = STATE["df"]
    return STATE["images"][STATE["page"]], df[df["Page_num"] == STATE["page"] + 1]

# =========================
# TABLE HIGHLIGHT
# =========================
def highlight(evt: gr.SelectData):
    df = STATE["df"]
    page_df = df[df["Page_num"] == STATE["page"] + 1].reset_index(drop=True)
    return page_df.iloc[evt.index[0]]["Paragraph_content"]

# =========================
# PDF WRAPPER
# =========================
def load_pdf_wrapper(file):
    img_out, df_out = load_pdf(file)
    return img_out, df_out, "extracted.csv"

# =========================
# CSV OVERRIDE
# =========================
def upload_csv1(file):
    df = pd.read_csv(file.name)
    STATE["df"] = df
    return df

def upload_csv2(file):
    df = pd.read_csv(file.name)
    STATE["df"] = df
    return df

# =========================
# RUN SA
# =========================
def run_sa_wrapper():

    df = STATE["df"].copy()

    bundle = get_model("SA")

    preds = predict_with_model(         
        df["Paragraph_content"].tolist(),
        bundle
    )

    df["SA_label"] = preds
    STATE["df"] = df

    out = "SFA_results.csv"
    df.to_csv(out, index=False)

    # Distribution plot
    counts = df["SA_label"].value_counts().reset_index()
    counts.columns = ["Label", "Count"]
    counts["Percentage"] = counts["Count"] / counts["Count"].sum() * 100

    fig1 = px.bar(
        counts,
        x="Label",
        y="Count",
        color="Label",
        text=counts["Percentage"].round(1).astype(str) + "%",
        title="SA Label Distribution"
    )
    fig1.update_traces(textposition="outside")


    return out, df[df["Page_num"] == STATE["page"] + 1], fig1

# =========================
# SET TASK
# =========================
def set_task(task):
    STATE["selected_task"] = task

    
# =========================
# SINGLE TASK RUNNER
# =========================
def run_task():

    df = STATE["df"].copy()
    task = STATE["selected_task"]

    bundle = get_model(task)

    preds = predict(
        df["Paragraph_content"].tolist(),
        bundle
    )

    # SDG mapping (for both CSV + charts)
    if task == "17 SDG Alignment":
        preds = [SDG_LABELS.get(p, p) for p in preds]

    df[f"{task}_label"] = preds
    STATE["df"] = df

    out = f"{task}_results.csv"
    df.to_csv(out, index=False)

    # only remove N/A for chart
    valid_values = df[f"{task}_label"][df[f"{task}_label"] != "N/A"]

    counts = valid_values.value_counts().reset_index()
    counts.columns = ["Label", "Count"]

    fig = px.bar(counts, x="Label", y="Count", title=f"{task} Distribution")

    return out, df[df["Page_num"] == STATE["page"] + 1], fig

# =========================
# SHARED TASK RUNNER
# =========================
def run_selected_tasks(tasks):

    df = STATE["df"].copy()

    # Only run on Relevant paragraphs
    mask = df["SA_label"] == "Relevant"

    all_data = []

    for task in tasks:

        bundle = get_model(task)

        texts = df.loc[mask, "Paragraph_content"].tolist()

        if len(texts) > 0:
            preds = predict(texts, bundle)

            # SDG mapping applied immediately
            if task == "17 SDG Alignment":
                preds = [SDG_LABELS.get(p, p) for p in preds]

            df.loc[mask, task] = preds

        df.loc[~mask, task] = "N/A"


        # CHART ONLY: remove N/A
        valid_values = df[task][df[task] != "N/A"]

        counts = valid_values.value_counts().reset_index()
        counts.columns = ["value", "count"]
        counts["task"] = task

        base = BASE_COLORS.get(task, "#999999")
        counts["color"] = get_shades(base, len(counts))

        all_data.append(counts)


    # combine all tasks
    plot_df = pd.concat(all_data)

    # SINGLE INTERACTIVE CHART
    fig = go.Figure()

    for task in plot_df["task"].unique():
        sub = plot_df[plot_df["task"] == task]

        fig.add_bar(
            x=sub["value"],
            y=sub["count"],
            name=task,
            marker_color=sub["color"]
        )

    fig.update_layout(
        title="Task Distribution Dashboard",
        barmode="group"
    )


    STATE["df"] = df

    out = "results.csv"
    df.to_csv(out, index=False)


    return out, df[df["Page_num"] == STATE["page"] + 1], fig