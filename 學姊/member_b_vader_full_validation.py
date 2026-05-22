# member_b_vader_full_validation.py
# Member B - Advanced VADER validation and full 20k re-scoring
#
# Purpose:
# 1. Compare original/native VADER vs aviation-domain adjusted VADER.
# 2. Compare full-review scoring vs sentence-by-sentence average scoring.
# 3. Compare sentiment thresholds: +/-0.05, +/-0.10, +/-0.30.
# 4. Use all high-confidence proxy-labeled reviews for validation, not only 100 samples.
# 5. Re-score the full sampled_20k_with_tokens.csv dataset with all methods.
# 6. Export the final selected VADER result and summary tables to output_vader_full/.
#
# Important:
# - This script only updates sentiment/VADER outputs.
# - It does NOT modify TF-IDF, LDA, BERTopic, topic modeling results, or sampling.
# - Original/native VADER results are preserved for comparison.
# - Aviation lexicon adjustment is clearly logged and compared against original VADER.

from pathlib import Path
import re
import json
import warnings
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

warnings.filterwarnings("ignore")


# =========================================================
# 0. Global settings
# =========================================================

RANDOM_STATE = 42
THRESHOLDS = [0.05, 0.10, 0.30]
OUTPUT_DIR_NAME = "output_vader_full"

# The teacher mentioned full review vs sentence-by-sentence.
# Following the user's requirement, sentence splitting is based on period ".".
SENTENCE_SPLIT_MODE = "period_only"

# For validation, use all high-confidence proxy labels rather than only 100 samples.
# Still exports a 100-row sample for teacher-reference if needed.
USE_ALL_PROXY_FOR_VALIDATION = True
PROXY_SAMPLE_PER_CLASS = 50

# Passenger-review-oriented categories based on the uploaded PDF description.
# The code still reads the full CSV, but by default only applies passenger-relevant terms
# to avoid over-adjusting safety-report-only vocabulary for passenger reviews.
PASSENGER_REVIEW_CATEGORIES = {
    "service", "comfort", "schedule", "pricing", "communication",
    "baggage", "operations", "emotion"
}

# If True, only terms with passenger domain or passenger-relevant categories are applied.
# This is more conservative and suitable for airline passenger reviews.
USE_PASSENGER_REVIEW_FILTER = True

# VADER score range is approximately -4 to +4 internally.
# The uploaded aviation lexicon uses -3 to +3. We keep the original score scale.
MIN_VADER_LEXICON_SCORE = -4.0
MAX_VADER_LEXICON_SCORE = 4.0


# =========================================================
# 1. Path helpers
# =========================================================

def get_base_dir() -> Path:
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()


BASE_DIR = get_base_dir()
OUTPUT_DIR = BASE_DIR / OUTPUT_DIR_NAME
OUTPUT_DIR.mkdir(exist_ok=True)


def find_file(filename: str, required: bool = True) -> Path:
    """Find a file in the project root or data/ folder."""
    candidates = [
        BASE_DIR / filename,
        BASE_DIR / "data" / filename,
        BASE_DIR.parent / filename,
        BASE_DIR.parent / "data" / filename,
        Path.cwd() / filename,
        Path.cwd() / "data" / filename,
    ]
    for path in candidates:
        if path.exists():
            return path

    if required:
        raise FileNotFoundError(
            f"Cannot find {filename}. Please place it in the project root folder "
            f"or in a data/ folder."
        )
    return None


# =========================================================
# 2. Basic text / sentiment helpers
# =========================================================

def normalize_recommended(value) -> str:
    return str(value).strip().lower()


def split_sentences_by_period(text: str) -> List[str]:
    """
    Split one review into sentences based on period only.
    This follows the user's requirement: whenever a period "." appears, treat it as a sentence boundary.
    Empty pieces are removed.
    """
    text = str(text).replace("\n", " ").replace("\r", " ").strip()
    parts = [p.strip() for p in text.split(".")]
    return [p for p in parts if p]


def label_by_threshold(score: float, threshold: float) -> str:
    if score >= threshold:
        return "positive"
    if score <= -threshold:
        return "negative"
    return "neutral"


