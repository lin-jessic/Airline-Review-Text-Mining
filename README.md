# Airline-Review-Text-Mining
網頁文字探勘
請閱讀學姊這個資料夾的README.md，member A & member B & member C詳細的工作內容文件則是放置在文件說明這個資料夾中(兩個docx)。

## 線上 Dashboard（直接點擊開啟）

> **[點此開啟 Dashboard](https://lin-jessic.github.io/Airline-Review-Text-Mining/%E5%AD%B8%E5%A7%8A/dashboard_2/index.html)**

---

## Airline Reviews Text Mining Dashboard 操作說明

本專題提供一個整合式互動 Dashboard，用來呈現 Airline Reviews Text Mining 的主要分析結果。
最終結果的 Dashboard 放置於 `學姊/dashboard_2/` 資料夾中，為完整整合版介面，內容包含 Member B 的 TF / TF-IDF、VADER 情緒分析、LDA 主題模型與標籤驗證結果，也整合 Member C 新增的 BERTopic 主題分析、模型比較，以及跨時間與航空公司分析。

---

### 1. Dashboard 放置位置

請確認專案資料夾中有以下結構：

```text
學姊/
├── dashboard_2/
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── README.md
├── output/
├── output_2/
├── output_vader_full/
├── output_vader_label_audit/
├── output_c/
├── aviation_negative_lexicon.csv
├── aviation_positive_lexicon.csv
└── aviation_sentiment_lexicon_full.csv
```

其中：

* `dashboard_2/`：Dashboard 主程式資料夾
* `index.html`：Dashboard 主頁面
* `app.js`：Dashboard 互動邏輯與圖表載入設定
* `styles.css`：Dashboard 頁面樣式
* `output/`：Member B 原始分析結果
* `output_2/`：Member B 修正版分析結果
* `output_vader_full/`：VADER 全量驗證結果
* `output_vader_label_audit/`：資料標籤佐證結果
* `output_c/`：Member C 新增分析結果，包含 BERTopic、RQ2、RQ3 相關圖表與 CSV 檔案

---

### 2. Dashboard 執行方式

請先開啟終端機或命令提示字元，並進入 `學姊/` 資料夾。

```bash
cd 學姊
```

接著啟動 Python 內建的本機伺服器：

```bash
python -m http.server 8000
```

成功啟動後，終端機會顯示類似以下訊息：

```text
Serving HTTP on :: port 8000
```

接著打開瀏覽器，輸入以下網址：

```text
http://localhost:8000/dashboard_2/index.html
```

即可開啟 Dashboard 主頁面。

---

### 3. 注意事項

執行 Dashboard 時，請務必在 `學姊/` 資料夾內啟動伺服器，而不是直接進入 `dashboard_2/` 資料夾執行。

正確方式：

```bash
cd 學姊
python -m http.server 8000
```

不建議直接在 `dashboard_2/` 內執行，因為 Dashboard 需要讀取上一層資料夾中的 `output/`、`output_2/`、`output_vader_full/`、`output_vader_label_audit/` 與 `output_c/` 等分析結果資料夾。
如果執行位置錯誤，部分圖片、CSV 檔案或分析結果可能會無法載入。

---

### 4. Dashboard 主要頁面內容

Dashboard 共整合多個分析頁面，主要分為 Member B 分析結果與 Member C 新增分析結果。

#### Member B 分析結果

1. **專題設計**
   說明本專題的研究問題、資料來源與整體分析流程。

2. **TF / TF-IDF 關鍵字**
   顯示不同評分、推薦與不推薦評論中的重要關鍵字，協助觀察乘客最常提及的航空服務問題。

3. **情緒分析結果**
   使用 VADER 進行情緒分析，觀察評論文字中的正向、負向與中性情緒分布。

4. **VADER 驗證比較**
   比較不同 VADER 設定版本，例如原生 VADER、航空詞彙調整版、整段分析與句子平均分析。

5. **資料標籤佐證**
   透過 rating 與 recommended 欄位交叉檢查，驗證資料標籤與情緒結果是否具有一致性。

6. **航空詞彙調整**
   說明本專題如何針對航空評論語境補充正向與負向詞彙，使 VADER 更符合航空評論分析需求。

7. **LDA 主題模型**
   使用 LDA 找出評論中常見的抱怨主題，例如 delay、seat、staff、baggage、refund、food、value 等。

8. **代表性評論**
   顯示不同主題或情緒分類下的代表性評論，協助理解模型分析結果與原始文字之間的對應關係。

#### Member C 新增分析結果

9. **BERTopic 主題分析**
   使用 BERTopic 對不推薦評論進行語意主題分群，透過 sentence-transformers、UMAP 與 HDBSCAN 找出更細緻的語意主題。

10. **模型比較與 RQ2**
    比較 LDA 與 BERTopic 的主題分析結果，並分析不同評分群組與矛盾旅客的評論特徵。

11. **RQ3 跨時間與航空公司分析**
    分析不同航空公司與不同時間階段中的關鍵字變化，例如疫情前、疫情期間與疫情後的評論差異。

---

### 5. Dashboard 使用方式

開啟 Dashboard 後，老師可以透過頁面中的導覽列或頁面區塊切換不同分析結果。
每個頁面皆會呈現對應的圖表、表格或文字說明，方便快速查看本專題的分析流程與研究發現。

建議查看順序如下：

1. 先查看「專題設計」，了解研究問題與資料處理流程。
2. 接著查看「TF / TF-IDF 關鍵字」與「情緒分析結果」，了解文字探勘的基礎分析結果。
3. 再查看「VADER 驗證比較」與「資料標籤佐證」，確認情緒分析方法的合理性。
4. 接著查看「LDA 主題模型」與「BERTopic 主題分析」，比較傳統主題模型與語意主題模型的差異。
5. 最後查看「模型比較與 RQ2」以及「RQ3 跨時間與航空公司分析」，了解不同模型、不同航空公司與不同時間階段下的評論差異。

---

### 6. Dashboard 補充說明

本 Dashboard 主要作為專題分析結果的視覺化展示介面。
它不是重新執行資料分析的程式，而是讀取已經產生好的圖表與 CSV 結果，並將 Member B 與 Member C 的分析成果整合成可互動瀏覽的網頁。

因此，在開啟 Dashboard 前，必須確認相關輸出資料夾與圖片檔案皆已放在正確位置。
若出現圖片無法顯示或資料讀取失敗，請優先檢查：

1. 是否在 `學姊/` 資料夾內執行 `python -m http.server 8000`
2. `dashboard_2/` 是否存在
3. `output/`、`output_2/`、`output_vader_full/`、`output_vader_label_audit/`、`output_c/` 是否存在
4. 圖片檔名與 CSV 檔名是否與程式設定一致
5. 瀏覽器網址是否為：

```text
http://localhost:8000/dashboard_2/index.html
```
