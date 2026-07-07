#!/usr/bin/env python3
"""
H5P Multi-Agent System - Integration Tests

Testet das gesamte System von Ende zu Ende.

Aufruf:
    python test_integration.py
    python test_integration.py -v  # Verbose
"""

import sys
import json
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test: Alle Module importierbar"""
    print("Test 1: Imports...")

    try:
        from h5p_system import H5PSystem, SystemResult, quick_generate
        from orchestrator import H5POrchestrator, ContentAnalysis
        from brand_config import BrandConfig, get_brand_preset, list_brand_presets
        from sub_agents import QuizAgent, CardAgent, DragAgent, DesignAgent

        print("  [OK] Alle Imports erfolgreich")
        return True
    except Exception as e:
        print(f"  [FAIL] Import-Fehler: {e}")
        return False


def test_brand_presets():
    """Test: Brand-Presets laden"""
    print("\nTest 2: Brand-Presets...")

    from brand_config import get_brand_preset, list_brand_presets

    presets = list_brand_presets()
    print(f"  Verfuegbare Presets: {presets}")

    if len(presets) < 3:
        print("  [FAIL] Weniger als 3 Presets")
        return False

    # BSWI laden
    bswi = get_brand_preset('bswi')
    if bswi.name != "BS:WI Hamburg":
        print(f"  [FAIL] BSWI Name falsch: {bswi.name}")
        return False

    print(f"  BSWI: {bswi.name}, Primary: {bswi.colors.primary}")
    print("  [OK] Brand-Presets funktionieren")
    return True


def test_system_init():
    """Test: H5PSystem Initialisierung"""
    print("\nTest 3: System-Initialisierung...")

    from h5p_system import H5PSystem

    # Ohne Brand
    system1 = H5PSystem()
    if system1.design_agent is not None:
        print("  [FAIL] Design Agent sollte None sein ohne Brand")
        return False

    # Mit Brand
    system2 = H5PSystem(brand='bswi')
    if system2.design_agent is None:
        print("  [FAIL] Design Agent sollte aktiv sein mit Brand")
        return False

    if system2.brand_config.name != "BS:WI Hamburg":
        print("  [FAIL] Brand nicht korrekt gesetzt")
        return False

    info = system2.get_system_info()
    print(f"  Version: {info['version']}")
    print(f"  Brand: {info['brand']}")
    print(f"  Design Agent: {'aktiv' if info['design_agent_active'] else 'inaktiv'}")

    print("  [OK] System-Initialisierung erfolgreich")
    return True


def test_content_analysis():
    """Test: Content-Analyse"""
    print("\nTest 4: Content-Analyse...")

    from h5p_system import H5PSystem

    system = H5PSystem()

    content = """
    ## Lernziele
    - Die Schueler koennen die drei Scrum-Rollen nennen
    - Die Schueler koennen Aufgaben den Rollen zuordnen
    - Die Schueler koennen den Sprint-Ablauf erklaeren
    """

    analysis = system.analyze_content(content)

    print(f"  Lernziele: {len(analysis.learning_goals)}")
    print(f"  Operatoren: {analysis.operators}")
    print(f"  Komplexitaet: {analysis.complexity.value}")

    if len(analysis.learning_goals) < 2:
        print("  [FAIL] Weniger als 2 Lernziele erkannt")
        return False

    if 'nennen' not in analysis.operators:
        print("  [FAIL] Operator 'nennen' nicht erkannt")
        return False

    print("  [OK] Content-Analyse funktioniert")
    return True


def test_flashcards_generation():
    """Test: Flashcards generieren"""
    print("\nTest 5: Flashcards generieren...")

    from h5p_system import H5PSystem

    system = H5PSystem(brand='bswi')

    result = system.generate_single(
        'flashcards',
        title='Test-Flashcards',
        cards=[
            {'front': 'Product Owner', 'back': 'Priorisiert das Backlog'},
            {'front': 'Scrum Master', 'back': 'Entfernt Hindernisse'},
            {'front': 'Dev Team', 'back': 'Entwickelt Features'},
        ]
    )

    if not result.success:
        print(f"  [FAIL] Generierung fehlgeschlagen: {result.errors}")
        return False

    if len(result.h5p_files) == 0:
        print("  [FAIL] Keine H5P-Dateien erstellt")
        return False

    h5p_file = result.h5p_files[0]
    if not h5p_file.exists():
        print(f"  [FAIL] H5P-Datei existiert nicht: {h5p_file}")
        return False

    print(f"  Erstellt: {h5p_file.name}")
    print(f"  Groesse: {h5p_file.stat().st_size} bytes")

    print("  [OK] Flashcards erfolgreich generiert")
    return True


def test_drag_drop_generation():
    """Test: Drag & Drop generieren"""
    print("\nTest 6: Drag & Drop generieren...")

    from h5p_system import H5PSystem

    system = H5PSystem(brand='minimal')

    result = system.generate_single(
        'drag_drop',
        title='Test-DragDrop',
        task='Ordne zu.',
        dropzones=['Kategorie A', 'Kategorie B'],
        draggables=[
            {'text': 'Item 1', 'dropzone': 0},
            {'text': 'Item 2', 'dropzone': 0},
            {'text': 'Item 3', 'dropzone': 1},
            {'text': 'Item 4', 'dropzone': 1},
        ]
    )

    if not result.success:
        print(f"  [FAIL] Generierung fehlgeschlagen: {result.errors}")
        return False

    print(f"  Erstellt: {result.h5p_files[0].name}")
    print("  [OK] Drag & Drop erfolgreich generiert")
    return True


def test_full_workflow():
    """Test: Vollstaendiger Workflow (Text → H5P)"""
    print("\nTest 7: Vollstaendiger Workflow...")

    from h5p_system import H5PSystem

    system = H5PSystem(brand='bswi')

    content = """
    ## Lernziele
    - Die Schueler koennen die drei Scrum-Rollen nennen
    """

    content_items = [
        {
            'cards': [
                {'front': 'PO', 'back': 'Product Owner'},
                {'front': 'SM', 'back': 'Scrum Master'},
                {'front': 'DT', 'back': 'Development Team'},
            ]
        }
    ]

    result = system.generate_from_text(content, content_items)

    if not result.success:
        print(f"  [FAIL] Workflow fehlgeschlagen: {result.errors}")
        return False

    print(f"  Analyse: {result.statistics.get('lernziele_erkannt', 0)} Lernziele")
    print(f"  Erstellt: {result.statistics.get('elemente_erstellt', 0)} Elemente")
    print(f"  Design: {result.statistics.get('design_angewendet', 0)} gestylt")

    if result.orchestrator_result:
        or_result = result.orchestrator_result
        if or_result.design_results:
            for dr in or_result.design_results:
                status = "OK" if dr.success else "Fehler"
                print(f"    Design [{status}]: {dr.changes_applied}")

    print("  [OK] Workflow erfolgreich")
    return True


def test_batch_generation():
    """Test: Batch-Generierung"""
    print("\nTest 8: Batch-Generierung...")

    from h5p_system import H5PSystem

    system = H5PSystem(brand='professional')

    elements = [
        {
            'type': 'flashcards',
            'title': 'Batch-Test-1',
            'cards': [
                {'front': 'A', 'back': 'Alpha'},
                {'front': 'B', 'back': 'Beta'},
                {'front': 'C', 'back': 'Gamma'},
            ]
        },
        {
            'type': 'true_false',
            'title': 'Batch-Test-2',
            'questions': [
                {'text': 'Dies ist wahr.', 'correct': True},
                {'text': 'Dies ist falsch.', 'correct': False},
            ]
        }
    ]

    result = system.generate_elements(elements)

    if not result.success:
        print(f"  [FAIL] Batch-Generierung fehlgeschlagen: {result.errors}")
        return False

    print(f"  Angefragt: {result.statistics.get('elemente_angefragt', 0)}")
    print(f"  Erstellt: {result.statistics.get('elemente_erstellt', 0)}")

    for f in result.h5p_files:
        print(f"    - {f.name}")

    print("  [OK] Batch-Generierung erfolgreich")
    return True


def test_design_application():
    """Test: Design auf existierende Datei anwenden"""
    print("\nTest 9: Design anwenden...")

    from h5p_system import H5PSystem
    from h5p_generator import create_flashcards

    # Zuerst Datei ohne Design erstellen
    result = create_flashcards(
        'Design-Test',
        [{'front': 'X', 'back': 'Y'}, {'front': 'A', 'back': 'B'}, {'front': 'C', 'back': 'D'}]
    )

    if not result.success:
        print(f"  [FAIL] Basis-Generierung fehlgeschlagen")
        return False

    # Design anwenden
    system = H5PSystem(brand='dark')
    design_result = system.apply_design_to_file(result.path)

    if not design_result.success:
        print(f"  [FAIL] Design fehlgeschlagen: {design_result.error}")
        return False

    print(f"  Datei: {design_result.original_path.name}")
    print(f"  Aenderungen: {design_result.changes_applied}")

    print("  [OK] Design erfolgreich angewendet")
    return True


def test_quick_functions():
    """Test: Quick-Convenience-Funktionen"""
    print("\nTest 10: Quick-Funktionen...")

    from h5p_system import quick_flashcards, quick_quiz, quick_drag_drop

    # Quick Flashcards
    result1 = quick_flashcards(
        'Quick-Flash',
        [{'front': 'Q1', 'back': 'A1'}, {'front': 'Q2', 'back': 'A2'}, {'front': 'Q3', 'back': 'A3'}],
        brand='bswi'
    )
    if not result1.success:
        print(f"  [FAIL] quick_flashcards: {result1.errors}")
        return False
    print(f"  quick_flashcards: OK")

    # Quick Quiz
    result2 = quick_quiz(
        'Quick-Quiz',
        [{'text': 'Wahr?', 'correct': True}],
        brand='minimal'
    )
    if not result2.success:
        print(f"  [FAIL] quick_quiz: {result2.errors}")
        return False
    print(f"  quick_quiz: OK")

    # Quick Drag Drop
    result3 = quick_drag_drop(
        'Quick-Drag',
        ['Zone A', 'Zone B'],
        [{'text': 'Item', 'dropzone': 0}],
        brand='professional'
    )
    if not result3.success:
        print(f"  [FAIL] quick_drag_drop: {result3.errors}")
        return False
    print(f"  quick_drag_drop: OK")

    print("  [OK] Alle Quick-Funktionen erfolgreich")
    return True


def run_all_tests(verbose=False):
    """Fuehrt alle Tests aus"""
    print("=" * 60)
    print("H5P Multi-Agent System - Integration Tests")
    print("=" * 60)

    tests = [
        test_imports,
        test_brand_presets,
        test_system_init,
        test_content_analysis,
        test_flashcards_generation,
        test_drag_drop_generation,
        test_full_workflow,
        test_batch_generation,
        test_design_application,
        test_quick_functions,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [EXCEPTION] {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print(f"Ergebnis: {passed} bestanden, {failed} fehlgeschlagen")
    print("=" * 60)

    if failed == 0:
        print("\n*** ALLE TESTS BESTANDEN ***\n")
        return 0
    else:
        print(f"\n*** {failed} TEST(S) FEHLGESCHLAGEN ***\n")
        return 1


if __name__ == "__main__":
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    sys.exit(run_all_tests(verbose))
