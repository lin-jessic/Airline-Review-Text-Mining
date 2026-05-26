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
    positiveLexicon: [],
    bertopicTopics: [],
    modelComparison: [],
    airlineKeywords: [],
    periodKeywords: []
  }
};

const i18n = {
  zh: {
    appTitle: "航空評論文字探勘",
    appSubtitle: "完整分析結果 Dashboard",
    navOverview: "專題設計",
    navKeywords: "TF / TF-IDF",
    navSentiment: "情緒分析結果",
    navVaderValidation: "VADER 驗證比較",
    navLabelAudit: "資料標籤佐證",
    navLexicon: "航空詞彙調整",
    navLda: "LDA 主題模型",
    navReviews: "代表性評論",
    navBertopic: "BERTopic 主題分析",
    navModelComparison: "模型比較與 RQ2",
    navRq3: "RQ3 跨時間與航空公司",
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
    pageTitleBertopic: "BERTopic 主題分析結果",
    pageTitleModelComparison: "模型比較與 RQ2 分析",
    pageTitleRq3: "RQ3 跨時間與航空公司",
    overviewEyebrow: "Balanced Sampling Design",
    overviewTitle: "以 Recommended 做分層抽樣，讓 LDA 與 BERTopic 公平比較",
    overviewDesc: "本專題將 Airline Reviews dataset 依照 Recommended 欄位縮減為平衡資料集：yes 10,000 筆、no 10,000 筆，共 20,000 筆。Member B 使用同一份 sampled_20k_with_tokens.csv 完成 TF/TF-IDF、VADER sentiment analysis 與 LDA baseline。",
    metricTotal: "總評論數", metricYes: "Recommended = yes", metricNo: "Recommended = no", metricSeed: "Random state",
    memberA: "Member A：資料與前處理", memberADesc: "負責資料清理、分層抽樣、tokens 欄位、token_count 與 EDA 圖表。",
    memberB: "Member B：傳統方法、VADER 與 LDA", memberBDesc: "負責 TF/TF-IDF、VADER 嚴謹驗證、航空詞彙調整比較、資料標籤佐證、LDA baseline 與代表性評論。",
    memberC: "Member C：BERTopic 與展示", memberCDesc: "負責 BERTopic、LDA vs BERTopic 比較、dashboard / presentation 整合。",
    methodFlow: "Member B 分析流程",
    flow1: "讀取 sampled_20k_with_tokens.csv", flow2: "使用 review_cleaned 做 TF / TF-IDF",
    flow3: "使用 Review 原文做 VADER，並驗證四種設定", flow4: "使用 tokens 做 LDA topic modeling",
    flow5: "整合圖表、CSV、代表性評論與人工解釋",
    bestFindingTitle: "本次 VADER 驗證的主要結論",
    bestFindingDesc: "經過完整 20,000 筆重新評分與 17,567 筆 high-confidence proxy validation 後，最佳設定為原生 VADER、整段 Review 輸入、預設門檻 ±0.05。",
    keywordsTitle: "推薦與不推薦評論的關鍵字差異", keywordsDesc: "TF-IDF 用於找出各群組較具代表性的詞。",
    tfidfTableTitle: "TF-IDF yes/no 比較表", searchPlaceholder: "搜尋 keyword...",
    yesInsightTitle: "推薦評論常見語意", yesInsight: "通常偏向服務、舒適度、友善、良好經驗，例如 good、crew、friendly、comfortable、excellent。",
    noInsightTitle: "不推薦評論常見語意", noInsight: "通常偏向延誤、等待、客服、行李、票務與額外費用，例如 delayed、bag、ticket、customer service、worst、pay。",
    sentimentTitle: "最終 VADER 情緒分析結果", sentimentDesc: "最終設定採用原生 VADER、整段 Review 輸入、預設門檻 ±0.05。",
    sentimentSummaryTitle: "Validated VADER Summary by Recommended",
    sentimentNote: "Recommended = yes 的平均情緒分數約為 0.747，Recommended = no 約為 -0.362，方向與推薦標籤與 OverallScore 一致。",
    vaderValidationTitle: "四種 VADER 設定與三種門檻比較", vaderValidationDesc: "此頁比較原生 VADER / 航空詞彙調整 VADER，以及整段 Review / 逐句平均兩種輸入形式，並測試 ±0.05、±0.10、±0.30 三種門檻。",
    vaderThresholdTableTitle: "Threshold and Method Comparison",
    whyFullReviewTitle: "為什麼最後選整段 Review？", whyFullReviewDesc: "雖然逐句平均可以避免長評論正負情緒互相抵銷，但實際驗證結果顯示，整段 Review 的 accuracy 明顯較高。",
    whyOriginalTitle: "為什麼保留原生 VADER？", whyOriginalDesc: "航空詞彙調整後的 accuracy 沒有明顯提升，代表許多航空評論的情緒來自整體語境。",
    sentenceStatsTitle: "長評論與逐句切分驗證",
    labelAuditTitle: "用資料集自帶分數與推薦標籤佐證 VADER 結果", labelAuditDesc: "除了 high-confidence proxy validation，本 dashboard 也加入資料集自帶標籤一致性檢查。",
    labelAuditTableTitle: "Dataset Label Alignment Metrics",
    highProxyTitle: "High-confidence proxy", highProxyDesc: "Rating 1–4 且 Recommended = no 標為 negative；Rating 7–10 且 Recommended = yes 標為 positive。",
    recProxyTitle: "Recommended proxy", recProxyDesc: "直接用 Recommended = yes/no 對應 positive/negative。",
    ratingProxyTitle: "Rating proxy", ratingProxyDesc: "OverallScore 7–10 為 positive、5–6 為 neutral、1–4 為 negative。",
    confusionTitle: "Confusion Matrices",
    lexiconTitle: "航空領域詞彙調整與引用資料", lexiconDesc: "本次 VADER 驗證引用三個航空情緒詞彙 CSV。",
    negativeLexiconDesc: "航空領域負向詞彙，例如 delay、cancel、stranded、overbooked 相關語意。",
    positiveLexiconDesc: "航空領域正向詞彙，例如 friendly、comfortable、smooth、upgrade 相關語意。",
    fullLexiconDesc: "整合版航空情緒詞彙表，包含 term、polarity、score、category、domain 等欄位。",
    appliedLexiconTitle: "實際套用到 VADER 的詞彙", fullLexiconTitle: "引用詞彙總表預覽",
    lexiconConclusionTitle: "詞彙調整結果怎麼解釋？", lexiconConclusionDesc: "航空詞彙調整是合理的驗證步驟，但結果顯示它沒有明顯提高 accuracy。因此本研究保留原生 VADER。",
    ldaTitle: "不推薦評論中的主要抱怨主題", ldaDesc: "LDA 主要針對 Recommended = no 評論，找出 passenger complaints 的主題結構。",
    ldaTopicsTableTitle: "LDA 修正版人工主題命名",
    manualLabelTitle: "為什麼要人工修正 Topic Label？", manualLabelDesc: "LDA 產生的是 topic-word distribution，不會自動理解主題名稱。",
    openLdaVis: "開啟 pyLDAvis 互動視覺化",
    reviewsTitle: "每個 LDA Topic 的代表性評論", reviewsDesc: "代表性評論用來驗證 topic label 是否合理。",
    topicFilterLabel: "選擇 Topic", allTopics: "全部 Topics",
    readFail: "部分資料讀取失敗，請確認是否使用 http server 開啟。",
    bertopicTitle: "BERTopic 主題分析結果",
    bertopicDesc: "BERTopic 使用 sentence-transformers 將評論轉為語意向量，自動找出語意相近的抱怨主題，不需要事先指定主題數量。",
    bertopicTopicsTableTitle: "BERTopic 主題分布表",
    bertopicNoiseTitle: "Topic -1 雜訊堆說明",
    bertopicNoiseDesc: "BERTopic 使用 HDBSCAN 分群，語意不夠集中的評論會被歸入 topic -1。本次共有 4,300 筆（43%）被歸入雜訊堆，這是 BERTopic 的正常現象。",
    bertopicAdvTitle: "BERTopic 的優勢",
    bertopicAdvDesc: "BERTopic 自動找出 40 個語意群組，比 LDA 的 7 個主題更細緻，能區分出延誤問題的子類型與行李問題的細分。",
    modelCompTitle: "模型比較與 RQ2 分析",
    modelCompDesc: "比較 LDA 與 BERTopic 的主題結果，並分析不同評分群組與矛盾旅客的抱怨差異。",
    modelCompTableTitle: "LDA vs BERTopic 主題對應表",
    ldaAdvTitle: "LDA 的優點", ldaAdvDesc: "7 個主題清楚易懂，每個主題筆數多，統計穩定，適合管理者快速掌握主要抱怨類型。",
    bertopicCompAdvTitle: "BERTopic 的優點", bertopicCompAdvDesc: "40 個主題更細緻，能區分 LDA 合併在一起的子主題，基於語意而非詞頻。",
    ratingGroupTitle: "不同評分群組的主題差異", ratingGroupDesc: "將資料依 OverallScore 切分為低（1-4）、中（5-7）、高（8-10）三組，比較各組的主要抱怨主題。",
    contradictoryTitle: "矛盾旅客分析",
    contradictoryDesc: "分析評分 5-10 分但不推薦的旅客，找出他們與一般不滿意旅客（1-4 分不推薦）的關鍵字差異。",
    contradictoryFindingTitle: "矛盾旅客的特徵",
    contradictoryFindingDesc: "矛盾旅客的關鍵字以飛行體驗為主（food、cabin、crew、good），正面詞彙出現頻率高，代表他們整體體驗還可以，但特定缺點讓他們無法推薦。",
    normalNoFindingTitle: "一般不滿意旅客的特徵",
    normalNoFindingDesc: "一般不滿意旅客的關鍵字以問題導向為主（hour、customer、never、told、delayed），反映強烈的系統性不滿。",
    rq3Title: "跨航空公司與時間的抱怨模式比較",
    rq3Desc: "分析不同航空公司和時間段的抱怨關鍵字，找出 industry-wide 問題和 airline-specific 問題。",
    airlineCompTitle: "前10大航空公司抱怨關鍵字比較",
    airlineCompDesc: "flight、hour、time、seat、bag、service 等詞在所有航空公司都出現（industry-wide），而 istanbul、denver、abu dhabi 等地名只在特定航空公司出現（airline-specific）。",
    industryWideTitle: "Industry-wide 問題", industryWideDesc: "延誤、行李、座位、客服是所有主要航空公司共同面對的抱怨，代表這些是航空業系統性的服務問題。",
    airlineSpecificTitle: "Airline-specific 問題", airlineSpecificDesc: "地名和樞紐城市高度集中在特定航空公司，反映旅客對特定航線的不滿，而非根本性的服務品質差異。",
    temporalTitle: "疫情前中後抱怨主題變化",
    temporalDesc: "比較 2013-2019（疫情前）、2020-2021（疫情期間）、2022-2023（疫情後）三個時期的抱怨關鍵字差異。",
    preCOVIDTitle: "疫情前（2013-2019）", preCOVIDDesc: "抱怨集中在飛行體驗：seat、food、plane、staff，旅客在意機上服務品質。",
    duringCOVIDTitle: "疫情期間（2020-2021）", duringCOVIDDesc: "refund 突然躍升，cancelled 出現，反映大量航班取消和退款困難。customer service 首次進入前15名。",
    postCOVIDTitle: "疫情後（2022-2023）", postCOVIDDesc: "bag 問題突然增加（可能因地勤人力短缺），customer service 和 ticket 問題持續，never 情緒更強烈。"
  },
  en: {
    appTitle: "Airline Review Text Mining",
    appSubtitle: "Full Analysis Dashboard",
    navOverview: "Project Design", navKeywords: "TF / TF-IDF", navSentiment: "Sentiment Results",
    navVaderValidation: "VADER Validation", navLabelAudit: "Dataset Label Audit", navLexicon: "Aviation Lexicon",
    navLda: "LDA Topic Model", navReviews: "Representative Reviews",
    navBertopic: "BERTopic Analysis", navModelComparison: "Model Comparison & RQ2", navRq3: "RQ3 Temporal & Airline",
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
    pageTitleBertopic: "BERTopic Topic Analysis",
    pageTitleModelComparison: "Model Comparison and RQ2 Analysis",
    pageTitleRq3: "RQ3 Temporal and Airline Comparison",
    overviewEyebrow: "Balanced Sampling Design",
    overviewTitle: "Stratified sampling by Recommended enables a fair LDA vs BERTopic comparison",
    overviewDesc: "The project reduces the Airline Reviews dataset into a balanced 20,000-review dataset: 10,000 recommended and 10,000 not recommended reviews. Member B uses the same sampled_20k_with_tokens.csv for TF/TF-IDF, VADER sentiment analysis, and LDA baseline.",
    metricTotal: "Total Reviews", metricYes: "Recommended = yes", metricNo: "Recommended = no", metricSeed: "Random state",
    memberA: "Member A: Data and Preprocessing", memberADesc: "Responsible for cleaning, stratified sampling, tokens, token_count, and EDA figures.",
    memberB: "Member B: Traditional Methods, VADER, and LDA", memberBDesc: "Responsible for TF/TF-IDF, rigorous VADER validation, aviation lexicon comparison, dataset label audit, LDA baseline, and representative reviews.",
    memberC: "Member C: BERTopic and Presentation", memberCDesc: "Responsible for BERTopic, LDA vs BERTopic comparison, dashboard / presentation integration.",
    methodFlow: "Member B Analysis Workflow",
    flow1: "Load sampled_20k_with_tokens.csv", flow2: "Use review_cleaned for TF / TF-IDF",
    flow3: "Use original Review text for VADER and validate four settings", flow4: "Use tokens for LDA topic modeling",
    flow5: "Integrate figures, CSV tables, representative reviews, and interpretation",
    bestFindingTitle: "Main finding from VADER validation",
    bestFindingDesc: "After rescoring all 20,000 reviews and validating on 17,567 high-confidence proxy reviews, the best setting is original VADER, full-review input, and the default ±0.05 threshold.",
    keywordsTitle: "Keyword differences between recommended and not recommended reviews", keywordsDesc: "TF-IDF identifies representative terms for each group.",
    tfidfTableTitle: "TF-IDF yes/no Comparison Table", searchPlaceholder: "Search keyword...",
    yesInsightTitle: "Common meaning in recommended reviews", yesInsight: "Tend to emphasize service, comfort, friendliness, and positive experiences.",
    noInsightTitle: "Common meaning in not recommended reviews", noInsight: "Tend to emphasize delays, waiting, customer service, baggage, ticketing, and extra payment issues.",
    sentimentTitle: "Final VADER sentiment results", sentimentDesc: "The final setting uses original VADER, full-review input, and the default ±0.05 threshold.",
    sentimentSummaryTitle: "Validated VADER Summary by Recommended",
    sentimentNote: "Recommended = yes has an average sentiment score around 0.747, Recommended = no around -0.362, consistent with recommendation labels and OverallScore.",
    vaderValidationTitle: "Four VADER settings and three thresholds", vaderValidationDesc: "Compares original / aviation-adjusted VADER, full-review / sentence-average input, and ±0.05, ±0.10, ±0.30 thresholds.",
    vaderThresholdTableTitle: "Threshold and Method Comparison",
    whyFullReviewTitle: "Why choose full-review input?", whyFullReviewDesc: "Although sentence averaging may reduce sentiment cancellation, full-review input achieves higher accuracy in this dataset.",
    whyOriginalTitle: "Why retain original VADER?", whyOriginalDesc: "Aviation lexicon adjustment did not significantly improve accuracy, suggesting sentiment is driven by broader context.",
    sentenceStatsTitle: "Long-review and sentence-splitting validation",
    labelAuditTitle: "Using dataset ratings and recommendation labels to support VADER", labelAuditDesc: "Dataset-derived label audits: Recommended-based, Rating-based, and high-confidence proxy labels.",
    labelAuditTableTitle: "Dataset Label Alignment Metrics",
    highProxyTitle: "High-confidence proxy", highProxyDesc: "Rating 1–4 with Recommended = no is negative; Rating 7–10 with Recommended = yes is positive.",
    recProxyTitle: "Recommended proxy", recProxyDesc: "Recommended = yes/no mapped to positive/negative.",
    ratingProxyTitle: "Rating proxy", ratingProxyDesc: "OverallScore 7–10 is positive, 5–6 is neutral, 1–4 is negative.",
    confusionTitle: "Confusion Matrices",
    lexiconTitle: "Aviation-domain lexicon adjustment and cited CSV sources", lexiconDesc: "Three aviation sentiment lexicon CSV files used in VADER validation.",
    negativeLexiconDesc: "Aviation-domain negative terms related to delay, cancel, stranded, and overbooked.",
    positiveLexiconDesc: "Aviation-domain positive terms related to friendly, comfortable, smooth, and upgrade.",
    fullLexiconDesc: "Integrated aviation sentiment lexicon with term, polarity, score, category, and domain columns.",
    appliedLexiconTitle: "Terms actually applied to VADER", fullLexiconTitle: "Full cited lexicon preview",
    lexiconConclusionTitle: "How to interpret the lexicon adjustment result", lexiconConclusionDesc: "Aviation lexicon adjustment is a reasonable validation step, but it did not significantly improve accuracy. Original VADER is retained.",
    ldaTitle: "Major complaint themes in not recommended reviews", ldaDesc: "LDA focuses on Recommended = no reviews to identify passenger complaint themes.",
    ldaTopicsTableTitle: "Manually Revised LDA Topic Labels",
    manualLabelTitle: "Why manually revise topic labels?", manualLabelDesc: "LDA generates topic-word distributions but does not truly understand topic names.",
    openLdaVis: "Open pyLDAvis Interactive Visualization",
    reviewsTitle: "Representative reviews for each LDA topic", reviewsDesc: "Representative reviews validate topic labels and provide qualitative evidence.",
    topicFilterLabel: "Select Topic", allTopics: "All Topics",
    readFail: "Some data files failed to load. Please open this dashboard through an HTTP server.",
    bertopicTitle: "BERTopic Topic Analysis Results",
    bertopicDesc: "BERTopic uses sentence-transformers to convert reviews into semantic vectors and automatically identifies complaint topics without requiring a predefined number.",
    bertopicTopicsTableTitle: "BERTopic Topic Distribution Table",
    bertopicNoiseTitle: "Topic -1 Noise Cluster",
    bertopicNoiseDesc: "BERTopic uses HDBSCAN clustering. Reviews with insufficient semantic coherence are assigned to topic -1. A total of 4,300 reviews (43%) were assigned to the noise cluster.",
    bertopicAdvTitle: "BERTopic Advantages",
    bertopicAdvDesc: "BERTopic automatically identified 40 semantic groups, more granular than LDA's 7 topics, distinguishing delay sub-types and baggage sub-types.",
    modelCompTitle: "Model Comparison and RQ2 Analysis",
    modelCompDesc: "Compare LDA and BERTopic topic results and analyze complaint differences across rating groups and contradictory passengers.",
    modelCompTableTitle: "LDA vs BERTopic Topic Mapping",
    ldaAdvTitle: "LDA Advantages", ldaAdvDesc: "7 clear and interpretable topics with large topic sizes, suitable for managerial communication.",
    bertopicCompAdvTitle: "BERTopic Advantages", bertopicCompAdvDesc: "40 more granular topics that distinguish sub-categories merged by LDA. Semantic-based rather than frequency-based.",
    ratingGroupTitle: "Complaint Topic Differences by Rating Group", ratingGroupDesc: "Data divided into low (1-4), mid (5-7), and high (8-10) rating groups to compare major complaint topics.",
    contradictoryTitle: "Contradictory Passenger Analysis",
    contradictoryDesc: "Analysis of passengers who rated 5-10 but did not recommend, comparing keyword patterns with typical dissatisfied passengers (1-4, not recommended).",
    contradictoryFindingTitle: "Contradictory Passenger Characteristics",
    contradictoryFindingDesc: "Contradictory passengers show experience-focused keywords (food, cabin, crew, good), suggesting acceptable overall experience but specific issues prevented recommendation.",
    normalNoFindingTitle: "Typical Dissatisfied Passenger Characteristics",
    normalNoFindingDesc: "Typical dissatisfied passengers show problem-oriented keywords (hour, customer, never, told, delayed), reflecting strong systemic dissatisfaction.",
    rq3Title: "Complaint Pattern Comparison Across Airlines and Time",
    rq3Desc: "Analyze complaint keywords across airlines and time periods to identify industry-wide and airline-specific issues.",
    airlineCompTitle: "Top 10 Airline Complaint Keyword Comparison",
    airlineCompDesc: "Keywords like flight, hour, time, seat, bag, and service appear across all airlines (industry-wide), while place names like istanbul, denver, and abu dhabi only appear in specific airlines (airline-specific).",
    industryWideTitle: "Industry-wide Issues", industryWideDesc: "Delays, baggage, seating, and customer service are universal complaints, representing systemic airline industry problems.",
    airlineSpecificTitle: "Airline-specific Issues", airlineSpecificDesc: "Hub city names are concentrated in specific airlines, reflecting route-specific dissatisfaction rather than fundamentally different service quality.",
    temporalTitle: "Complaint Topic Changes: Pre-, During, and Post-COVID",
    temporalDesc: "Compare complaint keywords across three periods: 2013-2019 (pre-COVID), 2020-2021 (during COVID), and 2022-2023 (post-COVID).",
    preCOVIDTitle: "Pre-COVID (2013-2019)", preCOVIDDesc: "Complaints focused on in-flight experience: seat, food, plane, staff.",
    duringCOVIDTitle: "During COVID (2020-2021)", duringCOVIDDesc: "Refund surged to third place, cancelled appeared, reflecting massive flight cancellations and refund difficulties.",
    postCOVIDTitle: "Post-COVID (2022-2023)", postCOVIDDesc: "Bag issues suddenly increased, customer service and ticket problems persisted with stronger negative sentiment."
  }
};

