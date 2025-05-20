import streamlit as st
import re

# === Alankar Detection Functions ===

def detect_utpreksha(sentence):
    imagination_words = ["જાણે", "માનીએ કે", "જેમ કે", "જો કે", "થાય એવું કે", "લાગે એવું કે"]
    return "ઉત્પ્રેક્ષા અલંકાર – અર્થાલંકાર" if any(word in sentence for word in imagination_words) else None

def detect_rupak(sentence):
    starts = ["તે", "તેણે", "તેને", "તેનું", "તેવો", "એનું", "એના", "એ", "પેલો", "પેલી"]
    return "રૂપક અલંકાર – અર્થાલંકાર" if any(sentence.strip().startswith(start) for start in starts) else None

def detect_upama(sentence):
    markers = ["કેમ", "ની જેમ", "પ્રમાણે", "જેમ"]
    return "ઉપમા અલંકાર – અર્થાલંકાર" if any(marker in sentence for marker in markers) else None

def detect_virodh(sentence):
    contrast_words = ["પરંતુ", "પણ", "છતાં", "તેમ છતાં", "તોય", "તો પણ", "છતાં પણ"]
    return "વિરોધ અલંકાર – અર્થાલંકાર" if any(word in sentence for word in contrast_words) else None

def detect_apurnokti(sentence):
    apurnokti_keywords = [
        "હવે હું શું કરું", "હવે શું થાય", "હવે શું થશે", 
        "હવે શું કરવું", "હું શું કરું", "હવે શું", 
        "કેવી રીતે આગળ વધવું", "તો પછી હું", 
        "જો એ આવી જાય તો", "મારા આશાઓની دنیا તો બસ"
    ]
    sentence_clean = sentence.strip()
    if sentence_clean.endswith("..."):
        return "અપૂર્ણોક્તિ અલંકાર – અર્થાલંકાર"
    if sentence_clean.endswith("?") and any(keyword in sentence_clean for keyword in apurnokti_keywords):
        return "અપૂર્ણોક્તિ અલંકાર – અર્થાલંકાર"
    if any(sentence_clean.endswith(keyword) for keyword in apurnokti_keywords):
        return "અપૂર્ણોક્તિ અલંકાર – અર્થાલંકાર"
    return None

def detect_ananvay_absolute(sentence):
    exclusivity_keywords = ["માત્ર", "ફક્ત", "કેવળ", "જ"]
    negation_phrases = [
        "બીજું નથી", "બીજું કોઈ નથી", "બીજું નહિ", "બીજું કંઈ નથી", 
        "અન્ય કંઈ નથી", "બીજા બધામાં નથી", "બીજા ક્યાં છે"
    ]
    if any(kw in sentence for kw in exclusivity_keywords) and any(re.search(pattern, sentence) for pattern in negation_phrases):
        return "Ananvay (અનન્વય) – Absolute Uniqueness"
    return None

def detect_anuprasa(sentence):
    words = sentence.split()
    for ch in set(''.join(sentence)):
        count = sum(word.startswith(ch) for word in words)
        if count >= 2:
            return "વર્ણાનુપ્રાસ અલંકાર – શબ્દાલંકાર"
    return None

# === Streamlit Page Setup ===

st.set_page_config(page_title="ગુજરાતી અલંકાર", layout="wide")

st.markdown("""
<style>
/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #3b82f6, #fbcfe8);
    background-size: auto;
}
/* Input field styling */
.stTextInput > div > div > input {
    background-color: rgba(255, 255, 255, 0.8) !important;
    color: black !important;
    border: 1px solid #ffffff !important;
}
/* Button styling */
.stButton button {
    background-color: #165BAA !important;
    color: black !important;
    border-radius: 10px;
    font-weight: bold;
}
/* Title and text color */
h1, h2, h3, h4, h5, h6, p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# === App Title ===
st.title("ગુજરાતી અલંકાર શોધક")

# === Input ===
sentence = st.text_input("ગુજરાતી વાક્ય દાખલ કરો:")

if st.button("શોધો"):
    if sentence.strip():
        detected = None
        for fn in [
            detect_utpreksha,
            detect_rupak,
            detect_upama,
            detect_virodh,
            detect_apurnokti,
            detect_ananvay_absolute,
            detect_anuprasa
        ]:
            result = fn(sentence)
            if result:
                detected = result
                break
        
        st.markdown(f"### વાક્ય: `{sentence}`")
        st.success(f"🔍 શોધાયેલ અલંકાર: **{detected}**" if detected else "❌ અલંકાર મળ્યો નહીં.")
    else:
        st.warning("કૃપા કરીને કોઈ વાક્ય દાખલ કરો.")
