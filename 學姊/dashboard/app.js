const state = {
  lang: "zh",
  data: {
    tfidf: [],
    sentiment: [],
    ldaTopics: [],
    reviews: []
  }
};

const i18n = {
  zh: {
    appTitle: "航空評論文字探勘",
    appSubtitle: "Member B Dashboard",
    navOverview: "專題設計",
    navKeywords: "TF / TF-IDF 關鍵字",
    navSentiment: "情緒分析",
    navLda: "LDA 主題模型",
    navReviews: "代表性評論",
    navHandoff: "交接與檔案說明",
    langHint: "點擊切換英文介面",
    eyebrow: "Airline Reviews Text Mining Final Project",
    pageTitleOverview: "專題設計與資料策略",
    pageTitleKeywords: "TF / TF-IDF 關鍵字分析",
    pageTitleSentiment: "VADER 情緒分析",
    pageTitleLda: "LDA 主題模型分析",
    pageTitleReviews: "LDA 代表性評論",
    pageTitleHandoff: "交接與檔案說明",
    statusText: "讀取 output / output_2 結果",
    overviewEyebrow: "Balanced Sampling Design",
    overviewTitle: "以 Recommended 做分層抽樣，讓 LDA 與 BERTopic 公平比較",
    overviewDesc: "本專題先將 Airline Reviews dataset 依照 Recommended 欄位縮減為平衡資料集：yes 10,000 筆、no 10,000 筆，共 20,000 筆。Member B 使用同一份 sampled_20k_with_tokens.csv 完成 TF/TF-IDF、VADER sentiment analysis 與 LDA baseline。",
    metricTotal: "總評論數",
    metricYes: "Recommended = yes",
    metricNo: "Recommended = no",
    metricSeed: "Random state",
    memberA: "Member A：資料與前處理",
    memberADesc: "負責資料清理、分層抽樣、tokens 欄位、token_count 與 EDA 圖表。",
    memberB: "Member B：傳統方法與 LDA",
    memberBDesc: "負責 TF/TF-IDF、VADER 情緒分析、LDA baseline、coherence score、manual topic interpretation。",
    memberC: "Member C：BERTopic 與展示",
    memberCDesc: "負責 BERTopic、LDA vs BERTopic 比較、dashboard / presentation 整合。",
    methodFlow: "Member B 分析流程",
    flow1: "讀取 sampled_20k_with_tokens.csv",
    flow2: "使用 review_cleaned 做 TF / TF-IDF",
    flow3: "使用 Review 原文做 VADER sentiment",
    flow4: "使用 tokens 做 LDA topic modeling",
    flow5: "輸出圖表、CSV、代表性評論與人工解釋表",
    keywordsTitle: "推薦與不推薦評論的關鍵字差異",
    keywordsDesc: "TF-IDF 用於找出各群組較具代表性的詞，協助比較 Recommended = yes 與 Recommended = no 的語意差異。",
    tfidfTableTitle: "TF-IDF yes/no 比較表",
    searchPlaceholder: "搜尋 keyword...",
    yesInsightTitle: "推薦評論常見語意",
    yesInsight: "通常偏向服務、舒適度、友善、良好經驗，例如 good、crew、friendly、comfortable、excellent。",
    noInsightTitle: "不推薦評論常見語意",
    noInsight: "通常偏向延誤、等待、客服、行李、票務與額外費用，例如 delayed、bag、ticket、customer service、worst、pay。",
    sentimentTitle: "推薦標籤與情緒分數的一致性",
    sentimentDesc: "VADER 使用 Review 原始文字計算 compound score，範圍為 -1 到 +1。",
    sentimentSummaryTitle: "Sentiment Summary",
    sentimentNote: "結果通常可用來說明：Recommended = yes 的情緒分數明顯高於 Recommended = no，且與 OverallScore 方向一致。",
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
    handoffTitle: "交接檔案與下一位使用方式",
    handoffDesc: "這一頁整理 Member B 產出的重點檔案，以及下一位做 dashboard / BERTopic 比較時可以怎麼使用。",
    fileTfidf: "推薦 / 不推薦關鍵字比較",
    fileSentiment: "情緒分析摘要",
    fileLdaTopics: "原始 LDA topic 結果",
    fileRep: "原始代表性評論",
    fileVis: "pyLDAvis 互動視覺化",
    fileFixedTopics: "人工修正後 topic label",
    fileManual: "人工解釋表，報告優先使用",
    fileFixedRep: "加上修正版 topic label 的代表性評論",
    fileFixSummary: "說明人工命名沒有改模型結果",
    runTitle: "Dashboard 執行方式",
    runDesc: "然後在瀏覽器開啟：http://localhost:8000/dashboard/index.html",
    readFail: "部分資料讀取失敗，請確認是否使用 http server 開啟。"
  },
  en: {
    appTitle: "Airline Review Text Mining",
    appSubtitle: "Member B Dashboard",
    navOverview: "Project Design",
    navKeywords: "TF / TF-IDF Keywords",
    navSentiment: "Sentiment Analysis",
    navLda: "LDA Topic Model",
    navReviews: "Representative Reviews",
    navHandoff: "Handoff & Files",
    langHint: "Click to switch Chinese UI",
    eyebrow: "Airline Reviews Text Mining Final Project",
    pageTitleOverview: "Project Design and Data Strategy",
    pageTitleKeywords: "TF / TF-IDF Keyword Analysis",
    pageTitleSentiment: "VADER Sentiment Analysis",
    pageTitleLda: "LDA Topic Modeling Results",
    pageTitleReviews: "LDA Representative Reviews",
    pageTitleHandoff: "Handoff and File Guide",
    statusText: "Loading output / output_2 results",
    overviewEyebrow: "Balanced Sampling Design",
    overviewTitle: "Stratified sampling by Recommended enables a fair LDA vs BERTopic comparison",
    overviewDesc: "The project reduces the Airline Reviews dataset into a balanced 20,000-review dataset based on the Recommended field: 10,000 recommended reviews and 10,000 not recommended reviews. Member B uses the same sampled_20k_with_tokens.csv file for TF/TF-IDF, VADER sentiment analysis, and the LDA baseline.",
    metricTotal: "Total Reviews",
    metricYes: "Recommended = yes",
    metricNo: "Recommended = no",
    metricSeed: "Random state",
    memberA: "Member A: Data and Preprocessing",
    memberADesc: "Responsible for cleaning, stratified sampling, tokens, token_count, and EDA figures.",
    memberB: "Member B: Traditional Methods and LDA",
    memberBDesc: "Responsible for TF/TF-IDF, VADER sentiment analysis, LDA baseline, coherence score, and manual topic interpretation.",
    memberC: "Member C: BERTopic and Presentation",
    memberCDesc: "Responsible for BERTopic, LDA vs BERTopic comparison, dashboard / presentation integration.",
    methodFlow: "Member B Analysis Workflow",
    flow1: "Load sampled_20k_with_tokens.csv",
    flow2: "Use review_cleaned for TF / TF-IDF",
    flow3: "Use original Review text for VADER sentiment",
    flow4: "Use tokens for LDA topic modeling",
    flow5: "Export charts, CSV files, representative reviews, and manual interpretation tables",
    keywordsTitle: "Keyword differences between recommended and not recommended reviews",
    keywordsDesc: "TF-IDF identifies representative terms for each group and helps compare the semantic differences between Recommended = yes and Recommended = no reviews.",
    tfidfTableTitle: "TF-IDF yes/no Comparison Table",
    searchPlaceholder: "Search keyword...",
    yesInsightTitle: "Common meaning in recommended reviews",
    yesInsight: "Recommended reviews tend to emphasize service, comfort, friendliness, and positive experiences, such as good, crew, friendly, comfortable, and excellent.",
    noInsightTitle: "Common meaning in not recommended reviews",
    noInsight: "Not recommended reviews tend to emphasize delays, waiting, customer service, baggage, ticketing, and extra payment issues, such as delayed, bag, ticket, customer service, worst, and pay.",
    sentimentTitle: "Consistency between recommendation labels and sentiment scores",
    sentimentDesc: "VADER calculates compound scores from the original Review text. The score ranges from -1 to +1.",
    sentimentSummaryTitle: "Sentiment Summary",
    sentimentNote: "The results can support the finding that Recommended = yes reviews have much higher sentiment scores than Recommended = no reviews, consistent with OverallScore.",
    ldaTitle: "Major complaint themes in not recommended reviews",
    ldaDesc: "LDA focuses mainly on Recommended = no reviews to identify the topic structure of passenger complaints.",
    ldaTopicsTableTitle: "Manually Revised LDA Topic Labels",
    manualLabelTitle: "Why manually revise topic labels?",
    manualLabelDesc: "LDA generates topic-word distributions but does not truly understand topic names. Therefore, this dashboard uses the fixed output_2 version: topic_id, topic_size, top_words, and representative reviews are preserved. Only clearer human-readable topic labels are added based on top words and representative reviews.",
    openLdaVis: "Open pyLDAvis Interactive Visualization",
    reviewsTitle: "Representative reviews for each LDA topic",
    reviewsDesc: "Representative reviews are used to validate whether the topic labels are reasonable and to provide qualitative evidence for the report.",
    topicFilterLabel: "Select Topic",
    allTopics: "All Topics",
    handoffTitle: "Handoff files and usage guide",
    handoffDesc: "This page explains the key files produced by Member B and how the next member can use them for dashboard integration or LDA vs BERTopic comparison.",
    fileTfidf: "Keyword comparison between recommended and not recommended reviews",
    fileSentiment: "Sentiment analysis summary",
    fileLdaTopics: "Original LDA topic results",
    fileRep: "Original representative reviews",
    fileVis: "pyLDAvis interactive visualization",
    fileFixedTopics: "Manually revised topic labels",
    fileManual: "Manual interpretation table; recommended for report writing",
    fileFixedRep: "Representative reviews with fixed topic labels",
    fileFixSummary: "Explains that manual labeling does not change the model output",
    runTitle: "How to run this dashboard",
    runDesc: "Then open this URL in your browser: http://localhost:8000/dashboard/index.html",
    readFail: "Some data files failed to load. Please make sure you open the dashboard through an HTTP server."
  }
};