const pageTitles = {
  overview: "pageTitleOverview", keywords: "pageTitleKeywords", sentiment: "pageTitleSentiment",
  vaderValidation: "pageTitleVaderValidation", labelAudit: "pageTitleLabelAudit", lexicon: "pageTitleLexicon",
  lda: "pageTitleLda", reviews: "pageTitleReviews",
  bertopic: "pageTitleBertopic", modelComparison: "pageTitleModelComparison", rq3: "pageTitleRq3"
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
  if (cell || row.length) { row.push(cell); if (row.some(v => v.trim() !== "")) rows.push(row); }
  if (!rows.length) return [];
  const headers = rows[0].map(h => h.trim().replace(/^\ufeff/, ""));
  return rows.slice(1).map(r => { const obj = {}; headers.forEach((h, idx) => obj[h] = (r[idx] || "").trim()); return obj; });
}

async function fetchCSV(paths) {
  for (const path of paths) {
    try { const res = await fetch(path); if (res.ok) return parseCSV(await res.text()); } catch (e) {}
  }
  return [];
}

async function fetchJSON(paths) {
  for (const path of paths) {
    try { const res = await fetch(path); if (res.ok) return await res.json(); } catch (e) {}
  }
  return null;
}

function escapeHtml(str) {
  return String(str ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

function formatNumber(v, digits = 3) {
  const n = Number(v);
  return Number.isFinite(n) ? n.toFixed(digits) : (v ?? "");
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
    return `<div class="metric"><span>Recommended = ${escapeHtml(rec)}</span><strong>${escapeHtml(avg)}</strong><span>${state.lang === "zh" ? "評論數" : "Reviews"}: ${escapeHtml(count)} | + ${escapeHtml(pos)} / - ${escapeHtml(neg)}</span></div>`;
  }).join("");
}

