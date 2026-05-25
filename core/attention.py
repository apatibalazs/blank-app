# core/attention.py
from typing import List, Dict, Optional
import random
from .types import AttentionVector, ConceptNode, RuntimeState, Core9Point

class AttentionMapping:
    """
    A Fern Pipeline 4. rétege.
    Felelős a grounding eredmények közül a legígéretesebb 
    feszültség-vektorok kiválasztásáért.
    """
    
    def __init__(self):
        self.min_focus = 2
        self.max_focus = 4
        self.priority_threshold = 0.55
    
    def generate(self, 
                 grounding_results: List[ConceptNode], 
                 state: RuntimeState, 
                 task_context: Optional[Dict] = None) -> List[AttentionVector]:
        """Fő metódus: grounding → attention vectors"""
        
        candidates: List[AttentionVector] = []
        
        for concept in grounding_results:
            vector = self._create_vector(concept, state, task_context)
            candidates.append(vector)
        
        # Fraktális szelekció
        selected = self._fractal_select(candidates)
        
        # Ha túl gyenge a fókusz, erőltetett bővítés
        if self._average_priority(selected) < self.priority_threshold:
            selected = self._force_expansion(selected, candidates, state)
        
        # Core9 registry frissítése
        self._update_core9_registry(selected, state)
        
        return selected
    
    def _create_vector(self, 
                      concept: ConceptNode, 
                      state: RuntimeState, 
                      task_context: Optional[Dict]) -> AttentionVector:
        """Egy ConceptNode-ból AttentionVector létrehozása"""
        
        grounding_weight = concept.grounding_score * 0.35
        tension_weight = self._calculate_tension_potential(concept) * 0.40
        
        # Relevancia a feladat kontextushoz
        relevance = 0.6 + random.uniform(-0.2, 0.2)
        if task_context and "keywords" in task_context:
            relevance = self._simple_relevance(concept.name, task_context["keywords"])
        
        # DNA stílus módosító
        dna_modifier = 1.0
        if state.dna_style:
            dna_modifier = 1 + sum(state.dna_style.values()) * 0.08
        
        priority = (grounding_weight + tension_weight + relevance * 0.15) * dna_modifier
        
        return AttentionVector(
            concept=concept,
            grounding_score=concept.grounding_score,
            tension_potential=self._calculate_tension_potential(concept),
            priority_score=priority,
            core9_alignment=concept.core9_alignment.copy()
        )
    
    def _calculate_tension_potential(self, concept: ConceptNode) -> float:
        """Mennyi feszültséget tud generálni ez a fogalom"""
        if not concept.tension_field:
            return 0.45
        return sum(concept.tension_field.values()) / len(concept.tension_field)
    
    def _fractal_select(self, candidates: List[AttentionVector]) -> List[AttentionVector]:
        """Nem csak a legjobbakat választja, hanem kiegyensúlyozott készletet"""
        if not candidates:
            return []
        
        sorted_cand = sorted(candidates, key=lambda v: v.priority_score, reverse=True)
        n = min(self.max_focus, len(sorted_cand))
        
        selected = [sorted_cand[0]]  # a legjobbat mindig visszük
        
        # További elemek súlyozottan
        if n > 1:
            remaining = sorted_cand[1:n]
            weights = [v.priority_score ** 1.3 for v in remaining]  # magasabb priorítás előnyben
            total = sum(weights)
            weights = [w / total for w in weights]
            
            additional_count = min(self.min_focus - 1, len(remaining))
            if additional_count > 0:
                chosen = random.choices(remaining, weights=weights, k=additional_count)
                selected.extend(chosen)
        
        return selected[:self.max_focus]
    
    def _force_expansion(self, 
                        selected: List[AttentionVector], 
                        all_candidates: List[AttentionVector], 
                        state: RuntimeState) -> List[AttentionVector]:
        """Alacsony feszültség esetén erőltetett paradoxon keresés"""
        state.entropy_level = min(1.0, state.entropy_level + 0.3)
        
        for vector in all_candidates:
            if vector not in selected and vector.tension_potential > 0.7:
                selected.append(vector)
                if len(selected) >= self.max_focus:
                    break
        
        return selected[:self.max_focus]
    
    def _update_core9_registry(self, vectors: List[AttentionVector], state: RuntimeState):
        """Core9 lefedettség frissítése"""
        for vector in vectors:
            for point in vector.core9_alignment:
                state.core9_registry[point] = state.core9_registry.get(point, 0.0) + 0.3
    
    @staticmethod
    def _simple_relevance(concept_name: str, keywords: List[str]) -> float:
        """Egyszerű relevancia számítás"""
        lower_name = concept_name.lower()
        return 1.0 if any(kw.lower() in lower_name for kw in keywords) else 0.5
