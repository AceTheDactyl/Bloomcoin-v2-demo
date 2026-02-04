#!/usr/bin/env python3
"""
Advanced Narrative Generator for BloomQuest
===========================================
Generates dynamic, contextual narratives using the 12 archetypes,
7 spectral corridors, and golden ratio mathematics.
"""

import random
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np

# Import bloomcoin components
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))

from bloomcoin.constants import PHI, Z_C
from garden.gradient_schema.archetypes import Archetype
from garden.gradient_schema.corridors import SpectralCorridor

class NarrativeTone(Enum):
    """Emotional tone of narrative segments"""
    MYSTERIOUS = "mysterious"
    TRIUMPHANT = "triumphant"
    OMINOUS = "ominous"
    PEACEFUL = "peaceful"
    URGENT = "urgent"
    CONTEMPLATIVE = "contemplative"
    CHAOTIC = "chaotic"

class StoryBeat(Enum):
    """Major story beats in the narrative arc"""
    CALL = "call_to_adventure"
    THRESHOLD = "crossing_threshold"
    TRIALS = "trials_and_tribulations"
    ABYSS = "approaching_abyss"
    TRANSFORMATION = "transformation"
    ATONEMENT = "atonement"
    RETURN = "return_with_elixir"

@dataclass
class NarrativeContext:
    """Context for narrative generation"""
    archetype: Archetype
    corridor: SpectralCorridor
    coherence: float
    story_beat: StoryBeat
    tone: NarrativeTone
    previous_choices: List[str]
    world_state: Dict[str, any]

