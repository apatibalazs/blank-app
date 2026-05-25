# core/semantics.py
from typing import List, Dict, Optional
from .types import ConceptNode, Core9Point, FractureEvent, RuntimeState
import random

class GroundingGraph:
    """Ontológiai horgonyok és primitívek gráfja"""
    
    def __init__(self):
        self.nodes: Dict[str, ConceptNode] = {}
        self.primitive_core = [
            "test", "idő", "fájdalom", "halál", "mozgás", "látás", 
            "hang", "érintés", "éhség", "félelem", "öröm", "kényszer"
        ]
        self._initialize_primitives()
    
    def _initialize_primitives(self):
        for name in self.primitive_core:
            node = ConceptNode(
                name=name,
                is_primitive=True,
                grounding_score=1.0,
                core9_alignment=[Core9Point.ONTOLOGICAL_GROUNDING]
            )
            self.nodes[name] = node
    
    def distance_to_primitives(self, concept_name: str) -> float:
        if concept_name in self.nodes and self.nodes[concept_name].is_primitive:
            return 0.0
        if concept_name in self.nodes:
            return 1.0 - self.nodes[concept_name].grounding_score
        return 0.85  # ismeretlen fogalom


class DictionaryEngine:
    """A Cognito epistemológiai határőre és Core9 auditora"""
    
    def __init__(self):
        self.graph = GroundingGraph()
        self.tension_threshold = 0.45
        self.coherence_threshold = 0.52
    
    def analyze_concept(self, concept: ConceptNode, context: Optional[Dict] = None) -> ConceptNode:
        """Egy fogalom teljes elemzése"""
        
        # Grounding számítás
        prim_dist = self.graph.distance_to_primitives(concept.name)
        concept.grounding_score = max(0.0, 1.0 - prim_dist * 0.7)
        
        # Core9 validáció
        if not concept.validate_core9():
            raise FractureEvent(
                message=f"Core9 Audit sikertelen: '{concept.name}'",
                concept=concept.name,
                grounding_score=concept.grounding_score
            )
        
        # Wittgenstein-határ ellenőrzés
        if concept.grounding_score < self.tension_threshold:
            raise FractureEvent(
                message=f"Gyenge ontológiai horgony: '{concept.name}' (score: {concept.grounding_score:.2f})",
                concept=concept.name,
                grounding_score=concept.grounding_score
            )
        
        # Feszültség mező gazdagítása
        self._enrich_tension_field(concept)
        
        self.graph.nodes[concept.name] = concept
        return concept
    
    def _enrich_tension_field(self, concept: ConceptNode):
        """Automatikus ellentétpárok"""
        opposites_map = {
            "szabadság": ["kényszer", "felelősség"],
            "igazság": ["illúzió", "hatalom"],
            "tudat": ["anyag", "gépezet"],
            "idő": ["pillanat", "örökkévalóság"]
        }
        
        lower = concept.name.lower()
        if lower in opposites_map:
            for opp in opposites_map[lower]:
                concept.add_tension(opp, 0.75)
    
    def batch_analyze(self, concepts: List[ConceptNode], state: RuntimeState) -> List[ConceptNode]:
        """Több fogalom elemzése"""
        results = []
        for concept in concepts:
            try:
                analyzed = self.analyze_concept(concept)
                results.append(analyzed)
                
                # Core9 registry frissítése
                for point in analyzed.core9_alignment:
                    state.core9_registry[point] = state.core9_registry.get(point, 0.0) + 0.25
                    
            except FractureEvent as e:
                concept.grounding_score = 0.3
                results.append(concept)
                # Továbbdobjuk, a kernel fogja kezelni
                raise
        
        return results
