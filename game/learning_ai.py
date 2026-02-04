#!/usr/bin/env python3
"""
Advanced Learning AI Module for BloomQuest
==========================================
Implements adaptive AI that learns from player behavior using
golden ratio-based neural networks and reinforcement learning.
"""

import numpy as np
import json
import pickle
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import deque
import math
import random
from datetime import datetime
from pathlib import Path

# Add bloomcoin imports
import sys
sys.path.append(str(Path(__file__).parent.parent / "bloomcoin-v0.1.0" / "bloomcoin"))

from bloomcoin.constants import PHI, Z_C, K
from garden.consensus.kuramoto import KuramotoOscillator

# Neural network constants (all derived from φ)
INPUT_NEURONS = int(PHI * 13)     # 21 input neurons
HIDDEN_NEURONS = int(PHI * 8)     # 13 hidden neurons
OUTPUT_NEURONS = int(PHI * 5)     # 8 output neurons
LEARNING_RATE = 1 / (PHI ** 2)    # ~0.382
MOMENTUM = 1 / PHI                # ~0.618
DECAY_RATE = 1 / (PHI ** 3)       # ~0.236

@dataclass
class PlayerProfile:
    """Comprehensive profile of player behavior and preferences"""
    player_id: str
    play_sessions: int = 0
    total_playtime: float = 0.0

    # Behavioral metrics
    aggression_score: float = 0.5
    exploration_score: float = 0.5
    social_score: float = 0.5
    optimization_score: float = 0.5
    creativity_score: float = 0.5

    # Decision patterns
    decision_history: deque = field(default_factory=lambda: deque(maxlen=100))
    reaction_times: deque = field(default_factory=lambda: deque(maxlen=50))

    # Performance metrics
    success_rate: float = 0.5
    coherence_average: float = 0.5
    learning_curve: List[float] = field(default_factory=list)

    # Preferences
    preferred_actions: Dict[str, float] = field(default_factory=dict)
    avoided_actions: Dict[str, float] = field(default_factory=dict)
    favorite_locations: Dict[str, int] = field(default_factory=dict)

    # Oscillator coupling
    oscillator_history: List[float] = field(default_factory=list)
    phase_preferences: List[float] = field(default_factory=list)

class GoldenNeuralNetwork:
    """Neural network with architecture based on golden ratio"""

    def __init__(self, input_size: int = INPUT_NEURONS,
                 hidden_size: int = HIDDEN_NEURONS,
                 output_size: int = OUTPUT_NEURONS):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights using golden ratio scaling
        self.weights_input_hidden = self._golden_init(input_size, hidden_size)
        self.weights_hidden_output = self._golden_init(hidden_size, output_size)

        # Biases
        self.bias_hidden = np.zeros(hidden_size)
        self.bias_output = np.zeros(output_size)

        # Momentum terms
        self.momentum_ih = np.zeros_like(self.weights_input_hidden)
        self.momentum_ho = np.zeros_like(self.weights_hidden_output)

        # Activation history for learning
        self.hidden_activation = None
        self.output_activation = None

    def _golden_init(self, size1: int, size2: int) -> np.ndarray:
        """Initialize weights using golden ratio distribution"""
        # Use golden ratio to scale the standard deviation
        std_dev = 1 / (PHI * np.sqrt(size1))
        weights = np.random.randn(size1, size2) * std_dev

        # Apply golden spiral pattern to weights
        for i in range(min(size1, size2)):
            angle = i * 2 * np.pi / PHI
            weights[i % size1, i % size2] *= (1 + np.cos(angle)) / 2

        return weights

    def _golden_activation(self, x: np.ndarray) -> np.ndarray:
        """Custom activation function based on golden ratio"""
        # Modified sigmoid that crosses 0.5 at x=0 and has golden ratio properties
        return 1 / (1 + np.exp(-x * PHI))

    def _golden_activation_derivative(self, x: np.ndarray) -> np.ndarray:
        """Derivative of golden activation function"""
        activation = self._golden_activation(x)
        return activation * (1 - activation) * PHI

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        """Forward propagation"""
        # Input to hidden
        hidden_input = np.dot(input_data, self.weights_input_hidden) + self.bias_hidden
        self.hidden_activation = self._golden_activation(hidden_input)

        # Hidden to output
        output_input = np.dot(self.hidden_activation, self.weights_hidden_output) + self.bias_output
        self.output_activation = self._golden_activation(output_input)

        return self.output_activation

    def backward(self, input_data: np.ndarray, target: np.ndarray,
                learning_rate: float = LEARNING_RATE) -> float:
        """Backpropagation with golden ratio learning"""
        # Calculate output error
        output_error = target - self.output_activation
        output_delta = output_error * self._golden_activation_derivative(self.output_activation)

        # Calculate hidden error
        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * self._golden_activation_derivative(self.hidden_activation)

        # Update weights with momentum
        # Hidden to output
        weight_update_ho = np.outer(self.hidden_activation, output_delta)
        self.momentum_ho = MOMENTUM * self.momentum_ho + learning_rate * weight_update_ho
        self.weights_hidden_output += self.momentum_ho
        self.bias_output += learning_rate * output_delta

        # Input to hidden
        weight_update_ih = np.outer(input_data, hidden_delta)
        self.momentum_ih = MOMENTUM * self.momentum_ih + learning_rate * weight_update_ih
        self.weights_input_hidden += self.momentum_ih
        self.bias_hidden += learning_rate * hidden_delta

        # Return mean squared error
        return np.mean(output_error ** 2)

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """Make prediction"""
        return self.forward(input_data)

