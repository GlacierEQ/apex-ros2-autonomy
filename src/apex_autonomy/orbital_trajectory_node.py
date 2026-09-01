import json
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class OrbitalTrajectoryPoint:
    t: float
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    mass: float

class OrbitalTrajectoryNode:
    """
    Executes orbital trajectories.
    Expected schema for trajectory JSON:
    [
        {"t": 0.0, "x": 100.0, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 7.5, "vz": 0.0, "mass": 5000.0},
        ...
    ]
    """
    def load_trajectory(self, path: str) -> List[OrbitalTrajectoryPoint]:
        with open(path, 'r') as f:
            data = json.load(f)
        return [OrbitalTrajectoryPoint(**pt) for pt in data]

    def execute_trajectory(self, points: List[OrbitalTrajectoryPoint], transport: Any) -> dict:
        errors = self.validate_trajectory(points)
        if errors:
            return {"status": "error", "details": errors}
        return {"status": "executing", "point_count": len(points)}

    def interpolate(self, points: List[OrbitalTrajectoryPoint], t: float) -> OrbitalTrajectoryPoint:
        if not points:
            raise ValueError("Cannot interpolate empty trajectory")
        if t <= points[0].t:
            return points[0]
        if t >= points[-1].t:
            return points[-1]
        
        for i in range(len(points) - 1):
            p0 = points[i]
            p1 = points[i + 1]
            if p0.t <= t <= p1.t:
                dt = p1.t - p0.t
                ratio = (t - p0.t) / dt if dt > 0 else 0
                return OrbitalTrajectoryPoint(
                    t=t,
                    x=p0.x + (p1.x - p0.x) * ratio,
                    y=p0.y + (p1.y - p0.y) * ratio,
                    z=p0.z + (p1.z - p0.z) * ratio,
                    vx=p0.vx + (p1.vx - p0.vx) * ratio,
                    vy=p0.vy + (p1.vy - p0.vy) * ratio,
                    vz=p0.vz + (p1.vz - p0.vz) * ratio,
                    mass=p0.mass + (p1.mass - p0.mass) * ratio
                )
        return points[-1]

    def validate_trajectory(self, points: List[OrbitalTrajectoryPoint]) -> List[str]:
        errors = []
        if not points:
            return ["Trajectory is empty"]
        for i in range(len(points) - 1):
            if points[i].t >= points[i+1].t:
                errors.append(f"Non-monotonic timestamp at index {i+1}")
        return errors
