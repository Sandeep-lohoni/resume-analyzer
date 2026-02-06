import logging
import spacy

logger = logging.getLogger(__name__)

def _load_spacy_model():
    for model_name in ("en_core_web_trf", "en_core_web_sm"):
        try:
            return spacy.load(model_name)
        except OSError:
            continue

    logger.warning(
        "spaCy model not found. Install 'en_core_web_trf' or 'en_core_web_sm'. "
        "Falling back to a blank 'en' pipeline; NER will be disabled."
    )
    return spacy.blank("en")

nlp = _load_spacy_model()

def extract_entities(text: str):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def extract_skills_ner(text: str):
    entities = extract_entities(text)
    
    skill_like = []
    for ent_text, ent_label in entities:
        if ent_label in ["ORG", "PRODUCT", "LANGUAGE", "WORK_OF_ART"]:
            skill_like.append(ent_text.lower())

    return list(set(skill_like))

def normalize_ner_skills(ner_skills, taxonomy):
    normalized = set()

    for category in taxonomy.values():
        for skill, aliases in category.items():
            for alias in aliases:
                for ner_skill in ner_skills:
                    if alias in ner_skill:
                        normalized.add(skill)

    return list(normalized)