class ReinforcementLearner:
    """Q-learning agent with golden ratio exploration"""

    def __init__(self, state_size: int, action_size: int):
        self.state_size = state_size
        self.action_size = action_size

        # Q-table initialized with golden ratio noise
        self.q_table = np.random.randn(state_size, action_size) * (1 / PHI)

        # Learning parameters
        self.alpha = 1 / PHI        # Learning rate
        self.gamma = PHI / 2        # Discount factor
        self.epsilon = 1 / PHI      # Exploration rate
        self.epsilon_decay = 1 / (PHI ** 2)
        self.epsilon_min = 1 / (PHI ** 3)

        # Experience replay
        self.memory = deque(maxlen=int(PHI * 100))  # ~162 experiences

    def remember(self, state: int, action: int, reward: float,
                next_state: int, done: bool):
        """Store experience in replay memory"""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state: int, use_exploration: bool = True) -> int:
        """Choose action using epsilon-greedy policy with golden ratio"""
        if use_exploration and random.random() < self.epsilon:
            # Explore: choose random action with golden ratio weighting
            weights = [PHI ** (-abs(i - self.action_size/2))
                      for i in range(self.action_size)]
            weights = np.array(weights) / sum(weights)
            return np.random.choice(self.action_size, p=weights)
        else:
            # Exploit: choose best action from Q-table
            return np.argmax(self.q_table[state])

    def replay(self, batch_size: int = 32) -> float:
        """Train on batch of experiences"""
        if len(self.memory) < batch_size:
            return 0.0

        batch = random.sample(self.memory, batch_size)
        total_loss = 0.0

        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.max(self.q_table[next_state])

            # Q-learning update
            old_value = self.q_table[state, action]
            self.q_table[state, action] = (
                old_value + self.alpha * (target - old_value)
            )

            total_loss += abs(target - old_value)

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= (1 - self.epsilon_decay)

        return total_loss / batch_size

