#!/usr/bin/env python3
"""
H5P Media Helper - Bilder und Audio für H5P-Inhalte

Features:
- Bilder von URLs laden (undraw, unsplash, etc.)
- Audio via TTS generieren (Kokoro-Server)
- Medien in H5P-Pakete einbetten
"""

import os
import base64
import hashlib
import requests
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple
import json


# =============================================================================
# Configuration
# =============================================================================

# TTS Server (Kokoro on Hetzner)
TTS_URL = os.environ.get("TTS_URL", "https://tts.dirk-schulenburg.net")

# Image cache directory
CACHE_DIR = Path(os.environ.get("H5P_CACHE_DIR", "/tmp/h5p-media-cache"))

# Supported image formats
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.ogg', '.wav', '.m4a']


# =============================================================================
# Media Result Classes
# =============================================================================

@dataclass
class MediaFile:
    """Represents a media file for H5P embedding"""
    path: Path
    mime_type: str
    filename: str
    h5p_path: str  # Path within the H5P package (e.g., "images/intro.png")

    def to_h5p_reference(self) -> dict:
        """Returns H5P-compatible file reference"""
        return {
            "path": self.h5p_path,
            "mime": self.mime_type,
            "copyright": {"license": "U"}
        }


@dataclass
class ImageMedia(MediaFile):
    """Image file with dimensions"""
    width: int = 0
    height: int = 0
    alt_text: str = ""

    def to_h5p_image(self) -> dict:
        """Returns H5P-compatible image object"""
        return {
            "path": self.h5p_path,
            "mime": self.mime_type,
            "width": self.width,
            "height": self.height,
            "alt": self.alt_text,
            "copyright": {"license": "U"}
        }


@dataclass
class AudioMedia(MediaFile):
    """Audio file with duration"""
    duration_ms: int = 0
    text: str = ""  # Original text for TTS

    def to_h5p_audio(self) -> list:
        """Returns H5P-compatible audio array"""
        return [{
            "path": self.h5p_path,
            "mime": self.mime_type,
            "copyright": {"license": "U"}
        }]


# =============================================================================
# Image Functions
# =============================================================================

def get_mime_type(filename: str) -> str:
    """Determine MIME type from filename"""
    ext = Path(filename).suffix.lower()
    mime_map = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.webp': 'image/webp',
        '.mp3': 'audio/mpeg',
        '.ogg': 'audio/ogg',
        '.wav': 'audio/wav',
        '.m4a': 'audio/mp4'
    }
    return mime_map.get(ext, 'application/octet-stream')


def download_image(url: str, cache: bool = True) -> Optional[ImageMedia]:
    """
    Download an image from URL

    Args:
        url: Image URL
        cache: Whether to cache the image locally

    Returns:
        ImageMedia object or None on failure
    """
    try:
        # Generate cache filename from URL hash
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]

        # Determine extension from URL
        parsed_ext = Path(url.split('?')[0]).suffix.lower()
        if parsed_ext not in SUPPORTED_IMAGE_FORMATS:
            parsed_ext = '.png'  # Default

        cache_filename = f"img_{url_hash}{parsed_ext}"
        cache_path = CACHE_DIR / cache_filename

        # Check cache
        if cache and cache_path.exists():
            return ImageMedia(
                path=cache_path,
                mime_type=get_mime_type(cache_filename),
                filename=cache_filename,
                h5p_path=f"images/{cache_filename}"
            )

        # Download
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'H5P-Generator/2.0'
        })
        response.raise_for_status()

        # Ensure cache dir exists
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # Save to cache
        cache_path.write_bytes(response.content)

        # Try to get dimensions (requires PIL)
        width, height = 0, 0
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(response.content))
            width, height = img.size
        except ImportError:
            pass  # PIL not available
        except Exception:
            pass

        return ImageMedia(
            path=cache_path,
            mime_type=get_mime_type(cache_filename),
            filename=cache_filename,
            h5p_path=f"images/{cache_filename}",
            width=width,
            height=height
        )

    except Exception as e:
        print(f"[WARN] Image download failed: {e}")
        return None


