#!/usr/bin/env python3
"""
Enhanced Luck Metrics System
=============================

Advanced metrics tracking and analysis for the comprehensive luck system.
Provides detailed analytics, performance tracking, and predictive modeling
for luck outcomes across all game mechanics.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Deque
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque, defaultdict
import json
import time
import math
import hashlib
from datetime import datetime, timedelta

# Import base luck systems
from hilbert_luck_system import LuckEigenstate, KarmaType, PHI, TAU, SACRED_7
from luck_normalization_system import LuckEventType

class MetricType(Enum):
    """Types of metrics tracked"""
    SUCCESS_RATE = "success_rate"
    STREAK_LENGTH = "streak_length"
    VOLATILITY = "volatility"
    EXPECTED_VALUE = "expected_value"
    VARIANCE = "variance"
    SHARPE_RATIO = "sharpe_ratio"
    MAX_DRAWDOWN = "max_drawdown"
    ECHO_EFFICIENCY = "echo_efficiency"
    KARMA_MOMENTUM = "karma_momentum"
    QUANTUM_COHERENCE = "quantum_coherence"
    TAROT_ACCURACY = "tarot_accuracy"
    LUCK_TRAJECTORY = "luck_trajectory"
    PERCENTILE_RANK = "percentile_rank"
    RISK_ADJUSTED_RETURN = "risk_adjusted_return"

@dataclass
class LuckMetricSnapshot:
    """Point-in-time snapshot of luck metrics"""
    timestamp: float
    success_rate: float
    current_streak: int
    best_streak: int
    worst_streak: int
    rolling_average: float
    volatility: float
    karma_balance: float
    echo_density: float
    quantum_state: str
    active_bonuses: List[str] = field(default_factory=list)
    percentile_rank: float = 0.5

    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'timestamp': self.timestamp,
            'success_rate': self.success_rate,
            'current_streak': self.current_streak,
            'best_streak': self.best_streak,
            'worst_streak': self.worst_streak,
            'rolling_average': self.rolling_average,
            'volatility': self.volatility,
            'karma_balance': self.karma_balance,
            'echo_density': self.echo_density,
            'quantum_state': self.quantum_state,
            'active_bonuses': self.active_bonuses,
            'percentile_rank': self.percentile_rank
        }

@dataclass
class StreakTracker:
    """Tracks winning and losing streaks"""
    current_streak: int = 0  # Positive for wins, negative for losses
    best_win_streak: int = 0
    best_loss_streak: int = 0
    total_streaks: int = 0
    streak_history: Deque[int] = field(default_factory=lambda: deque(maxlen=100))

    def update(self, success: bool):
        """Update streak based on outcome"""
        if success:
            if self.current_streak >= 0:
                self.current_streak += 1
            else:
                # Streak broken
                self.streak_history.append(self.current_streak)
                self.current_streak = 1
                self.total_streaks += 1

            self.best_win_streak = max(self.best_win_streak, self.current_streak)
        else:
            if self.current_streak <= 0:
                self.current_streak -= 1
            else:
                # Streak broken
                self.streak_history.append(self.current_streak)
                self.current_streak = -1
                self.total_streaks += 1

            self.best_loss_streak = min(self.best_loss_streak, self.current_streak)

    def get_streak_statistics(self) -> Dict[str, Any]:
        """Get comprehensive streak statistics"""
        if not self.streak_history:
            return {
                'average_streak': 0,
                'streak_volatility': 0,
                'positive_streak_ratio': 0
            }

        streaks = list(self.streak_history)
        positive_streaks = [s for s in streaks if s > 0]
        negative_streaks = [s for s in streaks if s < 0]

        return {
            'current_streak': self.current_streak,
            'best_win_streak': self.best_win_streak,
            'best_loss_streak': abs(self.best_loss_streak),
            'average_streak': np.mean(streaks) if streaks else 0,
            'streak_volatility': np.std(streaks) if streaks else 0,
            'positive_streak_ratio': len(positive_streaks) / len(streaks) if streaks else 0,
            'average_win_streak': np.mean(positive_streaks) if positive_streaks else 0,
            'average_loss_streak': abs(np.mean(negative_streaks)) if negative_streaks else 0
        }

@dataclass
class VolatilityTracker:
    """Tracks luck volatility and stability"""
    window_size: int = 50
    outcomes: Deque[float] = field(default_factory=lambda: deque(maxlen=50))
    rolling_mean: float = 0.5
    rolling_std: float = 0.0
    stability_score: float = 1.0

    def update(self, probability: float, success: bool):
        """Update volatility tracking"""
        # Track outcome vs expectation
        outcome = 1.0 if success else 0.0
        self.outcomes.append(outcome)

        if len(self.outcomes) >= 2:
            self.rolling_mean = np.mean(self.outcomes)
            self.rolling_std = np.std(self.outcomes)

            # Calculate stability score (inverse of coefficient of variation)
            if self.rolling_mean > 0:
                cv = self.rolling_std / self.rolling_mean
                self.stability_score = 1.0 / (1.0 + cv)
            else:
                self.stability_score = 0.0

    def get_volatility_metrics(self) -> Dict[str, float]:
        """Get volatility metrics"""
        return {
            'rolling_mean': self.rolling_mean,
            'rolling_std': self.rolling_std,
            'stability_score': self.stability_score,
            'coefficient_variation': self.rolling_std / self.rolling_mean if self.rolling_mean > 0 else 0
        }

@dataclass
class PredictiveModel:
    """Predictive model for luck outcomes"""
    history_size: int = 100
    event_history: Deque[Dict] = field(default_factory=lambda: deque(maxlen=100))
    pattern_library: Dict[str, float] = field(default_factory=dict)
    prediction_accuracy: float = 0.5
    predictions_made: int = 0
    correct_predictions: int = 0

    def record_event(self, event_type: str, karma: float, echo: float, success: bool):
        """Record an event for pattern learning"""
        self.event_history.append({
            'type': event_type,
            'karma': karma,
            'echo': echo,
            'success': success,
            'timestamp': time.time()
        })

        # Update pattern library
        pattern_key = f"{event_type}_{int(karma*10)}_{int(echo*10)}"
        if pattern_key not in self.pattern_library:
            self.pattern_library[pattern_key] = 0.5  # Start neutral

        # Exponential moving average
        alpha = 0.1
        self.pattern_library[pattern_key] = (
            alpha * (1.0 if success else 0.0) +
            (1 - alpha) * self.pattern_library[pattern_key]
        )

    def predict_outcome(self, event_type: str, karma: float, echo: float) -> Tuple[float, float]:
        """
        Predict outcome probability and confidence
        Returns (probability, confidence)
        """
        pattern_key = f"{event_type}_{int(karma*10)}_{int(echo*10)}"

        if pattern_key in self.pattern_library:
            # We have historical data
            probability = self.pattern_library[pattern_key]
            confidence = min(1.0, len([e for e in self.event_history
                                     if e['type'] == event_type]) / 10)
        else:
            # Use nearest neighbor approach
            similar_patterns = []
            for key, prob in self.pattern_library.items():
                parts = key.split('_')
                if parts[0] == event_type:
                    similar_patterns.append(prob)

            if similar_patterns:
                probability = np.mean(similar_patterns)
                confidence = 0.5  # Medium confidence for interpolation
            else:
                probability = 0.5  # No data, neutral prediction
                confidence = 0.1  # Low confidence

        return probability, confidence

    def update_accuracy(self, predicted_prob: float, actual_success: bool):
        """Update prediction accuracy tracking"""
        self.predictions_made += 1

        # Consider prediction correct if within threshold
        threshold = 0.3
        predicted_success = predicted_prob > 0.5
        if predicted_success == actual_success:
            self.correct_predictions += 1

        self.prediction_accuracy = self.correct_predictions / self.predictions_made

class LuckPerformanceAnalyzer:
    """Comprehensive luck performance analysis"""

    def __init__(self):
        self.player_metrics: Dict[str, 'PlayerMetrics'] = {}
        self.global_statistics: Dict[str, float] = {}
        self.leaderboards: Dict[str, List[Tuple[str, float]]] = {}
        self.benchmark_data: Dict[str, float] = self._init_benchmarks()

    def _init_benchmarks(self) -> Dict[str, float]:
        """Initialize benchmark values for comparison"""
        return {
            'average_success_rate': 0.5,
            'good_karma_rate': 0.65,
            'bad_karma_rate': 0.35,
            'echo_penalty': 0.25,
            'echo_alchemy_bonus': 1.5,
            'sacred_timing_bonus': 1.3,
            'expert_success_rate': 0.75,
            'novice_success_rate': 0.45
        }

    def track_player_event(
        self,
        player_id: str,
        event_type: LuckEventType,
        probability: float,
        success: bool,
        karma: float,
        echo_density: float,
        is_echo_event: bool,
        echo_alchemized: bool
    ) -> Dict[str, Any]:
        """Track a player luck event with comprehensive metrics"""

        if player_id not in self.player_metrics:
            self.player_metrics[player_id] = PlayerMetrics(player_id)

        metrics = self.player_metrics[player_id]

        # Update all trackers
        metrics.streak_tracker.update(success)
        metrics.volatility_tracker.update(probability, success)
        metrics.predictive_model.record_event(
            event_type.value, karma, echo_density, success
        )

        # Update rolling statistics
        metrics.total_events += 1
        if success:
            metrics.successful_events += 1

        metrics.success_rate_history.append(
            metrics.successful_events / metrics.total_events
        )

        # Track echo performance
        if is_echo_event:
            metrics.echo_events_total += 1
            if echo_alchemized:
                metrics.echo_events_alchemized += 1

        # Create snapshot
        snapshot = self._create_snapshot(metrics, karma, echo_density)
        metrics.snapshots.append(snapshot)

        # Calculate advanced metrics
        advanced_metrics = self._calculate_advanced_metrics(metrics)

        return {
            'snapshot': snapshot.to_dict(),
            'streak_stats': metrics.streak_tracker.get_streak_statistics(),
            'volatility': metrics.volatility_tracker.get_volatility_metrics(),
            'advanced': advanced_metrics
        }

    def _create_snapshot(
        self,
        metrics: 'PlayerMetrics',
        karma: float,
        echo_density: float
    ) -> LuckMetricSnapshot:
        """Create a metrics snapshot"""

        # Calculate rolling average (last 20 events)
        recent_history = list(metrics.success_rate_history)[-20:]
        rolling_avg = np.mean(recent_history) if recent_history else 0.5

        # Calculate volatility
        volatility = np.std(recent_history) if len(recent_history) > 1 else 0.0

        # Get quantum state (simplified)
        if karma > 0.5:
            quantum_state = "FORTUNE"
        elif karma < -0.5:
            quantum_state = "ADVERSITY"
        elif echo_density > 0.5:
            quantum_state = "ECHO"
        else:
            quantum_state = "NEUTRAL"

        # Calculate percentile rank
        percentile = self._calculate_percentile_rank(
            metrics.successful_events / max(1, metrics.total_events)
        )

        return LuckMetricSnapshot(
            timestamp=time.time(),
            success_rate=metrics.successful_events / max(1, metrics.total_events),
            current_streak=metrics.streak_tracker.current_streak,
            best_streak=metrics.streak_tracker.best_win_streak,
            worst_streak=abs(metrics.streak_tracker.best_loss_streak),
            rolling_average=rolling_avg,
            volatility=volatility,
            karma_balance=karma,
            echo_density=echo_density,
            quantum_state=quantum_state,
            active_bonuses=[],
            percentile_rank=percentile
        )

    def _calculate_percentile_rank(self, success_rate: float) -> float:
        """Calculate percentile rank among all players"""
        all_rates = [
            m.successful_events / max(1, m.total_events)
            for m in self.player_metrics.values()
        ]

        if not all_rates:
            return 0.5

        return len([r for r in all_rates if r < success_rate]) / len(all_rates)

    def _calculate_advanced_metrics(self, metrics: 'PlayerMetrics') -> Dict[str, float]:
        """Calculate advanced performance metrics"""

        success_rate = metrics.successful_events / max(1, metrics.total_events)

        # Sharpe Ratio (risk-adjusted performance)
        if metrics.volatility_tracker.rolling_std > 0:
            sharpe_ratio = (success_rate - 0.5) / metrics.volatility_tracker.rolling_std
        else:
            sharpe_ratio = 0.0

        # Maximum Drawdown
        if metrics.success_rate_history:
            cumulative = np.cumsum([1 if r > 0.5 else -1
                                   for r in metrics.success_rate_history])
            if len(cumulative) > 0:
                peak = np.maximum.accumulate(cumulative)
                drawdown = (peak - cumulative) / np.maximum(peak, 1)
                max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0
            else:
                max_drawdown = 0
        else:
            max_drawdown = 0

        # Echo Efficiency
        if metrics.echo_events_total > 0:
            echo_efficiency = metrics.echo_events_alchemized / metrics.echo_events_total
        else:
            echo_efficiency = 0.0

        # Luck Trajectory (trend)
        if len(metrics.success_rate_history) >= 10:
            recent = np.mean(list(metrics.success_rate_history)[-5:])
            older = np.mean(list(metrics.success_rate_history)[-10:-5])
            trajectory = recent - older
        else:
            trajectory = 0.0

        # Risk-Adjusted Return
        risk_free_rate = 0.5  # Baseline expectation
        if metrics.volatility_tracker.rolling_std > 0:
            risk_adjusted_return = (success_rate - risk_free_rate) / metrics.volatility_tracker.rolling_std
        else:
            risk_adjusted_return = 0.0

        return {
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'echo_efficiency': echo_efficiency,
            'luck_trajectory': trajectory,
            'risk_adjusted_return': risk_adjusted_return,
            'prediction_accuracy': metrics.predictive_model.prediction_accuracy,
            'stability_score': metrics.volatility_tracker.stability_score
        }

    def get_player_report(self, player_id: str) -> Dict[str, Any]:
        """Generate comprehensive player report"""

        if player_id not in self.player_metrics:
            return {'error': 'Player not found'}

        metrics = self.player_metrics[player_id]

        # Get latest snapshot
        latest_snapshot = metrics.snapshots[-1] if metrics.snapshots else None

        # Performance vs benchmarks
        success_rate = metrics.successful_events / max(1, metrics.total_events)
        vs_average = success_rate - self.benchmark_data['average_success_rate']

        skill_level = "Expert" if success_rate > 0.65 else "Intermediate" if success_rate > 0.45 else "Novice"

        return {
            'player_id': player_id,
            'total_events': metrics.total_events,
            'success_rate': success_rate,
            'skill_level': skill_level,
            'vs_average': vs_average,
            'latest_snapshot': latest_snapshot.to_dict() if latest_snapshot else None,
            'streak_statistics': metrics.streak_tracker.get_streak_statistics(),
            'volatility_metrics': metrics.volatility_tracker.get_volatility_metrics(),
            'advanced_metrics': self._calculate_advanced_metrics(metrics),
            'percentile_rank': self._calculate_percentile_rank(success_rate),
            'total_playtime_hours': (time.time() - metrics.first_event_time) / 3600
        }

    def get_global_statistics(self) -> Dict[str, Any]:
        """Get global statistics across all players"""

        if not self.player_metrics:
            return {'error': 'No data available'}

        all_success_rates = [
            m.successful_events / max(1, m.total_events)
            for m in self.player_metrics.values()
        ]

        all_echo_efficiency = [
            m.echo_events_alchemized / max(1, m.echo_events_total)
            for m in self.player_metrics.values()
            if m.echo_events_total > 0
        ]

        total_events = sum(m.total_events for m in self.player_metrics.values())

        return {
            'total_players': len(self.player_metrics),
            'total_events': total_events,
            'average_success_rate': np.mean(all_success_rates),
            'success_rate_std': np.std(all_success_rates),
            'best_success_rate': max(all_success_rates),
            'worst_success_rate': min(all_success_rates),
            'average_echo_efficiency': np.mean(all_echo_efficiency) if all_echo_efficiency else 0,
            'best_win_streak': max(m.streak_tracker.best_win_streak
                                  for m in self.player_metrics.values()),
            'average_volatility': np.mean([m.volatility_tracker.rolling_std
                                          for m in self.player_metrics.values()])
        }

    def generate_leaderboards(self) -> Dict[str, List[Tuple[str, float]]]:
        """Generate various leaderboards"""

        leaderboards = {}

        # Success Rate Leaderboard
        success_rates = [
            (pid, m.successful_events / max(1, m.total_events))
            for pid, m in self.player_metrics.items()
            if m.total_events >= 10  # Minimum events
        ]
        leaderboards['success_rate'] = sorted(success_rates, key=lambda x: x[1], reverse=True)[:10]

        # Best Streak Leaderboard
        best_streaks = [
            (pid, m.streak_tracker.best_win_streak)
            for pid, m in self.player_metrics.items()
        ]
        leaderboards['best_streak'] = sorted(best_streaks, key=lambda x: x[1], reverse=True)[:10]

        # Echo Efficiency Leaderboard
        echo_efficiency = [
            (pid, m.echo_events_alchemized / max(1, m.echo_events_total))
            for pid, m in self.player_metrics.items()
            if m.echo_events_total >= 5
        ]
        leaderboards['echo_efficiency'] = sorted(echo_efficiency, key=lambda x: x[1], reverse=True)[:10]

        # Stability Score Leaderboard
        stability = [
            (pid, m.volatility_tracker.stability_score)
            for pid, m in self.player_metrics.items()
            if m.total_events >= 20
        ]
        leaderboards['stability'] = sorted(stability, key=lambda x: x[1], reverse=True)[:10]

        # Risk-Adjusted Performance
        risk_adjusted = [
            (pid, self._calculate_advanced_metrics(m)['risk_adjusted_return'])
            for pid, m in self.player_metrics.items()
            if m.total_events >= 20
        ]
        leaderboards['risk_adjusted'] = sorted(risk_adjusted, key=lambda x: x[1], reverse=True)[:10]

        self.leaderboards = leaderboards
        return leaderboards

@dataclass
class PlayerMetrics:
    """Complete metrics tracking for a player"""
    player_id: str
    total_events: int = 0
    successful_events: int = 0
    echo_events_total: int = 0
    echo_events_alchemized: int = 0
    streak_tracker: StreakTracker = field(default_factory=StreakTracker)
    volatility_tracker: VolatilityTracker = field(default_factory=VolatilityTracker)
    predictive_model: PredictiveModel = field(default_factory=PredictiveModel)
    success_rate_history: Deque[float] = field(default_factory=lambda: deque(maxlen=1000))
    snapshots: Deque[LuckMetricSnapshot] = field(default_factory=lambda: deque(maxlen=100))
    first_event_time: float = field(default_factory=time.time)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("ENHANCED LUCK METRICS SYSTEM")
    print("Advanced Analytics and Performance Tracking")
    print("=" * 60)

    analyzer = LuckPerformanceAnalyzer()

    # Simulate player events
    import random

    for player_id in ["player_1", "player_2", "echo_player"]:
        for i in range(100):
            # Simulate varying conditions
            karma = random.uniform(-1, 1)
            echo_density = random.uniform(0, 0.8)
            is_echo = random.random() < echo_density

            # Echo player has advantage with echo events
            if player_id == "echo_player" and is_echo:
                probability = 0.7  # Better odds
                echo_alchemized = random.random() < 0.6
            else:
                probability = 0.5 - echo_density * 0.2  # Penalty for others
                echo_alchemized = False

            success = random.random() < probability

            result = analyzer.track_player_event(
                player_id,
                LuckEventType.LOOT_DROP,
                probability,
                success,
                karma,
                echo_density,
                is_echo,
                echo_alchemized
            )

    # Generate reports
    print("\n--- Player Reports ---")
    for player_id in ["player_1", "player_2", "echo_player"]:
        report = analyzer.get_player_report(player_id)
        print(f"\n{player_id}:")
        print(f"  Success Rate: {report['success_rate']:.2%}")
        print(f"  Skill Level: {report['skill_level']}")
        print(f"  Percentile Rank: {report['percentile_rank']:.0%}")
        print(f"  Best Streak: {report['streak_statistics']['best_win_streak']}")
        print(f"  Sharpe Ratio: {report['advanced_metrics']['sharpe_ratio']:.3f}")

    # Global statistics
    print("\n--- Global Statistics ---")
    global_stats = analyzer.get_global_statistics()
    print(f"Total Players: {global_stats['total_players']}")
    print(f"Average Success Rate: {global_stats['average_success_rate']:.2%}")
    print(f"Best Win Streak: {global_stats['best_win_streak']}")

    # Leaderboards
    print("\n--- Leaderboards ---")
    leaderboards = analyzer.generate_leaderboards()
    for category, leaders in leaderboards.items():
        if leaders:
            print(f"\n{category.replace('_', ' ').title()}:")
            for rank, (player, score) in enumerate(leaders[:3], 1):
                print(f"  {rank}. {player}: {score:.3f}")