function renderVaderValidation() {
  renderTable("vaderComparisonTable", state.data.vaderComparison, ["method", "threshold", "accuracy", "macro_f1", "neutral_rate", "n_proxy_reviews"]);
  const box = document.getElementById("vaderBestMetrics");
  if (box) {
    const cfg = state.data.vaderBestConfig;
    if (cfg) {
      box.innerHTML = `
        <div class="metric"><span>Best score column</span><strong>${escapeHtml(cfg.score_column || "")}</strong></div>
        <div class="metric"><span>Threshold</span><strong>±${escapeHtml(String(cfg.threshold || ""))}</strong></div>
        <div class="metric"><span>Accuracy</span><strong>${formatNumber(cfg.accuracy, 4)}</strong></div>
        <div class="metric"><span>Macro F1</span><strong>${formatNumber(cfg.macro_f1, 4)}</strong></div>`;
    } else {
      const best = [...state.data.vaderComparison].sort((a,b)=>Number(b.accuracy)-Number(a.accuracy))[0];
      box.innerHTML = best ? `
        <div class="metric"><span>Best method</span><strong>${escapeHtml(best.method || "")}</strong></div>
        <div class="metric"><span>Threshold</span><strong>±${escapeHtml(best.threshold || "")}</strong></div>
        <div class="metric"><span>Accuracy</span><strong>${formatNumber(best.accuracy, 4)}</strong></div>
        <div class="metric"><span>Macro F1</span><strong>${formatNumber(best.macro_f1, 4)}</strong></div>` : "";
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
      <div class="metric"><span>Applied to VADER</span><strong>${state.data.appliedLexicon.length}</strong></div>`;
  }
  renderTable("appliedLexiconTable", state.data.appliedLexicon, null, 60);
  renderTable("fullLexiconTable", state.data.fullLexicon, null, 60);
}

function renderLdaTopics() {
  renderTable("ldaTopicsTable", state.data.ldaTopics, ["topic_id", "manual_topic_label", "topic_size", "top_words", "manual_interpretation"]);
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
  if (!rows.length) { container.innerHTML = `<div class="card">${state.lang === "zh" ? "尚未讀取到代表性評論。" : "No representative reviews loaded."}</div>`; return; }
  container.innerHTML = rows.map(r => `
    <article class="review-card">
      <h4>Topic ${Number(r.topic_id) + 1} · ${escapeHtml(r.manual_topic_label || r.topic_name_auto || "")}</h4>
      <div class="review-meta">
        <span class="badge">${state.lang === "zh" ? "機率" : "Probability"}: ${escapeHtml(r.topic_probability || "")}</span>
        <span class="badge">${escapeHtml(r.AirlineName || "")}</span>
        <span class="badge">${state.lang === "zh" ? "評分" : "Score"}: ${escapeHtml(r.OverallScore || "")}</span>
      </div>
      <p>${escapeHtml(r.representative_review || "")}</p>
    </article>`).join("");
}

function renderBertopic() {
  const box = document.getElementById("bertopicMetrics");
  if (box) {
    const topics = state.data.bertopicTopics.filter(r => String(r.Topic) !== "-1");
    const noise = state.data.bertopicTopics.find(r => String(r.Topic) === "-1");
    const totalAssigned = topics.reduce((s, r) => s + Number(r.Count || 0), 0);
    box.innerHTML = `
      <div class="metric"><span>Total Topics</span><strong>${topics.length}</strong></div>
      <div class="metric"><span>Assigned Reviews</span><strong>${totalAssigned.toLocaleString()}</strong></div>
      <div class="metric"><span>Noise (Topic -1)</span><strong>${noise ? Number(noise.Count).toLocaleString() : 0}</strong></div>
      <div class="metric"><span>Data Source</span><strong>10,000 no</strong></div>`;
  }
  renderTable("bertopicTopicsTable", state.data.bertopicTopics.filter(r => String(r.Topic) !== "-1"), ["Topic", "Count", "Name"]);
}

function renderModelComparison() {
  renderTable("modelCompTable", state.data.modelComparison, ["LDA Topic", "LDA Size", "BERTopic Equivalent Topics", "BERTopic Advantage"]);
}

function renderAll() {
  renderKeywords();
  renderSentiment();
  renderVaderValidation();
  renderLabelAudit();
  renderLexicon();
  renderLdaTopics();
  renderReviews();
  renderBertopic();
  renderModelComparison();
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
  state.data.tfidf = await fetchCSV(["../output_2/tfidf_yes_no_keyword_comparison.csv", "../output/tfidf_yes_no_keyword_comparison.csv"]);
  state.data.sentiment = await fetchCSV(["../output_vader_full/sentiment_summary_by_recommended_vader_validated.csv", "../output_2/sentiment_summary_by_recommended.csv", "../output/sentiment_summary_by_recommended.csv"]);
  state.data.ldaTopics = await fetchCSV(["../output_2/lda_topics_fixed.csv", "../output/lda_topics.csv"]);
  state.data.reviews = await fetchCSV(["../output_2/lda_representative_reviews_fixed.csv", "../output/lda_representative_reviews.csv"]);
  state.data.vaderComparison = await fetchCSV(["../output_vader_full/vader_threshold_method_comparison_all_proxy.csv"]);
  state.data.vaderBestConfig = await fetchJSON(["../output_vader_full/vader_best_config.json"]);
  state.data.vaderSentenceStats = await fetchCSV(["../output_vader_full/vader_sentence_statistics.csv"]);
  state.data.labelAudit = await fetchCSV(["../output_vader_label_audit/vader_dataset_label_alignment_metrics.csv"]);
  state.data.confusionHigh = await fetchCSV(["../output_vader_label_audit/confusion_high_confidence_proxy.csv"]);
  state.data.confusionRec = await fetchCSV(["../output_vader_label_audit/confusion_recommended_proxy.csv"]);
  state.data.confusionRating = await fetchCSV(["../output_vader_label_audit/confusion_rating_proxy_three_class.csv"]);
  state.data.appliedLexicon = await fetchCSV(["../output_vader_full/aviation_lexicon_applied_to_vader.csv"]);
  state.data.fullLexicon = await fetchCSV(["../aviation_sentiment_lexicon_full.csv"]);
  state.data.negativeLexicon = await fetchCSV(["../aviation_negative_lexicon.csv"]);
  state.data.positiveLexicon = await fetchCSV(["../aviation_positive_lexicon.csv"]);
  state.data.bertopicTopics = await fetchCSV(["../output_c/bertopic_final_results.csv"]);
  state.data.modelComparison = await fetchCSV(["../output_c/lda_vs_bertopic_comparison.csv"]);
  state.data.airlineKeywords = await fetchCSV(["../output_c/rq3_airline_keywords.csv"]);
  state.data.periodKeywords = await fetchCSV(["../output_c/rq3_period_keywords_full.csv"]);
  if (!Object.values(state.data).some(v => Array.isArray(v) ? v.length : v)) showToast(t("readFail"));
  renderAll();
}

bindEvents();
applyLanguage();
loadData();