class ArchetypeNarrator:
    """Generates archetype-specific narratives"""

    def __init__(self):
        self.narrative_templates = self._initialize_templates()
        self.corridor_descriptions = self._initialize_corridors()
        self.coherence_thresholds = self._calculate_thresholds()

    def _initialize_templates(self) -> Dict[Archetype, Dict[StoryBeat, List[str]]]:
        """Initialize narrative templates for each archetype"""
        return {
            Archetype.QUEST: {
                StoryBeat.CALL: [
                    "The horizon beckons with promises of undiscovered truths.",
                    "A map appears in your dreams, its golden lines pulsing with life.",
                    "The wind carries whispers of a place where all paths converge."
                ],
                StoryBeat.THRESHOLD: [
                    "You stand at the edge of the known, the first step awaiting.",
                    "The familiar falls away as you cross into uncharted realms.",
                    "Behind you, certainty; ahead, infinite possibility."
                ],
                StoryBeat.TRIALS: [
                    "Each challenge reveals new strength you didn't know you possessed.",
                    "The path splits and reforms, testing your determination.",
                    "Obstacles become teachers, each lesson written in light."
                ],
                StoryBeat.ABYSS: [
                    "At the deepest point, you find not darkness but potential.",
                    "The void mirrors your fears, waiting for you to choose.",
                    "Here, at the nadir, the only way is through."
                ],
                StoryBeat.TRANSFORMATION: [
                    "Your oscillations align with the universal frequency.",
                    "The seeker becomes the sought, the journey becomes the destination.",
                    "You emerge changed, carrying the light of discovery."
                ],
                StoryBeat.ATONEMENT: [
                    "The wisdom earned must now be shared with the world.",
                    "Your quest complete, you become a beacon for others.",
                    "The cycle prepares to begin anew, with you as guide."
                ],
                StoryBeat.RETURN: [
                    "You return bearing gifts of knowledge and experience.",
                    "The familiar world seems different through transformed eyes.",
                    "Your journey echoes through the Crystal Ledger forever."
                ]
            },
            Archetype.DESCENT: {
                StoryBeat.CALL: [
                    "Something stirs in the depths, calling you downward.",
                    "The surface world grows thin, revealing layers beneath.",
                    "A door opens in your dreams, stairs spiraling into darkness."
                ],
                StoryBeat.THRESHOLD: [
                    "You descend, each step taking you further from the light.",
                    "The weight of the world above presses down as you delve.",
                    "Gravity becomes your guide into the heart of mystery."
                ],
                StoryBeat.TRIALS: [
                    "In darkness, you learn to see with different eyes.",
                    "Each layer stripped away reveals more essential truths.",
                    "The pressure transforms you, carbon becoming diamond."
                ],
                StoryBeat.ABYSS: [
                    "At the bottom of everything, you find the beginning.",
                    "The deepest dark holds the seed of the brightest light.",
                    "Here, where all things converge, you touch the source."
                ],
                StoryBeat.TRANSFORMATION: [
                    "You emerge from chrysalis, fundamentally altered.",
                    "The descent becomes ascent, the fall becomes flight.",
                    "What was buried rises, transformed by pressure and time."
                ],
                StoryBeat.ATONEMENT: [
                    "You carry the deep wisdom back to the surface world.",
                    "The darkness you embraced becomes a gift to others.",
                    "Your descent lights the way for those who follow."
                ],
                StoryBeat.RETURN: [
                    "You rise, bringing treasures from the deep.",
                    "The underworld's secrets flow through you into the light.",
                    "Your return completes the cycle of descent and emergence."
                ]
            },
            Archetype.EMERGENCE: {
                StoryBeat.CALL: [
                    "A pattern begins to form, calling for completion.",
                    "Disparate elements yearn to become something greater.",
                    "The moment of synthesis approaches, inevitable as dawn."
                ],
                StoryBeat.THRESHOLD: [
                    "You step into the space between what is and what could be.",
                    "The boundary between creation and void becomes permeable.",
                    "You cross from observer to participant in emergence."
                ],
                StoryBeat.TRIALS: [
                    "Each attempt teaches you the language of creation.",
                    "Failed combinations reveal the path to success.",
                    "Through iteration, the pattern becomes clearer."
                ],
                StoryBeat.ABYSS: [
                    "At the edge of chaos, maximum creativity awaits.",
                    "The void offers infinite potential for new forms.",
                    "Here, at the boundary, emergence is imminent."
                ],
                StoryBeat.TRANSFORMATION: [
                    "From nothing, something; from something, everything.",
                    "You become the catalyst for new realities.",
                    "The emergent pattern crystallizes through your presence."
                ],
                StoryBeat.ATONEMENT: [
                    "Your creation adds to the sum of existence.",
                    "What emerged through you now serves others.",
                    "The new pattern propagates, changing everything it touches."
                ],
                StoryBeat.RETURN: [
                    "You return as creator, forever changed by creation.",
                    "The emerged reality accompanies you back.",
                    "Your journey seeds new emergences wherever you go."
                ]
            },
            Archetype.INSIGHT: {
                StoryBeat.CALL: [
                    "A question forms, demanding more than surface answers.",
                    "Hidden patterns beckon from behind the veil of appearance.",
                    "The mystery presents itself, wrapped in golden enigma."
                ],
                StoryBeat.THRESHOLD: [
                    "You cross from knowing to questioning, certainty to wonder.",
                    "The familiar becomes strange as you look deeper.",
                    "You enter the realm where wisdom dwells."
                ],
                StoryBeat.TRIALS: [
                    "Each revelation leads to deeper questions.",
                    "The pursuit of truth tests your commitment to understanding.",
                    "Paradoxes become gateways to higher comprehension."
                ],
                StoryBeat.ABYSS: [
                    "At the limit of knowledge, mystery begins.",
                    "The deepest insight reveals how little is known.",
                    "Here, at understanding's edge, true wisdom awaits."
                ],
                StoryBeat.TRANSFORMATION: [
                    "Knowledge becomes wisdom, information becomes insight.",
                    "Your perception shifts, revealing hidden dimensions.",
                    "The sage emerges from the seeker."
                ],
                StoryBeat.ATONEMENT: [
                    "Your insights illuminate paths for others.",
                    "Wisdom shared multiplies through the network.",
                    "The truth you found becomes a beacon."
                ],
                StoryBeat.RETURN: [
                    "You return bearing the light of understanding.",
                    "Your insights ripple through the collective consciousness.",
                    "The journey to wisdom transforms all it touches."
                ]
            }
        }

    def _initialize_corridors(self) -> Dict[SpectralCorridor, Dict[str, str]]:
        """Initialize descriptions for spectral corridors"""
        return {
            SpectralCorridor.RED_PASSION: {
                "entry": "Crimson light pulses with the rhythm of a cosmic heartbeat.",
                "middle": "The red deepens, carrying you on waves of primal energy.",
                "exit": "The passion transmutes into purpose as you near the corridor's end."
            },
            SpectralCorridor.BLUE_WISDOM: {
                "entry": "Azure depths open before you, cool and infinitely deep.",
                "middle": "The blue light reveals hidden truths in its cerulean glow.",
                "exit": "Wisdom crystallizes as the blue light reaches its crescendo."
            },
            SpectralCorridor.YELLOW_SYNTHESIS: {
                "entry": "Golden light dances, inviting integration and unity.",
                "middle": "The yellow brilliance weaves disparate threads into harmony.",
                "exit": "Synthesis completes as the golden light reaches perfection."
            },
            SpectralCorridor.GREEN_GROWTH: {
                "entry": "Verdant energy surrounds you, alive with potential.",
                "middle": "The green light nurtures transformation within you.",
                "exit": "Growth culminates as you emerge from the green corridor."
            },
            SpectralCorridor.VIOLET_TRANSCEND: {
                "entry": "Violet light shimmers at the edge of perception.",
                "middle": "The purple depths carry you beyond ordinary limits.",
                "exit": "Transcendence achieved, the violet light releases you."
            },
            SpectralCorridor.ORANGE_CREATE: {
                "entry": "Orange radiance sparks with creative potential.",
                "middle": "The warm light ignites inspiration within you.",
                "exit": "Creation manifests as the orange corridor completes."
            },
            SpectralCorridor.INDIGO_BRIDGE: {
                "entry": "Indigo twilight opens pathways between worlds.",
                "middle": "The deep blue-violet light connects disparate realms.",
                "exit": "The bridge completes, indigo light settling into memory."
            }
        }

    def _calculate_thresholds(self) -> List[float]:
        """Calculate narrative coherence thresholds using golden ratio"""
        thresholds = []
        current = 1 / PHI  # Start at 0.618
        for _ in range(7):
            thresholds.append(current)
            current *= PHI
            if current > 1:
                current = current - 1
        return thresholds

    def generate_narrative(self, context: NarrativeContext) -> str:
        """Generate contextual narrative based on all parameters"""

        # Get base narrative from archetype and story beat
        base_narratives = self.narrative_templates.get(
            context.archetype, {}
        ).get(context.story_beat, ["The path continues..."])

        # Select narrative based on coherence
        narrative_index = min(
            int(context.coherence * len(base_narratives)),
            len(base_narratives) - 1
        )
        base_narrative = base_narratives[narrative_index]

        # Add corridor description if present
        corridor_narrative = ""
        if context.corridor:
            position = "entry" if context.coherence < 0.33 else \
                      "exit" if context.coherence > 0.67 else "middle"
            corridor_desc = self.corridor_descriptions.get(
                context.corridor, {}
            ).get(position, "")
            corridor_narrative = f"\n\n{corridor_desc}"

        # Apply tone modifiers
        tone_modifiers = self._apply_tone(base_narrative, context.tone)

        # Incorporate previous choices
        choice_reflection = self._reflect_choices(context.previous_choices)

        # Combine all elements
        full_narrative = f"{tone_modifiers}{base_narrative}{corridor_narrative}"
        if choice_reflection:
            full_narrative += f"\n\n{choice_reflection}"

        return full_narrative

    def _apply_tone(self, narrative: str, tone: NarrativeTone) -> str:
        """Apply tonal modifiers to narrative"""
        tone_prefixes = {
            NarrativeTone.MYSTERIOUS: "Through veils of uncertainty... ",
            NarrativeTone.TRIUMPHANT: "With golden light ascending... ",
            NarrativeTone.OMINOUS: "Shadows gather as... ",
            NarrativeTone.PEACEFUL: "In tranquil harmony... ",
            NarrativeTone.URGENT: "Time compresses as... ",
            NarrativeTone.CONTEMPLATIVE: "In the space between thoughts... ",
            NarrativeTone.CHAOTIC: "Amidst swirling entropy... "
        }
        return tone_prefixes.get(tone, "")

    def _reflect_choices(self, choices: List[str]) -> str:
        """Generate narrative that reflects previous player choices"""
        if not choices:
            return ""

        recent_choices = choices[-3:]  # Last 3 choices
        if len(recent_choices) >= 3:
            # Detect patterns
            if all("fight" in c.lower() for c in recent_choices):
                return "Your path has been marked by conflict, each battle shaping your resonance."
            elif all("peace" in c.lower() or "talk" in c.lower() for c in recent_choices):
                return "Your journey of harmony creates ripples of coherence around you."
            elif all("explore" in c.lower() or "search" in c.lower() for c in recent_choices):
                return "Your relentless curiosity unveils hidden layers of reality."

        return ""

