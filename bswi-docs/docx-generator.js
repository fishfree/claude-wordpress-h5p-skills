/**
 * BS:WI DOCX Generator
 * 
 * Erstellt Word-Dokumente im offiziellen BS:WI Corporate Design.
 * 
 * Verwendung:
 *   node docx-generator.js
 * 
 * Voraussetzungen:
 *   npm install docx
 * 
 * Dieses Script dient als Vorlage und kann für verschiedene Dokumenttypen angepasst werden.
 */

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        Header, Footer, AlignmentType, LevelFormat, ImageRun,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
        Tab, TabStopType, HeadingLevel, VerticalAlign, convertInchesToTwip } = require('docx');
const fs = require('fs');
const path = require('path');

// ============================================================================
// BS:WI FARBEN
// ============================================================================

const BLAU_1 = "1C3D71";   // Headlines, Rahmen, Footer-Border
const BLAU_2 = "102141";   // Dunkler Hintergrund
const BLAU_3 = "1266B0";   // Untertitel, Links, Claim
const BLAU_4 = "008BC9";   // Akzent-Ränder, Buttons
const BLAU_5 = "41C0F0";   // Trennlinien, Highlights
const BLAU_6 = "A4DBF8";   // Tabellen-Rahmen
const BLAU_7 = "EAF6FE";   // Hintergründe (Info-Boxen, Header)
const HELLGRAU = "F6F6F6"; // Aufgaben-Box Hintergrund
const DUNKELGRAU = "666666"; // Sekundärtext, Labels
const AKZENT = "E8FF00";   // Neongelb für Warnungen

// ============================================================================
// SEITEN-EINSTELLUNGEN (A4)
// ============================================================================

const PAGE_WIDTH = 11906;  // A4 Breite in Twips
const PAGE_HEIGHT = 16838; // A4 Höhe in Twips
const MARGIN = 720;        // ~1.27cm Rand
const CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN); // ~10466

// ============================================================================
// RAHMEN-DEFINITIONEN
// ============================================================================

const taskBorderLeft = { style: BorderStyle.SINGLE, size: 24, color: BLAU_4 };
const taskBorderOther = { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 };
const infoBorderLeft = { style: BorderStyle.SINGLE, size: 20, color: BLAU_4 };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };

// ============================================================================
// LOGO LADEN
// Logo muss im templates/ Verzeichnis liegen
// Logo-Seitenverhältnis: 562x180 = 3.12:1
// ============================================================================

let logoBuffer;
const logoPath = path.join(__dirname, 'templates', 'Logo_BSWI_Quer_RGB.png');
if (fs.existsSync(logoPath)) {
    logoBuffer = fs.readFileSync(logoPath);
}

// ============================================================================
// HELPER-FUNKTIONEN
// ============================================================================

/**
 * Erstellt eine Eingabezeile (unterstrichener Platzhalter)
 */
function inputLine(length = 'full') {
    const spaces = length === 'short' 
        ? "                                                       "
        : "                                                                                                          ";
    return new Paragraph({
        spacing: { before: 80, after: 80 },
        children: [
            new TextRun({ 
                text: spaces,
                font: "Arial",
                size: 22,
                underline: { type: "single", color: DUNKELGRAU }
            })
        ]
    });
}

/**
 * Erstellt den Header mit Logo | Titel | Name/Datum
 */
