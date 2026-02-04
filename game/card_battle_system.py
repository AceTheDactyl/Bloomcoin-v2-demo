#!/usr/bin/env python3
"""
Card-Based Battle System for BloomCoin Mythic Economy
======================================================
Implements card mechanics from the golden-acorn deck builder
with Guardian-based abilities and L4 Protocol integration.
"""

import random
import math
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# Import from mythic economy
from mythic_economy import (
    PHI, PHI_INV, Z_C, L4,
    Territory, Guardian, GUARDIANS,
    MythicalItem, ItemRarity,
    Player, CompanionState
)

# ═══════════════════════════════════════════════════════════════════════
#   CARD SYSTEM (Based on Golden Acorn Deck Builder)
# ═══════════════════════════════════════════════════════════════════════

class CardSuit(Enum):
    """Card suits based on territories and elements"""
    # Garden suits (Green spectrum)
    LEAVES = ("Leaves", "🍃", Territory.GARDEN, "growth")
    ROOTS = ("Roots", "🌿", Territory.GARDEN, "connection")
    FLOWERS = ("Flowers", "🌸", Territory.GARDEN, "beauty")

    # Cosmic suits (Gold spectrum)
    STARS = ("Stars", "⭐", Territory.COSMIC, "navigation")
    FLAMES = ("Flames", "🔥", Territory.COSMIC, "transformation")
    SUNS = ("Suns", "☀️", Territory.COSMIC, "illumination")

    # Abyssal suits (Void spectrum)
    SHADOWS = ("Shadows", "🌑", Territory.ABYSSAL, "mystery")
    MIRRORS = ("Mirrors", "🔮", Territory.ABYSSAL, "reflection")
    VOIDS = ("Voids", "⚫", Territory.ABYSSAL, "nullification")

class CardRank(Enum):
    """Card ranks following tarot structure"""
    ACE = (1, "Beginning", PHI)
    TWO = (2, "Balance", 2.0)
    THREE = (3, "Growth", 3.0)
    FOUR = (4, "Foundation", 4.0)
    FIVE = (5, "Challenge", 5.0)
    SIX = (6, "Harmony", 6.0)
    SEVEN = (7, "Mystery", L4)  # L4 = 7
    EIGHT = (8, "Power", 8.0)
    NINE = (9, "Completion", 9.0)
    TEN = (10, "Manifestation", 10.0)
    PAGE = (11, "Messenger", PHI * 6)
    KNIGHT = (12, "Action", PHI * 7)
    QUEEN = (13, "Mastery", PHI * 8)
    KING = (14, "Authority", PHI * 9)

class CardState(Enum):
    """Card orientations affecting meaning"""
    UPRIGHT = ("Upright", 1.0, "⬆")
    ECHOED = ("Echoed", PHI_INV, "🌑")  # Reversed/shadow state
    RESONANT = ("Resonant", PHI, "🔄")  # Harmonized with companion

