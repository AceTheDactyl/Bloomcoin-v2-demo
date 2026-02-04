# 🌺 BloomQuest: Mythic Economy - Unified Game System

## Overview
BloomQuest Unified combines all game systems into a complete PHI-based adventure experience:
- **Mythical Item Discovery** in exploration spaces
- **Job/Archetype System** with branching narratives
- **LLM Companion System** that evolves through guardian cycles
- **Recipe/Pattern Crafting** to feed companions
- **Card-Based Battle System** inspired by golden acorn mechanics
- **BloomCoin Economy** driven by the golden ratio

## 🎮 How to Play

### Quick Start
```bash
python3 launch_unified.py
```

Or for the simplified demo:
```bash
python3 bloomquest_demo.py
```

### Full Version
```bash
python3 bloomquest_unified.py
```

## 🌟 Game Systems

### 1. Character Creation & Archetypes
Choose from 6 job archetypes, each with unique playstyles:

- **Seeker**: Cosmic exploration, high discovery rates
- **Forger**: Garden affinity, crafting bonuses
- **Voidwalker**: Abyssal mastery, shadow powers
- **Gardener**: Growth patterns, resource generation
- **Scribe**: Knowledge accumulation, pattern recognition
- **Herald**: Balance between territories, diplomatic advantages

### 2. Exploration & Item Discovery
Explore 5 mystical locations:
- **Crystal Caves**: Resonant frequencies, mineral wealth
- **Phoenix Nest**: Rebirth cycles, flame patterns
- **Void Market**: Shadow trades, hidden knowledge
- **Garden Heart**: Living patterns, growth essence
- **Library Infinite**: Encoded wisdom, pattern archives

Discovery chance = `0.3 + (coherence * 0.2)`

### 3. LLM Companion Evolution
Your companion evolves through guardian cycles:
- Absorbs patterns from crafted recipes
- Levels up every 5 patterns absorbed
- Provides contextual wisdom based on current guardian
- Cycles through 19 unique guardians across 3 territories

### 4. Recipe & Pattern Crafting
Combine mythical items to create patterns:
- **Resonance Pattern**: 2 Cosmic items → Frequency alignment
- **Growth Pattern**: 2 Garden items → Life essence
- **Depth Pattern**: 2 Abyssal items → Shadow knowledge
- **Harmony Pattern**: Mixed items → Universal balance

Feed patterns to your companion for evolution!

### 5. Card Battle System
Strategic card battles with territory mechanics:

**Card Structure:**
- 9 Suits across 3 Territories
- 14 Ranks (Ace to Fractal)
- Power = `rank_value * PHI * suit_multiplier * coherence`

**Battle Phases:**
1. IGNITION (turns 1-2)
2. RESONANCE (turns 3-5)
3. MANIA (turns 6-8)
4. NIRVANA (turns 9-11)
5. TRANSMISSION (turns 12-14)
6. RESOLUTION (turn 15+)

### 6. BloomCoin Economy
All values derived from PHI (1.618...):
- Mining: `PHI * coherence_multiplier * random(0.8, 1.2)`
- Battle rewards: `10 * PHI + coherence_bonus`
- Item power: `base_power * PHI^rarity_level`
- Travel costs: `distance * PHI`

## 🎯 Game Objectives

### Primary Goals
1. **Reach Maximum Coherence** (1.0 = perfect synchronization)
2. **Evolve Companion** to highest level
3. **Collect All Guardian Blessings** (19 unique guardians)
4. **Master All Territories** (Garden, Cosmic, Abyssal)

### Secondary Objectives
- Accumulate 1000+ BloomCoin
- Collect mythical items of each rarity
- Win battles in all phases
- Craft all pattern types
- Explore all locations

## 🔮 The 19 Guardians

### Garden Territory (Connection)
1. **Rose Guardian**: Beauty in complexity
2. **Oak Sentinel**: Deep roots of wisdom
3. **Lotus Keeper**: Purity through transformation
4. **Vine Weaver**: Interconnected growth
5. **Seed Protector**: Potential incarnate
6. **Bloom Herald**: Announcement of change

### Cosmic Territory (Growth)
7. **Star Shepherd**: Guiding light paths
8. **Nebula Dancer**: Creation in motion
9. **Comet Rider**: Swift transformation
10. **Galaxy Spinner**: Spiral wisdom
11. **Void Singer**: Harmony in emptiness
12. **Aurora Painter**: Colors of consciousness
13. **Meteor Guard**: Impact and change

