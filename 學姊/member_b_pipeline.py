# member_b_pipeline.py
# Member B: TF / TF-IDF, Sentiment Analysis, and LDA Baseline
# Author: 林冠妤
#
# 使用資料：
# sampled_20k_with_tokens.csv
#
# 欄位使用規則：
# 1. Review          -> VADER sentiment analysis
# 2. review_cleaned  -> TF / TF-IDF keyword analysis
# 3. tokens          -> LDA topic modeling

import os
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# =========================
# 0. 基本設定
# =========================

RANDOM_STATE = 42
TOP_N_KEYWORDS = 25
TOPIC_NUMBERS_TO_TEST = [5, 7, 10]
FINAL_NUM_TOPICS = 7
TOP_WORDS_PER_TOPIC = 12
REPRESENTATIVE_REVIEWS_PER_TOPIC = 3

# 你現在資料夾名稱是 output，所以這裡用 output
OUTPUT_DIR_NAME = "output"

warnings.filterwarnings("ignore", category=UserWarning)


def get_base_dir():
    """取得目前程式所在資料夾。"""
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()


BASE_DIR = get_base_dir()
OUTPUT_DIR = BASE_DIR / OUTPUT_DIR_NAME
OUTPUT_DIR.mkdir(exist_ok=True)


# =========================
# 1. 找資料檔
# =========================

