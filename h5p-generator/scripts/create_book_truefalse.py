#!/usr/bin/env python3
import zipfile
import json
from pathlib import Path

# Buch mit Flashcards + True/False
content = {
    "showCoverPage": False,
    "bookCover": {"coverDescription": "", "coverImage": {}, "coverMedium": {}},
    "title": "<p>Scrum Lernbuch</p>",
    "chapters": [
        {
            "title": "Kapitel 1: Begriffe",
            "params": {
                "content": [
                    {
                        "content": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {"text": "<h2>Scrum Begriffe</h2><p>Lerne mit Lernkarten:</p>"},
                            "subContentId": "ch1-text",
                            "metadata": {"contentType": "Text", "license": "U", "title": "Intro"}
                        },
                        "useSeparator": "auto"
                    },
                    {
                        "content": {
                            "library": "H5P.Dialogcards 1.9",
                            "params": {
                                "dialogs": [
                                    {"text": "<p>Sprint</p>", "answer": "<p>Zeitbox von 2-4 Wochen</p>"},
                                    {"text": "<p>Product Owner</p>", "answer": "<p>Verwaltet das Backlog</p>"},
                                    {"text": "<p>Scrum Master</p>", "answer": "<p>Coacht das Team</p>"}
                                ],
                                "behaviour": {"enableRetry": True, "disableBackwardsNavigation": False}
                            },
                            "subContentId": "ch1-cards",
                            "metadata": {"contentType": "Dialog Cards", "license": "U", "title": "Cards"}
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
                            "params": {"text": "<h2>Wahr oder Falsch?</h2><p>Teste dein Wissen:</p>"},
                            "subContentId": "ch2-text",
                            "metadata": {"contentType": "Text", "license": "U", "title": "Intro"}
                        },
                        "useSeparator": "auto"
                    },
                    {
                        "content": {
                            "library": "H5P.TrueFalse 1.8",
                            "params": {
                                "question": "<p>Ein Sprint dauert maximal 4 Wochen.</p>",
                                "correct": "true",
                                "behaviour": {"enableRetry": True, "enableSolutionsButton": True},
                                "l10n": {"trueText": "Wahr", "falseText": "Falsch", "checkAnswer": "Pruefen", "showSolutionButton": "Loesung", "tryAgain": "Nochmal"}
                            },
                            "subContentId": "ch2-tf1",
                            "metadata": {"contentType": "True/False Question", "license": "U", "title": "TF1"}
                        },
                        "useSeparator": "auto"
                    },
                    {
                        "content": {
                            "library": "H5P.TrueFalse 1.8",
                            "params": {
                                "question": "<p>Der Product Owner schreibt den Code.</p>",
                                "correct": "false",
                                "behaviour": {"enableRetry": True, "enableSolutionsButton": True},
                                "l10n": {"trueText": "Wahr", "falseText": "Falsch", "checkAnswer": "Pruefen", "showSolutionButton": "Loesung", "tryAgain": "Nochmal"}
                            },
                            "subContentId": "ch2-tf2",
                            "metadata": {"contentType": "True/False Question", "license": "U", "title": "TF2"}
                        },
                        "useSeparator": "auto"
                    }
                ]
            }
        }
    ],
    "behaviour": {"defaultTableOfContents": True, "progressIndicators": True, "displaySummary": True},
    "l10n": {
        "nextPage": "Weiter", "previousPage": "Zurueck", "navigateToTop": "Oben",
        "fullscreen": "Vollbild", "exitFullscreen": "Beenden",
        "bookProgressSubtext": "@count von @total", "interactionsProgressSubtext": "@count von @total",
        "submitReport": "OK", "restartLabel": "Neu", "summaryHeader": "Ende",
        "allInteractions": "Alle", "unansweredInteractions": "Offen",
        "scoreText": "Punkte:", "leftOfScore": "von", "noInteractions": "Keine",
        "score": "Punkte", "maxScore": "Max", "bookProgress": "Fortschritt",
        "interactionsProgress": "Interaktionen", "totalScoreLabel": "Gesamt"
    }
}

h5p = {
    "title": "Scrum Lernbuch",
    "language": "de",
    "mainLibrary": "H5P.InteractiveBook",
    "embedTypes": ["iframe"],
    "license": "U",
    "preloadedDependencies": [
        {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
        {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
        {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
        {"machineName": "H5P.Dialogcards", "majorVersion": 1, "minorVersion": 9},
        {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8}
    ]
}

output = Path('/home/claude/h5p-output/book_flashcards_truefalse.h5p')
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False))
    zf.writestr('h5p.json', json.dumps(h5p, ensure_ascii=False))

print(f'Erstellt: {output}')
print('Kapitel 1: Flashcards (3 Karten)')
print('Kapitel 2: Wahr/Falsch Quiz (2 Fragen)')