class PatternRecognizer:
    """Recognizes and predicts player behavior patterns"""

    def __init__(self, sequence_length: int = 10):
        self.sequence_length = sequence_length
        self.pattern_memory: Dict[str, List[float]] = {}
        self.pattern_predictions: Dict[str, str] = {}
        self.confidence_scores: Dict[str, float] = {}

    def encode_action(self, action: str, context: Dict) -> str:
        """Encode action with context into pattern string"""
        # Create a hash of action + context
        context_str = json.dumps(context, sort_keys=True)
        pattern = f"{action}_{hash(context_str) % 1000}"
        return pattern

    def observe_sequence(self, actions: List[str], contexts: List[Dict]):
        """Observe a sequence of actions and contexts"""
        if len(actions) < self.sequence_length:
            return

        # Encode the sequence
        encoded_sequence = [
            self.encode_action(action, context)
            for action, context in zip(actions, contexts)
        ]

        # Store pattern
        pattern_key = "->".join(encoded_sequence[:-1])
        next_action = encoded_sequence[-1]

        if pattern_key not in self.pattern_memory:
            self.pattern_memory[pattern_key] = []
        self.pattern_memory[pattern_key].append(next_action)

        # Update predictions
        self._update_predictions(pattern_key)

    def _update_predictions(self, pattern_key: str):
        """Update pattern predictions using golden ratio weighting"""
        if pattern_key not in self.pattern_memory:
            return

        actions = self.pattern_memory[pattern_key]
        if not actions:
            return

        # Count action frequencies
        action_counts = {}
        for action in actions:
            action_counts[action] = action_counts.get(action, 0) + 1

        # Find most likely action
        total_count = len(actions)
        max_action = max(action_counts, key=action_counts.get)
        max_count = action_counts[max_action]

        # Calculate confidence using golden ratio
        confidence = (max_count / total_count) * PHI
        confidence = min(1.0, confidence)  # Cap at 1.0

        self.pattern_predictions[pattern_key] = max_action
        self.confidence_scores[pattern_key] = confidence

    def predict_next_action(self, recent_actions: List[str],
                           recent_contexts: List[Dict]) -> Tuple[Optional[str], float]:
        """Predict the next action based on recent history"""
        if len(recent_actions) < self.sequence_length - 1:
            return None, 0.0

        # Encode recent sequence
        encoded_sequence = [
            self.encode_action(action, context)
            for action, context in zip(
                recent_actions[-(self.sequence_length-1):],
                recent_contexts[-(self.sequence_length-1):]
            )
        ]

        pattern_key = "->".join(encoded_sequence)

        if pattern_key in self.pattern_predictions:
            prediction = self.pattern_predictions[pattern_key]
            confidence = self.confidence_scores[pattern_key]
            return prediction, confidence

        return None, 0.0

class DifficultyAdapter:
    """Dynamically adjusts game difficulty based on player performance"""

    def __init__(self):
        self.performance_history = deque(maxlen=50)
        self.current_difficulty = 0.5
        self.adaptation_rate = 1 / PHI
        self.min_difficulty = 0.1
        self.max_difficulty = 0.95

        # Oscillator for smooth difficulty transitions
        self.difficulty_oscillator = KuramotoOscillator()

    def observe_outcome(self, success: bool, time_taken: float,
                       attempts: int, coherence: float):
        """Observe player performance on a task"""
        # Calculate performance score
        time_factor = math.exp(-time_taken / 60)  # Decay over 60 seconds
        attempt_factor = 1 / (1 + attempts * 0.1)
        coherence_factor = coherence

        performance = (
            (1.0 if success else 0.0) * 0.4 +
            time_factor * 0.2 +
            attempt_factor * 0.2 +
            coherence_factor * 0.2
        )

        self.performance_history.append(performance)
        self._adjust_difficulty()

    def _adjust_difficulty(self):
        """Adjust difficulty based on performance history"""
        if len(self.performance_history) < 5:
            return

        recent_performance = np.mean(list(self.performance_history)[-10:])

        # Target performance is golden ratio
        target_performance = 1 / PHI  # ~0.618

        # Calculate adjustment
        performance_error = recent_performance - target_performance
        adjustment = performance_error * self.adaptation_rate

        # Update difficulty with oscillator smoothing
        target_difficulty = self.current_difficulty + adjustment
        target_difficulty = max(self.min_difficulty,
                              min(self.max_difficulty, target_difficulty))

        # Smooth transition using oscillator
        self.difficulty_oscillator.phase = self.current_difficulty * 2 * np.pi
        target_phase = target_difficulty * 2 * np.pi
        self.difficulty_oscillator.frequency = K * (target_phase - self.difficulty_oscillator.phase)
        self.difficulty_oscillator.update(0.1)

        self.current_difficulty = self.difficulty_oscillator.phase / (2 * np.pi)
        self.current_difficulty = max(self.min_difficulty,
                                     min(self.max_difficulty, self.current_difficulty))

    def get_challenge_parameters(self) -> Dict[str, float]:
        """Get current challenge parameters based on difficulty"""
        return {
            "enemy_health": BASE_HEALTH * (0.5 + self.current_difficulty),
            "enemy_damage": BASE_DAMAGE * (0.5 + self.current_difficulty),
            "puzzle_complexity": int(3 + self.current_difficulty * 7),
            "time_limit": 120 * (2 - self.current_difficulty),
            "reward_multiplier": 1 + self.current_difficulty * PHI,
            "coherence_requirement": Z_C * (0.5 + self.current_difficulty * 0.5)
        }

