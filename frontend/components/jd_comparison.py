import streamlit as st


def display_jd_comparison(comparison: dict) -> None:
    st.subheader("Job description comparison")
    st.metric("Match", f"{comparison.get('match_percentage', 0):.1f}%")

    for field, label in (
        ("matched_keywords", "Matched keywords"),
        ("missing_keywords", "Missing keywords"),
        ("skills_gap", "Skills gap"),
    ):
        values = comparison.get(field) or []
        if values:
            st.markdown(f"**{label}**")
            st.text(", ".join(values))

