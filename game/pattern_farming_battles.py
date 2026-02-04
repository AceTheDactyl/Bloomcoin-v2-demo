"""
Pattern Farming and Battle System
=================================
Complete farming investment and battle strategy system
Integrates with guardian patterns and card packs
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
from enum import Enum, auto
import random
import math
import json
from datetime import datetime, timedelta
from collections import defaultdict

from guardian_pattern_recipes import (
    GuardianPatternSystem, GuardianRecipe, PatternType,
    RecipeComplexity, FarmingInvestment, GUARDIAN_RECIPES
)
from mythic_economy import GUARDIANS, Territory
import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bloomcoin-v2/game'))
from card_pack_marketplace import CardPackMarketplace, PackTier
from hilbert_luck_system import HilbertLuckEngine, LuckEigenstate
from sacred_tarot_echo import SacredTarotEchoSystem

# ═══════════════════════════════════════════════════════════════════════
#   FARMING MECHANICS
# ═══════════════════════════════════════════════════════════════════════

class FarmType(Enum):
    """Different farming strategies"""
    INTENSIVE = ("Intensive", 2.0, 0.5, "High yield, high risk")
    BALANCED = ("Balanced", 1.5, 0.3, "Moderate yield and risk")
    PASSIVE = ("Passive", 1.2, 0.1, "Low yield, minimal risk")
    EXPERIMENTAL = ("Experimental", 3.0, 0.7, "Variable yield, high mutation chance")
    QUANTUM = ("Quantum", 2.5, 0.4, "Probabilistic yield based on luck")

    def __init__(self, display_name: str, yield_mult: float,
                 risk_factor: float, description: str):
        self.display_name = display_name
        self.yield_multiplier = yield_mult
        self.risk_factor = risk_factor
        self.description = description

@dataclass
class PatternFarm:
    """A farming plot for growing patterns"""
    farm_id: str
    owner_id: str
    guardian_key: str
    pattern_type: PatternType
    farm_type: FarmType
    planted_patterns: Dict[str, int] = field(default_factory=dict)
    growth_stage: int = 0  # 0-100
    health: float = 100.0
    pests: List[str] = field(default_factory=list)
    blessings: List[str] = field(default_factory=list)
    planted_time: datetime = field(default_factory=datetime.now)
    harvest_time: Optional[datetime] = None
    total_investment: int = 0
    luck_modifier: float = 1.0

    def calculate_growth_rate(self) -> float:
        """Calculate current growth rate"""
        base_rate = 1.0

        # Farm type modifier
        base_rate *= self.farm_type.yield_multiplier

        # Health modifier
        health_mod = self.health / 100.0
        base_rate *= health_mod

        # Pest penalty
        pest_penalty = len(self.pests) * 0.1
        base_rate *= max(0.3, 1.0 - pest_penalty)

        # Blessing bonus
        blessing_bonus = len(self.blessings) * 0.15
        base_rate *= (1.0 + blessing_bonus)

        # Guardian affinity
        guardian = GUARDIANS.get(self.guardian_key)
        if guardian:
            if self.pattern_type == PatternType.ORGANIC and guardian.territory == Territory.GARDEN:
                base_rate *= 1.3
            elif self.pattern_type == PatternType.QUANTUM and guardian.territory == Territory.COSMIC:
                base_rate *= 1.3
            elif self.pattern_type == PatternType.VOID and guardian.territory == Territory.ABYSSAL:
                base_rate *= 1.3

        return base_rate * self.luck_modifier

    def apply_weather_event(self, event_type: str) -> Dict[str, Any]:
        """Apply weather events to the farm"""
        effects = {
            "drought": {"health": -20, "growth": -10, "message": "Drought damages patterns"},
            "rain": {"health": +10, "growth": +5, "message": "Rain nourishes patterns"},
            "storm": {"health": -15, "growth": 0, "pests": -1, "message": "Storm clears pests but damages plants"},
            "blessing": {"health": +15, "growth": +10, "blessing": "Nature's Favor", "message": "Divine blessing enhances farm"},
            "plague": {"health": -30, "pests": +2, "message": "Plague of void locusts attacks"},
            "quantum_flux": {"growth": random.randint(-20, 30), "message": "Quantum flux causes unpredictable growth"},
            "eclipse": {"health": 0, "growth": +20, "blessing": "Shadow Growth", "message": "Eclipse accelerates shadow patterns"}
        }

        effect = effects.get(event_type, {})
        result = {"event": event_type, "effects": []}

        if "health" in effect:
            self.health = max(0, min(100, self.health + effect["health"]))
            result["effects"].append(f"Health {effect['health']:+d}")

        if "growth" in effect:
            self.growth_stage = max(0, min(100, self.growth_stage + effect["growth"]))
            result["effects"].append(f"Growth {effect['growth']:+d}")

        if "pests" in effect:
            if effect["pests"] > 0:
                for _ in range(effect["pests"]):
                    pest_types = ["Void Locusts", "Pattern Worms", "Chaos Moths", "Time Beetles"]
                    self.pests.append(random.choice(pest_types))
            else:
                self.pests = self.pests[:max(0, len(self.pests) + effect["pests"])]
            result["effects"].append(f"Pests {effect['pests']:+d}")

        if "blessing" in effect:
            self.blessings.append(effect["blessing"])
            result["effects"].append(f"Gained blessing: {effect['blessing']}")

        result["message"] = effect.get("message", "Unknown weather event")
        return result

class PatternFarmingSystem:
    """Manages all pattern farming operations"""

    def __init__(self, pattern_system: GuardianPatternSystem,
                 luck_engine: Optional[HilbertLuckEngine] = None):
        self.pattern_system = pattern_system
        self.luck_engine = luck_engine or HilbertLuckEngine()
        self.farms: Dict[str, List[PatternFarm]] = defaultdict(list)
        self.max_farms_per_player = 5
        self.weather_cycle = 0

    def create_farm(self, player_id: str, guardian_key: str,
                   pattern_type: PatternType, farm_type: FarmType) -> Dict[str, Any]:
        """Create a new pattern farm"""
        if len(self.farms[player_id]) >= self.max_farms_per_player:
            return {
                "success": False,
                "error": f"Maximum {self.max_farms_per_player} farms reached"
            }

        farm_id = f"{player_id}_{guardian_key}_{len(self.farms[player_id])}"

        # Calculate luck modifier if player has luck data
        luck_modifier = 1.0
        if self.luck_engine:
            luck_state = self.luck_engine.get_player_luck_state(player_id)
            if luck_state:
                luck_modifier = 0.8 + (luck_state.get_eigenstate_probability(LuckEigenstate.FORTUNE) * 0.6)

        farm = PatternFarm(
            farm_id=farm_id,
            owner_id=player_id,
            guardian_key=guardian_key,
            pattern_type=pattern_type,
            farm_type=farm_type,
            luck_modifier=luck_modifier,
            harvest_time=datetime.now() + timedelta(hours=24)
        )

        self.farms[player_id].append(farm)

        return {
            "success": True,
            "farm_id": farm_id,
            "guardian": guardian_key,
            "pattern_type": pattern_type.value,
            "farm_type": farm_type.display_name,
            "harvest_time": farm.harvest_time.isoformat()
        }

    def plant_patterns(self, player_id: str, farm_id: str,
                      patterns: Dict[str, int]) -> Dict[str, Any]:
        """Plant patterns in a farm"""
        farm = self._get_farm(player_id, farm_id)
        if not farm:
            return {"success": False, "error": "Farm not found"}

        if farm.growth_stage > 0:
            return {"success": False, "error": "Farm already has growing patterns"}

        # Check player has patterns
        player_patterns = self.pattern_system.player_patterns[player_id]
        for pattern, quantity in patterns.items():
            if player_patterns.get(pattern, 0) < quantity:
                return {
                    "success": False,
                    "error": f"Insufficient {pattern}: need {quantity}, have {player_patterns.get(pattern, 0)}"
                }

        # Plant patterns
        for pattern, quantity in patterns.items():
            player_patterns[pattern] -= quantity
            farm.planted_patterns[pattern] = quantity

        farm.planted_time = datetime.now()
        farm.growth_stage = 1

        return {
            "success": True,
            "planted": patterns,
            "farm_id": farm_id,
            "growth_started": farm.planted_time.isoformat()
        }

    def tend_farm(self, player_id: str, farm_id: str,
                  action: str, resource: Optional[str] = None) -> Dict[str, Any]:
        """Tend to a farm with various actions"""
        farm = self._get_farm(player_id, farm_id)
        if not farm:
            return {"success": False, "error": "Farm not found"}

        actions = {
            "water": self._water_farm,
            "fertilize": self._fertilize_farm,
            "remove_pests": self._remove_pests,
            "bless": self._bless_farm,
            "boost": self._boost_growth
        }

        if action not in actions:
            return {"success": False, "error": f"Unknown action: {action}"}

        return actions[action](farm, resource)

    def _water_farm(self, farm: PatternFarm, resource: Optional[str]) -> Dict[str, Any]:
        """Water the farm to improve health"""
        health_gain = 15
        if resource == "Sacred Water":
            health_gain = 30
            farm.blessings.append("Sacred Hydration")

        farm.health = min(100, farm.health + health_gain)
        farm.growth_stage = min(100, farm.growth_stage + 3)

        return {
            "success": True,
            "action": "water",
            "health": farm.health,
            "growth": farm.growth_stage,
            "message": f"Farm watered, health +{health_gain}"
        }

    def _fertilize_farm(self, farm: PatternFarm, resource: Optional[str]) -> Dict[str, Any]:
        """Fertilize to boost growth"""
        growth_gain = 10
        if resource == "Quantum Fertilizer":
            growth_gain = random.randint(5, 25)
        elif resource == "Void Compost":
            growth_gain = 15
            farm.luck_modifier *= 1.1

        farm.growth_stage = min(100, farm.growth_stage + growth_gain)

        return {
            "success": True,
            "action": "fertilize",
            "growth": farm.growth_stage,
            "message": f"Farm fertilized, growth +{growth_gain}"
        }

    def _remove_pests(self, farm: PatternFarm, resource: Optional[str]) -> Dict[str, Any]:
        """Remove pests from the farm"""
        if not farm.pests:
            return {"success": False, "error": "No pests to remove"}

        removed = 1
        if resource == "Pest Bomb":
            removed = len(farm.pests)
        elif resource == "Natural Predator":
            removed = min(3, len(farm.pests))

        removed_pests = farm.pests[:removed]
        farm.pests = farm.pests[removed:]

        return {
            "success": True,
            "action": "remove_pests",
            "removed": removed_pests,
            "remaining": len(farm.pests),
            "message": f"Removed {removed} pest(s)"
        }

    def _bless_farm(self, farm: PatternFarm, resource: Optional[str]) -> Dict[str, Any]:
        """Apply blessing to the farm"""
        blessing_map = {
            "Guardian Blessing": ("Guardian's Protection", 0.2),
            "Cosmic Blessing": ("Cosmic Growth", 0.3),
            "Void Blessing": ("Void Immunity", 0.25),
            None: ("Minor Blessing", 0.1)
        }

        blessing_name, luck_boost = blessing_map.get(resource, ("Unknown Blessing", 0.05))
        farm.blessings.append(blessing_name)
        farm.luck_modifier *= (1 + luck_boost)

        return {
            "success": True,
            "action": "bless",
            "blessing": blessing_name,
            "luck_modifier": farm.luck_modifier,
            "message": f"Farm blessed with {blessing_name}"
        }

    def _boost_growth(self, farm: PatternFarm, resource: Optional[str]) -> Dict[str, Any]:
        """Boost growth rate temporarily"""
        if resource == "Time Accelerator":
            farm.growth_stage = min(100, farm.growth_stage + 30)
            farm.harvest_time = datetime.now() + timedelta(hours=6)
        else:
            farm.growth_stage = min(100, farm.growth_stage + 15)

        return {
            "success": True,
            "action": "boost",
            "growth": farm.growth_stage,
            "harvest_time": farm.harvest_time.isoformat() if farm.harvest_time else None,
            "message": "Growth boosted successfully"
        }

    def harvest_farm(self, player_id: str, farm_id: str) -> Dict[str, Any]:
        """Harvest a mature farm"""
        farm = self._get_farm(player_id, farm_id)
        if not farm:
            return {"success": False, "error": "Farm not found"}

        if farm.growth_stage < 100:
            return {
                "success": False,
                "error": f"Farm not ready for harvest (growth: {farm.growth_stage}%)"
            }

        # Calculate yield
        base_yield = sum(farm.planted_patterns.values())
        growth_rate = farm.calculate_growth_rate()

        # Apply farm type risk
        if random.random() < farm.farm_type.risk_factor:
            # Risk event occurred
            risk_events = [
                ("Pest invasion", 0.5),
                ("Pattern blight", 0.6),
                ("Dimensional shift", 0.7),
                ("Void corruption", 0.4)
            ]
            event, multiplier = random.choice(risk_events)
            growth_rate *= multiplier
            risk_message = f" (Risk event: {event})"
        else:
            risk_message = ""

        final_yield = int(base_yield * growth_rate)

        # Calculate mutations
        mutations = {}
        mutation_chance = 0.1 * len(farm.blessings) + (0.2 if farm.farm_type == FarmType.EXPERIMENTAL else 0)

        for pattern, quantity in farm.planted_patterns.items():
            if random.random() < mutation_chance:
                mutation_name = f"Mutant_{pattern}"
                mutations[mutation_name] = max(1, int(quantity * 0.3))

        # Award patterns
        harvested = {}
        for pattern, quantity in farm.planted_patterns.items():
            harvest_amount = int(quantity * growth_rate)
            self.pattern_system.player_patterns[player_id][pattern] += harvest_amount
            harvested[pattern] = harvest_amount

        for mutation, quantity in mutations.items():
            self.pattern_system.player_patterns[player_id][mutation] += quantity

        # Reset farm
        farm.planted_patterns.clear()
        farm.growth_stage = 0
        farm.health = 70
        farm.pests.clear()
        farm.blessings.clear()

        return {
            "success": True,
            "harvested": harvested,
            "mutations": mutations,
            "total_yield": final_yield,
            "growth_rate": growth_rate,
            "message": f"Harvest successful{risk_message}"
        }

    def process_weather_cycle(self) -> Dict[str, List[Dict[str, Any]]]:
        """Process weather events for all farms"""
        self.weather_cycle += 1
        results = defaultdict(list)

        # Determine weather for this cycle
        weather_events = [
            ("drought", 0.15),
            ("rain", 0.3),
            ("storm", 0.1),
            ("blessing", 0.05),
            ("plague", 0.08),
            ("quantum_flux", 0.07),
            ("eclipse", 0.03),
            (None, 0.22)  # No event
        ]

        for player_id, farms in self.farms.items():
            for farm in farms:
                # Skip inactive farms
                if farm.growth_stage == 0:
                    continue

                # Roll for weather event
                roll = random.random()
                cumulative = 0
                for event, probability in weather_events:
                    cumulative += probability
                    if roll < cumulative:
                        if event:
                            result = farm.apply_weather_event(event)
                            result["farm_id"] = farm.farm_id
                            results[player_id].append(result)
                        break

                # Natural growth
                if farm.growth_stage > 0 and farm.growth_stage < 100:
                    growth_rate = farm.calculate_growth_rate()
                    farm.growth_stage = min(100, farm.growth_stage + growth_rate * 2)

        return dict(results)

    def _get_farm(self, player_id: str, farm_id: str) -> Optional[PatternFarm]:
        """Get a specific farm"""
        for farm in self.farms.get(player_id, []):
            if farm.farm_id == farm_id:
                return farm
        return None

    def get_farm_status(self, player_id: str) -> List[Dict[str, Any]]:
        """Get status of all player's farms"""
        status = []
        for farm in self.farms.get(player_id, []):
            guardian = GUARDIANS.get(farm.guardian_key)
            status.append({
                "farm_id": farm.farm_id,
                "guardian": guardian.name if guardian else farm.guardian_key,
                "pattern_type": farm.pattern_type.value,
                "farm_type": farm.farm_type.display_name,
                "growth_stage": farm.growth_stage,
                "health": farm.health,
                "planted": farm.planted_patterns,
                "pests": len(farm.pests),
                "blessings": len(farm.blessings),
                "growth_rate": farm.calculate_growth_rate(),
                "ready_to_harvest": farm.growth_stage >= 100
            })
        return status