function createHeader(titel, untertitel) {
    const headerChildren = [
        new Table({
            width: { size: CONTENT_WIDTH, type: WidthType.DXA },
            columnWidths: [2000, 5500, 2966],
            borders: {
                top: noBorder, left: noBorder, right: noBorder,
                bottom: { style: BorderStyle.SINGLE, size: 12, color: BLAU_1 },
                insideHorizontal: noBorder, insideVertical: noBorder
            },
            rows: [
                new TableRow({
                    children: [
                        // Logo links
                        new TableCell({
                            width: { size: 2000, type: WidthType.DXA },
                            verticalAlign: VerticalAlign.CENTER,
                            borders: { top: noBorder, left: noBorder, right: noBorder, bottom: noBorder },
                            children: [
                                new Paragraph({
                                    children: logoBuffer ? [
                                        new ImageRun({
                                            data: logoBuffer,
                                            transformation: { width: 112, height: 36 }, // Korrektes Seitenverhältnis
                                            type: "png"
                                        })
                                    ] : []
                                })
                            ]
                        }),
                        // Titel Mitte
                        new TableCell({
                            width: { size: 5500, type: WidthType.DXA },
                            verticalAlign: VerticalAlign.CENTER,
                            borders: { top: noBorder, left: noBorder, right: noBorder, bottom: noBorder },
                            children: [
                                new Paragraph({
                                    alignment: AlignmentType.CENTER,
                                    children: [
                                        new TextRun({ text: titel, bold: true, font: "Arial", size: 30, color: BLAU_1 })
                                    ]
                                }),
                                new Paragraph({
                                    alignment: AlignmentType.CENTER,
                                    children: [
                                        new TextRun({ text: untertitel, font: "Arial", size: 20, color: BLAU_3 })
                                    ]
                                })
                            ]
                        }),
                        // Name/Datum rechts
                        new TableCell({
                            width: { size: 2966, type: WidthType.DXA },
                            verticalAlign: VerticalAlign.CENTER,
                            borders: { top: noBorder, left: noBorder, right: noBorder, bottom: noBorder },
                            children: [
                                new Paragraph({
                                    alignment: AlignmentType.RIGHT,
                                    spacing: { after: 60 },
                                    children: [
                                        new TextRun({ text: "Name: ", font: "Arial", size: 18, color: DUNKELGRAU }),
                                        new TextRun({ text: "_____________", font: "Arial", size: 18, underline: { type: "single", color: DUNKELGRAU } })
                                    ]
                                }),
                                new Paragraph({
                                    alignment: AlignmentType.RIGHT,
                                    children: [
                                        new TextRun({ text: "Datum: ", font: "Arial", size: 18, color: DUNKELGRAU }),
                                        new TextRun({ text: "_____________", font: "Arial", size: 18, underline: { type: "single", color: DUNKELGRAU } })
                                    ]
                                })
                            ]
                        })
                    ]
                })
            ]
        }),
        new Paragraph({ spacing: { after: 200 } })
    ];
    
    return new Header({ children: headerChildren });
}

/**
 * Erstellt den Footer mit Autor | Claim | Seitenzahl
 */
function createFooter() {
    return new Footer({
        children: [
            new Paragraph({
                border: { top: { style: BorderStyle.SINGLE, size: 8, color: BLAU_1 } },
                spacing: { before: 100 },
                tabStops: [
                    { type: TabStopType.CENTER, position: Math.floor(CONTENT_WIDTH / 2) },
                    { type: TabStopType.RIGHT, position: CONTENT_WIDTH }
                ],
                children: [
                    new TextRun({ text: "Dirk Schulenburg · BS:WI", font: "Arial", size: 17, color: DUNKELGRAU }),
                    new TextRun({ children: [new Tab()] }),
                    new TextRun({ text: "Kompetent Zukunft Gestalten", font: "Arial", size: 17, italics: true, color: BLAU_3 }),
                    new TextRun({ children: [new Tab()] }),
                    new TextRun({ text: "Seite ", font: "Arial", size: 17, color: BLAU_1 }),
                    new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 17, bold: true, color: BLAU_1 }),
                    new TextRun({ text: " von ", font: "Arial", size: 17, color: BLAU_1 }),
                    new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 17, bold: true, color: BLAU_1 })
                ]
            })
        ]
    });
}

/**
 * Erstellt eine Aufgaben-Box
 */
function createTaskBox(nummer, titel, punkte, inhalt) {
    const rows = [
        new TableRow({
            children: [
                new TableCell({
                    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
                    shading: { fill: HELLGRAU, type: ShadingType.CLEAR },
                    borders: {
                        top: taskBorderOther,
                        left: taskBorderLeft,
                        right: taskBorderOther,
                        bottom: noBorder
                    },
                    margins: { top: 100, bottom: 80, left: 200, right: 120 },
                    children: [
                        new Paragraph({
                            tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_WIDTH - 400 }],
                            children: [
                                new TextRun({ text: `📝 Aufgabe ${nummer}: ${titel}`, bold: true, font: "Arial", size: 23, color: BLAU_1 }),
                                new TextRun({ children: [new Tab()] }),
                                new TextRun({ text: `${punkte} Punkte`, bold: true, font: "Arial", size: 18, color: BLAU_4 })
                            ]
                        })
                    ]
                })
            ]
        })
    ];
    
    inhalt.forEach((paragraph, index) => {
        rows.push(new TableRow({
            children: [
                new TableCell({
                    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
                    shading: { fill: HELLGRAU, type: ShadingType.CLEAR },
                    borders: {
                        top: noBorder,
                        left: taskBorderLeft,
                        right: taskBorderOther,
                        bottom: index === inhalt.length - 1 ? taskBorderOther : noBorder
                    },
                    margins: { top: 40, bottom: 40, left: 200, right: 120 },
                    children: [paragraph]
                })
            ]
        }));
    });
    
    return new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: rows
    });
}

