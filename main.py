import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import VehicleAgent

def main():
    print("🚗 Starting Vehicle Search Application...")
    agent = VehicleAgent()
    agent.run()

if __name__ == "__main__":
    main()
