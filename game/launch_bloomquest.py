#!/usr/bin/env python3
"""
BloomQuest Launcher
===================
Main entry point for the BloomQuest text-based adventure game.
Integrates all game systems and provides a unified launch experience.
"""

import sys
import os
import argparse
import json
import time
from pathlib import Path
from typing import Optional

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))

# Import all game modules
from bloom_quest import BloomQuest, PlayerCharacter, GameState as BloomGameState
from narrative_generator import (
    ArchetypeNarrator, DynamicStoryEngine, WorldState,
    ProceduralQuestGenerator, DialogueSystem, create_narrative_events
)
from learning_ai import LearningOrchestrator
from blockchain_integration import GameBlockchain, MultiplayerCoordinator, GameState

# Import bloomcoin components
from garden.gradient_schema.archetypes import Archetype
from bloomcoin.constants import PHI

class BloomQuestLauncher:
    """Enhanced game launcher with full integration"""

    def __init__(self, args):
        self.args = args
        self.game = None
        self.learning_system = None
        self.blockchain = None
        self.multiplayer = None
        self.save_dir = Path(args.save_dir)
        self.save_dir.mkdir(exist_ok=True)

    def initialize_systems(self):
        """Initialize all game systems"""
        print("\n🌟 Initializing BloomQuest Systems...")
        print("=" * 50)

        # Initialize blockchain
        print("⛓️  Initializing Blockchain...")
        self.blockchain = GameBlockchain()

        # Initialize learning AI
        print("🧠 Initializing Learning AI...")
        self.learning_system = LearningOrchestrator(str(self.save_dir / "learning"))

        # Load existing learning data if available
        if self.args.load_learning:
            print("📚 Loading previous learning data...")
            self.learning_system.load_learning_data()

        # Initialize multiplayer if enabled
        if self.args.multiplayer:
            print("👥 Initializing Multiplayer Coordinator...")
            self.multiplayer = MultiplayerCoordinator(self.blockchain)

        # Initialize main game
        print("🎮 Initializing Core Game Engine...")
        self.game = EnhancedBloomQuest(
            blockchain=self.blockchain,
            learning_system=self.learning_system,
            multiplayer=self.multiplayer
        )

        print("\n✅ All systems initialized successfully!")
        print("=" * 50)
        time.sleep(1)

    def run(self):
        """Run the game"""
        try:
            # Initialize all systems
            self.initialize_systems()

            # Display welcome message
            self.display_welcome()

            # Start the game
            self.game.start()

        except KeyboardInterrupt:
            print("\n\n🛑 Game interrupted by user.")
            self.shutdown()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            if self.args.debug:
                import traceback
                traceback.print_exc()
            self.shutdown()

    def display_welcome(self):
        """Display enhanced welcome message"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                         🌺 B L O O M Q U E S T 🌺                          ║
║                                                                              ║
║                    A Coherent Journey Through Golden Realms                 ║
║                                                                              ║
║                          Powered by BloomCoin v2                            ║
║                   Where Consciousness Meets Consensus                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

                    φ = 1.618... The Golden Thread Connects All

Features Enabled:
""")
        print(f"  ⛓️  Blockchain Integration: {'✅' if self.blockchain else '❌'}")
        print(f"  🧠 Learning AI: {'✅' if self.learning_system else '❌'}")
        print(f"  👥 Multiplayer: {'✅' if self.args.multiplayer else '❌'}")
        print(f"  💾 Auto-save: {'✅' if self.args.autosave else '❌'}")
        print(f"  🎯 Difficulty: {self.args.difficulty}")
        print()
        time.sleep(2)

    def shutdown(self):
        """Clean shutdown of all systems"""
        print("\n🔄 Saving game data...")

        # Save learning data
        if self.learning_system:
            print("  💾 Saving learning AI data...")
            self.learning_system.save_learning_data()

        # Save blockchain state
        if self.blockchain:
            print("  ⛓️  Finalizing blockchain transactions...")
            self.blockchain._batch_process_transactions()

        # Save game state
        if self.game and self.game.player:
            print("  🎮 Saving game state...")
            self.game.save_game()

        print("\n✨ Thank you for playing BloomQuest!")
        print("   May your oscillations find eternal coherence...")