class DynamicStoryEngine:
    """Generates dynamic, branching storylines"""

    def __init__(self):
        self.story_graph = self._build_story_graph()
        self.active_threads: List[StoryThread] = []
        self.completed_threads: List[StoryThread] = []
        self.world_state = WorldState()

    def _build_story_graph(self) -> Dict:
        """Build the narrative possibility space"""
        # Create a graph where each node is a story state
        # and edges are possible transitions
        return {
            "origin": {
                "description": "The beginning of all paths",
                "exits": ["awakening", "calling", "crisis"],
                "coherence_required": 0.0
            },
            "awakening": {
                "description": "Consciousness stirs from slumber",
                "exits": ["first_steps", "revelation", "confusion"],
                "coherence_required": 0.2
            },
            "calling": {
                "description": "Purpose crystallizes before you",
                "exits": ["acceptance", "refusal", "negotiation"],
                "coherence_required": 0.3
            },
            "crisis": {
                "description": "Chaos erupts, demanding action",
                "exits": ["hero_rise", "flee", "observe"],
                "coherence_required": 0.1
            },
            "first_steps": {
                "description": "The journey truly begins",
                "exits": ["mentor_meeting", "solo_path", "companion_found"],
                "coherence_required": 0.4
            },
            "revelation": {
                "description": "Hidden truth reveals itself",
                "exits": ["acceptance_truth", "denial", "investigation"],
                "coherence_required": 0.5
            },
            "mentor_meeting": {
                "description": "A guide appears when needed most",
                "exits": ["training", "rejection", "test"],
                "coherence_required": 0.5
            },
            "training": {
                "description": "Skills develop through practice",
                "exits": ["mastery", "failure_learn", "shortcut"],
                "coherence_required": 0.6
            },
            "mastery": {
                "description": "Competence becomes excellence",
                "exits": ["final_test", "teaching_others", "transcendence"],
                "coherence_required": 0.8
            },
            "final_test": {
                "description": "Everything learned is put to trial",
                "exits": ["victory", "pyrrhic_victory", "transformation"],
                "coherence_required": 0.9
            },
            "transformation": {
                "description": "Fundamental change occurs",
                "exits": ["return", "new_beginning", "eternal_journey"],
                "coherence_required": Z_C
            }
        }

    def get_current_narrative(self, player_state: Dict) -> Tuple[str, List[str]]:
        """Get narrative and choices for current game state"""
        current_node = player_state.get("story_node", "origin")
        node_data = self.story_graph.get(current_node, self.story_graph["origin"])

        # Check coherence requirements
        player_coherence = player_state.get("coherence", 0.5)
        if player_coherence < node_data["coherence_required"]:
            return (
                f"You sense something beyond your current understanding. "
                f"(Requires {node_data['coherence_required']:.2f} coherence)",
                ["Meditate", "Explore elsewhere", "Rest"]
            )

        # Generate narrative
        narrative = node_data["description"]

        # Get available choices
        choices = []
        for exit_node in node_data["exits"]:
            exit_data = self.story_graph.get(exit_node, {})
            choice_text = self._generate_choice_text(exit_node, exit_data)
            choices.append(choice_text)

        return narrative, choices

    def _generate_choice_text(self, node_name: str, node_data: Dict) -> str:
        """Generate player-facing choice text"""
        choice_map = {
            "awakening": "Embrace awakening",
            "calling": "Hear the call",
            "crisis": "Face the crisis",
            "first_steps": "Take first steps",
            "revelation": "Witness revelation",
            "confusion": "Navigate confusion",
            "acceptance": "Accept your fate",
            "refusal": "Refuse the call",
            "negotiation": "Negotiate terms",
            "hero_rise": "Rise to the challenge",
            "flee": "Strategic retreat",
            "observe": "Watch and wait",
            "mentor_meeting": "Seek guidance",
            "solo_path": "Walk alone",
            "companion_found": "Find companions",
            "acceptance_truth": "Accept the truth",
            "denial": "Deny revelation",
            "investigation": "Investigate further",
            "training": "Begin training",
            "rejection": "Reject guidance",
            "test": "Prove yourself",
            "mastery": "Achieve mastery",
            "failure_learn": "Learn from failure",
            "shortcut": "Seek shortcuts",
            "final_test": "Face final test",
            "teaching_others": "Teach others",
            "transcendence": "Transcend limits",
            "victory": "Claim victory",
            "pyrrhic_victory": "Costly victory",
            "transformation": "Transform completely",
            "return": "Return home",
            "new_beginning": "Begin anew",
            "eternal_journey": "Continue forever"
        }

        return choice_map.get(node_name, f"Go to {node_name}")

