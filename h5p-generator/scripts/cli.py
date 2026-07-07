#!/usr/bin/env python3
"""
H5P Multi-Agent System - Command Line Interface

Aufruf:
    python cli.py generate "Lernmaterial..."
    python cli.py generate -f input.md -o ./output -b bswi
    python cli.py batch elements.json
    python cli.py info
    python cli.py brands

Beispiele:
    # Aus Text generieren
    python cli.py generate "## Lernziele\n- Schueler koennen Scrum-Rollen nennen"

    # Aus Datei mit Brand
    python cli.py generate -f lerneinheit.md -b bswi

    # Batch-Generierung
    python cli.py batch elements.json -o ./output

    # System-Info
    python cli.py info
"""

import argparse
import json
import sys
from pathlib import Path

# Modul-Pfad hinzufuegen
sys.path.insert(0, str(Path(__file__).parent))

from h5p_system import H5PSystem, SystemResult, quick_generate


def cmd_generate(args):
    """Generiert H5P-Inhalte aus Text oder Datei"""
    # Content laden
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Fehler: Datei nicht gefunden: {file_path}")
            return 1
        content = file_path.read_text(encoding='utf-8')
    elif args.content:
        content = args.content
    else:
        print("Fehler: Weder --file noch content angegeben")
        return 1

    # Content-Items laden (falls angegeben)
    content_items = None
    if args.items:
        items_path = Path(args.items)
        if items_path.exists():
            content_items = json.loads(items_path.read_text(encoding='utf-8'))
        else:
            print(f"Warnung: Content-Items-Datei nicht gefunden: {items_path}")

    # System initialisieren
    system = H5PSystem(
        output_dir=args.output,
        brand=args.brand
    )

    # Generieren
    print(f"Generiere H5P-Inhalte...")
    print(f"  Output: {system.output_dir}")
    print(f"  Brand: {args.brand or 'default'}")
    print()

    result = system.generate_from_text(
        content=content,
        content_items=content_items,
        apply_design=not args.no_design
    )

    # Ergebnis ausgeben
    if args.verbose:
        print(result.summary())
    else:
        print(result)

    return 0 if result.success else 1


def cmd_batch(args):
    """Batch-Generierung aus JSON-Datei"""
    elements_path = Path(args.file)
    if not elements_path.exists():
        print(f"Fehler: Datei nicht gefunden: {elements_path}")
        return 1

    elements = json.loads(elements_path.read_text(encoding='utf-8'))

    if not isinstance(elements, list):
        print("Fehler: JSON muss eine Liste von Elementen sein")
        return 1

    system = H5PSystem(
        output_dir=args.output,
        brand=args.brand
    )

    print(f"Batch-Generierung: {len(elements)} Elemente")
    print(f"  Output: {system.output_dir}")
    print()

    result = system.generate_elements(
        elements=elements,
        apply_design=not args.no_design
    )

    if args.verbose:
        print(result.summary())
    else:
        print(result)

    return 0 if result.success else 1


def cmd_single(args):
    """Generiert ein einzelnes H5P-Element"""
    system = H5PSystem(
        output_dir=args.output,
        brand=args.brand
    )

    # Parameter aus JSON oder Kommandozeile
    params = {}
    if args.params:
        params = json.loads(args.params)

    params['title'] = args.title

    print(f"Generiere {args.type}: {args.title}")

    result = system.generate_single(
        content_type=args.type,
        apply_design=not args.no_design,
        **params
    )

    print(result)
    return 0 if result.success else 1


def cmd_analyze(args):
    """Analysiert Content ohne Generierung"""
    if args.file:
        content = Path(args.file).read_text(encoding='utf-8')
    else:
        content = args.content

    system = H5PSystem()
    analysis = system.analyze_content(content)

    print("=" * 50)
    print("Content-Analyse")
    print("=" * 50)
    print(f"\nLernziele ({len(analysis.learning_goals)}):")
    for goal in analysis.learning_goals:
        print(f"  - {goal}")

    print(f"\nOperatoren: {analysis.operators}")
    print(f"Struktur: {analysis.content_structure.value}")
    print(f"Komplexitaet: {analysis.complexity.value}")
    print(f"Geschaetzte Elemente: {analysis.estimated_elements}")
    print(f"Container-Empfehlung: {analysis.suggested_container or 'Keiner'}")

    return 0


