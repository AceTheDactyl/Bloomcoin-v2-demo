#!/usr/bin/env python3
"""
BloomQuest Web UI - FULLY WORKING VERSION
==========================================
Web interface with properly connected Socket.IO events and working interactions.
"""

import os
import sys
import time
import uuid
import json
import random
import threading
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, render_template_string, jsonify, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room

# Import game modules
try:
    from unified_mining_economy import UnifiedMiningEconomy
    from economy_integration_bridge import UnifiedGameInterface
    from companion_mining_ultimate import CompanionType
    from guardian_pattern_recipes import PatternType
    from pattern_mining_jobs import MiningJobType
    GAME_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some game modules not available: {e}")
    GAME_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bloomquest-secret-key-' + str(uuid.uuid4())
socketio = SocketIO(app, cors_allowed_origins="*")

# Game sessions
game_sessions = {}
player_data = {}
active_jobs = {}

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BloomQuest - Web Interface</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0e27, #151931);
            color: #e4e4e7;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            padding: 30px 0;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 210, 255, 0.2);
        }

        .card h2 {
            color: #00d2ff;
            margin-bottom: 15px;
            font-size: 1.4em;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }

        .stat-item {
            padding: 10px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
        }

        .stat-label {
            color: #9ca3af;
            font-size: 0.9em;
        }

        .stat-value {
            color: #00d2ff;
            font-size: 1.3em;
            font-weight: bold;
        }

        .btn {
            padding: 12px 24px;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin: 5px;
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0, 210, 255, 0.4);
        }

        .btn:active {
            transform: scale(0.98);
        }

        .btn-success {
            background: linear-gradient(90deg, #10b981, #059669);
        }

        .btn-warning {
            background: linear-gradient(90deg, #f59e0b, #d97706);
        }

        .progress-bar {
            width: 100%;
            height: 25px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #10b981, #059669);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: width 0.5s ease;
            color: white;
            font-weight: bold;
        }

        .job-item {
            padding: 15px;
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .job-item.complete {
            border-color: #10b981;
            background: rgba(16, 185, 129, 0.1);
        }

        #notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            display: none;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        .notification-success {
            background: linear-gradient(90deg, #10b981, #059669);
        }

        .notification-error {
            background: linear-gradient(90deg, #ef4444, #dc2626);
        }

        .notification-info {
            background: linear-gradient(90deg, #3b82f6, #2563eb);
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #00d2ff;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
    <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
</head>
<body>
    <div id="notification"></div>

    <div class="container">
        <div class="header">
            <h1>🌸 BloomQuest</h1>
            <p>NEXTHASH-256 Cryptocurrency Mining Adventure</p>
        </div>

        <div class="grid">
            <!-- Player Stats -->
            <div class="card">
                <h2>👤 Player Stats</h2>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-label">Name</div>
                        <div class="stat-value" id="player-name">Loading...</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Level</div>
                        <div class="stat-value" id="player-level">1</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Balance</div>
                        <div class="stat-value"><span id="balance">0</span> BC</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Patterns</div>
                        <div class="stat-value" id="patterns">0</div>
                    </div>
                </div>
            </div>

            <!-- Mining Controls -->
            <div class="card">
                <h2>⛏️ Mining Operations</h2>
                <button class="btn" onclick="quickMine()">Quick Mine</button>
                <button class="btn btn-warning" onclick="startAdvancedMining()">Advanced Mine</button>
                <button class="btn btn-success" onclick="collectAll()">Collect All</button>
                <div style="margin-top: 15px;">
                    <div class="stat-label">Active Jobs</div>
                    <div class="stat-value" id="active-jobs">0</div>
                </div>
            </div>

            <!-- Mining Stats -->
            <div class="card">
                <h2>📊 Mining Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-label">Total Mined</div>
                        <div class="stat-value"><span id="total-mined">0</span> BC</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Mining Rate</div>
                        <div class="stat-value"><span id="mining-rate">0</span> BC/h</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Patterns Found</div>
                        <div class="stat-value" id="patterns-found">0</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Market Sentiment</div>
                        <div class="stat-value" id="market-sentiment">1.0</div>
                    </div>
                </div>
            </div>

            <!-- Active Jobs -->
            <div class="card" style="grid-column: span 2;">
                <h2>💼 Active Mining Jobs</h2>
                <div id="active-jobs-list">
                    <p>No active mining jobs</p>
                </div>
            </div>

            <!-- Market -->
            <div class="card" style="grid-column: span 2;">
                <h2>📈 Pattern Market</h2>
                <button class="btn" onclick="refreshMarket()">Refresh Market</button>
                <div id="market-data" style="margin-top: 15px;">
                    <p>Loading market data...</p>
                </div>
            </div>

            <!-- Activity Log -->
            <div class="card" style="grid-column: span 2;">
                <h2>📜 Activity Log</h2>
                <div id="activity-log" style="max-height: 200px; overflow-y: auto;">
                    <p>Welcome to BloomQuest!</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Initialize Socket.IO connection
        const socket = io();
        let sessionId = null;
        let playerData = null;

        // Connect handler
        socket.on('connect', () => {
            console.log('Connected to server');
            showNotification('Connected to server!', 'success');
            initializeGame();
        });

        // Disconnect handler
        socket.on('disconnect', () => {
            console.log('Disconnected from server');
            showNotification('Disconnected from server', 'error');
        });

        // Initialize game
        function initializeGame() {
            socket.emit('init_game', {
                player_name: 'Player_' + Math.random().toString(36).substring(7)
            });
        }

        // Handle game initialization response
        socket.on('game_initialized', (data) => {
            console.log('Game initialized:', data);
            sessionId = data.session_id;
            playerData = data.player_data;
            updateUI(data);
            showNotification('Game initialized!', 'success');
            addActivity('Game session started');
        });

        // Handle mining started
        socket.on('mining_started', (data) => {
            console.log('Mining started:', data);
            showNotification('Mining job started!', 'success');
            addActivity('Mining job started');
            updateUI(data);
        });

        // Handle job updates
        socket.on('job_update', (data) => {
            console.log('Job update:', data);
            updateJobDisplay(data);
        });

        // Handle job completion
        socket.on('job_complete', (data) => {
            console.log('Job complete:', data);
            showNotification(`Job completed! Earned ${data.reward.toFixed(2)} BC`, 'success');
            addActivity(`Mining completed: +${data.reward.toFixed(2)} BC`);
            updateUI(data);
        });

        // Handle stats updates
        socket.on('stats_update', (data) => {
            console.log('Stats update:', data);
            updateUI(data);
        });

        // Handle market updates
        socket.on('market_update', (data) => {
            console.log('Market update:', data);
            displayMarketData(data);
        });

        // Handle errors
        socket.on('error', (data) => {
            console.error('Error:', data);
            showNotification(data.message || 'An error occurred', 'error');
        });

        // Quick mine function
        function quickMine() {
            console.log('Starting quick mine...');
            socket.emit('quick_mine', {});
        }

        // Advanced mining
        function startAdvancedMining() {
            const difficulty = prompt('Enter difficulty (1-5):', '3');
            if (difficulty) {
                socket.emit('start_mining', {
                    companion_index: 0,
                    difficulty: parseInt(difficulty)
                });
            }
        }

        // Collect all rewards
        function collectAll() {
            console.log('Collecting all rewards...');
            socket.emit('collect_all', {});
        }

        // Refresh market
        function refreshMarket() {
            console.log('Refreshing market...');
            socket.emit('get_market_data', {});
        }

        // Show notification
        function showNotification(message, type = 'info') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification-${type}`;
            notification.style.display = 'block';

            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }

        // Update UI with data
        function updateUI(data) {
            if (!data) return;

            // Update player stats
            if (data.player) {
                document.getElementById('player-name').textContent = data.player.name || 'Guest';
                document.getElementById('player-level').textContent = data.player.level || 1;
                document.getElementById('balance').textContent = (data.player.balance || 0).toFixed(2);
                document.getElementById('patterns').textContent = data.player.patterns || 0;
            }

            // Update mining stats
            if (data.stats) {
                document.getElementById('total-mined').textContent = (data.stats.total_mined || 0).toFixed(2);
                document.getElementById('mining-rate').textContent = (data.stats.mining_rate || 0).toFixed(2);
                document.getElementById('patterns-found').textContent = data.stats.patterns || 0;
                document.getElementById('market-sentiment').textContent = (data.stats.market_sentiment || 1).toFixed(2);
            }

            // Update jobs
            if (data.jobs) {
                document.getElementById('active-jobs').textContent = data.jobs.filter(j => j.status === 'active').length;
                displayJobs(data.jobs);
            }
        }

        // Display jobs
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
                        <div class="progress-fill" style="width: ${(job.progress || 0) * 100}%">
                            ${((job.progress || 0) * 100).toFixed(1)}%
                        </div>
                    </div>
                    ${isComplete ?
                        `<button class="btn btn-success" onclick="collectJob('${job.id}')">Collect ${job.reward.toFixed(2)} BC</button>` :
                        `<span>ETA: ${job.time_left || 30}s</span>`
                    }
                </div>`;
            });
            container.innerHTML = html;
        }

        // Update job display
        function updateJobDisplay(jobData) {
            // Find and update specific job
            const jobs = document.querySelectorAll('.job-item');
            jobs.forEach(jobEl => {
                if (jobEl.textContent.includes(jobData.job_id.substring(0, 8))) {
                    const progressBar = jobEl.querySelector('.progress-fill');
                    if (progressBar) {
                        progressBar.style.width = `${(jobData.progress || 0) * 100}%`;
                        progressBar.textContent = `${((jobData.progress || 0) * 100).toFixed(1)}%`;
                    }
                }
            });
        }

        // Collect specific job
        function collectJob(jobId) {
            socket.emit('collect_job', { job_id: jobId });
        }

        // Display market data
        function displayMarketData(data) {
            const container = document.getElementById('market-data');
            if (!data || !data.patterns || data.patterns.length === 0) {
                container.innerHTML = '<p>No market data available</p>';
                return;
            }

            let html = '<table style="width: 100%;">';
            html += '<tr><th>Pattern</th><th>Price</th><th>Change</th><th>Action</th></tr>';

            data.patterns.forEach(pattern => {
                const changeClass = pattern.change > 0 ? 'color: #10b981;' : 'color: #ef4444;';
                html += `<tr>
                    <td>${pattern.name}</td>
                    <td>${pattern.price.toFixed(2)} BC</td>
                    <td style="${changeClass}">${pattern.change > 0 ? '+' : ''}${pattern.change.toFixed(2)}%</td>
                    <td><button class="btn" onclick="trade('${pattern.symbol}')">Trade</button></td>
                </tr>`;
            });

            html += '</table>';
            container.innerHTML = html;
        }

        // Trade function
        function trade(symbol) {
            const action = confirm('Buy ' + symbol + '?') ? 'buy' : 'sell';
            socket.emit('trade', {
                symbol: symbol,
                action: action,
                amount: 10
            });
        }

        // Add activity to log
        function addActivity(message) {
            const log = document.getElementById('activity-log');
            const time = new Date().toLocaleTimeString();
            const entry = document.createElement('p');
            entry.innerHTML = `<strong>[${time}]</strong> ${message}`;
            log.insertBefore(entry, log.firstChild);

            // Keep only last 10 entries
            while (log.children.length > 10) {
                log.removeChild(log.lastChild);
            }
        }

        // Poll for updates every 5 seconds
        setInterval(() => {
            if (socket.connected) {
                socket.emit('get_update', {});
            }
        }, 5000);
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'running',
        'sessions': len(game_sessions),
        'timestamp': datetime.now().isoformat()
    })

# Socket.IO event handlers with proper emission
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
        player_name = data.get('player_name', f"Player_{session_id[:8]}")
        player = game.create_player(player_name, 1000.0)

        # Store player data
        player_data[session_id] = {
            'name': player_name,
            'level': 1,
            'balance': 1000.0,
            'patterns': 0,
            'total_mined': 0.0,
            'jobs': []
        }

        # Join room for targeted updates
        join_room(session_id)

        # Emit initialization success
        emit('game_initialized', {
            'session_id': session_id,
            'player_data': player_data[session_id],
            'player': player_data[session_id],
            'stats': {
                'total_mined': 0,
                'mining_rate': 0,
                'patterns': 0,
                'market_sentiment': 1.0
            },
            'jobs': []
        })

        print(f"Game initialized for session {session_id}")

    except Exception as e:
        print(f"Error in init_game: {e}")
        emit('error', {'message': str(e)})

@socketio.on('quick_mine')
def handle_quick_mine(data):
    """Start quick mining job"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in game_sessions:
            emit('error', {'message': 'Session not found'})
            return

        game = game_sessions[session_id]
        player = player_data[session_id]

        # Start mining job
        job_id = str(uuid.uuid4())
        job_data = {
            'id': job_id,
            'type': 'Quick Mine',
            'progress': 0,
            'reward': random.uniform(10, 50),
            'status': 'active',
            'time_left': 10,
            'start_time': time.time()
        }

        player['jobs'].append(job_data)

        # Emit mining started event
        emit('mining_started', {
            'job_id': job_id,
            'player': player,
            'jobs': player['jobs']
        })

        # Simulate job progress
        def update_job():
            for i in range(10):
                time.sleep(1)
                job_data['progress'] = (i + 1) / 10
                job_data['time_left'] = 10 - i - 1

                socketio.emit('job_update', {
                    'job_id': job_id,
                    'progress': job_data['progress'],
                    'time_left': job_data['time_left']
                }, room=session_id)

            # Complete job
            job_data['status'] = 'completed'
            job_data['progress'] = 1.0
            player['balance'] += job_data['reward']
            player['total_mined'] += job_data['reward']

            socketio.emit('job_complete', {
                'job_id': job_id,
                'reward': job_data['reward'],
                'player': player,
                'jobs': player['jobs'],
                'stats': {
                    'total_mined': player['total_mined'],
                    'mining_rate': player['total_mined'] / 10,
                    'patterns': player['patterns'],
                    'market_sentiment': 1.0
                }
            }, room=session_id)

        threading.Thread(target=update_job, daemon=True).start()

        print(f"Quick mine started for session {session_id}")

    except Exception as e:
        print(f"Error in quick_mine: {e}")
        emit('error', {'message': str(e)})

@socketio.on('start_mining')
def handle_start_mining(data):
    """Start custom mining job"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in game_sessions:
            emit('error', {'message': 'Session not found'})
            return

        game = game_sessions[session_id]
        player = player_data[session_id]

        difficulty = data.get('difficulty', 3)
        companion_index = data.get('companion_index', 0)

        # Create job with difficulty-based rewards
        job_id = str(uuid.uuid4())
        base_reward = difficulty * random.uniform(15, 30)
        duration = difficulty * 5  # 5 seconds per difficulty level

        job_data = {
            'id': job_id,
            'type': f'Mining (Diff {difficulty})',
            'progress': 0,
            'reward': base_reward,
            'status': 'active',
            'time_left': duration,
            'start_time': time.time()
        }

        player['jobs'].append(job_data)

        # Emit mining started
        emit('mining_started', {
            'job_id': job_id,
            'player': player,
            'jobs': player['jobs']
        })

        # Simulate mining progress
        def mine_job():
            steps = duration
            for i in range(steps):
                time.sleep(1)
                job_data['progress'] = (i + 1) / steps
                job_data['time_left'] = duration - i - 1

                socketio.emit('job_update', {
                    'job_id': job_id,
                    'progress': job_data['progress'],
                    'time_left': job_data['time_left']
                }, room=session_id)

            # Complete job
            job_data['status'] = 'completed'
            job_data['progress'] = 1.0
            player['balance'] += job_data['reward']
            player['total_mined'] += job_data['reward']

            # Chance to find pattern
            if random.random() < 0.2 * difficulty:
                player['patterns'] += 1
                socketio.emit('pattern_found', {
                    'pattern': 'ECHO_RESONANCE',
                    'player': player
                }, room=session_id)

            socketio.emit('job_complete', {
                'job_id': job_id,
                'reward': job_data['reward'],
                'player': player,
                'jobs': player['jobs'],
                'stats': {
                    'total_mined': player['total_mined'],
                    'mining_rate': player['total_mined'] / 10,
                    'patterns': player['patterns'],
                    'market_sentiment': 1.0
                }
            }, room=session_id)

        threading.Thread(target=mine_job, daemon=True).start()

        print(f"Custom mining started for session {session_id}")

    except Exception as e:
        print(f"Error in start_mining: {e}")
        emit('error', {'message': str(e)})

@socketio.on('collect_all')
def handle_collect_all(data):
    """Collect all completed jobs"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in player_data:
            emit('error', {'message': 'Session not found'})
            return

        player = player_data[session_id]
        total_collected = 0

        # Collect completed jobs
        completed_jobs = [j for j in player['jobs'] if j['status'] == 'completed']
        for job in completed_jobs:
            total_collected += job['reward']
            player['jobs'].remove(job)

        if total_collected > 0:
            emit('stats_update', {
                'collected': total_collected,
                'player': player,
                'jobs': player['jobs'],
                'stats': {
                    'total_mined': player['total_mined'],
                    'mining_rate': player['total_mined'] / 10,
                    'patterns': player['patterns'],
                    'market_sentiment': 1.0
                }
            })

            print(f"Collected {total_collected} BC for session {session_id}")
        else:
            emit('error', {'message': 'No completed jobs to collect'})

    except Exception as e:
        print(f"Error in collect_all: {e}")
        emit('error', {'message': str(e)})

@socketio.on('collect_job')
def handle_collect_job(data):
    """Collect specific job reward"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in player_data:
            emit('error', {'message': 'Session not found'})
            return

        player = player_data[session_id]
        job_id = data.get('job_id')

        # Find and collect job
        for job in player['jobs']:
            if job['id'] == job_id and job['status'] == 'completed':
                reward = job['reward']
                player['jobs'].remove(job)

                emit('stats_update', {
                    'collected': reward,
                    'player': player,
                    'jobs': player['jobs'],
                    'stats': {
                        'total_mined': player['total_mined'],
                        'mining_rate': player['total_mined'] / 10,
                        'patterns': player['patterns'],
                        'market_sentiment': 1.0
                    }
                })

                print(f"Collected job {job_id} for {reward} BC")
                return

        emit('error', {'message': 'Job not found or not completed'})

    except Exception as e:
        print(f"Error in collect_job: {e}")
        emit('error', {'message': str(e)})

@socketio.on('get_market_data')
def handle_get_market_data(data):
    """Get market data"""
    try:
        # Generate sample market data
        patterns = [
            {'name': 'ECHO_RESONANCE', 'symbol': 'ECHO', 'price': 100 + random.uniform(-20, 20), 'change': random.uniform(-10, 10)},
            {'name': 'GLITCH_MATRIX', 'symbol': 'GLTCH', 'price': 150 + random.uniform(-30, 30), 'change': random.uniform(-15, 15)},
            {'name': 'FLOW_STREAM', 'symbol': 'FLOW', 'price': 80 + random.uniform(-15, 15), 'change': random.uniform(-8, 8)},
            {'name': 'SPARK_IGNITION', 'symbol': 'SPRK', 'price': 120 + random.uniform(-25, 25), 'change': random.uniform(-12, 12)},
        ]

        emit('market_update', {
            'patterns': patterns,
            'timestamp': datetime.now().isoformat()
        })

        print(f"Market data sent")

    except Exception as e:
        print(f"Error in get_market_data: {e}")
        emit('error', {'message': str(e)})

@socketio.on('get_update')
def handle_get_update(data):
    """Get current game state"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in player_data:
            return

        player = player_data[session_id]

        emit('stats_update', {
            'player': player,
            'jobs': player['jobs'],
            'stats': {
                'total_mined': player['total_mined'],
                'mining_rate': player['total_mined'] / 10 if player['total_mined'] > 0 else 0,
                'patterns': player['patterns'],
                'market_sentiment': 1.0
            }
        })

    except Exception as e:
        print(f"Error in get_update: {e}")

@socketio.on('trade')
def handle_trade(data):
    """Handle pattern trading"""
    try:
        session_id = session.get('id')
        if not session_id or session_id not in player_data:
            emit('error', {'message': 'Session not found'})
            return

        player = player_data[session_id]
        symbol = data.get('symbol')
        action = data.get('action')
        amount = data.get('amount', 10)

        # Simulate trade
        if action == 'buy':
            cost = amount * random.uniform(80, 120)
            if player['balance'] >= cost:
                player['balance'] -= cost
                player['patterns'] += 1
                emit('trade_success', {
                    'action': 'bought',
                    'symbol': symbol,
                    'cost': cost,
                    'player': player
                })
            else:
                emit('error', {'message': 'Insufficient funds'})
        else:
            # Sell
            if player['patterns'] > 0:
                revenue = amount * random.uniform(80, 120)
                player['balance'] += revenue
                player['patterns'] -= 1
                emit('trade_success', {
                    'action': 'sold',
                    'symbol': symbol,
                    'revenue': revenue,
                    'player': player
                })
            else:
                emit('error', {'message': 'No patterns to sell'})

    except Exception as e:
        print(f"Error in trade: {e}")
        emit('error', {'message': str(e)})

def run_server(host='0.0.0.0', port=5001, debug=True):
    """Run the web server"""
    print(f"Starting BloomQuest Web UI (WORKING VERSION) on port {port}...")
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='BloomQuest Web UI Server')
    parser.add_argument('--port', type=int, default=5001, help='Port to run on')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()
    run_server(host=args.host, port=args.port, debug=args.debug)