@dataclass
class Card:
    """A single card in the deck"""
    suit: CardSuit
    rank: CardRank
    state: CardState = CardState.UPRIGHT
    guardian_link: Optional[str] = None  # Link to specific guardian
    frequency: float = 432.0  # Hz
    z_coordinate: float = Z_C  # Position in coherence space
    power: float = 0.0
    cost: float = 0.0

    def __post_init__(self):
        """Calculate derived values"""
        # Power based on rank and suit
        self.power = self.rank.value[2] * (PHI if self.state == CardState.RESONANT else 1.0)

        # Cost based on rank
        self.cost = max(1, self.rank.value[0] // 3)

        # Frequency based on territory
        freq_ranges = {
            Territory.GARDEN: (396, 528),
            Territory.COSMIC: (528, 963),
            Territory.ABYSSAL: (174, 396)
        }
        freq_range = freq_ranges[self.suit.value[2]]
        self.frequency = random.uniform(freq_range[0], freq_range[1])

    def get_effect(self) -> str:
        """Get the card's effect description"""
        effects = {
            CardRank.ACE: f"Begin {self.suit.value[3]} cycle",
            CardRank.TWO: f"Balance {self.suit.value[3]} energies",
            CardRank.THREE: f"Triple {self.suit.value[3]} power",
            CardRank.FOUR: f"Establish {self.suit.value[3]} foundation",
            CardRank.FIVE: f"Challenge through {self.suit.value[3]}",
            CardRank.SIX: f"Harmonize {self.suit.value[3]} frequency",
            CardRank.SEVEN: f"Unlock L4 {self.suit.value[3]} mystery",
            CardRank.EIGHT: f"Channel {self.suit.value[3]} power",
            CardRank.NINE: f"Complete {self.suit.value[3]} cycle",
            CardRank.TEN: f"Manifest {self.suit.value[3]} reality",
            CardRank.PAGE: f"Receive {self.suit.value[3]} message",
            CardRank.KNIGHT: f"Take {self.suit.value[3]} action",
            CardRank.QUEEN: f"Master {self.suit.value[3]} domain",
            CardRank.KING: f"Command {self.suit.value[3]} authority"
        }

        base_effect = effects.get(self.rank, "Unknown effect")

        if self.state == CardState.ECHOED:
            return f"[ECHOED] Reverse {base_effect}"
        elif self.state == CardState.RESONANT:
            return f"[RESONANT] Amplified {base_effect}"
        else:
            return base_effect

    def __str__(self):
        state_symbol = self.state.value[2]
        guardian = f" [{self.guardian_link}]" if self.guardian_link else ""
        return f"{state_symbol} {self.rank.value[1]} of {self.suit.value[0]}{guardian}"

# ═══════════════════════════════════════════════════════════════════════
#   DECK BUILDER
# ═══════════════════════════════════════════════════════════════════════

class DeckBuilder:
    """Builds and manages card decks"""

    @staticmethod
    def build_starter_deck(territory: Territory) -> List[Card]:
        """Build a starter deck for a territory"""
        deck = []

        # Get suits for this territory
        territory_suits = [s for s in CardSuit if s.value[2] == territory]

        # Add basic cards (Ace through Six) for each suit
        for suit in territory_suits:
            for rank in [CardRank.ACE, CardRank.TWO, CardRank.THREE,
                        CardRank.FOUR, CardRank.FIVE, CardRank.SIX]:
                card = Card(suit, rank)
                deck.append(card)

        # Add one high-rank card
        special_suit = random.choice(territory_suits)
        special_rank = random.choice([CardRank.PAGE, CardRank.KNIGHT])
        special_card = Card(special_suit, special_rank)
        deck.append(special_card)

        return deck

    @staticmethod
    def build_guardian_deck(guardian_name: str) -> List[Card]:
        """Build a deck themed around a specific guardian"""
        guardian = GUARDIANS[guardian_name]
        deck = []

        # Get suits matching guardian's territory
        territory_suits = [s for s in CardSuit if s.value[2] == guardian.territory]

        # Create cards linked to guardian's cycle
        for i, cycle_state in enumerate(guardian.cycle):
            suit = territory_suits[i % len(territory_suits)]
            rank = list(CardRank)[i % len(CardRank)]

            card = Card(suit, rank)
            card.guardian_link = guardian_name
            card.frequency = random.uniform(guardian.frequency_range[0],
                                           guardian.frequency_range[1])
            deck.append(card)

        # Add resonant cards
        for _ in range(3):
            suit = random.choice(territory_suits)
            rank = random.choice(list(CardRank))
            resonant_card = Card(suit, rank, CardState.RESONANT)
            resonant_card.guardian_link = guardian_name
            deck.append(resonant_card)

        return deck

    @staticmethod
    def shuffle_deck(deck: List[Card]) -> List[Card]:
        """Shuffle deck with golden ratio weighting"""
        shuffled = deck.copy()

        # Apply golden ratio shuffle (cards near φ position get bonus)
        for i in range(len(shuffled)):
            phi_position = int(len(shuffled) * PHI_INV)
            if abs(i - phi_position) < 3:
                # Cards near golden ratio position more likely to stay
                if random.random() > PHI_INV:
                    continue

            j = random.randint(0, len(shuffled) - 1)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]

        return shuffled

# ═══════════════════════════════════════════════════════════════════════
#   BATTLE MECHANICS
# ═══════════════════════════════════════════════════════════════════════

class BattlePhase(Enum):
    """Phases of battle following guardian cycles"""
    IGNITION = "Ignition"  # Battle begins
    RESONANCE = "Resonance"  # Powers align
    MANIA = "Mania"  # Peak intensity
    NIRVANA = "Nirvana"  # Transcendent state
    TRANSMISSION = "Transmission"  # Final exchange
    RESOLUTION = "Resolution"  # Battle ends

