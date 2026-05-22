# Airline Reviews Text Mining Dashboard 1

這是給老師展示用的 `dashboard_1`，保留原本 Member B 的 TF-IDF、Sentiment、LDA 與 Representative Reviews 頁面，並新增完整 VADER 驗證結果。

## 放置位置

請把 `dashboard_1/` 放在專案根目錄，並且和下列資料夾與檔案同一層：

```text
學姊/
├── dashboard_1/
├── output/
├── output_2/
├── output_vader_full/
├── output_vader_label_audit/
├── aviation_negative_lexicon.csv
├── aviation_positive_lexicon.csv
├── aviation_sentiment_lexicon_full.csv
└── sampled_20k_with_tokens.csv
```

## 執行方式

請在專案根目錄執行：

```bash
python -m http.server 8000
```

然後開啟：

```text
http://localhost:8000/dashboard_1/index.html
```

## Dashboard 頁面

1. 專題設計
2. TF / TF-IDF
3. 情緒分析結果
4. VADER 驗證比較
5. 資料標籤佐證
6. 航空詞彙調整
7. LDA 主題模型
8. 代表性評論

## 新增 VADER 頁面說明

### VADER 驗證比較

讀取：

```text
output_vader_full/vader_threshold_method_comparison_all_proxy.csv
output_vader_full/vader_best_config.json
output_vader_full/vader_sentence_statistics.csv
output_vader_full/fig_vader_threshold_method_accuracy.png
output_vader_full/fig_vader_best_method_accuracy.png
```

此頁比較：

- original VADER + full review
- original VADER + sentence average
- adjusted VADER + full review
- adjusted VADER + sentence average
- thresholds: ±0.05, ±0.10, ±0.30

### 資料標籤佐證

讀取：

```text
output_vader_label_audit/vader_dataset_label_alignment_metrics.csv
output_vader_label_audit/confusion_high_confidence_proxy.csv
output_vader_label_audit/confusion_recommended_proxy.csv
output_vader_label_audit/confusion_rating_proxy_three_class.csv
output_vader_label_audit/fig_vader_dataset_label_alignment.png
```

此頁用資料集自帶欄位佐證 VADER 結果：

- Recommended-based proxy label
- Rating-based proxy label
- High-confidence proxy label

### 航空詞彙調整

讀取：

```text
aviation_negative_lexicon.csv
aviation_positive_lexicon.csv
aviation_sentiment_lexicon_full.csv
output_vader_full/aviation_lexicon_applied_to_vader.csv
```

此頁說明 VADER 引用的三個航空詞彙 CSV，以及實際套用到 VADER 的詞彙。

## 重要結論

驗證後的最佳 VADER 設定為：

```text
original VADER + full Review input + threshold ±0.05
```

也就是原本的 VADER 做法經過更嚴謹驗證後仍然成立。航空詞彙調整與逐句平均都有被測試，但沒有明顯提升結果，因此最後保留原生 VADER。
