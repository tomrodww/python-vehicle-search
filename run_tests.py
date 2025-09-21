import subprocess
import sys

def run_tests():
    print("Running Vehicle Search Tests...")
    print("=" * 50)
    
    try:
        # Run pytest with verbose output
        subprocess.run([
            sys.executable, 
            "-m", 
            "pytest",   # testing framework
            "tests/",   # specifies the test directory location
            "-v",       # shows detailed information about each test
            "--tb=short"  # short traceback format
        ], check=True)
        
        print("\n✅ All tests passed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ pytest not found. Install it with: pip install pytest")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