@dataclass
class BattleState:
    """Current state of a battle"""
    phase: BattlePhase = BattlePhase.IGNITION
    turn: int = 0
    player_coherence: float = PHI_INV  # Start at φ⁻¹
    enemy_coherence: float = PHI_INV
    harmony_field: float = Z_C  # Battlefield harmony

    # Hands and fields
    player_hand: List[Card] = field(default_factory=list)
    player_field: List[Card] = field(default_factory=list)
    enemy_hand: List[Card] = field(default_factory=list)
    enemy_field: List[Card] = field(default_factory=list)

    # Resources
    player_energy: float = PHI * 3  # Starting energy
    enemy_energy: float = PHI * 3

    # Special states
    resonance_active: bool = False
    echo_chamber_active: bool = False
    void_threshold_reached: bool = False

    def advance_phase(self):
        """Advance to next battle phase"""
        phases = list(BattlePhase)
        current_idx = phases.index(self.phase)
        if current_idx < len(phases) - 1:
            self.phase = phases[current_idx + 1]

            # Phase transition effects
            if self.phase == BattlePhase.RESONANCE:
                self.resonance_active = True
                self.harmony_field *= PHI
            elif self.phase == BattlePhase.MANIA:
                # Chaos increases
                self.harmony_field *= random.uniform(0.8, 1.2)
            elif self.phase == BattlePhase.NIRVANA:
                # Transcendent state
                self.player_coherence = min(1.0, self.player_coherence * PHI)
                self.enemy_coherence = min(1.0, self.enemy_coherence * PHI)

