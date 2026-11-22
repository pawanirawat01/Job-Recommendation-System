"""
Job Recommendation System - core engine
Content-based filtering using TF-IDF + Cosine Similarity.

Pipeline:
User Input -> Data Collection -> Preprocessing -> Feature Extraction
-> Similarity Calculation -> Ranking -> Recommendations
"""

import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Weights for the final score (sum = 1.0)
W_CONTENT = 0.80      # TF-IDF cosine similarity (skills, role, description)
W_LOCATION = 0.10     # location preference
W_EXPERIENCE = 0.10   # experience level match


# ---------------------------------------------------------------- preprocessing
def clean_text(text) -> str:
    """Lowercase, drop special characters (keeps + and # for C++, C#), trim spaces."""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9+#\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def split_skills(text) -> list:
    """'Python, SQL; Machine Learning' -> ['python', 'sql', 'machine learning']"""
    parts = re.split(r"[;,]", str(text))
    return [p.strip().lower() for p in parts if p.strip()]


def load_jobs(path: str = "jobs.csv") -> pd.DataFrame:
    """Load the job dataset (CSV) and prepare the text used for TF-IDF."""
    df = pd.read_csv(path)
    df = df.fillna("")                                         # handle missing values
    df = df.drop_duplicates(subset=["title", "company", "location"])
    df = df.reset_index(drop=True)

    df["skills_list"] = df["skills"].apply(split_skills)

    def combine(row):
        skills = " ".join(row["skills_list"])
        # title x2 and skills x3 give these fields more weight than the description
        text = f"{row['title']} {row['title']} {skills} {skills} {skills} " \
               f"{row['education']} {row['description']}"
        return clean_text(text)

    df["combined"] = df.apply(combine, axis=1)
    return df


# --------------------------------------------------------------- recommendation
def recommend(jobs: pd.DataFrame, skills: str, education: str = "",
              experience: str = "", role: str = "", location: str = "",
              top_n: int = 10) -> pd.DataFrame:
    """Return the top_n jobs ranked by match score (0-100)."""
    user_skills = split_skills(skills)
    skills_text = " ".join(user_skills)

    # User profile text (role and skills weighted higher, like the job text)
    user_text = clean_text(f"{role} {role} {skills_text} {skills_text} "
                           f"{skills_text} {education}")

    # Feature extraction: TF-IDF on all jobs + the user profile
    vectorizer = TfidfVectorizer(ngram_range=(1, 2),
                                 token_pattern=r"[a-z0-9+#]+",
                                 stop_words="english")
    matrix = vectorizer.fit_transform(list(jobs["combined"]) + [user_text])

    # Similarity: user vector (last row) vs every job vector
    content_score = cosine_similarity(matrix[-1], matrix[:-1]).ravel()

    # Extra signals
    loc = location.strip().lower()
    loc_score = jobs["location"].apply(
        lambda j: 1.0 if loc and (loc in j.lower() or j.lower() == "remote") else 0.0)
    exp = experience.strip().lower()
    exp_score = jobs["experience"].apply(lambda j: 1.0 if exp and exp == j.lower() else 0.0)

    final = W_CONTENT * content_score + W_LOCATION * loc_score + W_EXPERIENCE * exp_score

    result = jobs.copy()
    result["match_score"] = (final * 100).round(1)

    # Skill gap analysis: matched vs missing skills
    uset = set(user_skills)
    result["matched_skills"] = result["skills_list"].apply(
        lambda s: [x for x in s if x in uset])
    result["missing_skills"] = result["skills_list"].apply(
        lambda s: [x for x in s if x not in uset])

    result = result.sort_values("match_score", ascending=False)   # ranking
    result = result[result["match_score"] > 0].head(top_n)
    cols = ["title", "company", "location", "experience", "education", "skills",
            "description", "match_score", "matched_skills", "missing_skills"]
    return result[cols].reset_index(drop=True)


# --------------------------------------------------------------------- demo/CLI
if __name__ == "__main__":
    jobs = load_jobs("jobs.csv")
    print("Job Recommendation System (command line)\n")
    skills = input("Skills (comma separated): ") or "Python, SQL, Machine Learning"
    education = input("Education [BCA]: ") or "BCA"
    experience = input("Experience (Fresher / 1-2 years / 3+ years) [Fresher]: ") or "Fresher"
    role = input("Preferred job role [Data Analyst]: ") or "Data Analyst"
    location = input("Preferred location (optional): ")

    recs = recommend(jobs, skills, education, experience, role, location, top_n=5)
    print("\nTop recommendations:\n")
    for i, r in recs.iterrows():
        print(f"{i + 1}. {r['title']} - {r['company']} ({r['location']})")
        print(f"   Match: {r['match_score']}%  |  Matched: {', '.join(r['matched_skills']) or '-'}")
        print(f"   Missing: {', '.join(r['missing_skills']) or '-'}\n")
