import pandas as pd


def load_jobs(path):
    return pd.read_csv(path).fillna("")


def _split(text, sep):
    return [s.strip() for s in str(text).split(sep) if s.strip()]


def recommend(jobs, skills, education, experience, role, location, top_n=5):
    user_skills = {s.lower() for s in _split(skills, ",")}
    role_words = [w for w in role.lower().split() if w]
    rows = []

    for _, j in jobs.iterrows():
        job_skills = _split(j["skills"], ";")
        matched = [s for s in job_skills if s.lower() in user_skills]
        missing = [s for s in job_skills if s.lower() not in user_skills]

        skill_pts = len(matched) / len(job_skills) if job_skills else 0
        title = j["title"].lower()
        role_pts = (sum(w in title for w in role_words) / len(role_words)
                    if role_words else 0)
        exp_pts = 1.0 if j["experience"] == experience else 0.0
        edu_list = _split(j["education"], ";")
        edu_pts = 1.0 if (not edu_list or education in edu_list) else 0.0
        loc_pts = 1.0 if (not location or j["location"] == location) else 0.0

        score = 100 * (0.60 * skill_pts + 0.15 * role_pts + 0.10 * exp_pts
                       + 0.10 * edu_pts + 0.05 * loc_pts)

        if matched or role_pts > 0:
            row = j.to_dict()
            row.update(match_score=round(score, 1),
                       matched_skills=matched, missing_skills=missing)
            rows.append(row)

    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows).sort_values("match_score", ascending=False)
    return out.head(top_n).reset_index(drop=True)

