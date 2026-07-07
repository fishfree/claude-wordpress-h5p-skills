"""
Brand Configuration for H5P Design Agent

Provides branding presets and configuration dataclasses for applying
consistent corporate identity to H5P content.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ColorScheme:
    """Farbschema fuer CI"""
    primary: str = "#1a73e8"          # Hauptfarbe (Buttons, Akzente)
    secondary: str = "#5f6368"        # Sekundaerfarbe
    success: str = "#34a853"          # Richtige Antworten
    error: str = "#ea4335"            # Falsche Antworten
    warning: str = "#fbbc04"          # Warnungen
    background: str = "#ffffff"       # Hintergrund
    text: str = "#202124"             # Textfarbe
    text_light: str = "#5f6368"       # Sekundaerer Text


@dataclass
class LogoConfig:
    """Logo-Konfiguration"""
    logo_url: Optional[str] = None    # URL zum Logo
    position: str = "top-left"        # top-left, top-right, top-center
    max_width: int = 120              # Max Breite in Pixeln
    margin: int = 10                  # Abstand in Pixeln


@dataclass
class FeedbackTexts:
    """Lokalisierte Feedback-Texte"""
    correct: str = "Richtig! Gut gemacht!"
    wrong: str = "Leider falsch. Versuche es nochmal!"
    partial: str = "Teilweise richtig."
    try_again: str = "Nochmal versuchen"
    show_solution: str = "Loesung anzeigen"
    check: str = "Pruefen"
    submit: str = "Absenden"
    next: str = "Weiter"
    back: str = "Zurueck"
    finish: str = "Fertig"


@dataclass
class TypographyConfig:
    """Typografie-Einstellungen"""
    font_family: str = "Arial, sans-serif"
    font_size_base: str = "16px"
    font_size_heading: str = "20px"
    line_height: str = "1.5"


@dataclass
class BrandConfig:
    """
    Vollstaendige Brand-Konfiguration.

    Kombiniert alle CI-Aspekte:
    - Farben
    - Logo
    - Feedback-Texte (lokalisiert)
    - Typografie
    - Theme (vordefinierter Stil)
    """
    name: str = "Default"
    colors: ColorScheme = field(default_factory=ColorScheme)
    logo: LogoConfig = field(default_factory=LogoConfig)
    feedback: FeedbackTexts = field(default_factory=FeedbackTexts)
    typography: TypographyConfig = field(default_factory=TypographyConfig)
    theme: str = "default"            # education, professional, minimal, dark
    pass_percentage: int = 60         # Bestehensgrenze in Prozent

    def to_h5p_style_dict(self) -> dict:
        """Konvertiert zu H5P-kompatiblem Style-Dict"""
        return {
            "primary_color": self.colors.primary,
            "success_color": self.colors.success,
            "error_color": self.colors.error,
            "background_color": self.colors.background,
            "text_color": self.colors.text,
            "font_family": self.typography.font_family,
            "font_size": self.typography.font_size_base,
            "feedback_correct": self.feedback.correct,
            "feedback_wrong": self.feedback.wrong,
            "feedback_partial": self.feedback.partial,
            "pass_percentage": self.pass_percentage,
        }


# =============================================================================
# Brand Presets
# =============================================================================

BRAND_PRESETS = {
    "default": BrandConfig(
        name="Default",
        theme="default"
    ),

    "bswi": BrandConfig(
        name="BS:WI Hamburg",
        colors=ColorScheme(
            primary="#003366",        # Navy - Buttons, Navigation, Ueberschriften
            secondary="#00A3E0",      # Lightblue - Links, Fortschrittsbalken, Akzente
            success="#B5E505",        # Yellow - Erfolg, Highlights
            error="#dc3545",          # Rot
            warning="#B5E505",        # Yellow
            background="#F5F5F5",     # Helles Grau
            text="#333333",           # Textfarbe
            text_light="#666666",
        ),
        logo=LogoConfig(
            logo_url=None,            # Logo wird ueber CSS eingebettet
            position="top-left",
            max_width=150
        ),
        feedback=FeedbackTexts(
            correct="Super! Das ist richtig!",
            wrong="Das war leider nicht korrekt. Schau dir die Loesung an.",
            partial="Teilweise richtig. Schau nochmal genau hin.",
            try_again="Nochmal versuchen",
            show_solution="Loesung anzeigen",
        ),
        typography=TypographyConfig(
            font_family="Arial, Helvetica, sans-serif",
            font_size_base="16px",
        ),
        theme="education",
        pass_percentage=50
    ),

    "hnh": BrandConfig(
        name="High Nord Club Hamburg e.V.",
        colors=ColorScheme(
            primary="#003366",        # Navy - High Nord Hauptfarbe
            secondary="#00A3E0",      # Tuerkis
            success="#4CAF50",        # Gruen
            error="#ea4335",          # Rot
            warning="#FFD700",        # Gold
            background="#ffffff",     # Weiss
            text="#333333",           # Dunkelgrau
            text_light="#666666",
        ),
        logo=LogoConfig(
            logo_url=None,            # Kein Logo in H5P
            position="top-left",
            max_width=120
        ),
        feedback=FeedbackTexts(
            correct="Richtig! Super gemacht!",
            wrong="Das war leider nicht korrekt. Schau dir die Loesung nochmal an.",
            partial="Teilweise richtig. Du bist auf dem richtigen Weg!",
            try_again="Nochmal versuchen",
            show_solution="Loesung anzeigen",
        ),
        typography=TypographyConfig(
            font_family="Arial, Helvetica, sans-serif",
            font_size_base="16px",
        ),
        theme="education",
        pass_percentage=80           # 80% Bestehensgrenze
    ),

    "minimal": BrandConfig(
        name="Minimal",
        colors=ColorScheme(
            primary="#333333",
            secondary="#666666",
            success="#4caf50",
            error="#f44336",
            background="#ffffff",
            text="#333333",
        ),
        feedback=FeedbackTexts(
            correct="Korrekt.",
            wrong="Falsch.",
            partial="Teilweise.",
        ),
        typography=TypographyConfig(
            font_family="'Helvetica Neue', Helvetica, Arial, sans-serif",
        ),
        theme="minimal"
    ),

    "dark": BrandConfig(
        name="Dark Mode",
        colors=ColorScheme(
            primary="#8ab4f8",         # Helles Blau
            secondary="#aecbfa",
            success="#81c995",         # Helles Gruen
            error="#f28b82",           # Helles Rot
            warning="#fdd663",
            background="#202124",      # Dunkler Hintergrund
            text="#e8eaed",            # Heller Text
            text_light="#9aa0a6",
        ),
        feedback=FeedbackTexts(
            correct="Richtig!",
            wrong="Nicht ganz. Versuch es nochmal.",
            partial="Fast!",
        ),
        theme="dark"
    ),

    "professional": BrandConfig(
        name="Professional",
        colors=ColorScheme(
            primary="#1976d2",         # Material Blue
            secondary="#455a64",
            success="#388e3c",
            error="#d32f2f",
            background="#fafafa",
            text="#212121",
        ),
        typography=TypographyConfig(
            font_family="'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
            font_size_base="15px",
        ),
        feedback=FeedbackTexts(
            correct="Korrekte Antwort.",
            wrong="Ihre Antwort war nicht korrekt.",
            partial="Teilweise korrekt.",
        ),
        theme="professional"
    ),

    "accessible": BrandConfig(
        name="Accessible (High Contrast)",
        colors=ColorScheme(
            primary="#0000ff",         # Reines Blau
            secondary="#000080",
            success="#008000",         # Reines Gruen
            error="#ff0000",           # Reines Rot
            background="#ffffff",
            text="#000000",            # Schwarz auf Weiss
        ),
        typography=TypographyConfig(
            font_size_base="18px",     # Groessere Schrift
            line_height="1.8",
        ),
        feedback=FeedbackTexts(
            correct="RICHTIG!",
            wrong="FALSCH!",
            partial="TEILWEISE RICHTIG!",
        ),
        theme="accessible",
        pass_percentage=50
    ),
}


def get_brand_preset(name: str) -> BrandConfig:
    """
    Holt ein vordefiniertes Brand-Preset.

    Args:
        name: Name des Presets (bswi, minimal, dark, professional, accessible)

    Returns:
        BrandConfig Instanz

    Raises:
        KeyError: Wenn Preset nicht existiert
    """
    if name not in BRAND_PRESETS:
        available = ", ".join(BRAND_PRESETS.keys())
        raise KeyError(f"Brand preset '{name}' nicht gefunden. Verfuegbar: {available}")
    return BRAND_PRESETS[name]


def list_brand_presets() -> list[str]:
    """Gibt Liste aller verfuegbaren Preset-Namen zurueck"""
    return list(BRAND_PRESETS.keys())


def create_brand_config(
    name: str,
    primary_color: str = None,
    logo_url: str = None,
    feedback_correct: str = None,
    feedback_wrong: str = None,
    theme: str = "default",
    **kwargs
) -> BrandConfig:
    """
    Factory-Funktion fuer einfache Brand-Erstellung.

    Args:
        name: Name der Brand
        primary_color: Hauptfarbe (hex)
        logo_url: URL zum Logo
        feedback_correct: Feedback bei richtiger Antwort
        feedback_wrong: Feedback bei falscher Antwort
        theme: Theme-Name
        **kwargs: Weitere Optionen

    Returns:
        BrandConfig Instanz
    """
    colors = ColorScheme()
    if primary_color:
        colors.primary = primary_color

    logo = LogoConfig()
    if logo_url:
        logo.logo_url = logo_url

    feedback = FeedbackTexts()
    if feedback_correct:
        feedback.correct = feedback_correct
    if feedback_wrong:
        feedback.wrong = feedback_wrong

    return BrandConfig(
        name=name,
        colors=colors,
        logo=logo,
        feedback=feedback,
        theme=theme,
        pass_percentage=kwargs.get('pass_percentage', 60)
    )