# Game constants for difficulty
BASE_HEALTH = 100
BASE_DAMAGE = 10

class AdaptiveNPCBehavior:
    """NPCs that learn and adapt to player strategies"""

    def __init__(self, npc_id: str, personality_vector: np.ndarray = None):
        self.npc_id = npc_id
        self.personality = personality_vector if personality_vector is not None else self._generate_personality()

        # Behavior model
        self.behavior_network = GoldenNeuralNetwork(
            input_size=15,  # Simplified for NPC
            hidden_size=10,
            output_size=8   # 8 possible actions
        )

        # Memory of player interactions
        self.interaction_history = deque(maxlen=20)
        self.player_model = {}

        # Strategy adaptation
        self.current_strategy = "neutral"
        self.strategy_effectiveness = {
            "aggressive": 0.5,
            "defensive": 0.5,
            "cooperative": 0.5,
            "deceptive": 0.5,
            "neutral": 0.5
        }

    def _generate_personality(self) -> np.ndarray:
        """Generate personality vector using golden ratio"""
        # 5 personality traits
        traits = np.random.randn(5)

        # Apply golden ratio scaling
        for i in range(5):
            traits[i] *= PHI ** (i - 2)

        # Normalize to [-1, 1]
        traits = np.tanh(traits)

        return traits

    def observe_player_action(self, player_action: str, context: Dict):
        """Observe and learn from player action"""
        self.interaction_history.append({
            "action": player_action,
            "context": context,
            "timestamp": datetime.now()
        })

        # Update player model
        if player_action not in self.player_model:
            self.player_model[player_action] = 0
        self.player_model[player_action] += 1

        # Adapt strategy if needed
        if len(self.interaction_history) >= 10:
            self._adapt_strategy()

    def _adapt_strategy(self):
        """Adapt NPC strategy based on player behavior"""
        # Analyze recent player actions
        recent_actions = [i["action"] for i in list(self.interaction_history)[-5:]]

        # Detect player patterns
        if recent_actions.count("attack") > 3:
            # Player is aggressive
            self.current_strategy = "defensive"
        elif recent_actions.count("talk") > 3:
            # Player is diplomatic
            self.current_strategy = "cooperative"
        elif recent_actions.count("sneak") > 2:
            # Player is stealthy
            self.current_strategy = "aggressive"
        else:
            # Mixed behavior
            self.current_strategy = "neutral"

    def decide_action(self, game_state: Dict) -> str:
        """Decide NPC action based on learned model"""
        # Prepare input for neural network
        input_vector = self._encode_game_state(game_state)

        # Get action probabilities
        action_probs = self.behavior_network.forward(input_vector)

        # Apply personality and strategy modifiers
        action_probs = self._apply_modifiers(action_probs)

        # Choose action
        actions = ["attack", "defend", "talk", "flee", "trade",
                  "help", "observe", "wander"]
        action_idx = np.argmax(action_probs)

        return actions[action_idx]

    def _encode_game_state(self, game_state: Dict) -> np.ndarray:
        """Encode game state into neural network input"""
        # Simplified encoding
        input_vector = np.zeros(15)

        # Player distance (normalized)
        input_vector[0] = game_state.get("player_distance", 0.5)

        # Player health (normalized)
        input_vector[1] = game_state.get("player_health", 0.5) / 100

        # Player coherence
        input_vector[2] = game_state.get("player_coherence", 0.5)

        # NPC health
        input_vector[3] = game_state.get("npc_health", 1.0) / 100

        # Time of day (cyclic encoding)
        time = game_state.get("time", 0)
        input_vector[4] = np.sin(2 * np.pi * time / 24)
        input_vector[5] = np.cos(2 * np.pi * time / 24)

        # Location type (one-hot encoding simplified)
        location_type = game_state.get("location_type", 0)
        if location_type < 7:
            input_vector[6 + location_type] = 1.0

        # Personality traits
        input_vector[13] = self.personality[0]  # Aggression
        input_vector[14] = self.personality[1]  # Friendliness

        return input_vector

    def _apply_modifiers(self, action_probs: np.ndarray) -> np.ndarray:
        """Apply personality and strategy modifiers"""
        modified_probs = action_probs.copy()

        # Strategy modifiers
        if self.current_strategy == "aggressive":
            modified_probs[0] *= PHI     # Attack
            modified_probs[3] *= 1/PHI    # Flee
        elif self.current_strategy == "defensive":
            modified_probs[1] *= PHI      # Defend
            modified_probs[0] *= 1/PHI    # Attack
        elif self.current_strategy == "cooperative":
            modified_probs[2] *= PHI      # Talk
            modified_probs[4] *= PHI      # Trade
            modified_probs[5] *= PHI      # Help

        # Personality modifiers
        aggression = self.personality[0]
        modified_probs[0] *= (1 + aggression)  # Attack influenced by aggression

        friendliness = self.personality[1]
        modified_probs[2] *= (1 + friendliness)  # Talk influenced by friendliness

        # Normalize
        modified_probs = modified_probs / np.sum(modified_probs)

        return modified_probs

