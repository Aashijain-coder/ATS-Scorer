import streamlit as st


def display_recommendations(analysis: dict) -> None:
    suggestions = analysis.get("suggestions") or []
    if not suggestions:
        return

    st.subheader("Recommendations")
    for suggestion in suggestions:
        st.markdown(f"- {suggestion}")

