#!/usr/bin/env python3
"""
H5P Generator v2.0 - Test Suite
Testet alle 9 Content Types mit Fehlerbehandlung
"""

import sys
import os
from pathlib import Path

# Importiere den Generator
from h5p_generator import (
    create_true_false, create_multi_choice, create_fill_blanks,
    create_drag_drop, create_single_choice, create_flashcards,
    create_mark_words, create_summary, create_accordion,
    batch_create, THEMES, H5PStyle, H5PGenerator
)


def run_tests():
    """Führt alle Tests aus"""

    # Override output directory for Windows
    test_output = Path(__file__).parent.parent / "test-output"
    test_output.mkdir(exist_ok=True)

    # Monkey-patch the output directory
    H5PGenerator.__init__.__defaults__ = (str(test_output), None)

    print("=" * 60)
    print("H5P Generator v2.0 - Test Suite")
    print("=" * 60)
    print(f"Output: {test_output}")
    print()

    style = THEMES['education']
    results = []

    # -------------------------------------------------------------------------
    # 1. True/False
    # -------------------------------------------------------------------------
    print("1. True/False Quiz...")
    result = create_true_false(
        "Python Grundlagen",
        [
            {"text": "Python ist eine interpretierte Sprache.", "correct": True},
            {"text": "Python wurde 2020 veröffentlicht.", "correct": False},
            {"text": "Python unterstützt OOP.", "correct": True}
        ],
        "test-truefalse",
        style=style
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 2. Multiple Choice
    # -------------------------------------------------------------------------
    print("2. Multiple Choice Quiz...")
    result = create_multi_choice(
        "Hauptstädte Quiz",
        [
            {
                "question": "Was ist die Hauptstadt von Deutschland?",
                "answers": [
                    {"text": "Berlin", "correct": True},
                    {"text": "Hamburg", "correct": False},
                    {"text": "München", "correct": False},
                    {"text": "Köln", "correct": False}
                ]
            },
            {
                "question": "Was ist die Hauptstadt von Frankreich?",
                "answers": [
                    {"text": "Paris", "correct": True},
                    {"text": "Lyon", "correct": False},
                    {"text": "Marseille", "correct": False}
                ]
            }
        ],
        "test-multichoice",
        style=style
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 3. Fill in Blanks
    # -------------------------------------------------------------------------
    print("3. Fill in Blanks (Lückentext)...")
    result = create_fill_blanks(
        "Deutschland Fakten",
        "<p>Die Hauptstadt von Deutschland ist *Berlin*.</p><p>Die Währung ist der *Euro/EUR*.</p><p>Das Land hat *16* Bundesländer.</p>",
        "test-blanks",
        style=style
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 4. Drag and Drop
    # -------------------------------------------------------------------------
    print("4. Drag and Drop...")
    result = create_drag_drop(
        "Lebensmittel sortieren",
        "Ordne die Lebensmittel den richtigen Kategorien zu.",
        ["Obst", "Gemüse", "Getränk"],
        [
            {"text": "Apfel", "dropzone": 0},
            {"text": "Karotte", "dropzone": 1},
            {"text": "Wasser", "dropzone": 2},
            {"text": "Banane", "dropzone": 0},
            {"text": "Brokkoli", "dropzone": 1},
            {"text": "Saft", "dropzone": 2}
        ],
        "test-dragdrop",
        style=style
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 5. Single Choice Set
    # -------------------------------------------------------------------------
    print("5. Single Choice Set...")
    result = create_single_choice(
        "Mathe Quick Quiz",
        [
            {"question": "Was ist 2 + 2?", "answers": ["4", "3", "5", "6"]},
            {"question": "Was ist 5 x 5?", "answers": ["25", "20", "30", "15"]},
            {"question": "Was ist 10 / 2?", "answers": ["5", "4", "6", "3"]}
        ],
        "test-singlechoice",
        style=style
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 6. Flashcards
    # -------------------------------------------------------------------------
    print("6. Flashcards (Lernkarten)...")
    result = create_flashcards(
        "Englisch Vokabeln",
        [
            {"front": "Haus", "back": "house", "tip": "Beginnt mit H"},
            {"front": "Auto", "back": "car"},
            {"front": "Baum", "back": "tree"},
            {"front": "Hund", "back": "dog"},
            {"front": "Katze", "back": "cat"}
        ],
        "test-flashcards",
        style=style
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 7. Mark the Words
    # -------------------------------------------------------------------------
    print("7. Mark the Words...")
    result = create_mark_words(
        "Geografie Wörter",
        "Berlin ist die *Hauptstadt* von *Deutschland*. Hamburg ist eine *Hafenstadt*. Paris liegt in Frankreich.",
        "test-markwords",
        task="Markiere alle Begriffe, die zu Deutschland gehören.",
        style=style
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 8. Summary
    # -------------------------------------------------------------------------
    print("8. Summary...")
    result = create_summary(
        "Python Facts",
        [
            {
                "statements": [
                    "Python ist eine interpretierte Sprache",
                    "Python ist eine kompilierte Sprache",
                    "Python ist Assembler"
                ]
            },
            {
                "statements": [
                    "Python hat dynamische Typisierung",
                    "Python hat statische Typisierung",
                    "Python hat keine Typisierung"
                ]
            },
            {
                "statements": [
                    "Python wurde von Guido van Rossum entwickelt",
                    "Python wurde von Linus Torvalds entwickelt",
                    "Python wurde von Bill Gates entwickelt"
                ]
            }
        ],
        "test-summary",
        intro="Wähle jeweils die korrekte Aussage über Python.",
        style=style
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 9. Accordion
    # -------------------------------------------------------------------------
    print("9. Accordion...")
    result = create_accordion(
        "Python Tutorial",
        [
            {"title": "Einführung", "content": "Python ist eine vielseitige Programmiersprache, die 1991 von Guido van Rossum entwickelt wurde."},
            {"title": "Variablen", "content": "Variablen in Python werden einfach durch Zuweisung erstellt: x = 5"},
            {"title": "Funktionen", "content": "Funktionen werden mit def definiert: def meine_funktion():"},
            {"title": "Klassen", "content": "Klassen ermöglichen objektorientierte Programmierung: class MeineKlasse:"}
        ],
        "test-accordion",
        style=style
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # Fehlerbehandlung Tests
    # -------------------------------------------------------------------------
    print()
    print("-" * 60)
    print("Fehlerbehandlung Tests:")
    print("-" * 60)

    # Leere Fragenliste
    print("10. Leere Fragenliste (sollte Fehler zeigen)...")
    result = create_true_false("Leerer Test", [], "test-empty")
    print(f"    {result}")
    results.append(result)

    # Fehlende Pflichtfelder
    print("11. Fehlende Antwort-Markierung (sollte Fehler zeigen)...")
    result = create_multi_choice(
        "Bad Quiz",
        [{"question": "Was?", "answers": [{"text": "A"}, {"text": "B"}]}],  # keine correct-Markierung
        "test-bad"
    )
    print(f"    {result}")
    results.append(result)

    # Keine Lücken im Text
    print("12. Lückentext ohne Lücken (sollte Fehler zeigen)...")
    result = create_fill_blanks("No Blanks", "Text ohne Lücken", "test-noblanks")
    print(f"    {result}")
    results.append(result)

    # Ungültige Dropzone
    print("13. Ungültige Dropzone-Index (sollte Fehler zeigen)...")
    result = create_drag_drop(
        "Bad Drag",
        "Test",
        ["Zone1"],
        [{"text": "Item", "dropzone": 5}],  # Index 5 existiert nicht
        "test-baddrag"
    )
    print(f"    {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # Batch Creation Test
    # -------------------------------------------------------------------------
    print()
    print("-" * 60)
    print("Batch Creation Test:")
    print("-" * 60)

    batch_content = [
        {
            "type": "true_false",
            "title": "Batch Quiz 1",
            "questions": [{"text": "Test", "correct": True}]
        },
        {
            "type": "flashcards",
            "title": "Batch Vokabeln",
            "cards": [{"front": "Hallo", "back": "Hello"}]
        },
        {
            "type": "unknown_type",  # Sollte Fehler geben
            "title": "Bad Type"
        }
    ]

    batch_results = batch_create(batch_content, style=THEMES['professional'])
    for br in batch_results:
        print(f"    {br}")
        results.append(br)

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print()
    print("=" * 60)
    successful = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)

    print(f"Ergebnis: {successful} erfolgreich, {failed} fehlgeschlagen (erwartet)")
    print()

    # Liste erstellte Dateien
    h5p_files = list(test_output.glob("*.h5p"))
    if h5p_files:
        print("Erstellte H5P-Dateien:")
        for f in sorted(h5p_files):
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name} ({size_kb:.1f} KB)")

    print()
    print("=" * 60)
    print("Tests abgeschlossen!")

    return successful >= 9  # Mindestens 9 Content Types sollten funktionieren


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