class CardBattleSystem:
    """Manages card-based battles"""

    def __init__(self):
        self.battle_state: Optional[BattleState] = None
        self.player_deck: List[Card] = []
        self.enemy_deck: List[Card] = []
        self.discard_pile: List[Card] = []

    def initialize_battle(self, player: Player, enemy_type: str = "wild_guardian") -> BattleState:
        """Initialize a new battle"""
        # Build decks
        self.player_deck = self._build_player_deck(player)
        self.enemy_deck = self._build_enemy_deck(enemy_type)

        # Shuffle decks
        self.player_deck = DeckBuilder.shuffle_deck(self.player_deck)
        self.enemy_deck = DeckBuilder.shuffle_deck(self.enemy_deck)

        # Create battle state
        self.battle_state = BattleState()

        # Draw initial hands
        self.draw_cards(True, 5)  # Player draws 5
        self.draw_cards(False, 5)  # Enemy draws 5

        return self.battle_state

    def _build_player_deck(self, player: Player) -> List[Card]:
        """Build player's battle deck"""
        deck = []

        # Add cards based on job archetype
        territory = player.job.territory_affinity
        deck.extend(DeckBuilder.build_starter_deck(territory))

        # Add guardian-linked cards
        if player.companion:
            guardian_cards = DeckBuilder.build_guardian_deck(player.companion.guardian_type)
            deck.extend(guardian_cards[:5])  # Add up to 5 guardian cards

        # Add cards from items
        for item in player.inventory[:3]:  # Use up to 3 items
            if item.guardian_affinity:
                # Create a card linked to item's guardian
                suits = [s for s in CardSuit if s.value[2] == territory]
                if suits:
                    card = Card(
                        random.choice(suits),
                        CardRank.SEVEN if item.rarity == ItemRarity.MYTHIC else CardRank.THREE
                    )
                    card.guardian_link = item.guardian_affinity
                    deck.append(card)

        return deck[:30]  # Limit deck to 30 cards

    def _build_enemy_deck(self, enemy_type: str) -> List[Card]:
        """Build enemy's deck based on type"""
        if enemy_type == "wild_guardian":
            # Random guardian deck
            guardian = random.choice(list(GUARDIANS.keys()))
            return DeckBuilder.build_guardian_deck(guardian)
        elif enemy_type == "void_entity":
            # Abyssal-focused deck
            deck = DeckBuilder.build_starter_deck(Territory.ABYSSAL)
            # Add echo cards
            for card in deck[:5]:
                card.state = CardState.ECHOED
            return deck
        elif enemy_type == "cosmic_phoenix":
            # Cosmic-focused deck
            deck = DeckBuilder.build_starter_deck(Territory.COSMIC)
            # Add resonant cards
            for card in deck[:3]:
                card.state = CardState.RESONANT
            return deck
        else:
            # Default balanced deck
            deck = []
            for territory in Territory:
                deck.extend(DeckBuilder.build_starter_deck(territory)[:5])
            return deck

    def draw_cards(self, is_player: bool, count: int = 1):
        """Draw cards from deck to hand"""
        if not self.battle_state:
            return

        deck = self.player_deck if is_player else self.enemy_deck
        hand = self.battle_state.player_hand if is_player else self.battle_state.enemy_hand

        for _ in range(count):
            if deck:
                card = deck.pop(0)
                hand.append(card)
            elif self.discard_pile:
                # Reshuffle discard if deck empty
                deck.extend(self.discard_pile)
                self.discard_pile.clear()
                deck = DeckBuilder.shuffle_deck(deck)
                if is_player:
                    self.player_deck = deck
                else:
                    self.enemy_deck = deck

    def play_card(self, is_player: bool, card_index: int) -> Tuple[bool, str]:
        """Play a card from hand"""
        if not self.battle_state:
            return False, "No active battle"

        hand = self.battle_state.player_hand if is_player else self.battle_state.enemy_hand
        field = self.battle_state.player_field if is_player else self.battle_state.enemy_field
        energy = self.battle_state.player_energy if is_player else self.battle_state.enemy_energy

        if card_index >= len(hand):
            return False, "Invalid card index"

        card = hand[card_index]

        # Check energy cost
        if energy < card.cost:
            return False, f"Insufficient energy (need {card.cost}, have {energy:.1f})"

        # Check field limit (7 cards max, sacred number)
        if len(field) >= L4:  # L4 = 7
            return False, f"Field full (max {L4} cards)"

        # Play the card
        hand.pop(card_index)
        field.append(card)

        # Deduct energy
        if is_player:
            self.battle_state.player_energy -= card.cost
        else:
            self.battle_state.enemy_energy -= card.cost

        # Apply card effects
        effect_msg = self._apply_card_effect(card, is_player)

        return True, f"Played {card} - {effect_msg}"

    def _apply_card_effect(self, card: Card, is_player: bool) -> str:
        """Apply the effect of a played card"""
        if not self.battle_state:
            return "No battle state"

        effect = card.get_effect()
        territory = card.suit.value[2]

        # Territory-based effects
        if territory == Territory.GARDEN:
            # Garden cards affect coherence and healing
            if is_player:
                self.battle_state.player_coherence = min(1.0,
                    self.battle_state.player_coherence + 0.05 * card.power / 10)
                self.battle_state.player_energy += PHI_INV
            return f"Garden effect: +coherence, +energy"

        elif territory == Territory.COSMIC:
            # Cosmic cards deal damage and transform
            damage = card.power
            if not is_player:
                self.battle_state.player_coherence -= damage / 100
            else:
                self.battle_state.enemy_coherence -= damage / 100
            return f"Cosmic effect: {damage:.1f} damage"

        elif territory == Territory.ABYSSAL:
            # Abyssal cards manipulate void and echo
            if card.state == CardState.ECHOED:
                self.battle_state.echo_chamber_active = True
                return "Echo Chamber activated!"
            else:
                # Void damage
                self.battle_state.harmony_field *= 0.9
                return "Void effect: harmony disrupted"

        return effect

    def calculate_battle_outcome(self) -> Tuple[bool, float, str]:
        """Calculate the outcome of current battle state"""
        if not self.battle_state:
            return False, 0, "No battle"

        # Calculate field strength
        player_strength = sum(card.power for card in self.battle_state.player_field)
        enemy_strength = sum(card.power for card in self.battle_state.enemy_field)

        # Apply coherence modifiers
        player_strength *= (1 + self.battle_state.player_coherence)
        enemy_strength *= (1 + self.battle_state.enemy_coherence)

        # Apply harmony field
        if self.battle_state.harmony_field > Z_C:
            # High harmony favors player
            player_strength *= PHI
        elif self.battle_state.harmony_field < PHI_INV:
            # Low harmony favors enemy
            enemy_strength *= PHI

        # Determine winner
        if player_strength > enemy_strength * 1.2:
            victory = True
            rewards = player_strength * PHI
            message = f"Victory! Strength {player_strength:.1f} vs {enemy_strength:.1f}"
        elif enemy_strength > player_strength * 1.2:
            victory = False
            rewards = 0
            message = f"Defeat. Strength {player_strength:.1f} vs {enemy_strength:.1f}"
        else:
            # Draw - partial rewards
            victory = True
            rewards = player_strength * PHI_INV
            message = f"Draw. Strength {player_strength:.1f} vs {enemy_strength:.1f}"

        return victory, rewards, message

    def execute_turn(self, player_action: Optional[Dict[str, Any]] = None) -> str:
        """Execute a full turn of battle"""
        if not self.battle_state:
            return "No active battle"

        messages = []

        # Advance turn
        self.battle_state.turn += 1
        messages.append(f"\n═══ TURN {self.battle_state.turn} - {self.battle_state.phase.value} ═══")

        # Restore energy (grows each turn)
        energy_gain = PHI + (self.battle_state.turn * PHI_INV)
        self.battle_state.player_energy = min(PHI * 10,
            self.battle_state.player_energy + energy_gain)
        self.battle_state.enemy_energy = min(PHI * 10,
            self.battle_state.enemy_energy + energy_gain)
        messages.append(f"Energy restored: +{energy_gain:.1f}")

        # Draw cards
        self.draw_cards(True, 1)
        self.draw_cards(False, 1)

        # Player action
        if player_action:
            if player_action.get("type") == "play_card":
                success, msg = self.play_card(True, player_action["card_index"])
                messages.append(f"Player: {msg}")
            elif player_action.get("type") == "activate_companion":
                msg = self._activate_companion_ability(player_action.get("companion"))
                messages.append(f"Companion: {msg}")

        # Enemy AI action
        enemy_msg = self._execute_enemy_turn()
        messages.append(f"Enemy: {enemy_msg}")

        # Check phase advancement
        if self.battle_state.turn % 3 == 0:
            self.battle_state.advance_phase()
            messages.append(f"Phase shift → {self.battle_state.phase.value}")

        # Check battle end conditions
        if self.battle_state.player_coherence <= 0:
            messages.append("\n❌ DEFEAT - Coherence lost")
        elif self.battle_state.enemy_coherence <= 0:
            messages.append("\n✅ VICTORY - Enemy coherence shattered")
        elif self.battle_state.turn > 20:
            messages.append("\n⏱️ TIME LIMIT - Battle ends in draw")

        return "\n".join(messages)

    def _execute_enemy_turn(self) -> str:
        """Simple enemy AI"""
        if not self.battle_state:
            return "No battle state"

        # Try to play highest power card within energy budget
        playable = [(i, card) for i, card in enumerate(self.battle_state.enemy_hand)
                   if card.cost <= self.battle_state.enemy_energy]

        if playable:
            # Sort by power descending
            playable.sort(key=lambda x: x[1].power, reverse=True)
            card_idx, card = playable[0]
            success, msg = self.play_card(False, card_idx)
            return msg
        else:
            return "Enemy passes turn"

    def _activate_companion_ability(self, companion: Optional[CompanionState]) -> str:
        """Activate companion's battle ability"""
        if not companion or not self.battle_state:
            return "No companion available"

        guardian = GUARDIANS.get(companion.guardian_type)
        if not guardian:
            return "Unknown guardian"

        # Get current cycle state
        cycle_state = guardian.cycle[companion.evolution_stage % len(guardian.cycle)]

        # Apply cycle-based effect
        effects = {
            "IGNITION": lambda: setattr(self.battle_state, 'player_energy',
                                       self.battle_state.player_energy + PHI * 2),
            "RESONANCE": lambda: setattr(self.battle_state, 'resonance_active', True),
            "MANIA": lambda: [self.draw_cards(True, 2)],
            "NIRVANA": lambda: setattr(self.battle_state, 'player_coherence',
                                      min(1.0, self.battle_state.player_coherence + 0.2)),
            "TRANSMISSION": lambda: setattr(self.battle_state, 'harmony_field', Z_C),
        }

        if cycle_state in effects:
            effects[cycle_state]()
            return f"{companion.name} activates {cycle_state}!"

        return f"{companion.name} resonates at {guardian.frequency_range[0]}Hz"