/**
 * Erstellt eine Info-Box (Tipp, Hinweis, etc.)
 */
function createInfoBox(icon, titel, text) {
    return new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: [
            new TableRow({
                children: [
                    new TableCell({
                        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
                        shading: { fill: BLAU_7, type: ShadingType.CLEAR },
                        borders: {
                            top: { style: BorderStyle.SINGLE, size: 4, color: BLAU_4 },
                            left: infoBorderLeft,
                            right: { style: BorderStyle.SINGLE, size: 4, color: BLAU_4 },
                            bottom: { style: BorderStyle.SINGLE, size: 4, color: BLAU_4 }
                        },
                        margins: { top: 100, bottom: 100, left: 150, right: 120 },
                        children: [
                            new Paragraph({
                                children: [
                                    new TextRun({ text: `${icon} ${titel}: `, bold: true, font: "Arial", size: 22, color: BLAU_1 }),
                                    new TextRun({ text: text, font: "Arial", size: 22 })
                                ]
                            })
                        ]
                    })
                ]
            })
        ]
    });
}

/**
 * Erstellt eine Formel-Box
 */
function createFormelBox(formel, beschreibung = "", bgColor = BLAU_1) {
    const rows = [
        new TableRow({
            children: [
                new TableCell({
                    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
                    shading: { fill: bgColor, type: ShadingType.CLEAR },
                    borders: { top: noBorder, left: noBorder, right: noBorder, bottom: noBorder },
                    margins: { top: 150, bottom: beschreibung ? 80 : 150, left: 120, right: 120 },
                    children: [
                        new Paragraph({
                            alignment: AlignmentType.CENTER,
                            children: [
                                new TextRun({ text: formel, font: "Times New Roman", size: 36, italics: true, color: "FFFFFF" })
                            ]
                        })
                    ]
                })
            ]
        })
    ];
    
    if (beschreibung) {
        rows.push(new TableRow({
            children: [
                new TableCell({
                    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
                    shading: { fill: bgColor, type: ShadingType.CLEAR },
                    borders: { top: noBorder, left: noBorder, right: noBorder, bottom: noBorder },
                    margins: { top: 0, bottom: 150, left: 120, right: 120 },
                    children: [
                        new Paragraph({
                            alignment: AlignmentType.CENTER,
                            children: [
                                new TextRun({ text: beschreibung, font: "Arial", size: 18, color: "FFFFFF" })
                            ]
                        })
                    ]
                })
            ]
        }));
    }
    
    return new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: rows
    });
}

/**
 * Erstellt eine Lernziele-Box
 */
function createLernzieleBox(ziele) {
    const rows = [
        new TableRow({
            children: [
                new TableCell({
                    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
                    shading: { fill: BLAU_7, type: ShadingType.CLEAR },
                    borders: {
                        top: { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 },
                        left: { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 },
                        right: { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 },
                        bottom: noBorder
                    },
                    margins: { top: 120, bottom: 60, left: 150, right: 120 },
                    children: [
                        new Paragraph({
                            children: [
                                new TextRun({ text: "🎯 Lernziele", bold: true, font: "Arial", size: 24, color: BLAU_1 })
                            ]
                        })
                    ]
                })
            ]
        })
    ];
    
    ziele.forEach((ziel, index) => {
        rows.push(new TableRow({
            children: [
                new TableCell({
                    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
                    shading: { fill: BLAU_7, type: ShadingType.CLEAR },
                    borders: {
                        top: noBorder,
                        left: { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 },
                        right: { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 },
                        bottom: index === ziele.length - 1 ? { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 } : noBorder
                    },
                    margins: { top: 40, bottom: index === ziele.length - 1 ? 120 : 40, left: 150, right: 120 },
                    children: [
                        new Paragraph({
                            children: [
                                new TextRun({ text: `• ${ziel}`, font: "Arial", size: 22, color: BLAU_1 })
                            ]
                        })
                    ]
                })
            ]
        }));
    });
    
    return new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: rows
    });
}

