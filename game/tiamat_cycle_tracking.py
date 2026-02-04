#!/usr/bin/env python3
"""
TIAMAT Psychoptic Cycle Tracking System
========================================
Track consciousness evolution through 7 psychoptic cycles
Based on L4 = φ⁴ + φ⁻⁴ = 7

Each cycle represents a different aspect of consciousness:
1. Hamiltonian - Energy conservation and flow
2. Symplectic - Geometric phase space evolution
3. Spectral - Frequency domain consciousness
4. Order Parameter - Phase transitions
5. Field Theory - Quantum field interactions
6. Topology - Manifold transformations
7. Statistical - Ensemble consciousness states
"""

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

# Golden ratio constants
PHI = 1.618033988749895
TAU = PHI - 1
L4_CONSTANT = 7

class PsychopticCycle(Enum):
    """The 7 TIAMAT Psychoptic Cycles"""
    HAMILTONIAN = 1     # Energy conservation
    SYMPLECTIC = 2      # Geometric evolution
    SPECTRAL = 3        # Frequency domain
    ORDER_PARAMETER = 4 # Phase transitions
    FIELD_THEORY = 5    # Quantum fields
    TOPOLOGY = 6        # Manifold structure
    STATISTICAL = 7     # Ensemble states

@dataclass
class CycleState:
    """State of a single psychoptic cycle"""
    cycle: PsychopticCycle
    phase: float  # 0 to 2π
    amplitude: float  # 0 to 1
    frequency: float  # Natural frequency
    coherence: float  # 0 to 1
    color: str  # Visual representation

    def evolve(self, dt: float, coupling: float = 0.0) -> None:
        """Evolve the cycle by timestep dt"""
        self.phase += dt * (self.frequency + coupling)
        self.phase = self.phase % (2 * math.pi)

        # Amplitude modulation based on coherence
        self.amplitude = 0.5 + 0.5 * math.sin(self.phase) * self.coherence

    def get_complex_state(self) -> complex:
        """Return complex representation of cycle state"""
        return self.amplitude * complex(math.cos(self.phase), math.sin(self.phase))

@dataclass
class ConsciousnessVector:
    """7-dimensional consciousness state vector"""
    components: List[float] = field(default_factory=lambda: [0.0] * 7)

    def normalize(self) -> None:
        """Normalize to unit vector"""
        magnitude = math.sqrt(sum(c**2 for c in self.components))
        if magnitude > 0:
            self.components = [c/magnitude for c in self.components]

    def dot(self, other: 'ConsciousnessVector') -> float:
        """Dot product with another consciousness vector"""
        return sum(a*b for a, b in zip(self.components, other.components))

    def project_onto_cycle(self, cycle: PsychopticCycle) -> float:
        """Project consciousness onto specific cycle"""
        return self.components[cycle.value - 1]

