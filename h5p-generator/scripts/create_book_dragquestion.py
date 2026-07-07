#!/usr/bin/env python3
import zipfile
import json
from pathlib import Path

content = {
    "showCoverPage": False,
    "bookCover": {"coverDescription": "", "coverImage": {}, "coverMedium": {}},
    "title": "<p>Drag Question Test</p>",
    "chapters": [
        {
            "title": "Drag and Drop",
            "params": {
                "content": [
                    {
                        "content": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {"text": "<h2>Zuordnung</h2><p>Ziehe die Begriffe in die richtige Kategorie:</p>"},
                            "subContentId": "intro",
                            "metadata": {"contentType": "Text", "license": "U", "title": "Intro"}
                        },
                        "useSeparator": "auto"
                    },
                    {
                        "content": {
                            "library": "H5P.DragQuestion 1.14",
                            "params": {
                                "scoreShow": "Loesung zeigen",
                                "tryAgain": "Nochmal",
                                "checkAnswer": "Pruefen",
                                "behaviour": {
                                    "enableRetry": True,
                                    "enableCheckButton": True,
                                    "showSolutionsRequiresInput": True,
                                    "singlePoint": False,
                                    "applyPenalties": False,
                                    "enableScoreExplanation": True,
                                    "dropZoneHighlighting": "dragging",
                                    "autoAlignSpacing": 2,
                                    "enableFullScreen": False,
                                    "showScorePoints": True,
                                    "showTitle": True
                                },
                                "question": {
                                    "settings": {
                                        "size": {"width": 620, "height": 310}
                                    },
                                    "task": {
                                        "elements": [
                                            {
                                                "x": 0, "y": 0, "width": 5, "height": 2.5,
                                                "dropZones": ["0"],
                                                "type": {"library": "H5P.AdvancedText 1.1", "params": {"text": "<p>Sprint</p>"}},
                                                "backgroundOpacity": 100, "multiple": False
                                            },
                                            {
                                                "x": 10, "y": 0, "width": 5, "height": 2.5,
                                                "dropZones": ["1"],
                                                "type": {"library": "H5P.AdvancedText 1.1", "params": {"text": "<p>Backlog</p>"}},
                                                "backgroundOpacity": 100, "multiple": False
                                            }
                                        ],
                                        "dropZones": [
                                            {"x": 0, "y": 50, "width": 10, "height": 5, "label": "<p>Zeitbegriff</p>", "correctElements": ["0"], "showLabel": True, "autoAlign": True, "single": False},
                                            {"x": 50, "y": 50, "width": 10, "height": 5, "label": "<p>Artefakt</p>", "correctElements": ["1"], "showLabel": True, "autoAlign": True, "single": False}
                                        ]
                                    }
                                }
                            },
                            "subContentId": "drag1",
                            "metadata": {"contentType": "Drag Question", "license": "U", "title": "Drag"}
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
    "title": "Drag Question Test",
    "language": "de",
    "mainLibrary": "H5P.InteractiveBook",
    "embedTypes": ["iframe"],
    "license": "U",
    "preloadedDependencies": [
        {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
        {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
        {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
        {"machineName": "H5P.DragQuestion", "majorVersion": 1, "minorVersion": 14}
    ]
}

output = Path('/home/claude/h5p-output/book_test_dragquestion.h5p')
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False))
    zf.writestr('h5p.json', json.dumps(h5p, ensure_ascii=False))

print(f'Erstellt: {output}')
