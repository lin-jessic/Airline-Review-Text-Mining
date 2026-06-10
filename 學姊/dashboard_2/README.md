# Airline Reviews Text Mining Dashboard 2

這是 **dashboard_2**，由 Member C 完成的完整整合版 Dashboard，包含 Member B 的所有分析結果，以及 Member C 新增的 BERTopic、模型比較（RQ2）、跨時間與航空公司分析（RQ3）。

## 放置位置

請把 `dashboard_2/` 放在專案根目錄，並確認以下資料夾都存在：

```text
學姊/
├── dashboard_2/              ← 本資料夾
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── README.md
├── output/                   ← Member B 原始結果
├── output_2/                 ← Member B 修正版結果
├── output_vader_full/        ← Member B VADER 驗證結果
├── output_vader_label_audit/ ← Member B 標籤佐證結果
├── output_c/                 ← Member C 新增結果（需建立）
│   ├── fig_bertopic_top15_distribution.png
│   ├── fig_bertopic_top_keywords.png
│   ├── fig_bertopic_rating_groups.png
│   ├── fig_contradictory_vs_normal.png
│   ├── fig_lda_vs_bertopic_comparison.png
│   ├── fig_airline_keywords_heatmap_clean.png
│   ├── fig_period_keywords.png
│   ├── bertopic_final_results.csv
│   ├── lda_vs_bertopic_comparison.csv
│   ├── rq3_airline_keywords.csv
│   └── rq3_period_keywords_full.csv
├── aviation_negative_lexicon.csv
├── aviation_positive_lexicon.csv
└── aviation_sentiment_lexicon_full.csv
```

## 執行方式

請在 `學姊/` 資料夾內執行（不是專案根目錄）：

```bash
cd 學姊
python -m http.server 8000
```

然後開啟：

```text
http://localhost:8000/dashboard_2/index.html
```

## Dashboard 頁面

### Member B 分析結果（原有）
1. 專題設計
2. TF / TF-IDF 關鍵字
3. 情緒分析結果
4. VADER 驗證比較
5. 資料標籤佐證
6. 航空詞彙調整
7. LDA 主題模型
8. 代表性評論

### Member C 新增分析（新增）
9. BERTopic 主題分析
10. 模型比較與 RQ2
11. RQ3 跨時間與航空公司

## Member C 分析說明

### BERTopic 主題分析（對應 RQ1）

使用 sentence-transformers（all-MiniLM-L6-v2）對 10,000 筆不推薦評論進行語意嵌入，再透過 UMAP 降維與 HDBSCAN 分群，自動找出 40 個語意主題。

最終設定：
- `min_topic_size = 30`
- Stop words 包含常見停用詞、航空公司名稱、地名
- 資料：`sampled_20k_dataset.csv` 中的 Recommended = no 評論

### 模型比較與 RQ2

- LDA（7個主題）vs BERTopic（40個主題）對應關係表
- 低評分（1-4）、中評分（5-7）、高評分（8-10）三組的主題比較
- 矛盾旅客分析：評分 5-10 但不推薦的旅客關鍵字比較

### RQ3 跨時間與航空公司

- 前10大航空公司的 TF-IDF 關鍵字熱力圖
- 疫情前（2013-2019）、疫情期間（2020-2021）、疫情後（2022-2023）的關鍵字變化

## styles.css

直接使用 Member B 的 `styles.css`，不需要修改。
