#!/usr/bin/env python3
import zipfile
import json
from pathlib import Path

content = {
    "showCoverPage": False,
    "bookCover": {"coverDescription": "", "coverImage": {}, "coverMedium": {}},
    "title": "<p>Drag the Words Test</p>",
    "chapters": [
        {
            "title": "Woerter einsetzen",
            "params": {
                "content": [
                    {
                        "content": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {"text": "<h2>Drag the Words</h2><p>Ziehe die Woerter an die richtige Stelle:</p>"},
                            "subContentId": "intro",
                            "metadata": {"contentType": "Text", "license": "U", "title": "Intro"}
                        },
                        "useSeparator": "auto"
                    },
                    {
                        "content": {
                            "library": "H5P.DragText 1.10",
                            "params": {
                                "taskDescription": "<p>Ziehe die Woerter in die Luecken:</p>",
                                "textField": "Ein *Sprint* dauert 2-4 *Wochen*. Der *Product Owner* verwaltet das Backlog.",
                                "overallFeedback": [{"from": 0, "to": 100, "feedback": "Fertig!"}],
                                "checkAnswer": "Pruefen",
                                "tryAgain": "Nochmal",
                                "showSolution": "Loesung",
                                "dropZoneIndex": "Dropzone @index",
                                "empty": "Dropzone @index ist leer",
                                "contains": "Dropzone @index enthaelt",
                                "ariaDraggableIndex": "@index von @count",
                                "tipLabel": "Tipp",
                                "correctText": "Richtig!",
                                "incorrectText": "Falsch!",
                                "resetDropTitle": "Zuruecksetzen",
                                "resetDropDescription": "Willst du zuruecksetzen?",
                                "grabbed": "Gezogen",
                                "cancelledDragging": "Abgebrochen",
                                "correctAnswer": "Richtige Antwort",
                                "feedbackHeader": "Feedback",
                                "behaviour": {
                                    "enableRetry": True,
                                    "enableSolutionsButton": True,
                                    "enableCheckButton": True,
                                    "instantFeedback": False
                                }
                            },
                            "subContentId": "dragtext1",
                            "metadata": {"contentType": "Drag the Words", "license": "U", "title": "DragText"}
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
    "title": "Drag the Words Test",
    "language": "de",
    "mainLibrary": "H5P.InteractiveBook",
    "embedTypes": ["iframe"],
    "license": "U",
    "preloadedDependencies": [
        {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
        {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
        {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
        {"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 10}
    ]
}

output = Path('/home/claude/h5p-output/book_test_dragtext.h5p')
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False))
    zf.writestr('h5p.json', json.dumps(h5p, ensure_ascii=False))

print(f'Erstellt: {output}')
