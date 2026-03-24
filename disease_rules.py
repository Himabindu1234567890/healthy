RULES = {
    "Diabetes": {
        "avoid": ["Sugar", "White Rice", "Sweets"],
        "prefer": ["Vegetables", "Millets", "Nuts"]
    },
    "Heart": {
        "avoid": ["Butter", "Fried Foods"],
        "prefer": ["Fruits", "Leafy Vegetables"]
    },
    "Anemia": {
        "avoid": [],
        "prefer": ["Spinach", "Beetroot", "Dates"]
    }
}

def disease_analysis(disease, foods):
    if disease == "None":
        return None

    avoid, prefer = [], []

    for f in foods:
        for a in RULES[disease]["avoid"]:
            if a.lower() in f.lower():
                avoid.append(f)
        for p in RULES[disease]["prefer"]:
            if p.lower() in f.lower():
                prefer.append(f)

    return {
        "avoid": list(set(avoid)),
        "prefer": list(set(prefer))
    }
