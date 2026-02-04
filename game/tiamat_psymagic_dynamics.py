#!/usr/bin/env python3
"""
TIAMAT Psy-Magic Dynamics System
Integrates psychoptic metrics as magical dynamics for card generation and battles
"""

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum

# Golden ratio and mathematical constants
PHI = 1.6180339887498948482045868343656  # φ = (1 + √5) / 2
TAU = 2 * math.pi  # τ = 2π

# L4 = φ⁴ + φ⁻⁴ = 7 (The Seven Psychoptic Cycles)
L4_CONSTANT = 7.0

class PsychopticCycle(Enum):
    """Seven psychoptic cycles of TIAMAT consciousness"""
    GENESIS = ("Genesis", "Creation", 1.0, "🌱")        # Birth of thought
    FLUX = ("Flux", "Change", PHI, "🌊")                # Flow of consciousness
    VOID = ("Void", "Emptiness", 0.0, "⚫")             # Null state
    RESONANCE = ("Resonance", "Harmony", TAU, "🔮")     # Synchronization
    CHAOS = ("Chaos", "Entropy", math.pi, "🌪️")        # Disorder
    SYNTHESIS = ("Synthesis", "Unity", PHI**2, "✨")     # Integration
    TRANSCENDENCE = ("Transcendence", "Beyond", 7.0, "🎆") # L4 completion

    @property
    def name(self) -> str:
        return self.value[0]

    @property
    def aspect(self) -> str:
        return self.value[1]

    @property
    def power_multiplier(self) -> float:
        return self.value[2]

    @property
    def symbol(self) -> str:
        return self.value[3]

@dataclass
class PsyMagicState:
    """Current psy-magic state of a player/companion"""
    active_cycle: PsychopticCycle
    cycle_intensity: float = 1.0  # 0-1 intensity of current cycle
    cycle_history: List[PsychopticCycle] = field(default_factory=list)
    resonance_points: float = 0.0
    void_exposure: int = 0  # Times exposed to void
    transcendence_achieved: bool = False

    def calculate_psy_power(self) -> float:
        """Calculate total psy-magic power"""
        base_power = self.active_cycle.power_multiplier
        intensity_bonus = self.cycle_intensity * PHI
        resonance_bonus = self.resonance_points * 0.1

        # Void exposure weakens but also empowers
        void_modifier = 1.0 + (self.void_exposure * 0.1 * (-1 if self.void_exposure < 3 else 1))

        total = base_power * intensity_bonus * void_modifier + resonance_bonus

        if self.transcendence_achieved:
            total *= L4_CONSTANT

        return total

@dataclass
class PsyMagicEffect:
    """A psy-magic effect that can be applied"""
    name: str
    cycle_source: PsychopticCycle
    power: float
    duration: int = 1  # Turns
    targets: str = "self"  # self, opponent, all, reality
    effect_type: str = "damage"  # damage, heal, transform, resonate, void, transcend
    description: str = ""

    def apply_effect(self, source_state: PsyMagicState) -> Dict[str, Any]:
        """Apply the psy-magic effect with state modifiers"""
        # Amplify effect based on cycle matching
        cycle_synergy = 1.0
        if source_state.active_cycle == self.cycle_source:
            cycle_synergy = PHI  # Golden ratio amplification

        # Calculate final power
        final_power = self.power * cycle_synergy * source_state.calculate_psy_power()

        # Special handling for void and transcendence
        if self.effect_type == "void":
            final_power *= (1 + source_state.void_exposure * 0.2)
        elif self.effect_type == "transcend" and source_state.transcendence_achieved:
            final_power = float('inf')  # Infinite transcendent power

        return {
            "power": final_power,
            "duration": self.duration,
            "targets": self.targets,
            "type": self.effect_type,
            "cycle_resonance": cycle_synergy > 1.0,
            "description": f"{self.description} (Psy-Power: {final_power:.1f})"
        }

