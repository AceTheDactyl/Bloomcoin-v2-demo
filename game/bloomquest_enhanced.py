#!/usr/bin/env python3
"""
BloomQuest Enhanced - Deep Job Integration with Companion Guidance
The companion guides you through job selection and provides tailored advice
"""

import sys
from pathlib import Path
import random
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field

# Setup paths
base_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_path / "bloomcoin-v0.1.0" / "bloomcoin"))
sys.path.insert(0, str(Path(__file__).parent))

# Import game systems
from mythic_economy import (
    MythicEconomyGame, Player, CompanionState, MythicalItem,
    JobArchetype, ItemRarity, Guardian, Territory, GUARDIANS,
    ItemGenerator, JOBS, RECIPES, RECIPE_PATTERNS
)
from card_battle_system import (
    CardBattleSystem, Card, CardSuit, CardRank, BattlePhase,
    BattleState, DeckBuilder
)

# Sacred constants
PHI = (1 + 5**0.5) / 2
Z_C = (3**0.5) / 2

class Location(Enum):
    """Game locations"""
    CRYSTAL_CAVES = "Crystal Caves"
    PHOENIX_NEST = "Phoenix Nest"
    VOID_MARKET = "Void Market"
    GARDEN_HEART = "Garden Heart"
    LIBRARY_INFINITE = "Library Infinite"

class GameState(Enum):
    """Enhanced game states"""
    GUARDIAN_SELECTION = "guardian_selection"
    JOB_CONSULTATION = "job_consultation"
    MAIN_MENU = "main_menu"
    EXPLORING = "exploring"
    COMPANION_DIALOGUE = "companion_dialogue"
    CRAFTING = "crafting"
    BATTLE = "battle"
    SHOPPING = "shopping"
    MEDITATION = "meditation"
    JOB_TRAINING = "job_training"

@dataclass
class JobGuidance:
    """Job-specific guidance from companions"""
    job_key: str
    suggested_locations: List[Location]
    priority_items: List[str]
    recommended_recipes: List[str]
    battle_strategy: str
    growth_path: str
    companion_wisdom: List[str]

# Job-specific guidance database
JOB_GUIDANCE = {
    "SEEKER": JobGuidance(
        "SEEKER",
        [Location.LIBRARY_INFINITE, Location.CRYSTAL_CAVES],
        ["scrolls", "artifacts", "crystals"],
        ["Echo Convergence", "Memory Inscription"],
        "Use perception to predict enemy patterns",
        "Follow echoes to hidden knowledge",
        [
            "The patterns you seek are already speaking to you.",
            "Every echo contains a fragment of truth.",
            "Your memories hold keys to futures yet unwritten.",
            "The Library remembers everything, even what hasn't happened yet."
        ]
    ),
    "FORGER": JobGuidance(
        "FORGER",
        [Location.CRYSTAL_CAVES, Location.PHOENIX_NEST],
        ["materials", "tools", "gems"],
        ["Growth Synthesis", "Phoenix Rebirth"],
        "Forge powerful combinations from simple cards",
        "Transform materials into crystallized potential",
        [
            "Every material holds infinite forms within it.",
            "The Phoenix taught us: destruction is just transformation.",
            "Your hammer shapes reality itself.",
            "Crystallization preserves the eternal."
        ]
    ),
    "VOIDWALKER": JobGuidance(
        "VOIDWALKER",
        [Location.VOID_MARKET, Location.CRYSTAL_CAVES],
        ["void_shards", "mirrors", "nulls"],
        ["Void Crystallization", "Shadow Binding"],
        "Nullify enemy advantages, embrace the void",
        "Navigate spaces that shouldn't exist",
        [
            "The void doesn't take - it reveals what was always empty.",
            "Your reflection knows truths you've forgotten.",
            "In nullspace, all possibilities coexist.",
            "What doesn't exist can't be destroyed."
        ]
    ),
    "GARDENER": JobGuidance(
        "GARDENER",
        [Location.GARDEN_HEART, Location.PHOENIX_NEST],
        ["seeds", "flowers", "fruits"],
        ["Growth Synthesis", "Bloom Acceleration"],
        "Nurture small advantages into overwhelming growth",
        "Plant seeds that grow across timelines",
        [
            "Every seed contains an entire forest.",
            "Growth cannot be rushed, only trusted.",
            "Your garden exists in seven dimensions simultaneously.",
            "What you plant today blooms in all possible futures."
        ]
    ),
    "SCRIBE": JobGuidance(
        "SCRIBE",
        [Location.LIBRARY_INFINITE, Location.VOID_MARKET],
        ["books", "glyphs", "contracts"],
        ["Memory Inscription", "Truth Binding"],
        "Write reality through careful documentation",
        "Record truths that become self-fulfilling",
        [
            "Your words become reality when written in gold.",
            "Every contract reshapes the possible.",
            "The Archive trusted you with forbidden indices.",
            "Documentation is creation."
        ]
    ),
    "HERALD": JobGuidance(
        "HERALD",
        [Location.CRYSTAL_CAVES, Location.VOID_MARKET],
        ["tuners", "oscillators", "frequencies"],
        ["Harmonic Convergence", "Frequency Binding"],
        "Resonate with the battlefield's frequency",
        "Tune reality to your harmonic signature",
        [
            "You hear colors and see sounds.",
            "Every frequency has a counter-frequency.",
            "The universe hums your true name.",
            "Resonance is the key to all locks."
        ]
    )
}