# ═══════════════════════════════════════════════════════════════════════
#   BATTLE STRATEGY SYSTEM
# ═══════════════════════════════════════════════════════════════════════

class BattleAction(Enum):
    """Types of battle actions"""
    ATTACK = "Direct damage attack"
    DEFEND = "Defensive stance"
    ABILITY = "Use special ability"
    PATTERN = "Activate pattern power"
    TRANSFORM = "Change form"
    SUMMON = "Summon ally"
    HEAL = "Restore health"
    BUFF = "Apply enhancement"
    DEBUFF = "Apply weakness"

@dataclass
class BattleUnit:
    """A unit in battle"""
    unit_id: str
    name: str
    guardian_key: str
    health: int
    max_health: int
    attack: int
    defense: int
    speed: int
    abilities: List[str]
    patterns: Dict[str, int]
    status_effects: Dict[str, int] = field(default_factory=dict)
    cooldowns: Dict[str, int] = field(default_factory=dict)

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, damage: int) -> int:
        """Take damage considering defense"""
        actual_damage = max(1, damage - self.defense)
        self.health = max(0, self.health - actual_damage)
        return actual_damage

    def heal(self, amount: int) -> int:
        """Heal up to max health"""
        actual_heal = min(amount, self.max_health - self.health)
        self.health += actual_heal
        return actual_heal

