import json

def load_skill_weights(path: str):
    with open(path, "r") as f:
        return json.load(f)

def rank_missing_skills(missing_skills, skill_weights):
    ranked = []

    for skill in missing_skills:
        weight = skill_weights.get(skill, 0.4)
        ranked.append((skill, weight))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked

def assign_priority_levels(ranked_skills):
    prioritized = []

    for skill, weight in ranked_skills:
        if weight >= 0.8:
            level = "High"
        elif weight >= 0.6:
            level = "Medium"
        else:
            level = "Low"

        prioritized.append({
            "skill": skill,
            "importance": weight,
            "priority": level
        })

    return prioritized
