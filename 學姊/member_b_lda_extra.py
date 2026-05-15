# member_b_lda_extra.py
# Member B Extra LDA Analysis
# 補做：
# 1. lda_coherence_scores.csv
# 2. fig_lda_coherence_scores.png
# 3. lda_visualization.html
# 4. lda_manual_interpretation_table.csv
#
# 這支程式不會取代原本的 member_b_pipeline.py
# 它只是補強 LDA 的進階分析。

import os
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

warnings.filterwarnings("ignore")


# =========================
# 0. 基本設定
# =========================

RANDOM_STATE = 42

TOPIC_NUMBERS_TO_TEST = [5, 7, 10]
FINAL_NUM_TOPICS = 7

TOP_WORDS_PER_TOPIC = 12
REPRESENTATIVE_REVIEWS_PER_TOPIC = 3

OUTPUT_DIR_NAME = "output"

LDA_EXTRA_STOPWORDS = [
    "flight", "airlin", "airline", "airway",
    "plane", "passeng", "passenger",
    "trip", "travel", "travell",
    "fly", "flew", "fli",
    "review", "would", "could", "also",
    "one", "get", "got", "go", "went",
    "us", "u"
]


# =========================
# 1. optional packages
# =========================

try:
    from gensim.corpora import Dictionary
    from gensim.models import CoherenceModel
    GENSIM_AVAILABLE = True
except ImportError:
    GENSIM_AVAILABLE = False

try:
    import pyLDAvis
    import pyLDAvis.lda_model
    PYLDA_AVAILABLE = True
except ImportError:
    PYLDA_AVAILABLE = False


# =========================
# 2. 路徑設定
# =========================

def get_base_dir():
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()


BASE_DIR = get_base_dir()
OUTPUT_DIR = BASE_DIR / OUTPUT_DIR_NAME
OUTPUT_DIR.mkdir(exist_ok=True)


def find_input_file():
    """
    自動尋找 sampled_20k_with_tokens.csv。
    支援以下放法：
    1. 和這支 py 同一層
    2. data/ 資料夾
    3. 上一層 data/ 資料夾
    """
    candidates = [
        BASE_DIR / "sampled_20k_with_tokens.csv",
        BASE_DIR / "data" / "sampled_20k_with_tokens.csv",
        BASE_DIR.parent / "data" / "sampled_20k_with_tokens.csv",
        Path.cwd() / "sampled_20k_with_tokens.csv",
        Path.cwd() / "data" / "sampled_20k_with_tokens.csv",
    ]

    for path in candidates:
        if path.exists():
            return path

    raise FileNotFoundError(
        "找不到 sampled_20k_with_tokens.csv。\n"
        "請把 sampled_20k_with_tokens.csv 放在 member_b_lda_extra.py 同一層，"
        "或放在 data/ 資料夾。"
    )


# =========================
# 3. 工具函式
# =========================

def clean_excerpt(text, max_len=280):
    text = str(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        return text[:max_len].rstrip() + "..."
    return text


def get_topic_words(lda_model, feature_names, topic_id, top_n=12):
    topic_weights = lda_model.components_[topic_id]
    top_indices = topic_weights.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices]