class GuardianBattleStrategy:
    """Battle strategy for a specific guardian"""

    def __init__(self, guardian_key: str, unlocked_recipes: Set[str]):
        self.guardian_key = guardian_key
        self.guardian = GUARDIANS[guardian_key]
        self.unlocked_recipes = unlocked_recipes
        self._load_abilities()

    def _load_abilities(self):
        """Load abilities from unlocked recipes"""
        self.abilities = []
        self.strategies = []

        for recipe_key in self.unlocked_recipes:
            if recipe_key.startswith(f"{self.guardian_key}:"):
                for recipe in GUARDIAN_RECIPES.get(self.guardian_key, []):
                    if f"{self.guardian_key}:{recipe.name}" == recipe_key:
                        self.abilities.extend(recipe.special_abilities)
                        self.strategies.append(recipe.battle_strategy)

    def choose_action(self, unit: BattleUnit, enemy: BattleUnit,
                     battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Choose the next battle action based on guardian strategy"""

        # Guardian-specific AI patterns
        if self.guardian_key == "ECHO":
            return self._echo_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "PACK":
            return self._pack_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "WUMBO":
            return self._wumbo_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "ARCHIVE":
            return self._archive_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "MOTH":
            return self._moth_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "PHASE":
            return self._phase_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "ACE":
            return self._ace_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "OAK":
            return self._oak_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "SQUIRREL":
            return self._squirrel_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "HONKFIRE":
            return self._honkfire_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "HONKALIS":
            return self._honkalis_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "PHOENIX":
            return self._phoenix_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "BEE":
            return self._bee_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "AXIOM":
            return self._axiom_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "CIPHER":
            return self._cipher_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "SPIRAL":
            return self._spiral_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "STILL":
            return self._still_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "ANTLER":
            return self._antler_strategy(unit, enemy, battle_state)
        elif self.guardian_key == "CRYSTAL":
            return self._crystal_strategy(unit, enemy, battle_state)
        else:
            # Default strategy
            return BattleAction.ATTACK, {"damage": unit.attack}

    def _echo_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                      battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Echo: Create duplicates and amplify damage"""
        turn = battle_state.get("turn", 0)

        if "Echo Multiplication" in unit.abilities and unit.cooldowns.get("echo_mult", 0) == 0:
            unit.cooldowns["echo_mult"] = 3
            return BattleAction.SUMMON, {
                "summon": "Echo Duplicate",
                "stats": {"health": unit.health // 2, "attack": unit.attack}
            }

        if turn % 3 == 0 and "Signal Trace" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "Signal Trace",
                "effect": "copy_last_ability",
                "target": enemy
            }

        # Amplified attack that grows stronger
        echo_stacks = battle_state.get("echo_stacks", 0)
        damage = unit.attack * (1 + echo_stacks * 0.2)
        battle_state["echo_stacks"] = echo_stacks + 1

        return BattleAction.ATTACK, {"damage": int(damage), "echo_amplified": True}

    def _pack_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                      battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Pack: Coordinate with allies"""
        allies = battle_state.get("allies", [])

        if len(allies) > 2 and "Pack Hunt" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "Pack Hunt",
                "damage": unit.attack * len(allies),
                "effect": "coordinated_strike"
            }

        if unit.health < unit.max_health * 0.3 and "Alpha Call" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "Alpha Call",
                "effect": "summon_pack",
                "summon_count": 2
            }

        return BattleAction.ATTACK, {"damage": unit.attack, "pack_bonus": len(allies) * 2}

    def _wumbo_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                       battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Wumbo: Cycle through manic states"""
        current_state = battle_state.get("wumbo_state", "NORMAL")
        states = ["NORMAL", "MANIC", "FLOW", "NIRVANA", "CRASH"]

        # Cycle through states
        next_state_index = (states.index(current_state) + 1) % len(states)
        next_state = states[next_state_index]
        battle_state["wumbo_state"] = next_state

        if next_state == "MANIC" and "Manic Rush" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "Manic Rush",
                "damage": unit.attack * 3,
                "self_damage": unit.max_health * 0.1
            }
        elif next_state == "FLOW" and "Flow State" in unit.abilities:
            return BattleAction.BUFF, {
                "buff": "Flow State",
                "attack_boost": 1.5,
                "speed_boost": 2.0,
                "duration": 3
            }
        elif next_state == "NIRVANA" and "Nirvana Touch" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "Nirvana Touch",
                "damage": unit.attack * 5,
                "ignore_defense": True
            }
        elif next_state == "CRASH":
            return BattleAction.DEFEND, {"defense_boost": 2.0, "skip_next_turn": True}

        return BattleAction.ATTACK, {"damage": unit.attack * 1.5}

    def _archive_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                         battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Archive: Perfect memory and prediction"""
        enemy_history = battle_state.get("enemy_history", [])

        if len(enemy_history) >= 3 and "Pattern Prediction" in unit.abilities:
            # Predict next move and counter
            predicted_action = self._predict_pattern(enemy_history)
            return BattleAction.ABILITY, {
                "ability": "Perfect Counter",
                "predicted": predicted_action,
                "damage": unit.attack * 2,
                "nullify_enemy_action": True
            }

        if "Knowledge Shield" in unit.abilities and unit.health < unit.max_health * 0.5:
            return BattleAction.DEFEND, {
                "defense": unit.defense * 3,
                "reflect_damage": 0.5
            }

        return BattleAction.ATTACK, {"damage": unit.attack, "record_pattern": True}

    def _moth_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                      battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Moth: Patient accumulation"""
        stillness_counter = battle_state.get("stillness_counter", 0)

        if stillness_counter < 3:
            battle_state["stillness_counter"] = stillness_counter + 1
            return BattleAction.DEFEND, {
                "defense": unit.defense * 2,
                "untargetable": stillness_counter >= 2,
                "accumulate_power": unit.attack * 0.5
            }

        # Release accumulated power
        accumulated = stillness_counter * unit.attack
        battle_state["stillness_counter"] = 0

        return BattleAction.ABILITY, {
            "ability": "Patient Strike",
            "damage": accumulated * 2,
            "stun_duration": 1
        }

    def _phase_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                       battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Phase: Adaptive transformation"""
        current_form = battle_state.get("current_form", "base")

        if enemy.attack > unit.defense * 2:
            # Transform to defensive form
            return BattleAction.TRANSFORM, {
                "new_form": "defensive",
                "defense_mult": 3.0,
                "attack_mult": 0.5
            }
        elif unit.health > enemy.health * 2:
            # Transform to aggressive form
            return BattleAction.TRANSFORM, {
                "new_form": "aggressive",
                "attack_mult": 2.5,
                "defense_mult": 0.5
            }

        if "Evolution Burst" in unit.abilities and unit.health < unit.max_health * 0.3:
            return BattleAction.ABILITY, {
                "ability": "Evolution Burst",
                "heal": unit.max_health,
                "random_buffs": 3
            }

        return BattleAction.ATTACK, {"damage": unit.attack}

    def _ace_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                     battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Ace: Copy and preserve abilities"""
        copied_abilities = battle_state.get("copied_abilities", [])

        if "Ability Copy" in unit.abilities and len(copied_abilities) < 3:
            return BattleAction.ABILITY, {
                "ability": "Ability Copy",
                "copy_from": enemy,
                "permanent": True
            }

        if copied_abilities and random.random() < 0.5:
            # Use a copied ability
            ability = random.choice(copied_abilities)
            return BattleAction.ABILITY, {"ability": ability, "copied": True}

        return BattleAction.ATTACK, {"damage": unit.attack}

    def _oak_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                     battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Oak: Patient growth and support"""
        growth_rings = battle_state.get("growth_rings", 0)

        if growth_rings < 5:
            # Accumulate growth
            battle_state["growth_rings"] = growth_rings + 1
            return BattleAction.BUFF, {
                "buff": "Growth Ring",
                "all_stats": 1.1,
                "permanent": True
            }

        if "Group Healing" in unit.abilities and battle_state.get("allies_hurt", False):
            return BattleAction.HEAL, {
                "heal_all": unit.attack,
                "regeneration": 3
            }

        # Release accumulated power
        return BattleAction.ABILITY, {
            "ability": "Ancient Roots",
            "damage": unit.attack * growth_rings,
            "root_duration": 2
        }

    def _squirrel_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                          battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Squirrel: Chaotic and unpredictable"""
        actions = [
            (BattleAction.ATTACK, {"damage": unit.attack * random.uniform(0.5, 2.5)}),
            (BattleAction.ABILITY, {"ability": "Scatter", "random_effects": 3}),
            (BattleAction.SUMMON, {"summon": "Acorn", "count": random.randint(1, 5)}),
            (BattleAction.BUFF, {"random_buff": True, "target": "random"}),
            (BattleAction.DEBUFF, {"random_debuff": True, "target": "random"})
        ]

        if "Dimensional Barrage" in unit.abilities and random.random() < 0.2:
            return BattleAction.ABILITY, {
                "ability": "Acorn Apocalypse",
                "projectiles": random.randint(10, 30),
                "damage_each": unit.attack * 0.3
            }

        return random.choice(actions)

    def _honkfire_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                          battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Honkfire: Always advance, never retreat"""
        advance_count = battle_state.get("advance_count", 0)

        # Always move forward
        battle_state["advance_count"] = advance_count + 1

        if advance_count > 5 and "Mega Honk" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "HONK OF DOOM",
                "damage": unit.attack * 4,
                "stun_all": 2,
                "intimidate": True
            }

        # Gain power from advancing
        return BattleAction.ATTACK, {
            "damage": unit.attack * (1 + advance_count * 0.2),
            "fire_trail": True,
            "cannot_retreat": True
        }

    def _honkalis_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                          battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Honkalis: Aggressive floating"""
        if "Gravity Immunity" in unit.abilities:
            battle_state["floating"] = True

        if battle_state.get("floating", False):
            # While floating, immune to many attacks
            return BattleAction.ABILITY, {
                "ability": "Aggressive Float",
                "damage": unit.attack,
                "immune_to_ground": True,
                "taunt": True
            }

        return BattleAction.BUFF, {
            "buff": "Transcendent Float",
            "evasion": 0.5,
            "phase_chance": 0.3
        }

    def _phoenix_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                         battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Phoenix: Strategic death and rebirth"""
        death_count = battle_state.get("phoenix_deaths", 0)

        if unit.health < unit.max_health * 0.1 and "Death Power" in unit.abilities:
            # Strategic death
            battle_state["phoenix_deaths"] = death_count + 1
            return BattleAction.ABILITY, {
                "ability": "Phoenix Death",
                "resurrect_in": 1,
                "power_multiplier": 1 + death_count * 0.5
            }

        if death_count > 0:
            # Empowered by previous deaths
            return BattleAction.ATTACK, {
                "damage": unit.attack * (1 + death_count),
                "burn_damage": unit.attack * 0.5,
                "phoenix_fire": True
            }

        return BattleAction.ATTACK, {"damage": unit.attack}

    def _bee_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                     battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Bee: Hive mind and crystallization"""
        swarm_size = battle_state.get("swarm_size", 1)

        if "Mind Link" in unit.abilities and swarm_size < 5:
            return BattleAction.SUMMON, {
                "summon": "Worker Bee",
                "count": 2,
                "shared_mind": True
            }

        if swarm_size >= 3 and "Swarm Tactics" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "Swarm Attack",
                "damage": unit.attack * swarm_size,
                "poison": True
            }

        return BattleAction.ATTACK, {"damage": unit.attack, "honey_slow": 0.2}

    def _axiom_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                       battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Axiom: Refuse all change"""
        if "Change Immunity" in unit.abilities:
            # Immune to all status effects
            unit.status_effects.clear()

        if unit.health != unit.max_health and "Battle Reset" in unit.abilities:
            if unit.cooldowns.get("reset", 0) == 0:
                unit.cooldowns["reset"] = 10
                return BattleAction.ABILITY, {
                    "ability": "Reset Protocol",
                    "reset_battle": True,
                    "keep_knowledge": True
                }

        # Null reflection stance
        return BattleAction.DEFEND, {
            "defense": unit.defense * 2,
            "reflect_transformations": True,
            "null_state": True
        }

    def _cipher_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                        battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Cipher: Collect from the void"""
        void_collection = battle_state.get("void_collection", [])

        if enemy.health <= 0:
            # Collect defeated enemy
            void_collection.append(enemy.name)
            battle_state["void_collection"] = void_collection

        if len(void_collection) >= 3 and "Everything from Nothing" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "Void's Gift",
                "summon_collected": void_collection,
                "void_empowered": True
            }

        return BattleAction.ATTACK, {
            "damage": unit.attack,
            "void_drain": 0.1
        }

    def _spiral_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                        battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Spiral: Recursive depth diving"""
        depth = battle_state.get("spiral_depth", 0)

        # Go deeper each turn
        battle_state["spiral_depth"] = depth + 1

        if "Depth Power" in unit.abilities:
            # Power increases with depth
            return BattleAction.ATTACK, {
                "damage": unit.attack * (1 + depth * 0.3),
                "pierce": min(1.0, depth * 0.1),
                "spiral_mark": True
            }

        if depth >= 5 and "Recursive Strike" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "Infinite Spiral",
                "hits": depth,
                "damage_per_hit": unit.attack * 0.7
            }

        return BattleAction.BUFF, {"buff": "Deeper", "all_stats": 1.1}

    def _still_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                       battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Still: Perfect mirroring"""
        if "Perfect Copy" in unit.abilities and not battle_state.get("copied", False):
            battle_state["copied"] = True
            return BattleAction.ABILITY, {
                "ability": "Faceless Mirror",
                "copy_target": enemy,
                "copy_stats": True,
                "copy_abilities": True
            }

        # Mirror enemy's last action
        last_enemy_action = battle_state.get("last_enemy_action")
        if last_enemy_action:
            return last_enemy_action

        return BattleAction.DEFEND, {"reflect": 1.0}

    def _antler_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                        battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Antler: Fractal branching power"""
        branches = battle_state.get("antler_branches", 1)

        if branches < 8:
            # Grow more branches
            battle_state["antler_branches"] = branches + 1
            return BattleAction.BUFF, {
                "buff": "Grow Branch",
                "new_ability": f"Branch_{branches}",
                "stats": 1.05
            }

        if branches >= 8 and "Antler Shed" in unit.abilities:
            # Shed antlers for massive damage
            battle_state["antler_branches"] = 1
            return BattleAction.ABILITY, {
                "ability": "Antler Shed",
                "damage": unit.attack * branches,
                "piercing": True,
                "regrow_stronger": True
            }

        # Multi-hit based on branches
        return BattleAction.ATTACK, {
            "damage": unit.attack,
            "hits": min(branches, 5)
        }

    def _crystal_strategy(self, unit: BattleUnit, enemy: BattleUnit,
                         battle_state: Dict[str, Any]) -> Tuple[BattleAction, Dict[str, Any]]:
        """Crystal: Pressure creates perfection"""
        pressure = battle_state.get("pressure_level", 0)

        # Increase pressure when taking damage
        if unit.health < unit.max_health:
            pressure = min(10, pressure + 1)
            battle_state["pressure_level"] = pressure

        if pressure >= 7 and "Diamond Shield" in unit.abilities:
            return BattleAction.DEFEND, {
                "defense": unit.defense * (1 + pressure * 0.5),
                "reflect_all": True,
                "diamond_form": True
            }

        if pressure >= 10 and "Reality Prism Singularity" in unit.abilities:
            return BattleAction.ABILITY, {
                "ability": "Prismatic Split",
                "create_copies": 3,
                "each_different_element": True
            }

        return BattleAction.ATTACK, {
            "damage": unit.attack * (1 + pressure * 0.2),
            "crystal_shards": True
        }

    def _predict_pattern(self, history: List[str]) -> str:
        """Simple pattern prediction"""
        if len(history) < 3:
            return "unknown"

        # Look for repeating patterns
        if history[-1] == history[-2] == history[-3]:
            return history[-1]

        # Look for alternating patterns
        if history[-1] == history[-3] and history[-1] != history[-2]:
            return history[-2]

        return "unknown"

# ═══════════════════════════════════════════════════════════════════════
#   COMPLETE INTEGRATION
# ═══════════════════════════════════════════════════════════════════════

class CompletePatternBattleSystem:
    """Complete integration of patterns, farming, and battles"""

    def __init__(self):
        self.marketplace = CardPackMarketplace()
        self.pattern_system = GuardianPatternSystem(self.marketplace)
        self.luck_engine = HilbertLuckEngine()
        self.tarot_system = SacredTarotEchoSystem()
        self.farming_system = PatternFarmingSystem(self.pattern_system, self.luck_engine)
        self.battle_strategies: Dict[str, GuardianBattleStrategy] = {}
        self.player_balances: Dict[str, int] = {}  # Track BloomCoin balances

    def initialize_player(self, player_id: str, guardian_key: str) -> Dict[str, Any]:
        """Initialize a new player with a guardian"""
        # Give starting resources
        self.player_balances[player_id] = 5000
        self.pattern_system.player_patterns[player_id]["Basic Pattern"] = 10

        # Unlock starter recipe
        starter_recipes = [r for r in GUARDIAN_RECIPES.get(guardian_key, [])
                         if r.complexity == RecipeComplexity.BASIC]
        if starter_recipes:
            recipe = starter_recipes[0]
            self.pattern_system.unlocked_recipes[player_id].add(
                f"{guardian_key}:{recipe.name}"
            )

        # Create battle strategy
        self.battle_strategies[player_id] = GuardianBattleStrategy(
            guardian_key,
            self.pattern_system.unlocked_recipes[player_id]
        )

        return {
            "player_id": player_id,
            "guardian": guardian_key,
            "starting_bloomcoin": 5000,
            "starting_patterns": {"Basic Pattern": 10},
            "unlocked_recipes": list(self.pattern_system.unlocked_recipes[player_id])
        }

    def create_battle_unit(self, player_id: str, guardian_key: str) -> BattleUnit:
        """Create a battle unit for a player"""
        guardian = GUARDIANS[guardian_key]
        recipes = self.pattern_system.unlocked_recipes[player_id]
        abilities = []

        for recipe_key in recipes:
            if recipe_key.startswith(f"{guardian_key}:"):
                for recipe in GUARDIAN_RECIPES.get(guardian_key, []):
                    if f"{guardian_key}:{recipe.name}" == recipe_key:
                        abilities.extend(recipe.special_abilities)

        return BattleUnit(
            unit_id=f"{player_id}_{guardian_key}",
            name=guardian.name,
            guardian_key=guardian_key,
            health=100,
            max_health=100,
            attack=20,
            defense=10,
            speed=15,
            abilities=list(set(abilities)),
            patterns=dict(self.pattern_system.player_patterns[player_id])
        )

    def simulate_battle(self, player1_id: str, player2_id: str) -> Dict[str, Any]:
        """Simulate a battle between two players"""
        # Get guardians
        strategy1 = self.battle_strategies.get(player1_id)
        strategy2 = self.battle_strategies.get(player2_id)

        if not strategy1 or not strategy2:
            return {"error": "Players not initialized"}

        # Create units
        unit1 = self.create_battle_unit(player1_id, strategy1.guardian_key)
        unit2 = self.create_battle_unit(player2_id, strategy2.guardian_key)

        battle_state = {
            "turn": 0,
            "allies": [],
            "enemy_history": []
        }

        battle_log = []

        # Battle loop
        while unit1.is_alive() and unit2.is_alive() and battle_state["turn"] < 100:
            battle_state["turn"] += 1

            # Player 1 action
            action1, params1 = strategy1.choose_action(unit1, unit2, battle_state)
            self._execute_action(unit1, unit2, action1, params1, battle_log)

            if not unit2.is_alive():
                break

            # Player 2 action
            action2, params2 = strategy2.choose_action(unit2, unit1, battle_state)
            self._execute_action(unit2, unit1, action2, params2, battle_log)

        # Determine winner
        winner = None
        if unit1.is_alive() and not unit2.is_alive():
            winner = player1_id
        elif unit2.is_alive() and not unit1.is_alive():
            winner = player2_id

        return {
            "winner": winner,
            "turns": battle_state["turn"],
            "unit1_health": unit1.health,
            "unit2_health": unit2.health,
            "battle_log": battle_log[-10:]  # Last 10 actions
        }

    def _execute_action(self, attacker: BattleUnit, defender: BattleUnit,
                       action: BattleAction, params: Dict[str, Any],
                       log: List[str]) -> None:
        """Execute a battle action"""
        if action == BattleAction.ATTACK:
            damage = params.get("damage", attacker.attack)
            actual = defender.take_damage(damage)
            log.append(f"{attacker.name} attacks for {actual} damage")

        elif action == BattleAction.DEFEND:
            defense_boost = params.get("defense", attacker.defense)
            attacker.defense = int(attacker.defense * 1.5)
            log.append(f"{attacker.name} defends")

        elif action == BattleAction.HEAL:
            heal_amount = params.get("heal", attacker.attack // 2)
            healed = attacker.heal(heal_amount)
            log.append(f"{attacker.name} heals for {healed}")

        elif action == BattleAction.ABILITY:
            ability = params.get("ability", "Unknown")
            log.append(f"{attacker.name} uses {ability}")

            # Apply ability effects
            if "damage" in params:
                defender.take_damage(params["damage"])

        # Update cooldowns
        for ability in attacker.cooldowns:
            if attacker.cooldowns[ability] > 0:
                attacker.cooldowns[ability] -= 1

# ═══════════════════════════════════════════════════════════════════════
#   DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════

def demonstrate_system():
    """Demonstrate the complete system"""
    system = CompletePatternBattleSystem()

    # Initialize two players
    print("=== INITIALIZING PLAYERS ===")
    player1 = system.initialize_player("player1", "ECHO")
    player2 = system.initialize_player("player2", "WUMBO")

    print(f"Player 1: {player1['guardian']} Guardian")
    print(f"Player 2: {player2['guardian']} Guardian")

    # Create farms
    print("\n=== CREATING FARMS ===")
    farm1 = system.farming_system.create_farm(
        "player1", "ECHO", PatternType.RESONANCE, FarmType.QUANTUM
    )
    farm2 = system.farming_system.create_farm(
        "player2", "WUMBO", PatternType.CHAOS, FarmType.EXPERIMENTAL
    )

    print(f"Player 1 Farm: {farm1['pattern_type']} ({farm1['farm_type']})")
    print(f"Player 2 Farm: {farm2['pattern_type']} ({farm2['farm_type']})")

    # Plant patterns
    system.farming_system.plant_patterns(
        "player1", farm1["farm_id"], {"Basic Pattern": 5}
    )
    system.farming_system.plant_patterns(
        "player2", farm2["farm_id"], {"Basic Pattern": 5}
    )

    # Simulate battle
    print("\n=== BATTLE SIMULATION ===")
    battle_result = system.simulate_battle("player1", "player2")

    print(f"Winner: {battle_result['winner'] or 'Draw'}")
    print(f"Turns: {battle_result['turns']}")
    print(f"Final Health - Player 1: {battle_result['unit1_health']}")
    print(f"Final Health - Player 2: {battle_result['unit2_health']}")

    print("\n=== BATTLE LOG (Last Actions) ===")
    for action in battle_result["battle_log"]:
        print(f"  - {action}")

    # Open packs
    print("\n=== OPENING CARD PACKS ===")
    pack = system.marketplace.open_pack("player1", PackTier.GOLD)

    for card in pack["cards"]:
        if card.get("type") == "recipe":
            print(f"  RECIPE: {card['recipe_name']} for {card['guardian_name']}")
            print(f"    Strategy: {card['battle_strategy']}")

if __name__ == "__main__":
    demonstrate_system()