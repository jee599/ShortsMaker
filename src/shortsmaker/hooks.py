from __future__ import annotations

from typing import Iterable

from shortsmaker.languages import get_language_pack
from shortsmaker.models import HookVariant, SajuProfile
from shortsmaker.utils import chunk_text


ELEMENT_MOTIFS = {
    "wood": ["growth", "sprout", "rise"],
    "fire": ["flash", "spotlight", "heat"],
    "earth": ["ground", "weight", "stability"],
    "metal": ["blade", "signal", "clarity"],
    "water": ["wave", "flow", "mystery"],
}

TEMPLATES: dict[str, list[dict[str, str]]] = {
    "en": [
        {
            "angle": "warning",
            "title": "If {dominant} is overrunning your chart, one habit is choking your {theme}.",
            "support": "{day_master} day masters recover when {missing} energy comes back into balance.",
            "cta": "Save this before your next luck shift.",
        },
        {
            "angle": "reveal",
            "title": "Your weak {missing} energy may be the hidden reason your {theme} feels stuck.",
            "support": "When {dominant} pushes too hard in {season}, timing matters more than force.",
            "cta": "Follow for the next saju signal.",
        },
        {
            "angle": "timing",
            "title": "People with strong {dominant} in their chart are entering a sharp {theme} reset.",
            "support": "{balance_hint} means you win faster when you stop chasing and start aligning.",
            "cta": "Keep this short nearby when the signs repeat.",
        },
    ],
    "ko": [
        {
            "angle": "warning",
            "title": "{dominant} 기운이 사주를 과하게 누르면, {theme}을 막는 습관이 하나 생깁니다.",
            "support": "{day_master} 일간은 약한 {missing} 기운을 채워야 흐름이 다시 열립니다.",
            "cta": "다음 운의 변곡점 전에 저장해 두세요.",
        },
        {
            "angle": "reveal",
            "title": "약한 {missing} 기운이 지금 {theme}이 답답한 숨은 이유일 수 있습니다.",
            "support": "{season}의 흐름에서 {dominant}가 너무 강하면, 밀어붙임보다 타이밍이 먼저입니다.",
            "cta": "다음 사주 쇼츠도 받아보려면 팔로우하세요.",
        },
        {
            "angle": "timing",
            "title": "{dominant} 기운이 강한 사람은 곧 {theme} 판이 다시 짜입니다.",
            "support": "{balance_hint}일수록 억지보다 정렬이 훨씬 빨리 먹힙니다.",
            "cta": "같은 징조가 보이면 이 영상을 다시 보세요.",
        },
    ],
    "ja": [
        {
            "angle": "warning",
            "title": "命式で{dominant}が強すぎる人は、{theme}を止める習慣をひとつ抱えています。",
            "support": "{day_master}日主は、弱い{missing}の気を戻すほど流れが開きます。",
            "cta": "次の運気の切り替わり前に保存してください。",
        },
        {
            "angle": "reveal",
            "title": "弱い{missing}の気が、今の{theme}停滞の隠れた理由かもしれません。",
            "support": "{season}の流れで{dominant}が強すぎる時は、押すよりタイミングです。",
            "cta": "次の四柱ショートも見たいならフォローしてください。",
        },
        {
            "angle": "timing",
            "title": "{dominant}が強い命式の人は、これから{theme}の流れが大きく組み替わります。",
            "support": "{balance_hint}ほど、無理を減らして整える方が早く勝てます。",
            "cta": "同じサインが来たらこの動画を見返してください。",
        },
    ],
    "id": [
        {
            "angle": "warning",
            "title": "Kalau unsur {dominant} terlalu kuat di chart-mu, ada satu kebiasaan yang menahan {theme}.",
            "support": "Day master {day_master} pulih lebih cepat saat energi {missing} kembali seimbang.",
            "cta": "Simpan ini sebelum gelombang keberuntungan berikutnya datang.",
        },
        {
            "angle": "reveal",
            "title": "Energi {missing} yang lemah bisa jadi alasan tersembunyi kenapa {theme} terasa macet.",
            "support": "Saat {dominant} terlalu keras di {season}, timing lebih penting daripada memaksa.",
            "cta": "Ikuti untuk sinyal saju berikutnya.",
        },
        {
            "angle": "timing",
            "title": "Orang dengan unsur {dominant} yang kuat sedang masuk ke reset besar untuk {theme}.",
            "support": "{balance_hint} berarti kamu menang lebih cepat saat mulai selaras, bukan mengejar terus.",
            "cta": "Kembali ke video ini saat tandanya muncul lagi.",
        },
    ],
    "th": [
        {
            "angle": "warning",
            "title": "ถ้าธาตุ{dominant}แรงเกินไปในดวงของคุณ มีนิสัยหนึ่งอย่างที่กำลังบล็อก{theme}",
            "support": "คนที่มี day master เป็น{day_master}จะฟื้นตัวเมื่อพลัง{missing}กลับมาสมดุล",
            "cta": "บันทึกคลิปนี้ก่อนจังหวะดวงรอบถัดไปจะมา",
        },
        {
            "angle": "reveal",
            "title": "พลัง{missing}ที่อ่อน อาจเป็นเหตุผลลับที่ทำให้{theme}ของคุณยังไม่ไหล",
            "support": "เมื่อ{dominant}แรงเกินไปใน{season} จังหวะสำคัญกว่าการฝืน",
            "cta": "ติดตามไว้เพื่อดูสัญญาณซาจูคลิปถัดไป",
        },
        {
            "angle": "timing",
            "title": "คนที่มีธาตุ{dominant}เด่น กำลังเข้าสู่จุดรีเซ็ตครั้งใหญ่ของ{theme}",
            "support": "{balance_hint}ยิ่งต้องจัดพลังให้ตรง มากกว่าพยายามฝืนต่อ",
            "cta": "ถ้าสัญญาณเดิมกลับมา ให้ย้อนมาดูคลิปนี้อีกครั้ง",
        },
    ],
    "vi": [
        {
            "angle": "warning",
            "title": "Neu hanh {dominant} qua manh trong la so, co mot thoi quen dang chan {theme}.",
            "support": "Nguoi co ngay chu {day_master} se mo lai dong chay khi bo sung nang luong {missing}.",
            "cta": "Luu video nay truoc khi van may cua ban doi nhip.",
        },
        {
            "angle": "reveal",
            "title": "Nang luong {missing} yeu co the la ly do an sau khien {theme} cua ban bi dung.",
            "support": "Khi {dominant} qua manh vao {season}, dung nhin luc ma hay nhin dung thoi diem.",
            "cta": "Theo doi de xem tin hieu saju tiep theo.",
        },
        {
            "angle": "timing",
            "title": "Nguoi co hanh {dominant} manh sap buoc vao mot lan reset lon cua {theme}.",
            "support": "{balance_hint} co nghia la can can chinh thay vi theo duoi vo luc.",
            "cta": "Khi dau hieu lap lai, quay lai clip nay.",
        },
    ],
    "hi": [
        {
            "angle": "warning",
            "title": "अगर आपकी कुंडली में {dominant} बहुत हावी है, तो एक आदत आपकी {theme} रोक रही है।",
            "support": "{day_master} day master वाले लोग {missing} ऊर्जा लौटने पर फिर से खुलते हैं।",
            "cta": "अगले भाग्य मोड़ से पहले इसे सेव करें।",
        },
        {
            "angle": "reveal",
            "title": "कमज़ोर {missing} ऊर्जा ही शायद आपकी {theme} रुकने की छिपी वजह है।",
            "support": "{season} में जब {dominant} बहुत तेज़ हो, तब ज़ोर से ज़्यादा टाइमिंग काम करती है।",
            "cta": "अगला साजु सिग्नल पाने के लिए फॉलो करें।",
        },
        {
            "angle": "timing",
            "title": "जिनकी कुंडली में {dominant} बहुत मजबूत है, वे {theme} के बड़े रीसेट में प्रवेश कर रहे हैं।",
            "support": "{balance_hint} बताता है कि संतुलन बनाकर चलना, अंधी दौड़ से तेज़ जीत देता है।",
            "cta": "यही संकेत फिर दिखे तो इस वीडियो पर वापस आएँ।",
        },
    ],
}

