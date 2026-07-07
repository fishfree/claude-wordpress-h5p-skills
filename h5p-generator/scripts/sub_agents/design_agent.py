"""
Design Agent - Wendet Branding auf H5P-Dateien an

Post-Processing Agent, der nach der Content-Generierung
Corporate Identity (Farben, Logos, Texte) auf H5P-Dateien anwendet.
"""

import json
import zipfile
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import sys
import os

# Parent-Verzeichnis zum Path hinzufuegen
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brand_config import BrandConfig, get_brand_preset
from .base_agent import AgentResult, AgentStatus


@dataclass
class DesignResult:
    """Ergebnis der Design-Anwendung"""
    success: bool
    original_path: Path
    styled_path: Optional[Path] = None
    content_type: str = ""
    changes_applied: list[str] = field(default_factory=list)
    error: Optional[str] = None

    def __str__(self):
        if self.success:
            changes = ", ".join(self.changes_applied) if self.changes_applied else "keine"
            return f"[DESIGN OK] {self.content_type}: {changes}"
        return f"[DESIGN FAIL] {self.content_type}: {self.error}"


class DesignAgent:
    """
    Design Agent fuer H5P Branding.

    Workflow:
    1. H5P-Datei extrahieren
    2. content.json modifizieren (Farben, Feedback-Texte)
    3. Logo einbetten (falls konfiguriert)
    4. H5P neu verpacken

    Unterstuetzte Typen und deren Styling-Moeglichkeiten:
    - DragQuestion: Farben, Background, Feedback
    - MemoryGame: themeColor, Feedback
    - QuestionSet: Feedback-Texte, Pass-Percentage
    - MultiChoice: UI-Texte, Feedback
    - TrueFalse: Feedback-Texte
    - Blanks: Feedback-Texte
    - DialogCards: Keine direkte Farb-Unterstuetzung
    - Accordion: Keine direkte Farb-Unterstuetzung
    - Timeline: Begrenzte Unterstuetzung
    - DragText: Feedback-Texte
    - MarkTheWords: Feedback-Texte
    - Summary: Feedback-Texte
    """

    # Pfad zur BS:WI CSS-Datei
    BSWI_CSS_PATH = Path(__file__).parent.parent / "assets" / "bswi-h5p.css"

    # H5P-Typ zu Styling-Handler Mapping
    STYLE_HANDLERS = {
        'H5P.DragQuestion': '_style_drag_question',
        'H5P.MemoryGame': '_style_memory_game',
        'H5P.QuestionSet': '_style_question_set',
        'H5P.MultiChoice': '_style_multi_choice',
        'H5P.TrueFalse': '_style_true_false',
        'H5P.Blanks': '_style_blanks',
        'H5P.Dialogcards': '_style_dialog_cards',
        'H5P.Accordion': '_style_accordion',
        'H5P.Timeline': '_style_timeline',
        'H5P.DragText': '_style_drag_text',
        'H5P.MarkTheWords': '_style_mark_words',
        'H5P.Summary': '_style_summary',
        'H5P.SingleChoiceSet': '_style_single_choice_set',
    }

    def __init__(self, brand_config: BrandConfig = None):
        """
        Initialisiert Design Agent.

        Args:
            brand_config: BrandConfig Instanz oder None fuer Default
        """
        self.brand_config = brand_config or get_brand_preset('default')

    def apply_branding(self, agent_result: AgentResult) -> DesignResult:
        """
        Wendet Branding auf ein AgentResult an.

        Args:
            agent_result: Ergebnis eines Sub-Agents (QuizAgent, etc.)

        Returns:
            DesignResult mit gestylter H5P-Datei
        """
        if not agent_result.success or not agent_result.h5p_result:
            return DesignResult(
                success=False,
                original_path=None,
                content_type=agent_result.original_type,
                error="Kein gueltiges AgentResult"
            )

        h5p_path = agent_result.h5p_result.path
        if not h5p_path or not Path(h5p_path).exists():
            return DesignResult(
                success=False,
                original_path=h5p_path,
                content_type=agent_result.final_type,
                error=f"H5P-Datei nicht gefunden: {h5p_path}"
            )

        return self.style_h5p_file(h5p_path, agent_result.final_type)

    def style_h5p_file(self, h5p_path: Path | str, content_type: str = None) -> DesignResult:
        """
        Wendet Branding auf eine H5P-Datei an.

        Args:
            h5p_path: Pfad zur H5P-Datei
            content_type: Optionaler Content-Type (wird sonst aus h5p.json gelesen)

        Returns:
            DesignResult
        """
        h5p_path = Path(h5p_path)
        changes = []

        try:
            # 1. Temporaeres Verzeichnis erstellen
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                # 2. H5P extrahieren
                with zipfile.ZipFile(h5p_path, 'r') as zf:
                    zf.extractall(temp_path)

                # 3. h5p.json lesen um Typ zu bestimmen
                h5p_json_path = temp_path / "h5p.json"
                if not h5p_json_path.exists():
                    return DesignResult(
                        success=False,
                        original_path=h5p_path,
                        content_type=content_type or "unknown",
                        error="h5p.json nicht gefunden"
                    )

                with open(h5p_json_path, 'r', encoding='utf-8') as f:
                    h5p_meta = json.load(f)

                main_library = h5p_meta.get('mainLibrary', '')
                if not content_type:
                    content_type = main_library

                # 4. content.json lesen und modifizieren
                content_json_path = temp_path / "content" / "content.json"
                if not content_json_path.exists():
                    return DesignResult(
                        success=False,
                        original_path=h5p_path,
                        content_type=content_type,
                        error="content/content.json nicht gefunden"
                    )

                with open(content_json_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)

                # 5. Typ-spezifisches Styling anwenden
                handler_name = self.STYLE_HANDLERS.get(main_library)
                if not handler_name:
                    handler_name = self.CONTAINER_HANDLERS.get(main_library)
                if handler_name:
                    handler = getattr(self, handler_name, None)
                    if handler:
                        content, type_changes = handler(content)
                        changes.extend(type_changes)

                # 6. Allgemeine Aenderungen (falls keine typ-spezifischen)
                if not changes:
                    content, generic_changes = self._apply_generic_styling(content)
                    changes.extend(generic_changes)

                # 7. Custom CSS einbetten (fuer BS:WI und andere Brands)
                css_changes = self._inject_custom_css(temp_path, h5p_meta)
                changes.extend(css_changes)

                # 7b. Logo einbetten (falls konfiguriert)
                if self.brand_config.logo.logo_url:
                    logo_changes = self._embed_logo(temp_path, content)
                    changes.extend(logo_changes)

                # 8. Modifizierte content.json speichern
                with open(content_json_path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)

                # 9. H5P neu verpacken (ueberschreibt Original)
                self._repackage_h5p(temp_path, h5p_path)

            return DesignResult(
                success=True,
                original_path=h5p_path,
                styled_path=h5p_path,
                content_type=content_type,
                changes_applied=changes if changes else ["Keine Aenderungen notwendig"]
            )

        except Exception as e:
            return DesignResult(
                success=False,
                original_path=h5p_path,
                content_type=content_type or "unknown",
                error=str(e)
            )

    def process_batch(self, agent_results: list[AgentResult]) -> list[DesignResult]:
        """
        Verarbeitet mehrere AgentResults.

        Args:
            agent_results: Liste von AgentResults

        Returns:
            Liste von DesignResults
        """
        return [self.apply_branding(result) for result in agent_results]

    # =========================================================================
    # Type-specific styling handlers
    # =========================================================================

    def _style_drag_question(self, content: dict) -> tuple[dict, list[str]]:
        """
        DragQuestion: Volle Unterstuetzung
        - Background-Farbe
        - Dropzone-Farben
        - Feedback-Texte
        """
        changes = []
        colors = self.brand_config.colors
        feedback = self.brand_config.feedback

        # Feedback-Texte
        if 'overallFeedback' in content:
            content['overallFeedback'] = self._create_feedback_ranges()
            changes.append("Feedback-Texte aktualisiert")

        # Dropzones stylen
        if 'question' in content and 'task' in content['question']:
            task = content['question']['task']
            if 'dropZones' in task:
                for i, dz in enumerate(task['dropZones']):
                    # Farben basierend auf Index rotieren
                    zone_colors = [
                        colors.primary,
                        colors.secondary,
                        colors.success,
                        colors.warning,
                    ]
                    # backgroundOpacity beibehalten aber Farbe koennte via CSS injection
                    pass
                # changes.append("Dropzone-Farben angepasst")  # Nur wenn implementiert

        # UI-Texte
        if feedback.try_again:
            content['tryAgain'] = feedback.try_again
            changes.append("UI-Texte lokalisiert")
        if feedback.show_solution:
            content['showSolution'] = feedback.show_solution

        return content, changes

    def _style_memory_game(self, content: dict) -> tuple[dict, list[str]]:
        """
        MemoryGame: themeColor Unterstuetzung
        """
        changes = []
        colors = self.brand_config.colors

        # Theme-Farbe setzen
        if 'lookNFeel' not in content:
            content['lookNFeel'] = {}
        content['lookNFeel']['themeColor'] = colors.primary
        changes.append(f"Theme-Farbe: {colors.primary}")

        # Feedback-Texte
        if 'l10n' in content:
            content['l10n']['feedback'] = self.brand_config.feedback.correct
            changes.append("Feedback-Text aktualisiert")

        return content, changes

    def _style_question_set(self, content: dict) -> tuple[dict, list[str]]:
        """
        QuestionSet: Wrapper fuer TrueFalse/MultiChoice
        - Pass-Percentage
        - End-Game Texte
        """
        changes = []
        feedback = self.brand_config.feedback

        # Pass-Percentage
        content['passPercentage'] = self.brand_config.pass_percentage
        changes.append(f"Bestehensgrenze: {self.brand_config.pass_percentage}%")

        # End-Game Konfiguration
        if 'endGame' in content:
            eg = content['endGame']
            eg['successComment'] = feedback.correct
            eg['failComment'] = feedback.wrong
            eg['solutionButtonText'] = feedback.show_solution
            eg['retryButtonText'] = feedback.try_again
            eg['finishButtonText'] = feedback.finish
            changes.append("Endscreen-Texte aktualisiert")

        # UI-Texte
        if 'texts' in content:
            content['texts']['finishButton'] = feedback.finish
            content['texts']['nextButton'] = feedback.next
            content['texts']['prevButton'] = feedback.back
            content['texts']['submitButton'] = feedback.submit

        return content, changes

    def _style_multi_choice(self, content: dict) -> tuple[dict, list[str]]:
        """
        MultiChoice: UI und Feedback
        """
        changes = []
        feedback = self.brand_config.feedback

        # Fuer eingebettete MultiChoice in QuestionSet
        if 'params' in content:
            params = content['params']
            if 'UI' in params:
                params['UI']['correctText'] = feedback.correct
                params['UI']['incorrectText'] = feedback.wrong
                params['UI']['tryAgainButton'] = feedback.try_again
                params['UI']['showSolutionButton'] = feedback.show_solution
                params['UI']['checkAnswerButton'] = feedback.check
                changes.append("MultiChoice UI-Texte aktualisiert")

        return content, changes

    def _style_true_false(self, content: dict) -> tuple[dict, list[str]]:
        """
        TrueFalse: Feedback-Texte
        """
        changes = []
        feedback = self.brand_config.feedback

        if 'params' in content:
            content['params']['feedbackOnCorrect'] = feedback.correct
            content['params']['feedbackOnWrong'] = feedback.wrong
            changes.append("TrueFalse Feedback aktualisiert")

        return content, changes

    def _style_blanks(self, content: dict) -> tuple[dict, list[str]]:
        """
        Fill in the Blanks: Feedback
        """
        changes = []

        content['overallFeedback'] = self._create_feedback_ranges()
        content['tryAgain'] = self.brand_config.feedback.try_again
        content['showSolutions'] = self.brand_config.feedback.show_solution
        content['checkAnswer'] = self.brand_config.feedback.check
        changes.append("Blanks Feedback aktualisiert")

        return content, changes

    def _style_dialog_cards(self, content: dict) -> tuple[dict, list[str]]:
        """
        DialogCards/Flashcards: Begrenzte Styling-Optionen
        """
        changes = []
        feedback = self.brand_config.feedback

        # UI-Texte aktualisieren
        content['retry'] = feedback.try_again
        content['next'] = feedback.next
        content['prev'] = feedback.back
        changes.append("Flashcards UI-Texte aktualisiert")

        return content, changes

    def _style_accordion(self, content: dict) -> tuple[dict, list[str]]:
        """
        Accordion: Minimale Styling-Optionen
        """
        # Accordion hat kaum Styling-Optionen in H5P
        return content, []

    def _style_timeline(self, content: dict) -> tuple[dict, list[str]]:
        """
        Timeline: Begrenzte Unterstuetzung
        """
        # Timeline nutzt TimelineJS - begrenzte Anpassung moeglich
        return content, []

    def _style_drag_text(self, content: dict) -> tuple[dict, list[str]]:
        """
        DragText: Feedback und UI
        """
        changes = []
        feedback = self.brand_config.feedback

        content['overallFeedback'] = self._create_feedback_ranges()
        content['tryAgain'] = feedback.try_again
        content['showSolution'] = feedback.show_solution
        content['checkAnswer'] = feedback.check
        content['correctText'] = feedback.correct
        content['incorrectText'] = feedback.wrong
        changes.append("DragText Feedback aktualisiert")

        return content, changes

    def _style_mark_words(self, content: dict) -> tuple[dict, list[str]]:
        """
        MarkTheWords: Feedback
        """
        changes = []
        feedback = self.brand_config.feedback

        content['overallFeedback'] = self._create_feedback_ranges()
        content['tryAgainButton'] = feedback.try_again
        content['showSolutionButton'] = feedback.show_solution
        content['checkAnswerButton'] = feedback.check
        changes.append("MarkTheWords Feedback aktualisiert")

        return content, changes

    def _style_summary(self, content: dict) -> tuple[dict, list[str]]:
        """
        Summary: Feedback
        """
        changes = []
        feedback = self.brand_config.feedback

        content['overallFeedback'] = self._create_feedback_ranges()
        content['labelCorrect'] = feedback.correct
        content['labelIncorrect'] = feedback.wrong
        changes.append("Summary Feedback aktualisiert")

        return content, changes

    def _style_single_choice_set(self, content: dict) -> tuple[dict, list[str]]:
        """
        SingleChoiceSet: Feedback und Lokalisierung
        """
        changes = []
        feedback = self.brand_config.feedback

        content['overallFeedback'] = self._create_feedback_ranges()

        if 'l10n' in content:
            content['l10n']['correctText'] = feedback.correct
            content['l10n']['incorrectText'] = feedback.wrong
            content['l10n']['retryButtonLabel'] = feedback.try_again
            content['l10n']['showSolutionButtonLabel'] = feedback.show_solution
            changes.append("SingleChoiceSet Lokalisierung aktualisiert")

        # Pass-Percentage
        if 'behaviour' in content:
            content['behaviour']['passPercentage'] = self.brand_config.pass_percentage

        return content, changes

    # =========================================================================
    # Container Styling (v3.0)
    # =========================================================================

    CONTAINER_HANDLERS = {
        'H5P.InteractiveBook': '_style_interactive_book',
        'H5P.CoursePresentation': '_style_course_presentation',
        'H5P.Column': '_style_column',
    }

    def _style_interactive_book(self, content: dict) -> tuple[dict, list[str]]:
        """InteractiveBook: baseColor und Navigation"""
        changes = []
        colors = self.brand_config.colors

        if 'behaviour' not in content:
            content['behaviour'] = {}
        content['behaviour']['baseColor'] = colors.primary
        content['behaviour']['progressIndicators'] = True
        content['behaviour']['progressAuto'] = True
        changes.append(f"InteractiveBook baseColor: {colors.primary}")

        return content, changes

    def _style_course_presentation(self, content: dict) -> tuple[dict, list[str]]:
        """CoursePresentation: Slide-Styling"""
        changes = []
        # CoursePresentation hat keine direkten Farb-Optionen,
        # Styling erfolgt ueber CSS-Injection
        return content, changes

    def _style_column(self, content: dict) -> tuple[dict, list[str]]:
        """Column: Keine direkten Farb-Optionen"""
        return content, []

    # =========================================================================
    # CSS Injection (v3.0)
    # =========================================================================

    def _inject_custom_css(self, temp_path: Path, h5p_meta: dict) -> list[str]:
        """
        Bettet Custom-CSS in H5P-Package ein.

        Strategie: CSS als <style> Block in AdvancedText-Elemente injizieren.
        Dies funktioniert zuverlaessiger als preloadedCss, da es keine
        Library-Installation auf dem H5P-Host erfordert.
        """
        changes = []

        # CSS laden
        css_path = self.BSWI_CSS_PATH
        if not css_path.exists():
            return changes

        # Nur fuer BS:WI Brand
        if self.brand_config.name != "BS:WI Hamburg":
            return changes

        css_content = css_path.read_text(encoding='utf-8')

        # CSS in content.json als Style-Block injizieren
        content_json_path = temp_path / "content" / "content.json"
        if content_json_path.exists():
            with open(content_json_path, 'r', encoding='utf-8') as f:
                content = json.load(f)

            # Style-Block der in AdvancedText eingebettet wird
            style_block = f'<style>{css_content}</style>'

            # In verschiedene Content-Strukturen injizieren
            injected = self._inject_style_into_content(content, style_block)

            if injected:
                with open(content_json_path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)
                changes.append("BS:WI CSS injiziert")

        return changes

    def _inject_style_into_content(self, content: dict, style_block: str) -> bool:
        """
        Injiziert Style-Block in den ersten AdvancedText-Inhalt.
        Durchsucht verschachtelte Strukturen (Column, InteractiveBook, etc.)
        """
        # Direkt: AdvancedText mit text-Feld
        if 'text' in content and isinstance(content['text'], str):
            if '<style>' not in content['text']:
                content['text'] = style_block + content['text']
                return True

        # Column: content[].content.params.text
        if 'content' in content and isinstance(content['content'], list):
            for item in content['content']:
                inner = item.get('content', {})
                params = inner.get('params', {})
                if 'text' in params and isinstance(params['text'], str):
                    if '<style>' not in params['text']:
                        params['text'] = style_block + params['text']
                        return True

        # InteractiveBook: chapters[].chapter.params.content[].content.params.text
        if 'chapters' in content and isinstance(content['chapters'], list):
            for chapter in content['chapters']:
                ch = chapter.get('chapter', {})
                ch_params = ch.get('params', {})
                ch_content = ch_params.get('content', [])
                if isinstance(ch_content, list):
                    for item in ch_content:
                        inner = item.get('content', {})
                        params = inner.get('params', {})
                        if 'text' in params and isinstance(params['text'], str):
                            if '<style>' not in params['text']:
                                params['text'] = style_block + params['text']
                                return True

        # CoursePresentation: presentation.slides[].elements[].action.params.text
        if 'presentation' in content:
            slides = content.get('presentation', {}).get('slides', [])
            for slide in slides:
                for elem in slide.get('elements', []):
                    action = elem.get('action', {})
                    params = action.get('params', {})
                    if 'text' in params and isinstance(params['text'], str):
                        if '<style>' not in params['text']:
                            params['text'] = style_block + params['text']
                            return True

        # QuestionSet: introPage.introduction
        if 'introPage' in content:
            intro = content['introPage'].get('introduction', '')
            if isinstance(intro, str) and '<style>' not in intro:
                content['introPage']['introduction'] = style_block + intro
                return True

        return False

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _create_feedback_ranges(self) -> list[dict]:
        """Erstellt Standard-Feedback-Ranges"""
        feedback = self.brand_config.feedback
        return [
            {"from": 0, "to": 50, "feedback": feedback.wrong},
            {"from": 51, "to": 80, "feedback": feedback.partial},
            {"from": 81, "to": 100, "feedback": feedback.correct}
        ]

    def _apply_generic_styling(self, content: dict) -> tuple[dict, list[str]]:
        """
        Wendet generisches Styling an wenn kein spezifischer Handler existiert.
        """
        changes = []
        feedback = self.brand_config.feedback

        # Versuche overallFeedback zu setzen wenn vorhanden
        if 'overallFeedback' in content:
            content['overallFeedback'] = self._create_feedback_ranges()
            changes.append("Generisches Feedback aktualisiert")

        # Versuche gaengige UI-Keys zu aktualisieren
        ui_mappings = {
            'tryAgain': feedback.try_again,
            'showSolution': feedback.show_solution,
            'showSolutions': feedback.show_solution,
            'checkAnswer': feedback.check,
            'submit': feedback.submit,
            'next': feedback.next,
            'prev': feedback.back,
            'retry': feedback.try_again,
        }

        for key, value in ui_mappings.items():
            if key in content:
                content[key] = value

        return content, changes

    def _embed_logo(self, temp_path: Path, content: dict) -> list[str]:
        """
        Bettet Logo in H5P-Content ein.

        Note: Logo-Embedding ist nur fuer bestimmte Typen sinnvoll
        und erfordert HTML-Manipulation. Aktuell Placeholder.
        """
        # Logo-Embedding ist komplex und erfordert:
        # 1. Bild herunterladen und in content/images speichern
        # 2. HTML in Text-Feldern anpassen
        # Diese Funktion ist ein Placeholder fuer zukuenftige Implementierung
        return []

    def _repackage_h5p(self, source_dir: Path, output_path: Path):
        """
        Verpackt extrahierte H5P-Dateien zurueck in ZIP.
        """
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(source_dir)
                    zf.write(file_path, arcname)
