#!/usr/bin/env python3
"""
BloomQuest Web UI - Modern Web Interface for Complete Game Access
===================================================================
Flask-based web interface providing full access to all game modules
through a responsive, interactive web application.
"""

from flask import Flask, render_template, jsonify, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import time
import threading
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import os

# Import game systems
from unified_mining_economy import (
    UnifiedMiningEconomy,
    MiningJobType,
    format_bloomcoin
)
from economy_integration_bridge import UnifiedGameInterface
from companion_mining_ultimate import CompanionType
from guardian_pattern_recipes import PatternType

# Create Flask app
app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.config['SECRET_KEY'] = 'bloomquest-nexthash-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Game instances per session
game_sessions: Dict[str, UnifiedGameInterface] = {}
player_sessions: Dict[str, Dict] = {}

# ═══════════════════════════════════════════════════════════════════════
# HTML TEMPLATES (stored as strings for single-file deployment)
# ═══════════════════════════════════════════════════════════════════════

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BloomQuest - NEXTHASH Mining Adventure</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #6C63FF;
            --secondary: #FF6B6B;
            --success: #4ECDC4;
            --warning: #FFD93D;
            --danger: #FF6B6B;
            --dark: #2D3436;
            --light: #F4F4F4;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            color: var(--dark);
        }

        /* Header Styles */
        .header {
            background: rgba(255, 255, 255, 0.95);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            background: var(--bg-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-decoration: none;
        }

        .status-bar {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--light);
            border-radius: 20px;
            font-weight: 600;
        }

        .status-icon {
            font-size: 1.2rem;
        }

        /* Main Container */
        .main-container {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 250px 1fr 300px;
            gap: 2rem;
        }

        /* Sidebar Navigation */
        .sidebar {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 1.5rem;
            height: fit-content;
            position: sticky;
            top: 100px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.8rem 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            color: var(--dark);
        }

        .nav-item:hover {
            background: var(--light);
            transform: translateX(5px);
        }

        .nav-item.active {
            background: var(--primary);
            color: white;
        }

        .nav-icon {
            font-size: 1.3rem;
            width: 30px;
            text-align: center;
        }

        /* Content Area */
        .content {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 2rem;
            min-height: 600px;
        }

        .content-header {
            border-bottom: 2px solid var(--light);
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }

        .content-title {
            font-size: 2rem;
            color: var(--dark);
            margin-bottom: 0.5rem;
        }

        .content-subtitle {
            color: #666;
            font-size: 1.1rem;
        }

        /* Cards */
        .card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--light);
        }

        .card-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--dark);
        }

        .card-badge {
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .badge-success {
            background: var(--success);
            color: white;
        }

        .badge-warning {
            background: var(--warning);
            color: var(--dark);
        }

        .badge-primary {
            background: var(--primary);
            color: white;
        }

        /* Progress Bars */
        .progress-container {
            margin: 1rem 0;
        }

        .progress-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }

        .progress-bar {
            height: 25px;
            background: var(--light);
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 15px;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 0.9rem;
        }

        /* Buttons */
        .btn {
            padding: 0.8rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background: #5753d9;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 99, 255, 0.3);
        }

        .btn-success {
            background: var(--success);
            color: white;
        }

        .btn-success:hover {
            background: #45b8b1;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(78, 205, 196, 0.3);
        }

        .btn-danger {
            background: var(--danger);
            color: white;
        }

        .btn-group {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
        }

        /* Mining Job Cards */
        .mining-job {
            border-left: 4px solid var(--primary);
            padding-left: 1rem;
            margin: 1rem 0;
        }

        .mining-job.complete {
            border-left-color: var(--success);
        }

        .mining-job-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .mining-job-id {
            font-family: monospace;
            background: var(--light);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }

        /* Right Panel */
        .right-panel {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 1.5rem;
            height: fit-content;
            position: sticky;
            top: 100px;
        }

        .activity-feed {
            max-height: 400px;
            overflow-y: auto;
        }

        .activity-item {
            padding: 0.8rem;
            margin: 0.5rem 0;
            background: var(--light);
            border-radius: 8px;
            font-size: 0.9rem;
            animation: slideIn 0.5s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* Market Table */
        .market-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }

        .market-table th {
            background: var(--light);
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            color: var(--dark);
        }

        .market-table td {
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--light);
        }

        .market-table tr:hover {
            background: #fafafa;
        }

        .price-up {
            color: var(--success);
            font-weight: 600;
        }

        .price-down {
            color: var(--danger);
            font-weight: 600;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            animation: modalPop 0.3s ease;
        }

        @keyframes modalPop {
            from {
                opacity: 0;
                transform: scale(0.8);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        .modal-header {
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--light);
        }

        .modal-title {
            font-size: 1.5rem;
            color: var(--dark);
        }

        /* Forms */
        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--dark);
        }

        .form-control {
            width: 100%;
            padding: 0.8rem;
            border: 2px solid var(--light);
            border-radius: 8px;
            font-size: 1rem;
            transition: border 0.3s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary);
        }

        .form-select {
            width: 100%;
            padding: 0.8rem;
            border: 2px solid var(--light);
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
        }

        /* Notifications */
        .notification {
            position: fixed;
            top: 100px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            animation: slideInRight 0.5s ease;
            z-index: 2000;
            min-width: 300px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }

        .notification.success {
            background: var(--success);
        }

        .notification.error {
            background: var(--danger);
        }

        .notification.info {
            background: var(--primary);
        }

        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* Responsive Design */
        @media (max-width: 1200px) {
            .main-container {
                grid-template-columns: 200px 1fr;
            }
            .right-panel {
                display: none;
            }
        }

        @media (max-width: 768px) {
            .main-container {
                grid-template-columns: 1fr;
            }
            .sidebar {
                position: relative;
                margin-bottom: 2rem;
            }
            .header-content {
                flex-direction: column;
                gap: 1rem;
            }
            .status-bar {
                flex-wrap: wrap;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <a href="#" class="logo">🌸 BloomQuest</a>
            <div class="status-bar">
                <div class="status-item">
                    <span class="status-icon">👤</span>
                    <span id="player-name">Guest</span>
                </div>
                <div class="status-item">
                    <span class="status-icon">⭐</span>
                    <span>Level <span id="player-level">1</span></span>
                </div>
                <div class="status-item">
                    <span class="status-icon">💰</span>
                    <span id="player-balance">0.00 BC</span>
                </div>
                <div class="status-item">
                    <span class="status-icon">⛏️</span>
                    <span id="active-jobs">0</span> Jobs
                </div>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <div class="main-container">
        <!-- Sidebar Navigation -->
        <nav class="sidebar">
            <div class="nav-item active" onclick="showSection('dashboard')">
                <span class="nav-icon">🏠</span>
                <span>Dashboard</span>
            </div>
            <div class="nav-item" onclick="showSection('mining')">
                <span class="nav-icon">⛏️</span>
                <span>Mining</span>
            </div>
            <div class="nav-item" onclick="showSection('companions')">
                <span class="nav-icon">🤝</span>
                <span>Companions</span>
            </div>
            <div class="nav-item" onclick="showSection('patterns')">
                <span class="nav-icon">🔮</span>
                <span>Patterns</span>
            </div>
            <div class="nav-item" onclick="showSection('market')">
                <span class="nav-icon">📈</span>
                <span>Market</span>
            </div>
            <div class="nav-item" onclick="showSection('residue')">
                <span class="nav-icon">⚗️</span>
                <span>Residue Lab</span>
            </div>
            <div class="nav-item" onclick="showSection('stats')">
                <span class="nav-icon">📊</span>
                <span>Statistics</span>
            </div>
        </nav>

        <!-- Main Content Area -->
        <main class="content" id="main-content">
            <!-- Dashboard Section -->
            <div id="dashboard-section" class="content-section">
                <div class="content-header">
                    <h1 class="content-title">Dashboard</h1>
                    <p class="content-subtitle">Your BloomQuest command center</p>
                </div>

                <!-- Quick Stats Cards -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-title">Quick Stats</span>
                        <span class="card-badge badge-primary">Live</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                        <div style="text-align: center; padding: 1rem; background: var(--light); border-radius: 8px;">
                            <div style="font-size: 2rem; color: var(--primary);">⛏️</div>
                            <div style="font-size: 1.5rem; font-weight: bold;" id="total-mined">0</div>
                            <div style="color: #666;">Total Mined</div>
                        </div>
                        <div style="text-align: center; padding: 1rem; background: var(--light); border-radius: 8px;">
                            <div style="font-size: 2rem; color: var(--success);">🔮</div>
                            <div style="font-size: 1.5rem; font-weight: bold;" id="patterns-count">0</div>
                            <div style="color: #666;">Patterns</div>
                        </div>
                        <div style="text-align: center; padding: 1rem; background: var(--light); border-radius: 8px;">
                            <div style="font-size: 2rem; color: var(--warning);">📈</div>
                            <div style="font-size: 1.5rem; font-weight: bold;" id="market-trades">0</div>
                            <div style="color: #666;">Trades</div>
                        </div>
                        <div style="text-align: center; padding: 1rem; background: var(--light); border-radius: 8px;">
                            <div style="font-size: 2rem; color: var(--danger);">⚗️</div>
                            <div style="font-size: 1.5rem; font-weight: bold;" id="residue-amount">0</div>
                            <div style="color: #666;">Residue</div>
                        </div>
                    </div>
                </div>

                <!-- Active Mining Jobs -->
                <div class="card">
                    <div class="card-header">
                        <span class="card-title">Active Mining Jobs</span>
                        <button class="btn btn-primary btn-sm" onclick="startQuickMine()">
                            <span>⛏️</span> Quick Mine
                        </button>
                    </div>
                    <div id="active-jobs-list">
                        <p style="text-align: center; color: #999; padding: 2rem;">No active mining jobs</p>
                    </div>
                </div>
            </div>

            <!-- Mining Section -->
            <div id="mining-section" class="content-section" style="display: none;">
                <div class="content-header">
                    <h1 class="content-title">Mining Operations</h1>
                    <p class="content-subtitle">NEXTHASH-256 powered cryptocurrency mining</p>
                </div>

                <div class="card">
                    <div class="card-header">
                        <span class="card-title">Start New Mining Job</span>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Mining Type</label>
                        <select class="form-select" id="mining-type">
                            <option value="PATTERN_DISCOVERY">Pattern Discovery</option>
                            <option value="HASH_OPTIMIZATION">Hash Optimization</option>
                            <option value="RESIDUE_COLLECTION">Residue Collection</option>
                            <option value="GUARDIAN_ALIGNMENT">Guardian Alignment</option>
                            <option value="ECHO_RESONANCE">Echo Resonance</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Difficulty</label>
                        <select class="form-select" id="mining-difficulty">
                            <option value="1">Easy (1-2 min)</option>
                            <option value="2">Normal (2-3 min)</option>
                            <option value="3">Hard (3-5 min)</option>
                            <option value="4">Expert (5-10 min)</option>
                        </select>
                    </div>
                    <button class="btn btn-success" onclick="startMining()">
                        <span>⛏️</span> Start Mining
                    </button>
                </div>
            </div>

            <!-- Market Section -->
            <div id="market-section" class="content-section" style="display: none;">
                <div class="content-header">
                    <h1 class="content-title">Pattern Stock Market</h1>
                    <p class="content-subtitle">Trade pattern stocks for profit</p>
                </div>

                <div class="card">
                    <div class="card-header">
                        <span class="card-title">Market Overview</span>
                        <span class="card-badge badge-success" id="market-sentiment">1.0x</span>
                    </div>
                    <table class="market-table">
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Price</th>
                                <th>24h Change</th>
                                <th>Volume</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="market-table-body">
                            <!-- Market data will be inserted here -->
                        </tbody>
                    </table>
                </div>
            </div>
        </main>

        <!-- Right Panel - Activity Feed -->
        <aside class="right-panel">
            <h3 style="margin-bottom: 1rem;">Activity Feed</h3>
            <div class="activity-feed" id="activity-feed">
                <div class="activity-item">
                    Welcome to BloomQuest!
                </div>
            </div>
        </aside>
    </div>

    <!-- Modals -->
    <div class="modal" id="trade-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">Trade Pattern Stock</h2>
            </div>
            <div class="form-group">
                <label class="form-label">Action</label>
                <select class="form-select" id="trade-action">
                    <option value="buy">Buy</option>
                    <option value="sell">Sell</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">Amount</label>
                <input type="number" class="form-control" id="trade-amount" value="10" min="1">
            </div>
            <div class="btn-group">
                <button class="btn btn-success" onclick="executeTrade()">Execute Trade</button>
                <button class="btn btn-danger" onclick="closeModal('trade-modal')">Cancel</button>
            </div>
        </div>
    </div>

    <!-- Socket.IO -->
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>

    <!-- Game Script -->
    <script>
        // Initialize Socket.IO connection
        const socket = io();
        let sessionId = null;
        let currentSection = 'dashboard';
        let currentTradeSymbol = '';

        // Connect to server
        socket.on('connect', () => {
            console.log('Connected to BloomQuest server');
            initializeGame();
        });

        // Initialize game
        function initializeGame() {
            socket.emit('init_game', {}, (response) => {
                sessionId = response.session_id;
                updateUI(response);
                startPolling();
            });
        }

        // Update UI with game state
        function updateUI(data) {
            if (data.player) {
                document.getElementById('player-name').textContent = data.player.name;
                document.getElementById('player-level').textContent = data.player.level;
                document.getElementById('player-balance').textContent = data.player.balance.toFixed(2) + ' BC';
            }

            if (data.stats) {
                document.getElementById('total-mined').textContent = data.stats.total_mined.toFixed(0);
                document.getElementById('patterns-count').textContent = data.stats.patterns;
                document.getElementById('market-trades').textContent = data.stats.trades;
                document.getElementById('residue-amount').textContent = data.stats.residue.toFixed(0);
            }

            if (data.active_jobs !== undefined) {
                document.getElementById('active-jobs').textContent = data.active_jobs;
                updateActiveJobsList(data.jobs);
            }

            if (data.market) {
                updateMarketTable(data.market);
            }
        }

        // Update active jobs list
        function updateActiveJobsList(jobs) {
            const container = document.getElementById('active-jobs-list');
            if (!jobs || jobs.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No active mining jobs</p>';
                return;
            }

            let html = '';
            jobs.forEach(job => {
                const progressPercent = (job.progress * 100).toFixed(1);
                html += `
                    <div class="mining-job ${job.status === 'completed' ? 'complete' : ''}">
                        <div class="mining-job-header">
                            <span class="mining-job-id">${job.id.substring(0, 8)}</span>
                            <span>${job.type}</span>
                        </div>
                        <div class="progress-container">
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${progressPercent}%">
                                    ${progressPercent}%
                                </div>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                            <span>Est. Reward: ${job.reward.toFixed(2)} BC</span>
                            ${job.status === 'completed' ?
                                '<button class="btn btn-success btn-sm" onclick="collectReward(\'' + job.id + '\')">Collect</button>' :
                                '<span>Time left: ' + job.time_left + 's</span>'
                            }
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        }

        // Update market table
        function updateMarketTable(market) {
            const tbody = document.getElementById('market-table-body');
            if (!market.stocks) return;

            document.getElementById('market-sentiment').textContent = market.sentiment.toFixed(2) + 'x';

            let html = '';
            market.stocks.forEach(stock => {
                const changeClass = stock.change > 0 ? 'price-up' : 'price-down';
                const changeSymbol = stock.change > 0 ? '+' : '';
                html += `
                    <tr>
                        <td><strong>${stock.symbol}</strong></td>
                        <td>${stock.price.toFixed(2)} BC</td>
                        <td class="${changeClass}">${changeSymbol}${stock.change.toFixed(1)}%</td>
                        <td>${stock.volume}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" onclick="openTradeModal('${stock.symbol}')">
                                Trade
                            </button>
                        </td>
                    </tr>
                `;
            });
            tbody.innerHTML = html;
        }

        // Show section
        function showSection(section) {
            // Hide all sections
            document.querySelectorAll('.content-section').forEach(el => {
                el.style.display = 'none';
            });

            // Show selected section
            document.getElementById(section + '-section').style.display = 'block';

            // Update nav
            document.querySelectorAll('.nav-item').forEach(el => {
                el.classList.remove('active');
            });
            event.target.closest('.nav-item').classList.add('active');

            currentSection = section;

            // Load section data
            loadSectionData(section);
        }

        // Load section data
        function loadSectionData(section) {
            socket.emit('load_section', {section: section}, (response) => {
                updateUI(response);
            });
        }

        // Start quick mine
        function startQuickMine() {
            socket.emit('quick_mine', {}, (response) => {
                if (response.success) {
                    showNotification('Mining job started!', 'success');
                    addActivity('Started quick mining job');
                    updateUI(response);
                } else {
                    showNotification(response.error, 'error');
                }
            });
        }

        // Start mining with options
        function startMining() {
            const type = document.getElementById('mining-type').value;
            const difficulty = parseInt(document.getElementById('mining-difficulty').value);

            socket.emit('start_mining', {
                type: type,
                difficulty: difficulty
            }, (response) => {
                if (response.success) {
                    showNotification('Mining job started!', 'success');
                    addActivity('Started ' + type + ' mining');
                    updateUI(response);
                } else {
                    showNotification(response.error, 'error');
                }
            });
        }

        // Collect reward
        function collectReward(jobId) {
            socket.emit('collect_reward', {job_id: jobId}, (response) => {
                if (response.success) {
                    showNotification('Collected ' + response.reward.toFixed(2) + ' BC!', 'success');
                    addActivity('Collected mining reward: ' + response.reward.toFixed(2) + ' BC');
                    updateUI(response);
                } else {
                    showNotification(response.error, 'error');
                }
            });
        }

        // Open trade modal
        function openTradeModal(symbol) {
            currentTradeSymbol = symbol;
            document.getElementById('trade-modal').classList.add('active');
        }

        // Close modal
        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }

        // Execute trade
        function executeTrade() {
            const action = document.getElementById('trade-action').value;
            const amount = parseInt(document.getElementById('trade-amount').value);

            socket.emit('trade', {
                symbol: currentTradeSymbol,
                action: action,
                amount: amount
            }, (response) => {
                if (response.success) {
                    showNotification('Trade executed successfully!', 'success');
                    addActivity(action + ' ' + amount + ' ' + currentTradeSymbol);
                    closeModal('trade-modal');
                    updateUI(response);
                } else {
                    showNotification(response.error, 'error');
                }
            });
        }

        // Show notification
        function showNotification(message, type) {
            const notification = document.createElement('div');
            notification.className = 'notification ' + type;
            notification.textContent = message;
            document.body.appendChild(notification);

            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        // Add to activity feed
        function addActivity(message) {
            const feed = document.getElementById('activity-feed');
            const item = document.createElement('div');
            item.className = 'activity-item';
            item.textContent = new Date().toLocaleTimeString() + ' - ' + message;
            feed.insertBefore(item, feed.firstChild);

            // Keep only last 10 activities
            while (feed.children.length > 10) {
                feed.removeChild(feed.lastChild);
            }
        }

        // Poll for updates
        function startPolling() {
            setInterval(() => {
                socket.emit('get_update', {}, (response) => {
                    updateUI(response);
                });
            }, 5000);  // Update every 5 seconds
        }

        // Handle real-time events
        socket.on('job_completed', (data) => {
            showNotification('Mining job completed! Reward: ' + data.reward.toFixed(2) + ' BC', 'success');
            addActivity('Mining job completed: ' + data.reward.toFixed(2) + ' BC');
            updateUI(data);
        });

        socket.on('pattern_discovered', (data) => {
            showNotification('Pattern discovered: ' + data.pattern, 'info');
            addActivity('Discovered pattern: ' + data.pattern);
        });

        socket.on('market_update', (data) => {
            if (currentSection === 'market') {
                updateMarketTable(data.market);
            }
        });
    </script>
</body>
</html>
"""

# ═══════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ═══════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """Serve main game interface"""
    return INDEX_HTML

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# ═══════════════════════════════════════════════════════════════════════
# SOCKETIO EVENTS
# ═══════════════════════════════════════════════════════════════════════

@socketio.on('init_game')
def handle_init_game(data):
    """Initialize new game session"""
    session_id = str(uuid.uuid4())
    session['game_id'] = session_id

    # Create new game instance
    game = UnifiedGameInterface()
    game_sessions[session_id] = game

    # Create player
    player_data = game.create_player(f"Player_{session_id[:8]}", 1000.0)

    # Store player session
    player_sessions[session_id] = {
        "name": f"Player_{session_id[:8]}",
        "level": 1,
        "balance": 1000.0,
        "experience": 0,
        "total_mined": 0.0,
        "patterns": [],
        "residue": 0.0,
        "trades": 0
    }

    # Join room for updates
    join_room(session_id)

    # Return initial state
    return {
        "session_id": session_id,
        "player": player_sessions[session_id],
        "stats": {
            "total_mined": 0,
            "patterns": 0,
            "trades": 0,
            "residue": 0.0
        },
        "active_jobs": 0,
        "jobs": []
    }

@socketio.on('quick_mine')
def handle_quick_mine(data):
    """Start quick mining job"""
    session_id = session.get('game_id')
    if not session_id or session_id not in game_sessions:
        return {"success": False, "error": "Session not found"}

    game = game_sessions[session_id]
    player = player_sessions[session_id]

    # Start mining
    job = game.start_mining(player["name"])

    if job:
        # Start background thread to complete job
        def complete_job():
            time.sleep(job.duration if hasattr(job, 'duration') else 60)
            game.economy.process_mining(job.job_id)

            # Update player
            status = game.check_mining(job.job_id)
            if status["status"] == "completed":
                player["balance"] += status.get("reward", 0)
                player["total_mined"] += status.get("reward", 0)

                # Emit completion event
                socketio.emit('job_completed', {
                    "job_id": job.job_id,
                    "reward": status.get("reward", 0)
                }, room=session_id)

        threading.Thread(target=complete_job, daemon=True).start()

        return {
            "success": True,
            "job_id": job.job_id,
            "player": player,
            "active_jobs": 1
        }

    return {"success": False, "error": "Failed to start mining job"}

@socketio.on('start_mining')
def handle_start_mining(data):
    """Start mining with specific options"""
    session_id = session.get('game_id')
    if not session_id or session_id not in game_sessions:
        return {"success": False, "error": "Session not found"}

    game = game_sessions[session_id]
    player = player_sessions[session_id]

    job_type = data.get('type', 'PATTERN_DISCOVERY')
    difficulty = data.get('difficulty', 2)

    # Create mining job
    job_enum = MiningJobType[job_type] if hasattr(MiningJobType, job_type) else None

    job = game.economy.create_mining_job(
        player_id=player["name"],
        companion_id=f"{player['name']}_starter",
        job_type=job_enum,
        difficulty=difficulty
    )

    if job:
        # Start completion thread
        def complete_job():
            time.sleep(job.duration)
            game.economy.process_mining(job.job_id)

            socketio.emit('job_completed', {
                "job_id": job.job_id,
                "reward": job.final_reward
            }, room=session_id)

        threading.Thread(target=complete_job, daemon=True).start()

        return {
            "success": True,
            "job_id": job.job_id,
            "player": player
        }

    return {"success": False, "error": "Failed to start mining job"}

@socketio.on('collect_reward')
def handle_collect_reward(data):
    """Collect mining reward"""
    session_id = session.get('game_id')
    if not session_id or session_id not in game_sessions:
        return {"success": False, "error": "Session not found"}

    game = game_sessions[session_id]
    player = player_sessions[session_id]

    job_id = data.get('job_id')
    status = game.check_mining(job_id)

    if status["status"] == "completed":
        reward = status.get("reward", 0)
        player["balance"] += reward
        player["total_mined"] += reward

        return {
            "success": True,
            "reward": reward,
            "player": player
        }

    return {"success": False, "error": "Job not completed"}

@socketio.on('trade')
def handle_trade(data):
    """Execute market trade"""
    session_id = session.get('game_id')
    if not session_id or session_id not in game_sessions:
        return {"success": False, "error": "Session not found"}

    game = game_sessions[session_id]
    player = player_sessions[session_id]

    symbol = data.get('symbol')
    action = data.get('action')
    amount = data.get('amount', 10)

    # Execute trade
    success = game.economy.trade_pattern_stock(
        player["name"], symbol, action, amount
    )

    if success:
        player["trades"] += 1
        # Update balance from wallet
        wallet = game.economy.wallet_manager.get_wallet_by_owner(player["name"])
        if wallet:
            player["balance"] = wallet.balance

        return {
            "success": True,
            "player": player
        }

    return {"success": False, "error": "Trade failed"}

@socketio.on('get_update')
def handle_get_update(data):
    """Get current game state update"""
    session_id = session.get('game_id')
    if not session_id or session_id not in game_sessions:
        return {}

    game = game_sessions[session_id]
    player = player_sessions[session_id]

    # Get active jobs
    jobs = []
    for job_id in game.economy.active_jobs:
        status = game.check_mining(job_id)
        if status["status"] == "active":
            jobs.append({
                "id": job_id,
                "type": "Mining",
                "progress": status["progress"],
                "reward": status["estimated_reward"],
                "time_left": int(status["duration"] - status["elapsed"]),
                "status": "active"
            })

    # Get market data
    market_stocks = []
    for symbol, stock in list(game.economy.stock_market.stocks.items())[:10]:
        change = ((stock.current_price - stock.opening_price) /
                 stock.opening_price * 100)
        market_stocks.append({
            "symbol": symbol,
            "price": stock.current_price,
            "change": change,
            "volume": stock.volume_24h
        })

    return {
        "player": player,
        "active_jobs": len(jobs),
        "jobs": jobs,
        "market": {
            "sentiment": game.economy._calculate_market_sentiment(),
            "stocks": market_stocks
        },
        "stats": {
            "total_mined": player["total_mined"],
            "patterns": len(player["patterns"]),
            "trades": player["trades"],
            "residue": player["residue"]
        }
    }

@socketio.on('load_section')
def handle_load_section(data):
    """Load specific section data"""
    session_id = session.get('game_id')
    if not session_id or session_id not in game_sessions:
        return {}

    section = data.get('section')
    game = game_sessions[session_id]
    player = player_sessions[session_id]

    # Return section-specific data
    if section == 'market':
        market_data = []
        for symbol, stock in game.economy.stock_market.stocks.items():
            change = ((stock.current_price - stock.opening_price) /
                     stock.opening_price * 100)
            market_data.append({
                "symbol": symbol,
                "price": stock.current_price,
                "change": change,
                "volume": stock.volume_24h
            })

        return {
            "market": {
                "sentiment": game.economy._calculate_market_sentiment(),
                "stocks": market_data
            }
        }

    return {"player": player}

# ═══════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

def run_server(host='0.0.0.0', port=5000, debug=False):
    """Run the Flask web server"""
    print(f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                     BLOOMQUEST WEB UI                           ║
    ║                  NEXTHASH-256 Mining Adventure                  ║
    ╚══════════════════════════════════════════════════════════════════╝

    Server starting at: http://{host}:{port}
    Open your browser to play!

    Press Ctrl+C to stop the server.
    """)

    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    run_server(debug=True)