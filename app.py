import streamlit as st

from recommender import load_jobs, recommend
from ui_components import (CSS, card_html, footer_html, hero_html,
                           next_skills_html, steps_html)

st.set_page_config(page_title="Job Recommendation System", page_icon="💼", layout="centered",
                   initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data
def get_jobs():
    return load_jobs("jobs.csv")


jobs = get_jobs()

EDUCATION = ["BCA", "MCA", "B.Tech", "M.Tech", "BSc", "Other"]
EXPERIENCE = ["Fresher", "1-2 years", "3+ years"]
LOCATIONS = ["Any"] + sorted(jobs["location"].unique())

SAMPLES = {
    "Data analyst (fresher)": dict(skills="Python, SQL, Excel, Statistics, Data Visualization",
                                   education="BCA", experience="Fresher", role="Data Analyst", location="Any"),
    "Generative AI developer": dict(skills="Python, LLM, RAG, LangChain, FastAPI",
                                    education="B.Tech", experience="Fresher", role="Generative AI Engineer", location="Any"),
    "Web developer": dict(skills="JavaScript, React, HTML, CSS, Git",
                          education="BCA", experience="Fresher", role="Frontend Developer", location="Any"),
}

# default values (only set once per session)
st.session_state.setdefault("searched", False)
for k, v in SAMPLES["Data analyst (fresher)"].items():
    st.session_state.setdefault(k, v)


def use_sample(name):
    st.session_state.update(SAMPLES[name])
    st.session_state["searched"] = True


def start_search():
    st.session_state["searched"] = True


# ------------------------------------------------------------------- sidebar
with st.sidebar:
    st.subheader("Your profile")
    st.text_area("Skills (separate with commas)", key="skills", height=90)
    st.selectbox("Education", EDUCATION, key="education")
    st.selectbox("Experience", EXPERIENCE, key="experience")
    st.text_input("Job role you want", key="role")
    st.selectbox("Location", LOCATIONS, key="location")
    top_n = st.slider("How many jobs to show", 3, 15, 5)
    st.button("Find jobs", type="primary", use_container_width=True, on_click=start_search)

    st.divider()
    st.caption("Not sure where to start? Try an example profile.")
    for name in SAMPLES:
        st.button(name, key=f"sample_{name}", use_container_width=True,
                  on_click=use_sample, args=(name,))

# ---------------------------------------------------------------------- main
st.markdown(hero_html(len(jobs)), unsafe_allow_html=True)

if not st.session_state["searched"]:
    st.markdown(steps_html(), unsafe_allow_html=True)
elif not st.session_state["skills"].strip():
    st.warning("Add at least one skill in the panel on the left to get recommendations.")
else:
    s = st.session_state
    recs = recommend(jobs, s["skills"], s["education"], s["experience"], s["role"],
                     "" if s["location"] == "Any" else s["location"], top_n)
    if recs.empty:
        st.info("No matching jobs found. Try adding more skills or a different job role.")
    else:
        title = s["role"].strip() or "your skills"
        st.markdown(f'<div class="jr-summary">Top {len(recs)} matches for {title}</div>',
                    unsafe_allow_html=True)
        st.markdown(next_skills_html(recs), unsafe_allow_html=True)
        for _, row in recs.iterrows():
            st.markdown(card_html(row), unsafe_allow_html=True)
        st.markdown(footer_html(), unsafe_allow_html=True)
