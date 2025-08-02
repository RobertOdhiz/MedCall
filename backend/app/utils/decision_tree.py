def classify_basic(text: str) -> str:
    keywords = {
        "chest pain": "Critical",
        "shortness of breath": "Critical",
        "headache": "Mild",
        "fever": "Moderate",
    }
    for k, v in keywords.items():
        if k in text.lower():
            return v
    return "Unknown"