BALANCE_HINTS = {
    "en": {
        "balanced": "A balanced chart",
        "yin-heavy": "A yin-heavy chart",
        "yang-heavy": "A yang-heavy chart",
    },
    "ko": {
        "balanced": "균형형 사주",
        "yin-heavy": "음 기운이 강한 사주",
        "yang-heavy": "양 기운이 강한 사주",
    },
    "ja": {
        "balanced": "バランス型の命式",
        "yin-heavy": "陰が強い命式",
        "yang-heavy": "陽が強い命式",
    },
    "id": {
        "balanced": "Chart yang seimbang",
        "yin-heavy": "Chart yang berat ke yin",
        "yang-heavy": "Chart yang berat ke yang",
    },
    "th": {
        "balanced": "ดวงที่สมดุล",
        "yin-heavy": "ดวงที่พลังหยินเด่น",
        "yang-heavy": "ดวงที่พลังหยางเด่น",
    },
    "vi": {
        "balanced": "La so can bang",
        "yin-heavy": "La so nghien ve am",
        "yang-heavy": "La so nghien ve duong",
    },
    "hi": {
        "balanced": "संतुलित कुंडली",
        "yin-heavy": "यिन प्रधान कुंडली",
        "yang-heavy": "यांग प्रधान कुंडली",
    },
}


