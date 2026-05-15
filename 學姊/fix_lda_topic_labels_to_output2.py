# fix_lda_topic_labels_to_output2.py
# Purpose:
# 修正 LDA topics 的人工解釋名稱，並輸出到 output_2 資料夾。
#
# 重要原則：
# 1. 不重新訓練 LDA
# 2. 不改 topic_id
# 3. 不改 topic_size
# 4. 不改 top_words
# 5. 不改 representative reviews
# 6. 只根據 top_words 和 representative reviews 修正 manual topic label
#
# 這不是造假結果，而是正式 topic modeling 分析中常見的
# manual interpretation / human labeling 步驟。

from pathlib import Path
import shutil
import pandas as pd


# =========================
# 1. 路徑設定
# =========================

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR = BASE_DIR / "output_2"
OUTPUT_DIR.mkdir(exist_ok=True)


# =========================
# 2. 檔案路徑
# =========================

MANUAL_FILE = INPUT_DIR / "lda_manual_interpretation_table.csv"
TOPICS_FILE = INPUT_DIR / "lda_topics.csv"

# 你的 extra 程式可能輸出這個檔名
REPRESENTATIVE_FILE_EXTRA = INPUT_DIR / "lda_representative_reviews_extra.csv"

# 原本主程式可能輸出這個檔名
REPRESENTATIVE_FILE_NORMAL = INPUT_DIR / "lda_representative_reviews.csv"


# =========================
# 3. 檢查檔案是否存在
# =========================

def check_required_files():
    missing_files = []

    if not MANUAL_FILE.exists():
        missing_files.append(str(MANUAL_FILE))

    if not TOPICS_FILE.exists():
        missing_files.append(str(TOPICS_FILE))

    if not REPRESENTATIVE_FILE_EXTRA.exists() and not REPRESENTATIVE_FILE_NORMAL.exists():
        missing_files.append(
            str(REPRESENTATIVE_FILE_EXTRA) + " 或 " + str(REPRESENTATIVE_FILE_NORMAL)
        )

    if missing_files:
        raise FileNotFoundError(
            "找不到必要檔案，請先確認 output 資料夾中有以下檔案：\n"
            + "\n".join(missing_files)
        )


# =========================
# 4. 人工修正 topic label
# =========================

# 這些 label 是根據 lda_topics.csv 的 top_words
# 以及 lda_representative_reviews 的內容做人工解釋。
# 注意：這裡沒有改模型結果，只是改 interpretation label。

MANUAL_TOPIC_LABELS = {
    0: "Boarding Delay and Airport Waiting",
    1: "Baggage Fees and Extra Charges",
    2: "Customer Service and Baggage Handling",
    3: "Flight Delay, Cancellation, and Missed Connections",
    4: "Booking, Refund, and Ticket Changes",
    5: "Cabin Experience, Seat, Food, and Crew Service",
    6: "Route-specific Service Complaints"
}

MANUAL_REASONING = {
    0: (
        "The top words and representative reviews suggest airport-side waiting experiences, "
        "including boarding, gate waiting, check-in, delayed arrival, and waiting time."
    ),
    1: (
        "The topic words indicate extra payment and baggage-related issues, including bags, "
        "seat selection, check-in luggage, extra charges, and paid services."
    ),
    2: (
        "The topic combines customer service and luggage handling issues. Words such as "
        "customer, service, told, call, help, luggage, and bag suggest unclear assistance "
        "and baggage-related complaints."
    ),
    3: (
        "This topic clearly reflects serious flight disruptions. Words such as delay, cancel, "
        "hour, wait, hotel, next, and connect are associated with long delays, cancellations, "
        "missed connections, and rebooking or accommodation problems."
    ),
    4: (
        "This topic focuses on booking, ticket, refund, and communication problems. Words such "
        "as book, ticket, refund, change, email, call, and customer service indicate problems "
        "before or after the flight rather than only the flight experience itself."
    ),
    5: (
        "This topic describes the in-flight and cabin experience. Words such as seat, food, "
        "service, class, crew, cabin, meal, economy, and business suggest comfort, meals, "
        "crew service, and cabin class experience."
    ),
    6: (
        "This topic contains many airline, airport, or route-related words, such as air, via, "
        "Canada, Dubai, Singapore, London, Sydney, and Emirates. Therefore, it is better "
        "interpreted as route-specific or airline-specific service complaints rather than "
        "a single service factor."
    )
}


