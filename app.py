from flask import Flask, render_template, request, jsonify
import re
import ast

app = Flask(__name__)

SUPPORTED_LANGS = ["python", "javascript", "cpp", "java"]

# -------------------------
# Simple template generator
# -------------------------

def generate_code(prompt: str, language: str) -> str:
    p = prompt.lower().strip()
    if language == "python":
        return generate_python(p)
    if language == "javascript":
        return generate_js(p)
    if language == "cpp":
        return generate_cpp(p)
    if language == "java":
        return generate_java(p)
    return "// Language not supported yet."

def generate_python(p: str) -> str:
    if "calculator" in p:
        return """# Simple Python Calculator
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b if b != 0 else float('inf')

if __name__ == "__main__":
    print("Calculator: add/sub/mul/div")
    op = input("Operation: ")
    a = float(input("a = "))
    b = float(input("b = "))
    ops = {"add": add, "sub": sub, "mul": mul, "div": div}
    if op in ops:
        print("Result:", ops[op](a, b))
    else:
        print("Unknown operation")
"""
    if "todo" in p or "to-do" in p:
        return """# Minimal CLI To-Do
todos = []
def show():
    print("\\nYour To-Dos:")
    for i, t in enumerate(todos, 1):
        print(f"{i}. {t}")
while True:
    cmd = input("\\n(add/list/quit): ").strip().lower()
    if cmd == "add":
        todos.append(input("Task: ").strip())
    elif cmd == "list":
        show()
    elif cmd == "quit":
        break
    else:
        print("Try: add, list, quit")
"""
    if "fizz" in p:
        return """# FizzBuzz
for i in range(1, 101):
    out = ""
    if i % 3 == 0: out += "Fizz"
    if i % 5 == 0: out += "Buzz"
    print(out or i)
"""
    if "guess" in p:
        return """# Number Guessing Game
import random
secret = random.randint(1, 100)
while True:
    g = int(input("Guess 1-100: "))
    if g == secret:
        print("Correct!")
        break
    print("Too low" if g < secret else "Too high")
"""
    # Default scaffold
    return """# Starter Python Program
def main():
    print("Hello from CodePal!")
if __name__ == "__main__":
    main()
"""

def generate_js(p: str) -> str:
    if "calculator" in p:
        return """// Simple JS Calculator (Node)
function calc(op, a, b){
  const ops = {
    add: (x,y)=>x+y, sub:(x,y)=>x-y, mul:(x,y)=>x*y, div:(x,y)=>y!==0?x/y:Infinity
  };
  return ops[op] ? ops[op](a,b) : "Unknown op";
}
console.log(calc("add", 2, 3));
"""
    if "todo" in p or "to-do" in p:
        return """// Minimal To-Do in JS
const todos = [];
function add(task){ todos.push(task); }
function list(){ console.log(todos.map((t,i)=>`${i+1}. ${t}`).join("\\n")); }
add("Learn JS"); add("Build CodePal"); list();
"""
    if "fizz" in p:
        return """// FizzBuzz
for (let i=1;i<=100;i++){
  let out = "";
  if (i%3===0) out += "Fizz";
  if (i%5===0) out += "Buzz";
  console.log(out || i);
}
"""
    if "guess" in p:
        return """// Number Guessing Game (Browser)
let secret = Math.floor(Math.random()*100)+1;
function guess(n){
  if(n===secret){ console.log("Correct!"); return true; }
  console.log(n<secret? "Too low":"Too high"); return false;
}
"""
    return """// Starter JS
console.log("Hello from CodePal!");
"""

def generate_cpp(p: str) -> str:
    if "fizz" in p:
        return r"""#include <bits/stdc++.h>
using namespace std;
int main(){
  for(int i=1;i<=100;i++){
    string out="";
    if(i%3==0) out+="Fizz";
    if(i%5==0) out+="Buzz";
    cout << (out.size()? out: to_string(i)) << "\n";
  }
}
"""
    return r"""#include <bits/stdc++.h>
using namespace std;
int main(){ cout<<"Hello from CodePal!"<<endl; }
"""

def generate_java(p: str) -> str:
    if "fizz" in p:
        return """public class Main {
  public static void main(String[] args){
    for(int i=1;i<=100;i++){
      String out="";
      if(i%3==0) out+="Fizz";
      if(i%5==0) out+="Buzz";
      System.out.println(out.isEmpty()? i: out);
    }
  }
}
"""
    return """public class Main {
  public static void main(String[] args){
    System.out.println("Hello from CodePal!");
  }
}
"""

# -------------------------
# Explainer
# -------------------------

def explain_code(code: str, language: str) -> str:
    lines = code.splitlines()
    annotated = []
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        hint = ""
        if stripped.startswith("#") or stripped.startswith("//"):
            hint = " (comment)"
        elif any(k in stripped for k in ["def ", "function ", "class "]):
            hint = " (defines a function or class)"
        elif "=" in stripped and "==" not in stripped and not stripped.startswith(("==", "!==")):
            hint = " (assigns a value)"
        elif "(" in stripped and ")" in stripped and ";" in line:
            hint = " (likely a statement or function call)"
        annotated.append(f"{idx:>3}: {line}{hint}")
    summary = "This code was analyzed line-by-line. Comments, definitions, assignments, and calls were highlighted."
    return summary + "\n\n" + "\n".join(annotated)

# -------------------------
# Debugger (basic)
# -------------------------

def debug_code(code: str, language: str):
    issues = []
    suggestion = ""

    if language == "python":
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(f"Python SyntaxError: {e.msg} at line {e.lineno}, col {e.offset}")
            # Simple suggestion
            suggestion = "Check for missing colons, unmatched quotes/parentheses, or bad indentation."
        else:
            suggestion = "No syntax errors detected. Consider logic checks or unit tests."
    else:
        # Very light static checks for other langs
        # Parentheses/brace balance
        paren = code.count("(") - code.count(")")
        brace = code.count("{") - code.count("}")
        bracket = code.count("[") - code.count("]")
        if paren or brace or bracket:
            issues.append(f"Unbalanced delimiters: ()={paren}, {{}}={brace}, []={bracket}")
            suggestion = "Ensure all parentheses/braces/brackets are properly closed."
        if language in ("javascript", "java", "cpp"):
            # Semicolon hint
            if language != "javascript" and any(re.search(r"System\.out\.println\(", code)) and ";" not in code:
                issues.append("Missing semicolons may cause compile errors.")
        if not issues:
            suggestion = "No obvious structural issues found. If it fails, check your toolchain or run-time errors."

    return {
        "issues": issues,
        "suggestion": suggestion
    }

# -------------------------
# Routes
# -------------------------

@app.route("/")
def index():
    return render_template("index.html", languages=SUPPORTED_LANGS)

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(force=True)
    prompt = data.get("prompt","")
    language = data.get("language","python").lower()
    if language not in SUPPORTED_LANGS:
        return jsonify({"ok": False, "error": "Unsupported language"}), 400
    code = generate_code(prompt, language)
    return jsonify({"ok": True, "code": code})

@app.route("/api/explain", methods=["POST"])
def api_explain():
    data = request.get_json(force=True)
    code = data.get("code","")
    language = data.get("language","python").lower()
    explanation = explain_code(code, language)
    return jsonify({"ok": True, "explanation": explanation})

@app.route("/api/debug", methods=["POST"])
def api_debug():
    data = request.get_json(force=True)
    code = data.get("code","")
    language = data.get("language","python").lower()
    result = debug_code(code, language)
    return jsonify({"ok": True, **result})

if __name__ == "__main__":
    app.run(debug=True)
