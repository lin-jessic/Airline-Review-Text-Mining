const state = {
  lang: "zh",
  data: {
    tfidf: [],
    sentiment: [],
    ldaTopics: [],
    reviews: [],
    vaderComparison: [],
    vaderBestConfig: null,
    vaderSentenceStats: [],
    labelAudit: [],
    confusionHigh: [],
    confusionRec: [],
    confusionRating: [],
    appliedLexicon: [],
    fullLexicon: [],
    negativeLexicon: [],
    positiveLexicon: []
  }
};

const i18n = {
  zh: {
    appTitle: "航空評論文字探勘",
    appSubtitle: "Member B Results Dashboard",
    navOverview: "專題設計",
    navKeywords: "TF / TF-IDF",
    navSentiment: "情緒分析結果",
    navVaderValidation: "VADER 驗證比較",
    navLabelAudit: "資料標籤佐證",
    navLexicon: "航空詞彙調整",
    navLda: "LDA 主題模型",
    navReviews: "代表性評論",
    langHint: "點擊切換英文介面",
    eyebrow: "Airline Reviews Text Mining Final Project",
    statusText: "讀取分析結果與圖表",
    pageTitleOverview: "專題設計與資料策略",
    pageTitleKeywords: "TF / TF-IDF 關鍵字分析",
    pageTitleSentiment: "Validated VADER 情緒分析",
    pageTitleVaderValidation: "VADER 方法驗證與比較",
    pageTitleLabelAudit: "資料集自帶標籤一致性佐證",
    pageTitleLexicon: "航空領域詞彙調整分析",
    pageTitleLda: "LDA 主題模型分析",
    pageTitleReviews: "LDA 代表性評論",
    overviewEyebrow: "Balanced Sampling Design",
    overviewTitle: "以 Recommended 做分層抽樣，讓 LDA 與 BERTopic 公平比較",
    overviewDesc: "本專題將 Airline Reviews dataset 依照 Recommended 欄位縮減為平衡資料集：yes 10,000 筆、no 10,000 筆，共 20,000 筆。Member B 使用同一份 sampled_20k_with_tokens.csv 完成 TF/TF-IDF、VADER sentiment analysis 與 LDA baseline。",
    metricTotal: "總評論數",
    metricYes: "Recommended = yes",
    metricNo: "Recommended = no",
    metricSeed: "Random state",
    memberA: "Member A：資料與前處理",
    memberADesc: "負責資料清理、分層抽樣、tokens 欄位、token_count 與 EDA 圖表。",
    memberB: "Member B：傳統方法、VADER 與 LDA",
    memberBDesc: "負責 TF/TF-IDF、VADER 嚴謹驗證、航空詞彙調整比較、資料標籤佐證、LDA baseline 與代表性評論。",
    memberC: "Member C：BERTopic 與展示",
    memberCDesc: "負責 BERTopic、LDA vs BERTopic 比較、dashboard / presentation 整合。",
    methodFlow: "Member B 分析流程",
    flow1: "讀取 sampled_20k_with_tokens.csv",
    flow2: "使用 review_cleaned 做 TF / TF-IDF",
    flow3: "使用 Review 原文做 VADER，並驗證四種設定",
    flow4: "使用 tokens 做 LDA topic modeling",
    flow5: "整合圖表、CSV、代表性評論與人工解釋",
    bestFindingTitle: "本次 VADER 驗證的主要結論",
    bestFindingDesc: "經過完整 20,000 筆重新評分與 17,567 筆 high-confidence proxy validation 後，最佳設定為原生 VADER、整段 Review 輸入、預設門檻 ±0.05。航空詞彙調整與逐句平均都有被測試，但沒有比原生整段輸入更好。",
    keywordsTitle: "推薦與不推薦評論的關鍵字差異",
    keywordsDesc: "TF-IDF 用於找出各群組較具代表性的詞，協助比較 Recommended = yes 與 Recommended = no 的語意差異。",
    tfidfTableTitle: "TF-IDF yes/no 比較表",
    searchPlaceholder: "搜尋 keyword...",
    yesInsightTitle: "推薦評論常見語意",
    yesInsight: "通常偏向服務、舒適度、友善、良好經驗，例如 good、crew、friendly、comfortable、excellent。",
    noInsightTitle: "不推薦評論常見語意",
    noInsight: "通常偏向延誤、等待、客服、行李、票務與額外費用，例如 delayed、bag、ticket、customer service、worst、pay。",
    sentimentTitle: "最終 VADER 情緒分析結果",
    sentimentDesc: "最終設定採用原生 VADER、整段 Review 輸入、預設門檻 ±0.05。此頁呈現 Recommended yes/no 的最終情緒差異。",
    sentimentSummaryTitle: "Validated VADER Summary by Recommended",
    sentimentNote: "Recommended = yes 的平均情緒分數約為 0.747，Recommended = no 約為 -0.362，方向與推薦標籤與 OverallScore 一致。",
    vaderValidationTitle: "四種 VADER 設定與三種門檻比較",
    vaderValidationDesc: "此頁比較原生 VADER / 航空詞彙調整 VADER，以及整段 Review / 逐句平均兩種輸入形式，並測試 ±0.05、±0.10、±0.30 三種門檻。",
    vaderThresholdTableTitle: "Threshold and Method Comparison",
    whyFullReviewTitle: "為什麼最後選整段 Review？",
    whyFullReviewDesc: "雖然逐句平均可以避免長評論正負情緒互相抵銷，但實際驗證結果顯示，整段 Review 的 accuracy 明顯較高。這代表在本資料集中，完整評論語境對 VADER 判斷更穩定。",
    whyOriginalTitle: "為什麼保留原生 VADER？",
    whyOriginalDesc: "航空詞彙調整後的 accuracy 沒有明顯提升，代表許多航空評論的情緒來自整體語境，不只是單一航空詞彙。因此最終保留原生 VADER 是有資料支持的選擇。",
    sentenceStatsTitle: "長評論與逐句切分驗證",
    labelAuditTitle: "用資料集自帶分數與推薦標籤佐證 VADER 結果",
    labelAuditDesc: "除了 high-confidence proxy validation，本 dashboard 也加入資料集自帶標籤一致性檢查：Recommended-based label、Rating-based label，以及兩者共同建立的 high-confidence proxy。",
    labelAuditTableTitle: "Dataset Label Alignment Metrics",
    highProxyTitle: "High-confidence proxy",
    highProxyDesc: "Rating 1–4 且 Recommended = no 標為 negative；Rating 7–10 且 Recommended = yes 標為 positive。這是最嚴格、最主要的驗證依據。",
    recProxyTitle: "Recommended proxy",
    recProxyDesc: "直接用 Recommended = yes/no 對應 positive/negative，可檢查 VADER 與推薦行為的一致性。",
    ratingProxyTitle: "Rating proxy",
    ratingProxyDesc: "OverallScore 7–10 為 positive、5–6 為 neutral、1–4 為 negative，可檢查 VADER 與數字評分的一致性。",
    confusionTitle: "Confusion Matrices",
    lexiconTitle: "航空領域詞彙調整與引用資料",
    lexiconDesc: "本次 VADER 驗證引用三個航空情緒詞彙 CSV，並將適合旅客評論情境的詞彙加入 VADER lexicon，再比較調整前後效果。",
    negativeLexiconDesc: "航空領域負向詞彙，例如 delay、cancel、stranded、overbooked 相關語意。",
    positiveLexiconDesc: "航空領域正向詞彙，例如 friendly、comfortable、smooth、upgrade 相關語意。",
    fullLexiconDesc: "整合版航空情緒詞彙表，包含 term、polarity、score、category、domain 等欄位。",
    appliedLexiconTitle: "實際套用到 VADER 的詞彙",
    fullLexiconTitle: "引用詞彙總表預覽",
    lexiconConclusionTitle: "詞彙調整結果怎麼解釋？",
    lexiconConclusionDesc: "航空詞彙調整是合理的驗證步驟，但結果顯示它沒有明顯提高 accuracy。因此本研究不是強行使用調整版，而是根據驗證結果保留原生 VADER。這也表示旅客評論的情緒常由完整句子與語境決定，而不只是由單一航空詞彙決定。",
    ldaTitle: "不推薦評論中的主要抱怨主題",
    ldaDesc: "LDA 主要針對 Recommended = no 評論，找出 passenger complaints 的主題結構。",
    ldaTopicsTableTitle: "LDA 修正版人工主題命名",
    manualLabelTitle: "為什麼要人工修正 Topic Label？",
    manualLabelDesc: "LDA 產生的是 topic-word distribution，不會自動理解主題名稱。因此本 dashboard 使用 output_2 的修正版：保留 topic_id、topic_size、top_words、representative reviews，不改模型結果，只根據 top words 與代表性評論提供更清楚的人工主題命名。",
    openLdaVis: "開啟 pyLDAvis 互動視覺化",
    reviewsTitle: "每個 LDA Topic 的代表性評論",
    reviewsDesc: "代表性評論用來驗證 topic label 是否合理，並提供報告中的質性解釋素材。",
    topicFilterLabel: "選擇 Topic",
    allTopics: "全部 Topics",
    readFail: "部分資料讀取失敗，請確認是否使用 http server 開啟。"
  },
  en: {
    appTitle: "Airline Review Text Mining",
    appSubtitle: "Member B Results Dashboard",
    navOverview: "Project Design",
    navKeywords: "TF / TF-IDF",
    navSentiment: "Sentiment Results",
    navVaderValidation: "VADER Validation",
    navLabelAudit: "Dataset Label Audit",
    navLexicon: "Aviation Lexicon",
    navLda: "LDA Topic Model",
    navReviews: "Representative Reviews",
    langHint: "Click to switch Chinese UI",
    eyebrow: "Airline Reviews Text Mining Final Project",
    statusText: "Loading analysis outputs and figures",
    pageTitleOverview: "Project Design and Data Strategy",
    pageTitleKeywords: "TF / TF-IDF Keyword Analysis",
    pageTitleSentiment: "Validated VADER Sentiment Analysis",
    pageTitleVaderValidation: "VADER Method Validation and Comparison",
    pageTitleLabelAudit: "Dataset-derived Label Alignment Evidence",
    pageTitleLexicon: "Aviation-domain Lexicon Adjustment",
    pageTitleLda: "LDA Topic Modeling Results",
    pageTitleReviews: "LDA Representative Reviews",
    overviewEyebrow: "Balanced Sampling Design",
    overviewTitle: "Stratified sampling by Recommended enables a fair LDA vs BERTopic comparison",
    overviewDesc: "The project reduces the Airline Reviews dataset into a balanced 20,000-review dataset based on the Recommended field: 10,000 recommended and 10,000 not recommended reviews. Member B uses the same sampled_20k_with_tokens.csv for TF/TF-IDF, VADER sentiment analysis, and LDA baseline.",
    metricTotal: "Total Reviews",
    metricYes: "Recommended = yes",
    metricNo: "Recommended = no",
    metricSeed: "Random state",
    memberA: "Member A: Data and Preprocessing",
    memberADesc: "Responsible for cleaning, stratified sampling, tokens, token_count, and EDA figures.",
    memberB: "Member B: Traditional Methods, VADER, and LDA",
    memberBDesc: "Responsible for TF/TF-IDF, rigorous VADER validation, aviation lexicon adjustment comparison, dataset label audit, LDA baseline, and representative reviews.",
    memberC: "Member C: BERTopic and Presentation",
    memberCDesc: "Responsible for BERTopic, LDA vs BERTopic comparison, dashboard / presentation integration.",
    methodFlow: "Member B Analysis Workflow",
    flow1: "Load sampled_20k_with_tokens.csv",
    flow2: "Use review_cleaned for TF / TF-IDF",
    flow3: "Use original Review text for VADER and validate four settings",
    flow4: "Use tokens for LDA topic modeling",
    flow5: "Integrate figures, CSV tables, representative reviews, and interpretation",
    bestFindingTitle: "Main finding from VADER validation",
    bestFindingDesc: "After rescoring all 20,000 reviews and validating on 17,567 high-confidence proxy reviews, the best setting is original VADER, full-review input, and the default ±0.05 threshold. Aviation lexicon adjustment and sentence averaging were both tested but did not outperform the original full-review method.",
    keywordsTitle: "Keyword differences between recommended and not recommended reviews",
    keywordsDesc: "TF-IDF identifies representative terms for each group and compares semantic differences between Recommended = yes and no reviews.",
    tfidfTableTitle: "TF-IDF yes/no Comparison Table",
    searchPlaceholder: "Search keyword...",
    yesInsightTitle: "Common meaning in recommended reviews",
    yesInsight: "Recommended reviews tend to emphasize service, comfort, friendliness, and positive experiences, such as good, crew, friendly, comfortable, and excellent.",
    noInsightTitle: "Common meaning in not recommended reviews",
    noInsight: "Not recommended reviews tend to emphasize delays, waiting, customer service, baggage, ticketing, and extra payment issues, such as delayed, bag, ticket, customer service, worst, and pay.",
    sentimentTitle: "Final VADER sentiment results",
    sentimentDesc: "The final setting uses original VADER, full-review input, and the default ±0.05 threshold. This page presents final sentiment differences by Recommended group.",
    sentimentSummaryTitle: "Validated VADER Summary by Recommended",
    sentimentNote: "Recommended = yes has an average sentiment score around 0.747, while Recommended = no is around -0.362, consistent with recommendation labels and OverallScore.",
    vaderValidationTitle: "Four VADER settings and three thresholds",
    vaderValidationDesc: "This page compares original / aviation-adjusted VADER, full-review / sentence-average input forms, and ±0.05, ±0.10, ±0.30 thresholds.",
    vaderThresholdTableTitle: "Threshold and Method Comparison",
    whyFullReviewTitle: "Why choose full-review input?",
    whyFullReviewDesc: "Although sentence averaging may reduce sentiment cancellation in long reviews, the validation results show that full-review input achieves higher accuracy. In this dataset, full-context review input is more stable for VADER.",
    whyOriginalTitle: "Why retain original VADER?",
    whyOriginalDesc: "Aviation lexicon adjustment did not significantly improve accuracy. This suggests that sentiment in airline reviews is often determined by broader context, not only isolated aviation terms.",
    sentenceStatsTitle: "Long-review and sentence-splitting validation",
    labelAuditTitle: "Using dataset-provided ratings and recommendation labels to support VADER",
    labelAuditDesc: "In addition to high-confidence proxy validation, this dashboard includes dataset-derived label audits: Recommended-based labels, Rating-based labels, and high-confidence proxy labels derived from both.",
    labelAuditTableTitle: "Dataset Label Alignment Metrics",
    highProxyTitle: "High-confidence proxy",
    highProxyDesc: "Rating 1–4 with Recommended = no is negative; Rating 7–10 with Recommended = yes is positive. This is the strictest and primary validation source.",
    recProxyTitle: "Recommended proxy",
    recProxyDesc: "Recommended = yes/no is mapped to positive/negative to check consistency between VADER and recommendation behavior.",
    ratingProxyTitle: "Rating proxy",
    ratingProxyDesc: "OverallScore 7–10 is positive, 5–6 is neutral, and 1–4 is negative, checking consistency between VADER and numeric ratings.",
    confusionTitle: "Confusion Matrices",
    lexiconTitle: "Aviation-domain lexicon adjustment and cited CSV sources",
    lexiconDesc: "The VADER validation uses three aviation sentiment lexicon CSV files. Passenger-review-related terms are added into VADER lexicon and compared with the original VADER setting.",
    negativeLexiconDesc: "Aviation-domain negative terms, such as delay, cancel, stranded, and overbooked-related meanings.",
    positiveLexiconDesc: "Aviation-domain positive terms, such as friendly, comfortable, smooth, and upgrade-related meanings.",
    fullLexiconDesc: "The integrated aviation sentiment lexicon containing term, polarity, score, category, and domain columns.",
    appliedLexiconTitle: "Terms actually applied to VADER",
    fullLexiconTitle: "Full cited lexicon preview",
    lexiconConclusionTitle: "How to interpret the lexicon adjustment result",
    lexiconConclusionDesc: "Aviation lexicon adjustment is a reasonable validation step, but it did not significantly improve accuracy. Therefore, the final method keeps original VADER based on validation results, suggesting airline review sentiment is often driven by full sentence context rather than isolated domain words.",
    ldaTitle: "Major complaint themes in not recommended reviews",
    ldaDesc: "LDA focuses on Recommended = no reviews to identify passenger complaint themes.",
    ldaTopicsTableTitle: "Manually Revised LDA Topic Labels",
    manualLabelTitle: "Why manually revise topic labels?",
    manualLabelDesc: "LDA generates topic-word distributions but does not truly understand topic names. Therefore, this dashboard uses fixed output_2 results: topic_id, topic_size, top_words, and representative reviews are preserved, and clearer human-readable labels are added.",
    openLdaVis: "Open pyLDAvis Interactive Visualization",
    reviewsTitle: "Representative reviews for each LDA topic",
    reviewsDesc: "Representative reviews validate topic labels and provide qualitative evidence for the report.",
    topicFilterLabel: "Select Topic",
    allTopics: "All Topics",
    readFail: "Some data files failed to load. Please open this dashboard through an HTTP server."
  }
};