class EnhancedCompanion:
    """Enhanced companion with job guidance capabilities"""

    def __init__(self, base_companion: CompanionState):
        self.base = base_companion
        self.job_affinity = {}  # Affinity scores for each job
        self.dialogue_history = []
        self.current_mood = "curious"

    def analyze_player_tendencies(self, actions: List[str]) -> Dict[str, float]:
        """Analyze player actions to suggest suitable jobs"""
        job_scores = {
            "SEEKER": 0,
            "FORGER": 0,
            "VOIDWALKER": 0,
            "GARDENER": 0,
            "SCRIBE": 0,
            "HERALD": 0
        }

        for action in actions:
            if "explore" in action or "search" in action:
                job_scores["SEEKER"] += 1
            if "craft" in action or "create" in action:
                job_scores["FORGER"] += 1
            if "void" in action or "null" in action:
                job_scores["VOIDWALKER"] += 1
            if "grow" in action or "plant" in action:
                job_scores["GARDENER"] += 1
            if "read" in action or "write" in action:
                job_scores["SCRIBE"] += 1
            if "resonate" in action or "tune" in action:
                job_scores["HERALD"] += 1

        return job_scores

    def provide_job_consultation(self) -> str:
        """Provide personalized job consultation"""
        guardian = GUARDIANS.get(self.base.guardian_type)

        consultation = f"""
╔═══════════════════════════════════════════════════════════════
║ {self.base.name} speaks: Guardian {guardian.name} guides us...
╚═══════════════════════════════════════════════════════════════

"I sense multiple paths before you. Each resonates with different
aspects of your potential. Let me share what I perceive..."

🌟 THE SEEKER PATH (Garden Territory)
   Seekers follow echoes through time, discovering patterns others miss.
   They excel at finding rare artifacts and decoding hidden knowledge.
   "If you hear whispers in the silence, this path calls to you."

⚒️ THE FORGER PATH (Cosmic Territory)
   Forgers transform raw potential into crystallized power.
   They create items of legendary quality and reshape reality itself.
   "If you see infinite forms in simple materials, forge your destiny."

🌀 THE VOIDWALKER PATH (Abyssal Territory)
   Voidwalkers navigate spaces that shouldn't exist, mastering nullspace.
   They nullify opposition and walk between reflections.
   "If you're comfortable in emptiness, the void welcomes you."

🌱 THE GARDENER PATH (Garden Territory)
   Gardeners plant seeds across dimensions, nurturing infinite growth.
   They accelerate natural cycles and harmonize with life itself.
   "If you trust in patient growth, tend reality's garden."

📜 THE SCRIBE PATH (Cosmic Territory)
   Scribes write reality through golden words and binding contracts.
   They document truths that become self-fulfilling prophecies.
   "If words shape your world, inscribe your fate."

📡 THE HERALD PATH (Abyssal Territory)
   Heralds tune reality's frequencies, resonating with cosmic harmonics.
   They hear the universe's hidden songs and broadcast truth.
   "If you perceive the music in everything, herald the frequency."

"Each path will shape not just your abilities, but how we grow
together. I will adapt my guidance to complement your choice."
"""
        return consultation

    def get_job_specific_advice(self, job_key: str, context: str) -> str:
        """Provide job-specific contextual advice"""
        guidance = JOB_GUIDANCE.get(job_key)
        guardian = GUARDIANS.get(self.base.guardian_type)

        if not guidance:
            return self.base.get_advice(context)

        advice_templates = {
            "exploration": f"For a {JOBS[job_key].name}, {random.choice(guidance.suggested_locations).value} holds special significance.",
            "combat": f"Remember your {JOBS[job_key].name} strategy: {guidance.battle_strategy}",
            "crafting": f"As a {JOBS[job_key].name}, consider crafting {random.choice(guidance.recommended_recipes)}.",
            "trading": f"Seek {random.choice(guidance.priority_items)} - they resonate with your {JOBS[job_key].name} nature.",
            "meditation": random.choice(guidance.companion_wisdom),
            "growth": guidance.growth_path
        }

        base_advice = advice_templates.get(context, random.choice(guidance.companion_wisdom))

        # Add guardian influence
        guardian_state = guardian.get_cycle_state(self.base.evolution_stage)
        return f"{base_advice}\n[Guardian {guardian.name} whispers: Currently in {guardian_state} phase]"

    def suggest_next_action(self, player_state: Dict[str, Any]) -> str:
        """Suggest next action based on job and current state"""
        job_key = player_state.get("job_key", "SEEKER")
        guidance = JOB_GUIDANCE.get(job_key)

        suggestions = []

        # Low on items? Suggest exploration
        if player_state.get("inventory_count", 0) < 3:
            location = random.choice(guidance.suggested_locations)
            suggestions.append(f"Visit {location.value} to find {random.choice(guidance.priority_items)}")

        # Have items? Suggest crafting
        if player_state.get("inventory_count", 0) >= 2:
            suggestions.append(f"Craft {random.choice(guidance.recommended_recipes)}")

        # Low coherence? Suggest meditation
        if player_state.get("coherence", 0) < 0.5:
            suggestions.append("Meditate to restore coherence and receive wisdom")

        # Ready for battle?
        if player_state.get("deck_ready", False):
            suggestions.append(f"Test your {guidance.battle_strategy} in battle")

        return random.choice(suggestions) if suggestions else "Explore and follow your path"

