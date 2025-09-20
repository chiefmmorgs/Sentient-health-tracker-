import subprocess, sys

def run(cmd):
    print(">>", " ".join(cmd))
    subprocess.check_call(cmd)

run([sys.executable, "-m", "pytest", "-q"])
