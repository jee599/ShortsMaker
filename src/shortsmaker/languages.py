from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguagePack:
    code: str
    label: str
    edge_voice: str
    azure_voice: str
    font_family: str
    badge_label: str
    element_names: dict[str, str]
    theme_names: dict[str, str]
    season_names: dict[str, str]


LANGUAGE_PACKS: dict[str, LanguagePack] = {
    "en": LanguagePack(
        code="en",
        label="English",
        edge_voice="en-US-AriaNeural",
        azure_voice="en-US-AvaMultilingualNeural",
        font_family="'Aptos', 'Segoe UI', sans-serif",
        badge_label="SAJU SIGNAL",
        element_names={
            "wood": "Wood",
            "fire": "Fire",
            "earth": "Earth",
            "metal": "Metal",
            "water": "Water",
        },
        theme_names={
            "money": "money",
            "career": "career",
            "love": "love life",
            "healing": "healing",
            "luck": "luck",
        },
        season_names={
            "spring": "spring",
            "summer": "summer",
            "autumn": "autumn",
            "winter": "winter",
        },
    ),
    "ko": LanguagePack(
        code="ko",
        label="Korean",
        edge_voice="ko-KR-SunHiNeural",
        azure_voice="ko-KR-SunHiNeural",
        font_family="'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif",
        badge_label="사주 시그널",
        element_names={
            "wood": "목",
            "fire": "화",
            "earth": "토",
            "metal": "금",
            "water": "수",
        },
        theme_names={
            "money": "돈 흐름",
            "career": "커리어",
            "love": "연애운",
            "healing": "회복운",
            "luck": "운의 흐름",
        },
        season_names={
            "spring": "봄",
            "summer": "여름",
            "autumn": "가을",
            "winter": "겨울",
        },
    ),
    "ja": LanguagePack(
        code="ja",
        label="Japanese",
        edge_voice="ja-JP-NanamiNeural",
        azure_voice="ja-JP-NanamiNeural",
        font_family="'Yu Gothic UI', 'Meiryo', sans-serif",
        badge_label="四柱シグナル",
        element_names={
            "wood": "木",
            "fire": "火",
            "earth": "土",
            "metal": "金",
            "water": "水",
        },
        theme_names={
            "money": "お金",
            "career": "仕事運",
            "love": "恋愛運",
            "healing": "回復運",
            "luck": "運気",
        },
        season_names={
            "spring": "春",
            "summer": "夏",
            "autumn": "秋",
            "winter": "冬",
        },
    ),
    "id": LanguagePack(
        code="id",
        label="Indonesian",
        edge_voice="id-ID-GadisNeural",
        azure_voice="id-ID-GadisNeural",
        font_family="'Segoe UI', 'Noto Sans', sans-serif",
        badge_label="SINYAL SAJU",
        element_names={
            "wood": "Kayu",
            "fire": "Api",
            "earth": "Tanah",
            "metal": "Logam",
            "water": "Air",
        },
        theme_names={
            "money": "rezeki",
            "career": "karier",
            "love": "asmara",
            "healing": "pemulihan",
            "luck": "keberuntungan",
        },
        season_names={
            "spring": "musim semi",
            "summer": "musim panas",
            "autumn": "musim gugur",
            "winter": "musim dingin",
        },
    ),
    "th": LanguagePack(
        code="th",
        label="Thai",
        edge_voice="th-TH-PremwadeeNeural",
        azure_voice="th-TH-PremwadeeNeural",
        font_family="'Leelawadee UI', 'Noto Sans Thai', sans-serif",
        badge_label="สัญญาณซาจู",
        element_names={
            "wood": "ไม้",
            "fire": "ไฟ",
            "earth": "ดิน",
            "metal": "โลหะ",
            "water": "น้ำ",
        },
        theme_names={
            "money": "การเงิน",
            "career": "งาน",
            "love": "ความรัก",
            "healing": "การฟื้นตัว",
            "luck": "โชค",
        },
        season_names={
            "spring": "ฤดูใบไม้ผลิ",
            "summer": "ฤดูร้อน",
            "autumn": "ฤดูใบไม้ร่วง",
            "winter": "ฤดูหนาว",
        },
    ),
    "vi": LanguagePack(
        code="vi",
        label="Vietnamese",
        edge_voice="vi-VN-HoaiMyNeural",
        azure_voice="vi-VN-HoaiMyNeural",
        font_family="'Segoe UI', 'Noto Sans', sans-serif",
        badge_label="TIN HIEU SAJU",
        element_names={
            "wood": "Moc",
            "fire": "Hoa",
            "earth": "Tho",
            "metal": "Kim",
            "water": "Thuy",
        },
        theme_names={
            "money": "tai loc",
            "career": "su nghiep",
            "love": "tinh cam",
            "healing": "phuc hoi",
            "luck": "van may",
        },
        season_names={
            "spring": "mua xuan",
            "summer": "mua he",
            "autumn": "mua thu",
            "winter": "mua dong",
        },
    ),
    "hi": LanguagePack(
        code="hi",
        label="Hindi",
        edge_voice="hi-IN-SwaraNeural",
        azure_voice="hi-IN-SwaraNeural",
        font_family="'Nirmala UI', 'Noto Sans Devanagari', sans-serif",
        badge_label="साजु सिग्नल",
        element_names={
            "wood": "लकड़ी",
            "fire": "अग्नि",
            "earth": "पृथ्वी",
            "metal": "धातु",
            "water": "जल",
        },
        theme_names={
            "money": "धन",
            "career": "कैरियर",
            "love": "प्रेम",
            "healing": "उपचार",
            "luck": "भाग्य",
        },
        season_names={
            "spring": "वसंत",
            "summer": "गर्मी",
            "autumn": "शरद",
            "winter": "सर्दी",
        },
    ),
}


def get_language_pack(code: str) -> LanguagePack:
    normalized = code.strip().lower()
    if normalized not in LANGUAGE_PACKS:
        raise ValueError(f"Unsupported language code: {code}")
    return LANGUAGE_PACKS[normalized]