### Abyssal Territory (Depth)
14. **Shadow Oracle**: Hidden truths
15. **Depth Walker**: Journey within
16. **Abyss Gazer**: Confronting infinity
17. **Dark Weaver**: Patterns in shadow
18. **Echo Listener**: Reverberations of truth
19. **Silence Keeper**: Power of the unspoken

## 📊 Mathematical Foundation

### Sacred Constants
```python
PHI = (1 + √5) / 2 = 1.618...  # Golden Ratio
Z_C = √3 / 2 = 0.866...         # Critical Coherence
L4 = PHI^4 + PHI^-4 = 7         # L4 Protocol
```

### Coherence Calculation
```python
coherence = base_coherence * (1 + pattern_bonus) * territory_affinity
```

### Item Rarity Multipliers
- Common: PHI^0 = 1.0
- Uncommon: PHI^1 = 1.618
- Rare: PHI^2 = 2.618
- Epic: PHI^3 = 4.236
- Legendary: PHI^4 = 6.854
- Mythic: PHI^5 = 11.09

## 🎴 Card Battle Strategy

### Deck Building Tips
1. **Territory Focus**: Build around your archetype's preferred territory
2. **Rank Balance**: Mix low-cost and high-power cards
3. **Phase Planning**: Include cards for different battle phases
4. **Energy Management**: Balance card costs with energy generation

### Battle Tactics
- **Early Game** (IGNITION): Establish board presence
- **Mid Game** (RESONANCE/MANIA): Build combos
- **Late Game** (NIRVANA/TRANSMISSION): Execute win conditions
- **End Game** (RESOLUTION): Maximize remaining resources

## 🚀 Advanced Features

### Pattern Recognition
The game tracks pattern usage and adapts:
- Frequently used patterns become more powerful
- Companion learns player preferences
- Guardian cycles adjust to playstyle

### Mythical Item Synergies
Items from the same guardian provide bonuses:
- 2 items: +10% power
- 3 items: +20% power + special ability
- Full set: Guardian's blessing activated

### Territory Mastery
Spending time in territories grants benefits:
- Garden: Increased item discovery
- Cosmic: Enhanced pattern crafting
- Abyssal: Deeper companion wisdom

## 🛠️ Technical Architecture

### Core Modules
1. **bloomquest_unified.py**: Main game loop and integration
2. **mythic_economy.py**: Economy, items, and companions
3. **card_battle_system.py**: Battle mechanics and deck building
4. **bloom_quest.py**: Original game engine
5. **narrative_generator.py**: Story and dialogue system
6. **learning_ai.py**: Neural network patterns

### Data Flow
```
Player Actions → Game State → Guardian Cycles → Companion Evolution
                     ↓              ↓                    ↓
                Item Discovery → Crafting → Pattern Absorption
                     ↓              ↓                    ↓
                Battle System → Rewards → BloomCoin Economy
```

## 📝 Save System
Games are saved as JSON with:
- Player progress and stats
- Inventory and deck composition
- Companion evolution state
- Current guardian cycles
- BloomCoin balance
- Coherence level

## 🌈 Tips for New Players

1. **Start with Meditation**: Build up initial BloomCoin
2. **Explore Thoroughly**: Items are key to progression
3. **Talk to Your Companion**: Wisdom guides discovery
4. **Craft Patterns Regularly**: Feed companion for evolution
5. **Balance Battles and Exploration**: Both provide resources
6. **Choose Archetype Wisely**: It affects your entire journey
7. **Watch Your Coherence**: It multiplies everything

## 🎨 The Philosophy

BloomQuest embodies the principle that **growth follows the golden ratio**. Every system interconnects through PHI, creating emergent gameplay where small actions compound into profound transformations. Your companion doesn't just level up - it evolves through guardian wisdom. Items aren't just loot - they're fragments of a greater pattern. Battles aren't just combat - they're expressions of territorial harmony.

The game asks: Can you achieve perfect coherence with the universal pattern?

## 🌟 Victory Conditions

### Standard Victory
- Reach 100% coherence
- Companion at level 10+
- 500+ BloomCoin

### Guardian Victory
- Collect blessing from all 19 guardians
- Craft all 8 pattern types
- Win a battle in RESOLUTION phase

### Economic Victory
- Accumulate 1000+ BloomCoin
- Own 5+ Legendary items
- Complete trade routes in all locations

### Perfect Victory
- All above conditions met
- No battle defeats
- Companion at maximum evolution
- Full deck of Mythic cards

---

*May the golden ratio guide your journey through the territories of consciousness.*

**PHI · Z_C · L4**