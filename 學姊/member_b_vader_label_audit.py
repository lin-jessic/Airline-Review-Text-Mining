# member_b_vader_label_audit.py
# Member B - VADER label audit using dataset-provided rating and recommendation fields
#
# Purpose:
# This script DOES NOT rerun VADER.
# It reads the final VADER result produced by member_b_vader_full_validation.py
# and creates additional proxy labels from the dataset's own fields:
#   1. Recommended-based label: yes -> positive, no -> negative
#   2. Rating-based label: OverallScore >= 7 -> positive, 5-6 -> neutral, <=4 -> negative
#   3. High-confidence proxy label: OverallScore <=4 and Recommended=no -> negative;
#                                OverallScore >=7 and Recommended=yes -> positive
#
# Why this is useful:
# - It supports the VADER result using the dataset's own labels.
# - It avoids manually reading thousands of reviews one by one.
# - It keeps the strict high-confidence proxy validation separate from a broader all-data audit.
#
# Important:
# - High-confidence proxy is the PRIMARY validation because it is less noisy.
# - All-data Recommended / Rating labels are used as SUPPLEMENTARY evidence.
# - This script does NOT change LDA, TF-IDF, BERTopic, sampling, or the VADER scores.

from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "output_vader_full"
OUTPUT_DIR = BASE_DIR / "output_vader_label_audit"
OUTPUT_DIR.mkdir(exist_ok=True)

FINAL_VADER_FILE = INPUT_DIR / "vader_final_sentiment_results.csv"


def normalize_rec(x):
    return str(x).strip().lower()


def label_from_recommended(rec):
    rec = normalize_rec(rec)
    if rec == "yes":
        return "positive"
    if rec == "no":
        return "negative"
    return "unknown"


def label_from_rating(score):
    try:
        score = float(score)
    except Exception:
        return "unknown"

    if score >= 7:
        return "positive"
    if score <= 4:
        return "negative"
    return "neutral"


def high_confidence_proxy(row):
    rec = normalize_rec(row.get("Recommended", ""))
    try:
        score = float(row.get("OverallScore"))
    except Exception:
        return "unknown"

    if score <= 4 and rec == "no":
        return "negative"
    if score >= 7 and rec == "yes":
        return "positive"
    return "unknown"


def label_consistency_type(row):
    rec_label = row["dataset_label_recommended"]
    rating_label = row["dataset_label_rating"]

    if rec_label == "unknown" or rating_label == "unknown":
        return "unknown"

    if rating_label == "neutral":
        return "medium_rating"

    if rec_label == rating_label:
        return "consistent"

    return "conflict"


def evaluate_binary(df, true_col, pred_col, label_name):
    eval_df = df[df[true_col].isin(["positive", "negative"]) & df[pred_col].isin(["positive", "negative"])].copy()

    if len(eval_df) == 0:
        return {
            "label_source": label_name,
            "n_used": 0,
            "accuracy": np.nan,
            "precision_macro": np.nan,
            "recall_macro": np.nan,
            "f1_macro": np.nan,
            "positive_count": 0,
            "negative_count": 0,
            "note": "No valid positive/negative rows available."
        }

    y_true = eval_df[true_col]
    y_pred = eval_df[pred_col]

    return {
        "label_source": label_name,
        "n_used": int(len(eval_df)),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision_macro": round(float(precision_score(y_true, y_pred, labels=["positive", "negative"], average="macro", zero_division=0)), 4),
        "recall_macro": round(float(recall_score(y_true, y_pred, labels=["positive", "negative"], average="macro", zero_division=0)), 4),
        "f1_macro": round(float(f1_score(y_true, y_pred, labels=["positive", "negative"], average="macro", zero_division=0)), 4),
        "positive_count": int((eval_df[true_col] == "positive").sum()),
        "negative_count": int((eval_df[true_col] == "negative").sum()),
        "note": "Binary comparison using positive/negative labels only."
    }