const pageTitles = {
  overview: "pageTitleOverview",
  keywords: "pageTitleKeywords",
  sentiment: "pageTitleSentiment",
  lda: "pageTitleLda",
  reviews: "pageTitleReviews",
  handoff: "pageTitleHandoff"
};

function t(key) {
  return i18n[state.lang][key] || key;
}

function applyLanguage() {
  document.documentElement.lang = state.lang === "zh" ? "zh-Hant" : "en";
  document.querySelectorAll("[data-i18n]").forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });
  document.getElementById("langToggle").textContent = state.lang === "zh" ? "EN" : "中文";
  const active = document.querySelector(".nav-btn.active")?.dataset.page || "overview";
  document.getElementById("pageTitle").textContent = t(pageTitles[active]);
  renderAll();
}

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3200);
}

function parseCSV(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    const next = text[i + 1];

    if (char === '"' && inQuotes && next === '"') {
      cell += '"';
      i++;
    } else if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === "," && !inQuotes) {
      row.push(cell);
      cell = "";
    } else if ((char === "\n" || char === "\r") && !inQuotes) {
      if (char === "\r" && next === "\n") i++;
      row.push(cell);
      if (row.some(v => v.trim() !== "")) rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }

  if (cell || row.length) {
    row.push(cell);
    if (row.some(v => v.trim() !== "")) rows.push(row);
  }

  if (!rows.length) return [];
  const headers = rows[0].map(h => h.trim());
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
      if (res.ok) {
        const text = await res.text();
        return parseCSV(text);
      }
    } catch (err) {
      // try next path
    }
  }
  return [];
}