def cmd_design(args):
    """Wendet Branding auf existierende H5P-Datei an"""
    h5p_path = Path(args.file)
    if not h5p_path.exists():
        print(f"Fehler: Datei nicht gefunden: {h5p_path}")
        return 1

    system = H5PSystem(brand=args.brand)

    if not system.design_agent:
        print("Fehler: Kein Brand konfiguriert")
        return 1

    print(f"Wende Branding an: {h5p_path}")
    print(f"  Brand: {args.brand}")

    result = system.apply_design_to_file(h5p_path)

    if result.success:
        print(f"  Aenderungen: {', '.join(result.changes_applied)}")
        print("OK")
        return 0
    else:
        print(f"  Fehler: {result.error}")
        return 1


def cmd_info(args):
    """Zeigt System-Informationen"""
    system = H5PSystem()
    info = system.get_system_info()

    print("=" * 50)
    print("H5P Multi-Agent System")
    print("=" * 50)
    print(f"\nVersion: {info['version']}")
    print(f"Output-Dir: {info['output_dir']}")

    print(f"\nVerfuegbare H5P-Typen ({len(info['content_types'])}):")
    for ct in info['content_types']:
        print(f"  - {ct}")

    print(f"\nVerfuegbare Brand-Presets ({len(info['brand_presets'])}):")
    for bp in info['brand_presets']:
        print(f"  - {bp}")

    return 0


def cmd_brands(args):
    """Zeigt Brand-Preset Details"""
    from brand_config import BRAND_PRESETS

    if args.name:
        if args.name not in BRAND_PRESETS:
            print(f"Fehler: Brand '{args.name}' nicht gefunden")
            return 1

        brand = BRAND_PRESETS[args.name]
        print(f"\nBrand: {brand.name}")
        print(f"  Theme: {brand.theme}")
        print(f"  Farben:")
        print(f"    Primary: {brand.colors.primary}")
        print(f"    Success: {brand.colors.success}")
        print(f"    Error: {brand.colors.error}")
        print(f"  Feedback:")
        print(f"    Korrekt: {brand.feedback.correct}")
        print(f"    Falsch: {brand.feedback.wrong}")
        print(f"  Pass-Percentage: {brand.pass_percentage}%")
    else:
        print("Verfuegbare Brand-Presets:")
        for name, brand in BRAND_PRESETS.items():
            print(f"\n  {name}:")
            print(f"    Name: {brand.name}")
            print(f"    Primary: {brand.colors.primary}")
            print(f"    Theme: {brand.theme}")

    return 0


