from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from shortsmaker.languages import LanguagePack, get_language_pack


@dataclass(frozen=True)
class TtsArtifact:
    provider: str
    voice: str
    output_path: str
    duration_seconds: float

    def to_dict(self) -> dict[str, object]:
        return {
            "provider": self.provider,
            "voice": self.voice,
            "output_path": self.output_path,
            "duration_seconds": round(self.duration_seconds, 2),
        }


class TtsProvider(Protocol):
    name: str

    def voice_for(self, language_code: str) -> str: ...

    def synthesize(
        self,
        text: str,
        language_code: str,
        output_path: Path,
    ) -> TtsArtifact: ...


class EdgeTtsProvider:
    name = "edge"

    def voice_for(self, language_code: str) -> str:
        return get_language_pack(language_code).edge_voice

    def synthesize(
        self,
        text: str,
        language_code: str,
        output_path: Path,
    ) -> TtsArtifact:
        try:
            import edge_tts
        except ImportError as exc:
            raise RuntimeError(
                "edge-tts is not installed. Run `python -m pip install -e .` first."
            ) from exc

        voice = self.voice_for(language_code)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        async def _run() -> None:
            communicator = edge_tts.Communicate(text=text, voice=voice)
            await communicator.save(str(output_path))

        asyncio.run(_run())
        duration_seconds = _mp3_duration(output_path)
        return TtsArtifact(
            provider=self.name,
            voice=voice,
            output_path=str(output_path),
            duration_seconds=duration_seconds,
        )


class AzureSpeechProvider:
    name = "azure"

    def __init__(self) -> None:
        self._speech_key = os.getenv("AZURE_SPEECH_KEY")
        self._speech_region = os.getenv("AZURE_SPEECH_REGION")
        if not self._speech_key or not self._speech_region:
            raise RuntimeError(
                "Azure Speech requires AZURE_SPEECH_KEY and AZURE_SPEECH_REGION."
            )

    def voice_for(self, language_code: str) -> str:
        return get_language_pack(language_code).azure_voice

    def synthesize(
        self,
        text: str,
        language_code: str,
        output_path: Path,
    ) -> TtsArtifact:
        try:
            import azure.cognitiveservices.speech as speechsdk
        except ImportError as exc:
            raise RuntimeError(
                "Azure Speech SDK is not installed. Run `python -m pip install -e .[azure]`."
            ) from exc

        voice = self.voice_for(language_code)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        speech_config = speechsdk.SpeechConfig(
            subscription=self._speech_key,
            region=self._speech_region,
        )
        speech_config.speech_synthesis_voice_name = voice
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3
        )
        audio_config = speechsdk.audio.AudioOutputConfig(filename=str(output_path))
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )
        result = synthesizer.speak_text_async(text).get()

        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise RuntimeError("Azure Speech synthesis failed.")

        return TtsArtifact(
            provider=self.name,
            voice=voice,
            output_path=str(output_path),
            duration_seconds=_mp3_duration(output_path),
        )


def create_tts_provider(name: str) -> TtsProvider:
    normalized = name.strip().lower()
    if normalized == "edge":
        return EdgeTtsProvider()
    if normalized == "azure":
        return AzureSpeechProvider()
    raise ValueError(f"Unsupported TTS provider: {name}")


def voice_catalog(language_code: str) -> dict[str, str]:
    pack: LanguagePack = get_language_pack(language_code)
    return {
        "edge": pack.edge_voice,
        "azure": pack.azure_voice,
    }


def _mp3_duration(path: Path) -> float:
    from mutagen.mp3 import MP3

    return float(MP3(path).info.length)