const pageTitles = {
  overview: "pageTitleOverview",
  keywords: "pageTitleKeywords",
  sentiment: "pageTitleSentiment",
  vaderValidation: "pageTitleVaderValidation",
  labelAudit: "pageTitleLabelAudit",
  lexicon: "pageTitleLexicon",
  lda: "pageTitleLda",
  reviews: "pageTitleReviews"
};

function t(key) { return i18n[state.lang][key] || key; }

function applyLanguage() {
  document.documentElement.lang = state.lang === "zh" ? "zh-Hant" : "en";
  document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => { el.placeholder = t(el.dataset.i18nPlaceholder); });
  document.getElementById("langToggle").textContent = state.lang === "zh" ? "EN" : "中文";
  const active = document.querySelector(".nav-btn.active")?.dataset.page || "overview";
  document.getElementById("pageTitle").textContent = t(pageTitles[active]);
  renderAll();
}

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3500);
}

function parseCSV(text) {
  const rows = [];
  let row = [], cell = "", inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const char = text[i], next = text[i + 1];
    if (char === '"' && inQuotes && next === '"') { cell += '"'; i++; }
    else if (char === '"') { inQuotes = !inQuotes; }
    else if (char === "," && !inQuotes) { row.push(cell); cell = ""; }
    else if ((char === "\n" || char === "\r") && !inQuotes) {
      if (char === "\r" && next === "\n") i++;
      row.push(cell);
      if (row.some(v => v.trim() !== "")) rows.push(row);
      row = []; cell = "";
    } else { cell += char; }
  }
  if (cell || row.length) {
    row.push(cell);
    if (row.some(v => v.trim() !== "")) rows.push(row);
  }
  if (!rows.length) return [];
  const headers = rows[0].map(h => h.trim().replace(/^\ufeff/, ""));
  return rows.slice(1).map(r => {
    const obj = {};
    headers.forEach((h, idx) => obj[h] = (r[idx] || "").trim());
    return obj;
  });
}

