#!/usr/bin/env python3
"""
BloomQuest Web UI - Fixed Version with Working Interactions
=============================================================
Fully functional web interface with all interactive elements working.
"""

from flask import Flask, render_template_string, jsonify, session
from flask_socketio import SocketIO, emit
import json
import time
import threading
import uuid
from datetime import datetime
import random

# Import game systems
from unified_mining_economy import UnifiedMiningEconomy, MiningJobType
from economy_integration_bridge import UnifiedGameInterface

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bloomquest-secret-' + str(uuid.uuid4())
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Game instances
game_sessions = {}
player_data = {}

# HTML Template with fixed JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BloomQuest - Mining Adventure</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .header h1 {
            color: #6C63FF;
            margin-bottom: 10px;
        }

        .stats-bar {
            display: flex;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .stat-item {
            background: #f0f0f0;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: 600;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .card h2 {
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }

        .btn {
            background: #6C63FF;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            margin: 5px;
            transition: all 0.3s;
        }

        .btn:hover {
            background: #5753d9;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 99, 255, 0.3);
        }

        .btn-success {
            background: #4ECDC4;
        }

        .btn-success:hover {
            background: #45b8b1;
        }

        .btn-warning {
            background: #FFD93D;
            color: #333;
        }

        .btn-danger {
            background: #FF6B6B;
        }

        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #6C63FF, #FF6B6B);
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }

        .job-item {
            background: #f5f5f5;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #6C63FF;
        }

        .job-item.complete {
            border-left-color: #4ECDC4;
        }

        #activity-log {
            max-height: 200px;
            overflow-y: auto;
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }

        .activity-item {
            padding: 5px 0;
            border-bottom: 1px solid #e0e0e0;
            font-size: 0.9rem;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            animation: slideIn 0.5s;
            z-index: 1000;
        }

        .notification.success {
            background: #4ECDC4;
        }

        .notification.error {
            background: #FF6B6B;
        }

        .notification.info {
            background: #6C63FF;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(100px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .hidden {
            display: none;
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🌸 BloomQuest - NEXTHASH-256 Mining Adventure</h1>
            <div class="stats-bar">
                <div class="stat-item">👤 <span id="player-name">Guest</span></div>
                <div class="stat-item">⭐ Level <span id="player-level">1</span></div>
                <div class="stat-item">💰 <span id="balance">0</span> BC</div>
                <div class="stat-item">⛏️ <span id="active-jobs">0</span> Jobs</div>
                <div class="stat-item">🔮 <span id="patterns">0</span> Patterns</div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Mining Panel -->
            <div class="card">
                <h2>⛏️ Mining Operations</h2>
                <div id="mining-status">
                    <p>Ready to start mining!</p>
                </div>
                <div id="active-jobs-list"></div>
                <div style="margin-top: 20px;">
                    <button class="btn btn-success" onclick="quickMine()">Quick Mine</button>
                    <button class="btn" onclick="startCustomMine()">Custom Mine</button>
                    <button class="btn btn-warning" onclick="collectAll()">Collect All</button>
                </div>
                <div id="custom-mine-options" class="hidden" style="margin-top: 15px;">
                    <select id="mine-type" style="padding: 8px; margin: 5px;">
                        <option value="PATTERN_DISCOVERY">Pattern Discovery</option>
                        <option value="HASH_OPTIMIZATION">Hash Optimization</option>
                        <option value="RESIDUE_COLLECTION">Residue Collection</option>
                        <option value="GUARDIAN_ALIGNMENT">Guardian Alignment</option>
                    </select>
                    <select id="mine-difficulty" style="padding: 8px; margin: 5px;">
                        <option value="1">Easy</option>
                        <option value="2">Normal</option>
                        <option value="3">Hard</option>
                        <option value="4">Expert</option>
                    </select>
                    <button class="btn btn-success" onclick="executeMine()">Start Mining</button>
                </div>
            </div>

            <!-- Game Info Panel -->
            <div class="card">
                <h2>📊 Game Statistics</h2>
                <div id="game-stats">
                    <p>Total Mined: <strong><span id="total-mined">0</span> BC</strong></p>
                    <p>Mining Rate: <strong><span id="mining-rate">0</span> BC/hr</strong></p>
                    <p>Patterns Found: <strong><span id="patterns-found">0</span></strong></p>
                    <p>Market Sentiment: <strong><span id="market-sentiment">1.0</span>x</strong></p>
                </div>
                <div style="margin-top: 20px;">
                    <button class="btn" onclick="refreshStats()">Refresh Stats</button>
                    <button class="btn btn-success" onclick="showMarket()">View Market</button>
                </div>
            </div>

            <!-- Activity Log -->
            <div class="card" style="grid-column: 1 / -1;">
                <h2>📜 Activity Log</h2>
                <div id="activity-log">
                    <div class="activity-item">Welcome to BloomQuest!</div>
                </div>
            </div>

            <!-- Market Panel (hidden by default) -->
            <div id="market-panel" class="card hidden" style="grid-column: 1 / -1;">
                <h2>📈 Pattern Stock Market</h2>
                <div id="market-data">Loading market data...</div>
                <button class="btn btn-danger" onclick="hideMarket()">Close Market</button>
            </div>
        </div>
    </div>

    <script>
        // Initialize Socket.IO connection
        const socket = io();
        let sessionId = null;
        let activeJobs = {};

        // Connection handling
        socket.on('connect', () => {
            console.log('Connected to server');
            addActivity('Connected to BloomQuest server');
            initGame();
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from server');
            addActivity('Disconnected from server');
        });

        socket.on('error', (error) => {
            console.error('Socket error:', error);
            showNotification('Connection error: ' + error, 'error');
        });

        // Initialize game
        function initGame() {
            socket.emit('init_game', {}, (response) => {
                console.log('Game initialized:', response);
                if (response.success) {
                    sessionId = response.session_id;
                    updateUI(response.data);
                    showNotification('Game initialized!', 'success');

                    // Start polling for updates
                    setInterval(pollUpdates, 5000);
                } else {
                    showNotification('Failed to initialize game', 'error');
                }
            });
        }

        // Quick mine
        function quickMine() {
            socket.emit('quick_mine', {}, (response) => {
                console.log('Quick mine response:', response);
                if (response.success) {
                    showNotification('Mining started!', 'success');
                    addActivity('Started quick mining job');
                    updateUI(response.data);
                    if (response.job_id) {
                        activeJobs[response.job_id] = Date.now();
                    }
                } else {
                    showNotification(response.error || 'Mining failed', 'error');
                }
            });
        }

        // Custom mine options
        function startCustomMine() {
            const options = document.getElementById('custom-mine-options');
            options.classList.toggle('hidden');
        }

        // Execute custom mine
        function executeMine() {
            const type = document.getElementById('mine-type').value;
            const difficulty = parseInt(document.getElementById('mine-difficulty').value);

            socket.emit('start_mining', {
                type: type,
                difficulty: difficulty
            }, (response) => {
                console.log('Mining response:', response);
                if (response.success) {
                    showNotification('Mining job started!', 'success');
                    addActivity('Started ' + type + ' mining');
                    updateUI(response.data);
                    document.getElementById('custom-mine-options').classList.add('hidden');
                } else {
                    showNotification(response.error || 'Mining failed', 'error');
                }
            });
        }

        // Collect all rewards
        function collectAll() {
            socket.emit('collect_all', {}, (response) => {
                console.log('Collect response:', response);
                if (response.success) {
                    showNotification('Collected ' + response.total_reward.toFixed(2) + ' BC!', 'success');
                    addActivity('Collected rewards: ' + response.total_reward.toFixed(2) + ' BC');
                    updateUI(response.data);
                } else {
                    showNotification(response.error || 'No rewards to collect', 'error');
                }
            });
        }

        // Refresh stats
        function refreshStats() {
            socket.emit('get_stats', {}, (response) => {
                console.log('Stats response:', response);
                if (response.success) {
                    updateUI(response.data);
                    showNotification('Stats updated!', 'info');
                }
            });
        }

        // Show/hide market
        function showMarket() {
            document.getElementById('market-panel').classList.remove('hidden');
            socket.emit('get_market', {}, (response) => {
                if (response.success && response.market) {
                    displayMarket(response.market);
                }
            });
        }

        function hideMarket() {
            document.getElementById('market-panel').classList.add('hidden');
        }

        // Display market data
        function displayMarket(market) {
            let html = '<table style="width: 100%;">';
            html += '<tr><th>Symbol</th><th>Price</th><th>Change</th><th>Action</th></tr>';

            if (market.stocks) {
                market.stocks.forEach(stock => {
                    const changeColor = stock.change > 0 ? 'green' : 'red';
                    html += `<tr>
                        <td>${stock.symbol}</td>
                        <td>${stock.price.toFixed(2)} BC</td>
                        <td style="color: ${changeColor}">${stock.change.toFixed(1)}%</td>
                        <td><button class="btn" onclick="trade('${stock.symbol}')">Trade</button></td>
                    </tr>`;
                });
            }

            html += '</table>';
            document.getElementById('market-data').innerHTML = html;
        }

        // Trade function
        function trade(symbol) {
            const action = confirm('Buy ' + symbol + '?') ? 'buy' : 'sell';
            socket.emit('trade', {
                symbol: symbol,
                action: action,
                amount: 10
            }, (response) => {
                if (response.success) {
                    showNotification('Trade executed!', 'success');
                    updateUI(response.data);
                } else {
                    showNotification(response.error || 'Trade failed', 'error');
                }
            });
        }

        // Poll for updates
        function pollUpdates() {
            socket.emit('get_update', {}, (response) => {
                if (response.success) {
                    updateUI(response.data);
                }
            });
        }

        // Update UI with data
        function updateUI(data) {
            if (!data) return;

            // Update stats
            if (data.player) {
                document.getElementById('player-name').textContent = data.player.name || 'Guest';
                document.getElementById('player-level').textContent = data.player.level || 1;
                document.getElementById('balance').textContent = (data.player.balance || 0).toFixed(2);
                document.getElementById('patterns').textContent = data.player.patterns || 0;
            }

            if (data.stats) {
                document.getElementById('total-mined').textContent = (data.stats.total_mined || 0).toFixed(2);
                document.getElementById('mining-rate').textContent = (data.stats.mining_rate || 0).toFixed(2);
                document.getElementById('patterns-found').textContent = data.stats.patterns || 0;
                document.getElementById('market-sentiment').textContent = (data.stats.market_sentiment || 1).toFixed(2);
            }

            // Update active jobs
            if (data.jobs) {
                document.getElementById('active-jobs').textContent = data.jobs.length;
                displayJobs(data.jobs);
            }
        }

        // Display active jobs
        function displayJobs(jobs) {
            const container = document.getElementById('active-jobs-list');
            if (!jobs || jobs.length === 0) {
                container.innerHTML = '<p>No active mining jobs</p>';
                return;
            }

            let html = '';
            jobs.forEach(job => {
                const isComplete = job.status === 'completed';
                html += `<div class="job-item ${isComplete ? 'complete' : ''}">
                    <strong>Job ${job.id.substring(0, 8)}</strong> - ${job.type}
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${job.progress * 100}%">
                            ${(job.progress * 100).toFixed(1)}%
                        </div>
                    </div>
                    ${isComplete ?
                        `<button class="btn btn-success" onclick="collectJob('${job.id}')">Collect ${job.reward.toFixed(2)} BC</button>` :
                        `<span>ETA: ${job.time_left}s</span>`
                    }
                </div>`;
            });
            container.innerHTML = html;
        }

        // Collect specific job
        function collectJob(jobId) {
            socket.emit('collect_job', { job_id: jobId }, (response) => {
                if (response.success) {
                    showNotification('Collected ' + response.reward.toFixed(2) + ' BC!', 'success');
                    addActivity('Job completed: +' + response.reward.toFixed(2) + ' BC');
                    updateUI(response.data);
                } else {
                    showNotification('Failed to collect', 'error');
                }
            });
        }

        // Add activity to log
        function addActivity(message) {
            const log = document.getElementById('activity-log');
            const item = document.createElement('div');
            item.className = 'activity-item';
            item.textContent = new Date().toLocaleTimeString() + ' - ' + message;
            log.insertBefore(item, log.firstChild);

            // Keep only last 10 items
            while (log.children.length > 10) {
                log.removeChild(log.lastChild);
            }
        }

        // Show notification
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = 'notification ' + type;
            notification.textContent = message;
            document.body.appendChild(notification);

            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        // Listen for server events
        socket.on('job_completed', (data) => {
            showNotification('Mining job completed! +' + data.reward.toFixed(2) + ' BC', 'success');
            addActivity('Mining completed: +' + data.reward.toFixed(2) + ' BC');
            updateUI(data);
        });

        socket.on('game_update', (data) => {
            updateUI(data);
        });
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Socket.IO event handlers
@socketio.on('init_game')
def handle_init(data):
    """Initialize game session"""
    try:
        session_id = str(uuid.uuid4())
        session['id'] = session_id

        # Create game instance
        game = UnifiedGameInterface()
        game_sessions[session_id] = game

        # Create player
        player = game.create_player(f"Player_{session_id[:8]}", 1000.0)

        # Store player data
        player_data[session_id] = {
            'name': f"Player_{session_id[:8]}",
            'level': 1,
            'balance': 1000.0,
            'patterns': 0,
            'total_mined': 0.0,
            'jobs': []
        }

        return {
            'success': True,
            'session_id': session_id,
            'data': {
                'player': player_data[session_id],
                'stats': {
                    'total_mined': 0,
                    'mining_rate': 0,
                    'patterns': 0,
                    'market_sentiment': 1.0
                },
                'jobs': []
            }
        }
    except Exception as e:
        print(f"Error in init_game: {e}")
        return {'success': False, 'error': str(e)}

@socketio.on('quick_mine')
def handle_quick_mine(data):
    """Start quick mining job"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in game_sessions:
            return {'success': False, 'error': 'Session not found'}

        game = game_sessions[session_id]
        player = player_data[session_id]

        # Start mining
        job = game.start_mining(player['name'])

        if job:
            # Add to player's jobs
            job_data = {
                'id': job.job_id,
                'type': 'Quick Mine',
                'progress': 0,
                'reward': job.base_reward,
                'status': 'active',
                'time_left': 30,
                'start_time': time.time()
            }
            player['jobs'].append(job_data)

            # Auto-complete after delay
            def complete_job():
                time.sleep(30)  # 30 second job
                game.economy.process_mining(job.job_id)

                # Update job status
                for j in player['jobs']:
                    if j['id'] == job.job_id:
                        j['status'] = 'completed'
                        j['progress'] = 1.0

                        # Update player balance
                        player['balance'] += job.base_reward
                        player['total_mined'] += job.base_reward

                        # Emit completion event
                        socketio.emit('job_completed', {
                            'job_id': job.job_id,
                            'reward': job.base_reward,
                            'player': player
                        }, room=session_id)
                        break

            threading.Thread(target=complete_job, daemon=True).start()

            return {
                'success': True,
                'job_id': job.job_id,
                'data': {
                    'player': player,
                    'jobs': player['jobs']
                }
            }

        return {'success': False, 'error': 'Failed to start mining'}
    except Exception as e:
        print(f"Error in quick_mine: {e}")
        return {'success': False, 'error': str(e)}

@socketio.on('start_mining')
def handle_start_mining(data):
    """Start custom mining job"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in game_sessions:
            return {'success': False, 'error': 'Session not found'}

        game = game_sessions[session_id]
        player = player_data[session_id]

        job_type = data.get('type', 'PATTERN_DISCOVERY')
        difficulty = data.get('difficulty', 2)

        # Create mining job
        try:
            job_enum = MiningJobType[job_type]
        except:
            job_enum = MiningJobType.PATTERN_DISCOVERY

        job = game.economy.create_mining_job(
            player_id=player['name'],
            companion_id=f"{player['name']}_companion",
            job_type=job_enum,
            difficulty=difficulty
        )

        if job:
            duration = min(60 * difficulty, 120)  # Max 2 minutes

            job_data = {
                'id': job.job_id,
                'type': job_type,
                'progress': 0,
                'reward': job.base_reward,
                'status': 'active',
                'time_left': duration,
                'start_time': time.time()
            }
            player['jobs'].append(job_data)

            # Auto-complete
            def complete_job():
                time.sleep(duration)
                game.economy.process_mining(job.job_id)

                for j in player['jobs']:
                    if j['id'] == job.job_id:
                        j['status'] = 'completed'
                        j['progress'] = 1.0
                        player['balance'] += job.base_reward
                        player['total_mined'] += job.base_reward
                        break

            threading.Thread(target=complete_job, daemon=True).start()

            return {
                'success': True,
                'data': {
                    'player': player,
                    'jobs': player['jobs']
                }
            }

        return {'success': False, 'error': 'Failed to start mining'}
    except Exception as e:
        print(f"Error in start_mining: {e}")
        return {'success': False, 'error': str(e)}

@socketio.on('collect_all')
def handle_collect_all(data):
    """Collect all completed jobs"""
    try:
        session_id = session.get('id')
        if not session_id:
            return {'success': False, 'error': 'Session not found'}

        player = player_data[session_id]
        total_reward = 0

        # Collect all completed jobs
        completed_jobs = [j for j in player['jobs'] if j['status'] == 'completed']
        for job in completed_jobs:
            total_reward += job['reward']
            player['jobs'].remove(job)

        if total_reward > 0:
            return {
                'success': True,
                'total_reward': total_reward,
                'data': {
                    'player': player,
                    'jobs': player['jobs'],
                    'stats': {
                        'total_mined': player['total_mined'],
                        'mining_rate': total_reward * 120,  # per hour estimate
                        'patterns': player['patterns'],
                        'market_sentiment': 1.0 + random.random()
                    }
                }
            }

        return {'success': False, 'error': 'No rewards to collect'}
    except Exception as e:
        print(f"Error in collect_all: {e}")
        return {'success': False, 'error': str(e)}

@socketio.on('collect_job')
def handle_collect_job(data):
    """Collect specific job"""
    try:
        session_id = session.get('id')
        if not session_id:
            return {'success': False, 'error': 'Session not found'}

        player = player_data[session_id]
        job_id = data.get('job_id')

        for job in player['jobs']:
            if job['id'] == job_id and job['status'] == 'completed':
                reward = job['reward']
                player['jobs'].remove(job)

                return {
                    'success': True,
                    'reward': reward,
                    'data': {
                        'player': player,
                        'jobs': player['jobs']
                    }
                }

        return {'success': False, 'error': 'Job not found or not completed'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@socketio.on('get_update')
def handle_get_update(data):
    """Get current game state"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in player_data:
            return {'success': False}

        player = player_data[session_id]

        # Update job progress
        current_time = time.time()
        for job in player['jobs']:
            if job['status'] == 'active':
                elapsed = current_time - job['start_time']
                total_duration = job['time_left']
                job['progress'] = min(1.0, elapsed / total_duration)

                if job['progress'] >= 1.0:
                    job['status'] = 'completed'
                    job['progress'] = 1.0
                else:
                    job['time_left'] = int(total_duration - elapsed)

        return {
            'success': True,
            'data': {
                'player': player,
                'jobs': player['jobs'],
                'stats': {
                    'total_mined': player['total_mined'],
                    'mining_rate': 100.0 * len([j for j in player['jobs'] if j['status'] == 'active']),
                    'patterns': player['patterns'],
                    'market_sentiment': 1.0 + random.random() * 0.5
                }
            }
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

@socketio.on('get_stats')
def handle_get_stats(data):
    """Get detailed stats"""
    return handle_get_update(data)

@socketio.on('get_market')
def handle_get_market(data):
    """Get market data"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in game_sessions:
            return {'success': False}

        # Generate some mock market data
        stocks = []
        symbols = ['ECHO', 'GLTCH', 'FLOW', 'SPRK', 'SAGE']
        for symbol in symbols:
            stocks.append({
                'symbol': symbol,
                'price': 100 + random.random() * 50,
                'change': random.uniform(-10, 10)
            })

        return {
            'success': True,
            'market': {
                'stocks': stocks
            }
        }
    except:
        return {'success': False}

@socketio.on('trade')
def handle_trade(data):
    """Execute trade"""
    try:
        session_id = session.get('id')
        if not session_id:
            return {'success': False}

        player = player_data[session_id]
        symbol = data.get('symbol')
        action = data.get('action')
        amount = data.get('amount', 10)

        # Simple mock trade
        if action == 'buy':
            cost = amount * 10
            if player['balance'] >= cost:
                player['balance'] -= cost
                return {'success': True, 'data': {'player': player}}
        else:
            player['balance'] += amount * 10
            return {'success': True, 'data': {'player': player}}

        return {'success': False, 'error': 'Insufficient funds'}
    except:
        return {'success': False}

if __name__ == '__main__':
    print("Starting BloomQuest Web UI (Fixed Version)...")
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, allow_unsafe_werkzeug=True)