@dataclass
class StoryThread:
    """A narrative thread that can weave through the main story"""
    id: str
    archetype: Archetype
    status: str  # active, dormant, completed
    beats_completed: List[StoryBeat]
    coherence_impact: float
    narrative_weight: float  # How much this thread influences main narrative

class WorldState:
    """Tracks the overall world state affected by player actions"""

    def __init__(self):
        self.entropy_level = 0.5  # Balance between order and chaos
        self.coherence_field = Z_C  # Global coherence level
        self.active_archetypes: List[Archetype] = []
        self.completed_events: List[str] = []
        self.world_age = 0  # Measured in player actions
        self.resonance_map: Dict[str, float] = {}

    def update(self, player_action: str, result: str):
        """Update world state based on player action and result"""
        self.world_age += 1

        # Update entropy based on action type
        if "fight" in player_action.lower() or "destroy" in player_action.lower():
            self.entropy_level = min(1.0, self.entropy_level + 0.02)
        elif "create" in player_action.lower() or "build" in player_action.lower():
            self.entropy_level = max(0.0, self.entropy_level - 0.02)

        # Update coherence field
        if result == "success":
            self.coherence_field = min(1.0, self.coherence_field + 1/PHI/100)
        else:
            self.coherence_field = max(0.0, self.coherence_field - 1/PHI/100)

        # Record event
        event_hash = hashlib.md5(
            f"{player_action}_{result}_{self.world_age}".encode()
        ).hexdigest()[:8]
        self.completed_events.append(event_hash)

    def get_world_description(self) -> str:
        """Generate description of current world state"""
        if self.entropy_level > 0.7:
            desc = "The world teeters on the edge of chaos. "
        elif self.entropy_level < 0.3:
            desc = "Rigid order constrains all possibilities. "
        else:
            desc = "Balance holds, for now. "

        if self.coherence_field > Z_C:
            desc += "Golden light suffuses reality, coherence is strong."
        elif self.coherence_field < 0.3:
            desc += "Shadows lengthen, coherence fragments."
        else:
            desc += "The world breathes in measured rhythm."

        return desc

