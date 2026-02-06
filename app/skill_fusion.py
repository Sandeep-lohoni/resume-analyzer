def fuse_skills(rule_skills: dict, ner_skills: list):
    fused = rule_skills.copy()

    for skill in ner_skills:
        if skill not in fused:
            fused[skill] = 0.6

    return fused