def generate_hook_variants(
    profile: SajuProfile,
    language_code: str,
) -> list[HookVariant]:
    pack = get_language_pack(language_code)
    templates = TEMPLATES[pack.code]
    primary_theme = profile.focus_themes[0] if profile.focus_themes else "luck"
    balance_hint = BALANCE_HINTS[pack.code].get(
        profile.yin_yang_balance,
        BALANCE_HINTS[pack.code]["balanced"],
    )
    format_values = {
        "dominant": pack.element_names[profile.dominant_element],
        "missing": pack.element_names[profile.lacking_element],
        "day_master": pack.element_names[profile.day_master],
        "theme": pack.theme_names.get(primary_theme, primary_theme),
        "season": pack.season_names.get(profile.season, profile.season),
        "balance_hint": balance_hint,
    }

    variants: list[HookVariant] = []
    for index, template in enumerate(templates, start=1):
        title = template["title"].format(**format_values)
        support = template["support"].format(**format_values)
        cta = template["cta"].format(**format_values)
        narration = " ".join([title, support, cta]).strip()
        caption_lines = list(_build_captions([title, support, cta]))
        keywords = [
            profile.dominant_element,
            profile.lacking_element,
            profile.day_master,
            primary_theme,
            *profile.special_traits[:2],
        ]
        visual_motifs = list(ELEMENT_MOTIFS[profile.dominant_element])
        visual_motifs.extend(ELEMENT_MOTIFS[profile.lacking_element][:1])
        variants.append(
            HookVariant(
                variant_id=f"{pack.code}-v{index}",
                angle=template["angle"],
                title=title,
                support=support,
                cta=cta,
                narration=narration,
                caption_lines=caption_lines,
                keywords=[keyword for keyword in keywords if keyword],
                visual_motifs=visual_motifs,
            )
        )

    return variants


def _build_captions(parts: list[str]) -> Iterable[str]:
    for part in parts:
        for line in chunk_text(part, max_chars=34):
            yield line