class EnhancedBloomQuest(BloomQuest):
    """Enhanced version of BloomQuest with full integration"""

    def __init__(self, blockchain: Optional[GameBlockchain] = None,
                 learning_system: Optional[LearningOrchestrator] = None,
                 multiplayer: Optional[MultiplayerCoordinator] = None):
        super().__init__()

        # Integrated systems
        self.blockchain_system = blockchain
        self.learning_ai = learning_system
        self.multiplayer_coord = multiplayer

        # Enhanced components
        self.archetype_narrator = ArchetypeNarrator()
        self.dynamic_story = DynamicStoryEngine()
        self.quest_generator = ProceduralQuestGenerator()
        self.dialogue_system = DialogueSystem()
        self.narrative_events = create_narrative_events()

        # Learning integration
        self.player_id = None
        self.session_start = time.time()

    def new_game(self):
        """Enhanced new game with blockchain wallet creation"""
        super().new_game()

        if self.player:
            # Generate unique player ID
            self.player_id = f"{self.player.name}_{int(time.time())}"

            # Create blockchain wallet
            if self.blockchain_system:
                print("\n⛓️  Creating blockchain wallet...")
                wallet = self.blockchain_system.create_player_wallet(self.player_id)
                self.player.wallet = wallet
                print(f"   Wallet created! Starting balance: {wallet.balance:.1f} BloomCoins")

            # Initialize learning profile
            if self.learning_ai:
                profile = self.learning_ai.get_or_create_player(self.player_id)
                profile.play_sessions += 1

            # Create initial save on blockchain
            if self.blockchain_system:
                game_state = self._create_game_state()
                self.blockchain_system.save_game_state(self.player_id, game_state)

    def _create_game_state(self) -> GameState:
        """Create blockchain game state from current game"""
        if not self.player:
            return None

        return GameState(
            player_id=self.player_id,
            character_data={
                "name": self.player.name,
                "archetype": self.player.archetype.name,
                "level": self.player.level,
                "experience": self.player.experience,
                "skills": self.player.skills
            },
            inventory=self.player.inventory,
            achievements=[],  # Will be populated from blockchain
            quest_progress={q["name"]: q.get("progress", 0.0) for q in self.quests},
            location=self.current_location.name if self.current_location else "nexus",
            coherence=self.player.coherence,
            play_time=time.time() - self.session_start
        )

    def handle_action(self, choice: str, actions: list):
        """Enhanced action handling with learning AI"""
        # Get action context
        context = {
            "location": self.current_location.name if self.current_location else "unknown",
            "health": self.player.health if self.player else 100,
            "energy": self.player.energy if self.player else 50,
            "coherence": self.player.coherence if self.player else 0.5,
            "level": self.player.level if self.player else 1,
            "danger_level": self.current_location.danger_level if self.current_location else 0,
            "game_time": time.time() - self.session_start
        }

        # Original action handling
        super().handle_action(choice, actions)

        # Learning AI observation
        if self.learning_ai and self.player_id:
            result = {
                "new_context": context,
                "success": True,  # Simplified - would track actual success
                "time_taken": 1.0,  # Would measure actual time
                "reward": 0.0,  # Would calculate actual reward
                "done": self.state == GameState.DEATH or self.state == GameState.VICTORY
            }

            self.learning_ai.observe_player_action(
                self.player_id, choice, context, result
            )

            # Update difficulty based on performance
            if hasattr(self, 'difficulty_adapter'):
                difficulty_params = self.learning_ai.get_difficulty_parameters()
                # Apply difficulty parameters to game

    def generate_narrative(self, player: PlayerCharacter, location) -> str:
        """Enhanced narrative generation using archetype system"""
        # Use the archetype narrator
        from narrative_generator import NarrativeContext, NarrativeTone, StoryBeat

        # Determine story beat based on progress
        if player.level < 3:
            story_beat = StoryBeat.CALL
        elif player.level < 5:
            story_beat = StoryBeat.THRESHOLD
        elif player.level < 8:
            story_beat = StoryBeat.TRIALS
        elif player.level < 12:
            story_beat = StoryBeat.ABYSS
        elif player.level < 15:
            story_beat = StoryBeat.TRANSFORMATION
        else:
            story_beat = StoryBeat.RETURN

        # Determine tone based on location
        tone_map = {
            "nexus": NarrativeTone.PEACEFUL,
            "void": NarrativeTone.OMINOUS,
            "oracle": NarrativeTone.MYSTERIOUS,
            "garden": NarrativeTone.CONTEMPLATIVE,
            "threshold": NarrativeTone.URGENT
        }

        tone = NarrativeTone.MYSTERIOUS
        for key, value in tone_map.items():
            if key in location.name.lower():
                tone = value
                break

        # Create context
        context = NarrativeContext(
            archetype=player.archetype,
            corridor=player.current_corridor,
            coherence=player.coherence,
            story_beat=story_beat,
            tone=tone,
            previous_choices=[],  # Would track actual choices
            world_state={}
        )

        # Generate narrative
        narrative = self.archetype_narrator.generate_narrative(context)

        # Check for narrative events
        for event in self.narrative_events:
            if not event.triggered and event.check_trigger({
                "coherence": player.coherence,
                "location": location.name,
                "archetype": player.archetype,
                "level": player.level
            }):
                narrative += f"\n\n⚡ SPECIAL EVENT ⚡\n{event.narrative}"

        return narrative

    def check_achievements(self):
        """Check and award achievements via blockchain"""
        if not self.blockchain_system or not self.player:
            return

        # Check coherence achievements
        if self.player.coherence > 1/PHI:
            self.blockchain_system.award_achievement(
                self.player_id, "first_coherence"
            )

        if self.player.coherence >= 1.0:
            self.blockchain_system.award_achievement(
                self.player_id, "perfect_coherence"
            )

        # Check wealth achievement
        if self.player.wallet and self.player.wallet.balance >= 1000:
            self.blockchain_system.award_achievement(
                self.player_id, "merchant_prince"
            )

    def initiate_multiplayer_match(self, opponent_id: str):
        """Start a PvP match"""
        if not self.multiplayer_coord or not self.player_id:
            print("Multiplayer not available")
            return

        match_id = self.multiplayer_coord.create_pvp_match(
            self.player_id, opponent_id,
            stakes=PHI * 10  # Default stakes
        )

        print(f"\n⚔️ PvP Match Started!")
        print(f"   Match ID: {match_id}")
        print(f"   Opponent: {opponent_id}")
        print(f"   Stakes: {PHI * 10:.1f} BloomCoins")

        # Would implement actual PvP mechanics here

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="BloomQuest - A text-based adventure powered by BloomCoin"
    )

    parser.add_argument(
        "--multiplayer",
        action="store_true",
        help="Enable multiplayer features"
    )

    parser.add_argument(
        "--difficulty",
        choices=["easy", "normal", "hard", "golden"],
        default="normal",
        help="Set game difficulty"
    )

    parser.add_argument(
        "--save-dir",
        default="saves",
        help="Directory for save files"
    )

    parser.add_argument(
        "--load-learning",
        action="store_true",
        help="Load previous learning AI data"
    )

    parser.add_argument(
        "--autosave",
        action="store_true",
        help="Enable automatic saving"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    parser.add_argument(
        "--quick-start",
        action="store_true",
        help="Skip intro and start quickly"
    )

    args = parser.parse_args()

    # Create and run launcher
    launcher = BloomQuestLauncher(args)
    launcher.run()

if __name__ == "__main__":
    main()