def guess_topic_name(top_words):
    """
    用 top words 初步幫 topic 命名。
    最後報告仍建議你看 representative reviews 後人工修正。
    """
    words = set(top_words)

    topic_rules = [
        (
            "Flight Delay and Cancellation",
            {"delay", "delai", "cancel", "cancell", "late", "hour", "wait", "miss", "connect", "connection"}
        ),
        (
            "Staff Service and Attitude",
            {"staff", "crew", "service", "rude", "attend", "attitud", "help", "helpful", "unhelp"}
        ),
        (
            "Baggage and Luggage Problems",
            {"bag", "baggag", "luggag", "lost", "damag", "claim"}
        ),
        (
            "Refund and Compensation Issues",
            {"refund", "money", "compens", "voucher", "claim", "pay", "paid", "charg", "cost"}
        ),
        (
            "Seat Comfort and Cabin Space",
            {"seat", "legroom", "space", "comfort", "uncomfort", "cabin", "room"}
        ),
        (
            "Food and Meal Quality",
            {"food", "meal", "drink", "breakfast", "dinner", "lunch", "beverag"}
        ),
        (
            "Value for Money and Pricing",
            {"value", "price", "cost", "expens", "cheap", "fare", "ticket"}
        ),
        (
            "Booking, Check-in, and Boarding",
            {"book", "booking", "check", "checkin", "board", "boarding", "gate", "ticket"}
        ),
    ]

    best_name = "General Complaint Topic"
    best_overlap = 0

    for name, keywords in topic_rules:
        overlap = len(words.intersection(keywords))
        if overlap > best_overlap:
            best_name = name
            best_overlap = overlap

    return best_name


def make_interpretation(topic_name):
    interpretation_map = {
        "Flight Delay and Cancellation":
            "This topic mainly reflects complaints about delayed flights, cancellations, missed connections, and long waiting time.",
        "Staff Service and Attitude":
            "This topic focuses on passengers' dissatisfaction with staff attitude, cabin crew service, and lack of assistance.",
        "Baggage and Luggage Problems":
            "This topic is related to lost, delayed, damaged, or mishandled baggage and luggage claim issues.",
        "Refund and Compensation Issues":
            "This topic describes complaints about refund difficulty, compensation problems, extra charges, or payment issues.",
        "Seat Comfort and Cabin Space":
            "This topic captures complaints about uncomfortable seats, limited legroom, cabin space, and overall seating experience.",
        "Food and Meal Quality":
            "This topic is associated with meal quality, drinks, food options, and in-flight dining experience.",
        "Value for Money and Pricing":
            "This topic reflects whether passengers think the airline service is worth the price paid.",
        "Booking, Check-in, and Boarding":
            "This topic includes problems during booking, check-in, boarding, ticket handling, or gate procedures.",
        "General Complaint Topic":
            "This topic contains general negative experiences that may require manual interpretation based on the top words and reviews."
    }

    return interpretation_map.get(topic_name, interpretation_map["General Complaint Topic"])


def calculate_coherence_score(topics_words, token_lists):
    """
    使用 gensim 計算 c_v coherence score。
    分數越高，通常代表 topic words 語意一致性越好。
    """
    if not GENSIM_AVAILABLE:
        return None

    dictionary = Dictionary(token_lists)

    coherence_model = CoherenceModel(
        topics=topics_words,
        texts=token_lists,
        dictionary=dictionary,
        coherence="c_v"
    )

    return coherence_model.get_coherence()


# =========================
# 4. 讀取資料
# =========================