def proxy_label(row) -> str:
    """High-confidence proxy label based on rating and Recommended."""
    rating = row.get("OverallScore")
    rec = row.get("Recommended")
    if pd.notna(rating) and rating <= 4 and rec == "no":
        return "negative"
    if pd.notna(rating) and rating >= 7 and rec == "yes":
        return "positive"
    return "unknown"


def safe_float(value, default=np.nan):
    try:
        return float(value)
    except Exception:
        return default


# =========================================================
# 3. Aviation lexicon loading and preprocessing
# =========================================================

def standardize_lexicon_df(df: pd.DataFrame, source_file: str) -> pd.DataFrame:
    """Validate and standardize aviation lexicon dataframe."""
    required_cols = ["term", "polarity", "score", "category", "domain"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"{source_file} is missing columns: {missing}")

    out = df[required_cols].copy()
    out["term"] = out["term"].astype(str).str.strip().str.lower()
    out["polarity"] = out["polarity"].astype(str).str.strip().str.lower()
    out["category"] = out["category"].astype(str).str.strip().str.lower()
    out["domain"] = out["domain"].astype(str).str.strip().str.lower()
    out["score"] = pd.to_numeric(out["score"], errors="coerce")
    out["source_file"] = source_file

    out = out[(out["term"] != "") & out["score"].notna()].copy()
    out["score"] = out["score"].clip(MIN_VADER_LEXICON_SCORE, MAX_VADER_LEXICON_SCORE)

    return out


def load_aviation_lexicon() -> pd.DataFrame:
    """
    Load the three uploaded aviation lexicon CSV files.
    The full CSV is used as the primary source. Positive/negative CSV files are also read
    and merged for consistency checking.
    """
    full_path = find_file("aviation_sentiment_lexicon_full.csv", required=True)
    pos_path = find_file("aviation_positive_lexicon.csv", required=False)
    neg_path = find_file("aviation_negative_lexicon.csv", required=False)

    frames = []
    frames.append(standardize_lexicon_df(pd.read_csv(full_path), full_path.name))

    if pos_path is not None:
        frames.append(standardize_lexicon_df(pd.read_csv(pos_path), pos_path.name))
    if neg_path is not None:
        frames.append(standardize_lexicon_df(pd.read_csv(neg_path), neg_path.name))

    lex = pd.concat(frames, ignore_index=True)

    # Deduplicate by term. If duplicates exist, keep the strongest absolute score.
    lex["abs_score"] = lex["score"].abs()
    lex = lex.sort_values(["term", "abs_score"], ascending=[True, False])
    lex = lex.drop_duplicates(subset=["term"], keep="first").drop(columns=["abs_score"])

    # Conservative passenger-review filtering.
    if USE_PASSENGER_REVIEW_FILTER:
        lex["is_passenger_relevant"] = (
            (lex["domain"] == "passenger") |
            (lex["category"].isin(PASSENGER_REVIEW_CATEGORIES))
        )
        applied = lex[lex["is_passenger_relevant"]].copy()
    else:
        lex["is_passenger_relevant"] = True
        applied = lex.copy()

    # Prepare VADER-ready keys.
    # For phrase terms, add underscore version and use phrase preprocessing.
    applied["vader_key"] = applied["term"].str.replace(r"\s+", "_", regex=True)
    applied["is_phrase"] = applied["term"].str.contains(r"\s+", regex=True)

    # Save lexicon audit outputs.
    lex.to_csv(OUTPUT_DIR / "aviation_lexicon_loaded_all_terms.csv", index=False, encoding="utf-8-sig")
    applied.to_csv(OUTPUT_DIR / "aviation_lexicon_applied_to_vader.csv", index=False, encoding="utf-8-sig")

    return applied


def build_domain_lexicon_dict(applied_lexicon: pd.DataFrame) -> Dict[str, float]:
    """
    Build dictionary for analyzer.lexicon.update().
    Uses underscore phrase keys for multi-word expressions.
    """
    lex_dict = {}
    for _, row in applied_lexicon.iterrows():
        key = str(row["vader_key"]).strip().lower()
        score = float(row["score"])
        if key:
            lex_dict[key] = score
    return lex_dict


