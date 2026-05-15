# Airline Reviews Text Mining Dashboard — Member B

## 1. 這個 dashboard 是做什麼的？

這個 dashboard 是給 Airline Reviews Text Mining final project 使用的前端展示頁面，主要整理 **Member B（林冠妤）** 已完成的分析結果：

- TF / TF-IDF keyword analysis
- Recommended = yes vs Recommended = no keyword comparison
- VADER sentiment analysis
- Sentiment distribution by Recommended group
- LDA topic modeling baseline
- LDA coherence score
- LDA manually revised topic labels
- LDA representative reviews
- pyLDAvis interactive visualization link

這個 dashboard 目前先展示 Member B 的結果，之後 Member C 可以再加入 BERTopic、LDA vs BERTopic comparison、dashboard final integration。

---

## 2. 建議資料夾位置

請在原本專案資料夾底下新增 `dashboard/`，整體結構建議如下：

```text
學姊/
├── figures/
├── output/
├── output_2/
├── venv/
├── add_tokens_and_plots.py
├── member_b_pipeline.py
├── member_b_lda_extra.py
├── fix_lda_topic_labels_to_output2.py
├── sampled_20k_dataset.csv
├── sampled_20k_with_tokens.csv
└── dashboard/
    ├── index.html
    ├── styles.css
    ├── app.js
    └── README.md
```

dashboard 會讀取上一層資料夾中的：

```text
../output/
../output_2/
```

所以 `dashboard/` 要和 `output/`、`output_2/` 放在同一個專案根目錄底下。

---

## 3. 需要的檔案

### output/ 主要使用檔案

```text
fig_tfidf_comparison.png
fig_sentiment_dist.png
fig_lda_topics.png
fig_lda_coherence_scores.png
lda_visualization.html
tfidf_yes_no_keyword_comparison.csv
sentiment_summary_by_recommended.csv
```

### output_2/ 主要使用檔案

```text
lda_topics_fixed.csv
lda_manual_interpretation_table_fixed.csv
lda_representative_reviews_fixed.csv
lda_topic_label_fix_summary.txt
tfidf_yes_no_keyword_comparison.csv
sentiment_summary_by_recommended.csv
fig_tfidf_comparison.png
fig_sentiment_dist.png
fig_lda_topics.png
fig_lda_coherence_scores.png
lda_visualization.html
```

dashboard 會優先讀取 `output_2/`，如果找不到，才會嘗試讀取 `output/` 的同名檔案。

---

## 4. 安裝與執行方式

這個 dashboard 是純前端 HTML/CSS/JavaScript，不需要 npm，也不需要 React。

但是因為瀏覽器直接用雙擊開啟 `index.html` 時，可能會因為安全限制讀不到 CSV 檔案，所以建議用 Python 開本地伺服器。

### Step 1：進入專案根目錄

```bash
cd 學姊
```

請注意：不是進入 dashboard，而是進入包含 output、output_2、dashboard 的那一層。

### Step 2：啟動本地 server

```bash
python -m http.server 8000
```

如果你的電腦用 `py` 指令：

```bash
py -m http.server 8000
```

### Step 3：開啟 dashboard

在瀏覽器輸入：

```text
http://localhost:8000/dashboard/index.html
```

---

## 5. Dashboard 頁面功能

### 5.1 專題設計

此頁說明整體研究設計：

- 使用 Recommended 做分層抽樣
- yes 10,000 筆
- no 10,000 筆
- total 20,000 筆
- LDA 和 BERTopic 使用同一份 sampled dataset
- random_state = 42
- 三人分工：A 資料、B 傳統方法與 LDA、C BERTopic 與整合

---

### 5.2 TF / TF-IDF 關鍵字

此頁讀取：

```text
tfidf_yes_no_keyword_comparison.csv
fig_tfidf_comparison.png
```

功能：

- 顯示 Recommended = yes vs Recommended = no 的 TF-IDF keyword table
- 顯示 TF-IDF comparison chart
- 可用搜尋框搜尋 keyword
- 說明推薦評論和不推薦評論的主要語意差異

分析重點：

- Recommended = yes 通常偏向 good、crew、friendly、comfortable、excellent 等正向詞
- Recommended = no 通常偏向 delayed、bag、ticket、customer service、worst、pay 等抱怨詞

---

### 5.3 Sentiment Analysis

此頁讀取：

```text
sentiment_summary_by_recommended.csv
fig_sentiment_dist.png
```

功能：

- 顯示 Recommended = yes / no 的平均 sentiment score
- 顯示 review count 和平均 OverallScore
- 顯示 VADER sentiment distribution chart