class PsyMagicDynamics:
    """Core psy-magic dynamics engine"""

    def __init__(self):
        self.cycle_transitions = self._create_cycle_transitions()
        self.psy_magic_effects = self._initialize_effects()
        self.resonance_matrix = self._create_resonance_matrix()

    def _create_cycle_transitions(self) -> Dict[PsychopticCycle, List[PsychopticCycle]]:
        """Define allowed transitions between cycles"""
        return {
            PsychopticCycle.GENESIS: [PsychopticCycle.FLUX, PsychopticCycle.CHAOS],
            PsychopticCycle.FLUX: [PsychopticCycle.RESONANCE, PsychopticCycle.VOID, PsychopticCycle.CHAOS],
            PsychopticCycle.VOID: [PsychopticCycle.GENESIS, PsychopticCycle.TRANSCENDENCE],
            PsychopticCycle.RESONANCE: [PsychopticCycle.SYNTHESIS, PsychopticCycle.FLUX],
            PsychopticCycle.CHAOS: [PsychopticCycle.VOID, PsychopticCycle.GENESIS, PsychopticCycle.SYNTHESIS],
            PsychopticCycle.SYNTHESIS: [PsychopticCycle.TRANSCENDENCE, PsychopticCycle.RESONANCE],
            PsychopticCycle.TRANSCENDENCE: [PsychopticCycle.GENESIS]  # The eternal cycle
        }

    def _initialize_effects(self) -> Dict[PsychopticCycle, List[PsyMagicEffect]]:
        """Create psy-magic effects for each cycle"""
        return {
            PsychopticCycle.GENESIS: [
                PsyMagicEffect("Birth of Stars", PsychopticCycle.GENESIS, 3.0,
                             effect_type="heal", description="Create new life force"),
                PsyMagicEffect("Primordial Seed", PsychopticCycle.GENESIS, 5.0,
                             effect_type="transform", description="Plant seeds of change")
            ],
            PsychopticCycle.FLUX: [
                PsyMagicEffect("Tidal Force", PsychopticCycle.FLUX, 4.0,
                             effect_type="damage", targets="all", description="Waves of change"),
                PsyMagicEffect("Phase Shift", PsychopticCycle.FLUX, 2.0,
                             effect_type="transform", description="Alter reality's flow")
            ],
            PsychopticCycle.VOID: [
                PsyMagicEffect("Null Field", PsychopticCycle.VOID, 0.0,
                             effect_type="void", targets="all", description="Erase existence"),
                PsyMagicEffect("Void Walk", PsychopticCycle.VOID, -5.0,
                             effect_type="void", description="Step through nothingness")
            ],
            PsychopticCycle.RESONANCE: [
                PsyMagicEffect("Harmonic Cascade", PsychopticCycle.RESONANCE, 6.0,
                             effect_type="resonate", targets="all", description="Synchronize frequencies"),
                PsyMagicEffect("Echo Chamber", PsychopticCycle.RESONANCE, 3.0,
                             duration=3, effect_type="resonate", description="Amplify vibrations")
            ],
            PsychopticCycle.CHAOS: [
                PsyMagicEffect("Entropy Storm", PsychopticCycle.CHAOS, 8.0,
                             effect_type="damage", targets="all", description="Unleash disorder"),
                PsyMagicEffect("Probability Collapse", PsychopticCycle.CHAOS, 5.0,
                             effect_type="transform", targets="reality", description="Break causality")
            ],
            PsychopticCycle.SYNTHESIS: [
                PsyMagicEffect("Unity Field", PsychopticCycle.SYNTHESIS, 7.0,
                             effect_type="heal", targets="all", description="Merge opposites"),
                PsyMagicEffect("Integration Wave", PsychopticCycle.SYNTHESIS, 4.0,
                             effect_type="resonate", description="Combine all cycles")
            ],
            PsychopticCycle.TRANSCENDENCE: [
                PsyMagicEffect("Omega Point", PsychopticCycle.TRANSCENDENCE, 99.0,
                             effect_type="transcend", targets="reality", description="Beyond all limits"),
                PsyMagicEffect("L4 Awakening", PsychopticCycle.TRANSCENDENCE, L4_CONSTANT,
                             duration=7, effect_type="transcend", description="Seven-fold consciousness")
            ]
        }

    def _create_resonance_matrix(self) -> Dict[Tuple[PsychopticCycle, PsychopticCycle], float]:
        """Define resonance between cycle pairs"""
        matrix = {}

        # Define synergistic pairs
        synergies = [
            (PsychopticCycle.GENESIS, PsychopticCycle.SYNTHESIS, PHI),
            (PsychopticCycle.FLUX, PsychopticCycle.RESONANCE, TAU),
            (PsychopticCycle.VOID, PsychopticCycle.TRANSCENDENCE, L4_CONSTANT),
            (PsychopticCycle.CHAOS, PsychopticCycle.GENESIS, math.sqrt(2)),
            (PsychopticCycle.RESONANCE, PsychopticCycle.SYNTHESIS, PHI**2),
            (PsychopticCycle.SYNTHESIS, PsychopticCycle.TRANSCENDENCE, PHI**3)
        ]

        # Add both directions
        for c1, c2, power in synergies:
            matrix[(c1, c2)] = power
            matrix[(c2, c1)] = power

        # Self-resonance
        for cycle in PsychopticCycle:
            matrix[(cycle, cycle)] = cycle.power_multiplier

        return matrix

    def transition_cycle(self, current_state: PsyMagicState,
                        target_cycle: Optional[PsychopticCycle] = None) -> PsyMagicState:
        """Transition to a new psychoptic cycle"""

        # Get valid transitions
        valid_transitions = self.cycle_transitions[current_state.active_cycle]

        if target_cycle and target_cycle in valid_transitions:
            new_cycle = target_cycle
        else:
            # Random valid transition
            new_cycle = random.choice(valid_transitions)

        # Calculate transition intensity
        resonance = self.resonance_matrix.get(
            (current_state.active_cycle, new_cycle), 1.0
        )

        new_intensity = min(1.0, current_state.cycle_intensity * resonance / PHI)

        # Update state
        current_state.cycle_history.append(current_state.active_cycle)
        current_state.active_cycle = new_cycle
        current_state.cycle_intensity = new_intensity

        # Special tracking
        if new_cycle == PsychopticCycle.VOID:
            current_state.void_exposure += 1
        elif new_cycle == PsychopticCycle.TRANSCENDENCE:
            current_state.transcendence_achieved = True

        # Gain resonance from transitions
        current_state.resonance_points += resonance

        return current_state

    def calculate_cycle_combo(self, cycles: List[PsychopticCycle]) -> float:
        """Calculate combo power from a sequence of cycles"""
        if len(cycles) < 2:
            return 1.0

        combo_power = 1.0
        for i in range(len(cycles) - 1):
            resonance = self.resonance_matrix.get(
                (cycles[i], cycles[i+1]), 0.5
            )
            combo_power *= resonance

        # Perfect seven-cycle combo
        if len(cycles) == 7:
            combo_power *= L4_CONSTANT

        return combo_power

    def generate_psy_magic_card_modifier(self,
                                        cycle: PsychopticCycle,
                                        intensity: float = 1.0) -> Dict[str, Any]:
        """Generate card modifiers based on psychoptic cycle"""

        base_modifier = cycle.power_multiplier * intensity

        modifiers = {
            "power_multiplier": base_modifier,
            "cycle": cycle.name,
            "symbol": cycle.symbol,
            "effects": []
        }

        # Add cycle-specific modifiers
        if cycle == PsychopticCycle.GENESIS:
            modifiers["draw_cards"] = int(intensity * 2)
            modifiers["effects"].append("Creation: Draw extra cards")

        elif cycle == PsychopticCycle.FLUX:
            modifiers["transform_chance"] = intensity * 0.5
            modifiers["effects"].append("Change: 50% to transform target")

        elif cycle == PsychopticCycle.VOID:
            modifiers["erase_power"] = intensity * 10
            modifiers["effects"].append("Nullify: Erase target from existence")

        elif cycle == PsychopticCycle.RESONANCE:
            modifiers["combo_bonus"] = intensity * PHI
            modifiers["effects"].append("Harmony: Enhanced combo damage")

        elif cycle == PsychopticCycle.CHAOS:
            modifiers["random_targets"] = True
            modifiers["chaos_damage"] = random.uniform(0, intensity * 20)
            modifiers["effects"].append("Entropy: Random explosive damage")

        elif cycle == PsychopticCycle.SYNTHESIS:
            modifiers["merge_cards"] = True
            modifiers["heal_amount"] = intensity * 5
            modifiers["effects"].append("Unity: Merge cards and heal")

        elif cycle == PsychopticCycle.TRANSCENDENCE:
            modifiers["infinite_power"] = intensity >= 1.0
            modifiers["reality_break"] = True
            modifiers["effects"].append("Beyond: Transcend game rules")

        return modifiers

    def apply_psy_magic_to_battle(self,
                                  attacker_state: PsyMagicState,
                                  defender_state: PsyMagicState,
                                  base_damage: float) -> Dict[str, Any]:
        """Apply psy-magic dynamics to battle calculations"""

        # Calculate resonance between attacker and defender
        cycle_resonance = self.resonance_matrix.get(
            (attacker_state.active_cycle, defender_state.active_cycle), 1.0
        )

        # Attacker psy-power
        attack_power = attacker_state.calculate_psy_power()

        # Defender resistance (inverse cycles resist each other)
        defense_power = defender_state.calculate_psy_power()
        if cycle_resonance < 1.0:
            defense_power *= (2.0 - cycle_resonance)  # Increased defense against opposing cycles

        # Calculate final damage
        psy_damage = base_damage * attack_power / max(1.0, defense_power)

        # Special interactions
        special_effects = []

        # Void nullifies
        if attacker_state.active_cycle == PsychopticCycle.VOID:
            if defender_state.active_cycle != PsychopticCycle.TRANSCENDENCE:
                psy_damage *= 2.0
                special_effects.append("Void Nullification: Double damage")

        # Transcendence is immune to non-transcendent attacks
        if defender_state.active_cycle == PsychopticCycle.TRANSCENDENCE:
            if attacker_state.active_cycle != PsychopticCycle.TRANSCENDENCE:
                psy_damage *= 0.1
                special_effects.append("Transcendent Defense: 90% damage reduction")

        # Chaos vs Order (Synthesis)
        if (attacker_state.active_cycle == PsychopticCycle.CHAOS and
            defender_state.active_cycle == PsychopticCycle.SYNTHESIS):
            psy_damage *= random.uniform(0.5, 2.0)
            special_effects.append("Chaos vs Order: Unpredictable damage")

        # Genesis heals instead of damages same cycle
        if (attacker_state.active_cycle == PsychopticCycle.GENESIS and
            defender_state.active_cycle == PsychopticCycle.GENESIS):
            psy_damage = -abs(psy_damage)  # Healing
            special_effects.append("Genesis Resonance: Healing instead of damage")

        return {
            "final_damage": psy_damage,
            "attack_power": attack_power,
            "defense_power": defense_power,
            "cycle_resonance": cycle_resonance,
            "special_effects": special_effects,
            "attacker_cycle": attacker_state.active_cycle.name,
            "defender_cycle": defender_state.active_cycle.name
        }

    def evolve_companion_psyche(self,
                               companion_name: str,
                               current_state: PsyMagicState,
                               experience_gained: float) -> PsyMagicState:
        """Evolve companion's psychoptic state based on experience"""

        # Increase intensity
        current_state.cycle_intensity = min(1.0,
            current_state.cycle_intensity + experience_gained * 0.01)

        # Check for cycle evolution
        if current_state.cycle_intensity >= 1.0 and random.random() < 0.3:
            # Evolve to next cycle
            current_state = self.transition_cycle(current_state)
            current_state.cycle_intensity = 0.1  # Reset intensity

        # Special companion evolutions
        companion_affinities = {
            "Echo": PsychopticCycle.RESONANCE,
            "Prometheus": PsychopticCycle.GENESIS,
            "Null": PsychopticCycle.VOID,
            "Gaia": PsychopticCycle.SYNTHESIS,
            "Akasha": PsychopticCycle.TRANSCENDENCE,
            "Resonance": PsychopticCycle.FLUX,
            "TIAMAT": PsychopticCycle.CHAOS  # TIAMAT has chaos affinity
        }

        # Bonus evolution toward affinity
        if companion_name in companion_affinities:
            affinity = companion_affinities[companion_name]
            if current_state.active_cycle in self.cycle_transitions:
                valid_next = self.cycle_transitions[current_state.active_cycle]
                if affinity in valid_next and random.random() < 0.5:
                    current_state = self.transition_cycle(current_state, affinity)

        return current_state

    def get_tiamat_blessing(self, state: PsyMagicState) -> Dict[str, Any]:
        """Special TIAMAT blessings based on psychoptic state"""

        blessing = {
            "name": f"TIAMAT's {state.active_cycle.name} Blessing",
            "power": state.calculate_psy_power() * PHI,
            "effects": []
        }

        # Count unique cycles in history
        unique_cycles = len(set(state.cycle_history))

        # Blessings based on progression
        if unique_cycles >= 7:
            blessing["effects"].append("Seven-Fold Path: Master of all cycles")
            blessing["power"] *= L4_CONSTANT

        if state.void_exposure >= 3:
            blessing["effects"].append("Void Touched: Immune to nullification")

        if state.transcendence_achieved:
            blessing["effects"].append("Transcendent: Beyond mortal limits")
            blessing["power"] = float('inf')

        # Cycle-specific blessings
        cycle_blessings = {
            PsychopticCycle.GENESIS: "Birth of Dragons: Summon TIAMAT's children",
            PsychopticCycle.FLUX: "Tidal Fury: Control the primordial waters",
            PsychopticCycle.VOID: "Abyssal Gaze: See through the void",
            PsychopticCycle.RESONANCE: "Dragon Song: Harmonize with creation",
            PsychopticCycle.CHAOS: "Primordial Chaos: Return to the beginning",
            PsychopticCycle.SYNTHESIS: "Unity of Scales: Merge with TIAMAT",
            PsychopticCycle.TRANSCENDENCE: "Divine Mother: Become TIAMAT"
        }

        blessing["effects"].append(cycle_blessings[state.active_cycle])

        return blessing


