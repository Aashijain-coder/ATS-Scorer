from typing import List

import numpy as np
import spacy
from sentence_transformers import SentenceTransformer

from Backend.core.config import JD_KEYWORD_WEIGHT, JD_SEMANTIC_WEIGHT
from Backend.utils.matching import fuzzy_match_keywords


def compare_resume_with_jd(
    resume_text: str,
    resume_keywords: List[str],
    resume_skills: List[str],
    jd_text: str,
    jd_keywords: List[str],
    embedder: SentenceTransformer,
    nlp: spacy.Language,
) -> dict:
    matches = fuzzy_match_keywords(resume_keywords + resume_skills, jd_keywords)
    matched = matches["matched"]
    missing = matches["missing"]
    keyword_score = len(matched) / (len(matched) + len(missing)) if matched or missing else 0.0

    resume_vector, jd_vector = embedder.encode(
        [resume_text, jd_text], normalize_embeddings=True
    )
    similarity = float(np.clip(np.dot(resume_vector, jd_vector), 0.0, 1.0))
    match_score = JD_KEYWORD_WEIGHT * keyword_score + JD_SEMANTIC_WEIGHT * similarity

    return {
        "match_percentage": 100.0 * match_score,
        "semantic_similarity": similarity,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "skills_gap": missing.copy(),
    }
