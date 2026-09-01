import time
import hashlib
import re
import threading
from dataclasses import dataclass
from typing import Optional, List, Dict, Callable

@dataclass
class TelemetryFrame:
    frame_id: str
    timestamp: float
    source_system: str
    data: dict
    checksum: str

class TelemetryBridge:
    def __init__(self):
        self.history: Dict[str, List[TelemetryFrame]] = {}
        self.subscriptions: List[tuple[str, Callable]] = []
        self._lock = threading.Lock()

    def ingest(self, source: str, data: dict) -> TelemetryFrame:
        ts = time.time()
        frame_id = f"{source}-{ts}"
        data_str = str(data).encode('utf-8')
        checksum = hashlib.sha256(data_str).hexdigest()
        frame = TelemetryFrame(frame_id, ts, source, data, checksum)

        with self._lock:
            if source not in self.history:
                self.history[source] = []
            self.history[source].append(frame)
            
            for pattern, callback in self.subscriptions:
                if re.match(pattern, source):
                    callback(frame)
        return frame

    def get_latest(self, source: str) -> Optional[TelemetryFrame]:
        with self._lock:
            frames = self.history.get(source, [])
            return frames[-1] if frames else None

    def get_history(self, source: str, limit: int) -> List[TelemetryFrame]:
        with self._lock:
            return self.history.get(source, [])[-limit:]

    def export_apex_format(self) -> dict:
        with self._lock:
            exported = []
            for source, frames in self.history.items():
                if frames:
                    last_frame = frames[-1]
                    exported.append({
                        "source": source,
                        "timestamp": last_frame.timestamp,
                        "data": last_frame.data
                    })
            return {"telemetry_sync": exported}

    def subscribe(self, source_pattern: str, callback: Callable) -> None:
        with self._lock:
            self.subscriptions.append((source_pattern, callback))
