from __future__ import annotations

from dataclasses import dataclass, field


ELEMENTS = ("wood", "fire", "earth", "metal", "water")
DEFAULT_LANGUAGES = ("en", "ko", "ja", "id", "th", "vi", "hi")
DEFAULT_PLATFORMS = ("tiktok", "instagram_reels", "facebook_reels")


def normalize_element(element: str) -> str:
    value = element.strip().lower()
    if value not in ELEMENTS:
        raise ValueError(f"Unsupported element: {element}")
    return value


@dataclass(frozen=True)
class SajuProfile:
    profile_id: str
    display_name: str
    day_master: str
    five_elements: dict[str, int]
    dominant_element: str
    lacking_element: str
    energy_flow: str
    yin_yang_balance: str
    season: str
    focus_themes: list[str] = field(default_factory=list)
    special_traits: list[str] = field(default_factory=list)
    target_languages: list[str] = field(default_factory=lambda: list(DEFAULT_LANGUAGES))
    target_platforms: list[str] = field(default_factory=lambda: list(DEFAULT_PLATFORMS))
    brand_label: str = "Saju Signal"

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "SajuProfile":
        five_elements_raw = payload.get("five_elements")
        if not isinstance(five_elements_raw, dict):
            raise ValueError("`five_elements` must be an object with element scores.")

        five_elements = {
            element: int(five_elements_raw.get(element, 0))
            for element in ELEMENTS
        }

        dominant = payload.get("dominant_element")
        lacking = payload.get("lacking_element")

        if not dominant:
            dominant = max(five_elements, key=five_elements.__getitem__)
        if not lacking:
            lacking = min(five_elements, key=five_elements.__getitem__)

        return cls(
            profile_id=str(payload.get("profile_id", "sample-saju")),
            display_name=str(payload.get("display_name", "Sample Saju Profile")),
            day_master=normalize_element(str(payload.get("day_master", dominant))),
            five_elements=five_elements,
            dominant_element=normalize_element(str(dominant)),
            lacking_element=normalize_element(str(lacking)),
            energy_flow=str(payload.get("energy_flow", "balanced-growth")),
            yin_yang_balance=str(payload.get("yin_yang_balance", "balanced")),
            season=str(payload.get("season", "spring")),
            focus_themes=[
                str(theme).strip().lower()
                for theme in payload.get("focus_themes", ["money", "career", "love"])
            ],
            special_traits=[
                str(trait).strip() for trait in payload.get("special_traits", [])
            ],
            target_languages=[
                str(code).strip().lower()
                for code in payload.get("target_languages", list(DEFAULT_LANGUAGES))
            ],
            target_platforms=[
                str(platform).strip().lower()
                for platform in payload.get("target_platforms", list(DEFAULT_PLATFORMS))
            ],
            brand_label=str(payload.get("brand_label", "Saju Signal")),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "profile_id": self.profile_id,
            "display_name": self.display_name,
            "day_master": self.day_master,
            "five_elements": self.five_elements,
            "dominant_element": self.dominant_element,
            "lacking_element": self.lacking_element,
            "energy_flow": self.energy_flow,
            "yin_yang_balance": self.yin_yang_balance,
            "season": self.season,
            "focus_themes": self.focus_themes,
            "special_traits": self.special_traits,
            "target_languages": self.target_languages,
            "target_platforms": self.target_platforms,
            "brand_label": self.brand_label,
        }


@dataclass(frozen=True)
class HookVariant:
    variant_id: str
    angle: str
    title: str
    support: str
    cta: str
    narration: str
    caption_lines: list[str]
    keywords: list[str]
    visual_motifs: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "variant_id": self.variant_id,
            "angle": self.angle,
            "title": self.title,
            "support": self.support,
            "cta": self.cta,
            "narration": self.narration,
            "caption_lines": self.caption_lines,
            "keywords": self.keywords,
            "visual_motifs": self.visual_motifs,
        }
