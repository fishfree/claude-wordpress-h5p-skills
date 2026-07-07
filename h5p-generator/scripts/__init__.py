"""
H5P Multi-Agent System

Ein intelligentes System zur automatischen Generierung von H5P-Inhalten
aus Lernmaterialien mit Multi-Agent-Architektur und Branding-Support.

Quick Start:
    from scripts import H5PSystem

    system = H5PSystem(brand='bswi')
    result = system.generate_from_text('''
        ## Lernziele
        - Schueler koennen Scrum-Rollen nennen
    ''')

Architektur:
    - H5PSystem: Unified API (Haupteinstiegspunkt)
    - H5POrchestrator: Multi-Agent Koordination
    - Sub-Agents: Quiz, Card, Drag, Design
    - Brand-Config: CI/Branding-Presets
"""

__version__ = "2.0.0"
__author__ = "Claude Code"

# Main API
from .h5p_system import (
    H5PSystem,
    SystemResult,
    quick_generate,
    quick_flashcards,
    quick_quiz,
    quick_drag_drop,
)

# Orchestrator
from .orchestrator import (
    H5POrchestrator,
    OrchestratorResult,
    ContentAnalysis,
    ExecutionPlan,
    ContentStructure,
    Complexity,
)

# Sub-Agents
from .sub_agents import (
    BaseH5PAgent,
    AgentResult,
    QuizAgent,
    CardAgent,
    DragAgent,
    DesignAgent,
    DesignResult,
)

# Brand Configuration
from .brand_config import (
    BrandConfig,
    ColorScheme,
    LogoConfig,
    FeedbackTexts,
    get_brand_preset,
    list_brand_presets,
    create_brand_config,
    BRAND_PRESETS,
)

# Low-level Generators
from .h5p_generator import (
    H5PResult,
    H5PStyle,
    THEMES,
    create_true_false,
    create_multi_choice,
    create_fill_blanks,
    create_drag_drop,
    create_single_choice,
    create_flashcards,
    create_mark_words,
    create_summary,
    create_accordion,
    create_drag_text,
    create_timeline,
    create_memory_game,
    batch_create,
)

__all__ = [
    # Version
    '__version__',

    # Main API
    'H5PSystem',
    'SystemResult',
    'quick_generate',
    'quick_flashcards',
    'quick_quiz',
    'quick_drag_drop',

    # Orchestrator
    'H5POrchestrator',
    'OrchestratorResult',
    'ContentAnalysis',
    'ExecutionPlan',
    'ContentStructure',
    'Complexity',

    # Sub-Agents
    'BaseH5PAgent',
    'AgentResult',
    'QuizAgent',
    'CardAgent',
    'DragAgent',
    'DesignAgent',
    'DesignResult',

    # Brand Configuration
    'BrandConfig',
    'ColorScheme',
    'LogoConfig',
    'FeedbackTexts',
    'get_brand_preset',
    'list_brand_presets',
    'create_brand_config',
    'BRAND_PRESETS',

    # Low-level Generators
    'H5PResult',
    'H5PStyle',
    'THEMES',
    'create_true_false',
    'create_multi_choice',
    'create_fill_blanks',
    'create_drag_drop',
    'create_single_choice',
    'create_flashcards',
    'create_mark_words',
    'create_summary',
    'create_accordion',
    'create_drag_text',
    'create_timeline',
    'create_memory_game',
    'batch_create',
]