def get_illustration_url(keyword: str, style: str = "illustration") -> Optional[str]:
    """
    Get an illustration URL from various sources

    Args:
        keyword: Search keyword (e.g., "learning", "teamwork")
        style: "illustration", "photo", "icon"

    Returns:
        Image URL or None
    """
    # Curated education-focused image URLs from reliable sources
    # Using Unsplash (reliable CDN) and picsum.photos for illustrations

    illustration_map = {
        # =====================================================================
        # UNSPLASH PHOTOS - Reliable CDN, high quality
        # These URLs are stable and work consistently
        # =====================================================================

        # Agile & Scrum (project/team focused)
        "scrum": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=500&fit=crop",
        "agile": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=500&fit=crop",
        "kanban": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=500&fit=crop",
        "sprint": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800&h=500&fit=crop",

        # Teamwork & Collaboration
        "teamwork": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&h=500&fit=crop",
        "collaboration": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&h=500&fit=crop",
        "team": "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=800&h=500&fit=crop",
        "meeting": "https://images.unsplash.com/photo-1531498860502-7c67cf02f657?w=800&h=500&fit=crop",
        "discussion": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=500&fit=crop",

        # Learning & Education
        "learning": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=500&fit=crop",
        "education": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&h=500&fit=crop",
        "teaching": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800&h=500&fit=crop",
        "student": "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=800&h=500&fit=crop",
        "reading": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&h=500&fit=crop",
        "studying": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=500&fit=crop",
        "knowledge": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&h=500&fit=crop",
        "school": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&h=500&fit=crop",
        "exam": "https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?w=800&h=500&fit=crop",
        "quiz": "https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?w=800&h=500&fit=crop",

        # Communication
        "communication": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=800&h=500&fit=crop",
        "presentation": "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=500&fit=crop",

        # Creativity & Thinking
        "creativity": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800&h=500&fit=crop",
        "idea": "https://images.unsplash.com/photo-1493612276216-ee3925520721?w=800&h=500&fit=crop",
        "brainstorm": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800&h=500&fit=crop",
        "thinking": "https://images.unsplash.com/photo-1453847668862-487637052f8a?w=800&h=500&fit=crop",
        "problem_solving": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=500&fit=crop",

        # Technology & Programming
        "coding": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=500&fit=crop",
        "programming": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&h=500&fit=crop",
        "computer": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&h=500&fit=crop",
        "technology": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=500&fit=crop",
        "data": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=500&fit=crop",

        # Project Management
        "project": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=500&fit=crop",
        "planning": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800&h=500&fit=crop",
        "tasks": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=500&fit=crop",
        "workflow": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800&h=500&fit=crop",

        # General / Positive
        "success": "https://images.unsplash.com/photo-1552508744-1696d4464960?w=800&h=500&fit=crop",
        "goal": "https://images.unsplash.com/photo-1533227268428-f9ed0900fb3b?w=800&h=500&fit=crop",
        "progress": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=500&fit=crop",
        "question": "https://images.unsplash.com/photo-1484069560501-87d72b0c3669?w=800&h=500&fit=crop",
        "choice": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=500&fit=crop",
        "organize": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=500&fit=crop",

        # Default
        "default": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=500&fit=crop"
    }

    # Find matching image
    keyword_lower = keyword.lower().replace(" ", "_").replace("-", "_")
    url = illustration_map.get(keyword_lower)

    if not url:
        # Try partial match
        for key, img_url in illustration_map.items():
            if key in keyword_lower or keyword_lower in key:
                url = img_url
                break

    if not url:
        url = illustration_map["default"]

    return url


# Alias for backwards compatibility
def get_undraw_image(keyword: str, color: str = "6366f1") -> Optional[str]:
    """Alias for get_illustration_url"""
    return get_illustration_url(keyword)


# =============================================================================
# Audio Functions (TTS)
# =============================================================================

