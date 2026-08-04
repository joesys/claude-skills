"""Prompt-as-code contracts for the huh plain-language explainer skill."""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILL = REPO_ROOT / "skills" / "huh" / "SKILL.md"
CODEX_SKILL = REPO_ROOT / "codex-skills" / "huh" / "SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def compact(value: str) -> str:
    return " ".join(value.replace("\n>", "\n").split())


def huh_skills() -> tuple[str, str]:
    missing = [
        str(path.relative_to(REPO_ROOT))
        for path in (CANONICAL_SKILL, CODEX_SKILL)
        if not path.is_file()
    ]
    assert not missing, f"Missing huh skill files: {', '.join(missing)}"
    return read(CANONICAL_SKILL), read(CODEX_SKILL)


def test_huh_skill_is_discoverable_on_both_hosts() -> None:
    canonical, codex = huh_skills()

    for skill in (canonical, codex):
        frontmatter = skill.split("---", 2)[1]
        assert "name: huh" in frontmatter
        assert "plain language" in frontmatter
        assert "previous assistant message" in frontmatter

    assert "/huh <focus>" in canonical
    assert "$huh <focus>" in codex
    assert "/huh <focus>" not in codex


def test_huh_skill_explains_and_never_acts() -> None:
    for skill in huh_skills():
        normalized = compact(skill)
        assert "It never acts" in normalized
        assert "writes the explanation and stops" in normalized


def test_huh_skill_always_closes_with_both_disclosures() -> None:
    for skill in huh_skills():
        normalized = compact(skill)
        assert "Where I am least sure" in normalized
        assert "What you have not asked" in normalized
        assert "name a concrete part and the reason" in normalized
        assert "One to three items, biggest first" in normalized


def test_huh_skill_labels_added_analysis() -> None:
    for skill in huh_skills():
        normalized = compact(skill)
        # Dash-free substring: the adapter turns the canonical em dash
        # into "-" in the Codex copy.
        assert "the earlier answer did not mention this" in normalized


def test_huh_skill_stays_faithful_to_the_original() -> None:
    for skill in huh_skills():
        normalized = compact(skill)
        assert "do not rewrite history" in normalized
        assert "never repeat the first explanation verbatim" in normalized
