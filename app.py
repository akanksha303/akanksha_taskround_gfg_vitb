from flask import Flask, render_template, request, send_from_directory
import subprocess
import os

app = Flask(__name__)

# Predefined problems with test cases
problems = {
    1: {
        "title": "Sum of Two Numbers",
        "description": "Write a function to return the sum of two numbers.",
        "test_cases": [
            {"input": "2 3", "output": "5"},
            {"input": "10 20", "output": "30"},
            {"input": "0 0", "output": "0"},
        ],
    },
    2: {
        "title": "Factorial of a Number",
        "description": "Write a function to calculate the factorial of a number.",
        "test_cases": [
            {"input": "5", "output": "120"},
            {"input": "3", "output": "6"},
            {"input": "0", "output": "1"},
        ],
    },
}

@app.route("/")
def index():
    return render_template("index.html", problems=problems)

@app.route("/submit", methods=["POST"])
def submit():
    problem_id = int(request.form["problem_id"])
    user_code = request.form["code"]
    problem = problems.get(problem_id)

    if not problem:
        return "Invalid problem ID", 400

    results = []
    score = 0
    for case in problem["test_cases"]:
        try:
            # Save user code to a temporary file
            with open("temp_code.py", "w") as f:
                f.write(user_code)

            # Execute the user code and pass the input
            process = subprocess.run(
                ["python3", "temp_code.py"],
                input=case["input"],
                text=True,
                capture_output=True,
                timeout=2,
            )
            user_output = process.stdout.strip()
            if user_output == case["output"]:
                results.append({"input": case["input"], "expected": case["output"], "output": user_output, "status": "Pass"})
                score += 1
            else:
                results.append({"input": case["input"], "expected": case["output"], "output": user_output, "status": "Fail"})
        except Exception as e:
            results.append({"input": case["input"], "expected": case["output"], "output": str(e), "status": "Error"})

    percentage_score = (score / len(problem["test_cases"])) * 100
    return render_template("results.html", results=results, score=percentage_score, problem_id=problem_id, problems=problems)

if __name__ == "__main__":
    app.run(debug=True)