def evaluate_three_class(df, true_col, pred_col, label_name):
    eval_df = df[df[true_col].isin(["positive", "neutral", "negative"]) & df[pred_col].isin(["positive", "neutral", "negative"])].copy()

    if len(eval_df) == 0:
        return {
            "label_source": label_name,
            "n_used": 0,
            "accuracy": np.nan,
            "precision_macro": np.nan,
            "recall_macro": np.nan,
            "f1_macro": np.nan,
            "positive_count": 0,
            "neutral_count": 0,
            "negative_count": 0,
            "note": "No valid three-class rows available."
        }

    y_true = eval_df[true_col]
    y_pred = eval_df[pred_col]

    return {
        "label_source": label_name,
        "n_used": int(len(eval_df)),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision_macro": round(float(precision_score(y_true, y_pred, labels=["positive", "neutral", "negative"], average="macro", zero_division=0)), 4),
        "recall_macro": round(float(recall_score(y_true, y_pred, labels=["positive", "neutral", "negative"], average="macro", zero_division=0)), 4),
        "f1_macro": round(float(f1_score(y_true, y_pred, labels=["positive", "neutral", "negative"], average="macro", zero_division=0)), 4),
        "positive_count": int((eval_df[true_col] == "positive").sum()),
        "neutral_count": int((eval_df[true_col] == "neutral").sum()),
        "negative_count": int((eval_df[true_col] == "negative").sum()),
        "note": "Three-class comparison. Rating 5-6 is treated as neutral."
    }


def save_confusion_matrix(df, true_col, pred_col, labels, filename):
    eval_df = df[df[true_col].isin(labels) & df[pred_col].isin(labels)].copy()
    if eval_df.empty:
        return

    cm = confusion_matrix(eval_df[true_col], eval_df[pred_col], labels=labels)
    cm_df = pd.DataFrame(cm, index=[f"true_{x}" for x in labels], columns=[f"pred_{x}" for x in labels])
    cm_df.to_csv(OUTPUT_DIR / filename, encoding="utf-8-sig")


def plot_accuracy(metrics_df):
    plot_df = metrics_df.dropna(subset=["accuracy"]).copy()
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(plot_df["label_source"], plot_df["accuracy"])
    ax.set_title("VADER Alignment with Dataset-derived Proxy Labels", fontsize=14, fontweight="bold")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=20)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.3f}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_vader_dataset_label_alignment.png", dpi=180, bbox_inches="tight")
    plt.close()


