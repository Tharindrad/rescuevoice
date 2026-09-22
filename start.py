"""RescueVoice local demo launcher.

Starts FastAPI on :8000. Run `npm install && npm run dev` in a second terminal
for the React dashboard on :5173.
"""
import os
import subprocess
import sys

if __name__ == "__main__":
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", os.path.join(os.path.dirname(__file__), "backend"))
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"], env=env)
