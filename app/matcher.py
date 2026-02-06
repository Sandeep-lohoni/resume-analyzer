from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_skill_similarity(resume_skills, jd_skills, embedder):
    resume_names = list(resume_skills.keys())
    jd_names = list(jd_skills)

    if not resume_names or not jd_names:
        empty = np.zeros((len(resume_names), len(jd_names)))
        return empty, resume_names, jd_names

    resume_emb = embedder.embed(resume_names)
    jd_emb = embedder.embed(jd_names)

    similarity_matrix = cosine_similarity(resume_emb, jd_emb)

    return similarity_matrix, resume_names, jd_names


def compute_match_score(similarity_matrix, resume_skills, resume_names, jd_names, threshold=0.6):
    if not jd_names:
        return 0, [], []

    if not resume_names or similarity_matrix.size == 0:
        return 0, [], list(jd_names)

    total_score = 0.0
    total_weight = len(jd_names)

    matched_skills = []
    missing_skills = []

    for j, jd_skill in enumerate(jd_names):
        max_sim = float(similarity_matrix[:, j].max())

        if max_sim >= threshold:
            i = similarity_matrix[:, j].argmax()
            resume_skill = resume_names[i]
            confidence = resume_skills[resume_skill]
            weighted_score = max_sim * float(confidence)
            total_score += weighted_score
            matched_skills.append((jd_skill, resume_skill, float(round(max_sim, 2))))
        else:
            missing_skills.append(jd_skill)

    final_score = total_score / total_weight if total_weight else 0.0
    return float(round(final_score, 2)), matched_skills, missing_skills
