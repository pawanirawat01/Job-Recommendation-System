"""HTML/CSS building blocks for the Streamlit UI (no Streamlit import, so it is easy to test)."""

from collections import Counter
from html import escape

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --ink: #16213E; --muted: #5B6785; --line: #E2E7F0; --bg: #F5F7FB;
  --brand: #2F5BEA; --good: #0F7A57; --good-bg: #E3F4EC;
  --gap: #8A5200; --gap-line: #EBCF98;
}
html, body, .stApp, [class*="css"] {
  font-family: 'Manrope', system-ui, -apple-system, 'Segoe UI', sans-serif;
}
.block-container { max-width: 920px; padding-top: 2.2rem; padding-bottom: 3rem; }
#MainMenu, footer { visibility: hidden; }

/* ---------- hero ---------- */
.jr-hero h1 {
  font-size: 2.3rem; line-height: 1.15; font-weight: 800; letter-spacing: -0.02em;
  color: var(--ink); margin: 0 0 .6rem 0; padding: 0;
}
.jr-hero p { font-size: 1.05rem; line-height: 1.6; color: var(--muted); max-width: 60ch; margin: 0 0 1.6rem 0; }

/* ---------- steps (empty state) ---------- */
.jr-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: .4rem; }
.jr-step { border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; background: #fff; }
.jr-step b { display: block; color: var(--ink); font-size: 1rem; margin-bottom: 4px; }
.jr-step span { color: var(--muted); font-size: .9rem; line-height: 1.5; }
.jr-step i { font-style: normal; font-weight: 800; color: var(--brand); margin-right: 6px; }
@media (max-width: 720px) { .jr-steps { grid-template-columns: 1fr; } }

/* ---------- result summary ---------- */
.jr-summary { font-size: 1.15rem; font-weight: 700; color: var(--ink); margin: .2rem 0 .9rem 0; }
.jr-next { border: 1px solid var(--line); border-radius: 12px; background: #fff;
           padding: 14px 18px; margin-bottom: 20px; }
.jr-next p { margin: 0 0 8px 0; font-weight: 700; color: var(--ink); font-size: .95rem; }
.jr-next small { color: var(--muted); font-weight: 500; }

/* ---------- job card ---------- */
.jr-card { border: 1px solid var(--line); border-radius: 14px; background: #fff;
           padding: 20px 22px; margin-bottom: 14px; }
.jr-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 18px; }
.jr-title { font-size: 1.2rem; font-weight: 800; color: var(--ink); line-height: 1.3; }
.jr-company { font-size: .95rem; font-weight: 600; color: var(--muted); margin: 2px 0 10px 0; }
.jr-tags span { display: inline-block; font-size: .8rem; font-weight: 600; color: var(--ink);
                background: var(--bg); border-radius: 6px; padding: 3px 9px; margin: 0 6px 6px 0; }

