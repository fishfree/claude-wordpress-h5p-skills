#!/usr/bin/env python3
"""Test: Interactive Book Generator"""

import zipfile
import json
from pathlib import Path
import shutil
from datetime import datetime

output_dir = Path('/home/claude/h5p-output')
output_name = 'interactive_book_test'
temp_dir = Path('/tmp') / f'h5p_{output_name}_{datetime.now().strftime("%H%M%S")}'
temp_dir.mkdir(parents=True, exist_ok=True)
(temp_dir / 'content').mkdir(exist_ok=True)

# Interactive Book Struktur mit echten interaktiven Elementen
content = {
    "showCoverPage": True,
    "bookCover": {
        "coverDescription": "<p>Eine interaktive Lerneinheit zu Scrum</p>",
        "coverImage": {},
        "coverMedium": {}
    },
    "title": "<p>Scrum Grundlagen</p>",
    "chapters": [
        {
            "title": "Kapitel 1: Einfuehrung",
            "params": {
                "content": [
                    {
                        "content": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {
                                "text": "<h2>Willkommen</h2><p>In diesem Buch lernst du die Grundlagen von Scrum.</p>"
                            },
                            "subContentId": "ch1-text",
                            "metadata": {"contentType": "Text", "license": "U", "title": "Intro"}
                        },
                        "useSeparator": "auto"
                    },
                    {
                        "content": {
                            "library": "H5P.Dialogcards 1.9",
                            "params": {
                                "title": "<p>Scrum Begriffe</p>",
                                "mode": "normal",
                                "description": "<p>Lerne die wichtigsten Begriffe</p>",
                                "dialogs": [
                                    {
                                        "text": "<p style=\"text-align:center;\">Sprint</p>",
                                        "answer": "<p style=\"text-align:center;\">Zeitbox von 2-4 Wochen</p>"
                                    },
                                    {
                                        "text": "<p style=\"text-align:center;\">Product Owner</p>",
                                        "answer": "<p style=\"text-align:center;\">Verantwortet das Product Backlog</p>"
                                    }
                                ],
                                "behaviour": {"enableRetry": True, "disableBackwardsNavigation": False},
                                "answer": "Umdrehen",
                                "next": "Weiter",
                                "prev": "Zurueck",
                                "retry": "Nochmal",
                                "correctAnswer": "Richtig!",
                                "incorrectAnswer": "Falsch",
                                "round": "Runde @round",
                                "cardsLeft": "Noch @number Karten",
                                "progressText": "@card von @total"
                            },
                            "subContentId": "ch1-cards",
                            "metadata": {"contentType": "Dialog Cards", "license": "U", "title": "Flashcards"}
                        },
                        "useSeparator": "auto"
                    }
                ]
            }
        },
        {
            "title": "Kapitel 2: Quiz",
            "params": {
                "content": [
                    {
                        "content": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {
                                "text": "<h2>Teste dein Wissen</h2><p>Fuelle die Luecken aus:</p>"
                            },
                            "subContentId": "ch2-text",
                            "metadata": {"contentType": "Text", "license": "U", "title": "Quiz Intro"}
                        },
                        "useSeparator": "auto"
                    },
                    {
                        "content": {
                            "library": "H5P.Blanks 1.14",
                            "params": {
                                "questions": "<p>Fuelle die Luecken aus:</p>",
                                "text": "<p>Ein *Sprint* ist eine *Zeitbox* von 2-4 Wochen. Der *Product Owner* verwaltet das Backlog.</p>",
                                "overallFeedback": [
                                    {"from": 0, "to": 50, "feedback": "Versuche es nochmal!"},
                                    {"from": 51, "to": 100, "feedback": "Gut gemacht!"}
                                ],
                                "showSolutions": "Loesung zeigen",
                                "tryAgain": "Nochmal",
                                "checkAnswer": "Pruefen",
                                "notFilledOut": "Bitte alle Luecken ausfuellen",
                                "behaviour": {
                                    "enableRetry": True,
                                    "enableSolutionsButton": True,
                                    "caseSensitive": False
                                }
                            },
                            "subContentId": "ch2-blanks",
                            "metadata": {"contentType": "Fill in the Blanks", "license": "U", "title": "Lueckentext"}
                        },
                        "useSeparator": "auto"
                    }
                ]
            }
        }
    ],
    "behaviour": {
        "defaultTableOfContents": True,
        "progressIndicators": True,
        "displaySummary": True
    },
    "l10n": {
        "nextPage": "Weiter",
        "previousPage": "Zurueck",
        "navigateToTop": "Nach oben",
        "fullscreen": "Vollbild",
        "exitFullscreen": "Vollbild beenden",
        "bookProgressSubtext": "@count von @total Seiten",
        "interactionsProgressSubtext": "@count von @total Interaktionen",
        "submitReport": "Absenden",
        "restartLabel": "Neustart",
        "summaryHeader": "Zusammenfassung",
        "allInteractions": "Alle Interaktionen",
        "unansweredInteractions": "Unbeantwortet",
        "scoreText": "Punkte:",
        "leftOfScore": "von",
        "noInteractions": "Keine Interaktionen",
        "score": "Punkte",
        "maxScore": "Max Punkte",
        "bookProgress": "Buchfortschritt",
        "interactionsProgress": "Interaktionen",
        "totalScoreLabel": "Gesamtpunkte"
    }
}

h5p_meta = {
    "title": "Scrum Grundlagen - Interactive Book",
    "language": "de",
    "mainLibrary": "H5P.InteractiveBook",
    "embedTypes": ["iframe"],
    "license": "CC BY",
    "preloadedDependencies": [
        {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
        {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
        {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
        {"machineName": "H5P.Dialogcards", "majorVersion": 1, "minorVersion": 9},
        {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14},
        {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5}
    ]
}

with open(temp_dir / 'content' / 'content.json', 'w', encoding='utf-8') as f:
    json.dump(content, f, ensure_ascii=False, indent=2)

with open(temp_dir / 'h5p.json', 'w', encoding='utf-8') as f:
    json.dump(h5p_meta, f, ensure_ascii=False, indent=2)

output_path = output_dir / f'{output_name}.h5p'
with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for file in (temp_dir / 'content').iterdir():
        zf.write(file, f'content/{file.name}')
    zf.write(temp_dir / 'h5p.json', 'h5p.json')

shutil.rmtree(temp_dir, ignore_errors=True)

print(f'Erstellt: {output_path}')
print()
print('Interactive Book mit:')
print('- Kapitel 1: Text + Flashcards (interaktiv)')
print('- Kapitel 2: Text + Lueckentext (interaktiv)')
print('- Inhaltsverzeichnis und Fortschrittsanzeige')