# =========================
# 5. 驗證 topic_id 是否合理
# =========================

def validate_topic_ids(df, file_name):
    topic_ids = sorted(df["topic_id"].dropna().astype(int).unique().tolist())
    expected_ids = sorted(MANUAL_TOPIC_LABELS.keys())

    if topic_ids != expected_ids:
        raise ValueError(
            f"{file_name} 的 topic_id 與人工 label 設定不一致。\n"
            f"檔案中的 topic_id: {topic_ids}\n"
            f"程式設定的 topic_id: {expected_ids}\n"
            "請先檢查 LDA 是否仍然是 7 topics，或是否 topic_id 有變動。"
        )


# =========================
# 6. 修正 manual interpretation table
# =========================

def fix_manual_interpretation_table():
    manual_df = pd.read_csv(MANUAL_FILE)

    if "topic_id" not in manual_df.columns:
        raise ValueError("lda_manual_interpretation_table.csv 缺少 topic_id 欄位。")

    validate_topic_ids(manual_df, "lda_manual_interpretation_table.csv")

    # 保留原本自動命名，方便報告說明有做人工修正
    if "manual_topic_label" in manual_df.columns:
        manual_df["original_auto_or_previous_label"] = manual_df["manual_topic_label"]
    elif "topic_name_auto" in manual_df.columns:
        manual_df["original_auto_or_previous_label"] = manual_df["topic_name_auto"]
    else:
        manual_df["original_auto_or_previous_label"] = ""

    # 套用人工 label
    manual_df["manual_topic_label"] = manual_df["topic_id"].astype(int).map(MANUAL_TOPIC_LABELS)
    manual_df["complaint_category"] = manual_df["topic_id"].astype(int).map(MANUAL_TOPIC_LABELS)
    manual_df["reason_for_labeling"] = manual_df["topic_id"].astype(int).map(MANUAL_REASONING)

    # 加上方法說明，避免被誤會是在亂改結果
    manual_df["labeling_method"] = (
        "Manual interpretation based on LDA top words and representative reviews. "
        "The model output, topic_id, topic_size, top_words, and representative reviews were not changed."
    )

    manual_df["is_model_output_changed"] = "no"

    output_path = OUTPUT_DIR / "lda_manual_interpretation_table_fixed.csv"
    manual_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Saved: {output_path}")
    return manual_df


# =========================
# 7. 修正 lda_topics 表中的 topic label
# =========================

def fix_lda_topics_table():
    topics_df = pd.read_csv(TOPICS_FILE)

    if "topic_id" not in topics_df.columns:
        raise ValueError("lda_topics.csv 缺少 topic_id 欄位。")

    validate_topic_ids(topics_df, "lda_topics.csv")

    # 保留原本自動命名
    if "topic_name_auto" in topics_df.columns:
        topics_df["original_topic_name_auto"] = topics_df["topic_name_auto"]
    else:
        topics_df["original_topic_name_auto"] = ""

    # 新增人工修正版 label
    topics_df["manual_topic_label"] = topics_df["topic_id"].astype(int).map(MANUAL_TOPIC_LABELS)
    topics_df["manual_interpretation"] = topics_df["topic_id"].astype(int).map(MANUAL_REASONING)

    topics_df["labeling_method"] = (
        "Manual interpretation based on top_words and representative reviews. "
        "The LDA topic words and topic sizes remain unchanged."
    )

    topics_df["is_model_output_changed"] = "no"

    output_path = OUTPUT_DIR / "lda_topics_fixed.csv"
    topics_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Saved: {output_path}")
    return topics_df


# =========================
# 8. 修正代表性評論檔案中的 topic label
# =========================

