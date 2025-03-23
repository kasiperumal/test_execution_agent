import subprocess
import os
import re

def run_karate_tests():
    """Execute Karate BDD tests and return correct test results summary after execution."""
    try:
        karate_jar = os.path.join('libs', 'karate-1.4.0.jar')
        test_dir = os.path.abspath("karate-tests")

        if not os.path.exists(test_dir):
            print(f"❌ Test directory not found: {test_dir}")
            return {"error": "Test directory not found"}

        # ✅ Run Karate and capture full output
        process = subprocess.Popen(
            ['/usr/lib/jvm/java-17-openjdk-amd64/bin/java', '-jar', karate_jar, test_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        karate_output, karate_error = process.communicate()  # Wait and capture full output

        # 🔍 Debugging: Print full Karate output
        print("\n🔹 Karate Raw Output:\n", karate_output)

        # ✅ Extract only the last summary block using regex
        summary_matches = re.findall(r"scenarios:\s*(\d+)\s*\|\s*passed:\s*(\d+)\s*\|\s*failed:\s*(\d+)", karate_output)

        if summary_matches:
            # Get the last occurrence to avoid older logs
            total_scenarios, passed_tests, failed_tests = map(int, summary_matches[-1])
        else:
            print("❌ Could not parse test results correctly!")
            return {"error": "Failed to parse test results"}

        # ✅ Build the final test report
        summary = {
            "scenarios": total_scenarios,
            "passed": passed_tests,
            "failed": failed_tests,
            "status": "success" if failed_tests == 0 else "failed"
        }

        return summary

    except subprocess.SubprocessError as e:
        print("❌ Karate execution failed:", str(e))
        return {"error": "Karate execution failed", "details": str(e)}

if __name__ == "__main__":
    test_results = run_karate_tests()
    print("\n✅ Karate Test Summary:",test_results)