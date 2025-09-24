from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get("/api/simple/status")
def status():
    return jsonify({
        "ok": True,
        "service": "roma",
        "endpoints": ["/api/simple/status", "/api/simple/execute", "/api/simple/research", "/api/simple/analysis"]
    })

@app.post("/api/simple/execute")
def simple_execute():
    payload = request.get_json(silent=True) or {}
    goal = payload.get("goal") or ""
    # trivial behavior to prove the pipe works
    if goal.strip().lower() == "reply with exactly the word ok.":
        return jsonify({"final_output": "OK", "status": "completed"})
    return jsonify({"final_output": f"Echo: {goal}", "status": "completed"})

@app.post("/api/simple/research")
def simple_research():
    payload = request.get_json(silent=True) or {}
    return jsonify({"status": "ok", "topic": payload.get("topic")})

@app.post("/api/simple/analysis")
def simple_analysis():
    payload = request.get_json(silent=True) or {}
    if "data_description" not in payload:
        return jsonify({"error":"Missing required fields: data_description"}), 400
    return jsonify({"status":"ok","summary":"placeholder"})

if __name__ == "__main__":
    # default to 0.0.0.0:5000 unless you override in Dockerfile
    app.run(host="0.0.0.0", port=5000)
