#!/usr/bin/env python3
"""
4K-Bildung Beispiel: Agile Softwareentwicklung
Demonstriert alle 4K-Aspekte mit Bildern und interaktiven Elementen
"""

import sys
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

from h5p_generator import (
    create_multi_choice, create_drag_drop, create_flashcards,
    create_accordion, create_summary, create_fill_blanks,
    create_mark_words, THEMES, H5PStyle, H5PGenerator
)
from h5p_media import download_image, get_illustration_url, embed_media_in_h5p

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


def create_agile_course():
    """Erstellt einen kompletten 4K-Kurs zu Agile"""

    print("=" * 60)
    print("4K-Bildung: Agile Softwareentwicklung")
    print("=" * 60)
    results = []

    # -------------------------------------------------------------------------
    # 1. ACCORDION: Einfuehrung mit Bildern (Wissensaufbau)
    # -------------------------------------------------------------------------
    print("\n1. Erstelle Accordion (Theorie-Einfuehrung)...")

    result = create_accordion(
        "Agile Methoden - Einfuehrung",
        [
            {
                "title": "Was ist Agile?",
                "content": """
                    <strong>Agile</strong> ist ein iterativer Ansatz fuer Projektmanagement
                    und Softwareentwicklung. Statt alles im Voraus zu planen, arbeiten
                    Teams in kurzen Zyklen (Sprints) und passen sich flexibel an.<br><br>
                    <em>4K-Tipp: Diskutiere mit deinem Nachbarn - wo hast du schon
                    agiles Arbeiten erlebt?</em>
                """
            },
            {
                "title": "Die 4 Werte des Agilen Manifests",
                "content": """
                    <ol>
                        <li><strong>Individuen und Interaktionen</strong> vor Prozessen und Werkzeugen</li>
                        <li><strong>Funktionierende Software</strong> vor umfassender Dokumentation</li>
                        <li><strong>Zusammenarbeit mit dem Kunden</strong> vor Vertragsverhandlung</li>
                        <li><strong>Reagieren auf Veraenderung</strong> vor Befolgen eines Plans</li>
                    </ol>
                    <em>Kreativ-Aufgabe: Formuliere einen 5. Wert, der dir wichtig waere!</em>
                """
            },
            {
                "title": "Scrum - Das bekannteste Framework",
                "content": """
                    Scrum organisiert Arbeit in <strong>Sprints</strong> (meist 2 Wochen).<br><br>
                    <strong>Rollen:</strong><br>
                    - Product Owner (Was wird gebaut?)<br>
                    - Scrum Master (Wie arbeiten wir zusammen?)<br>
                    - Development Team (Wer baut es?)<br><br>
                    <strong>Events:</strong><br>
                    Sprint Planning, Daily Standup, Sprint Review, Retrospektive
                """
            },
            {
                "title": "Kanban - Visualisiere den Workflow",
                "content": """
                    Kanban nutzt ein <strong>Board</strong> mit Spalten wie:<br>
                    To Do | In Progress | Review | Done<br><br>
                    <strong>Prinzipien:</strong><br>
                    - Visualisiere die Arbeit<br>
                    - Limitiere Work in Progress (WIP)<br>
                    - Fokussiere auf Flow<br><br>
                    <em>Kollaborations-Aufgabe: Erstellt gemeinsam ein Kanban-Board
                    fuer euer naechstes Gruppenprojekt!</em>
                """
            }
        ],
        "01-agile-einfuehrung",
        style=STYLE_4K
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 2. DRAG & DROP: Rollen zuordnen (Kritisches Denken)
    # -------------------------------------------------------------------------
    print("\n2. Erstelle Drag & Drop (Rollen-Zuordnung)...")

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
        "02-scrum-rollen",
        style=STYLE_4K
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 3. MULTIPLE CHOICE: Szenarien analysieren (Kritisches Denken)
    # -------------------------------------------------------------------------
    print("\n3. Erstelle Multiple Choice (Szenario-Analyse)...")

    result = create_multi_choice(
        "Agile Entscheidungen",
        [
            {
                "question": "Der Kunde moechte mitten im Sprint neue Features. Was tut ihr?",
                "answers": [
                    {"text": "Ins naechste Sprint Planning aufnehmen", "correct": True},
                    {"text": "Sofort einbauen, der Kunde hat immer Recht", "correct": False},
                    {"text": "Ablehnen - der Sprint ist heilig", "correct": False},
                    {"text": "Sprint abbrechen und neu planen", "correct": False}
                ]
            },
            {
                "question": "Das Daily Standup dauert regelmaessig 45 Minuten. Was ist das Problem?",
                "answers": [
                    {"text": "Es werden Probleme diskutiert statt nur Status geteilt", "correct": True},
                    {"text": "Das Team ist zu gross", "correct": False},
                    {"text": "Der Scrum Master ist nicht streng genug", "correct": False},
                    {"text": "45 Minuten sind normal bei komplexen Projekten", "correct": False}
                ]
            },
            {
                "question": "Welches Prinzip verfolgt Kanban hauptsaechlich?",
                "answers": [
                    {"text": "Kontinuierlicher Flow durch WIP-Limits", "correct": True},
                    {"text": "Feste Sprints mit klarem Ende", "correct": False},
                    {"text": "Taegliche Team-Meetings", "correct": False},
                    {"text": "Umfassende Dokumentation", "correct": False}
                ]
            }
        ],
        "03-agile-entscheidungen",
        style=STYLE_4K
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 4. FLASHCARDS: Begriffe lernen (Kommunikation)
    # -------------------------------------------------------------------------
    print("\n4. Erstelle Flashcards (Agile Vokabeln)...")

    result = create_flashcards(
        "Agile Begriffe",
        [
            {
                "front": "Sprint",
                "back": "Festgelegter Zeitraum (1-4 Wochen), in dem ein nutzbares Produktinkrement erstellt wird.",
                "tip": "Denk an einen kurzen Lauf"
            },
            {
                "front": "User Story",
                "back": "Anforderung aus Nutzersicht: 'Als [Rolle] moechte ich [Funktion], um [Nutzen]'",
                "tip": "Wer will was warum?"
            },
            {
                "front": "Backlog",
                "back": "Priorisierte Liste aller Anforderungen an das Produkt.",
                "tip": "Die Warteschlange der Arbeit"
            },
            {
                "front": "Velocity",
                "back": "Menge an Arbeit (Story Points), die ein Team pro Sprint schafft.",
                "tip": "Geschwindigkeit des Teams"
            },
            {
                "front": "Retrospektive",
                "back": "Meeting am Sprint-Ende: Was lief gut? Was koennen wir verbessern?",
                "tip": "Rueckblick zur Verbesserung"
            },
            {
                "front": "Definition of Done",
                "back": "Checkliste, wann eine Aufgabe als 'fertig' gilt (z.B. getestet, dokumentiert, deployed).",
                "tip": "Wann ist fertig wirklich fertig?"
            },
            {
                "front": "MVP",
                "back": "Minimum Viable Product - kleinstmoegliches Produkt mit echtem Kundennutzen.",
                "tip": "Start small, learn fast"
            },
            {
                "front": "WIP-Limit",
                "back": "Work in Progress Limit - maximale Anzahl paralleler Aufgaben pro Spalte/Person.",
                "tip": "Weniger gleichzeitig = mehr Fokus"
            }
        ],
        "04-agile-begriffe",
        style=STYLE_4K
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 5. SUMMARY: Kernaussagen identifizieren (Kritisches Denken)
    # -------------------------------------------------------------------------
    print("\n5. Erstelle Summary (Kernaussagen)...")

    result = create_summary(
        "Agile Kernprinzipien",
        [
            {
                "statements": [
                    "Agile Teams liefern regelmaessig funktionierende Software",
                    "Agile Teams dokumentieren zuerst alles, dann wird programmiert",
                    "Agile Teams arbeiten immer alleine ohne Kundenkontakt"
                ]
            },
            {
                "statements": [
                    "Ein Scrum Master schuetzt das Team vor Stoerungen",
                    "Ein Scrum Master weist dem Team Aufgaben zu",
                    "Ein Scrum Master programmiert den schwierigsten Code"
                ]
            },
            {
                "statements": [
                    "Kanban visualisiert den Arbeitsfluss auf einem Board",
                    "Kanban erfordert feste 2-Wochen-Sprints",
                    "Kanban verbietet jegliche Planung"
                ]
            },
            {
                "statements": [
                    "WIP-Limits verhindern Ueberlastung und verbessern den Flow",
                    "WIP-Limits bedeuten, dass jeder nur eine Aufgabe pro Jahr machen darf",
                    "WIP-Limits sind nur fuer Anfaenger wichtig"
                ]
            }
        ],
        "05-agile-kernprinzipien",
        intro="Waehle jeweils die korrekte Aussage. Die erste Aussage je Gruppe ist richtig.",
        style=STYLE_4K
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 6. FILL IN BLANKS: User Story schreiben (Kreativitaet + Kommunikation)
    # -------------------------------------------------------------------------
    print("\n6. Erstelle Fill in Blanks (User Story)...")

    result = create_fill_blanks(
        "User Story vervollstaendigen",
        """<p><strong>Vervollstaendige die User Story:</strong></p>
        <p>Als *Nutzer/Benutzer/User* moechte ich mich *einloggen/anmelden*,
        um auf meine persoenlichen *Daten/Informationen* zugreifen zu koennen.</p>
        <p><br></p>
        <p><strong>Noch eine:</strong></p>
        <p>Als *Administrator/Admin* moechte ich *Benutzer/Nutzer/User* verwalten,
        um *Zugriffsrechte/Berechtigungen* zu kontrollieren.</p>
        <p><br></p>
        <p><em>Kreativ-Bonus: Schreibe selbst eine User Story fuer eine App deiner Wahl!</em></p>
        """,
        "06-user-story",
        style=STYLE_4K
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # 7. MARK THE WORDS: Agile vs. Wasserfall (Kritisches Denken)
    # -------------------------------------------------------------------------
    print("\n7. Erstelle Mark the Words (Agile erkennen)...")

    result = create_mark_words(
        "Agile Prinzipien erkennen",
        """In einem agilen Projekt sind *Iterationen* und *Feedback* zentral.
        Das Team arbeitet in kurzen *Sprints* und haelt taeglich ein *Standup* ab.
        Lange Planungsphasen und umfassende Vorab-Dokumentation gehoeren zum Wasserfall-Modell.
        *Flexibilitaet* und *Kundennaehe* sind typisch agil.
        Starre Hierarchien und isolierte Abteilungen widersprechen dem agilen Gedanken.
        *Selbstorganisation* und *kontinuierliche Verbesserung* sind Kernprinzipien.""",
        "07-agile-erkennen",
        task="Markiere alle Begriffe, die typisch fuer agiles Arbeiten sind.",
        style=STYLE_4K
    )
    print(f"   {result}")
    results.append(result)

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    successful = sum(1 for r in results if r.success)
    print(f"Ergebnis: {successful}/{len(results)} H5P-Dateien erstellt")
    print(f"\nDateien in: {OUTPUT_DIR}")

    for f in sorted(OUTPUT_DIR.glob("*.h5p")):
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.1f} KB)")

    print("\n4K-Aspekte abgedeckt:")
    print("  [K] Kreativitaet: User Stories schreiben, eigene Werte formulieren")
    print("  [K] Kritisches Denken: Szenarien analysieren, Rollen zuordnen")
    print("  [K] Kommunikation: Begriffe erklaeren, Flashcards")
    print("  [K] Kollaboration: Diskussionsaufgaben, Gruppenarbeit-Hinweise")

    return results


if __name__ == "__main__":
    create_agile_course()
