import json
from typing import Dict, List

def load_skill_taxonomy(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)
    
def extract_skills_rule_based(text: str, taxonomy: Dict) -> List[str]:
    extracted_skills = set()
    text_lower = text.lower()

    for category in taxonomy.values():
        for skill, aliases in category.items():
            for alias in aliases:
                if alias in text_lower:
                    extracted_skills.add(skill)
    return list(extracted_skills)

def extract_skills_from_sections(sections: Dict, taxonomy: Dict) -> Dict:
    skills = {
        "skills_section": [],
        "experience_section": []
    }

    if sections.get("skills"):
        skills["skills_section"] = extract_skills_rule_based(
            sections["skills"], taxonomy
        )

    if sections.get("experience"):
        skills["experience_section"] = extract_skills_rule_based(
            sections["experience"], taxonomy
        )

    return skills

def merge_and_score_skills(extracted: Dict) -> Dict:
    skill_scores = {}

    for skill in extracted.get("experience_section", []):
        skill_scores[skill] = 0.7

    for skill in extracted.get("skills_section", []):
        skill_scores[skill] = max(skill_scores.get(skill, 0), 1.0)

    return skill_scores