def cmd_types(args):
    """Zeigt H5P-Typ Details"""
    type_info = {
        'true_false': {
            'name': 'True/False',
            'agent': 'quiz',
            'params': ['title', 'questions: [{text, correct}]'],
            'use_case': 'Fakten ueberpruefen'
        },
        'multi_choice': {
            'name': 'Multiple Choice',
            'agent': 'quiz',
            'params': ['title', 'questions: [{question, answers: [{text, correct}]}]'],
            'use_case': 'Detailwissen abfragen'
        },
        'flashcards': {
            'name': 'Flashcards/Dialog Cards',
            'agent': 'card',
            'params': ['title', 'cards: [{front, back, tip?}]'],
            'use_case': 'Vokabeln, Definitionen'
        },
        'drag_drop': {
            'name': 'Drag & Drop',
            'agent': 'drag',
            'params': ['title', 'dropzones: []', 'draggables: [{text, dropzone}]'],
            'use_case': 'Kategorisieren, Zuordnen'
        },
        'accordion': {
            'name': 'Accordion',
            'agent': 'card',
            'params': ['title', 'panels: [{title, content}]'],
            'use_case': 'Strukturierte Informationen'
        },
        'timeline': {
            'name': 'Timeline',
            'agent': 'card',
            'params': ['title', 'events: [{headline, start_date, text}]'],
            'use_case': 'Chronologie, Geschichte'
        },
        'fill_blanks': {
            'name': 'Fill in the Blanks',
            'agent': 'drag',
            'params': ['title', 'text (mit *Luecken*)'],
            'use_case': 'Lueckentexte'
        },
        'drag_text': {
            'name': 'Drag the Words',
            'agent': 'drag',
            'params': ['title', 'text (mit *Luecken*)'],
            'use_case': 'Woerter in Luecken ziehen'
        },
        'mark_words': {
            'name': 'Mark the Words',
            'agent': 'drag',
            'params': ['title', 'text (mit *markierten* Woertern)'],
            'use_case': 'Begriffe identifizieren'
        },
        'summary': {
            'name': 'Summary',
            'agent': 'quiz',
            'params': ['title', 'items: [{statements: []}]'],
            'use_case': 'Kernaussagen'
        },
        'single_choice': {
            'name': 'Single Choice Set',
            'agent': 'quiz',
            'params': ['title', 'questions: [{question, answers: []}]'],
            'use_case': 'Schnelle Entscheidungen'
        },
        'memory_game': {
            'name': 'Memory Game',
            'agent': 'card',
            'params': ['title', 'cards: [{description, image?}]'],
            'use_case': 'Spielerisches Lernen'
        }
    }

    if args.name:
        if args.name not in type_info:
            print(f"Fehler: Typ '{args.name}' nicht gefunden")
            return 1

        info = type_info[args.name]
        print(f"\nH5P-Typ: {info['name']}")
        print(f"  Agent: {info['agent']}")
        print(f"  Use Case: {info['use_case']}")
        print(f"  Parameter:")
        for p in info['params']:
            print(f"    - {p}")
    else:
        print("Verfuegbare H5P-Typen:")
        for name, info in type_info.items():
            print(f"\n  {name}:")
            print(f"    {info['name']} - {info['use_case']}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description='H5P Multi-Agent System CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Beispiele:
  %(prog)s generate "## Lernziele\\n- Schueler koennen..."
  %(prog)s generate -f input.md -b bswi
  %(prog)s batch elements.json -o ./output
  %(prog)s analyze -f input.md
  %(prog)s info
  %(prog)s brands
  %(prog)s types flashcards
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='Verfuegbare Befehle')

    # generate
    gen_parser = subparsers.add_parser('generate', help='H5P aus Text/Datei generieren')
    gen_parser.add_argument('content', nargs='?', help='Lernmaterial als Text')
    gen_parser.add_argument('-f', '--file', help='Input-Datei (Markdown/Text)')
    gen_parser.add_argument('-i', '--items', help='Content-Items JSON-Datei')
    gen_parser.add_argument('-o', '--output', help='Output-Verzeichnis')
    gen_parser.add_argument('-b', '--brand', help='Brand-Preset (bswi, minimal, etc.)')
    gen_parser.add_argument('--no-design', action='store_true', help='Kein Branding anwenden')
    gen_parser.add_argument('-v', '--verbose', action='store_true', help='Ausfuehrliche Ausgabe')

    # batch
    batch_parser = subparsers.add_parser('batch', help='Batch-Generierung aus JSON')
    batch_parser.add_argument('file', help='Elements JSON-Datei')
    batch_parser.add_argument('-o', '--output', help='Output-Verzeichnis')
    batch_parser.add_argument('-b', '--brand', help='Brand-Preset')
    batch_parser.add_argument('--no-design', action='store_true', help='Kein Branding')
    batch_parser.add_argument('-v', '--verbose', action='store_true')

    # single
    single_parser = subparsers.add_parser('single', help='Einzelnes Element generieren')
    single_parser.add_argument('type', help='H5P-Typ (flashcards, drag_drop, etc.)')
    single_parser.add_argument('title', help='Titel')
    single_parser.add_argument('-p', '--params', help='Parameter als JSON')
    single_parser.add_argument('-o', '--output', help='Output-Verzeichnis')
    single_parser.add_argument('-b', '--brand', help='Brand-Preset')
    single_parser.add_argument('--no-design', action='store_true')

    # analyze
    analyze_parser = subparsers.add_parser('analyze', help='Content analysieren')
    analyze_parser.add_argument('content', nargs='?', help='Content als Text')
    analyze_parser.add_argument('-f', '--file', help='Input-Datei')

    # design
    design_parser = subparsers.add_parser('design', help='Branding auf H5P anwenden')
    design_parser.add_argument('file', help='H5P-Datei')
    design_parser.add_argument('-b', '--brand', required=True, help='Brand-Preset')

    # info
    subparsers.add_parser('info', help='System-Informationen')

    # brands
    brands_parser = subparsers.add_parser('brands', help='Brand-Presets anzeigen')
    brands_parser.add_argument('name', nargs='?', help='Preset-Name fuer Details')

    # types
    types_parser = subparsers.add_parser('types', help='H5P-Typen anzeigen')
    types_parser.add_argument('name', nargs='?', help='Typ-Name fuer Details')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        'generate': cmd_generate,
        'batch': cmd_batch,
        'single': cmd_single,
        'analyze': cmd_analyze,
        'design': cmd_design,
        'info': cmd_info,
        'brands': cmd_brands,
        'types': cmd_types,
    }

    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())