async function fetchCSV(paths) {
  for (const path of paths) {
    try {
      const res = await fetch(path);
      if (res.ok) return parseCSV(await res.text());
    } catch (e) {}
  }
  return [];
}

async function fetchJSON(paths) {
  for (const path of paths) {
    try {
      const res = await fetch(path);
      if (res.ok) return await res.json();
    } catch (e) {}
  }
  return null;
}

function escapeHtml(str) {
  return String(str ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function formatNumber(v, digits = 3) {
  const n = Number(v);
  if (Number.isFinite(n)) return n.toFixed(digits);
  return v ?? "";
}

function renderTable(elId, rows, columns, limit = null) {
  const table = document.getElementById(elId);
  if (!table) return;

  if (!rows || rows.length === 0) {
    table.innerHTML = `<tbody><tr><td>${state.lang === "zh" ? "尚未讀取到資料" : "No data loaded"}</td></tr></tbody>`;
    return;
  }

  const data = limit ? rows.slice(0, limit) : rows;
  const cols = columns || Object.keys(data[0]);
  const head = `<thead><tr>${cols.map(c => `<th>${escapeHtml(c)}</th>`).join("")}</tr></thead>`;
  const body = data.map(r => `<tr>${cols.map(c => `<td>${escapeHtml(r[c] ?? "")}</td>`).join("")}</tr>`).join("");
  table.innerHTML = `${head}<tbody>${body}</tbody>`;
}

function renderKeywords() {
  const search = (document.getElementById("keywordSearch")?.value || "").toLowerCase();
  const rows = state.data.tfidf.filter(r => !search || Object.values(r).join(" ").toLowerCase().includes(search));
  renderTable("tfidfTable", rows, ["rank", "yes_keyword", "yes_score", "no_keyword", "no_score"]);
}

function renderSentiment() {
  renderTable("sentimentTable", state.data.sentiment);
  const box = document.getElementById("sentimentMetrics");
  if (!box) return;
  if (!state.data.sentiment.length) { box.innerHTML = ""; return; }

  box.innerHTML = state.data.sentiment.map(r => {
    const rec = r.Recommended || r.recommended || "";
    const avg = r.avg_sentiment || r.average_sentiment || "";
    const count = r.review_count || "";
    const pos = r.positive_count || "";
    const neg = r.negative_count || "";
    return `
      <div class="metric">
        <span>Recommended = ${escapeHtml(rec)}</span>
        <strong>${escapeHtml(avg)}</strong>
        <span>${state.lang === "zh" ? "評論數" : "Reviews"}: ${escapeHtml(count)} | + ${escapeHtml(pos)} / - ${escapeHtml(neg)}</span>
      </div>`;
  }).join("");
}

function renderVaderValidation() {
  renderTable("vaderComparisonTable", state.data.vaderComparison, [
    "method", "threshold", "accuracy", "macro_f1", "neutral_rate", "n_proxy_reviews"
  ]);

  const box = document.getElementById("vaderBestMetrics");
  if (box) {
    const cfg = state.data.vaderBestConfig;
    if (cfg) {
      box.innerHTML = `
        <div class="metric"><span>Best score column</span><strong>${escapeHtml(cfg.score_column || "")}</strong></div>
        <div class="metric"><span>Threshold</span><strong>±${escapeHtml(cfg.threshold || "")}</strong></div>
        <div class="metric"><span>Accuracy</span><strong>${formatNumber(cfg.accuracy, 4)}</strong></div>
        <div class="metric"><span>Macro F1</span><strong>${formatNumber(cfg.macro_f1, 4)}</strong></div>
      `;
    } else {
      const best = [...state.data.vaderComparison].sort((a,b)=>Number(b.accuracy)-Number(a.accuracy))[0];
      box.innerHTML = best ? `
        <div class="metric"><span>Best method</span><strong>${escapeHtml(best.method || "")}</strong></div>
        <div class="metric"><span>Threshold</span><strong>±${escapeHtml(best.threshold || "")}</strong></div>
        <div class="metric"><span>Accuracy</span><strong>${formatNumber(best.accuracy, 4)}</strong></div>
        <div class="metric"><span>Macro F1</span><strong>${formatNumber(best.macro_f1, 4)}</strong></div>
      ` : "";
    }
  }

  renderTable("sentenceStatsTable", state.data.vaderSentenceStats);
}

function renderLabelAudit() {
  renderTable("labelAuditTable", state.data.labelAudit);
  renderTable("confusionHighTable", state.data.confusionHigh);
  renderTable("confusionRecTable", state.data.confusionRec);
  renderTable("confusionRatingTable", state.data.confusionRating);
}

function renderLexicon() {
  const box = document.getElementById("lexiconMetrics");
  if (box) {
    box.innerHTML = `
      <div class="metric"><span>Full lexicon terms</span><strong>${state.data.fullLexicon.length}</strong></div>
      <div class="metric"><span>Negative lexicon terms</span><strong>${state.data.negativeLexicon.length}</strong></div>
      <div class="metric"><span>Positive lexicon terms</span><strong>${state.data.positiveLexicon.length}</strong></div>
      <div class="metric"><span>Applied to VADER</span><strong>${state.data.appliedLexicon.length}</strong></div>
    `;
  }
  renderTable("appliedLexiconTable", state.data.appliedLexicon, null, 60);
  renderTable("fullLexiconTable", state.data.fullLexicon, null, 60);
}

function renderLdaTopics() {
  renderTable("ldaTopicsTable", state.data.ldaTopics, [
    "topic_id", "manual_topic_label", "topic_size", "top_words", "manual_interpretation"
  ]);
}

function renderReviews() {
  const filter = document.getElementById("topicFilter");
  const container = document.getElementById("reviewCards");
  if (!container) return;

  const topics = Array.from(new Set(state.data.reviews.map(r => r.topic_id))).filter(Boolean).sort((a,b)=>Number(a)-Number(b));
  if (filter && filter.options.length <= 1) {
    topics.forEach(topic => {
      const option = document.createElement("option");
      option.value = topic;
      option.textContent = `Topic ${Number(topic) + 1}`;
      filter.appendChild(option);
    });
  }

  const selected = filter?.value || "all";
  const rows = state.data.reviews.filter(r => selected === "all" || r.topic_id === selected);
  if (!rows.length) {
    container.innerHTML = `<div class="card">${state.lang === "zh" ? "尚未讀取到代表性評論。" : "No representative reviews loaded."}</div>`;
    return;
  }

  container.innerHTML = rows.map(r => `
    <article class="review-card">
      <h4>Topic ${Number(r.topic_id) + 1} · ${escapeHtml(r.manual_topic_label || r.topic_name_auto || "")}</h4>
      <div class="review-meta">
        <span class="badge">${state.lang === "zh" ? "機率" : "Probability"}: ${escapeHtml(r.topic_probability || "")}</span>
        <span class="badge">${escapeHtml(r.AirlineName || "")}</span>
        <span class="badge">${state.lang === "zh" ? "評分" : "Score"}: ${escapeHtml(r.OverallScore || "")}</span>
      </div>
      <p>${escapeHtml(r.representative_review || "")}</p>
    </article>
  `).join("");
}

function renderAll() {
  renderKeywords();
  renderSentiment();
  renderVaderValidation();
  renderLabelAudit();
  renderLexicon();
  renderLdaTopics();
  renderReviews();
}

function bindEvents() {
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(btn.dataset.page).classList.add("active");
      document.getElementById("pageTitle").textContent = t(pageTitles[btn.dataset.page]);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  document.getElementById("langToggle").addEventListener("click", () => {
    state.lang = state.lang === "zh" ? "en" : "zh";
    applyLanguage();
  });

  document.getElementById("keywordSearch")?.addEventListener("input", renderKeywords);
  document.getElementById("topicFilter")?.addEventListener("change", renderReviews);
}

async function loadData() {
  state.data.tfidf = await fetchCSV([
    "../output_2/tfidf_yes_no_keyword_comparison.csv",
    "../output/tfidf_yes_no_keyword_comparison.csv"
  ]);
  state.data.sentiment = await fetchCSV([
    "../output_vader_full/sentiment_summary_by_recommended_vader_validated.csv",
    "../output_vader_full/vader_final_summary_by_recommended.csv",
    "../output_2/sentiment_summary_by_recommended.csv",
    "../output/sentiment_summary_by_recommended.csv"
  ]);
  state.data.ldaTopics = await fetchCSV([
    "../output_2/lda_topics_fixed.csv",
    "../output/lda_topics.csv"
  ]);
  state.data.reviews = await fetchCSV([
    "../output_2/lda_representative_reviews_fixed.csv",
    "../output/lda_representative_reviews_extra.csv",
    "../output/lda_representative_reviews.csv"
  ]);

  state.data.vaderComparison = await fetchCSV([
    "../output_vader_full/vader_threshold_method_comparison_all_proxy.csv"
  ]);
  state.data.vaderBestConfig = await fetchJSON([
    "../output_vader_full/vader_best_config.json"
  ]);
  state.data.vaderSentenceStats = await fetchCSV([
    "../output_vader_full/vader_sentence_statistics.csv"
  ]);

  state.data.labelAudit = await fetchCSV([
    "../output_vader_label_audit/vader_dataset_label_alignment_metrics.csv"
  ]);
  state.data.confusionHigh = await fetchCSV([
    "../output_vader_label_audit/confusion_high_confidence_proxy.csv"
  ]);
  state.data.confusionRec = await fetchCSV([
    "../output_vader_label_audit/confusion_recommended_proxy.csv"
  ]);
  state.data.confusionRating = await fetchCSV([
    "../output_vader_label_audit/confusion_rating_proxy_three_class.csv"
  ]);

  state.data.appliedLexicon = await fetchCSV([
    "../output_vader_full/aviation_lexicon_applied_to_vader.csv",
    "../aviation_lexicon_applied_to_vader.csv"
  ]);
  state.data.fullLexicon = await fetchCSV([
    "../aviation_sentiment_lexicon_full.csv"
  ]);
  state.data.negativeLexicon = await fetchCSV([
    "../aviation_negative_lexicon.csv"
  ]);
  state.data.positiveLexicon = await fetchCSV([
    "../aviation_positive_lexicon.csv"
  ]);

  if (!Object.values(state.data).some(v => Array.isArray(v) ? v.length : v)) {
    showToast(t("readFail"));
  }
  renderAll();
}

bindEvents();
applyLanguage();
loadData();