def find_input_file():
    """
    自動尋找 sampled_20k_with_tokens.csv。
    這樣不管你把檔案放在目前資料夾、data/、或上一層 data/ 都比較不容易出錯。
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
        "請確認檔案有放在 member_b_pipeline.py 同一層，或放在 data/ 資料夾中。"
    )


INPUT_PATH = find_input_file()


# =========================
# 2. 載入與檢查資料
# =========================

def load_and_check_data(path):
    """讀取資料，檢查必要欄位，並做基本清理。"""
    print("=" * 60)
    print("Step 1. Loading dataset")
    print("=" * 60)
    print(f"Input file: {path}")

    df = pd.read_csv(path)

    required_columns = [
        "Review",
        "review_cleaned",
        "tokens",
        "Recommended",
        "OverallScore"
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(
            f"資料缺少必要欄位：{missing}\n"
            "請確認你使用的是 Member A 產出的 sampled_20k_with_tokens.csv。"
        )

    # 統一 Recommended 格式
    df["Recommended"] = df["Recommended"].astype(str).str.lower().str.strip()

    # 只保留 yes / no
    df = df[df["Recommended"].isin(["yes", "no"])].copy()

    # 補空值，避免後面 vectorizer 或 VADER 爆掉
    df["Review"] = df["Review"].fillna("").astype(str)
    df["review_cleaned"] = df["review_cleaned"].fillna("").astype(str)
    df["tokens"] = df["tokens"].fillna("").astype(str)

    # OverallScore 轉數字
    df["OverallScore"] = pd.to_numeric(df["OverallScore"], errors="coerce")

    # tokens: pipe 字串轉成 list
    # 例如：first|flight|delay -> ["first", "flight", "delay"]
    df["token_list"] = df["tokens"].apply(
        lambda x: [t.strip() for t in str(x).split("|") if len(t.strip()) > 1]
    )

    # LDA 使用空白分隔的 token 文字
    df["token_text"] = df["token_list"].apply(lambda tokens: " ".join(tokens))

    # token_count 如果不存在就自己補
    if "token_count" not in df.columns:
        df["token_count"] = df["token_list"].apply(len)

    print(f"Dataset shape: {df.shape}")
    print("\nRecommended counts:")
    print(df["Recommended"].value_counts())

    print("\nColumns:")
    print(df.columns.tolist())

    # 輸出基本資料檢查
    summary = {
        "total_reviews": len(df),
        "recommended_yes": int((df["Recommended"] == "yes").sum()),
        "recommended_no": int((df["Recommended"] == "no").sum()),
        "empty_review_count": int((df["Review"].str.strip() == "").sum()),
        "empty_review_cleaned_count": int((df["review_cleaned"].str.strip() == "").sum()),
        "empty_tokens_count": int((df["token_text"].str.strip() == "").sum()),
        "average_token_count": round(float(df["token_count"].mean()), 2),
    }

    pd.DataFrame([summary]).to_csv(
        OUTPUT_DIR / "data_check_summary.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return df


df = load_and_check_data(INPUT_PATH)


# =========================
# 3. 分組
# =========================

df_yes = df[df["Recommended"] == "yes"].copy()
df_no = df[df["Recommended"] == "no"].copy()

# high-rated / low-rated
# 這邊用常見切法：
# 1-4 = low-rated
# 5-7 = middle-rated
# 8-10 = high-rated
df["rating_group"] = pd.cut(
    df["OverallScore"],
    bins=[0, 4, 7, 10],
    labels=["low", "middle", "high"],
    include_lowest=True
)

df_low = df[df["rating_group"] == "low"].copy()
df_high = df[df["rating_group"] == "high"].copy()


# =========================
# 4. TF / TF-IDF Keyword Analysis
# =========================

# 一些航空評論中太普通、太常見的詞
# 這些字如果不拿掉，關鍵字表會一直出現 flight / airline，解釋力比較弱
DOMAIN_STOPWORDS = [
    "flight", "flights", "airline", "airlines", "airway", "airways",
    "plane", "planes", "airport", "airports",
    "passenger", "passengers",
    "trip", "travel", "travelling", "traveled",
    "fly", "flying", "flew",
    "review", "reviews"
]


def get_top_vector_keywords(vectorizer, fitted_matrix, group_index, top_n=25):
    """
    給定已 fit 好的 vectorizer 和整份 matrix，
    計算某一組資料的平均分數，取 top keywords。
    """
    feature_names = np.array(vectorizer.get_feature_names_out())

    group_matrix = fitted_matrix[group_index]
    scores = np.asarray(group_matrix.mean(axis=0)).ravel()

    top_idx = scores.argsort()[::-1][:top_n]

    result = pd.DataFrame({
        "rank": range(1, top_n + 1),
        "keyword": feature_names[top_idx],
        "score": scores[top_idx]
    })

    result["score"] = result["score"].round(6)
    return result


def make_keyword_comparison(left_df, right_df, left_name, right_name):
    """把兩組 top keywords 合併成比較表。"""
    comparison = pd.DataFrame({
        "rank": left_df["rank"],
        f"{left_name}_keyword": left_df["keyword"],
        f"{left_name}_score": left_df["score"],
        f"{right_name}_keyword": right_df["keyword"],
        f"{right_name}_score": right_df["score"],
    })
    return comparison


def plot_keyword_comparison(comparison_df, left_keyword_col, left_score_col,
                            right_keyword_col, right_score_col, title, output_path):
    """
    畫 yes/no 或 high/low 的 top keyword 比較圖。
    為了讓圖不要太擠，只畫前 12 個。
    """
    top_k = min(12, len(comparison_df))

    left_words = comparison_df[left_keyword_col].head(top_k).tolist()[::-1]
    left_scores = comparison_df[left_score_col].head(top_k).tolist()[::-1]

    right_words = comparison_df[right_keyword_col].head(top_k).tolist()[::-1]
    right_scores = comparison_df[right_score_col].head(top_k).tolist()[::-1]

    fig, axes = plt.subplots(1, 2, figsize=(13, 6))

    axes[0].barh(left_words, left_scores)
    axes[0].set_title(left_keyword_col.replace("_keyword", ""))
    axes[0].set_xlabel("Average Score")

    axes[1].barh(right_words, right_scores)
    axes[1].set_title(right_keyword_col.replace("_keyword", ""))
    axes[1].set_xlabel("Average Score")

    fig.suptitle(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close()


def run_tf_tfidf_analysis(df):
    """做 TF 和 TF-IDF，並輸出 yes/no 與 high/low 比較。"""
    print("\n" + "=" * 60)
    print("Step 2. TF and TF-IDF keyword analysis")
    print("=" * 60)

    text_data = df["review_cleaned"].fillna("").astype(str)

    # ---------- TF ----------
    tf_vectorizer = CountVectorizer(
        max_features=8000,
        ngram_range=(1, 2),
        min_df=5,
        max_df=0.90,
        stop_words=DOMAIN_STOPWORDS
    )

    tf_matrix = tf_vectorizer.fit_transform(text_data)

    # ---------- TF-IDF ----------
    tfidf_vectorizer = TfidfVectorizer(
        max_features=8000,
        ngram_range=(1, 2),
        min_df=5,
        max_df=0.90,
        stop_words=DOMAIN_STOPWORDS
    )

    tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)

    yes_index = df["Recommended"].values == "yes"
    no_index = df["Recommended"].values == "no"
    high_index = df["rating_group"].astype(str).values == "high"
    low_index = df["rating_group"].astype(str).values == "low"

    # TF yes / no
    tf_yes = get_top_vector_keywords(tf_vectorizer, tf_matrix, yes_index, TOP_N_KEYWORDS)
    tf_no = get_top_vector_keywords(tf_vectorizer, tf_matrix, no_index, TOP_N_KEYWORDS)
    tf_yes_no_comparison = make_keyword_comparison(tf_yes, tf_no, "yes", "no")

    # TF-IDF yes / no
    tfidf_yes = get_top_vector_keywords(tfidf_vectorizer, tfidf_matrix, yes_index, TOP_N_KEYWORDS)
    tfidf_no = get_top_vector_keywords(tfidf_vectorizer, tfidf_matrix, no_index, TOP_N_KEYWORDS)
    tfidf_yes_no_comparison = make_keyword_comparison(tfidf_yes, tfidf_no, "yes", "no")

    # TF-IDF high / low
    tfidf_high = get_top_vector_keywords(tfidf_vectorizer, tfidf_matrix, high_index, TOP_N_KEYWORDS)
    tfidf_low = get_top_vector_keywords(tfidf_vectorizer, tfidf_matrix, low_index, TOP_N_KEYWORDS)
    tfidf_high_low_comparison = make_keyword_comparison(tfidf_high, tfidf_low, "high_rated", "low_rated")

    # 存檔
    tf_yes.to_csv(OUTPUT_DIR / "tf_yes_keywords.csv", index=False, encoding="utf-8-sig")
    tf_no.to_csv(OUTPUT_DIR / "tf_no_keywords.csv", index=False, encoding="utf-8-sig")
    tf_yes_no_comparison.to_csv(OUTPUT_DIR / "tf_yes_no_keyword_comparison.csv", index=False, encoding="utf-8-sig")

    tfidf_yes.to_csv(OUTPUT_DIR / "tfidf_yes_keywords.csv", index=False, encoding="utf-8-sig")
    tfidf_no.to_csv(OUTPUT_DIR / "tfidf_no_keywords.csv", index=False, encoding="utf-8-sig")
    tfidf_yes_no_comparison.to_csv(OUTPUT_DIR / "tfidf_yes_no_keyword_comparison.csv", index=False, encoding="utf-8-sig")

    tfidf_high.to_csv(OUTPUT_DIR / "tfidf_high_rated_keywords.csv", index=False, encoding="utf-8-sig")
    tfidf_low.to_csv(OUTPUT_DIR / "tfidf_low_rated_keywords.csv", index=False, encoding="utf-8-sig")
    tfidf_high_low_comparison.to_csv(OUTPUT_DIR / "tfidf_high_low_keyword_comparison.csv", index=False, encoding="utf-8-sig")

    # 畫圖
    plot_keyword_comparison(
        tfidf_yes_no_comparison,
        "yes_keyword", "yes_score",
        "no_keyword", "no_score",
        "Top TF-IDF Keywords: Recommended Yes vs No",
        OUTPUT_DIR / "fig_tfidf_comparison.png"
    )

    plot_keyword_comparison(
        tfidf_high_low_comparison,
        "high_rated_keyword", "high_rated_score",
        "low_rated_keyword", "low_rated_score",
        "Top TF-IDF Keywords: High-rated vs Low-rated Reviews",
        OUTPUT_DIR / "fig_tfidf_high_low_comparison.png"
    )

    print("TF / TF-IDF keyword tables saved.")
    print("Keyword comparison figures saved.")

    return tfidf_yes_no_comparison


tfidf_comparison = run_tf_tfidf_analysis(df)


# =========================
# 5. Sentiment Analysis
# =========================

def label_sentiment(score):
    """依照 VADER 常用門檻標記情緒。"""
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"


def check_recommend_sentiment_consistency(row):
    """
    檢查 Recommended 和 sentiment 是否大致一致。
    yes + positive = consistent
    no + negative = consistent
    其他則視為 possible mismatch，方便報告討論。
    """
    rec = row["Recommended"]
    label = row["sentiment_label"]

    if rec == "yes" and label == "positive":
        return "consistent"
    if rec == "no" and label == "negative":
        return "consistent"
    return "possible_mismatch"


def run_sentiment_analysis(df):
    """用 VADER 做情緒分析，並檢查 Recommended / Rating / Sentiment 的一致性。"""
    print("\n" + "=" * 60)
    print("Step 3. VADER sentiment analysis")
    print("=" * 60)

    analyzer = SentimentIntensityAnalyzer()

    # VADER 用原始 Review，不用 cleaned text
    scores = df["Review"].apply(lambda x: analyzer.polarity_scores(str(x)))

    df["sentiment_neg"] = scores.apply(lambda x: x["neg"])
    df["sentiment_neu"] = scores.apply(lambda x: x["neu"])
    df["sentiment_pos"] = scores.apply(lambda x: x["pos"])
    df["sentiment_score"] = scores.apply(lambda x: x["compound"])
    df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)

    df["recommend_sentiment_consistency"] = df.apply(
        check_recommend_sentiment_consistency,
        axis=1
    )

    # rating 和 sentiment 的簡單一致性
    df["rating_sentiment_note"] = "normal"

    df.loc[
        (df["OverallScore"] <= 4) & (df["sentiment_score"] >= 0.05),
        "rating_sentiment_note"
    ] = "low_rating_but_positive_text"

    df.loc[
        (df["OverallScore"] >= 8) & (df["sentiment_score"] <= -0.05),
        "rating_sentiment_note"
    ] = "high_rating_but_negative_text"

    # 每筆結果
    sentiment_cols = [
        "AirlineName", "CabinType", "OverallScore", "Recommended",
        "Review",
        "sentiment_neg", "sentiment_neu", "sentiment_pos",
        "sentiment_score", "sentiment_label",
        "recommend_sentiment_consistency",
        "rating_sentiment_note"
    ]

    existing_cols = [col for col in sentiment_cols if col in df.columns]

    df[existing_cols].to_csv(
        OUTPUT_DIR / "sentiment_results.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # Recommended yes/no summary
    summary = df.groupby("Recommended").agg(
        review_count=("Review", "count"),
        avg_sentiment=("sentiment_score", "mean"),
        median_sentiment=("sentiment_score", "median"),
        positive_count=("sentiment_label", lambda x: (x == "positive").sum()),
        neutral_count=("sentiment_label", lambda x: (x == "neutral").sum()),
        negative_count=("sentiment_label", lambda x: (x == "negative").sum()),
        avg_overall_score=("OverallScore", "mean")
    ).reset_index()

    summary["avg_sentiment"] = summary["avg_sentiment"].round(4)
    summary["median_sentiment"] = summary["median_sentiment"].round(4)
    summary["avg_overall_score"] = summary["avg_overall_score"].round(3)

    summary.to_csv(
        OUTPUT_DIR / "sentiment_summary_by_recommended.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # Sentiment label 分布
    label_dist = pd.crosstab(
        df["Recommended"],
        df["sentiment_label"],
        normalize="index"
    ).round(4)

    label_dist.to_csv(
        OUTPUT_DIR / "sentiment_label_distribution_by_recommended.csv",
        encoding="utf-8-sig"
    )

    # mismatch examples
    mismatch_examples = df[
        df["recommend_sentiment_consistency"] == "possible_mismatch"
    ][existing_cols].head(100)

    mismatch_examples.to_csv(
        OUTPUT_DIR / "sentiment_possible_mismatch_examples.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # ---------- 圖 1: sentiment distribution ----------
    fig, ax = plt.subplots(figsize=(9, 5))

    bins = np.linspace(-1, 1, 41)

    ax.hist(
        df[df["Recommended"] == "yes"]["sentiment_score"],
        bins=bins,
        alpha=0.65,
        label="Recommended = yes"
    )

    ax.hist(
        df[df["Recommended"] == "no"]["sentiment_score"],
        bins=bins,
        alpha=0.65,
        label="Recommended = no"
    )

    ax.set_title("Sentiment Score Distribution by Recommended Group", fontsize=13, fontweight="bold")
    ax.set_xlabel("VADER Compound Sentiment Score")
    ax.set_ylabel("Number of Reviews")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_sentiment_dist.png", dpi=180, bbox_inches="tight")
    plt.close()

    # ---------- 圖 2: average sentiment by recommended ----------
    fig, ax = plt.subplots(figsize=(6, 4))

    bar_data = summary.set_index("Recommended")["avg_sentiment"].reindex(["yes", "no"])
    bars = ax.bar(bar_data.index, bar_data.values)

    ax.set_title("Average Sentiment Score by Recommended", fontsize=13, fontweight="bold")
    ax.set_xlabel("Recommended")
    ax.set_ylabel("Average VADER Compound Score")
    ax.axhline(0, linewidth=1)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.3f}",
            ha="center",
            va="bottom" if height >= 0 else "top"
        )

    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_avg_sentiment_by_recommended.png", dpi=180, bbox_inches="tight")
    plt.close()

    print("Sentiment result tables saved.")
    print("Sentiment figures saved.")

    return df


df = run_sentiment_analysis(df)


# =========================
# 6. LDA Topic Modeling
# =========================

# LDA 用的是 stemmed tokens，所以 stopwords 也要偏 stemmed 形式
LDA_EXTRA_STOPWORDS = [
    "flight", "airlin", "airline", "airway",
    "plane", "passeng", "passenger",
    "trip", "travel", "travell",
    "fly", "flew", "fli",
    "review", "would", "could", "also",
    "one", "get", "got", "go", "went",
    "us", "u"
]


def clean_excerpt(text, max_len=280):
    """把代表性評論整理成短一點的句子，方便報告貼上。"""
    text = str(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        return text[:max_len].rstrip() + "..."
    return text


def guess_topic_name(top_words):
    """
    根據 top words 粗略命名 topic。
    這不是模型自動知道意思，而是用關鍵字規則幫你先命名。
    你最後報告可以再人工修正名稱。
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
    """根據 topic name 產生簡短解釋，方便直接放報告。"""
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


