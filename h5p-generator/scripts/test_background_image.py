#!/usr/bin/env python3
"""
Test: Drag & Drop mit Hintergrundbild (v10)
"""

import sys
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

from h5p_generator import create_drag_drop, H5PStyle, H5PGenerator
from h5p_media import get_illustration_url

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "test-output" / "4k-beispiele"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
H5PGenerator.__init__.__defaults__ = (str(OUTPUT_DIR), None)

# Custom 4K Education Style
STYLE_4K = H5PStyle(
    primary_color="#4f46e5",      # Indigo
    success_color="#10b981",      # Emerald
    error_color="#ef4444",        # Red
    feedback_correct="Sehr gut! Du hast kritisch gedacht und die richtige Loesung gefunden.",
    feedback_wrong="Nicht ganz - diskutiere mit einem Partner und versuche es nochmal!",
    feedback_partial="Fast! Ueberlege kreativ, was noch fehlen koennte.",
    pass_percentage=70
)

def create_scrum_drag_drop_v10():
    """Erstellt Drag & Drop mit Hintergrundbild"""

    print("=" * 60)
    print("Test: Drag & Drop mit Hintergrundbild (v10)")
    print("=" * 60)

    # Hintergrundbild von undraw-style SVG
    bg_url = get_illustration_url("scrum")
    print(f"\nHintergrundbild: {bg_url}")

    # Alternative: Teamwork-Bild
    # bg_url = get_illustration_url("teamwork")

    result = create_drag_drop(
        "Scrum-Rollen zuordnen",
        "Ordne die Aufgaben den richtigen Scrum-Rollen zu. Ueberlege kritisch!",
        ["Product Owner", "Scrum Master", "Dev Team"],
        [
            {"text": "Priorisiert das Backlog", "dropzone": 0},
            {"text": "Entfernt Hindernisse", "dropzone": 1},
            {"text": "Implementiert Features", "dropzone": 2},
            {"text": "Definiert User Stories", "dropzone": 0},
            {"text": "Moderiert Retrospektive", "dropzone": 1},
            {"text": "Schaetzt Aufwaende", "dropzone": 2},
            {"text": "Vertritt Kundenwuensche", "dropzone": 0},
            {"text": "Schuetzt das Team", "dropzone": 1},
            {"text": "Testet die Software", "dropzone": 2}
        ],
        "02-scrum-rollen-v10",
        style=STYLE_4K,
        background_image=bg_url
    )

    print(f"\nErgebnis: {result}")

    if result.success:
        print(f"\nDatei erstellt: {result.path}")
        size_kb = result.path.stat().st_size / 1024
        print(f"Groesse: {size_kb:.1f} KB")
    else:
        print(f"\nFehler: {result.error}")

    return result


if __name__ == "__main__":
    create_scrum_drag_drop_v10()
