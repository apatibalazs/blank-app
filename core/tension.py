# core/tension.py
from typing import List, Dict
from .types import AttentionVector, RuntimeState, Core9Point, FractureEvent
from .semantics import DictionaryEngine

class TensionResult:
    """A TensionEngine kimeneti objektuma"""
    def __init__(self):
        self.injections: List[Dict] = []
        self.tension_delta: float = 0.0
        self.entropy_increase: float = 0.0
        self.core9_strength: float = 0.0


class TensionEngine:
    """
    A Fern Pipeline 5. rétege.
    Aktívan generálja a kognitív súrlódást és paradoxonokat.
    """
    
    def __init__(self, dictionary_engine: DictionaryEngine):
        self.dictionary = dictionary_engine
        self.min_tension_threshold = 0.58
        self.fracture_sensitivity = 0.45
    
    def generate_tension(self, 
                        attention_vectors: List[AttentionVector], 
                        state: RuntimeState) -> TensionResult:
        
        result = TensionResult()
        
        for vector in attention_vectors:
            concept = vector.concept
            
            # 1. Core9 ellenőrzés
            self._ensure_core9_compliance(concept)
            
            # 2. Ellentétpólusok keresése és feszültség injektálása
            opposites = self._find_opposites(concept)
            for opp in opposites:
                delta = self._inject_tension(concept, opp)
                result.tension_delta += delta
                
                if delta >= 0.72:
                    result.injections.append({
                        "type": "paradox_injection",
                        "source": concept.name,
                        "opposite": opp,
                        "strength": round(delta, 3),
                        "core9": [p.value for p in concept.core9_alignment]
                    })
            
            # 3. Ha még mindig alacsony a feszültség → Fracture
            current_tension = self._get_tension_level(concept)
            if current_tension < self.min_tension_threshold:
                try:
                    self.dictionary.analyze_concept(concept)
                except FractureEvent:
                    self._force_fracture(concept, state, result)
        
        # Globális állapot frissítése
        state.tension_gradient = min(1.0, state.tension_gradient + result.tension_delta * 0.38)
        state.entropy_level = min(1.0, state.entropy_level + len(result.injections) * 0.15)
        
        result.entropy_increase = state.entropy_level
        result.core9_strength = self._calculate_core9_strength(attention_vectors)
        
        return result
    
    def _ensure_core9_compliance(self, concept: ConceptNode):
        """Biztosítjuk, hogy a feszültség generálás is hordozza a Core9 szellemiségét"""
        tension_points = {
            Core9Point.COGNITIVE_FRICTION,
            Core9Point.CONTRADICTION,
            Core9Point.TENSION_GENERATION
        }
        if not any(p in concept.core9_alignment for p in tension_points):
            concept.core9_alignment.append(Core9Point.COGNITIVE_FRICTION)
    
    def _find_opposites(self, concept: ConceptNode) -> List[str]:
        """Ellentétpólusok generálása"""
        opposites_map = {
            "szabadság": ["kényszer", "felelősség", "korlát"],
            "igazság": ["illúzió", "hatalom", "relativitás"],
            "tudat": ["anyag", "gépezet", "véletlen"],
            "idő": ["pillanat", "örökkévalóság"],
            "félelem": ["bátorság", "biztonság"]
        }
        
        lower = concept.name.lower()
        return opposites_map.get(lower, ["ellentét", "korlát", "ellentmondás"])
    
    def _inject_tension(self, concept: ConceptNode, opposite: str) -> float:
        """Feszültség vektor létrehozása"""
        strength = 0.65 + (concept.grounding_score * 0.35)
        concept.add_tension(opposite, strength)
        return strength
    
    def _get_tension_level(self, concept: ConceptNode) -> float:
        if not concept.tension_field:
            return 0.0
        return sum(concept.tension_field.values()) / len(concept.tension_field)
    
    def _force_fracture(self, concept: ConceptNode, state: RuntimeState, result: TensionResult):
        """Kényszerített törés"""
        state.entropy_level += 0.4
        result.injections.append({
            "type": "forced_fracture",
            "concept": concept.name,
            "reason": "insufficient_tension"
        })
    
    def _calculate_core9_strength(self, vectors: List[AttentionVector]) -> float:
        if not vectors:
            return 0.0
        total = sum(len(v.concept.core9_alignment) for v in vectors)
        return total / (len(vectors) * len(Core9Point))