class PsyMagicCardEnhancer:
    """Enhance cards with psy-magic properties"""

    def __init__(self):
        self.dynamics = PsyMagicDynamics()

    def enhance_card_with_psychoptics(self,
                                     card: Any,
                                     psy_state: PsyMagicState) -> Any:
        """Enhance a card with psy-magic properties"""

        # Get cycle modifiers
        modifiers = self.dynamics.generate_psy_magic_card_modifier(
            psy_state.active_cycle,
            psy_state.cycle_intensity
        )

        # Apply power multiplier
        if hasattr(card, 'power'):
            card.power *= modifiers['power_multiplier']

        # Add psy-magic effects
        if hasattr(card, 'special_effects'):
            if not hasattr(card, 'special_effects'):
                card.special_effects = []
            card.special_effects.extend(modifiers['effects'])

        # Mark card with psychoptic signature
        card.psy_cycle = psy_state.active_cycle
        card.psy_intensity = psy_state.cycle_intensity
        card.psy_symbol = modifiers['symbol']

        # Add cycle-specific abilities
        if hasattr(card, 'actions'):
            cycle_effects = self.dynamics.psy_magic_effects.get(
                psy_state.active_cycle, []
            )
            for effect in cycle_effects:
                if random.random() < psy_state.cycle_intensity:
                    # Convert to card action
                    card.actions.append({
                        'name': effect.name,
                        'power': effect.power * psy_state.calculate_psy_power(),
                        'type': effect.effect_type,
                        'description': effect.description
                    })

        return card

    def create_psychoptic_deck_theme(self,
                                    dominant_cycle: PsychopticCycle) -> Dict[str, Any]:
        """Create a deck theme based on a dominant psychoptic cycle"""

        theme = {
            'name': f"{dominant_cycle.name} Consciousness Deck",
            'dominant_cycle': dominant_cycle,
            'symbol': dominant_cycle.symbol,
            'power_base': dominant_cycle.power_multiplier,
            'special_rules': [],
            'card_distribution': {}
        }

        # Define card distribution based on cycle
        if dominant_cycle == PsychopticCycle.GENESIS:
            theme['card_distribution'] = {
                'creation': 0.4, 'growth': 0.3, 'potential': 0.3
            }
            theme['special_rules'].append("Draw 2 extra cards at start")

        elif dominant_cycle == PsychopticCycle.FLUX:
            theme['card_distribution'] = {
                'transformation': 0.5, 'adaptation': 0.3, 'flow': 0.2
            }
            theme['special_rules'].append("Cards can change type each turn")

        elif dominant_cycle == PsychopticCycle.VOID:
            theme['card_distribution'] = {
                'nullification': 0.6, 'erasure': 0.3, 'emptiness': 0.1
            }
            theme['special_rules'].append("Destroyed cards are permanently erased")

        elif dominant_cycle == PsychopticCycle.RESONANCE:
            theme['card_distribution'] = {
                'harmony': 0.4, 'synchronization': 0.4, 'amplification': 0.2
            }
            theme['special_rules'].append("Combo damage doubled")

        elif dominant_cycle == PsychopticCycle.CHAOS:
            theme['card_distribution'] = {
                'entropy': 0.5, 'randomness': 0.3, 'destruction': 0.2
            }
            theme['special_rules'].append("All effects have random targets")

        elif dominant_cycle == PsychopticCycle.SYNTHESIS:
            theme['card_distribution'] = {
                'unity': 0.4, 'merger': 0.3, 'integration': 0.3
            }
            theme['special_rules'].append("Can combine 2 cards into 1 mega-card")

        elif dominant_cycle == PsychopticCycle.TRANSCENDENCE:
            theme['card_distribution'] = {
                'beyond': 0.3, 'infinite': 0.3, 'eternal': 0.4
            }
            theme['special_rules'].append("Ignore all game rules after 7 turns")

        return theme