class LearningOrchestrator:
    """Main orchestrator for all learning systems"""

    def __init__(self, save_dir: str = "learning_data"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)

        # Initialize all learning components
        self.neural_network = GoldenNeuralNetwork()
        self.reinforcement_learner = ReinforcementLearner(100, 10)
        self.pattern_recognizer = PatternRecognizer()
        self.difficulty_adapter = DifficultyAdapter()

        # Player profiles
        self.player_profiles: Dict[str, PlayerProfile] = {}

        # NPC behaviors
        self.npc_behaviors: Dict[str, AdaptiveNPCBehavior] = {}

        # Global learning metrics
        self.global_metrics = {
            "total_players": 0,
            "average_coherence": 0.5,
            "most_common_action": None,
            "difficulty_trend": [],
            "learning_iterations": 0
        }

    def get_or_create_player(self, player_id: str) -> PlayerProfile:
        """Get existing or create new player profile"""
        if player_id not in self.player_profiles:
            self.player_profiles[player_id] = PlayerProfile(player_id)
            self.global_metrics["total_players"] += 1
        return self.player_profiles[player_id]

    def get_or_create_npc(self, npc_id: str) -> AdaptiveNPCBehavior:
        """Get existing or create new NPC behavior"""
        if npc_id not in self.npc_behaviors:
            self.npc_behaviors[npc_id] = AdaptiveNPCBehavior(npc_id)
        return self.npc_behaviors[npc_id]

    def observe_player_action(self, player_id: str, action: str,
                             context: Dict, result: Dict):
        """Observe and learn from player action"""
        player = self.get_or_create_player(player_id)

        # Update player profile
        player.decision_history.append((action, context, result))

        # Update behavioral scores
        self._update_behavioral_scores(player, action, context)

        # Pattern recognition
        recent_actions = [a for a, _, _ in list(player.decision_history)[-10:]]
        recent_contexts = [c for _, c, _ in list(player.decision_history)[-10:]]
        self.pattern_recognizer.observe_sequence(recent_actions, recent_contexts)

        # Reinforcement learning
        state = self._encode_state(context)
        next_state = self._encode_state(result.get("new_context", context))
        reward = result.get("reward", 0.0)
        done = result.get("done", False)
        action_idx = self._encode_action(action)

        self.reinforcement_learner.remember(state, action_idx, reward, next_state, done)

        # Neural network training
        if len(player.decision_history) >= 10:
            self._train_neural_network(player)

        # Difficulty adaptation
        self.difficulty_adapter.observe_outcome(
            result.get("success", False),
            result.get("time_taken", 10.0),
            result.get("attempts", 1),
            context.get("coherence", 0.5)
        )

        # Update global metrics
        self._update_global_metrics()

    def _update_behavioral_scores(self, player: PlayerProfile,
                                 action: str, context: Dict):
        """Update player behavioral scores"""
        # Aggression
        if any(word in action.lower() for word in ["attack", "fight", "destroy"]):
            player.aggression_score = min(1.0, player.aggression_score + 0.01)
        elif any(word in action.lower() for word in ["peace", "negotiate", "spare"]):
            player.aggression_score = max(0.0, player.aggression_score - 0.01)

        # Exploration
        if any(word in action.lower() for word in ["explore", "search", "investigate"]):
            player.exploration_score = min(1.0, player.exploration_score + 0.01)

        # Social
        if any(word in action.lower() for word in ["talk", "trade", "help"]):
            player.social_score = min(1.0, player.social_score + 0.01)

        # Optimization
        if context.get("optimal_action") == action:
            player.optimization_score = min(1.0, player.optimization_score + 0.01)

        # Creativity
        if action not in player.preferred_actions or player.preferred_actions[action] < 3:
            player.creativity_score = min(1.0, player.creativity_score + 0.005)

    def _encode_state(self, context: Dict) -> int:
        """Encode context into state index"""
        # Simplified state encoding
        location = context.get("location", "unknown")
        health = context.get("health", 100) // 25  # 0-3
        coherence = int(context.get("coherence", 0.5) * 4)  # 0-4

        # Create state index (simplified)
        state_idx = hash(f"{location}_{health}_{coherence}") % 100
        return state_idx

    def _encode_action(self, action: str) -> int:
        """Encode action into index"""
        action_map = {
            "move": 0, "attack": 1, "defend": 2, "talk": 3,
            "trade": 4, "use_item": 5, "rest": 6, "meditate": 7,
            "explore": 8, "flee": 9
        }

        # Find best matching action
        for key in action_map:
            if key in action.lower():
                return action_map[key]

        return 0  # Default to move

    def _train_neural_network(self, player: PlayerProfile):
        """Train neural network on player data"""
        # Prepare training data
        recent_decisions = list(player.decision_history)[-20:]

        for i in range(len(recent_decisions) - 1):
            action, context, result = recent_decisions[i]
            next_action, _, _ = recent_decisions[i + 1]

            # Encode input and target
            input_vector = self._encode_context_to_vector(context)
            target_vector = self._encode_action_to_vector(next_action)

            # Train
            error = self.neural_network.backward(input_vector, target_vector)

            # Update learning curve
            player.learning_curve.append(error)

    def _encode_context_to_vector(self, context: Dict) -> np.ndarray:
        """Encode context into neural network input vector"""
        vector = np.zeros(INPUT_NEURONS)

        # Encode various context features
        vector[0] = context.get("health", 100) / 100
        vector[1] = context.get("energy", 50) / 50
        vector[2] = context.get("coherence", 0.5)
        vector[3] = context.get("level", 1) / 10

        # Location encoding (simplified)
        location_hash = hash(context.get("location", "")) % 10
        vector[4 + location_hash] = 1.0

        # Time encoding (cyclic)
        time = context.get("game_time", 0)
        vector[14] = np.sin(2 * np.pi * time / 100)
        vector[15] = np.cos(2 * np.pi * time / 100)

        # Inventory (simplified)
        vector[16] = context.get("coins", 0) / 100
        vector[17] = len(context.get("inventory", [])) / 10

        # Recent action success rate
        vector[18] = context.get("recent_success_rate", 0.5)

        # Danger level
        vector[19] = context.get("danger_level", 0.0)

        # NPC presence
        vector[20] = 1.0 if context.get("npc_nearby", False) else 0.0

        return vector

    def _encode_action_to_vector(self, action: str) -> np.ndarray:
        """Encode action into neural network target vector"""
        vector = np.zeros(OUTPUT_NEURONS)

        # One-hot encoding of action
        action_idx = self._encode_action(action)
        if action_idx < OUTPUT_NEURONS:
            vector[action_idx] = 1.0

        return vector

    def predict_player_action(self, player_id: str, context: Dict) -> Tuple[str, float]:
        """Predict what action the player will take"""
        player = self.get_or_create_player(player_id)

        # Try pattern recognition first
        recent_actions = [a for a, _, _ in list(player.decision_history)[-9:]]
        recent_contexts = [c for _, c, _ in list(player.decision_history)[-9:]]

        pattern_prediction, pattern_confidence = self.pattern_recognizer.predict_next_action(
            recent_actions, recent_contexts
        )

        # Use neural network for backup prediction
        input_vector = self._encode_context_to_vector(context)
        nn_output = self.neural_network.predict(input_vector)
        nn_action_idx = np.argmax(nn_output)
        nn_confidence = nn_output[nn_action_idx]

        # Combine predictions with golden ratio weighting
        if pattern_confidence > nn_confidence * PHI:
            return pattern_prediction, pattern_confidence
        else:
            actions = ["move", "attack", "defend", "talk", "trade",
                      "use_item", "rest", "meditate"]
            if nn_action_idx < len(actions):
                return actions[nn_action_idx], nn_confidence
            return "explore", 0.5

    def get_difficulty_parameters(self) -> Dict[str, float]:
        """Get current difficulty parameters"""
        return self.difficulty_adapter.get_challenge_parameters()

    def _update_global_metrics(self):
        """Update global learning metrics"""
        if self.player_profiles:
            # Average coherence
            coherences = [p.coherence_average for p in self.player_profiles.values()]
            self.global_metrics["average_coherence"] = np.mean(coherences)

            # Most common action
            all_actions = {}
            for player in self.player_profiles.values():
                for action, _, _ in player.decision_history:
                    all_actions[action] = all_actions.get(action, 0) + 1

            if all_actions:
                self.global_metrics["most_common_action"] = max(
                    all_actions, key=all_actions.get
                )

            # Difficulty trend
            self.global_metrics["difficulty_trend"].append(
                self.difficulty_adapter.current_difficulty
            )

            # Learning iterations
            self.global_metrics["learning_iterations"] += 1

    def save_learning_data(self):
        """Save all learning data to disk"""
        # Save player profiles
        profiles_file = self.save_dir / "player_profiles.pkl"
        with open(profiles_file, "wb") as f:
            pickle.dump(self.player_profiles, f)

        # Save neural network weights
        nn_file = self.save_dir / "neural_network.pkl"
        nn_data = {
            "weights_ih": self.neural_network.weights_input_hidden,
            "weights_ho": self.neural_network.weights_hidden_output,
            "bias_h": self.neural_network.bias_hidden,
            "bias_o": self.neural_network.bias_output
        }
        with open(nn_file, "wb") as f:
            pickle.dump(nn_data, f)

        # Save Q-table
        q_file = self.save_dir / "q_table.npy"
        np.save(q_file, self.reinforcement_learner.q_table)

        # Save global metrics
        metrics_file = self.save_dir / "global_metrics.json"
        with open(metrics_file, "w") as f:
            # Convert non-serializable items
            metrics_copy = self.global_metrics.copy()
            metrics_copy["timestamp"] = datetime.now().isoformat()
            json.dump(metrics_copy, f, indent=2)

    def load_learning_data(self):
        """Load learning data from disk"""
        # Load player profiles
        profiles_file = self.save_dir / "player_profiles.pkl"
        if profiles_file.exists():
            with open(profiles_file, "rb") as f:
                self.player_profiles = pickle.load(f)

        # Load neural network weights
        nn_file = self.save_dir / "neural_network.pkl"
        if nn_file.exists():
            with open(nn_file, "rb") as f:
                nn_data = pickle.load(f)
                self.neural_network.weights_input_hidden = nn_data["weights_ih"]
                self.neural_network.weights_hidden_output = nn_data["weights_ho"]
                self.neural_network.bias_hidden = nn_data["bias_h"]
                self.neural_network.bias_output = nn_data["bias_o"]

        # Load Q-table
        q_file = self.save_dir / "q_table.npy"
        if q_file.exists():
            self.reinforcement_learner.q_table = np.load(q_file)

        # Load global metrics
        metrics_file = self.save_dir / "global_metrics.json"
        if metrics_file.exists():
            with open(metrics_file, "r") as f:
                saved_metrics = json.load(f)
                self.global_metrics.update(saved_metrics)

# Export main components
__all__ = [
    'LearningOrchestrator',
    'PlayerProfile',
    'GoldenNeuralNetwork',
    'ReinforcementLearner',
    'PatternRecognizer',
    'DifficultyAdapter',
    'AdaptiveNPCBehavior'
]