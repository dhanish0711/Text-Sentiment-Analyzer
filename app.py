from flask import Flask, render_template, request, jsonify
import json
import os
import re

app = Flask(__name__)

LEXICON_FILE = "lexicon.json"

DEFAULT_LEXICON = {
    "positive": [
        "accomplish", "accomplished", "achieve", "achievement", "amazing", "amused", 
        "amusing", "appreciate", "appreciated", "appreciation", "awesome", "beautiful", 
        "best", "better", "blessed", "brave", "bright", "brilliant", "calm", 
        "cheerful", "cheerfully", "clean", "comfort", "comfortable", "cozy", 
        "creative", "dazzling", "delighted", "delicious", "easy", "efficient", 
        "enjoy", "enjoyable", "enjoyed", "exceed", "exceeded", "excellent", 
        "excited", "fabulous", "fantastic", "favorite", "favor", "favored", 
        "fine", "flawless", "friendly", "fresh", "funny", "genius", "gentle", 
        "gifted", "glad", "gladly", "gladness", "glorious", "good", "grand", 
        "grateful", "gratitude", "great", "handsomely", "happy", "happier", 
        "happiest", "healthy", "heavenly", "heroic", "honest", "hope", "hopeful", 
        "hopefuls", "hopes", "ideal", "improve", "improved", "improvement", 
        "improving", "joy", "kind", "legendary", "liked", "likes", "love", 
        "lovely", "luck", "lucky", "luckily", "magic", "magical", "magnificent", 
        "marvel", "marvelous", "neat", "nice", "optimistic", "original", 
        "outstanding", "peaceful", "perfect", "perfectly", "pleasant", "please", 
        "pleased", "praise", "praised", "precious", "prefer", "preferred", 
        "proud", "recommend", "refreshing", "relaxed", "relaxing", "reliable", 
        "safe", "satisfactory", "satisfied", "satisfying", "secure", "simple", 
        "skilful", "skillful", "smart", "smartest", "smile", "smiles", "smiled", 
        "smiling", "spectacular", "splendid", "stable", "strong", "stunning", 
        "succeed", "succeeded", "succeeding", "successful", "super", "superb", 
        "superbly", "supportive", "supreme", "sweet", "talented", "tasty", 
        "terrific", "thank", "thanks", "thankful", "thrilled", "tidy", 
        "treasure", "trusted", "trustworthy", "valuable", "victory", "virtue", 
        "warm", "warmth", "welcoming", "winner", "win", "winning", "won", 
        "wonderful", "wonderfully", "worth", "worthy", "yummy"
    ],
    "negative": [
        "alarm", "alarmed", "alarming", "angry", "annoy", "annoyance", 
        "annoyed", "annoying", "annoys", "anxiety", "anxious", "ashamed", 
        "attack", "avoid", "avoided", "avoiding", "awful", "awfully", 
        "bad", "badly", "betray", "betrayed", "blame", "blamed", 
        "bored", "boring", "bore", "broken", "brutal", "bug", 
        "bugs", "careless", "cheap", "cheat", "cheated", "cheater", 
        "cold", "complain", "complained", "complaint", "complaints", "crap", 
        "criticize", "criticism", "cruel", "cry", "crying", "damage", 
        "damaged", "damages", "danger", "dangerous", "dead", "death", 
        "defect", "defective", "delay", "delayed", "deny", "denied", 
        "depressed", "depressing", "depression", "deprived", "despair", "desperate", 
        "destroy", "destroyed", "destruction", "destructive", "difficult", "difficulties", 
        "difficultly", "dirty", "disagree", "disaster", "disappointed", "disappointing", 
        "disappointment", "discomfort", "disgrace", "disgust", "disgusted", "disgusting", 
        "dislike", "disliked", "dislikes", "distress", "disturbed", "disturbing", 
        "dreadful", "dreadfully", "dumb", "empty", "error", "errors", 
        "exhausted", "expensive", "fail", "failed", "failing", "failure", 
        "fake", "fatal", "faulty", "fear", "fearful", "fearing", 
        "filthy", "foolish", "fraud", "frustrate", "frustrated", "frustrates", 
        "frustration", "garbage", "gloomy", "grief", "hard", "hardship", 
        "harm", "harmed", "harmful", "harms", "harsh", "hate", 
        "hated", "hateful", "hates", "hazard", "hazardous", "helpless", 
        "horrible", "hostile", "hurt", "hurting", "hurts", "ignorant", 
        "ignore", "ignored", "ill", "illness", "imperfect", "impossible", 
        "insecure", "irritated", "irritating", "jealous", "junk", 
        "lagging", "laggy", "liar", "lie", "lies", "lonely", 
        "lose", "loser", "losing", "lost", "mad", "mean", 
        "miserable", "nasty", "negative", "neglect", "neglected", "nonsense", 
        "offensive", "offended", "overpriced", "pain", "painful", "painfully", 
        "panic", "pessimistic", "poison", "poisonous", "poor", "poorly", 
        "problem", "problems", "regret", "regretful", "rejected", "rejection", 
        "ridiculous", "risk", "risky", "rude", "rubbish", 
        "ruin", "ruined", "ruins", "sad", "sadly", "saddened", 
        "scam", "scared", "scary", "shame", "sick", "sickness", 
        "silly", "slow", "sluggish", "smelly", "sorrow", "sorry", 
        "stinky", "stress", "stressed", "stressful", "struggle", "struggling", 
        "stupid", "suspicious", "tense", "terrible", "terribly", "threat", 
        "threatening", "tired", "trash", "trouble", "troubles", "unacceptable", 
        "uncomfortable", "unfair", "unfriendly", "unhappy", "unpleasant", "unlucky", 
        "unsuccessful", "untrustworthy", "ugly", "unsafe", "useless", "vulnerable", 
        "waste", "wasted", "weak", "worse", "worst", "worthless", 
        "worried", "worrisome", "worry", "wrong"
    ]
}

