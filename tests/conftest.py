import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BOOKINGS_DB", str(tmp_path / "reservas.db"))
    monkeypatch.delenv("NOTIFICATION_URL", raising=False)
    with TestClient(app) as cliente:
        yield cliente


@pytest.fixture(scope="session")
def servidor(tmp_path_factory):
    pasta = tmp_path_factory.mktemp("servidor")
    with socket.socket() as soquete:
        soquete.bind(("127.0.0.1", 0))
        porta = soquete.getsockname()[1]
    url = f"http://127.0.0.1:{porta}"
    ambiente = {**os.environ, "BOOKINGS_DB": str(pasta / "reservas.db")}
    ambiente.pop("NOTIFICATION_URL", None)
    processo = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(porta)],
        env=ambiente,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    for _ in range(100):
        if processo.poll() is not None:
            raise RuntimeError(f"Servidor encerrou: {processo.stderr.read().decode()}")
        try:
            with urlopen(f"{url}/api/health", timeout=0.2) as resposta:
                if resposta.status == 200:
                    break
        except (URLError, TimeoutError):
            time.sleep(0.1)
    else:
        processo.terminate()
        raise RuntimeError("Servidor não iniciou em 10 segundos")
    yield url
    processo.terminate()
    try:
        processo.wait(timeout=5)
    except subprocess.TimeoutExpired:
        processo.kill()
        processo.wait(timeout=5)


@pytest.fixture(scope="session")
def browser_type_launch_args():
    chrome = shutil.which("google-chrome")
    if chrome:
        return {"executable_path": chrome, "args": ["--no-sandbox"]}
    return {}