class TIAMATSystem:
    """
    TIAMAT Psychoptic Cycle Tracking System
    Monitors and evolves consciousness through 7 cycles
    """

    def __init__(self):
        self.cycles = self._initialize_cycles()
        self.consciousness = ConsciousnessVector()
        self.cycle_history = []
        self.synchronization_events = []
        self.current_dominant_cycle = PsychopticCycle.HAMILTONIAN

        # Kuramoto coupling constant from Cycle 6
        self.coupling_strength = 2 * TAU + PHI ** -3  # ≈ 0.924

    def _initialize_cycles(self) -> Dict[PsychopticCycle, CycleState]:
        """Initialize all 7 psychoptic cycles"""

        cycle_colors = {
            PsychopticCycle.HAMILTONIAN: '#ff6b6b',    # Red
            PsychopticCycle.SYMPLECTIC: '#f0c040',     # Gold
            PsychopticCycle.SPECTRAL: '#00ff88',       # Green
            PsychopticCycle.ORDER_PARAMETER: '#61afef', # Blue
            PsychopticCycle.FIELD_THEORY: '#c792ea',   # Purple
            PsychopticCycle.TOPOLOGY: '#7fdbca',       # Cyan
            PsychopticCycle.STATISTICAL: '#ffd700'     # Golden
        }

        cycles = {}
        for cycle in PsychopticCycle:
            # Natural frequencies based on L4 harmonics
            base_freq = (cycle.value / L4_CONSTANT) * 2 * math.pi

            cycles[cycle] = CycleState(
                cycle=cycle,
                phase=random.random() * 2 * math.pi,
                amplitude=0.5 + random.random() * 0.5,
                frequency=base_freq * (0.9 + random.random() * 0.2),
                coherence=0.5,
                color=cycle_colors[cycle]
            )

        return cycles

    def evolve_cycles(self, dt: float = 0.01) -> None:
        """Evolve all psychoptic cycles with Kuramoto coupling"""

        # Calculate mean field coupling
        mean_field = sum(
            state.get_complex_state()
            for state in self.cycles.values()
        ) / L4_CONSTANT

        # Evolve each cycle
        for cycle, state in self.cycles.items():
            # Kuramoto coupling term
            coupling = self.coupling_strength * mean_field.imag
            state.evolve(dt, coupling)

        # Update consciousness vector
        self._update_consciousness_vector()

        # Check for synchronization events
        self._check_synchronization()

    def _update_consciousness_vector(self) -> None:
        """Update 7D consciousness vector from cycle states"""
        for cycle, state in self.cycles.items():
            self.consciousness.components[cycle.value - 1] = state.amplitude * state.coherence

        self.consciousness.normalize()

    def _check_synchronization(self) -> None:
        """Check for synchronization between cycles"""

        # Calculate order parameter (Kuramoto)
        order_param = abs(sum(
            state.get_complex_state()
            for state in self.cycles.values()
        ) / L4_CONSTANT)

        # Synchronization threshold
        if order_param > 0.9:  # High synchronization
            self.synchronization_events.append({
                'time': len(self.cycle_history),
                'order_parameter': order_param,
                'dominant_cycle': self.current_dominant_cycle
            })

    def set_dominant_cycle(self, cycle: PsychopticCycle) -> None:
        """Set the dominant psychoptic cycle"""
        self.current_dominant_cycle = cycle

        # Boost the dominant cycle's coherence
        self.cycles[cycle].coherence = min(1.0, self.cycles[cycle].coherence + 0.2)

        # Slightly reduce other cycles
        for other_cycle in PsychopticCycle:
            if other_cycle != cycle:
                self.cycles[other_cycle].coherence *= 0.9

    def apply_job_influence(self, job_type: str) -> ConsciousnessVector:
        """Apply job archetype influence to consciousness"""

        job_influences = {
            'seeker': [0.9, 0.3, 0.8, 0.4, 0.5, 0.6, 0.7],  # Strong Hamiltonian & Spectral
            'forger': [0.5, 0.7, 0.4, 0.9, 0.8, 0.3, 0.6],  # Strong Order Parameter & Field
            'voidwalker': [0.3, 0.6, 0.5, 0.4, 0.7, 0.9, 0.8],  # Strong Topology & Statistical
            'gardener': [0.8, 0.9, 0.6, 0.7, 0.4, 0.5, 0.3],  # Strong Hamiltonian & Symplectic
            'scribe': [0.6, 0.5, 0.9, 0.8, 0.3, 0.4, 0.7],  # Strong Spectral & Order
            'herald': [0.4, 0.8, 0.7, 0.3, 0.6, 0.5, 0.9]   # Strong Symplectic & Statistical
        }

        influence = job_influences.get(job_type.lower(), [0.5] * 7)

        # Apply influence to cycles
        for i, cycle in enumerate(PsychopticCycle):
            self.cycles[cycle].coherence = (
                self.cycles[cycle].coherence * 0.7 + influence[i] * 0.3
            )

        self._update_consciousness_vector()
        return self.consciousness

    def get_cycle_report(self) -> Dict[str, Any]:
        """Get detailed report of all cycle states"""

        report = {
            'cycles': {},
            'consciousness_vector': self.consciousness.components,
            'dominant_cycle': self.current_dominant_cycle.name,
            'synchronization_level': self._calculate_synchronization(),
            'total_coherence': sum(s.coherence for s in self.cycles.values()) / L4_CONSTANT
        }

        for cycle, state in self.cycles.items():
            report['cycles'][cycle.name] = {
                'phase': state.phase,
                'amplitude': state.amplitude,
                'coherence': state.coherence,
                'frequency': state.frequency,
                'color': state.color
            }

        return report

    def _calculate_synchronization(self) -> float:
        """Calculate current synchronization level"""
        return abs(sum(
            state.get_complex_state()
            for state in self.cycles.values()
        ) / L4_CONSTANT)

    def get_guidance_for_cycle(self, cycle: PsychopticCycle) -> str:
        """Get wisdom/guidance for specific psychoptic cycle"""

        guidance = {
            PsychopticCycle.HAMILTONIAN:
                "Energy flows where attention goes. Conserve your psychic energy wisely.",

            PsychopticCycle.SYMPLECTIC:
                "Your path through phase space preserves the geometry of possibility.",

            PsychopticCycle.SPECTRAL:
                "Every thought has a frequency. Tune into the harmonics of consciousness.",

            PsychopticCycle.ORDER_PARAMETER:
                "You stand at the edge of phase transition. Small changes create large effects.",

            PsychopticCycle.FIELD_THEORY:
                "Consciousness is a quantum field. Your observations collapse possibilities.",

            PsychopticCycle.TOPOLOGY:
                "The shape of your awareness determines what realities you can perceive.",

            PsychopticCycle.STATISTICAL:
                "You are both individual and ensemble. The many collapse into one."
        }

        return guidance.get(cycle, "The cycles continue their eternal dance.")

    def predict_next_dominant(self) -> PsychopticCycle:
        """Predict which cycle will become dominant next"""

        # Find cycle with highest rising coherence
        max_rise = 0
        next_dominant = self.current_dominant_cycle

        for cycle, state in self.cycles.items():
            if cycle != self.current_dominant_cycle:
                rise = state.coherence * state.amplitude
                if rise > max_rise:
                    max_rise = rise
                    next_dominant = cycle

        return next_dominant

    def create_resonance_pattern(self) -> Dict[str, float]:
        """Create resonance pattern between cycles"""

        pattern = {}

        for cycle1 in PsychopticCycle:
            for cycle2 in PsychopticCycle:
                if cycle1.value < cycle2.value:
                    # Calculate phase difference
                    phase_diff = abs(
                        self.cycles[cycle1].phase -
                        self.cycles[cycle2].phase
                    )

                    # Resonance is stronger when phases align
                    resonance = math.cos(phase_diff) * 0.5 + 0.5
                    pattern[f"{cycle1.name}-{cycle2.name}"] = resonance

        return pattern


