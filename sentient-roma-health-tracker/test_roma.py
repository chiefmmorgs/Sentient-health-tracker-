from roma_engine.sentient_roma_runner import ROMARunner

def test_weekly_flow():
    r = ROMARunner()
    out = r.run_weekly({"steps": 10000})
    assert out and "ok" in out