def preprocess_phrases_for_vader(text: str, phrase_terms: List[str]) -> str:
    """
    Replace aviation phrase terms with underscore keys so VADER can match them as one lexicon item.
    Example: "bad service" -> "bad_service".
    """
    text = str(text)
    processed = text.lower()

    # Longer phrases first to avoid partial replacement issues.
    for phrase in sorted(phrase_terms, key=len, reverse=True):
        phrase = phrase.strip().lower()
        if not phrase or " " not in phrase:
            continue
        key = phrase.replace(" ", "_")
        pattern = r"\b" + re.escape(phrase) + r"\b"
        processed = re.sub(pattern, key, processed, flags=re.IGNORECASE)

    return processed


def make_analyzer(adjusted: bool, applied_lexicon: pd.DataFrame = None) -> Tuple[SentimentIntensityAnalyzer, List[str]]:
    analyzer = SentimentIntensityAnalyzer()
    phrase_terms = []

    if adjusted:
        if applied_lexicon is None or applied_lexicon.empty:
            raise ValueError("Adjusted analyzer requires aviation lexicon.")
        lex_dict = build_domain_lexicon_dict(applied_lexicon)
        analyzer.lexicon.update(lex_dict)
        phrase_terms = applied_lexicon.loc[applied_lexicon["is_phrase"], "term"].astype(str).tolist()

    return analyzer, phrase_terms


# =========================================================
# 4. VADER scoring methods
# =========================================================

def score_full_review(text: str, analyzer: SentimentIntensityAnalyzer, adjusted: bool = False, phrase_terms: List[str] = None) -> float:
    if adjusted and phrase_terms:
        text = preprocess_phrases_for_vader(text, phrase_terms)
    return analyzer.polarity_scores(str(text))["compound"]


def score_sentence_average(text: str, analyzer: SentimentIntensityAnalyzer, adjusted: bool = False, phrase_terms: List[str] = None) -> float:
    sentences = split_sentences_by_period(text)
    if not sentences:
        return 0.0

    scores = []
    for sent in sentences:
        if adjusted and phrase_terms:
            sent = preprocess_phrases_for_vader(sent, phrase_terms)
        scores.append(analyzer.polarity_scores(str(sent))["compound"])

    return float(np.mean(scores)) if scores else 0.0


def add_all_vader_scores(df: pd.DataFrame, applied_lexicon: pd.DataFrame) -> pd.DataFrame:
    """Compute four scoring methods for the full dataset."""
    print("Preparing VADER analyzers...")
    original_analyzer, _ = make_analyzer(adjusted=False)
    adjusted_analyzer, phrase_terms = make_analyzer(adjusted=True, applied_lexicon=applied_lexicon)

    out = df.copy()

    print("Scoring: original VADER + full review...")
    out["vader_original_full"] = out["Review"].apply(
        lambda x: score_full_review(x, original_analyzer, adjusted=False)
    )

    print("Scoring: original VADER + sentence average...")
    out["vader_original_sentence_avg"] = out["Review"].apply(
        lambda x: score_sentence_average(x, original_analyzer, adjusted=False)
    )

    print("Scoring: adjusted aviation VADER + full review...")
    out["vader_adjusted_full"] = out["Review"].apply(
        lambda x: score_full_review(x, adjusted_analyzer, adjusted=True, phrase_terms=phrase_terms)
    )

    print("Scoring: adjusted aviation VADER + sentence average...")
    out["vader_adjusted_sentence_avg"] = out["Review"].apply(
        lambda x: score_sentence_average(x, adjusted_analyzer, adjusted=True, phrase_terms=phrase_terms)
    )

    return out


# =========================================================
# 5. Validation metrics
# =========================================================

