from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from app.parser import extract_text_from_pdf, segment_sections
from app.cleaner import clean_text
from app.skill_extractor import (
    load_skill_taxonomy,
    extract_skills_from_sections,
    merge_and_score_skills,
    extract_jd_skills
)
from app.ner_extractor import extract_skills_ner, normalize_ner_skills
from app.skill_fusion import fuse_skills
from app.embedder import SkillEmbedder
from app.matcher import compute_skill_similarity, compute_match_score
from app.skill_priority import load_skill_weights, rank_missing_skills, assign_priority_levels
from app.analysis_builder import build_analysis_output
from app.llm_chain import generate_llm_feedback

app = FastAPI(title="LLM Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

taxonomy = load_skill_taxonomy("data/skill_taxonomy.json")
skill_weights = load_skill_weights("data/skill_weights.json")
embedder = SkillEmbedder()

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # 1. Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await resume.read())
        resume_path = tmp.name

    # 2. Parse & clean resume
    raw_text = extract_text_from_pdf(resume_path)
    cleaned_text = clean_text(raw_text)
    sections = segment_sections(cleaned_text)

    os.remove(resume_path)

    # 3. Rule-based skill extraction
    rule_extracted = extract_skills_from_sections(sections, taxonomy)
    rule_scores = merge_and_score_skills(rule_extracted)

    # 4. Transformer NER extraction
    ner_raw = extract_skills_ner(cleaned_text)
    ner_normalized = normalize_ner_skills(ner_raw, taxonomy)

    # 5. Hybrid skill fusion
    resume_skills = fuse_skills(rule_scores, ner_normalized)

    # 6. JD skill extraction
    jd_cleaned = clean_text(job_description)
    jd_skills = extract_jd_skills(jd_cleaned, taxonomy)

    # 7. Semantic matching
    sim_matrix, resume_names, jd_names = compute_skill_similarity(
        resume_skills, jd_skills, embedder
    )

    score, matched, missing = compute_match_score(
        sim_matrix, resume_skills, resume_names, jd_names
    )

    # 8. Skill gap prioritization
    ranked = rank_missing_skills(missing, skill_weights)
    prioritized = assign_priority_levels(ranked)

    # 9. Build structured analysis
    analysis_output = build_analysis_output(score, matched, prioritized)

    # 10. LLM explanation
    llm_response = generate_llm_feedback(analysis_output)

    return {
        "analysis": analysis_output,
        "llm_feedback": llm_response
    }