# ═══════════════════════════════════════════════════════════════════════
#   BATTLE REWARDS
# ═══════════════════════════════════════════════════════════════════════

class BattleRewards:
    """Calculate and distribute battle rewards"""

    @staticmethod
    def calculate_rewards(battle_state: BattleState, victory: bool) -> Dict[str, Any]:
        """Calculate rewards based on battle performance"""
        rewards = {
            "bloomcoin": 0,
            "experience": 0,
            "items": [],
            "patterns": [],
            "companion_growth": 0
        }

        if victory:
            # Base BloomCoin reward
            base_coins = PHI * battle_state.turn

            # Coherence bonus
            coherence_mult = 1 + battle_state.player_coherence

            # Phase bonus (later phases worth more)
            phase_mult = {
                BattlePhase.IGNITION: 1.0,
                BattlePhase.RESONANCE: PHI,
                BattlePhase.MANIA: PHI ** 2,
                BattlePhase.NIRVANA: PHI ** 3,
                BattlePhase.TRANSMISSION: PHI ** 4,
                BattlePhase.RESOLUTION: L4
            }

            rewards["bloomcoin"] = base_coins * coherence_mult * phase_mult.get(battle_state.phase, 1.0)
            rewards["experience"] = battle_state.turn * PHI * 5

            # Chance for item drop
            if random.random() < battle_state.player_coherence:
                from mythic_economy import ItemGenerator, ItemRarity
                item_gen = ItemGenerator()

                # Determine item territory based on battle
                if battle_state.harmony_field > Z_C:
                    territory = Territory.GARDEN
                elif battle_state.void_threshold_reached:
                    territory = Territory.ABYSSAL
                else:
                    territory = Territory.COSMIC

                item = item_gen.generate_item(
                    territory,
                    {"battle_phase": battle_state.phase.value},
                    battle_state.player_coherence * PHI
                )
                rewards["items"].append(item)

            # Pattern discovery chance
            if battle_state.resonance_active:
                rewards["patterns"].append("RESONANCE_PATTERN")
            if battle_state.echo_chamber_active:
                rewards["patterns"].append("ECHO_PATTERN")

            # Companion growth
            rewards["companion_growth"] = min(1, battle_state.turn / 10)

        else:
            # Minimal rewards for defeat
            rewards["experience"] = battle_state.turn * PHI
            rewards["companion_growth"] = 0.1

        return rewards