function renderTable(elId, rows, columns) {
  const table = document.getElementById(elId);
  if (!table) return;

  if (!rows || rows.length === 0) {
    table.innerHTML = `<tbody><tr><td>${state.lang === "zh" ? "尚未讀取到資料" : "No data loaded"}</td></tr></tbody>`;
    return;
  }

  const cols = columns || Object.keys(rows[0]);
  const head = `<thead><tr>${cols.map(c => `<th>${c}</th>`).join("")}</tr></thead>`;
  const body = rows.map(r => {
    return `<tr>${cols.map(c => `<td>${escapeHtml(r[c] || "")}</td>`).join("")}</tr>`;
  }).join("");

  table.innerHTML = `${head}<tbody>${body}</tbody>`;
}

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderKeywords() {
  const search = (document.getElementById("keywordSearch")?.value || "").toLowerCase();
  const rows = state.data.tfidf.filter(r => {
    if (!search) return true;
    return Object.values(r).join(" ").toLowerCase().includes(search);
  });

  renderTable("tfidfTable", rows, [
    "rank",
    "yes_keyword",
    "yes_score",
    "no_keyword",
    "no_score"
  ]);
}

function renderSentiment() {
  const rows = state.data.sentiment;
  renderTable("sentimentTable", rows);

  const box = document.getElementById("sentimentMetrics");
  if (!box) return;

  if (!rows.length) {
    box.innerHTML = "";
    return;
  }

  box.innerHTML = rows.map(r => {
    const rec = r.Recommended || r.recommended || "";
    const avg = r.avg_sentiment || "";
    const count = r.review_count || "";
    const score = r.avg_overall_score || "";
    return `
      <div class="metric">
        <span>Recommended = ${escapeHtml(rec)}</span>
        <strong>${escapeHtml(avg)}</strong>
        <span>${state.lang === "zh" ? "評論數" : "Reviews"}: ${escapeHtml(count)} | ${state.lang === "zh" ? "平均評分" : "Avg rating"}: ${escapeHtml(score)}</span>
      </div>
    `;
  }).join("");
}

function renderLdaTopics() {
  renderTable("ldaTopicsTable", state.data.ldaTopics, [
    "topic_id",
    "manual_topic_label",
    "topic_size",
    "top_words",
    "manual_interpretation"
  ]);
}

function renderReviews() {
  const filter = document.getElementById("topicFilter");
  const container = document.getElementById("reviewCards");
  if (!container) return;

  const topics = Array.from(new Set(state.data.reviews.map(r => r.topic_id))).sort((a, b) => Number(a) - Number(b));

  if (filter && filter.options.length <= 1) {
    topics.forEach(topic => {
      const option = document.createElement("option");
      option.value = topic;
      option.textContent = `Topic ${topic}`;
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
      <h4>Topic ${escapeHtml(r.topic_id)} · ${escapeHtml(r.manual_topic_label || r.topic_name_auto || "")}</h4>
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

  const anyLoaded = Object.values(state.data).some(arr => arr.length);
  if (!anyLoaded) {
    showToast(t("readFail"));
  }

  renderAll();
}

bindEvents();
applyLanguage();
loadData();
