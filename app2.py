if st.button("🚀 Run AI Scan Risk Analysis"):
    if not text_input.strip():
        st.warning("⚠️ Please paste some text content to analyze.")
    else:
        words = text_input.lower().split()
        word_count = len(words)
        risk_score = 0
        triggered_features = []

        # 1. Structural Anomaly: Check for suspicious/too short description
        if word_count < 10:
            risk_score += 40
            triggered_features.append(f"Structural Anomaly: Unusually brief description ({word_count} words). Lacks typical job specifications.")

        # 2. Check Scam Keywords
        for word in SCAM_KEYWORDS:
            if word in words:
                risk_score += 20
                triggered_features.append(f"Keyword Flag Intercepted: '{word}'")

        # 3. Check Domain
        if any(domain in email_input.lower() for domain in SUSPICIOUS_DOMAINS):
            risk_score += 15
            triggered_features.append("Sender Domain Alert: Public server used instead of corporate domain.")

        risk_score = min(risk_score, 100)