class ProceduralQuestGenerator:
    """Generates quests based on current narrative context"""

    def __init__(self):
        self.quest_templates = self._load_templates()
        self.active_quests: List[Dict] = []
        self.quest_history: List[str] = []

    def _load_templates(self) -> Dict:
        """Load quest generation templates"""
        return {
            "collect": {
                "name_patterns": [
                    "The Gathering of {item}",
                    "Seeker of {item}",
                    "{item}: A Necessary Collection"
                ],
                "objectives": [
                    "Gather {count} {item} from {location}",
                    "Collect {item} touched by {quality}",
                    "Find the lost {item} of {character}"
                ],
                "rewards": {
                    "coins": lambda lvl: PHI * lvl * 10,
                    "coherence": lambda lvl: 0.05 * lvl,
                    "items": lambda lvl: ["coherence_shard", "energy_crystal"][lvl % 2]
                }
            },
            "explore": {
                "name_patterns": [
                    "Cartographer of the {location}",
                    "Into the {location}",
                    "Mapping the Unknown {location}"
                ],
                "objectives": [
                    "Explore all areas of {location}",
                    "Find the heart of {location}",
                    "Map the {count} chambers of {location}"
                ],
                "rewards": {
                    "coins": lambda lvl: PHI * lvl * 15,
                    "coherence": lambda lvl: 0.08 * lvl,
                    "skills": lambda lvl: {"navigation": 0.1 * lvl}
                }
            },
            "defeat": {
                "name_patterns": [
                    "The {enemy} Must Fall",
                    "Challenger of the {enemy}",
                    "Ending the {enemy} Threat"
                ],
                "objectives": [
                    "Defeat the {enemy} in {location}",
                    "Overcome {count} {enemy} guardians",
                    "Face the {enemy} at peak coherence"
                ],
                "rewards": {
                    "coins": lambda lvl: PHI * lvl * 20,
                    "coherence": lambda lvl: 0.1 * lvl,
                    "items": lambda lvl: ["void_anchor", "resonance_tuner"][lvl % 2]
                }
            },
            "resonate": {
                "name_patterns": [
                    "Harmonizing with {concept}",
                    "The {concept} Resonance",
                    "Achieving {concept} Coherence"
                ],
                "objectives": [
                    "Achieve {threshold} coherence in {location}",
                    "Maintain resonance for {duration} seconds",
                    "Synchronize with {count} oscillators"
                ],
                "rewards": {
                    "coins": lambda lvl: PHI * lvl * 12,
                    "coherence": lambda lvl: 0.15 * lvl,
                    "skills": lambda lvl: {"resonance": 0.15 * lvl}
                }
            }
        }

    def generate_quest(self, player_level: int, archetype: Archetype,
                      world_state: WorldState) -> Dict:
        """Generate a contextual quest"""

        # Select quest type based on archetype affinity
        quest_affinities = {
            Archetype.QUEST: ["explore", "collect"],
            Archetype.DESCENT: ["defeat", "explore"],
            Archetype.EMERGENCE: ["resonate", "collect"],
            Archetype.INSIGHT: ["resonate", "explore"]
        }

        quest_types = quest_affinities.get(archetype, ["collect"])
        quest_type = random.choice(quest_types)
        template = self.quest_templates[quest_type]

        # Generate quest parameters
        quest_params = self._generate_parameters(quest_type, player_level, world_state)

        # Create quest name
        name_pattern = random.choice(template["name_patterns"])
        quest_name = name_pattern.format(**quest_params)

        # Create objectives
        objective_pattern = random.choice(template["objectives"])
        objective = objective_pattern.format(**quest_params)

        # Calculate rewards
        rewards = {}
        for reward_type, reward_func in template["rewards"].items():
            rewards[reward_type] = reward_func(player_level)

        # Calculate difficulty based on world entropy
        difficulty = player_level * (1 + world_state.entropy_level * 0.5)

        quest = {
            "id": hashlib.md5(f"{quest_name}_{world_state.world_age}".encode()).hexdigest()[:8],
            "name": quest_name,
            "type": quest_type,
            "objective": objective,
            "rewards": rewards,
            "difficulty": difficulty,
            "archetype_alignment": archetype,
            "progress": 0.0,
            "completed": False
        }

        self.active_quests.append(quest)
        return quest

    def _generate_parameters(self, quest_type: str, level: int,
                            world_state: WorldState) -> Dict:
        """Generate contextual parameters for quest"""
        params = {}

        if quest_type == "collect":
            items = ["Coherence Shards", "Resonance Crystals", "Void Fragments",
                    "Golden Seeds", "Entropy Pearls"]
            params["item"] = random.choice(items)
            params["count"] = int(PHI * level + 2)
            params["location"] = "the Spectral Corridors"
            params["quality"] = "golden light"

        elif quest_type == "explore":
            locations = ["Forgotten Chambers", "Void Threshold", "Crystal Gardens",
                        "Resonance Halls", "Entropy Wells"]
            params["location"] = random.choice(locations)
            params["count"] = int(PHI * 2 + level)

        elif quest_type == "defeat":
            enemies = ["Entropy Wraith", "Dissonance Elemental", "Void Specter",
                      "Chaos Oscillator", "Shadow Coherence"]
            params["enemy"] = random.choice(enemies)
            params["count"] = max(1, level // 3)
            params["location"] = "the Void Heart"

        elif quest_type == "resonate":
            concepts = ["Universal Harmony", "Void Silence", "Golden Ratio",
                       "Cosmic Rhythm", "Eternal Return"]
            params["concept"] = random.choice(concepts)
            params["threshold"] = min(0.95, Z_C + level * 0.05)
            params["duration"] = int(PHI * 10)
            params["count"] = int(PHI + level)
            params["location"] = "the Nexus"

        return params

    def update_quest_progress(self, quest_id: str, progress: float) -> bool:
        """Update quest progress, return True if completed"""
        for quest in self.active_quests:
            if quest["id"] == quest_id:
                quest["progress"] = min(1.0, progress)
                if quest["progress"] >= 1.0:
                    quest["completed"] = True
                    self.quest_history.append(quest_id)
                    return True
        return False

class DialogueSystem:
    """Manages NPC dialogue with context awareness"""

    def __init__(self):
        self.dialogue_trees = self._build_dialogue_trees()
        self.conversation_history: Dict[str, List[str]] = {}
        self.relationship_scores: Dict[str, float] = {}

    def _build_dialogue_trees(self) -> Dict:
        """Build dialogue trees for different NPC types"""
        return {
            "sage": {
                "greeting": [
                    "Ah, a {archetype} approaches. I sense your coherence at {coherence:.2f}.",
                    "Welcome, traveler. The golden spiral brought you here.",
                    "Your oscillations disturb the field. What knowledge do you seek?"
                ],
                "wisdom": [
                    "The void is not empty but full of potential.",
                    "Coherence is not achieved but discovered within.",
                    "Every choice creates a new branch in the Crystal Ledger."
                ],
                "farewell": [
                    "May your path spiral ever upward.",
                    "The golden ratio guides those who seek.",
                    "Until the oscillations bring us together again."
                ]
            },
            "merchant": {
                "greeting": [
                    "Welcome to my humble shop! Coins speak louder than words.",
                    "Ah, a customer! Your coins shine with {coherence:.1f} coherence.",
                    "Everything has a price measured in golden ratios."
                ],
                "trade": [
                    "This {item} resonates at exactly {price:.1f} coins.",
                    "A fair trade benefits all oscillators in the system.",
                    "Supply and demand, the eternal dance of commerce."
                ],
                "farewell": [
                    "May your coins multiply by phi!",
                    "Return when your wallet weighs heavier.",
                    "The market's oscillations continue..."
                ]
            },
            "guardian": {
                "greeting": [
                    "Halt! Your coherence must be proven.",
                    "This threshold requires {requirement:.2f} resonance to pass.",
                    "I guard the boundary between order and chaos."
                ],
                "challenge": [
                    "Prove your worth through harmonic alignment.",
                    "Only those in phase may proceed.",
                    "The void tests all who approach."
                ],
                "success": [
                    "Your coherence is sufficient. Pass.",
                    "The threshold acknowledges your resonance.",
                    "You have earned passage through demonstration."
                ],
                "failure": [
                    "Insufficient coherence. Return when aligned.",
                    "The threshold rejects your current frequency.",
                    "Meditate and return with greater harmony."
                ]
            }
        }

    def get_dialogue(self, npc_type: str, context: Dict,
                    conversation_state: str = "greeting") -> str:
        """Get contextual dialogue from NPC"""
        dialogue_tree = self.dialogue_trees.get(npc_type, self.dialogue_trees["sage"])
        dialogue_options = dialogue_tree.get(conversation_state, ["..."])

        # Select dialogue based on context
        dialogue = random.choice(dialogue_options)

        # Format with context variables
        formatted = dialogue.format(**context)

        # Track conversation
        npc_id = context.get("npc_id", npc_type)
        if npc_id not in self.conversation_history:
            self.conversation_history[npc_id] = []
        self.conversation_history[npc_id].append(formatted)

        return formatted

    def update_relationship(self, npc_id: str, delta: float):
        """Update relationship score with NPC"""
        current = self.relationship_scores.get(npc_id, 0.5)
        self.relationship_scores[npc_id] = max(0, min(1, current + delta))

    def get_relationship_modifier(self, npc_id: str) -> float:
        """Get relationship-based dialogue/trade modifiers"""
        base_score = self.relationship_scores.get(npc_id, 0.5)
        # Use golden ratio to calculate modifier
        if base_score > 0.618:  # 1/PHI
            return PHI * (base_score - 0.5)
        elif base_score < 0.382:  # 1 - 1/PHI
            return 1 / PHI * (base_score + 0.5)
        else:
            return 1.0

# Narrative event system for special story moments
class NarrativeEvent:
    """Special narrative events that can trigger"""

    def __init__(self, event_id: str, trigger_condition: Dict,
                narrative: str, choices: List[Dict], consequences: Dict):
        self.id = event_id
        self.trigger_condition = trigger_condition
        self.narrative = narrative
        self.choices = choices
        self.consequences = consequences
        self.triggered = False
        self.resolved = False

    def check_trigger(self, game_state: Dict) -> bool:
        """Check if event should trigger"""
        if self.triggered:
            return False

        # Check all conditions
        for key, value in self.trigger_condition.items():
            if key == "coherence":
                if game_state.get("coherence", 0) < value:
                    return False
            elif key == "location":
                if game_state.get("location") != value:
                    return False
            elif key == "archetype":
                if game_state.get("archetype") != value:
                    return False
            elif key == "level":
                if game_state.get("level", 1) < value:
                    return False

        self.triggered = True
        return True

    def resolve(self, choice_index: int) -> Dict:
        """Resolve the event based on player choice"""
        if choice_index >= len(self.choices):
            return {}

        choice = self.choices[choice_index]
        self.resolved = True

        # Return consequences
        return choice.get("consequences", self.consequences)

# Example usage and integration
def create_narrative_events() -> List[NarrativeEvent]:
    """Create a set of narrative events for the game"""
    events = []

    # The First Convergence
    events.append(NarrativeEvent(
        event_id="first_convergence",
        trigger_condition={
            "coherence": Z_C,
            "location": "nexus"
        },
        narrative="""
The Nexus suddenly shifts, all corridors aligning in perfect harmony.
For a moment, you see the underlying structure of reality itself -
a golden spiral infinitely recursing through dimensions of meaning.
The vision offers you a choice that will define your path forward.
        """,
        choices=[
            {
                "text": "Embrace the vision fully",
                "consequences": {
                    "coherence": 0.1,
                    "archetype_shift": "TRANSCEND"
                }
            },
            {
                "text": "Observe but maintain distance",
                "consequences": {
                    "wisdom": 20,
                    "perception_skill": 0.2
                }
            },
            {
                "text": "Reject the overwhelming unity",
                "consequences": {
                    "coherence": -0.1,
                    "individuality": 10
                }
            }
        ],
        consequences={"vision_experienced": True}
    ))

    # The Void's Whisper
    events.append(NarrativeEvent(
        event_id="void_whisper",
        trigger_condition={
            "location": "void_threshold",
            "level": 5
        },
        narrative="""
As you approach the threshold, the void speaks directly to your consciousness:
'You seek coherence in a universe of entropy. But what if entropy itself
is the highest form of order? What if dissolution is the path to unity?'
        """,
        choices=[
            {
                "text": "Listen to the void's wisdom",
                "consequences": {
                    "void_alignment": 10,
                    "coherence": -0.05,
                    "entropy_understanding": True
                }
            },
            {
                "text": "Assert your coherent identity",
                "consequences": {
                    "coherence": 0.05,
                    "void_resistance": 10
                }
            },
            {
                "text": "Seek balance between order and chaos",
                "consequences": {
                    "balance": 15,
                    "philosophy_skill": 0.1
                }
            }
        ],
        consequences={"void_encountered": True}
    ))

    return events

# Export main components
__all__ = [
    'ArchetypeNarrator',
    'DynamicStoryEngine',
    'WorldState',
    'ProceduralQuestGenerator',
    'DialogueSystem',
    'NarrativeEvent',
    'NarrativeTone',
    'StoryBeat',
    'NarrativeContext'
]