/**
 * Erstellt eine Überschrift mit Icon
 */
function createHeading(icon, text) {
    return new Paragraph({
        spacing: { before: 300, after: 150 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: BLAU_5 } },
        children: [
            new TextRun({ text: `${icon} ${text}`, bold: true, font: "Arial", size: 26, color: BLAU_1 })
        ]
    });
}

/**
 * Erstellt eine Wertetabelle
 */
function createWertetabelle(headers, emptyRow = true) {
    const cellWidth = Math.floor(CONTENT_WIDTH / headers.length);
    const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: BLAU_5 };
    
    const rows = [
        new TableRow({
            children: headers.map(val => 
                new TableCell({
                    width: { size: cellWidth, type: WidthType.DXA },
                    shading: { fill: BLAU_1, type: ShadingType.CLEAR },
                    borders: { top: cellBorder, left: cellBorder, right: cellBorder, bottom: cellBorder },
                    margins: { top: 80, bottom: 80, left: 40, right: 40 },
                    children: [
                        new Paragraph({
                            alignment: AlignmentType.CENTER,
                            children: [new TextRun({ text: val, bold: true, font: "Arial", size: 22, color: "FFFFFF" })]
                        })
                    ]
                })
            )
        })
    ];
    
    if (emptyRow) {
        rows.push(new TableRow({
            children: headers.map((_, i) => 
                new TableCell({
                    width: { size: cellWidth, type: WidthType.DXA },
                    shading: { fill: i % 2 === 0 ? BLAU_7 : "FFFFFF", type: ShadingType.CLEAR },
                    borders: { top: cellBorder, left: cellBorder, right: cellBorder, bottom: cellBorder },
                    margins: { top: 80, bottom: 80, left: 40, right: 40 },
                    children: [
                        new Paragraph({
                            alignment: AlignmentType.CENTER,
                            children: [new TextRun({ text: i === 0 ? "f(x)" : " ", bold: i === 0, font: "Arial", size: 22 })]
                        })
                    ]
                })
            )
        }));
    }
    
    return new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: Array(headers.length).fill(cellWidth),
        rows: rows
    });
}

/**
 * Erstellt einen Koordinatensystem-Platzhalter
 */
function createKoordinatensystem(height = 3000) {
    return new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: [
            new TableRow({
                height: { value: height, rule: "exact" },
                children: [
                    new TableCell({
                        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
                        shading: { fill: "FFFFFF", type: ShadingType.CLEAR },
                        borders: {
                            top: { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 },
                            left: { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 },
                            right: { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 },
                            bottom: { style: BorderStyle.SINGLE, size: 8, color: BLAU_4 }
                        },
                        verticalAlign: VerticalAlign.CENTER,
                        children: [
                            new Paragraph({
                                alignment: AlignmentType.CENTER,
                                children: [
                                    new TextRun({ text: "[Koordinatensystem hier zeichnen]", font: "Arial", size: 20, color: DUNKELGRAU, italics: true })
                                ]
                            })
                        ]
                    })
                ]
            })
        ]
    });
}

// ============================================================================
// EXPORT
// ============================================================================

module.exports = {
    // Farben
    BLAU_1, BLAU_2, BLAU_3, BLAU_4, BLAU_5, BLAU_6, BLAU_7,
    HELLGRAU, DUNKELGRAU, AKZENT,
    
    // Seiten-Einstellungen
    PAGE_WIDTH, PAGE_HEIGHT, MARGIN, CONTENT_WIDTH,
    
    // Funktionen
    inputLine,
    createHeader,
    createFooter,
    createTaskBox,
    createInfoBox,
    createFormelBox,
    createLernzieleBox,
    createHeading,
    createWertetabelle,
    createKoordinatensystem
};