def write_summary(df, metrics_df):
    lines = []
    lines.append("VADER Dataset Label Audit Summary")
    lines.append("=" * 72)
    lines.append("")
    lines.append("Purpose")
    lines.append("-" * 72)
    lines.append("This audit compares the final VADER labels with dataset-derived proxy labels.")
    lines.append("The labels are created automatically from the dataset's OverallScore and Recommended fields,")
    lines.append("so we do not need to manually read and label thousands of reviews.")
    lines.append("")
    lines.append("Important Methodological Note")
    lines.append("-" * 72)
    lines.append("This is not manual human annotation. It is automatic proxy labeling based on existing dataset fields.")
    lines.append("High-confidence proxy labels remain the strictest validation source.")
    lines.append("Recommended-based and rating-based labels are supplementary evidence because they may contain noise.")
    lines.append("")
    lines.append("Dataset Coverage")
    lines.append("-" * 72)
    lines.append(f"Total reviews in final VADER result: {len(df)}")
    lines.append(f"Recommended = yes: {int((df['Recommended'].astype(str).str.lower() == 'yes').sum())}")
    lines.append(f"Recommended = no : {int((df['Recommended'].astype(str).str.lower() == 'no').sum())}")
    lines.append(f"High-confidence proxy rows: {int((df['dataset_label_high_confidence'] != 'unknown').sum())}")
    lines.append(f"Recommended-based label rows: {int((df['dataset_label_recommended'] != 'unknown').sum())}")
    lines.append(f"Rating-based label rows: {int((df['dataset_label_rating'] != 'unknown').sum())}")
    lines.append("")
    lines.append("Consistency between Recommended and Rating")
    lines.append("-" * 72)
    consistency_counts = df["dataset_label_consistency"].value_counts().to_dict()
    for key, value in consistency_counts.items():
        lines.append(f"{key}: {value}")
    lines.append("")
    lines.append("Alignment Metrics")
    lines.append("-" * 72)
    for _, row in metrics_df.iterrows():
        lines.append(
            f"{row['label_source']} | n={row['n_used']} | "
            f"accuracy={row['accuracy']} | macro_f1={row['f1_macro']} | note={row['note']}"
        )
    lines.append("")
    lines.append("Recommended Report Wording")
    lines.append("-" * 72)
    lines.append(
        "To further support the VADER sentiment results, we created automatic proxy labels from the dataset's "
        "Recommended and OverallScore fields. The strictest validation used high-confidence proxy labels, "
        "where low ratings with not recommended reviews were treated as negative and high ratings with recommended "
        "reviews were treated as positive. All 20,000 reviews were scored by VADER, while the high-confidence subset "
        "was used for the main validation."
    )

    with open(OUTPUT_DIR / "vader_dataset_label_audit_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    if not FINAL_VADER_FILE.exists():
        raise FileNotFoundError(
            f"Cannot find {FINAL_VADER_FILE}. Please run member_b_vader_full_validation.py first."
        )

    df = pd.read_csv(FINAL_VADER_FILE)

    required_cols = ["Review", "Recommended", "OverallScore", "vader_final_label", "vader_final_score"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in final VADER result: {missing}")

    df["Recommended"] = df["Recommended"].apply(normalize_rec)
    df["OverallScore"] = pd.to_numeric(df["OverallScore"], errors="coerce")

    df["dataset_label_recommended"] = df["Recommended"].apply(label_from_recommended)
    df["dataset_label_rating"] = df["OverallScore"].apply(label_from_rating)
    df["dataset_label_high_confidence"] = df.apply(high_confidence_proxy, axis=1)
    df["dataset_label_consistency"] = df.apply(label_consistency_type, axis=1)

    metrics = []
    metrics.append(evaluate_binary(df, "dataset_label_high_confidence", "vader_final_label", "high_confidence_rating_recommendation_proxy"))
    metrics.append(evaluate_binary(df, "dataset_label_recommended", "vader_final_label", "all_20k_recommended_label_proxy"))
    metrics.append(evaluate_three_class(df, "dataset_label_rating", "vader_final_label", "all_20k_rating_label_proxy_three_class"))

    metrics_df = pd.DataFrame(metrics)

    df.to_csv(OUTPUT_DIR / "vader_final_with_dataset_proxy_labels.csv", index=False, encoding="utf-8-sig")
    metrics_df.to_csv(OUTPUT_DIR / "vader_dataset_label_alignment_metrics.csv", index=False, encoding="utf-8-sig")

    save_confusion_matrix(df, "dataset_label_high_confidence", "vader_final_label", ["positive", "negative"], "confusion_high_confidence_proxy.csv")
    save_confusion_matrix(df, "dataset_label_recommended", "vader_final_label", ["positive", "negative"], "confusion_recommended_proxy.csv")
    save_confusion_matrix(df, "dataset_label_rating", "vader_final_label", ["positive", "neutral", "negative"], "confusion_rating_proxy_three_class.csv")

    conflict_df = df[df["dataset_label_consistency"] == "conflict"].copy()
    conflict_df.to_csv(OUTPUT_DIR / "dataset_rating_recommended_conflict_cases.csv", index=False, encoding="utf-8-sig")

    plot_accuracy(metrics_df)
    write_summary(df, metrics_df)

    print("=" * 72)
    print("VADER dataset label audit finished.")
    print(f"All outputs are saved in: {OUTPUT_DIR}")
    print(metrics_df.to_string(index=False))


if __name__ == "__main__":
    main()
