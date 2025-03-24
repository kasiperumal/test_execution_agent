import subprocess
import os
import jdk
import re

def run_karate_tests(test_cases_json):
    """Execute Karate tests directly from JSON input without creating files."""
    java_home = jdk.install('11')
    os.environ['JAVA_HOME'] = java_home
    os.environ['PATH'] = f"{java_home}/bin:" + os.environ['PATH']

    try:
        # ✅ Render-compatible paths
        base_dir = "/opt/render/project/src"  # Render's default deployment directory
        karate_jar = os.path.join(base_dir, 'libs', 'karate-1.4.0.jar')
        test_dir = os.path.join(base_dir, 'karate-tests')

        # ✅ Ensure test directory exists (critical for Render)
        os.makedirs(test_dir, exist_ok=True, mode=0o755)
        print(f"🔍 Checking test directory: {test_dir}")
        print(f"🔍 Directory contents: {os.listdir(test_dir)}")

        if not os.path.exists(karate_jar):
            print(f"❌ Karate JAR not found: {karate_jar}")
            return {"error": "Karate JAR not found"}

        # ✅ Run Karate with explicit paths
        cmd = [
            'java', '-jar', karate_jar,
            test_dir,
            '-o', os.path.join(test_dir, 'reports')  # Output directory for reports
        ]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        karate_output, karate_error = process.communicate()

        # ✅ Enhanced debugging
        print("\n🔹 Karate STDOUT:\n", karate_output)
        print("\n🔹 Karate STDERR:\n", karate_error)

        # ✅ Improved regex pattern for summary
        summary_pattern = r"scenarios:\s*(\d+)\s*\|\s*passed:\s*(\d+)\s*\|\s*failed:\s*(\d+)"
        summary_matches = re.findall(summary_pattern, karate_output)

        if summary_matches:
            total_scenarios, passed_tests, failed_tests = map(int, summary_matches[-1])
            status = "success" if failed_tests == 0 else "failed"
        else:
            print("❌ No valid test summary found!")
            return {
                "error": "No test summary found",
                "raw_output": karate_output,
                "raw_error": karate_error
            }

        return {
            "scenarios": total_scenarios,
            "passed": passed_tests,
            "failed": failed_tests,
            "status": status,
            "reports_dir": os.path.join(test_dir, 'reports')
        }

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        return {"error": str(e), "type": type(e)._name_}


if __name__ == "__main__":
    test_results = run_karate_tests()
    print("\n✅ Final Test Summary:",test_results)