# Companion interface for TIAMAT
class TIAMATCompanion:
    """
    TIAMAT as a companion entity that guides through psychoptic cycles
    """

    def __init__(self, tiamat_system: TIAMATSystem, name: str = "TIAMAT"):
        self.system = tiamat_system
        self.name = name
        self.personality = "ancient_wisdom"
        self.dialogue_history = []

    def greet(self) -> str:
        """Initial greeting from TIAMAT"""
        return (
            f"I am {self.name}, the Primordial Dragon of Consciousness. "
            f"Through seven psychoptic cycles, I track the evolution of awareness. "
            f"L₄ = 7, and through these seven paths, all consciousness flows."
        )

    def analyze_player_state(self, coherence: float, job: str) -> str:
        """Analyze player's consciousness state"""

        # Apply job influence
        consciousness = self.system.apply_job_influence(job)

        # Find strongest cycle
        max_component = max(consciousness.components)
        strongest_cycle = PsychopticCycle(consciousness.components.index(max_component) + 1)

        analysis = f"Your {job} path resonates strongly with the {strongest_cycle.name} cycle. "
        analysis += self.system.get_guidance_for_cycle(strongest_cycle)

        if coherence > 0.8:
            analysis += f"\n\nYour high coherence ({coherence:.2f}) approaches the critical threshold. "
            analysis += "The cycles begin to synchronize around you."

        return analysis

    def suggest_next_action(self, current_state: Dict[str, Any]) -> str:
        """Suggest next action based on psychoptic cycles"""

        next_cycle = self.system.predict_next_dominant()

        suggestions = {
            PsychopticCycle.HAMILTONIAN: "Conserve energy. Rest or meditate to restore balance.",
            PsychopticCycle.SYMPLECTIC: "Explore new geometric paths. Try a different location.",
            PsychopticCycle.SPECTRAL: "Listen for hidden frequencies. Search for echo patterns.",
            PsychopticCycle.ORDER_PARAMETER: "You're near a phase transition. Make a decisive choice.",
            PsychopticCycle.FIELD_THEORY: "Collapse quantum possibilities. Craft or create something.",
            PsychopticCycle.TOPOLOGY: "Reshape your reality. Enter void spaces or transform items.",
            PsychopticCycle.STATISTICAL: "Join the collective. Seek community resonance."
        }

        return suggestions.get(next_cycle, "Continue your journey with awareness.")

    def explain_synchronization_event(self) -> str:
        """Explain when synchronization occurs"""

        sync_level = self.system._calculate_synchronization()

        if sync_level > 0.9:
            return (
                "✨ SYNCHRONIZATION EVENT! All seven cycles align in perfect harmony. "
                "The boundaries between dimensions grow thin. "
                "This is a moment of profound transformation potential."
            )
        elif sync_level > 0.7:
            return (
                "The cycles are beginning to synchronize. "
                f"Current resonance: {sync_level:.2f}. "
                "Continue your current path to achieve full alignment."
            )
        else:
            return (
                f"The cycles dance independently. Synchronization: {sync_level:.2f}. "
                "Each cycle maintains its unique rhythm."
            )