.jr-score { text-align: center; flex: 0 0 auto; }
.jr-ring { width: 72px; height: 72px; border-radius: 50%; position: relative; display: grid;
           place-items: center;
           background: conic-gradient(var(--c) calc(var(--p) * 1%), #E6EAF2 0); }
.jr-ring::before { content: ""; position: absolute; inset: 7px; background: #fff; border-radius: 50%; }
.jr-ring span { position: relative; font-weight: 800; font-size: 1rem; color: var(--ink); }
.jr-label { font-size: .75rem; font-weight: 700; color: var(--muted); margin-top: 6px; }

.jr-row { display: flex; align-items: baseline; gap: 12px; margin-top: 6px; }
.jr-k { flex: 0 0 62px; font-size: .82rem; font-weight: 700; color: var(--muted); }
.jr-chips { flex: 1; }
.chip { display: inline-block; font-size: .8rem; font-weight: 600; border-radius: 999px;
        padding: 3px 11px; margin: 0 6px 6px 0; }
.chip.good { background: var(--good-bg); color: var(--good); }
.chip.gap  { background: #fff; color: var(--gap); border: 1px solid var(--gap-line); }
.chip.none { color: var(--muted); font-weight: 500; padding-left: 0; }

.jr-card details { margin-top: 10px; border-top: 1px solid var(--line); padding-top: 10px; }
.jr-card summary { cursor: pointer; font-size: .88rem; font-weight: 700; color: var(--brand); }
.jr-card summary:focus-visible { outline: 2px solid var(--brand); outline-offset: 3px; border-radius: 4px; }
.jr-card details p { font-size: .9rem; line-height: 1.6; color: var(--ink); margin: 8px 0 0 0; max-width: 70ch; }

.jr-foot { color: var(--muted); font-size: .82rem; line-height: 1.5; margin-top: 18px; }

@media (max-width: 560px) {
  .jr-hero h1 { font-size: 1.7rem; }
  .jr-top { flex-direction: column-reverse; align-items: flex-start; }
  .jr-row { flex-direction: column; gap: 2px; }
}
</style>
"""


def hero_html(n_jobs: int) -> str:
    return (f'<div class="jr-hero"><h1>Find the tech jobs that fit your skills</h1>'
            f'<p>Add your skills and experience. We rank {n_jobs} jobs by how well they match you, '
            f'and show which skills to learn next.</p></div>')


def steps_html() -> str:
    steps = [("Add your profile", "Skills, education, experience and the role you want. Use the panel on the left."),
             ("We compare", "Your profile is matched against every job using TF-IDF and cosine similarity."),
             ("Pick the best fits", "See ranked jobs, the skills you already have, and the ones to learn.")]
    items = "".join(f'<div class="jr-step"><b><i>{i}</i>{escape(t)}</b><span>{escape(d)}</span></div>'
                    for i, (t, d) in enumerate(steps, 1))
    return f'<div class="jr-steps">{items}</div>'


def _band(score: float):
    if score >= 50:
        return "Strong match", "#0F7A57"
    if score >= 30:
        return "Good match", "#2F5BEA"
    return "Partial match", "#8791A8"


def _chips(items, kind: str, prefix: str) -> str:
    if not items:
        return '<span class="chip none">None</span>'
    return "".join(f'<span class="chip {kind}">{prefix}{escape(s)}</span>' for s in items)


def card_html(row) -> str:
    score = float(row["match_score"])
    label, color = _band(score)
    pct = max(3, min(int(round(score)), 100))
    tags = "".join(f"<span>{escape(str(t))}</span>"
                   for t in (row["location"], row["experience"], row.get("education", "")) if t)
    desc = escape(str(row.get("description", "")))
    details = f"<details><summary>Job description</summary><p>{desc}</p></details>" if desc else ""
    return (
        '<div class="jr-card">'
        '<div class="jr-top"><div>'
        f'<div class="jr-title">{escape(str(row["title"]))}</div>'
        f'<div class="jr-company">{escape(str(row["company"]))}</div>'
        f'<div class="jr-tags">{tags}</div></div>'
        f'<div class="jr-score"><div class="jr-ring" style="--p:{pct};--c:{color}">'
        f'<span>{score:.0f}%</span></div><div class="jr-label">{label}</div></div></div>'
        f'<div class="jr-row"><span class="jr-k">You have</span>'
        f'<div class="jr-chips">{_chips(row["matched_skills"], "good", "✓ ")}</div></div>'
        f'<div class="jr-row"><span class="jr-k">To learn</span>'
        f'<div class="jr-chips">{_chips(row["missing_skills"], "gap", "+ ")}</div></div>'
        f'{details}</div>'
    )


def next_skills_html(recs, limit: int = 6) -> str:
    """Skills that appear most often in the matched jobs but are missing from the user's profile."""
    counts = Counter(s for lst in recs["missing_skills"] for s in lst)
    if not counts:
        return ""
    chips = "".join(f'<span class="chip gap">+ {escape(s)} <small>in {c}</small></span>'
                    for s, c in counts.most_common(limit))
    return f'<div class="jr-next"><p>Worth learning next</p>{chips}</div>'


def footer_html() -> str:
    return ('<div class="jr-foot">Scores combine text similarity (80%), location (10%) and experience (10%). '
            'Recommendations are suggestions and do not guarantee a job.</div>')
