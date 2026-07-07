#!/usr/bin/env python3
import zipfile
import json
from pathlib import Path

content = {
    "showCoverPage": False,
    "bookCover": {"coverDescription": "", "coverImage": {}, "coverMedium": {}},
    "title": "<p>MultiChoice Test</p>",
    "chapters": [
        {
            "title": "Multiple Choice Quiz",
            "params": {
                "content": [
                    {
                        "content": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {"text": "<h2>Quiz</h2><p>Waehle die richtige Antwort:</p>"},
                            "subContentId": "intro",
                            "metadata": {"contentType": "Text", "license": "U", "title": "Intro"}
                        },
                        "useSeparator": "auto"
                    },
                    {
                        "content": {
                            "library": "H5P.MultiChoice 1.16",
                            "params": {
                                "question": "<p>Wie lange dauert ein Sprint maximal?</p>",
                                "answers": [
                                    {"text": "<p>1 Woche</p>", "correct": False},
                                    {"text": "<p>4 Wochen</p>", "correct": True},
                                    {"text": "<p>3 Monate</p>", "correct": False}
                                ],
                                "behaviour": {
                                    "enableRetry": True,
                                    "enableSolutionsButton": True,
                                    "singleAnswer": True,
                                    "shuffleAnswers": False,
                                    "showSolutionsRequiresInput": True,
                                    "type": "auto"
                                },
                                "UI": {
                                    "checkAnswerButton": "Pruefen",
                                    "showSolutionButton": "Loesung",
                                    "tryAgainButton": "Nochmal",
                                    "correctText": "Richtig!",
                                    "wrongText": "Falsch!"
                                }
                            },
                            "subContentId": "mc1",
                            "metadata": {"contentType": "Multiple Choice", "license": "U", "title": "MC"}
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
    "title": "MultiChoice Test",
    "language": "de",
    "mainLibrary": "H5P.InteractiveBook",
    "embedTypes": ["iframe"],
    "license": "U",
    "preloadedDependencies": [
        {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
        {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
        {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
        {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16}
    ]
}

output = Path('/home/claude/h5p-output/book_test_multichoice.h5p')
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False))
    zf.writestr('h5p.json', json.dumps(h5p, ensure_ascii=False))

print(f'Erstellt: {output}')