def evaluate_method_threshold(proxy_df: pd.DataFrame, score_col: str, threshold: float) -> Dict:
    temp = proxy_df.copy()
    temp["pred_label"] = temp[score_col].apply(lambda s: label_by_threshold(s, threshold))

    # Accuracy for three classes including neutral.
    # Since proxy labels only have positive/negative, neutral predictions count as incorrect.
    y_true = temp["proxy_label"].tolist()
    y_pred = temp["pred_label"].tolist()

    labels = ["negative", "positive"]
    binary_eval = temp[temp["pred_label"].isin(labels)].copy()

    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, labels=["negative", "positive"], average="macro", zero_division=0)
    precision = precision_score(y_true, y_pred, labels=["negative", "positive"], average="macro", zero_division=0)
    recall = recall_score(y_true, y_pred, labels=["negative", "positive"], average="macro", zero_division=0)

    neutral_rate = float((temp["pred_label"] == "neutral").mean())

    neg_df = temp[temp["proxy_label"] == "negative"]
    pos_df = temp[temp["proxy_label"] == "positive"]

    neg_acc = accuracy_score(neg_df["proxy_label"], neg_df["pred_label"]) if len(neg_df) else np.nan
    pos_acc = accuracy_score(pos_df["proxy_label"], pos_df["pred_label"]) if len(pos_df) else np.nan

    return {
        "score_column": score_col,
        "threshold": threshold,
        "n_proxy_reviews": len(temp),
        "accuracy": round(float(acc), 4),
        "macro_f1": round(float(macro_f1), 4),
        "macro_precision": round(float(precision), 4),
        "macro_recall": round(float(recall), 4),
        "neutral_rate": round(float(neutral_rate), 4),
        "negative_accuracy": round(float(neg_acc), 4) if pd.notna(neg_acc) else np.nan,
        "positive_accuracy": round(float(pos_acc), 4) if pd.notna(pos_acc) else np.nan,
        "negative_count": int(len(neg_df)),
        "positive_count": int(len(pos_df)),
    }


