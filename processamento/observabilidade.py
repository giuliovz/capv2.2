import json
from datetime import datetime
from pathlib import Path

from config import LOGS_DIR


class ObservabilidadeExecucao:
    def __init__(self, run_id: str):
        self.run_id = run_id
        LOGS_DIR.mkdir(exist_ok=True, parents=True)
        self.path = Path(LOGS_DIR) / "execucoes.jsonl"

    def evento(self, tipo: str, payload: dict):
        registro = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "tipo": tipo,
            "payload": payload,
        }
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