def load_data():
    input_path = find_input_file()

    print("=" * 60)
    print("Loading data")
    print("=" * 60)
    print(f"Input file: {input_path}")

    df = pd.read_csv(input_path)

    required_columns = [
        "Review",
        "tokens",
        "Recommended",
        "OverallScore"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(
            f"缺少必要欄位：{missing}\n"
            "請確認你使用的是 sampled_20k_with_tokens.csv。"
        )

    df["Recommended"] = df["Recommended"].astype(str).str.lower().str.strip()
    df = df[df["Recommended"].isin(["yes", "no"])].copy()

    df["Review"] = df["Review"].fillna("").astype(str)
    df["tokens"] = df["tokens"].fillna("").astype(str)

    if "token_count" not in df.columns:
        df["token_count"] = df["tokens"].apply(
            lambda x: len([t for t in str(x).split("|") if len(t.strip()) > 1])
        )

    df["token_list"] = df["tokens"].apply(
        lambda x: [t.strip() for t in str(x).split("|") if len(t.strip()) > 1]
    )

    df["token_text"] = df["token_list"].apply(lambda tokens: " ".join(tokens))

    df["OverallScore"] = pd.to_numeric(df["OverallScore"], errors="coerce")

    print(f"Dataset shape: {df.shape}")
    print(df["Recommended"].value_counts())

    return df


# =========================
# 5. 主要 LDA extra analysis
# =========================

def run_lda_extra(df):
    print("\n" + "=" * 60)
    print("Running extra LDA analysis")
    print("=" * 60)

    lda_df = df[
        (df["Recommended"] == "no") &
        (df["token_text"].str.strip() != "")
    ].copy()

    lda_df = lda_df[lda_df["token_count"] >= 3].copy()

    if len(lda_df) == 0:
        raise ValueError("沒有足夠的不推薦評論可以做 LDA。")

    print(f"LDA input reviews: {len(lda_df)}")

    token_lists = lda_df["token_list"].tolist()

    vectorizer = CountVectorizer(
        max_features=6000,
        min_df=5,
        max_df=0.85,
        stop_words=LDA_EXTRA_STOPWORDS,
        token_pattern=r"(?u)\b\w+\b"
    )

    X = vectorizer.fit_transform(lda_df["token_text"])
    feature_names = np.array(vectorizer.get_feature_names_out())

    print(f"Document-term matrix shape: {X.shape}")

    fitted_models = {}
    coherence_rows = []
    model_rows = []
    all_topic_rows = []

    for num_topics in TOPIC_NUMBERS_TO_TEST:
        print(f"\nTraining LDA with {num_topics} topics...")

        lda = LatentDirichletAllocation(
            n_components=num_topics,
            max_iter=25,
            learning_method="batch",
            random_state=RANDOM_STATE,
            evaluate_every=-1,
            n_jobs=-1
        )

        doc_topic = lda.fit_transform(X)
        assigned_topic = doc_topic.argmax(axis=1)
        topic_sizes = pd.Series(assigned_topic).value_counts().sort_index()

        perplexity = lda.perplexity(X)

        topics_words = []

        for topic_id in range(num_topics):
            top_words = get_topic_words(
                lda,
                feature_names,
                topic_id,
                TOP_WORDS_PER_TOPIC
            )
            topics_words.append(top_words)

        coherence_score = calculate_coherence_score(topics_words, token_lists)

        fitted_models[num_topics] = {
            "model": lda,
            "doc_topic": doc_topic,
            "assigned_topic": assigned_topic,
            "topic_sizes": topic_sizes,
            "coherence_score": coherence_score
        }

        coherence_rows.append({
            "num_topics": num_topics,
            "coherence_score": round(float(coherence_score), 4) if coherence_score is not None else np.nan,
            "note": "Higher c_v coherence usually means the topic words are more semantically coherent."
        })

        model_rows.append({
            "num_topics": num_topics,
            "perplexity": round(float(perplexity), 4),
            "coherence_score": round(float(coherence_score), 4) if coherence_score is not None else "not_available",
            "selection_note": "Final topic number should consider both coherence and human interpretability."
        })

        for topic_id in range(num_topics):
            top_words = topics_words[topic_id]
            topic_name = guess_topic_name(top_words)

            all_topic_rows.append({
                "num_topics": num_topics,
                "topic_id": topic_id,
                "topic_name_auto": topic_name,
                "topic_size": int(topic_sizes.get(topic_id, 0)),
                "top_words": ", ".join(top_words),
                "interpretation": make_interpretation(topic_name)
            })

    coherence_df = pd.DataFrame(coherence_rows)
    model_df = pd.DataFrame(model_rows)
    all_topics_df = pd.DataFrame(all_topic_rows)

    coherence_df.to_csv(
        OUTPUT_DIR / "lda_coherence_scores.csv",
        index=False,
        encoding="utf-8-sig"
    )

    model_df.to_csv(
        OUTPUT_DIR / "lda_model_selection_extra.csv",
        index=False,
        encoding="utf-8-sig"
    )

    all_topics_df.to_csv(
        OUTPUT_DIR / "lda_all_topic_numbers_extra.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # coherence 圖
    if coherence_df["coherence_score"].notna().any():
        fig, ax = plt.subplots(figsize=(7, 4))

        ax.plot(
            coherence_df["num_topics"],
            coherence_df["coherence_score"],
            marker="o",
            linewidth=2
        )

        for _, row in coherence_df.iterrows():
            if pd.notna(row["coherence_score"]):
                ax.text(
                    row["num_topics"],
                    row["coherence_score"],
                    f"{row['coherence_score']:.4f}",
                    ha="center",
                    va="bottom",
                    fontsize=9
                )

        ax.set_title(
            "LDA Coherence Scores by Number of Topics",
            fontsize=13,
            fontweight="bold"
        )
        ax.set_xlabel("Number of Topics")
        ax.set_ylabel("Coherence Score (c_v)")
        ax.set_xticks(coherence_df["num_topics"])
        ax.spines[["top", "right"]].set_visible(False)

        plt.tight_layout()
        plt.savefig(
            OUTPUT_DIR / "fig_lda_coherence_scores.png",
            dpi=180,
            bbox_inches="tight"
        )
        plt.close()

        print("Saved: fig_lda_coherence_scores.png")
    else:
        print("沒有產生 coherence 圖，因為 gensim 沒有安裝或 coherence 無法計算。")

    # 最終 LDA model
    final_topic_num = FINAL_NUM_TOPICS

    if final_topic_num not in fitted_models:
        final_topic_num = TOPIC_NUMBERS_TO_TEST[0]

    final_lda = fitted_models[final_topic_num]["model"]
    final_doc_topic = fitted_models[final_topic_num]["doc_topic"]
    final_assigned_topic = fitted_models[final_topic_num]["assigned_topic"]
    final_topic_sizes = fitted_models[final_topic_num]["topic_sizes"]

    # final topic table
    final_topic_rows = []

    for topic_id in range(final_topic_num):
        top_words = get_topic_words(
            final_lda,
            feature_names,
            topic_id,
            TOP_WORDS_PER_TOPIC
        )
        topic_name = guess_topic_name(top_words)

        final_topic_rows.append({
            "topic_id": topic_id,
            "topic_name_auto": topic_name,
            "topic_size": int(final_topic_sizes.get(topic_id, 0)),
            "top_words": ", ".join(top_words),
            "interpretation": make_interpretation(topic_name)
        })

    final_topics_df = pd.DataFrame(final_topic_rows)

    final_topics_df.to_csv(
        OUTPUT_DIR / "lda_topics_extra.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # manual interpretation table
    manual_rows = []

    for _, row in final_topics_df.iterrows():
        manual_rows.append({
            "topic_id": row["topic_id"],
            "top_words": row["top_words"],
            "topic_size": row["topic_size"],
            "manual_topic_label": row["topic_name_auto"],
            "complaint_category": row["topic_name_auto"],
            "reason_for_labeling": row["interpretation"],
            "is_related_to_passenger_complaints": "yes",
            "need_manual_check": "yes",
            "notes_for_report": (
                "This topic label is generated from top words first. "
                "Please check representative reviews and manually adjust the label if needed."
            )
        })

    manual_df = pd.DataFrame(manual_rows)

    manual_df.to_csv(
        OUTPUT_DIR / "lda_manual_interpretation_table.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Saved: lda_manual_interpretation_table.csv")

    # representative reviews
    lda_df = lda_df.reset_index(drop=False).rename(columns={"index": "original_index"})
    lda_df["lda_topic"] = final_assigned_topic
    lda_df["lda_topic_probability"] = final_doc_topic.max(axis=1).round(6)

    rep_rows = []

    for topic_id in range(final_topic_num):
        topic_reviews = lda_df[lda_df["lda_topic"] == topic_id].copy()

        if len(topic_reviews) == 0:
            continue

        topic_reviews = topic_reviews.sort_values(
            by="lda_topic_probability",
            ascending=False
        ).head(REPRESENTATIVE_REVIEWS_PER_TOPIC)

        topic_name = final_topics_df.loc[
            final_topics_df["topic_id"] == topic_id,
            "topic_name_auto"
        ].iloc[0]

        top_words = final_topics_df.loc[
            final_topics_df["topic_id"] == topic_id,
            "top_words"
        ].iloc[0]

        for rank, (_, row) in enumerate(topic_reviews.iterrows(), start=1):
            rep_rows.append({
                "topic_id": topic_id,
                "topic_name_auto": topic_name,
                "representative_rank": rank,
                "topic_probability": row["lda_topic_probability"],
                "top_words": top_words,
                "OverallScore": row.get("OverallScore", np.nan),
                "AirlineName": row.get("AirlineName", ""),
                "CabinType": row.get("CabinType", ""),
                "representative_review": clean_excerpt(row.get("Review", ""))
            })

    rep_df = pd.DataFrame(rep_rows)

    rep_df.to_csv(
        OUTPUT_DIR / "lda_representative_reviews_extra.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Saved: lda_representative_reviews_extra.csv")

    # pyLDAvis html
    if PYLDA_AVAILABLE:
        try:
            vis = pyLDAvis.lda_model.prepare(
                final_lda,
                X,
                vectorizer,
                sort_topics=False
            )

            pyLDAvis.save_html(
                vis,
                str(OUTPUT_DIR / "lda_visualization.html")
            )

            print("Saved: lda_visualization.html")
        except Exception as e:
            print("pyLDAvis 產生失敗，但其他檔案已正常輸出。")
            print(f"原因：{e}")
    else:
        print("pyLDAvis 沒有安裝，所以沒有產生 lda_visualization.html。")
        print("需要的話請執行：pip install pyLDAvis")

    # 文字說明
    write_extra_summary(coherence_df, final_topics_df)

    print("\nExtra LDA analysis finished.")
    print(f"All outputs are saved in: {OUTPUT_DIR}")


def write_extra_summary(coherence_df, final_topics_df):
    lines = []

    lines.append("Member B Extra LDA Analysis Summary")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Purpose")
    lines.append("-" * 60)
    lines.append(
        "This extra analysis improves the LDA baseline by adding topic coherence scores, "
        "a coherence score figure, an optional pyLDAvis visualization, and a manual topic interpretation table."
    )
    lines.append("")
    lines.append("Coherence Scores")
    lines.append("-" * 60)

    for _, row in coherence_df.iterrows():
        score = row["coherence_score"]

        if pd.isna(score):
            score_text = "not available"
        else:
            score_text = f"{score:.4f}"

        lines.append(f"{int(row['num_topics'])} topics: coherence score = {score_text}")

    lines.append("")
    lines.append("Final Topic Setting")
    lines.append("-" * 60)
    lines.append(f"Final number of topics used for manual interpretation: {FINAL_NUM_TOPICS}")
    lines.append("")
    lines.append("Final LDA Topics")
    lines.append("-" * 60)

    for _, row in final_topics_df.iterrows():
        lines.append(
            f"Topic {row['topic_id']} | {row['topic_name_auto']} | "
            f"size = {row['topic_size']} | top words = {row['top_words']}"
        )

    lines.append("")
    lines.append("Report Usage")
    lines.append("-" * 60)
    lines.append(
        "In the report, these outputs can support the explanation that the final topic number "
        "was selected based on both topic coherence and human interpretability."
    )

    with open(
        OUTPUT_DIR / "member_b_lda_extra_summary.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("\n".join(lines))

    print("Saved: member_b_lda_extra_summary.txt")


# =========================
# 6. main
# =========================

if __name__ == "__main__":
    df = load_data()
    run_lda_extra(df)