def run_validation(scored_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
    """Run threshold, input-form, and adjusted-vs-original validation."""
    proxy_df = scored_df[scored_df["proxy_label"].isin(["negative", "positive"])].copy()

    if proxy_df.empty:
        raise ValueError("No proxy-labeled reviews found. Please check OverallScore and Recommended columns.")

    score_cols = [
        "vader_original_full",
        "vader_original_sentence_avg",
        "vader_adjusted_full",
        "vader_adjusted_sentence_avg",
    ]

    rows = []
    for col in score_cols:
        for threshold in THRESHOLDS:
            rows.append(evaluate_method_threshold(proxy_df, col, threshold))

    validation_df = pd.DataFrame(rows)
    validation_df.to_csv(OUTPUT_DIR / "vader_threshold_method_comparison_all_proxy.csv", index=False, encoding="utf-8-sig")

    # Select best configuration: highest accuracy, then highest macro_f1, then lower neutral_rate.
    best_row = validation_df.sort_values(
        by=["accuracy", "macro_f1", "neutral_rate"],
        ascending=[False, False, True]
    ).iloc[0].to_dict()

    # A compact input-form comparison at each method's best threshold.
    method_best = validation_df.sort_values(
        by=["score_column", "accuracy", "macro_f1", "neutral_rate"],
        ascending=[True, False, False, True]
    ).groupby("score_column", as_index=False).head(1)
    method_best.to_csv(OUTPUT_DIR / "vader_best_threshold_by_method.csv", index=False, encoding="utf-8-sig")

    # Export proxy sample 100 for teacher's original requirement reference.
    sample_parts = []
    for label in ["negative", "positive"]:
        part = proxy_df[proxy_df["proxy_label"] == label]
        n = min(PROXY_SAMPLE_PER_CLASS, len(part))
        sample_parts.append(part.sample(n=n, random_state=RANDOM_STATE))
    sample_100 = pd.concat(sample_parts, ignore_index=True).sample(frac=1, random_state=RANDOM_STATE)
    sample_100.to_csv(OUTPUT_DIR / "vader_proxy_sample_100_for_reference.csv", index=False, encoding="utf-8-sig")

    proxy_df.to_csv(OUTPUT_DIR / "vader_proxy_all_high_confidence_reviews.csv", index=False, encoding="utf-8-sig")

    return validation_df, method_best, best_row


# =========================================================
# 6. Final output generation
# =========================================================

def add_final_labels(scored_df: pd.DataFrame, best_config: Dict) -> pd.DataFrame:
    final_col = best_config["score_column"]
    final_threshold = float(best_config["threshold"])

    out = scored_df.copy()
    out["vader_final_score"] = out[final_col]
    out["vader_final_label"] = out["vader_final_score"].apply(lambda s: label_by_threshold(s, final_threshold))
    out["vader_final_score_source"] = final_col
    out["vader_final_threshold"] = final_threshold

    return out


def summarize_by_recommended(final_df: pd.DataFrame) -> pd.DataFrame:
    summary = final_df.groupby("Recommended").agg(
        review_count=("Review", "count"),
        avg_sentiment=("vader_final_score", "mean"),
        median_sentiment=("vader_final_score", "median"),
        positive_count=("vader_final_label", lambda x: int((x == "positive").sum())),
        neutral_count=("vader_final_label", lambda x: int((x == "neutral").sum())),
        negative_count=("vader_final_label", lambda x: int((x == "negative").sum())),
        avg_overall_score=("OverallScore", "mean"),
        avg_sentence_count=("sentence_count_period", "mean"),
    ).reset_index()

    for col in ["avg_sentiment", "median_sentiment", "avg_overall_score", "avg_sentence_count"]:
        summary[col] = summary[col].round(4)

    return summary


def build_sentence_statistics(df: pd.DataFrame) -> pd.DataFrame:
    stats = {
        "total_reviews": len(df),
        "avg_sentence_count_period": round(float(df["sentence_count_period"].mean()), 4),
        "median_sentence_count_period": round(float(df["sentence_count_period"].median()), 4),
        "reviews_over_5_sentences": int((df["sentence_count_period"] > 5).sum()),
        "share_over_5_sentences": round(float((df["sentence_count_period"] > 5).mean()), 4),
        "max_sentence_count_period": int(df["sentence_count_period"].max()),
        "split_mode": SENTENCE_SPLIT_MODE,
    }
    return pd.DataFrame([stats])


# =========================================================
# 7. Figures
# =========================================================

def plot_threshold_comparison(validation_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(11, 5))

    for score_col, group in validation_df.groupby("score_column"):
        group = group.sort_values("threshold")
        ax.plot(group["threshold"], group["accuracy"], marker="o", linewidth=2, label=score_col)

    ax.set_title("VADER Validation Accuracy by Threshold and Method", fontsize=13, fontweight="bold")
    ax.set_xlabel("Threshold (+/-)")
    ax.set_ylabel("Accuracy on high-confidence proxy labels")
    ax.set_xticks(THRESHOLDS)
    ax.legend(fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_vader_threshold_method_accuracy.png", dpi=180, bbox_inches="tight")
    plt.close()


def plot_method_best(method_best: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 5))
    labels = method_best["score_column"].tolist()
    values = method_best["accuracy"].astype(float).tolist()

    bars = ax.bar(labels, values)
    ax.set_title("Best Accuracy by VADER Scoring Method", fontsize=13, fontweight="bold")
    ax.set_ylabel("Best accuracy")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", labelrotation=20)
    ax.spines[["top", "right"]].set_visible(False)

    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:.3f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_vader_best_method_accuracy.png", dpi=180, bbox_inches="tight")
    plt.close()


def plot_final_sentiment_distribution(final_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 5))
    bins = np.linspace(-1, 1, 41)

    for rec in ["yes", "no"]:
        values = final_df[final_df["Recommended"] == rec]["vader_final_score"]
        ax.hist(values, bins=bins, alpha=0.62, label=f"Recommended = {rec}")

    ax.set_title("Final VADER Sentiment Distribution by Recommended", fontsize=13, fontweight="bold")
    ax.set_xlabel("Final VADER compound score")
    ax.set_ylabel("Number of reviews")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_vader_final_sentiment_distribution.png", dpi=180, bbox_inches="tight")
    plt.close()


def plot_final_avg_sentiment(summary_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    ordered = summary_df.set_index("Recommended").reindex(["yes", "no"]).reset_index()
    bars = ax.bar(ordered["Recommended"], ordered["avg_sentiment"])

    ax.set_title("Final Average VADER Sentiment by Recommended", fontsize=13, fontweight="bold")
    ax.set_xlabel("Recommended")
    ax.set_ylabel("Average sentiment score")
    ax.axhline(0, linewidth=1)
    ax.spines[["top", "right"]].set_visible(False)

    for bar in bars:
        value = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:.3f}", ha="center", va="bottom" if value >= 0 else "top")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_vader_final_avg_sentiment.png", dpi=180, bbox_inches="tight")
    plt.close()