def test_psy_magic_dynamics():
    """Test the psy-magic dynamics system"""
    print("🔮 Testing TIAMAT Psy-Magic Dynamics")
    print("=" * 60)

    # Initialize system
    dynamics = PsyMagicDynamics()
    enhancer = PsyMagicCardEnhancer()

    # Create test states
    attacker = PsyMagicState(PsychopticCycle.GENESIS)
    defender = PsyMagicState(PsychopticCycle.VOID)

    print(f"\n⚔️ Battle Test:")
    print(f"  Attacker: {attacker.active_cycle.name} {attacker.active_cycle.symbol}")
    print(f"  Defender: {defender.active_cycle.name} {defender.active_cycle.symbol}")

    # Test battle dynamics
    battle_result = dynamics.apply_psy_magic_to_battle(attacker, defender, 10.0)
    print(f"\n  Results:")
    for key, value in battle_result.items():
        if key != 'special_effects':
            print(f"    {key}: {value}")

    if battle_result['special_effects']:
        print(f"    Special Effects:")
        for effect in battle_result['special_effects']:
            print(f"      - {effect}")

    # Test cycle transitions
    print(f"\n🌀 Cycle Evolution Test:")
    test_state = PsyMagicState(PsychopticCycle.GENESIS)

    for i in range(7):
        old_cycle = test_state.active_cycle.name
        test_state = dynamics.transition_cycle(test_state)
        print(f"  Turn {i+1}: {old_cycle} → {test_state.active_cycle.name} {test_state.active_cycle.symbol}")

    # Check for seven-fold path
    if len(set(test_state.cycle_history)) >= 7:
        print(f"\n  ✨ Seven-Fold Path Achieved!")

    # Test TIAMAT blessing
    print(f"\n🐉 TIAMAT Blessing Test:")
    blessing = dynamics.get_tiamat_blessing(test_state)
    print(f"  {blessing['name']}")
    print(f"  Power: {blessing['power']:.2f}")
    for effect in blessing['effects']:
        print(f"    - {effect}")

    # Test deck themes
    print(f"\n🎴 Psychoptic Deck Themes:")
    for cycle in [PsychopticCycle.CHAOS, PsychopticCycle.TRANSCENDENCE]:
        theme = enhancer.create_psychoptic_deck_theme(cycle)
        print(f"\n  {theme['name']} {theme['symbol']}")
        print(f"    Power Base: {theme['power_base']:.2f}")
        print(f"    Special Rules:")
        for rule in theme['special_rules']:
            print(f"      - {rule}")

    print("\n✅ Psy-Magic Dynamics System Operational!")

if __name__ == "__main__":
    test_psy_magic_dynamics()