def load_lexicon():
    """Loads the lexicon from file or returns default lexicon."""
    if os.path.exists(LEXICON_FILE):
        try:
            with open(LEXICON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading lexicon file: {e}. Falling back to default.")
            return DEFAULT_LEXICON.copy()
    else:
        # Save default to file
        save_lexicon(DEFAULT_LEXICON)
        return DEFAULT_LEXICON.copy()

def save_lexicon(lexicon):
    """Saves the lexicon to a JSON file."""
    try:
        with open(LEXICON_FILE, "w", encoding="utf-8") as f:
            json.dump(lexicon, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving lexicon file: {e}")

# Load active lexicon on startup
active_lexicon = load_lexicon()

@app.route("/")
def index():
    """Serves the main frontend page."""
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyzes text sentiment and returns statistics."""
    data = request.get_json() or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "sentiment": "READY",
            "emoji": "😐",
            "positive_count": 0,
            "negative_count": 0,
            "total_words": 0,
            "ratio": 0,
            "matched_positive": [],
            "matched_negative": []
        })

    # Tokenize: strip punctuation, lowercase, split
    cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = cleaned_text.split()
    total_words = len(words)

    # Match words against lexicon
    pos_set = set(active_lexicon.get("positive", []))
    neg_set = set(active_lexicon.get("negative", []))

    matched_pos = [w for w in words if w in pos_set]
    matched_neg = [w for w in words if w in neg_set]

    pos_count = len(matched_pos)
    neg_count = len(matched_neg)

    # Sentiment logic
    if pos_count > neg_count:
        sentiment = "POSITIVE"
        emoji = "🌟"
    elif neg_count > pos_count:
        sentiment = "NEGATIVE"
        emoji = "😢"
    else:
        sentiment = "NEUTRAL"
        emoji = "😐"

    # Unique matches for display
    unique_pos = sorted(list(set(matched_pos)))
    unique_neg = sorted(list(set(matched_neg)))

    # Sentiment Ratio: percentage of positive words out of total sentiment words
    total_sentiment = pos_count + neg_count
    ratio = int((pos_count / total_sentiment) * 100) if total_sentiment > 0 else 0

    return jsonify({
        "sentiment": sentiment,
        "emoji": emoji,
        "positive_count": pos_count,
        "negative_count": neg_count,
        "total_words": total_words,
        "ratio": ratio,
        "matched_positive": unique_pos,
        "matched_negative": unique_neg
    })

@app.route("/api/lexicon", methods=["GET"])
def get_lexicon():
    """Returns the current active lexicon lists."""
    return jsonify(active_lexicon)

@app.route("/api/lexicon/add", methods=["POST"])
def add_word():
    """Adds a word to positive or negative lexicon list."""
    global active_lexicon
    data = request.get_json() or {}
    word = data.get("word", "").strip().lower()
    is_positive = data.get("is_positive", True)

    # Strip symbols from the word
    word = re.sub(r'[^\w]', '', word)

    if not word:
        return jsonify({"success": False, "error": "Invalid word"}), 400

    # Ensure lists exist
    if "positive" not in active_lexicon:
        active_lexicon["positive"] = []
    if "negative" not in active_lexicon:
        active_lexicon["negative"] = []

    # Clean old classifications
    if word in active_lexicon["positive"]:
        active_lexicon["positive"].remove(word)
    if word in active_lexicon["negative"]:
        active_lexicon["negative"].remove(word)

    # Add to target list
    if is_positive:
        active_lexicon["positive"].append(word)
    else:
        active_lexicon["negative"].append(word)

    # Sort lists
    active_lexicon["positive"] = sorted(list(set(active_lexicon["positive"])))
    active_lexicon["negative"] = sorted(list(set(active_lexicon["negative"])))

    save_lexicon(active_lexicon)
    return jsonify({"success": True})

@app.route("/api/lexicon/remove", methods=["POST"])
def remove_word():
    """Removes a word from the active lexicon."""
    global active_lexicon
    data = request.get_json() or {}
    word = data.get("word", "").strip().lower()
    is_positive = data.get("is_positive", True)

    target_key = "positive" if is_positive else "negative"

    if word in active_lexicon.get(target_key, []):
        active_lexicon[target_key].remove(word)
        save_lexicon(active_lexicon)
        return jsonify({"success": True})

    return jsonify({"success": False, "error": "Word not found in target list"}), 404

if __name__ == "__main__":
    # Run locally on http://127.0.0.1:5000/
    app.run(debug=True, host="127.0.0.1", port=5000)
