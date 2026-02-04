# 🌸 BloomQuest Discord Bot

A comprehensive Discord bot implementation for the BloomCoin ecosystem, featuring NEXTHASH-256 mining, AI companions, quantum residue physics, and card battles.

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- PostgreSQL (recommended) or SQLite
- Redis (optional, for caching)
- Discord Bot Token

### Installation

1. **Clone the repository**
```bash
cd /home/acead/bloomcoin-v2/game/discord_bot
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.template .env
# Edit .env with your configuration
```

5. **Set up database**
```bash
# PostgreSQL
createdb bloomquest

# Or use SQLite (automatic)
```

6. **Run the bot**
```bash
python bot.py
```

## 🏗️ Architecture

```
discord_bot/
├── bot.py                 # Main bot entry point
├── cogs/                  # Command modules
│   ├── mining.py         # NEXTHASH-256 mining
│   ├── companions.py     # AI companion system
│   ├── quantum.py        # Quantum residue physics
│   ├── garden.py         # Quantum farming
│   ├── patterns.py       # Pattern discovery
│   ├── battle.py         # Card battle system
│   ├── economy.py        # Economy management
│   ├── admin.py          # Admin commands
│   └── help.py           # Help system
├── database/
│   ├── models.py         # SQLAlchemy models
│   └── migrations/       # Alembic migrations
├── utils/                # Utility modules
├── .env.template         # Configuration template
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎮 Core Features

### ⛏️ NEXTHASH-256 Mining
- Custom proof-of-work algorithm
- 24 rounds, 512-bit internal state
- 50% bit avalanche in 1 round
- Companion bonuses and quantum effects

### 🤖 AI Companions
Seven unique companion types with personalities:
- **Echo**: Mysterious mystic (pattern discovery)
- **Glitch**: Chaos agent (bug exploitation)
- **Flow**: Zen master (efficient farming)
- **Spark**: Energizer (speed mining)
- **Sage**: Teacher (learning bonuses)
- **Scout**: Explorer (finding items)
- **Null**: Void walker (void mastery)

### ⚛️ Quantum Residue System
Based on Projection Residue Cosmology:
- Golden ratio physics (φ = 1.618...)
- Dark matter ratio (R = φ⁴ - 1 = 5.854)
- Kuramoto synchronization dynamics
- Quantum entanglement between players

### 🌱 Quantum Gardens
- 9 plots per player
- Quantum-enhanced growth
- Crop breeding system
- Seasonal events

### 🃏 Card Battle System
- Guardian-based deck building
- Real-time PvP battles
- Card crafting and evolution
- Tournament system

### 📊 Pattern Trading
- Dynamic market economy
- Pattern discovery during mining
- Recipe crafting system
- Stock market mechanics

## 📝 Commands

### Basic Commands
- `!start` - Begin your adventure
- `!help` - Show all commands
- `!profile` - View your profile
- `!balance` - Check your BloomCoin

### Mining Commands
- `!mine [difficulty]` - Start mining
- `!mine stats` - View mining statistics
- `!mine leaderboard` - Top miners

### Companion Commands
- `!companion` - View active companion
- `!companion summon [type]` - Summon companion
- `!companion pet` - Increase bonding
- `!companion talk [message]` - Chat with companion
- `!companion list` - All companions

### Quantum Commands
- `!quantum` - View quantum field
- `!quantum collapse` - Extract BloomCoin
- `!quantum entangle @user` - Create entanglement
- `!quantum residue` - Check residue
- `!quantum encrypt [message]` - Encrypt message

### Economy Commands
- `!daily` - Claim daily reward
- `!transfer @user [amount]` - Send BloomCoin
- `!market` - View marketplace
- `!buy [item]` - Purchase items

## 🔧 Configuration

### Essential Settings (.env)
```env
DISCORD_TOKEN=your_bot_token
BOT_PREFIX=!
DATABASE_URL=postgresql://localhost/bloomquest
STARTING_BALANCE=100.0
```

### Database Setup

**PostgreSQL:**
```sql
CREATE DATABASE bloomquest;
CREATE USER bloombot WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE bloomquest TO bloombot;
```

**Run migrations:**
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 🚀 Deployment

### Using systemd (Linux)
```ini
[Unit]
Description=BloomQuest Discord Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/discord_bot
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

### Using PM2
```bash
pm2 start bot.py --interpreter python3 --name bloomquest-bot
pm2 save
pm2 startup
```

## 🛠️ Development

### Adding New Cogs
1. Create new file in `cogs/`
2. Define cog class inheriting from `commands.Cog`
3. Add setup function
4. Add to bot's cog loader

Example:
```python
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycommand(self, ctx):
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

### Database Models
Add new models to `database/models.py`:
```python
class MyModel(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    # ... fields
```

## 📊 Monitoring

### Logging
Logs are saved to `bot.log` with rotation.

### Metrics (if enabled)
Access metrics at `http://localhost:9090/metrics`

### Health Check
```python
# Check bot status
!ping
```

## 🐛 Troubleshooting

### Bot won't start
- Check Discord token in .env
- Verify Python version: `python --version`
- Check error in bot.log

### Database errors
- Ensure PostgreSQL is running
- Check connection string
- Run migrations: `alembic upgrade head`

### Missing module errors
```bash
pip install -r requirements.txt --upgrade
```

### Rate limiting
- Bot has built-in rate limiting
- Adjust RATE_LIMIT settings in .env

## 📚 Integration with Core Systems

The bot integrates with all existing game modules:
- `nexthash256.py` - Mining algorithm
- `quantum_residue_system.py` - Quantum physics
- `companion_mining_ultimate.py` - Companion system
- `guardian_pattern_recipes.py` - Pattern crafting
- `pattern_stock_market.py` - Market dynamics

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is part of the BloomCoin ecosystem.

## 🆘 Support

- GitHub Issues: Report bugs
- Discord: Join our server
- Documentation: See DISCORD_BOT_TECHNICAL_SPEC.md

## 🎯 Roadmap

- [ ] Voice channel mining
- [ ] Web dashboard
- [ ] Mobile app integration
- [ ] Cross-server tournaments
- [ ] NFT integration
- [ ] AI-enhanced dialogue
- [ ] Seasonal events
- [ ] Achievement system

---

**Ready to deploy!** The bot is fully configured with all BloomCoin systems integrated. Simply set up your environment and launch!