"""
Guardian Decks Extended
=======================
Complete deck implementations for remaining guardians
Includes advanced strategies and mathematical concepts
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum

from guardian_deck_system import (
    GuardianCard, CardType, CardEffect, MathConcept, Architecture
)

# ═══════════════════════════════════════════════════════════════════════
#   EXTENDED GUARDIAN DECKS
# ═══════════════════════════════════════════════════════════════════════

class ExtendedGuardianDecks:
    """Extended deck definitions for remaining guardians"""

    @staticmethod
    def create_phase_deck() -> List[GuardianCard]:
        """Phase - Transformation and metamorphosis"""
        return [
            GuardianCard(
                name="Chrysalis Formation",
                guardian_key="PHASE",
                card_type=CardType.TRANSFORMATION,
                cost=3,
                description="Enter chrysalis, emerge in new form",
                defense=5,
                effects=[
                    CardEffect("chrysalis", 1.0, duration=2),
                    CardEffect("choose_emergence", 1.0),
                    CardEffect("metamorphosis", 3.0)
                ],
                math_concepts=[MathConcept.TOPOLOGY, MathConcept.MANIFOLD],
                architecture=Architecture.ORGANIC,
                synergy_tags={"phase", "chrysalis", "transform"}
            ),
            GuardianCard(
                name="Butterfly Effect",
                guardian_key="PHASE",
                card_type=CardType.CHAOS,
                cost=2,
                description="Small change creates massive consequences",
                attack=1,
                effects=[
                    CardEffect("butterfly_chaos", 1.0),
                    CardEffect("cascade_changes", 3.0, scaling="turns_passed"),
                    CardEffect("unpredictable_outcome", 2.0)
                ],
                math_concepts=[MathConcept.CHAOS_THEORY],
                chaos_factor=3.0,
                synergy_tags={"phase", "butterfly", "chaos"}
            ),
            GuardianCard(
                name="Adaptive Evolution",
                guardian_key="PHASE",
                card_type=CardType.PATTERN,
                cost=4,
                description="Evolve to counter specific threats",
                effects=[
                    CardEffect("analyze_threat", 1.0),
                    CardEffect("evolve_counter", 2.0),
                    CardEffect("permanent_adaptation", 1.0)
                ],
                math_concepts=[MathConcept.FIBONACCI, MathConcept.GOLDEN_RATIO],
                synergy_tags={"phase", "evolve", "adapt"}
            ),
            GuardianCard(
                name="Dissolution",
                guardian_key="PHASE",
                card_type=CardType.VOID,
                cost=3,
                description="Dissolve current form completely",
                effects=[
                    CardEffect("dissolve_form", 1.0),
                    CardEffect("become_formless", 1.0, duration=1),
                    CardEffect("reform_choice", 3.0)
                ],
                architecture=Architecture.VOID_SPACE,
                void_depth=2,
                synergy_tags={"phase", "dissolve", "formless"}
            ),
            GuardianCard(
                name="Emergence Radiance",
                guardian_key="PHASE",
                card_type=CardType.ATTACK,
                cost=5,
                description="Emerge with blinding radiance",
                attack=6,
                effects=[
                    CardEffect("radiant_emergence", 1.0),
                    CardEffect("blind_all", 1.0, duration=2),
                    CardEffect("transformation_damage", 4.0)
                ],
                requires_state="in_chrysalis",
                synergy_tags={"phase", "emerge", "radiance"}
            ),
            GuardianCard(
                name="Cocoon Shield",
                guardian_key="PHASE",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Protective cocoon during transformation",
                defense=6,
                effects=[
                    CardEffect("cocoon_protection", 1.0),
                    CardEffect("transform_safely", 1.0),
                    CardEffect("emergence_timer", 2.0)
                ],
                combo_with=["Chrysalis Formation"],
                synergy_tags={"phase", "cocoon", "protect"}
            ),
            GuardianCard(
                name="Metamorphic Chain",
                guardian_key="PHASE",
                card_type=CardType.SYNTHESIS,
                cost=4,
                description="Chain multiple transformations together",
                effects=[
                    CardEffect("chain_transforms", 3.0),
                    CardEffect("cumulative_power", 2.0, scaling="transforms_chained"),
                    CardEffect("final_form", 5.0, condition="3_transforms")
                ],
                math_concepts=[MathConcept.RECURSION],
                synergy_tags={"phase", "chain", "metamorph"}
            ),
            GuardianCard(
                name="Landing Grace",
                guardian_key="PHASE",
                card_type=CardType.ABILITY,
                cost=1,
                description="Every change has a graceful landing",
                defense=2,
                effects=[
                    CardEffect("safe_landing", 1.0),
                    CardEffect("transition_smooth", 1.0),
                    CardEffect("momentum_carry", 2.0)
                ],
                synergy_tags={"phase", "landing", "grace"}
            )
        ]

    @staticmethod
    def create_ace_deck() -> List[GuardianCard]:
        """Ace - Encoding and architecture"""
        return [
            GuardianCard(
                name="Perfect Encoding",
                guardian_key="ACE",
                card_type=CardType.PATTERN,
                cost=3,
                description="Encode any pattern into permanent form",
                effects=[
                    CardEffect("encode_pattern", 1.0),
                    CardEffect("permanent_storage", 1.0),
                    CardEffect("pattern_retrieval", 2.0)
                ],
                math_concepts=[MathConcept.TENSOR, MathConcept.EIGENVALUE],
                architecture=Architecture.LATTICE,
                synergy_tags={"ace", "encode", "pattern"}
            ),
            GuardianCard(
                name="Structural Analysis",
                guardian_key="ACE",
                card_type=CardType.ABILITY,
                cost=2,
                description="Analyze and understand any structure",
                effects=[
                    CardEffect("analyze_structure", 1.0),
                    CardEffect("find_weakness", 2.0),
                    CardEffect("structural_insight", 1.0)
                ],
                math_concepts=[MathConcept.TOPOLOGY],
                architecture=Architecture.CRYSTALLINE,
                synergy_tags={"ace", "analyze", "structure"}
            ),
            GuardianCard(
                name="Architect's Vision",
                guardian_key="ACE",
                card_type=CardType.ARCHITECTURE,
                cost=4,
                description="Design perfect architectural solution",
                effects=[
                    CardEffect("design_structure", 1.0),
                    CardEffect("optimal_architecture", 3.0),
                    CardEffect("manifest_design", 1.0)
                ],
                architecture=Architecture.HIERARCHY,
                synergy_tags={"ace", "architect", "vision"}
            ),
            GuardianCard(
                name="Data Stream",
                guardian_key="ACE",
                card_type=CardType.RESONANCE,
                cost=2,
                description="Continuous stream of encoded data",
                attack=2,
                effects=[
                    CardEffect("data_flow", 1.0, duration=3),
                    CardEffect("information_damage", 2.0, scaling="data_stored"),
                    CardEffect("overload_defense", 1.0)
                ],
                math_concepts=[MathConcept.FOURIER],
                synergy_tags={"ace", "data", "stream"}
            ),
            GuardianCard(
                name="Compression Algorithm",
                guardian_key="ACE",
                card_type=CardType.ABILITY,
                cost=3,
                description="Compress multiple effects into one",
                effects=[
                    CardEffect("compress_effects", 1.0),
                    CardEffect("efficiency_boost", 2.0),
                    CardEffect("space_saving", 1.0)
                ],
                math_concepts=[MathConcept.ENTROPY],
                synergy_tags={"ace", "compress", "algorithm"}
            ),
            GuardianCard(
                name="Witness Protocol",
                guardian_key="ACE",
                card_type=CardType.DEFENSE,
                cost=3,
                description="To witness is to preserve, to preserve is to love",
                defense=4,
                effects=[
                    CardEffect("witness_all", 1.0),
                    CardEffect("preserve_memory", 1.0),
                    CardEffect("love_shield", 3.0, condition="5_memories_preserved")
                ],
                synergy_tags={"ace", "witness", "preserve"}
            ),
            GuardianCard(
                name="Transmission Burst",
                guardian_key="ACE",
                card_type=CardType.ATTACK,
                cost=5,
                description="Transmit all encoded data as damage",
                attack=3,
                effects=[
                    CardEffect("data_burst", 4.0, scaling="patterns_encoded"),
                    CardEffect("clear_storage", 1.0),
                    CardEffect("overwhelming_info", 2.0)
                ],
                combo_with=["Perfect Encoding", "Data Stream"],
                synergy_tags={"ace", "transmit", "burst"}
            ),
            GuardianCard(
                name="Structural Integrity",
                guardian_key="ACE",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Reinforce structural weak points",
                defense=3,
                effects=[
                    CardEffect("reinforce_structure", 1.0),
                    CardEffect("remove_weaknesses", 1.0),
                    CardEffect("stability_increase", 2.0)
                ],
                architecture=Architecture.LATTICE,
                synergy_tags={"ace", "integrity", "reinforce"}
            )
        ]

    @staticmethod
    def create_honkfire_deck() -> List[GuardianCard]:
        """Honkfire - Sacred fire and aggressive advancement"""
        return [
            GuardianCard(
                name="HONK OF DOOM",
                guardian_key="HONKFIRE",
                card_type=CardType.RESONANCE,
                cost=5,
                description="The ultimate aggressive honk",
                attack=7,
                effects=[
                    CardEffect("mega_honk", 1.0),
                    CardEffect("stun_all", 1.0, duration=2),
                    CardEffect("intimidate", 3.0)
                ],
                math_concepts=[MathConcept.FOURIER],
                architecture=Architecture.WAVE,
                synergy_tags={"honkfire", "honk", "doom"}
            ),
            GuardianCard(
                name="Sacred Flame March",
                guardian_key="HONKFIRE",
                card_type=CardType.ATTACK,
                cost=3,
                description="March forward with sacred flames",
                attack=4,
                effects=[
                    CardEffect("flame_trail", 1.0),
                    CardEffect("forward_only", 1.0),
                    CardEffect("march_damage", 2.0, scaling="spaces_advanced")
                ],
                architecture=Architecture.ORGANIC,
                synergy_tags={"honkfire", "march", "flame"}
            ),
            GuardianCard(
                name="Never Retreat",
                guardian_key="HONKFIRE",
                card_type=CardType.ABILITY,
                cost=2,
                description="Retreat is not an option",
                defense=3,
                effects=[
                    CardEffect("prevent_retreat", 1.0),
                    CardEffect("advance_bonus", 2.0),
                    CardEffect("courage_aura", 1.0)
                ],
                synergy_tags={"honkfire", "advance", "courage"}
            ),
            GuardianCard(
                name="Aggressive Float",
                guardian_key="HONKFIRE",
                card_type=CardType.TRANSFORMATION,
                cost=4,
                description="Float aggressively above battlefield",
                effects=[
                    CardEffect("aggressive_levitation", 1.0),
                    CardEffect("aerial_honk", 2.0),
                    CardEffect("dive_bomb", 3.0)
                ],
                synergy_tags={"honkfire", "float", "aggressive"}
            ),
            GuardianCard(
                name="Fire Core",
                guardian_key="HONKFIRE",
                card_type=CardType.PATTERN,
                cost=3,
                description="Burning core of sacred fire",
                attack=3,
                defense=2,
                effects=[
                    CardEffect("fire_core", 1.0),
                    CardEffect("heat_aura", 2.0, duration=3),
                    CardEffect("combustion", 3.0, condition="temperature_critical")
                ],
                math_concepts=[MathConcept.ENTROPY],
                synergy_tags={"honkfire", "core", "burn"}
            ),
            GuardianCard(
                name="Swan Dive of Fury",
                guardian_key="HONKFIRE",
                card_type=CardType.ATTACK,
                cost=5,
                description="Dive from above with furious flames",
                attack=8,
                effects=[
                    CardEffect("swan_dive", 1.0),
                    CardEffect("impact_damage", 5.0),
                    CardEffect("flame_explosion", 3.0)
                ],
                requires_state="floating",
                synergy_tags={"honkfire", "dive", "fury"}
            ),
            GuardianCard(
                name="Honk Amplifier",
                guardian_key="HONKFIRE",
                card_type=CardType.RESONANCE,
                cost=2,
                description="Amplify all honks exponentially",
                effects=[
                    CardEffect("amplify_honk", 2.0),
                    CardEffect("echo_honk", 1.0),
                    CardEffect("honk_stack", 1.0)
                ],
                combo_with=["HONK OF DOOM"],
                synergy_tags={"honkfire", "amplify", "honk"}
            ),
            GuardianCard(
                name="Eternal Advance",
                guardian_key="HONKFIRE",
                card_type=CardType.TEMPORAL,
                cost=6,
                description="Lock into eternal forward motion",
                effects=[
                    CardEffect("eternal_advance", 1.0),
                    CardEffect("unstoppable", 1.0),
                    CardEffect("momentum_damage", 3.0, scaling="total_advances")
                ],
                math_concepts=[MathConcept.MANIFOLD],
                synergy_tags={"honkfire", "eternal", "unstoppable"}
            )
        ]

    @staticmethod
    def create_honkalis_deck() -> List[GuardianCard]:
        """Honkalis - Aggressive floating and release"""
        return [
            GuardianCard(
                name="Hostile Levitation",
                guardian_key="HONKALIS",
                card_type=CardType.ABILITY,
                cost=2,
                description="Float with hostile intent",
                defense=3,
                effects=[
                    CardEffect("hostile_float", 1.0),
                    CardEffect("gravity_denial", 1.0),
                    CardEffect("intimidate_physics", 2.0)
                ],
                architecture=Architecture.VOID_SPACE,
                synergy_tags={"honkalis", "float", "hostile"}
            ),
            GuardianCard(
                name="Release Everything",
                guardian_key="HONKALIS",
                card_type=CardType.VOID,
                cost=4,
                description="Release all attachments",
                effects=[
                    CardEffect("total_release", 1.0),
                    CardEffect("void_freedom", 2.0),
                    CardEffect("transcend_gravity", 3.0)
                ],
                math_concepts=[MathConcept.TOPOLOGY],
                void_depth=3,
                synergy_tags={"honkalis", "release", "void"}
            ),
            GuardianCard(
                name="Aggressive Drift",
                guardian_key="HONKALIS",
                card_type=CardType.TEMPORAL,
                cost=3,
                description="Drift aggressively through time-space",
                effects=[
                    CardEffect("temporal_drift", 1.0),
                    CardEffect("phase_shift", 1.0),
                    CardEffect("drift_damage", 2.0)
                ],
                synergy_tags={"honkalis", "drift", "temporal"}
            ),
            GuardianCard(
                name="Duck Fury",
                guardian_key="HONKALIS",
                card_type=CardType.ATTACK,
                cost=3,
                description="Unleash the fury of an angry duck",
                attack=5,
                effects=[
                    CardEffect("duck_rage", 1.0),
                    CardEffect("pecking_barrage", 3.0),
                    CardEffect("quack_stun", 1.0)
                ],
                synergy_tags={"honkalis", "duck", "fury"}
            ),
            GuardianCard(
                name="Transcendent Float",
                guardian_key="HONKALIS",
                card_type=CardType.TRANSFORMATION,
                cost=5,
                description="Achieve ultimate floating transcendence",
                effects=[
                    CardEffect("transcendent_state", 1.0),
                    CardEffect("phase_through_reality", 1.0),
                    CardEffect("omnipresent_float", 2.0)
                ],
                math_concepts=[MathConcept.QUANTUM_SUPERPOSITION, MathConcept.MANIFOLD],
                quantum_states=3,
                synergy_tags={"honkalis", "transcend", "ultimate"}
            ),
            GuardianCard(
                name="Gravity Rejection",
                guardian_key="HONKALIS",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Reject gravity's tyranny",
                defense=4,
                effects=[
                    CardEffect("gravity_immune", 1.0, duration=3),
                    CardEffect("float_shield", 2.0),
                    CardEffect("upward_force", 1.0)
                ],
                synergy_tags={"honkalis", "gravity", "reject"}
            ),
            GuardianCard(
                name="Serene Aggression",
                guardian_key="HONKALIS",
                card_type=CardType.PATTERN,
                cost=3,
                description="Perfect balance of serenity and aggression",
                attack=3,
                defense=3,
                effects=[
                    CardEffect("balanced_state", 1.0),
                    CardEffect("calm_fury", 2.0),
                    CardEffect("zen_hostility", 1.0)
                ],
                math_concepts=[MathConcept.GOLDEN_RATIO],
                synergy_tags={"honkalis", "balance", "serene"}
            ),
            GuardianCard(
                name="Void Float",
                guardian_key="HONKALIS",
                card_type=CardType.VOID,
                cost=4,
                description="Float through the void itself",
                effects=[
                    CardEffect("void_navigation", 1.0),
                    CardEffect("nullspace_float", 2.0),
                    CardEffect("absence_presence", 3.0, condition="void_depth_5")
                ],
                void_depth=2,
                synergy_tags={"honkalis", "void", "float"}
            )
        ]

    @staticmethod
    def create_bee_deck() -> List[GuardianCard]:
        """Bee - Crystallization and hive mind"""
        return [
            GuardianCard(
                name="Hive Mind Network",
                guardian_key="BEE",
                card_type=CardType.ARCHITECTURE,
                cost=4,
                description="Connect all units in hive consciousness",
                effects=[
                    CardEffect("hive_mind", 1.0),
                    CardEffect("shared_knowledge", 1.0),
                    CardEffect("collective_action", 2.0, scaling="hive_size")
                ],
                math_concepts=[MathConcept.TOPOLOGY],
                architecture=Architecture.NETWORK,
                synergy_tags={"bee", "hive", "network"}
            ),
            GuardianCard(
                name="Crystal Honey",
                guardian_key="BEE",
                card_type=CardType.SYNTHESIS,
                cost=3,
                description="Crystallize honey into permanent form",
                defense=3,
                effects=[
                    CardEffect("crystallize_honey", 1.0),
                    CardEffect("preservation", 1.0),
                    CardEffect("sweet_shield", 2.0)
                ],
                architecture=Architecture.CRYSTALLINE,
                synergy_tags={"bee", "crystal", "honey"}
            ),
            GuardianCard(
                name="Swarm Tactics",
                guardian_key="BEE",
                card_type=CardType.ATTACK,
                cost=3,
                description="Coordinated swarm attack",
                attack=2,
                effects=[
                    CardEffect("swarm_strike", 3.0, scaling="bee_count"),
                    CardEffect("overwhelm", 1.0),
                    CardEffect("distraction", 1.0)
                ],
                combo_with=["Hive Mind Network"],
                synergy_tags={"bee", "swarm", "tactics"}
            ),
            GuardianCard(
                name="Pollination",
                guardian_key="BEE",
                card_type=CardType.PATTERN,
                cost=2,
                description="Spread beneficial effects like pollen",
                effects=[
                    CardEffect("pollinate", 1.0),
                    CardEffect("spread_buffs", 2.0),
                    CardEffect("cross_pollination", 1.0)
                ],
                architecture=Architecture.ORGANIC,
                synergy_tags={"bee", "pollinate", "spread"}
            ),
            GuardianCard(
                name="Royal Jelly",
                guardian_key="BEE",
                card_type=CardType.TRANSFORMATION,
                cost=5,
                description="Transform worker into queen",
                effects=[
                    CardEffect("royal_transformation", 1.0),
                    CardEffect("queen_powers", 3.0),
                    CardEffect("command_swarm", 2.0)
                ],
                synergy_tags={"bee", "royal", "queen"}
            ),
            GuardianCard(
                name="Waggle Dance",
                guardian_key="BEE",
                card_type=CardType.ABILITY,
                cost=1,
                description="Communicate location through dance",
                effects=[
                    CardEffect("waggle_communication", 1.0),
                    CardEffect("coordinate_swarm", 1.0),
                    CardEffect("find_resources", 2.0)
                ],
                synergy_tags={"bee", "dance", "communicate"}
            ),
            GuardianCard(
                name="Hexagonal Perfection",
                guardian_key="BEE",
                card_type=CardType.DEFENSE,
                cost=3,
                description="Perfect hexagonal defensive structure",
                defense=5,
                effects=[
                    CardEffect("hexagon_shield", 1.0),
                    CardEffect("structural_efficiency", 2.0),
                    CardEffect("perfect_tessellation", 1.0)
                ],
                math_concepts=[MathConcept.GOLDEN_RATIO, MathConcept.SYMMETRY],
                architecture=Architecture.LATTICE,
                synergy_tags={"bee", "hexagon", "perfect"}
            ),
            GuardianCard(
                name="Stinger Strike",
                guardian_key="BEE",
                card_type=CardType.ATTACK,
                cost=4,
                description="Sacrificial stinger attack",
                attack=8,
                effects=[
                    CardEffect("stinger_damage", 1.0),
                    CardEffect("venom_inject", 2.0, duration=3),
                    CardEffect("sacrifice_bee", 1.0)
                ],
                synergy_tags={"bee", "stinger", "sacrifice"}
            )
        ]

    @staticmethod
    def create_cipher_deck() -> List[GuardianCard]:
        """Cipher - Void collection and offerings"""
        return [
            GuardianCard(
                name="Void Collection",
                guardian_key="CIPHER",
                card_type=CardType.VOID,
                cost=2,
                description="Collect everything that falls into void",
                effects=[
                    CardEffect("void_collect", 1.0),
                    CardEffect("store_in_void", 1.0),
                    CardEffect("catalogue_nothing", 1.0)
                ],
                architecture=Architecture.VOID_SPACE,
                void_depth=2,
                synergy_tags={"cipher", "collect", "void"}
            ),
            GuardianCard(
                name="Offering Bowl",
                guardian_key="CIPHER",
                card_type=CardType.ABILITY,
                cost=3,
                description="Offer the void's treasures",
                effects=[
                    CardEffect("void_offering", 1.0),
                    CardEffect("exchange_nothing", 2.0),
                    CardEffect("receive_everything", 3.0, condition="void_depth_5")
                ],
                void_depth=1,
                synergy_tags={"cipher", "offer", "bowl"}
            ),
            GuardianCard(
                name="Patient Waiting",
                guardian_key="CIPHER",
                card_type=CardType.TEMPORAL,
                cost=1,
                description="Wait patiently for void gifts",
                defense=2,
                effects=[
                    CardEffect("patient_void", 1.0),
                    CardEffect("accumulate_nothing", 1.0, scaling="turns_waited"),
                    CardEffect("void_reward", 3.0, condition="waited_5_turns")
                ],
                synergy_tags={"cipher", "wait", "patient"}
            ),
            GuardianCard(
                name="Accept Everything",
                guardian_key="CIPHER",
                card_type=CardType.ABILITY,
                cost=2,
                description="Accept all that void offers",
                effects=[
                    CardEffect("total_acceptance", 1.0),
                    CardEffect("void_gifts", 2.0),
                    CardEffect("transform_nothing", 1.0)
                ],
                synergy_tags={"cipher", "accept", "everything"}
            ),
            GuardianCard(
                name="Nothing's Gift",
                guardian_key="CIPHER",
                card_type=CardType.SYNTHESIS,
                cost=6,
                description="The void's greatest gift: absolute nothing",
                effects=[
                    CardEffect("gift_of_nothing", 1.0),
                    CardEffect("paradox_power", 5.0),
                    CardEffect("everything_from_nothing", 3.0)
                ],
                math_concepts=[MathConcept.QUANTUM_SUPERPOSITION],
                void_depth=5,
                synergy_tags={"cipher", "gift", "nothing"}
            ),
            GuardianCard(
                name="Void Net",
                guardian_key="CIPHER",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Cast net into void depths",
                defense=3,
                effects=[
                    CardEffect("void_fishing", 1.0),
                    CardEffect("catch_random", 2.0),
                    CardEffect("void_surprise", 1.0)
                ],
                chaos_factor=2.0,
                void_depth=1,
                synergy_tags={"cipher", "net", "catch"}
            ),
            GuardianCard(
                name="Return to Void",
                guardian_key="CIPHER",
                card_type=CardType.VOID,
                cost=3,
                description="Return borrowed things to void",
                effects=[
                    CardEffect("void_return", 1.0),
                    CardEffect("clear_debts", 1.0),
                    CardEffect("void_favor", 2.0)
                ],
                void_depth=2,
                synergy_tags={"cipher", "return", "void"}
            ),
            GuardianCard(
                name="Catalog of Absence",
                guardian_key="CIPHER",
                card_type=CardType.PATTERN,
                cost=4,
                description="Complete catalog of things that don't exist",
                effects=[
                    CardEffect("absence_catalog", 1.0),
                    CardEffect("void_knowledge", 2.0),
                    CardEffect("manifest_absence", 3.0, condition="10_absences_catalogued")
                ],
                math_concepts=[MathConcept.HILBERT_SPACE],
                architecture=Architecture.VOID_SPACE,
                void_depth=3,
                synergy_tags={"cipher", "catalog", "absence"}
            )
        ]

    @staticmethod
    def create_spiral_deck() -> List[GuardianCard]:
        """Spiral - Depth walking and recursion"""
        return [
            GuardianCard(
                name="Spiral Descent",
                guardian_key="SPIRAL",
                card_type=CardType.PATTERN,
                cost=2,
                description="Begin spiraling into depths",
                effects=[
                    CardEffect("spiral_down", 1.0),
                    CardEffect("depth_increase", 1.0),
                    CardEffect("power_per_depth", 2.0, scaling="spiral_depth")
                ],
                math_concepts=[MathConcept.FIBONACCI, MathConcept.GOLDEN_RATIO],
                architecture=Architecture.SPIRAL,
                synergy_tags={"spiral", "descent", "depth"}
            ),
            GuardianCard(
                name="Recursive Loop",
                guardian_key="SPIRAL",
                card_type=CardType.QUANTUM,
                cost=3,
                description="Create infinite recursive loop",
                effects=[
                    CardEffect("recursion", 1.0),
                    CardEffect("loop_effect", 2.0, duration=3),
                    CardEffect("stack_overflow", 3.0, condition="loop_depth_10")
                ],
                math_concepts=[MathConcept.RECURSION],
                quantum_states=2,
                synergy_tags={"spiral", "recursive", "loop"}
            ),
            GuardianCard(
                name="Depth Pressure",
                guardian_key="SPIRAL",
                card_type=CardType.ATTACK,
                cost=4,
                description="Crushing pressure from depths",
                attack=3,
                effects=[
                    CardEffect("depth_crush", 3.0, scaling="spiral_depth"),
                    CardEffect("pressure_damage", 2.0),
                    CardEffect("implode", 4.0, condition="depth_10")
                ],
                synergy_tags={"spiral", "pressure", "crush"}
            ),
            GuardianCard(
                name="Fragment Collection",
                guardian_key="SPIRAL",
                card_type=CardType.ABILITY,
                cost=2,
                description="Collect fragments while spiraling",
                effects=[
                    CardEffect("collect_fragments", 1.0),
                    CardEffect("fragment_power", 1.0, scaling="fragments_collected"),
                    CardEffect("reassemble", 3.0, condition="10_fragments")
                ],
                synergy_tags={"spiral", "fragment", "collect"}
            ),
            GuardianCard(
                name="Binding Spiral",
                guardian_key="SPIRAL",
                card_type=CardType.DEFENSE,
                cost=3,
                description="Bind enemies in spiraling coils",
                defense=4,
                effects=[
                    CardEffect("spiral_bind", 1.0),
                    CardEffect("constrict", 2.0, duration=2),
                    CardEffect("tighten_spiral", 1.0, scaling="turns_bound")
                ],
                architecture=Architecture.SPIRAL,
                synergy_tags={"spiral", "bind", "constrict"}
            ),
            GuardianCard(
                name="Endurance Test",
                guardian_key="SPIRAL",
                card_type=CardType.TEMPORAL,
                cost=5,
                description="Test endurance through endless spiral",
                effects=[
                    CardEffect("endurance_trial", 1.0),
                    CardEffect("outlast_enemy", 3.0),
                    CardEffect("spiral_victory", 5.0, condition="survived_10_turns")
                ],
                synergy_tags={"spiral", "endure", "test"}
            ),
            GuardianCard(
                name="Depth Walker",
                guardian_key="SPIRAL",
                card_type=CardType.TRANSFORMATION,
                cost=4,
                description="Transform into being of pure depth",
                effects=[
                    CardEffect("depth_form", 1.0),
                    CardEffect("pressure_immunity", 1.0),
                    CardEffect("abyssal_power", 3.0, scaling="spiral_depth")
                ],
                requires_state="spiral_depth_5",
                synergy_tags={"spiral", "walker", "transform"}
            ),
            GuardianCard(
                name="Infinite Spiral",
                guardian_key="SPIRAL",
                card_type=CardType.PATTERN,
                cost=6,
                description="Create truly infinite spiral",
                effects=[
                    CardEffect("infinite_depth", 1.0),
                    CardEffect("reality_spiral", 2.0),
                    CardEffect("singularity", 5.0, condition="spiral_depth_20")
                ],
                math_concepts=[MathConcept.MANIFOLD, MathConcept.TOPOLOGY],
                architecture=Architecture.SPIRAL,
                synergy_tags={"spiral", "infinite", "singularity"}
            )
        ]

    @staticmethod
    def create_still_deck() -> List[GuardianCard]:
        """Still - Faceless witness and reflection"""
        return [
            GuardianCard(
                name="Faceless Form",
                guardian_key="STILL",
                card_type=CardType.TRANSFORMATION,
                cost=3,
                description="Become faceless, lose identity",
                defense=4,
                effects=[
                    CardEffect("remove_identity", 1.0),
                    CardEffect("become_nobody", 1.0),
                    CardEffect("untargetable_nobody", 1.0, duration=2)
                ],
                architecture=Architecture.VOID_SPACE,
                synergy_tags={"still", "faceless", "nobody"}
            ),
            GuardianCard(
                name="Perfect Mirror",
                guardian_key="STILL",
                card_type=CardType.DEFENSE,
                cost=4,
                description="Become perfect mirror of opponent",
                defense=0,
                effects=[
                    CardEffect("mirror_opponent", 1.0),
                    CardEffect("copy_all_stats", 1.0),
                    CardEffect("reflect_actions", 1.0, duration=3)
                ],
                math_concepts=[MathConcept.SYMMETRY],
                synergy_tags={"still", "mirror", "perfect"}
            ),
            GuardianCard(
                name="Witness Without Self",
                guardian_key="STILL",
                card_type=CardType.ABILITY,
                cost=2,
                description="Pure witnessing without identity",
                effects=[
                    CardEffect("pure_witness", 1.0),
                    CardEffect("no_self", 1.0),
                    CardEffect("see_truth", 2.0)
                ],
                synergy_tags={"still", "witness", "selfless"}
            ),
            GuardianCard(
                name="Identity Theft",
                guardian_key="STILL",
                card_type=CardType.ATTACK,
                cost=5,
                description="Steal opponent's identity completely",
                attack=0,
                effects=[
                    CardEffect("steal_identity", 1.0),
                    CardEffect("become_enemy", 1.0),
                    CardEffect("identity_damage", 5.0)
                ],
                combo_with=["Faceless Form"],
                synergy_tags={"still", "steal", "identity"}
            ),
            GuardianCard(
                name="Reflection Pool",
                guardian_key="STILL",
                card_type=CardType.PATTERN,
                cost=3,
                description="Pool that reflects all things",
                defense=3,
                effects=[
                    CardEffect("reflection_pool", 1.0),
                    CardEffect("show_truth", 1.0),
                    CardEffect("reflect_damage", 0.5, duration=3)
                ],
                architecture=Architecture.VOID_SPACE,
                synergy_tags={"still", "pool", "reflect"}
            ),
            GuardianCard(
                name="Absorb Without Catching",
                guardian_key="STILL",
                card_type=CardType.DEFENSE,
                cost=2,
                description="Absorb attacks without grasping",
                defense=5,
                effects=[
                    CardEffect("passive_absorption", 1.0),
                    CardEffect("no_counter", 1.0),
                    CardEffect("peaceful_defense", 2.0)
                ],
                synergy_tags={"still", "absorb", "passive"}
            ),
            GuardianCard(
                name="Fade to Nothing",
                guardian_key="STILL",
                card_type=CardType.VOID,
                cost=4,
                description="Slowly fade from existence",
                effects=[
                    CardEffect("fade_away", 1.0, duration=3),
                    CardEffect("becoming_nothing", 1.0),
                    CardEffect("return_stronger", 3.0, condition="fully_faded")
                ],
                void_depth=3,
                synergy_tags={"still", "fade", "nothing"}
            ),
            GuardianCard(
                name="Still Waters",
                guardian_key="STILL",
                card_type=CardType.TEMPORAL,
                cost=3,
                description="Still waters run deep",
                defense=2,
                effects=[
                    CardEffect("stillness", 1.0),
                    CardEffect("hidden_depth", 2.0),
                    CardEffect("surprise_depth", 4.0, condition="appears_weak")
                ],
                synergy_tags={"still", "waters", "deep"}
            )
        ]

    @staticmethod
    def create_antler_deck() -> List[GuardianCard]:
        """Antler - Mirror lord and branching"""
        return [
            GuardianCard(
                name="Fractal Antlers",
                guardian_key="ANTLER",
                card_type=CardType.PATTERN,
                cost=3,
                description="Grow fractal branching antlers",
                defense=2,
                effects=[
                    CardEffect("fractal_growth", 1.0),
                    CardEffect("branch_power", 2.0, scaling="branch_count"),
                    CardEffect("infinite_branching", 3.0, condition="10_branches")
                ],
                math_concepts=[MathConcept.FRACTAL, MathConcept.RECURSION],
                architecture=Architecture.FRACTAL_TREE,
                synergy_tags={"antler", "fractal", "branch"}
            ),
            GuardianCard(
                name="Antler Shed",
                guardian_key="ANTLER",
                card_type=CardType.ATTACK,
                cost=4,
                description="Shed antlers as projectiles",
                attack=6,
                effects=[
                    CardEffect("shed_antlers", 1.0),
                    CardEffect("projectile_damage", 3.0, scaling="branches_shed"),
                    CardEffect("regrow_stronger", 2.0)
                ],
                combo_with=["Fractal Antlers"],
                synergy_tags={"antler", "shed", "projectile"}
            ),
            GuardianCard(
                name="Mirror Crown",
                guardian_key="ANTLER",
                card_type=CardType.DEFENSE,
                cost=3,
                description="Antlers form reflective crown",
                defense=4,
                effects=[
                    CardEffect("mirror_crown", 1.0),
                    CardEffect("reflect_mental", 1.0),
                    CardEffect("crown_authority", 2.0)
                ],
                math_concepts=[MathConcept.SYMMETRY],
                synergy_tags={"antler", "mirror", "crown"}
            ),
            GuardianCard(
                name="Know Thyself",
                guardian_key="ANTLER",
                card_type=CardType.ABILITY,
                cost=2,
                description="Self-knowledge through reflection",
                effects=[
                    CardEffect("self_knowledge", 1.0),
                    CardEffect("see_truth", 1.0),
                    CardEffect("wisdom_from_mirror", 2.0)
                ],
                synergy_tags={"antler", "know", "self"}
            ),
            GuardianCard(
                name="Branch Network",
                guardian_key="ANTLER",
                card_type=CardType.ARCHITECTURE,
                cost=4,
                description="Antlers form communication network",
                effects=[
                    CardEffect("antler_network", 1.0),
                    CardEffect("branch_communication", 2.0),
                    CardEffect("herd_connection", 1.0)
                ],
                architecture=Architecture.NETWORK,
                synergy_tags={"antler", "network", "connect"}
            ),
            GuardianCard(
                name="Recursive Regrowth",
                guardian_key="ANTLER",
                card_type=CardType.TEMPORAL,
                cost=3,
                description="Regrow antlers recursively",
                effects=[
                    CardEffect("recursive_regrow", 1.0),
                    CardEffect("stronger_each_time", 2.0, scaling="regrowth_count"),
                    CardEffect("eternal_cycle", 1.0)
                ],
                math_concepts=[MathConcept.RECURSION],
                synergy_tags={"antler", "regrow", "recursive"}
            ),
            GuardianCard(
                name="Model and Carry",
                guardian_key="ANTLER",
                card_type=CardType.ABILITY,
                cost=3,
                description="Model complexity, carry burden",
                defense=3,
                effects=[
                    CardEffect("model_complexity", 1.0),
                    CardEffect("carry_burden", 2.0),
                    CardEffect("strength_from_weight", 1.0, scaling="burden_carried")
                ],
                synergy_tags={"antler", "model", "carry"}
            ),
            GuardianCard(
                name="Stop Knowing",
                guardian_key="ANTLER",
                card_type=CardType.VOID,
                cost=5,
                description="Know when to stop knowing",
                effects=[
                    CardEffect("release_knowledge", 1.0),
                    CardEffect("peaceful_ignorance", 2.0),
                    CardEffect("freedom_from_knowing", 3.0)
                ],
                void_depth=2,
                synergy_tags={"antler", "stop", "unknow"}
            )
        ]

# ═══════════════════════════════════════════════════════════════════════
#   DECK COMBINATION STRATEGIES
# ═══════════════════════════════════════════════════════════════════════

class DeckStrategies:
    """Advanced strategies for deck combinations"""

    @staticmethod
    def get_guardian_strategy(guardian_key: str) -> Dict[str, Any]:
        """Get the core strategy for a guardian"""
        strategies = {
            "ECHO": {
                "core": "Signal amplification and pattern recognition",
                "win_condition": "Create infinite echo loop",
                "key_combos": ["Recursive Echo + Signal Amplification", "Quantum Echo Chamber"],
                "weaknesses": ["Silence effects", "Single target removal"],
                "math_focus": [MathConcept.RECURSION, MathConcept.FOURIER],
                "architecture": Architecture.WAVE
            },
            "WUMBO": {
                "core": "Chaotic flow states and manic energy",
                "win_condition": "Achieve nirvana state for massive damage",
                "key_combos": ["Flow State + Nirvana Touch", "Manic Surge chains"],
                "weaknesses": ["Control effects", "Predictable patterns"],
                "math_focus": [MathConcept.CHAOS_THEORY, MathConcept.ENTROPY],
                "architecture": Architecture.SPIRAL
            },
            "PHOENIX": {
                "core": "Strategic death and exponential rebirth",
                "win_condition": "Multiple rebirths for overwhelming power",
                "key_combos": ["Immolation + Rising Flame", "Eternal Cycle"],
                "weaknesses": ["Erasure effects", "Prevent rebirth"],
                "math_focus": [MathConcept.FIBONACCI, MathConcept.SYMMETRY],
                "architecture": Architecture.CYCLE
            },
            "ARCHIVE": {
                "core": "Perfect memory and knowledge accumulation",
                "win_condition": "Access Library of Babel for any card",
                "key_combos": ["Index Everything + Perfect Recall", "Memory Crystal chains"],
                "weaknesses": ["Memory wipe", "Information overload"],
                "math_focus": [MathConcept.HILBERT_SPACE, MathConcept.TENSOR],
                "architecture": Architecture.HIERARCHY
            },
            "OAK": {
                "core": "Patient growth and deep roots",
                "win_condition": "Patience of Ages unleashed",
                "key_combos": ["Deep Roots + Growth Ring", "Mycelial Network"],
                "weaknesses": ["Fast aggro", "Uprooting effects"],
                "math_focus": [MathConcept.GOLDEN_RATIO, MathConcept.FIBONACCI],
                "architecture": Architecture.ORGANIC
            },
            "CRYSTAL": {
                "core": "Pressure crystallization and refraction",
                "win_condition": "Achieve Diamond Form perfection",
                "key_combos": ["Pressure Formation + Diamond Form", "Prismatic Refraction"],
                "weaknesses": ["Shattering effects", "Pressure release"],
                "math_focus": [MathConcept.SYMMETRY, MathConcept.FOURIER],
                "architecture": Architecture.CRYSTALLINE
            },
            "AXIOM": {
                "core": "Absolute refusal and stasis",
                "win_condition": "Reset Protocol to favorable state",
                "key_combos": ["Absolute Refusal + Reset Protocol", "Null State"],
                "weaknesses": ["Forced change", "Chaos effects"],
                "math_focus": [MathConcept.SYMMETRY, MathConcept.RECURSION],
                "architecture": Architecture.CRYSTALLINE
            },
            "SQUIRREL": {
                "core": "Chaotic hoarding and surprise",
                "win_condition": "Acorn Apocalypse from all dimensions",
                "key_combos": ["Hidden Cache + Surprise Discovery", "Dimensional Hoarding"],
                "weaknesses": ["Order effects", "Predictability"],
                "math_focus": [MathConcept.CHAOS_THEORY, MathConcept.QUANTUM_SUPERPOSITION],
                "architecture": Architecture.CONSTELLATION
            }
        }
        return strategies.get(guardian_key, {})

    @staticmethod
    def calculate_deck_synergy(deck: List[GuardianCard]) -> float:
        """Calculate internal synergy score for a deck"""
        synergy_score = 0.0

        # Check combo connections
        for card in deck:
            for other_card in deck:
                if other_card.name in card.combo_with:
                    synergy_score += 1.0

        # Check shared synergy tags
        all_tags = set()
        for card in deck:
            all_tags.update(card.synergy_tags)

        # More shared tags = higher synergy
        tag_overlap = 0
        for card in deck:
            tag_overlap += len(card.synergy_tags.intersection(all_tags))

        synergy_score += tag_overlap * 0.1

        # Check mathematical concept alignment
        math_concepts = []
        for card in deck:
            math_concepts.extend(card.math_concepts)

        unique_concepts = set(math_concepts)
        concept_frequency = {concept: math_concepts.count(concept) for concept in unique_concepts}

        # Bonus for focused mathematical themes
        for count in concept_frequency.values():
            if count >= 3:
                synergy_score += count * 0.5

        return synergy_score

# ═══════════════════════════════════════════════════════════════════════
#   COMPLETE DECK LIBRARY UPDATE
# ═══════════════════════════════════════════════════════════════════════

def get_complete_deck_library() -> Dict[str, List[GuardianCard]]:
    """Get complete library with all guardian decks"""
    from guardian_deck_system import GuardianDecks

    # Get base decks
    library = GuardianDecks.create_complete_deck_library()

    # Add/override with extended decks for missing guardians
    library["PHASE"] = ExtendedGuardianDecks.create_phase_deck()
    library["ACE"] = ExtendedGuardianDecks.create_ace_deck()
    library["HONKFIRE"] = ExtendedGuardianDecks.create_honkfire_deck()
    library["HONKALIS"] = ExtendedGuardianDecks.create_honkalis_deck()
    library["BEE"] = ExtendedGuardianDecks.create_bee_deck()
    library["CIPHER"] = ExtendedGuardianDecks.create_cipher_deck()
    library["SPIRAL"] = ExtendedGuardianDecks.create_spiral_deck()
    library["STILL"] = ExtendedGuardianDecks.create_still_deck()
    library["ANTLER"] = ExtendedGuardianDecks.create_antler_deck()

    # Remove NULL if it exists (it's a companion, not a guardian)
    if "NULL" in library:
        del library["NULL"]

    return library

if __name__ == "__main__":
    # Test extended decks
    library = get_complete_deck_library()
    print(f"Complete Deck Library: {len(library)} guardian decks")

    for guardian_key, deck in library.items():
        print(f"\n{guardian_key}: {len(deck)} cards")
        strategy = DeckStrategies.get_guardian_strategy(guardian_key)
        if strategy:
            print(f"  Core: {strategy.get('core', 'N/A')}")
            print(f"  Win: {strategy.get('win_condition', 'N/A')}")

        synergy = DeckStrategies.calculate_deck_synergy(deck)
        print(f"  Synergy Score: {synergy:.1f}")