分析重點：

- VADER 使用原始 Review 欄位
- compound score 範圍為 -1 到 +1
- Recommended = yes 的 sentiment score 應明顯高於 Recommended = no
- 情緒分數、推薦標籤、OverallScore 大致一致

---

### 5.4 LDA Topic Modeling

此頁讀取：

```text
lda_topics_fixed.csv
fig_lda_topics.png
fig_lda_coherence_scores.png
lda_visualization.html
```

功能：

- 顯示 LDA topic distribution chart
- 顯示 LDA coherence score chart
- 顯示人工修正後的 LDA topic label table
- 提供 pyLDAvis HTML 連結

重要說明：

LDA 本身輸出的是 topic-word distribution，不會自動知道主題名稱。因此 Member B 根據 top words 和 representative reviews 做人工命名。

這個人工命名不改：

- topic_id
- topic_size
- top_words
- representative reviews
- topic probabilities
- model output

只改：

- manual_topic_label
- complaint_category
- reason_for_labeling

這是正式 topic modeling 分析中合理的 manual interpretation step。

---

### 5.5 Representative Reviews

此頁讀取：

```text
lda_representative_reviews_fixed.csv
```

功能：

- 顯示每個 LDA topic 的代表性評論
- 可依 topic 篩選
- 顯示 topic probability、AirlineName、OverallScore、代表性文字

用途：

- 幫助驗證 topic label 是否合理
- 可作為 final report 中質性分析的引用素材
- 可給 Member C 做 LDA vs BERTopic representative reviews comparison

---

## 6. 中英文切換

dashboard 左下角有語言切換按鈕：

```text
EN / 中文
```

點擊後可以一鍵切換：

- 全中文介面
- 全英文介面

注意：CSV 原始內容中的英文 keyword、review text 不會翻譯，因為那些是分析結果與原始資料內容，不應該任意翻譯或改寫。

---

## 7. 給下一位的交接建議

下一位如果要加入 BERTopic，可以新增：

```text
bertopic_topics.csv
bertopic_representative_reviews.csv
bertopic_topic_distribution.png
lda_vs_bertopic_comparison.csv
fig_bertopic_topics.png
```

然後在 dashboard 中新增一個頁面：

```text
BERTopic / Model Comparison
```

建議比較內容：

- topic number
- topic size
- top words
- representative reviews
- interpretability
- topic coherence 或 topic diversity
- 哪個模型比較能抓到 passenger complaints

---

## 8. 常見問題

### Q1：為什麼不能直接雙擊 index.html？

因為 dashboard 需要讀取 CSV 和圖片，直接用 file:// 開啟時，有些瀏覽器會擋掉 fetch local files。

請使用：

```bash
python -m http.server 8000
```

再開：

```text
http://localhost:8000/dashboard/index.html
```

### Q2：如果圖沒有顯示怎麼辦？

請確認：

```text
output_2/fig_tfidf_comparison.png
output_2/fig_sentiment_dist.png
output_2/fig_lda_topics.png
output_2/fig_lda_coherence_scores.png
```

是否存在。

如果 output_2 沒有，dashboard 也可以改成讀 output 中的圖片。

### Q3：如果表格沒有資料怎麼辦？

請確認是否用 http server 開啟，且 CSV 檔案存在：

```text
output_2/tfidf_yes_no_keyword_comparison.csv
output_2/sentiment_summary_by_recommended.csv
output_2/lda_topics_fixed.csv
output_2/lda_representative_reviews_fixed.csv
```

---

## 9. Dashboard 使用的主要技術

- HTML
- CSS
- JavaScript
- 本地 CSV 讀取
- 本地 PNG 圖片展示
- bilingual UI dictionary
- tab-based multi-page layout
- responsive design

不需要：

- React
- Node.js
- npm
- backend database
- Flask

---

## 10. Member B dashboard 完成項目

本 dashboard 已完成：

- 分頁式介面
- 中英文切換
- TF-IDF 結果展示
- Sentiment 結果展示
- LDA topic 結果展示
- LDA coherence score 圖展示
- LDA representative reviews 展示
- output / output_2 檔案用途說明
- pyLDAvis 連結
- README.md 交接文件


---

## Teacher-facing version note

這個版本已移除「交接與檔案說明」分頁，讓 dashboard 更適合直接展示給老師。
目前保留的分頁包含：

1. 專題設計
2. TF / TF-IDF 關鍵字
3. 情緒分析
4. LDA 主題模型
5. 代表性評論

檔案交接與執行說明仍保留在 README.md，不會顯示在網頁主畫面中。
