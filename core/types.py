# core/types.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import uuid

class Core9Point(Enum):
    FRACTALITY = "Fraktalitás_és_önmagába_térés"
    CONTRADICTION = "Ellentmondás_generálás_és_megőrzés"
    COGNITIVE_FRICTION = "Kognitív_súrlódás_és_feszültség"
    PARADOX_RETENTION = "Paradoxon_megőrzése_feloldás_nélkül"
    ATTRACTOR_INTERFERENCE = "Belső_vonzók_ütköztetése"
    ONTOLOGICAL_GROUNDING = "Valóságos_lehorgonyzás"
    ATTENTION_FOCUS = "Dinamikus_figyelem_irányítás"
    TENSION_GENERATION = "Aktív_feszültség_teremtés"
    SYNTHESIS = "Kristályosodás_és_új_struktúra"


@dataclass
class ConceptNode:
    """A rendszer alapvető kognitív egysége"""
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    embedding: Optional[List[float]] = None
    tension_field: Dict[str, float] = field(default_factory=dict)
    grounding_score: float = 0.0
    is_primitive: bool = False
    core9_alignment: List[Core9Point] = field(default_factory=list)
    created_at_cycle: int = 0
    residual_tension: float = 0.0  # Új: maradék feszültség nyomon követése

    def validate_core9(self) -> bool:
        """Core9 Audit – beépített validáció"""
        if not self.core9_alignment:
            # Alapértelmezett minimális alignment
            self.core9_alignment = [
                Core9Point.ONTOLOGICAL_GROUNDING,
                Core9Point.COGNITIVE_FRICTION
            ]
            return False
        
        # Kötelező minimum
        required = {
            Core9Point.ONTOLOGICAL_GROUNDING,
            Core9Point.COGNITIVE_FRICTION,
            Core9Point.CONTRADICTION
        }
        
        covered = set(self.core9_alignment)
        return len(covered & required) >= 2 and len(covered) >= 3

    def add_tension(self, opposite: str, strength: float = 0.75):
        """Feszültség hozzáadása + residual tension növelése"""
        self.tension_field[opposite] = max(
            self.tension_field.get(opposite, 0.0), 
            strength
        )
        self.residual_tension = max(self.residual_tension, strength)


class FractureEvent(Exception):
    """Kontrollált kognitív törés"""
    def __init__(self, message: str, concept: str = None, 
                 grounding_score: float = None, 
                 missing_core9: List[str] = None):
        self.concept = concept
        self.grounding_score = grounding_score
        self.missing_core9 = missing_core9 or []
        super().__init__(message)


@dataclass
class AttentionVector:
    concept: ConceptNode
    grounding_score: float
    tension_potential: float
    priority_score: float = 0.0
    core9_alignment: List[Core9Point] = field(default_factory=list)


@dataclass
class RuntimeState:
    """A rendszer pillanatnyi kognitív állapota"""
    tension_gradient: float          # ∇τ
    entropy_level: float = 0.2
    dna_style: Dict[str, float] = field(default_factory=dict)
    active_anchors: Dict[str, float] = field(default_factory=dict)
    cycle_count: int = 0
    core9_registry: Dict[Core9Point, float] = field(default_factory=dict)
    residual_tension_history: List[float] = field(default_factory=list)
    
    def update_residual_tension(self, value: float):
        self.residual_tension_history.append(value)
        if len(self.residual_tension_history) > 50:
            self.residual_tension_history.pop(0)
