#!/usr/bin/env python3
"""
Test Script for BloomQuest Web UI Interactions
==============================================
Tests all Socket.IO events and verifies web UI functionality.
"""

import socketio
import time
import json
import requests
from typing import Dict, Any

class WebUITester:
    def __init__(self, url: str = "http://localhost:5001"):
        self.url = url
        self.sio = socketio.Client()
        self.connected = False
        self.test_results = {}
        self.session_id = None
        self.player_data = None

        # Set up event handlers
        self.setup_handlers()

    def setup_handlers(self):
        """Set up Socket.IO event handlers"""

        @self.sio.on('connect')
        def on_connect():
            print("✅ Connected to WebSocket server")
            self.connected = True
            self.test_results['connection'] = True

        @self.sio.on('disconnect')
        def on_disconnect():
            print("🔌 Disconnected from server")
            self.connected = False

        @self.sio.on('game_initialized')
        def on_game_initialized(data):
            print(f"✅ Game initialized for player: {data.get('player_name')}")
            self.session_id = data.get('session_id')
            self.player_data = data.get('player_data')
            self.test_results['game_init'] = True

        @self.sio.on('mining_started')
        def on_mining_started(data):
            print(f"✅ Mining job started: {data.get('job_id')}")
            self.test_results['mining_start'] = True

        @self.sio.on('job_update')
        def on_job_update(data):
            print(f"📊 Job update: {data.get('job_id')} - Progress: {data.get('progress', 0)*100:.1f}%")
            self.test_results['job_update'] = True

        @self.sio.on('job_complete')
        def on_job_complete(data):
            print(f"✅ Job completed! Reward: {data.get('reward', 0)} BC")
            self.test_results['job_complete'] = True

        @self.sio.on('stats_update')
        def on_stats_update(data):
            print(f"📈 Stats updated - Balance: {data.get('balance', 0)} BC")
            self.test_results['stats_update'] = True

        @self.sio.on('market_update')
        def on_market_update(data):
            print(f"📊 Market data received: {len(data.get('patterns', []))} patterns")
            self.test_results['market_update'] = True

        @self.sio.on('error')
        def on_error(data):
            print(f"❌ Error: {data.get('message')}")

    def connect(self):
        """Connect to the server"""
        try:
            print(f"🔗 Connecting to {self.url}...")
            self.sio.connect(self.url)
            time.sleep(1)
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def test_game_initialization(self):
        """Test game initialization"""
        print("\n📋 Testing game initialization...")

        self.sio.emit('init_game', {
            'player_name': 'TestPlayer'
        })
        time.sleep(2)

        if self.test_results.get('game_init'):
            print("✅ Game initialization successful!")
            return True
        else:
            print("❌ Game initialization failed")
            return False

    def test_quick_mine(self):
        """Test quick mine functionality"""
        print("\n⛏️ Testing quick mine...")

        self.sio.emit('quick_mine', {})
        time.sleep(2)

        if self.test_results.get('mining_start'):
            print("✅ Quick mine started successfully!")
            # Wait for job to complete
            time.sleep(5)
            return True
        else:
            print("❌ Quick mine failed")
            return False

    def test_mining_with_companion(self):
        """Test mining with specific companion"""
        print("\n🤝 Testing companion mining...")

        self.sio.emit('start_mining', {
            'companion_index': 0,
            'difficulty': 3
        })
        time.sleep(2)

        if self.test_results.get('mining_start'):
            print("✅ Companion mining started!")
            return True
        else:
            print("❌ Companion mining failed")
            return False

    def test_collect_rewards(self):
        """Test collecting mining rewards"""
        print("\n💰 Testing reward collection...")

        # First start a quick job
        self.sio.emit('quick_mine', {})
        time.sleep(6)  # Wait for job to complete

        # Then collect all
        self.sio.emit('collect_all', {})
        time.sleep(2)

        if self.test_results.get('stats_update'):
            print("✅ Rewards collected successfully!")
            return True
        else:
            print("❌ Reward collection failed")
            return False

    def test_market_data(self):
        """Test market data retrieval"""
        print("\n📈 Testing market data...")

        self.sio.emit('get_market_data', {})
        time.sleep(2)

        if self.test_results.get('market_update'):
            print("✅ Market data received!")
            return True
        else:
            print("❌ Market data failed")
            return False

    def test_http_endpoints(self):
        """Test HTTP endpoints"""
        print("\n🌐 Testing HTTP endpoints...")

        tests_passed = 0

        # Test homepage
        try:
            response = requests.get(f"{self.url}/")
            if response.status_code == 200:
                print("✅ Homepage accessible")
                tests_passed += 1
            else:
                print(f"❌ Homepage returned {response.status_code}")
        except Exception as e:
            print(f"❌ Homepage error: {e}")

        # Test API endpoint
        try:
            response = requests.get(f"{self.url}/api/status")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API status: {data.get('status')}")
                tests_passed += 1
            else:
                print(f"❌ API status returned {response.status_code}")
        except Exception as e:
            print(f"❌ API error: {e}")

        return tests_passed == 2

    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("🧪 BLOOMQUEST WEB UI INTERACTION TEST SUITE")
        print("="*60)

        # Track overall results
        all_tests = []

        # Test 1: Connection
        if not self.connect():
            print("❌ Cannot connect to server. Is it running on port 5001?")
            return False
        all_tests.append(('WebSocket Connection', True))

        # Test 2: Game initialization
        result = self.test_game_initialization()
        all_tests.append(('Game Initialization', result))

        # Test 3: Quick mine
        result = self.test_quick_mine()
        all_tests.append(('Quick Mine', result))

        # Test 4: Companion mining
        result = self.test_mining_with_companion()
        all_tests.append(('Companion Mining', result))

        # Test 5: Collect rewards
        result = self.test_collect_rewards()
        all_tests.append(('Reward Collection', result))

        # Test 6: Market data
        result = self.test_market_data()
        all_tests.append(('Market Data', result))

        # Test 7: HTTP endpoints
        result = self.test_http_endpoints()
        all_tests.append(('HTTP Endpoints', result))

        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)

        passed = 0
        for test_name, result in all_tests:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
            if result:
                passed += 1

        print(f"\nTotal: {passed}/{len(all_tests)} tests passed")

        if passed == len(all_tests):
            print("\n🎉 ALL TESTS PASSED! Web UI is fully functional!")
        elif passed > len(all_tests) * 0.7:
            print("\n⚠️ Most tests passed but some interactions need attention.")
        else:
            print("\n❌ Multiple failures detected. Web UI needs fixes.")

        # Disconnect
        self.sio.disconnect()

        return passed == len(all_tests)

def main():
    """Main test runner"""
    import sys

    # Check command line args for custom URL
    url = "http://localhost:5001"
    if len(sys.argv) > 1:
        url = sys.argv[1]

    print(f"🎮 Testing BloomQuest Web UI at {url}")
    print("Please ensure the server is running first!")
    print()

    tester = WebUITester(url)
    success = tester.run_all_tests()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()