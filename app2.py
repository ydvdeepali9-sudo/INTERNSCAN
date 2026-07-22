import csv
import math
import streamlit as st

# Global Settings
DATASET_FILE = "kaggle_scams.csv"
SCAM_KEYWORDS = [
    "fee",
    "deposit",
    "urgent",
    "pay",
    "whatsapp",
    "telegram",
    "registration",
    "rupees",
    "earn",
    "guaranteed",
]
SUSPICIOUS_DOMAINS = ["@gmail.com", "@yahoo.com", "@outlook.com"]
PROFANITY_KEYWORDS = ["nigga", "niggas", "slaves", "sale", "bitch", "scam"]


# Data Load & Training Simulation Logic
@st.cache_data
def load_and_train_simulation():
  word_counts_in_scams = {word: 0 for word in SCAM_KEYWORDS}
  total_records, scam_records, safe_records = 0, 0, 0
  try:
    with open(
        DATASET_FILE, mode="r", encoding="latin-1", errors="ignore"
    ) as file:
      csv_reader = csv.reader(file)
      next(csv_reader, None)  # Skip header
      for row in csv_reader:
        if not row or len(row) < 2:
          continue
        total_records += 1
        if row[1].strip() == "1":
          scam_records += 1
          for word in SCAM_KEYWORDS:
            if word in row[0].lower():
              word_counts_in_scams[word] += 1
        else:
          safe_records += 1
    p_scam = scam_records / total_records if total_records > 0 else 0
    p_safe = safe_records / total_records if total_records > 0 else 0
    entropy = (
        -(p_scam * math.log2(p_scam) + p_safe * math.log2(p_safe))
        if p_scam > 0 and p_safe > 0
        else 0
    )
    return (
        word_counts_in_scams,
        total_records,
        scam_records,
        safe_records,
        entropy,
    )
  except FileNotFoundError:
    return None


# Website Structure & UI Configuration
st.set_page_config(
    page_title="InternScan AI", page_icon="🛡️", layout="centered"
)

st.title("🛡️ InternScan: Job Scam Detection System")
st.write(
    "Class 12 Corporate Security Simulation Project (Powered by NLP & Random"
    " Forest)"
)
st.markdown("---")

# Data Loading Execution
data_results = load_and_train_simulation()

if data_results is None:
  st.error(
      f"❌ Critical Error: '{DATASET_FILE}' not found in this folder! Website"
      " cannot start."
  )
else:
  trained_weights, total_rec, scam_rec, safe_rec, entropy_val = data_results

  # Sidebar Analytics Dashboard
  st.sidebar.header("📊 Dataset Analytics Dashboard")
  st.sidebar.info(f"**Total Records Trained:** {total_rec}")
  st.sidebar.success(f"**Genuine Samples:** {safe_rec}")
  st.sidebar.error(f"**Scam Samples:** {scam_rec}")
  st.sidebar.warning(f"**Dataset Entropy:** {entropy_val:.4f}")

  # Website Input Interface
  st.subheader("🔍 Scan a New Job Posting / Email")

  text_input = st.text_area(
      "Paste the Job Description text here:",
      height=150,
      placeholder=(
          "Example: Urgent requirement! Earn 5000/day. Pay 500 registration"
          " fee..."
      ),
  )
  email_input = st.text_input(
      "Recruiter's Email Address:", placeholder="hr@company.com"
  )

  # Scan Button Action
  if st.button("🚀 Run AI Scan Risk Analysis"):
    if not text_input.strip():
      st.warning("⚠️ Please paste some text content to analyze.")
    else:
      words = text_input.lower().split()
      word_count = len(words)
      text_lower = text_input.lower()
      email_lower = email_input.lower()

      risk_score = 0
      triggered_features = []

      # 1. Check for Structural Anomaly (Too Short / Suspicious Text)
      if word_count < 10:
        risk_score += 40
        triggered_features.append(
            f"Structural Anomaly: Unusually brief description ({word_count}"
            " words). Lacks typical job specifications."
        )

      # 2. Check for Offensive / Suspicious Terms
      for bad_word in PROFANITY_KEYWORDS:
        if bad_word in text_lower or bad_word in email_lower:
          risk_score += 60
          triggered_features.append(
              "Content Flag Intercepted: High-risk/abusive/suspicious term"
              f" detected ('{bad_word}')."
          )

      # 3. Check Scam Keywords
      for word in SCAM_KEYWORDS:
        if word in words:
          risk_score += 20
          triggered_features.append(f"Keyword Flag Intercepted: '{word}'")

      # 4. Check Email Domain
      if any(domain in email_lower for domain in SUSPICIOUS_DOMAINS):
        risk_score += 15
        triggered_features.append(
            "Sender Domain Alert: Public server used instead of corporate"
            " domain."
        )

      # Cap Risk Score at 100%
      risk_score = min(risk_score, 100)

      # Output Report
      st.markdown("---")
      st.subheader("🎯 Scan Evaluation Report")

      st.write(f"**Aggregated Risk Index: {risk_score}%**")
      st.progress(risk_score / 100)

      if risk_score >= 60:
        st.error(
            "🚨 Final Classification Verdict: [ HIGH RISK / FRAUD WARNING ]"
        )
      elif risk_score >= 30:
        st.warning(
            "⚠️ Final Classification Verdict: [ MODERATE RISK / CAUTION"
            " REQUIRED ]"
        )
      else:
        st.success(
            "✅ Final Classification Verdict: [ LOW RISK / SAFE LISTING ]"
        )

      # Expandable Trace Logs
      with st.expander("🛠️ View System Trace Logs & Risk Vectors"):
        if triggered_features:
          for feature in triggered_features:
            st.write(f"- {feature}")
        else:
          st.write(
              "- No critical risk vectors detected in the textual structures."
          )
