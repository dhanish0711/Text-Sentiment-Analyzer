// State variables
let currentSentiment = "READY";
let activeLexicon = { positive: [], negative: [] };
let debounceTimer;

// DOM Elements
const textInput = document.getElementById("text-input");
const emojiIndicator = document.getElementById("emoji-indicator");
const statusLabel = document.getElementById("status-label");
const progressCircle = document.getElementById("progress-circle");
const gaugePercentage = document.getElementById("gauge-percentage");
const posCountEl = document.getElementById("pos-count");
const negCountEl = document.getElementById("neg-count");
const totalCountEl = document.getElementById("total-count");
const matchesContainer = document.getElementById("matches-container");
const resultCard = document.querySelector(".result-card");

const newWordInput = document.getElementById("new-word-input");
const posWordList = document.getElementById("pos-word-list");
const negWordList = document.getElementById("neg-word-list");

// Initialize application
document.addEventListener("DOMContentLoaded", () => {
    // 1. Load Lexicon from Server
    loadLexicon();

    // 2. Set up Input Listeners (Debounced)
    textInput.addEventListener("input", () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(analyzeSentiment, 250);
    });

    // 3. Set up Example Buttons
    document.querySelectorAll(".btn-example").forEach(btn => {
        btn.addEventListener("click", () => {
            textInput.value = btn.getAttribute("data-text");
            textInput.focus();
            analyzeSentiment();
        });
    });

    // 4. Set up Dictionary Tabs
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            // Remove active from all tabs
            document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            
            // Add active to selected
            btn.classList.add("active");
            const tabId = `tab-${btn.getAttribute("data-tab")}`;
            document.getElementById(tabId).classList.add("active");
        });
    });

    // 5. Add Word buttons
    document.getElementById("btn-add-pos").addEventListener("click", () => addWord(true));
    document.getElementById("btn-add-neg").addEventListener("click", () => addWord(false));
    newWordInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            // Default to adding to currently selected tab
            const activeTab = document.querySelector(".tab-btn.active").getAttribute("data-tab");
            addWord(activeTab === "positive");
        }
    });

    // Trigger initial analysis
    analyzeSentiment();
});

// --- API METHODS ---

async function analyzeSentiment() {
    const text = textInput.value.trim();

    if (!text) {
        // Reset GUI states to default empty state
        updateUI({
            sentiment: "READY",
            emoji: "😐",
            positive_count: 0,
            negative_count: 0,
            total_words: 0,
            ratio: 0,
            matched_positive: [],
            matched_negative: []
        });
        return;
    }

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        if (response.ok) {
            const data = await response.json();
            updateUI(data);
        }
    } catch (error) {
        console.error("Error analyzing sentiment:", error);
    }
}

async function loadLexicon() {
    try {
        const response = await fetch("/api/lexicon");
        if (response.ok) {
            activeLexicon = await response.json();
            renderLexicon();
        }
    } catch (error) {
        console.error("Error loading lexicon:", error);
    }
}

async function addWord(isPositive) {
    const word = newWordInput.value.trim().toLowerCase();
    if (!word) return;

    try {
        const response = await fetch("/api/lexicon/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ word, is_positive: isPositive })
        });

        if (response.ok) {
            newWordInput.value = "";
            await loadLexicon();
            // Re-analyze existing text with new dictionary list
            analyzeSentiment();
        } else {
            const err = await response.json();
            alert(err.error || "Failed to add word.");
        }
    } catch (error) {
        console.error("Error adding word:", error);
    }
}

async function removeWord(word, isPositive) {
    try {
        const response = await fetch("/api/lexicon/remove", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ word, is_positive: isPositive })
        });

        if (response.ok) {
            await loadLexicon();
            // Re-analyze existing text
            analyzeSentiment();
        }
    } catch (error) {
        console.error("Error removing word:", error);
    }
}

// --- DOM RENDER METHODS ---

function updateUI(data) {
    // 1. Glow & Class border updates
    resultCard.classList.remove("state-positive", "state-negative", "state-neutral");
    
    if (data.sentiment === "POSITIVE") {
        resultCard.classList.add("state-positive");
    } else if (data.sentiment === "NEGATIVE") {
        resultCard.classList.add("state-negative");
    } else {
        resultCard.classList.add("state-neutral");
    }

    // 2. Animate Emoji if state changes
    if (currentSentiment !== data.sentiment) {
        emojiIndicator.classList.add("pulse-animation");
        setTimeout(() => emojiIndicator.classList.remove("pulse-animation"), 600);
        currentSentiment = data.sentiment;
    }

    emojiIndicator.textContent = data.emoji;
    statusLabel.textContent = data.sentiment;

    // 3. Update Numeric counters
    posCountEl.textContent = data.positive_count;
    negCountEl.textContent = data.negative_count;
    totalCountEl.textContent = data.total_words;

    // 4. Update SVG Circle Gauge
    // Circumference = 2 * PI * r = 2 * 3.14159 * 50 = 314.16
    const circumference = 314.16;
    let offset = circumference;
    
    if (data.positive_count + data.negative_count > 0) {
        offset = circumference - (circumference * data.ratio) / 100;
        gaugePercentage.textContent = `${data.ratio}%`;
    } else {
        gaugePercentage.textContent = "0%";
    }
    
    progressCircle.style.strokeDashoffset = offset;

    // 5. Update keyword lists helper
    matchesContainer.innerHTML = "";
    
    if (data.matched_positive.length === 0 && data.matched_negative.length === 0) {
        matchesContainer.innerHTML = `<p class="matches-placeholder">${data.total_words > 0 ? "No sentiment words detected" : "Type something to begin analysis"}</p>`;
    } else {
        if (data.matched_positive.length > 0) {
            const p = document.createElement("p");
            p.className = "match-line";
            p.innerHTML = `<span class="match-label-pos">Positive matched:</span> ${data.matched_positive.join(", ")}`;
            matchesContainer.appendChild(p);
        }
        if (data.matched_negative.length > 0) {
            const p = document.createElement("p");
            p.className = "match-line";
            p.innerHTML = `<span class="match-label-neg">Negative matched:</span> ${data.matched_negative.join(", ")}`;
            matchesContainer.appendChild(p);
        }
    }
}

function renderLexicon() {
    // Clear lists
    posWordList.innerHTML = "";
    negWordList.innerHTML = "";

    // Render positive words
    if (activeLexicon.positive && activeLexicon.positive.length > 0) {
        activeLexicon.positive.forEach(word => {
            const pill = createWordPill(word, true);
            posWordList.appendChild(pill);
        });
    } else {
        posWordList.innerHTML = '<span class="dict-sub" style="margin: auto; display: block; text-align: center;">No positive words.</span>';
    }

    // Render negative words
    if (activeLexicon.negative && activeLexicon.negative.length > 0) {
        activeLexicon.negative.forEach(word => {
            const pill = createWordPill(word, false);
            negWordList.appendChild(pill);
        });
    } else {
        negWordList.innerHTML = '<span class="dict-sub" style="margin: auto; display: block; text-align: center;">No negative words.</span>';
    }
}

function createWordPill(word, isPositive) {
    const pill = document.createElement("span");
    pill.className = `word-pill ${isPositive ? "pos-pill" : "neg-pill"}`;
    pill.textContent = word;

    const removeBtn = document.createElement("i");
    removeBtn.className = "fa-solid fa-xmark remove-btn";
    removeBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        removeWord(word, isPositive);
    });

    pill.appendChild(removeBtn);
    return pill;
}
