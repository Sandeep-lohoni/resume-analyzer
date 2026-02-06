def build_analysis_output(
    match_score,
    matched_skills,
    prioritized_missing_skills
):
    return {
        "match_score": float(round(float(match_score) * 100, 1)),
        "matched_skills": matched_skills,
        "missing_skills": prioritized_missing_skills,
        "summary": {
            "strengths": [m[1] for m in matched_skills],
            "gaps": [m["skill"] for m in prioritized_missing_skills]
        }
    }
