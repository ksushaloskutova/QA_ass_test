"""Utility functions for recommending electives based on user skills."""

from typing import List, Dict

# Example study plan structure mapping skill keywords to electives
STUDY_PLAN: Dict[str, List[str]] = {
    "programming": ["Введение в Python", "Разработка веб-приложений"],
    "data": ["Анализ данных", "Машинное обучение"],
    "design": ["UX/UI дизайн", "Графический дизайн"],
    "management": ["Проектный менеджмент", "Основы предпринимательства"],
}


def _parse_skills(skills_text: str) -> List[str]:
    """Split user input into a list of lowercase skill keywords."""
    return [s.strip().lower() for s in skills_text.split(",") if s.strip()]


def match_skills_to_subjects(skills: List[str], plan: Dict[str, List[str]] | None = None) -> List[str]:
    """Match user skills with subjects from the study plan."""
    if plan is None:
        plan = STUDY_PLAN

    electives: List[str] = []
    for skill in skills:
        for keyword, subjects in plan.items():
            if keyword in skill:
                electives.extend(subjects)
    # Remove duplicates while preserving order
    seen = set()
    unique_electives = []
    for subj in electives:
        if subj not in seen:
            seen.add(subj)
            unique_electives.append(subj)
    return unique_electives


def recommend_electives(skills_text: str) -> List[str]:
    """Return a list of recommended electives based on user skills text."""
    skills = _parse_skills(skills_text)
    return match_skills_to_subjects(skills)