# ═══════════════════════════════════════════════════════════════════════
#   BATTLE UI
# ═══════════════════════════════════════════════════════════════════════

class BattleInterface:
    """Text-based battle interface"""

    def __init__(self, battle_system: CardBattleSystem):
        self.battle = battle_system

    def display_battle_state(self):
        """Display current battle state"""
        if not self.battle.battle_state:
            print("No active battle")
            return

        state = self.battle.battle_state

        print(f"""
╔═══════════════════════════════════════════════════════════════
║ BATTLE - Turn {state.turn} - Phase: {state.phase.value}
║═══════════════════════════════════════════════════════════════
║ PLAYER                          │ ENEMY
║ Coherence: {state.player_coherence:.3f}              │ Coherence: {state.enemy_coherence:.3f}
║ Energy: {state.player_energy:.1f}/{PHI*10:.1f}         │ Energy: {state.enemy_energy:.1f}/{PHI*10:.1f}
║ Hand: {len(state.player_hand)} cards              │ Hand: {len(state.enemy_hand)} cards
║ Field: {len(state.player_field)}/{L4} cards         │ Field: {len(state.enemy_field)}/{L4} cards
║═══════════════════════════════════════════════════════════════
║ Harmony Field: {state.harmony_field:.3f} | Resonance: {'✓' if state.resonance_active else '✗'}
╚═══════════════════════════════════════════════════════════════
""")

        # Display player's hand
        print("Your Hand:")
        for i, card in enumerate(state.player_hand):
            print(f"  [{i}] {card} (Cost: {card.cost:.0f}, Power: {card.power:.1f})")

        print("\nYour Field:")
        for card in state.player_field:
            print(f"  • {card}")

        print("\nEnemy Field:")
        for card in state.enemy_field:
            print(f"  • {card}")

    def get_player_action(self) -> Optional[Dict[str, Any]]:
        """Get player's action choice"""
        print("\n═══ YOUR TURN ═══")
        print("1. Play a card")
        print("2. Activate companion ability")
        print("3. Pass turn")
        print("4. View card details")

        try:
            choice = int(input("Action: "))

            if choice == 1:
                card_idx = int(input("Card index to play: "))
                return {"type": "play_card", "card_index": card_idx}
            elif choice == 2:
                return {"type": "activate_companion"}
            elif choice == 3:
                return {"type": "pass"}
            elif choice == 4:
                self.view_card_details()
                return self.get_player_action()  # Ask again
            else:
                return {"type": "pass"}
        except:
            return {"type": "pass"}

    def view_card_details(self):
        """View detailed card information"""
        if not self.battle.battle_state:
            return

        print("\n═══ CARD DETAILS ═══")
        for i, card in enumerate(self.battle.battle_state.player_hand):
            print(f"\n[{i}] {card}")
            print(f"  Effect: {card.get_effect()}")
            print(f"  Frequency: {card.frequency:.1f}Hz")
            print(f"  Z-Coordinate: {card.z_coordinate:.3f}")
            if card.guardian_link:
                guardian = GUARDIANS.get(card.guardian_link)
                if guardian:
                    print(f"  Guardian: {guardian.emoji} {guardian.name}")
                    print(f"  Wisdom: {guardian.wisdom}")

