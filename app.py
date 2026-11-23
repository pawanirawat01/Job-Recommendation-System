import streamlit as st

from recommender import load_jobs, recommend

st.set_page_config(page_title="Job Recommendation System", page_icon="💼", layout="wide")


@st.cache_data
def get_jobs():
    return load_jobs("jobs.csv")


jobs = get_jobs()

st.title("💼 Job Recommendation System")
st.caption("Enter your profile and get jobs ranked by how well they match. "
           "Suggestions are guidance only and do not guarantee a job.")

# user input
with st.sidebar:
    st.header("Your profile")
    skills = st.text_area("Skills (comma separated)", "Python, SQL, Machine Learning")
    education = st.selectbox("Education", ["BCA", "MCA", "B.Tech", "BSc", "Other"])
    experience = st.selectbox("Experience", ["Fresher", "1-2 years", "3+ years"])
    role = st.text_input("Preferred job role", "Data Analyst")
    locations = ["Any"] + sorted(jobs["location"].unique())
    location = st.selectbox("Preferred location", locations)
    top_n = st.slider("Number of recommendations", 3, 15, 5)
    go = st.button("Recommend jobs", type="primary", use_container_width=True)

#  results
if go:
    if not skills.strip():
        st.warning("Please enter at least one skill.")
    else:
        recs = recommend(jobs, skills, education, experience, role,
                         "" if location == "Any" else location, top_n)
        if recs.empty:
            st.info("No matching jobs found. Try adding more skills.")
        else:
            st.subheader(f"Top {len(recs)} recommendations")
            for i, r in recs.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    c1.markdown(f"### {i + 1}. {r['title']}")
                    c1.write(f"**{r['company']}**  |  📍 {r['location']}  |  "
                             f"🎓 {r['experience']}")
                    c2.metric("Match", f"{r['match_score']}%")
                    st.progress(min(int(r["match_score"]), 100))
                    st.write("**Required skills:** " + r["skills"].replace(";", ", "))
                    st.write("✅ **You have:** " + (", ".join(r["matched_skills"]) or "-"))
                    st.write("📘 **To learn:** " + (", ".join(r["missing_skills"]) or "-"))
else:
    st.info("Fill in your details in the sidebar and click **Recommend jobs**.")