class BloomQuestEnhanced:
    """Enhanced game with deep job integration"""

    def __init__(self):
        # Initialize core systems
        self.economy = MythicEconomyGame()
        self.battle_system = CardBattleSystem()
        self.deck_builder = DeckBuilder()
        self.item_generator = ItemGenerator()

        # Enhanced game state
        self.state = GameState.GUARDIAN_SELECTION
        self.player = None
        self.enhanced_companion = None
        self.session_start = datetime.now()
        self.player_actions = []  # Track actions for tendency analysis

        # Battle management
        self.player_deck = None
        self.current_battle = None

        # Job training progress
        self.job_mastery = 0
        self.job_quests_completed = []

    def start(self):
        """Start the enhanced game experience"""
        print("\n" + "="*65)
        print("🌸 BLOOMQUEST ENHANCED: COMPANION-GUIDED JOURNEY 🌸")
        print("Your companion will guide you to your destined path")
        print("="*65)

        self._guardian_selection()
        self._job_consultation()

        # Main game loop
        self.running = True
        while self.running:
            try:
                if self.state == GameState.MAIN_MENU:
                    self._main_menu()
                elif self.state == GameState.EXPLORING:
                    self._explore()
                elif self.state == GameState.COMPANION_DIALOGUE:
                    self._companion_dialogue()
                elif self.state == GameState.CRAFTING:
                    self._crafting()
                elif self.state == GameState.BATTLE:
                    self._battle()
                elif self.state == GameState.SHOPPING:
                    self._shopping()
                elif self.state == GameState.MEDITATION:
                    self._meditation()
                elif self.state == GameState.JOB_TRAINING:
                    self._job_training()

            except KeyboardInterrupt:
                print("\n\n💫 Journey paused. Type 'quit' to end or press Enter to continue...")
                if input().lower() == 'quit':
                    self.running = False

        self._end_journey()

    def _guardian_selection(self):
        """Guardian selection phase"""
        print("\n" + "="*65)
        print("🌟 GUARDIAN SELECTION")
        print("="*65)

        name = input("\nSpeak your name into the void: ").strip() or "Wanderer"

        print(f"\nGreetings, {name}. The guardians are watching...")
        print("\nThree guardians step forward from the territories:\n")

        # Offer three random guardians
        available_guardians = random.sample(list(GUARDIANS.keys()), 3)

        for i, guardian_key in enumerate(available_guardians, 1):
            guardian = GUARDIANS[guardian_key]
            print(f"{i}. {guardian.name} {guardian.emoji} - {guardian.territory.value}")
            print(f"   '{guardian.wisdom}'")
            print()

        while True:
            try:
                choice = int(input("Which guardian calls to you? (1-3): "))
                if 1 <= choice <= 3:
                    chosen_guardian = available_guardians[choice - 1]
                    break
            except:
                pass
            print("Choose 1, 2, or 3")

        # Create temporary companion for consultation
        self.temp_name = name
        self.temp_guardian = chosen_guardian

        guardian = GUARDIANS[chosen_guardian]
        print(f"\n✨ {guardian.name} accepts your resonance.")
        print(f"A companion forms from {guardian.territory.value} energy...")

        companion_names = {
            Territory.GARDEN: ["Verdis", "Florin", "Sylva"],
            Territory.COSMIC: ["Stellis", "Solara", "Ignis"],
            Territory.ABYSSAL: ["Umbra", "Void-Echo", "Null-Whisper"]
        }

        companion_name = random.choice(companion_names[guardian.territory])
        print(f"\n🐾 {companion_name} manifests beside you.")
        print(f'"{guardian.wisdom}"')

        self.temp_companion_name = companion_name
        input("\nPress Enter to receive job consultation...")

    def _job_consultation(self):
        """Job consultation with companion guidance"""
        print("\n" + "="*65)
        print("📜 PATH CONSULTATION")
        print("="*65)

        # Create temporary enhanced companion for consultation
        from mythic_economy import CompanionSystem
        comp_system = CompanionSystem()

        # Use a temporary job for companion creation
        temp_job = JOBS["SEEKER"]
        base_companion = comp_system.create_companion(temp_job, self.temp_guardian)
        base_companion.name = self.temp_companion_name

        enhanced = EnhancedCompanion(base_companion)

        # Show consultation
        print(enhanced.provide_job_consultation())

        # Let player ask questions
        print("\n" + "-"*60)
        print("You may ask your companion about the paths:")
        print("1. Tell me more about the Seeker path")
        print("2. Tell me more about the Forger path")
        print("3. Tell me more about the Voidwalker path")
        print("4. Tell me more about the Gardener path")
        print("5. Tell me more about the Scribe path")
        print("6. Tell me more about the Herald path")
        print("7. I'm ready to choose my path")

        while True:
            choice = input("\nChoice (1-7): ").strip()

            if choice == "7":
                break

            job_details = {
                "1": ("SEEKER", "Seekers perceive patterns others miss. They excel at discovery and revelation."),
                "2": ("FORGER", "Forgers transform potential into power. They create legendary items."),
                "3": ("VOIDWALKER", "Voidwalkers master nullspace. They nullify and transcend."),
                "4": ("GARDENER", "Gardeners nurture growth across dimensions. They cultivate reality."),
                "5": ("SCRIBE", "Scribes write reality into existence. Their words become truth."),
                "6": ("HERALD", "Heralds tune reality's frequencies. They resonate with everything.")
            }

            if choice in job_details:
                job_key, description = job_details[choice]
                guidance = JOB_GUIDANCE[job_key]
                job = JOBS[job_key]

                print(f"\n🔍 {job.name}")
                print("-"*40)
                print(description)
                print(f"\nTerritory: {job.territory_affinity.value}")
                print(f"Primary Stat: {job.primary_stat}")
                print(f"Abilities: {', '.join(job.abilities)}")
                print(f"\nRecommended Locations: {', '.join([l.value for l in guidance.suggested_locations])}")
                print(f"Priority Items: {', '.join(guidance.priority_items)}")
                print(f"\n{self.temp_companion_name} says: '{random.choice(guidance.companion_wisdom)}'")

        # Final job selection
        print("\n" + "="*65)
        print("🎭 CHOOSE YOUR PATH")
        print("="*65)

        job_choices = [
            ("SEEKER", "Seeker of Echoes"),
            ("FORGER", "Pattern Forger"),
            ("VOIDWALKER", "Void Walker"),
            ("GARDENER", "Reality Gardener"),
            ("SCRIBE", "Covenant Scribe"),
            ("HERALD", "Frequency Herald")
        ]

        for i, (key, name) in enumerate(job_choices, 1):
            print(f"{i}. {name}")

        while True:
            try:
                choice = int(input("\nYour destiny (1-6): "))
                if 1 <= choice <= 6:
                    job_key = job_choices[choice - 1][0]
                    break
            except:
                pass
            print("Choose 1-6")

        # Create player with chosen job
        self.player = self.economy.create_character(self.temp_name, job_key, self.temp_guardian)
        self.enhanced_companion = EnhancedCompanion(self.player.companion)

        # Set starting location based on job
        guidance = JOB_GUIDANCE[job_key]
        self.player.current_location = guidance.suggested_locations[0]

        # Build initial deck
        self._build_job_deck()

        print(f"\n✨ You have become {self.player.name} the {self.player.job.name}!")
        print(f"💰 Starting BloomCoin: {self.player.bloomcoin_balance:.2f}")
        print(f"📍 Starting Location: {self.player.current_location.value}")
        print(f"\n{self.enhanced_companion.base.name} says: '{guidance.growth_path}'")

        input("\nPress Enter to begin your journey...")
        self.state = GameState.MAIN_MENU

    def _build_job_deck(self):
        """Build deck optimized for chosen job"""
        territory_suits = {
            Territory.GARDEN: [CardSuit.LEAVES, CardSuit.ROOTS, CardSuit.FLOWERS],
            Territory.COSMIC: [CardSuit.STARS, CardSuit.FLAMES, CardSuit.SUNS],
            Territory.ABYSSAL: [CardSuit.SHADOWS, CardSuit.MIRRORS, CardSuit.VOIDS]
        }

        preferred_territory = self.player.job.territory_affinity
        cards = []

        # 70% from preferred territory
        for suit in territory_suits[preferred_territory]:
            for rank in list(CardRank)[:7]:
                cards.append(Card(suit, rank))

        # 30% support cards
        other_territories = [t for t in Territory if t != preferred_territory]
        for territory in other_territories:
            suits = territory_suits[territory]
            for rank in list(CardRank)[:3]:
                cards.append(Card(suits[0], rank))

        self.player_deck = cards[:20]

    def _main_menu(self):
        """Enhanced main menu with companion suggestions"""
        print("\n" + "="*60)
        print(f"📍 {self.player.current_location.value}")
        print(f"🎭 {self.player.job.name}")
        print(f"💰 BloomCoin: {self.player.bloomcoin_balance:.2f}")
        print(f"🌟 Coherence: {self.player.coherence:.2%}")
        print(f"📚 Job Mastery: {self.job_mastery}%")
        print(f"🎒 Items: {len(self.player.inventory)}")
        print(f"🐾 {self.player.companion.name} (Stage {self.player.companion.evolution_stage})")
        print("="*60)

        # Companion suggestion
        player_state = {
            "job_key": [k for k, v in JOBS.items() if v == self.player.job][0],
            "inventory_count": len(self.player.inventory),
            "coherence": self.player.coherence,
            "deck_ready": len(self.player_deck) >= 20
        }

        suggestion = self.enhanced_companion.suggest_next_action(player_state)
        print(f"\n💭 {self.player.companion.name} suggests: {suggestion}")

        print("\n🧭 ACTIONS:")
        print("1. Explore (Job-optimized locations)")
        print("2. Companion Dialogue (Job guidance)")
        print("3. Craft Patterns (Job recipes)")
        print("4. Battle (Job strategies)")
        print("5. Shop (Job items)")
        print("6. Meditate (Job wisdom)")
        print("7. Job Training (Master your path)")
        print("8. Travel")
        print("9. Save & Exit")

        choice = input("\nChoice: ").strip()
        self.player_actions.append(f"menu_{choice}")

        if choice == "1":
            self.state = GameState.EXPLORING
        elif choice == "2":
            self.state = GameState.COMPANION_DIALOGUE
        elif choice == "3":
            self.state = GameState.CRAFTING
        elif choice == "4":
            self.state = GameState.BATTLE
        elif choice == "5":
            self.state = GameState.SHOPPING
        elif choice == "6":
            self.state = GameState.MEDITATION
        elif choice == "7":
            self.state = GameState.JOB_TRAINING
        elif choice == "8":
            self._travel()
        elif choice == "9":
            self.running = False

    def _explore(self):
        """Job-optimized exploration"""
        job_key = [k for k, v in JOBS.items() if v == self.player.job][0]
        guidance = JOB_GUIDANCE[job_key]

        print(f"\n🔍 EXPLORING: {self.player.current_location.value}")
        print("-"*50)

        # Job-specific exploration bonus
        in_preferred_location = self.player.current_location in guidance.suggested_locations

        if in_preferred_location:
            print(f"✨ Your {self.player.job.name} training enhances discovery here!")
            discovery_chance = 0.4 + (self.player.coherence * 0.3)
        else:
            discovery_chance = 0.25 + (self.player.coherence * 0.2)

        # Location-specific actions
        location_actions = {
            Location.CRYSTAL_CAVES: ["Resonate with crystals", "Mine deeper veins", "Listen to echoes"],
            Location.PHOENIX_NEST: ["Gather phoenix ash", "Study rebirth patterns", "Channel flames"],
            Location.VOID_MARKET: ["Browse null wares", "Trade shadows", "Investigate whispers"],
            Location.GARDEN_HEART: ["Tend sacred grove", "Harvest blooms", "Plant seeds"],
            Location.LIBRARY_INFINITE: ["Read forbidden texts", "Decode glyphs", "Access archives"]
        }

        actions = location_actions.get(self.player.current_location, ["Search", "Investigate", "Explore"])

        print("\n🎯 Actions:")
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
        print("4. Return")

        choice = input("\nChoice: ").strip()

        if choice in ["1", "2", "3"]:
            self.player_actions.append(f"explore_{actions[int(choice)-1]}")

            if random.random() < discovery_chance:
                # Generate job-appropriate item
                territory = Territory.GARDEN  # Default
                if self.player.current_location == Location.CRYSTAL_CAVES:
                    territory = Territory.COSMIC
                elif self.player.current_location == Location.VOID_MARKET:
                    territory = Territory.ABYSSAL

                item = self.item_generator.generate_item(
                    territory,
                    {"job": job_key},
                    self.player.luck_modifier
                )

                # Check if it's a priority item for this job
                is_priority = False
                for priority_type in guidance.priority_items:
                    if priority_type in item.item_type:
                        is_priority = True
                        item.base_value *= 1.5  # Bonus value for job items
                        break

                self.player.inventory.append(item)

                print(f"\n✨ DISCOVERY! {item.rarity.value[0]} {item.name}")
                if is_priority:
                    print(f"🎯 This {item.item_type} resonates with your {self.player.job.name} path!")

                print(f"💎 Value: {item.base_value:.1f}")

                # Job mastery increase
                self.job_mastery = min(100, self.job_mastery + 1)

            else:
                print("\nYou search carefully but find nothing...")
                advice = self.enhanced_companion.get_job_specific_advice(job_key, "exploration")
                print(f"\n{self.player.companion.name}: '{advice}'")

        input("\nPress Enter to continue...")
        self.state = GameState.MAIN_MENU

    def _companion_dialogue(self):
        """Enhanced companion dialogue with job guidance"""
        job_key = [k for k, v in JOBS.items() if v == self.player.job][0]
        guidance = JOB_GUIDANCE[job_key]

        print(f"\n🐾 {self.player.companion.name}")
        print(f"Evolution Stage: {self.player.companion.evolution_stage}")
        guardian = GUARDIANS.get(self.player.companion.guardian_type)
        print(f"Guardian: {guardian.name} {guardian.emoji}")
        print("-"*50)

        print("\n💭 DIALOGUE OPTIONS:")
        print("1. Ask about my job path")
        print("2. Request crafting guidance")
        print("3. Discuss battle strategies")
        print("4. Seek location advice")
        print("5. Feed pattern")
        print("6. Deep wisdom")
        print("7. Return")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            print(f"\n{self.player.companion.name} speaks about your path:")
            print(f"'{guidance.growth_path}'")
            print(f"\nYou've mastered {self.job_mastery}% of the {self.player.job.name} path.")
            if self.job_mastery < 25:
                print("You're just beginning to understand your potential.")
            elif self.job_mastery < 50:
                print("Your skills are developing nicely.")
            elif self.job_mastery < 75:
                print("You're becoming a true master of your craft.")
            else:
                print("You approach legendary mastery!")

        elif choice == "2":
            print(f"\n{self.player.companion.name} advises on crafting:")
            recipe_name = random.choice(guidance.recommended_recipes)
            recipe = next((r for r in RECIPES if r.name == recipe_name), None)
            if recipe:
                print(f"'Consider {recipe.name} - {recipe.description}'")
                print(f"Required: {', '.join(recipe.required_items)}")
            print(f"\nPriority items: {', '.join(guidance.priority_items)}")

        elif choice == "3":
            print(f"\n{self.player.companion.name} shares battle wisdom:")
            print(f"'{guidance.battle_strategy}'")
            print(f"\nYour {self.player.job.territory_affinity.value} cards will serve you well.")

        elif choice == "4":
            print(f"\n{self.player.companion.name} suggests locations:")
            for loc in guidance.suggested_locations:
                print(f"• {loc.value} - Strong resonance for {self.player.job.name}")

        elif choice == "5":
            if len(self.player.companion.fed_patterns) < 20:
                pattern = f"{self.player.job.name}_Pattern_{len(self.player.companion.fed_patterns)+1}"
                self.player.companion.fed_patterns.append(pattern)
                print(f"\n✨ Fed {pattern} to {self.player.companion.name}")

                if len(self.player.companion.fed_patterns) % 5 == 0:
                    self.player.companion.evolution_stage += 1
                    print(f"🎉 Evolution to stage {self.player.companion.evolution_stage}!")
                    print(f"'{random.choice(guidance.companion_wisdom)}'")

        elif choice == "6":
            wisdom = random.choice(guidance.companion_wisdom)
            print(f"\n{self.player.companion.name} shares deep wisdom:")
            print(f"'{wisdom}'")
            print(f"\n[Guardian {guardian.name}: {guardian.wisdom}]")

        input("\nPress Enter to continue...")
        self.state = GameState.MAIN_MENU

    def _job_training(self):
        """Special job training mode"""
        job_key = [k for k, v in JOBS.items() if v == self.player.job][0]
        guidance = JOB_GUIDANCE[job_key]

        print(f"\n🎓 {self.player.job.name} TRAINING")
        print("="*50)
        print(f"Current Mastery: {self.job_mastery}%")

        # Training options based on mastery level
        if self.job_mastery < 25:
            print("\n📖 NOVICE TRAINING")
            print("1. Study job fundamentals")
            print("2. Practice basic abilities")
            print("3. Learn priority items")
        elif self.job_mastery < 50:
            print("\n📘 ADEPT TRAINING")
            print("1. Advanced techniques")
            print("2. Recipe mastery")
            print("3. Territory attunement")
        elif self.job_mastery < 75:
            print("\n📙 EXPERT TRAINING")
            print("1. Master strategies")
            print("2. Guardian synchronization")
            print("3. Pattern weaving")
        else:
            print("\n📕 LEGENDARY TRAINING")
            print("1. Transcendent techniques")
            print("2. Reality manipulation")
            print("3. Ultimate mastery")

        print("4. Return")

        choice = input("\nChoice: ").strip()

        if choice in ["1", "2", "3"]:
            # Training costs bloomcoin but increases mastery
            cost = (self.job_mastery // 25 + 1) * PHI * 5

            if self.player.bloomcoin_balance >= cost:
                self.player.bloomcoin_balance -= cost
                mastery_gain = random.randint(3, 7)
                self.job_mastery = min(100, self.job_mastery + mastery_gain)

                print(f"\n💰 Spent {cost:.2f} BloomCoin on training")
                print(f"📈 Mastery increased by {mastery_gain}% to {self.job_mastery}%")

                # Learn something new
                lesson = random.choice(guidance.companion_wisdom)
                print(f"\n{self.player.companion.name}: '{lesson}'")

                # Unlock abilities at thresholds
                if self.job_mastery >= 25 and "novice" not in self.job_quests_completed:
                    self.job_quests_completed.append("novice")
                    print("\n🎉 Unlocked: Enhanced Discovery Rate!")
                    self.player.luck_modifier += 0.1

                if self.job_mastery >= 50 and "adept" not in self.job_quests_completed:
                    self.job_quests_completed.append("adept")
                    print("\n🎉 Unlocked: Advanced Crafting!")

                if self.job_mastery >= 75 and "expert" not in self.job_quests_completed:
                    self.job_quests_completed.append("expert")
                    print("\n🎉 Unlocked: Master Techniques!")
                    self.player.coherence = min(1.0, self.player.coherence + 0.1)

                if self.job_mastery >= 100:
                    print("\n🌟 LEGENDARY MASTERY ACHIEVED!")
                    print(f"You have become a legendary {self.player.job.name}!")
            else:
                print(f"\nNeed {cost:.2f} BloomCoin for this training")

        input("\nPress Enter to continue...")
        self.state = GameState.MAIN_MENU

    def _crafting(self):
        """Job-optimized crafting"""
        job_key = [k for k, v in JOBS.items() if v == self.player.job][0]
        guidance = JOB_GUIDANCE[job_key]

        print("\n🔨 PATTERN CRAFTING")
        print("-"*50)

        if len(self.player.inventory) < 2:
            print("Need at least 2 items to craft!")
            input("Press Enter...")
            self.state = GameState.MAIN_MENU
            return

        # Show recommended recipes for job
        print(f"Recommended for {self.player.job.name}:")
        for recipe_name in guidance.recommended_recipes[:3]:
            recipe = next((r for r in RECIPES if r.name == recipe_name), None)
            if recipe:
                print(f"• {recipe.name}: {recipe.description}")

        print("\n📦 Your items:")
        for i, item in enumerate(self.player.inventory[:10], 1):
            priority = "🎯" if any(p in item.item_type for p in guidance.priority_items) else ""
            print(f"{i}. {item.name} ({item.item_type}) {priority}")

        print("\n1. Craft recommended recipe")
        print("2. Experimental crafting")
        print("3. Cancel")

        choice = input("\nChoice: ").strip()

        if choice == "1" and len(self.player.inventory) >= 2:
            # Try to craft a recommended recipe
            success = False
            for recipe_name in guidance.recommended_recipes:
                recipe = next((r for r in RECIPES if r.name == recipe_name), None)
                if recipe:
                    # Check if player has required items
                    has_items = all(
                        any(req in item.item_type for item in self.player.inventory)
                        for req in recipe.required_items
                    )

                    if has_items:
                        # Remove items and create pattern
                        for _ in range(min(2, len(self.player.inventory))):
                            self.player.inventory.pop(0)

                        print(f"\n✨ Crafted {recipe.name}!")
                        print(f"Pattern: {recipe.pattern_output}")

                        # Feed to companion
                        self.player.companion.fed_patterns.append(recipe.pattern_output)
                        print(f"{self.player.companion.name} absorbed the pattern!")

                        # Job mastery increase
                        self.job_mastery = min(100, self.job_mastery + 2)
                        success = True
                        break

            if not success:
                print("\nMissing required items for recommended recipes")

        elif choice == "2" and len(self.player.inventory) >= 2:
            # Experimental crafting
            item1 = self.player.inventory.pop(0)
            item2 = self.player.inventory.pop(0)

            pattern_name = f"Experimental_{item1.item_type}_{item2.item_type}"
            print(f"\n🧪 Created {pattern_name}!")

            self.player.companion.fed_patterns.append(pattern_name)
            print(f"{self.player.companion.name} absorbed the experimental pattern!")

        input("\nPress Enter...")
        self.state = GameState.MAIN_MENU

    def _meditation(self):
        """Job-enhanced meditation"""
        job_key = [k for k, v in JOBS.items() if v == self.player.job][0]
        guidance = JOB_GUIDANCE[job_key]

        print("\n🧘 MEDITATION")
        print("-"*50)

        print(f"Aligning with {self.player.job.territory_affinity.value} frequencies...")

        # Job mastery bonus
        mastery_bonus = 1 + (self.job_mastery / 100)
        base_mine = PHI * mastery_bonus
        coherence_mult = 1 + self.player.coherence
        mined = base_mine * coherence_mult * random.uniform(0.8, 1.2)

        self.player.bloomcoin_balance += mined
        self.player.coherence = min(1.0, self.player.coherence + 0.025)

        print(f"\n✨ Mined {mined:.3f} BloomCoin")
        print(f"🌟 Coherence: {self.player.coherence:.2%}")

        # Job-specific wisdom during meditation
        wisdom = random.choice(guidance.companion_wisdom)
        print(f"\n{self.player.companion.name} shares wisdom:")
        print(f"'{wisdom}'")

        # Guardian wisdom
        guardian = GUARDIANS.get(self.player.companion.guardian_type)
        print(f"\nGuardian {guardian.name}: '{guardian.wisdom}'")

        input("\nPress Enter...")
        self.state = GameState.MAIN_MENU

    def _battle(self):
        """Simplified battle for demonstration"""
        print("\n⚔️ BATTLE")
        print("-"*50)

        job_key = [k for k, v in JOBS.items() if v == self.player.job][0]
        guidance = JOB_GUIDANCE[job_key]

        print(f"Battle Strategy: {guidance.battle_strategy}")
        print("\nBattle mechanics would go here...")

        # Simple victory
        reward = PHI * 10 * random.uniform(0.8, 1.2)
        self.player.bloomcoin_balance += reward

        print(f"\n🎉 Victory! Earned {reward:.2f} BloomCoin")

        input("\nPress Enter...")
        self.state = GameState.MAIN_MENU

    def _shopping(self):
        """Job-optimized shopping"""
        job_key = [k for k, v in JOBS.items() if v == self.player.job][0]
        guidance = JOB_GUIDANCE[job_key]

        print("\n🏪 RESONANCE MARKET")
        print(f"Your BloomCoin: {self.player.bloomcoin_balance:.2f}")
        print("-"*50)

        # Generate job-appropriate items
        shop_items = []
        for item_type in guidance.priority_items[:3]:
            price = PHI * random.randint(10, 30)
            shop_items.append((f"Quality {item_type}", price, f"Perfect for {self.player.job.name}"))

        shop_items.append(("Mystery Box", PHI * 25, "Contains random job items"))
        shop_items.append(("Training Manual", PHI * 15, "+5 Job Mastery"))

        for i, (name, price, desc) in enumerate(shop_items, 1):
            print(f"{i}. {name} - {price:.1f} BC")
            print(f"   {desc}")
        print("6. Leave")

        choice = input("\nChoice: ").strip()

        if choice in ["1", "2", "3", "4", "5"]:
            idx = int(choice) - 1
            if idx < len(shop_items):
                name, price, _ = shop_items[idx]

                if self.player.bloomcoin_balance >= price:
                    self.player.bloomcoin_balance -= price

                    if "Training Manual" in name:
                        self.job_mastery = min(100, self.job_mastery + 5)
                        print(f"\n📖 Job Mastery increased to {self.job_mastery}%!")
                    else:
                        print(f"\n✅ Purchased {name}!")
                        # Add to inventory
                        item = MythicalItem(
                            name=name,
                            description=f"Purchased from shop",
                            rarity=ItemRarity.RARE,
                            item_type=guidance.priority_items[0] if idx < 3 else "mystery",
                            base_value=price * 0.8,
                            properties={"source": "shop"},
                            guardian_affinity=None,
                            recipe_component=True
                        )
                        self.player.inventory.append(item)
                else:
                    print("Not enough BloomCoin!")

        if choice != "6":
            self._shopping()
        else:
            self.state = GameState.MAIN_MENU

    def _travel(self):
        """Travel between locations"""
        print("\n🗺️ TRAVEL")

        locations = list(Location)
        job_key = [k for k, v in JOBS.items() if v == self.player.job][0]
        guidance = JOB_GUIDANCE[job_key]

        for i, loc in enumerate(locations, 1):
            marker = "📍" if loc == self.player.current_location else ""
            recommended = "⭐" if loc in guidance.suggested_locations else ""
            print(f"{i}. {loc.value} {marker} {recommended}")

        print("\n⭐ = Recommended for your job")

        choice = input("\nDestination (number): ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(locations):
                new_loc = locations[idx]
                if new_loc != self.player.current_location:
                    cost = PHI * 3
                    if self.player.bloomcoin_balance >= cost:
                        self.player.bloomcoin_balance -= cost
                        self.player.current_location = new_loc
                        print(f"\n✈️ Traveled to {new_loc.value}")

                        if new_loc in guidance.suggested_locations:
                            print(f"✨ Strong resonance here for {self.player.job.name}!")
                    else:
                        print(f"Need {cost:.2f} BloomCoin to travel")
        except:
            pass

        input("\nPress Enter...")

    def _end_journey(self):
        """End game summary"""
        print("\n" + "="*65)
        print("🌅 JOURNEY'S END")
        print("="*65)

        if self.player:
            print(f"\n{self.player.name} the {self.player.job.name}")
            print(f"BloomCoin: {self.player.bloomcoin_balance:.2f}")
            print(f"Coherence: {self.player.coherence:.2%}")
            print(f"Job Mastery: {self.job_mastery}%")
            print(f"Items Collected: {len(self.player.inventory)}")
            print(f"Companion Evolution: Stage {self.player.companion.evolution_stage}")
            print(f"Patterns Fed: {len(self.player.companion.fed_patterns)}")

            # Final companion wisdom
            job_key = [k for k, v in JOBS.items() if v == self.player.job][0]
            guidance = JOB_GUIDANCE[job_key]
            wisdom = random.choice(guidance.companion_wisdom)
            print(f"\n{self.player.companion.name}'s parting wisdom:")
            print(f"'{wisdom}'")

        print("\n✨ May the golden ratio guide your path...")


def main():
    """Launch the enhanced game"""
    print("🌺 BloomQuest Enhanced Launcher")
    print("="*40)

    try:
        game = BloomQuestEnhanced()
        game.start()
    except KeyboardInterrupt:
        print("\n\n💫 Journey interrupted gracefully.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()