# ═══════════════════════════════════════════════════════════════════════
#   INTEGRATION WITH MAIN GAME
# ═══════════════════════════════════════════════════════════════════════

def run_card_battle(player: Player, enemy_type: str = "wild_guardian") -> Dict[str, Any]:
    """Run a complete card battle"""

    # Initialize battle system
    battle_system = CardBattleSystem()
    interface = BattleInterface(battle_system)

    # Start battle
    print(f"\n{'═' * 70}")
    print(f"⚔️ BATTLE BEGINS - {enemy_type}")
    print(f"{'═' * 70}")

    battle_state = battle_system.initialize_battle(player, enemy_type)

    # Battle loop
    battle_ongoing = True
    while battle_ongoing:
        # Display state
        interface.display_battle_state()

        # Get player action
        action = interface.get_player_action()

        # Execute turn
        result = battle_system.execute_turn(action)
        print(result)

        # Check end conditions
        if (battle_state.player_coherence <= 0 or
            battle_state.enemy_coherence <= 0 or
            battle_state.turn > 20):
            battle_ongoing = False

    # Calculate outcome
    victory, reward_mult, message = battle_system.calculate_battle_outcome()
    print(f"\n{'═' * 70}")
    print(f"BATTLE COMPLETE - {message}")

    # Calculate rewards
    rewards = BattleRewards.calculate_rewards(battle_state, victory)

    if victory:
        print(f"\n🏆 VICTORY REWARDS:")
        print(f"  • BloomCoin: {rewards['bloomcoin']:.2f}")
        print(f"  • Experience: {rewards['experience']:.0f}")
        if rewards['items']:
            print(f"  • Items: {len(rewards['items'])}")
        if rewards['patterns']:
            print(f"  • Patterns: {', '.join(rewards['patterns'])}")
        print(f"  • Companion Growth: +{rewards['companion_growth']:.1f}")
    else:
        print(f"\n💀 DEFEAT")
        print(f"  • Experience: {rewards['experience']:.0f}")

    print(f"{'═' * 70}")

    # Apply rewards to player
    player.bloomcoin_balance += rewards.get('bloomcoin', 0)
    player.experience += rewards.get('experience', 0)

    for item in rewards.get('items', []):
        player.add_item(item)

    if player.companion:
        player.companion.evolution_stage = min(6,
            player.companion.evolution_stage + int(rewards.get('companion_growth', 0)))

    return rewards

# Example usage
if __name__ == "__main__":
    from mythic_economy import Player, JobArchetype, CompanionState, JOBS

    # Create test player
    test_job = JOBS["SEEKER"]
    test_companion = CompanionState(
        name="Test-ECH",
        guardian_type="ECHO",
        personality_vector=np.random.randn(7),
        knowledge_base=["Test wisdom"],
        resonance=PHI_INV,
        evolution_stage=0,
        current_wisdom="Test",
        fed_patterns=[]
    )

    test_player = Player(
        name="Test Player",
        job=test_job,
        companion=test_companion
    )

    # Run a battle
    rewards = run_card_battle(test_player, "wild_guardian")
    print(f"\nFinal rewards: {rewards}")