# =========================================================
# 8. Reports
# =========================================================

def write_summary_report(
    df: pd.DataFrame,
    applied_lexicon: pd.DataFrame,
    validation_df: pd.DataFrame,
    method_best: pd.DataFrame,
    best_config: Dict,
    final_summary: pd.DataFrame,
    sentence_stats: pd.DataFrame,
):
    lines = []
    lines.append("Advanced VADER Validation and Full Re-scoring Summary")
    lines.append("=" * 72)
    lines.append("")
    lines.append("Purpose")
    lines.append("-" * 72)
    lines.append("This script validates and updates the VADER sentiment analysis method for the airline review project.")
    lines.append("It compares original VADER and aviation-domain adjusted VADER, full-review input and sentence-average input,")
    lines.append("and three thresholds: +/-0.05, +/-0.10, and +/-0.30.")
    lines.append("")
    lines.append("Important Methodological Note")
    lines.append("-" * 72)
    lines.append("This step only affects VADER sentiment analysis outputs. It does not modify TF-IDF, LDA, BERTopic, sampling, topic words, topic sizes, or representative reviews.")
    lines.append("")
    lines.append("Dataset")
    lines.append("-" * 72)
    lines.append(f"Total reviews scored: {len(df)}")
    lines.append(f"Recommended = yes: {int((df['Recommended'] == 'yes').sum())}")
    lines.append(f"Recommended = no : {int((df['Recommended'] == 'no').sum())}")
    lines.append("")
    lines.append("Sentence Statistics")
    lines.append("-" * 72)
    for col, val in sentence_stats.iloc[0].items():
        lines.append(f"{col}: {val}")
    lines.append("")
    lines.append("Aviation Lexicon")
    lines.append("-" * 72)
    lines.append(f"Applied aviation lexicon terms: {len(applied_lexicon)}")
    lines.append(f"Passenger-review filter enabled: {USE_PASSENGER_REVIEW_FILTER}")
    lines.append("Multi-word phrases were converted into underscore keys before VADER scoring, for example 'bad service' -> 'bad_service'.")
    lines.append("")
    lines.append("Best Configuration")
    lines.append("-" * 72)
    lines.append(f"Best score column: {best_config['score_column']}")
    lines.append(f"Best threshold: +/-{best_config['threshold']}")
    lines.append(f"Accuracy: {best_config['accuracy']}")
    lines.append(f"Macro F1: {best_config['macro_f1']}")
    lines.append(f"Neutral rate: {best_config['neutral_rate']}")
    lines.append("")
    lines.append("Best Threshold by Method")
    lines.append("-" * 72)
    for _, row in method_best.iterrows():
        lines.append(
            f"{row['score_column']} | threshold +/-{row['threshold']} | "
            f"accuracy={row['accuracy']} | macro_f1={row['macro_f1']} | neutral_rate={row['neutral_rate']}"
        )
    lines.append("")
    lines.append("Final Sentiment Summary by Recommended")
    lines.append("-" * 72)
    for _, row in final_summary.iterrows():
        lines.append(
            f"Recommended={row['Recommended']} | count={row['review_count']} | "
            f"avg_sentiment={row['avg_sentiment']} | median={row['median_sentiment']} | "
            f"positive={row['positive_count']} | neutral={row['neutral_count']} | negative={row['negative_count']} | "
            f"avg_score={row['avg_overall_score']}"
        )
    lines.append("")
    lines.append("Recommended Report Wording")
    lines.append("-" * 72)
    lines.append(
        "VADER sentiment analysis was validated by comparing different thresholds, input forms, and aviation-domain lexicon settings. "
        "The final setting was selected based on high-confidence proxy labels derived from rating and recommendation labels. "
        "This validation step only updates sentiment analysis outputs and does not affect the LDA or BERTopic topic modeling results."
    )

    with open(OUTPUT_DIR / "vader_validation_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    with open(OUTPUT_DIR / "vader_best_config.json", "w", encoding="utf-8") as f:
        json.dump(best_config, f, indent=2, ensure_ascii=False)


# =========================================================
# 9. Main pipeline
# =========================================================

def main():
    print("=" * 72)
    print("Advanced VADER validation and full 20k re-scoring")
    print("=" * 72)

    input_path = find_file("sampled_20k_with_tokens.csv", required=True)
    print(f"Loading dataset: {input_path}")
    df = pd.read_csv(input_path)

    required_columns = ["Review", "Recommended", "OverallScore"]
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    df["Review"] = df["Review"].fillna("").astype(str)
    df["Recommended"] = df["Recommended"].apply(normalize_recommended)
    df = df[df["Recommended"].isin(["yes", "no"])].copy()
    df["OverallScore"] = pd.to_numeric(df["OverallScore"], errors="coerce")

    # Sentence stats based on period-only splitting.
    df["sentence_count_period"] = df["Review"].apply(lambda x: len(split_sentences_by_period(x)))
    df["sentence_count_period"] = df["sentence_count_period"].replace(0, 1)

    # Proxy labels for validation.
    df["proxy_label"] = df.apply(proxy_label, axis=1)

    sentence_stats = build_sentence_statistics(df)
    sentence_stats.to_csv(OUTPUT_DIR / "vader_sentence_statistics.csv", index=False, encoding="utf-8-sig")

    print("Loading aviation lexicon...")
    applied_lexicon = load_aviation_lexicon()

    print("Running all VADER scoring methods on full dataset...")
    scored_df = add_all_vader_scores(df, applied_lexicon)

    score_output_cols = [
        "AirlineName", "CabinType", "OverallScore", "Recommended", "Review",
        "sentence_count_period", "proxy_label",
        "vader_original_full", "vader_original_sentence_avg",
        "vader_adjusted_full", "vader_adjusted_sentence_avg"
    ]
    score_output_cols = [c for c in score_output_cols if c in scored_df.columns]
    scored_df[score_output_cols].to_csv(
        OUTPUT_DIR / "vader_scores_all_methods_full_20k.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Running validation on high-confidence proxy labels...")
    validation_df, method_best, best_config = run_validation(scored_df)

    print("Creating final sentiment outputs...")
    final_df = add_final_labels(scored_df, best_config)
    final_summary = summarize_by_recommended(final_df)

    final_cols = [
        "AirlineName", "CabinType", "OverallScore", "Recommended", "Review",
        "sentence_count_period", "proxy_label",
        "vader_original_full", "vader_original_sentence_avg",
        "vader_adjusted_full", "vader_adjusted_sentence_avg",
        "vader_final_score", "vader_final_label", "vader_final_score_source", "vader_final_threshold"
    ]
    final_cols = [c for c in final_cols if c in final_df.columns]

    final_df[final_cols].to_csv(
        OUTPUT_DIR / "vader_final_sentiment_results.csv",
        index=False,
        encoding="utf-8-sig"
    )

    final_summary.to_csv(
        OUTPUT_DIR / "vader_final_summary_by_recommended.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # Also create a dashboard-compatible summary name if you want to replace old sentiment summary later.
    final_summary.to_csv(
        OUTPUT_DIR / "sentiment_summary_by_recommended_vader_validated.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Creating figures...")
    plot_threshold_comparison(validation_df)
    plot_method_best(method_best)
    plot_final_sentiment_distribution(final_df)
    plot_final_avg_sentiment(final_summary)

    print("Writing summary report...")
    write_summary_report(
        df=df,
        applied_lexicon=applied_lexicon,
        validation_df=validation_df,
        method_best=method_best,
        best_config=best_config,
        final_summary=final_summary,
        sentence_stats=sentence_stats,
    )

    print("=" * 72)
    print("Advanced VADER validation finished successfully.")
    print(f"All outputs are saved in: {OUTPUT_DIR}")
    print("Best configuration:")
    print(json.dumps(best_config, indent=2, ensure_ascii=False))
    print("=" * 72)


if __name__ == "__main__":
    main()