def get_topic_words(lda_model, feature_names, topic_id, top_n=12):
    """取得某個 topic 的 top words。"""
    topic_weights = lda_model.components_[topic_id]
    top_indices = topic_weights.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices]


def run_lda_topic_modeling(df):
    """
    使用 sklearn 的 LatentDirichletAllocation 做 LDA。
    主要分析 Recommended = no 的評論，因為研究重點是 passenger complaints。
    """
    print("\n" + "=" * 60)
    print("Step 4. LDA topic modeling baseline")
    print("=" * 60)

    # 主要使用不推薦評論
    lda_df = df[
        (df["Recommended"] == "no") &
        (df["token_text"].str.strip() != "")
    ].copy()

    # 過短評論會讓 topic 很不穩，所以保留 token_count >= 3
    lda_df = lda_df[lda_df["token_count"] >= 3].copy()

    if len(lda_df) == 0:
        raise ValueError("沒有足夠的 not recommended reviews 可以做 LDA。")

    print(f"LDA input reviews: {len(lda_df)}")

    vectorizer = CountVectorizer(
        max_features=6000,
        min_df=5,
        max_df=0.85,
        stop_words=LDA_EXTRA_STOPWORDS,
        token_pattern=r"(?u)\b\w+\b"
    )

    X = vectorizer.fit_transform(lda_df["token_text"])
    feature_names = np.array(vectorizer.get_feature_names_out())

    if X.shape[1] == 0:
        raise ValueError("LDA vectorizer 沒有產生任何 feature，請檢查 tokens 欄位。")

    model_selection_rows = []
    all_topic_rows = []

    fitted_models = {}

    # 試 5, 7, 10 topics
    for num_topics in TOPIC_NUMBERS_TO_TEST:
        print(f"Training LDA with {num_topics} topics...")

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

        fitted_models[num_topics] = {
            "model": lda,
            "doc_topic": doc_topic,
            "assigned_topic": assigned_topic,
            "topic_sizes": topic_sizes
        }

        model_selection_rows.append({
            "num_topics": num_topics,
            "perplexity": round(float(perplexity), 4),
            "note": "Lower perplexity is better mathematically, but final choice should also consider interpretability."
        })

        for topic_id in range(num_topics):
            top_words = get_topic_words(lda, feature_names, topic_id, TOP_WORDS_PER_TOPIC)
            topic_name = guess_topic_name(top_words)
            topic_size = int(topic_sizes.get(topic_id, 0))

            all_topic_rows.append({
                "num_topics": num_topics,
                "topic_id": topic_id,
                "topic_name_auto": topic_name,
                "topic_size": topic_size,
                "top_words": ", ".join(top_words),
                "interpretation": make_interpretation(topic_name)
            })

    model_selection_df = pd.DataFrame(model_selection_rows)
    all_topics_df = pd.DataFrame(all_topic_rows)

    model_selection_df.to_csv(
        OUTPUT_DIR / "lda_model_selection.csv",
        index=False,
        encoding="utf-8-sig"
    )

    all_topics_df.to_csv(
        OUTPUT_DIR / "lda_all_topic_numbers.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # 最終採用 7 topics
    final_topic_num = FINAL_NUM_TOPICS

    if final_topic_num not in fitted_models:
        final_topic_num = TOPIC_NUMBERS_TO_TEST[0]

    final_lda = fitted_models[final_topic_num]["model"]
    final_doc_topic = fitted_models[final_topic_num]["doc_topic"]
    final_assigned_topic = fitted_models[final_topic_num]["assigned_topic"]
    final_topic_sizes = fitted_models[final_topic_num]["topic_sizes"]

    lda_df = lda_df.reset_index(drop=False).rename(columns={"index": "original_index"})
    lda_df["lda_topic"] = final_assigned_topic
    lda_df["lda_topic_probability"] = final_doc_topic.max(axis=1).round(6)

    # 最終 topic table
    final_topic_rows = []

    for topic_id in range(final_topic_num):
        top_words = get_topic_words(final_lda, feature_names, topic_id, TOP_WORDS_PER_TOPIC)
        topic_name = guess_topic_name(top_words)
        topic_size = int(final_topic_sizes.get(topic_id, 0))

        final_topic_rows.append({
            "topic_id": topic_id,
            "topic_name_auto": topic_name,
            "topic_size": topic_size,
            "top_words": ", ".join(top_words),
            "interpretation": make_interpretation(topic_name)
        })

    final_topics_df = pd.DataFrame(final_topic_rows)

    final_topics_df.to_csv(
        OUTPUT_DIR / "lda_topics.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # 每篇評論的 topic assignment
    doc_topic_cols = [f"topic_{i}_prob" for i in range(final_topic_num)]
    doc_topic_df = pd.DataFrame(final_doc_topic, columns=doc_topic_cols).round(6)

    assignment_cols = [
        "original_index",
        "AirlineName",
        "CabinType",
        "OverallScore",
        "Recommended",
        "Review",
        "lda_topic",
        "lda_topic_probability"
    ]

    assignment_cols = [col for col in assignment_cols if col in lda_df.columns]

    lda_assignments = pd.concat(
        [lda_df[assignment_cols].reset_index(drop=True), doc_topic_df],
        axis=1
    )

    lda_assignments.to_csv(
        OUTPUT_DIR / "lda_doc_topic_assignments.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # 找每個 topic 的代表性評論
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

    representative_df = pd.DataFrame(rep_rows)

    representative_df.to_csv(
        OUTPUT_DIR / "lda_representative_reviews.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # 畫 LDA topic size 圖
    fig, ax = plt.subplots(figsize=(10, 5))

    plot_df = final_topics_df.sort_values("topic_id")
    labels = [
        f"Topic {row.topic_id}\n{row.topic_name_auto[:22]}"
        for row in plot_df.itertuples()
    ]

    bars = ax.bar(labels, plot_df["topic_size"])

    ax.set_title(f"LDA Topic Distribution ({final_topic_num} Topics, Recommended = no)", fontsize=13, fontweight="bold")
    ax.set_xlabel("LDA Topic")
    ax.set_ylabel("Number of Reviews")
    ax.tick_params(axis="x", labelrotation=25)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_lda_topics.png", dpi=180, bbox_inches="tight")
    plt.close()

    print("LDA topic tables saved.")
    print("LDA representative reviews saved.")
    print("LDA topic figure saved.")

    return final_topics_df, representative_df, model_selection_df


lda_topics_df, lda_rep_df, lda_model_selection_df = run_lda_topic_modeling(df)


# =========================
# 7. 產出簡短文字摘要
# =========================

def write_summary_report(df, lda_topics_df, lda_model_selection_df):
    """輸出一份簡短 summary，方便你之後寫報告。"""
    print("\n" + "=" * 60)
    print("Step 5. Writing summary report")
    print("=" * 60)

    recommended_counts = df["Recommended"].value_counts().to_dict()

    sentiment_summary_path = OUTPUT_DIR / "sentiment_summary_by_recommended.csv"
    sentiment_summary = pd.read_csv(sentiment_summary_path)

    lines = []

    lines.append("Member B Analysis Summary")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Dataset")
    lines.append("-" * 60)
    lines.append(f"Input file: {INPUT_PATH.name}")
    lines.append(f"Total reviews used: {len(df)}")
    lines.append(f"Recommended = yes: {recommended_counts.get('yes', 0)}")
    lines.append(f"Recommended = no : {recommended_counts.get('no', 0)}")
    lines.append("")
    lines.append("Methods")
    lines.append("-" * 60)
    lines.append("1. TF keyword analysis was used to identify frequent terms.")
    lines.append("2. TF-IDF keyword analysis was used to identify representative terms for each group.")
    lines.append("3. VADER sentiment analysis was used to calculate sentiment scores from the original Review column.")
    lines.append("4. LDA topic modeling was applied mainly to not recommended reviews to identify complaint themes.")
    lines.append("")
    lines.append("Sentiment Summary")
    lines.append("-" * 60)

    for _, row in sentiment_summary.iterrows():
        lines.append(
            f"Recommended = {row['Recommended']}: "
            f"review_count = {row['review_count']}, "
            f"avg_sentiment = {row['avg_sentiment']}, "
            f"avg_overall_score = {row['avg_overall_score']}"
        )

    lines.append("")
    lines.append("LDA Model Selection")
    lines.append("-" * 60)

    for _, row in lda_model_selection_df.iterrows():
        lines.append(
            f"num_topics = {row['num_topics']}, perplexity = {row['perplexity']}"
        )

    lines.append("")
    lines.append(f"Final LDA topic number used in output: {FINAL_NUM_TOPICS}")
    lines.append("")
    lines.append("Final LDA Topics")
    lines.append("-" * 60)

    for _, row in lda_topics_df.iterrows():
        lines.append(
            f"Topic {row['topic_id']} | {row['topic_name_auto']} | "
            f"size = {row['topic_size']} | top words = {row['top_words']}"
        )

    lines.append("")
    lines.append("Important Output Files")
    lines.append("-" * 60)
    lines.append("tf_yes_keywords.csv")
    lines.append("tf_no_keywords.csv")
    lines.append("tf_yes_no_keyword_comparison.csv")
    lines.append("tfidf_yes_keywords.csv")
    lines.append("tfidf_no_keywords.csv")
    lines.append("tfidf_yes_no_keyword_comparison.csv")
    lines.append("tfidf_high_rated_keywords.csv")
    lines.append("tfidf_low_rated_keywords.csv")
    lines.append("sentiment_results.csv")
    lines.append("sentiment_summary_by_recommended.csv")
    lines.append("lda_model_selection.csv")
    lines.append("lda_topics.csv")
    lines.append("lda_representative_reviews.csv")
    lines.append("fig_tfidf_comparison.png")
    lines.append("fig_sentiment_dist.png")
    lines.append("fig_lda_topics.png")

    summary_text = "\n".join(lines)

    with open(OUTPUT_DIR / "member_b_summary_report.txt", "w", encoding="utf-8") as f:
        f.write(summary_text)

    print("Summary report saved.")


write_summary_report(df, lda_topics_df, lda_model_selection_df)


# =========================
# 8. 完成
# =========================

print("\n" + "=" * 60)
print("Member B pipeline finished successfully!")
print("=" * 60)
print(f"All outputs are saved in: {OUTPUT_DIR}")