def fix_representative_reviews():
    if REPRESENTATIVE_FILE_EXTRA.exists():
        rep_file = REPRESENTATIVE_FILE_EXTRA
    else:
        rep_file = REPRESENTATIVE_FILE_NORMAL

    rep_df = pd.read_csv(rep_file)

    if "topic_id" not in rep_df.columns:
        raise ValueError(f"{rep_file.name} 缺少 topic_id 欄位。")

    # representative reviews 可能某些 topic 沒評論，所以不強制 topic_id 完全等於 0-6
    rep_df["manual_topic_label"] = rep_df["topic_id"].astype(int).map(MANUAL_TOPIC_LABELS)
    rep_df["manual_interpretation"] = rep_df["topic_id"].astype(int).map(MANUAL_REASONING)

    if "topic_name_auto" in rep_df.columns:
        rep_df["original_topic_name_auto"] = rep_df["topic_name_auto"]

    rep_df["labeling_method"] = (
        "Manual topic label added based on LDA top words and representative reviews. "
        "Representative review text and topic probability were not changed."
    )

    rep_df["is_model_output_changed"] = "no"

    output_path = OUTPUT_DIR / "lda_representative_reviews_fixed.csv"
    rep_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Saved: {output_path}")
    return rep_df


# =========================
# 9. 複製其他重要輸出到 output_2
# =========================

def copy_supporting_files():
    supporting_files = [
        "lda_coherence_scores.csv",
        "fig_lda_coherence_scores.png",
        "fig_lda_topics.png",
        "lda_visualization.html",
        "tfidf_yes_no_keyword_comparison.csv",
        "sentiment_summary_by_recommended.csv",
        "fig_tfidf_comparison.png",
        "fig_sentiment_dist.png"
    ]

    for file_name in supporting_files:
        src = INPUT_DIR / file_name
        dst = OUTPUT_DIR / file_name

        if src.exists():
            shutil.copy2(src, dst)
            print(f"Copied: {dst}")


# =========================
# 10. 輸出修正說明
# =========================

def write_fix_summary(manual_df, topics_df):
    lines = []

    lines.append("LDA Topic Label Fix Summary")
    lines.append("=" * 70)
    lines.append("")
    lines.append("Purpose")
    lines.append("-" * 70)
    lines.append(
        "This file documents the manual topic labeling step for the LDA baseline. "
        "The purpose is to improve interpretability after checking the LDA top words "
        "and representative reviews."
    )
    lines.append("")
    lines.append("Important Methodological Note")
    lines.append("-" * 70)
    lines.append(
        "This step does not change the LDA model results. The topic_id, topic_size, "
        "top_words, representative reviews, and topic probabilities are preserved. "
        "Only the human-readable topic labels and interpretation explanations are updated."
    )
    lines.append("")
    lines.append("Fixed Topic Labels")
    lines.append("-" * 70)

    for topic_id in sorted(MANUAL_TOPIC_LABELS.keys()):
        top_words = ""

        if "top_words" in topics_df.columns:
            matched = topics_df[topics_df["topic_id"].astype(int) == topic_id]
            if len(matched) > 0:
                top_words = matched.iloc[0]["top_words"]

        lines.append(f"Topic {topic_id}: {MANUAL_TOPIC_LABELS[topic_id]}")
        lines.append(f"Reason: {MANUAL_REASONING[topic_id]}")
        if top_words:
            lines.append(f"Top words: {top_words}")
        lines.append("")

    lines.append("Output Files")
    lines.append("-" * 70)
    lines.append("output_2/lda_manual_interpretation_table_fixed.csv")
    lines.append("output_2/lda_topics_fixed.csv")
    lines.append("output_2/lda_representative_reviews_fixed.csv")
    lines.append("")
    lines.append("Recommended Report Sentence")
    lines.append("-" * 70)
    lines.append(
        "After examining the LDA top words and representative reviews, the topics were "
        "manually labeled to improve interpretability. This manual labeling step did not "
        "modify the model output; it only provided clearer human-readable names for the topics."
    )

    output_path = OUTPUT_DIR / "lda_topic_label_fix_summary.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Saved: {output_path}")


# =========================
# 11. Main
# =========================

def main():
    print("=" * 70)
    print("Fixing LDA topic labels and saving results to output_2")
    print("=" * 70)

    check_required_files()

    manual_df = fix_manual_interpretation_table()
    topics_df = fix_lda_topics_table()
    fix_representative_reviews()
    copy_supporting_files()
    write_fix_summary(manual_df, topics_df)

    print("\nDone.")
    print(f"All fixed files are saved in: {OUTPUT_DIR}")
    print("\nImportant:")
    print("This script only changes human-readable topic labels.")
    print("It does not change the LDA model, top words, topic sizes, or representative reviews.")


if __name__ == "__main__":
    main()