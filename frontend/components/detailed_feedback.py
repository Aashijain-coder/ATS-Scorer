import streamlit as st


def display_detailed_feedback(analysis: dict) -> None:
    issues = analysis.get("detailed_feedback") or []
    if not issues:
        return

    st.subheader("Detailed feedback")
    for issue in issues:
        title = issue.get("issue_title") or "Resume feedback"
        severity = issue.get("severity_level")
        label = f"{title} ({severity.title()})" if severity else title
        with st.expander(label):
            for field, heading in (
                ("explanation", "Explanation"),
                ("ats_impact", "ATS impact"),
                ("where_it_appears", "Where it appears"),
                ("how_to_fix", "How to fix it"),
                ("example_improvement", "Example improvement"),
            ):
                value = issue.get(field)
                if value:
                    st.markdown(f"**{heading}**")
                    st.write(value)