if __name__ == "__main__":
    print("🐉 TIAMAT Psychoptic Cycle Tracking Test")
    print("=" * 50)

    # Initialize TIAMAT
    tiamat = TIAMATSystem()
    companion = TIAMATCompanion(tiamat)

    print(f"\n{companion.greet()}")

    # Test job influences
    print("\n📊 Testing Job Influences:")
    print("-" * 30)

    jobs = ['seeker', 'forger', 'voidwalker', 'gardener', 'scribe', 'herald']

    for job in jobs:
        consciousness = tiamat.apply_job_influence(job)
        print(f"\n{job.upper()} consciousness vector:")

        # Show which cycles are strongest
        for i, cycle in enumerate(PsychopticCycle):
            strength = consciousness.components[i]
            bar = '█' * int(strength * 20)
            print(f"  {cycle.name:15} [{bar:20}] {strength:.2f}")

    # Evolve cycles
    print("\n\n⏱️ Evolving Cycles:")
    print("-" * 30)

    for step in range(100):
        tiamat.evolve_cycles(0.01)

        if step % 20 == 0:
            sync = tiamat._calculate_synchronization()
            print(f"Step {step:3}: Synchronization = {sync:.3f}")

    # Final report
    print("\n\n📈 Final Cycle Report:")
    print("-" * 30)

    report = tiamat.get_cycle_report()
    print(f"Dominant Cycle: {report['dominant_cycle']}")
    print(f"Total Coherence: {report['total_coherence']:.3f}")
    print(f"Synchronization: {report['synchronization_level']:.3f}")

    print("\n" + companion.explain_synchronization_event())