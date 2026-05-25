# core/kernel.py
from typing import List, Dict, Optional
from .types import RuntimeState, ConceptNode, AttentionVector, FractureEvent
from .semantics import DictionaryEngine
from .attention import AttentionMapping
from .tension import TensionEngine, TensionResult

class FernPipeline:
    """
    A Cognito KORS központi orchestratora.
    Összefogja az 1-5. réteget egy teljes kognitív ciklusba.
    """
    
    def __init__(self):
        self.dictionary = DictionaryEngine()
        self.attention_mapping = AttentionMapping()
        self.tension_engine = TensionEngine(self.dictionary)
        
        # Kezdeti állapot
        self.state = RuntimeState(
            tension_gradient=0.35,
            entropy_level=0.25,
            dna_style={"default": 1.0},
            active_anchors={},
            cycle_count=0
        )
    
    def run_cycle(self, 
                  input_text: str, 
                  task_context: Optional[Dict] = None) -> Dict:
        """
        Egy teljes Fern Pipeline ciklus lefuttatása.
        """
        self.state.cycle_count += 1
        cycle_log = {"cycle": self.state.cycle_count, "input": input_text[:120]}
        
        try:
            # 1-2. Input Ingestion + Stability (egyszerűsített)
            processed = self._preprocess_input(input_text)
            
            # 2-3. DictionaryEngine + Ontological Grounding
            concepts = self._extract_concepts(processed)
            grounding_results = self.dictionary.batch_analyze(concepts, self.state)
            
            # 4. Attention Mapping
            attention_map: List[AttentionVector] = self.attention_mapping.generate(
                grounding_results, self.state, task_context
            )
            
            # 5. Tension Generation
            tension_result: TensionResult = self.tension_engine.generate_tension(
                attention_map, self.state
            )
            
            # Összefoglaló eredmény
            return {
                "status": "success",
                "cycle": self.state.cycle_count,
                "tension_gradient": round(self.state.tension_gradient, 3),
                "entropy_level": round(self.state.entropy_level, 3),
                "focus_concepts": [v.concept.name for v in attention_map],
                "injections": tension_result.injections,
                "core9_coverage": self._get_core9_coverage(),
                "residual_tension": round(self.state.residual_tension_history[-1], 3) 
                                    if self.state.residual_tension_history else 0.0,
                "next_phase": "council" if self.state.tension_gradient > 0.65 else "continue"
            }
            
        except FractureEvent as e:
            return self._handle_fracture(e, input_text, task_context)
        
        except Exception as e:
            return {
                "status": "error",
                "cycle": self.state.cycle_count,
                "message": str(e)
            }
    
    def _preprocess_input(self, text: str) -> str:
        """Egyszerű bemenet előkészítés"""
        return text.strip()
    
    def _extract_concepts(self, text: str) -> List[ConceptNode]:
        """Egyszerű fogalom kinyerés"""
        import re
        words = re.findall(r'\w+', text.lower())
        concepts = []
        
        for word in set(words):
            if len(word) > 3:
                node = ConceptNode(name=word, created_at_cycle=self.state.cycle_count)
                concepts.append(node)
        
        return concepts[:10]  # max 10 fogalom ciklusonként
    
    def _handle_fracture(self, 
                        event: FractureEvent, 
                        original_input: str, 
                        task_context: Optional[Dict]) -> Dict:
        """FractureEvent kezelése"""
        self.state.entropy_level = min(1.0, self.state.entropy_level + 0.45)
        self.state.tension_gradient = min(1.0, self.state.tension_gradient + 0.4)
        
        return {
            "status": "fracture_triggered",
            "message": str(event),
            "concept": getattr(event, 'concept', None),
            "tension_gradient": round(self.state.tension_gradient, 3),
            "entropy_level": round(self.state.entropy_level, 3),
            "action": "increased tension and restarting cycle",
            "cycle": self.state.cycle_count
        }
    
    def _get_core9_coverage(self) -> Dict[str, float]:
        """Core9 lefedettség áttekintése"""
        if not self.state.core9_registry:
            return {"coverage": 0.0}
        
        total = sum(self.state.core9_registry.values())
        return {point.value: round(val / max(self.state.cycle_count, 1), 3) 
                for point, val in self.state.core9_registry.items()}
    
    def set_dna_style(self, style: Dict[str, float]):
        """Stílusvektor beállítása"""
        self.state.dna_style = style