def generate_tts_audio(
    text: str,
    voice: str = "af_sarah",
    speed: float = 1.0,
    cache: bool = True
) -> Optional[AudioMedia]:
    """
    Generate audio from text using Kokoro TTS

    Args:
        text: Text to convert to speech
        voice: Voice ID (af_sarah, af_nicole, am_michael, etc.)
        speed: Speech speed (0.5-2.0)
        cache: Whether to cache the audio

    Returns:
        AudioMedia object or None on failure
    """
    try:
        # Generate cache filename from text hash
        text_hash = hashlib.md5(f"{text}_{voice}_{speed}".encode()).hexdigest()[:12]
        cache_filename = f"audio_{text_hash}.mp3"
        cache_path = CACHE_DIR / cache_filename

        # Check cache
        if cache and cache_path.exists():
            return AudioMedia(
                path=cache_path,
                mime_type="audio/mpeg",
                filename=cache_filename,
                h5p_path=f"audios/{cache_filename}",
                text=text
            )

        # Call TTS API (OpenAI-compatible endpoint)
        response = requests.post(
            f"{TTS_URL}/v1/audio/speech",
            json={
                "model": "kokoro",
                "input": text,
                "voice": voice,
                "speed": speed,
                "response_format": "mp3"
            },
            timeout=60,
            headers={
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()

        # Ensure cache dir exists
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # Save to cache
        cache_path.write_bytes(response.content)

        return AudioMedia(
            path=cache_path,
            mime_type="audio/mpeg",
            filename=cache_filename,
            h5p_path=f"audios/{cache_filename}",
            text=text
        )

    except Exception as e:
        print(f"[WARN] TTS generation failed: {e}")
        return None


# =============================================================================
# H5P Media Embedding
# =============================================================================

def embed_media_in_h5p(temp_dir: Path, media_files: list) -> dict:
    """
    Embed media files in H5P package structure

    Args:
        temp_dir: Temporary H5P build directory
        media_files: List of MediaFile objects

    Returns:
        Dict of embedded file references
    """
    embedded = {"images": [], "audios": []}

    for media in media_files:
        if media is None:
            continue

        # Determine target directory
        if isinstance(media, ImageMedia):
            target_dir = temp_dir / "content" / "images"
            embedded["images"].append(media)
        elif isinstance(media, AudioMedia):
            target_dir = temp_dir / "content" / "audios"
            embedded["audios"].append(media)
        else:
            target_dir = temp_dir / "content" / "files"

        # Create directory and copy file
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / media.filename

        if media.path.exists():
            import shutil
            shutil.copy2(media.path, target_path)

    return embedded


# =============================================================================
# 4K Education Helpers
# =============================================================================

def get_4k_prompt(aspect: str, topic: str) -> str:
    """
    Generate a 4K-focused learning prompt

    Args:
        aspect: One of "creativity", "critical_thinking", "communication", "collaboration"
        topic: The learning topic

    Returns:
        A pedagogically designed prompt
    """
    prompts = {
        "creativity": [
            f"Wie wuerdest du {topic} auf eine voellig neue Art erklaeren?",
            f"Erfinde eine kreative Loesung fuer ein Problem mit {topic}.",
            f"Stelle dir vor, {topic} gaebe es nicht - was waere anders?"
        ],
        "critical_thinking": [
            f"Welche Annahmen stecken hinter {topic}? Sind sie alle richtig?",
            f"Vergleiche verschiedene Perspektiven auf {topic}.",
            f"Was sind Staerken und Schwaechen von {topic}?"
        ],
        "communication": [
            f"Erklaere {topic} so, dass ein 10-Jaehriger es versteht.",
            f"Wie wuerdest du {topic} in einem Tweet zusammenfassen?",
            f"Erstelle eine Praesentation ueber {topic} mit 3 Kernpunkten."
        ],
        "collaboration": [
            f"Wie koennte ein Team gemeinsam {topic} erforschen?",
            f"Welche Rollen brauchte man, um {topic} umzusetzen?",
            f"Diskutiert in der Gruppe: Was ist das Wichtigste an {topic}?"
        ]
    }

    import random
    aspect_prompts = prompts.get(aspect.lower(), prompts["critical_thinking"])
    return random.choice(aspect_prompts)


def get_4k_feedback(aspect: str, correct: bool) -> str:
    """
    Generate 4K-appropriate feedback
    """
    if correct:
        feedback = {
            "creativity": "Kreative Antwort! Du denkst ueber den Tellerrand hinaus.",
            "critical_thinking": "Gut analysiert! Du hinterfragst kritisch.",
            "communication": "Klar formuliert! So versteht es jeder.",
            "collaboration": "Teamgeist! Zusammen erreicht man mehr."
        }
    else:
        feedback = {
            "creativity": "Versuch es nochmal mit einem anderen Blickwinkel!",
            "critical_thinking": "Denk nochmal darueber nach - was uebersieht man leicht?",
            "communication": "Wie koenntest du es anders ausdruecken?",
            "collaboration": "Frag einen Mitschueler - gemeinsam findet ihr die Loesung!"
        }

    return feedback.get(aspect.lower(), feedback["critical_thinking"])


# =============================================================================
# Test
# =============================================================================

if __name__ == "__main__":
    print("H5P Media Helper - Test")
    print("=" * 50)

    # Test undraw URL
    print("\n1. Undraw Image URL:")
    url = get_undraw_image("learning")
    print(f"   {url}")

    # Test image download
    print("\n2. Image Download:")
    img = download_image(url)
    if img:
        print(f"   [OK] {img.filename} ({img.mime_type})")
    else:
        print("   [SKIP] Download failed or network unavailable")

    # Test TTS (only if server available)
    print("\n3. TTS Generation:")
    try:
        audio = generate_tts_audio("Dies ist ein Test.", cache=False)
        if audio:
            print(f"   [OK] {audio.filename}")
        else:
            print("   [SKIP] TTS server not available")
    except Exception as e:
        print(f"   [SKIP] {e}")

    # Test 4K prompts
    print("\n4. 4K Prompts:")
    for aspect in ["creativity", "critical_thinking", "communication", "collaboration"]:
        prompt = get_4k_prompt(aspect, "Python-Programmierung")
        print(f"   {aspect}: {prompt[:50]}...")

    print("\n" + "=" * 50)
    print("Test abgeschlossen!")
