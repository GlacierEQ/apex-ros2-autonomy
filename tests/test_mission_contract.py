import os
import sys
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from apex_autonomy.mission_contract import MissionContractExecutor, MissionPhase, InvalidTransitionError
from apex_autonomy.mission_transport import MockMissionTransport
from apex_autonomy.telemetry_bridge import TelemetryBridge
from apex_autonomy.orbital_trajectory_node import OrbitalTrajectoryNode, OrbitalTrajectoryPoint

@pytest.fixture
def mock_transport():
    return MockMissionTransport()

@pytest.fixture
def test_changeset_json(tmp_path):
    data = {
        "operation_id": "op-1234",
        "actions": [
            {"action_type": "NAVIGATE", "parameters": {"x": 10, "y": 20}, "sequence_number": 1}
        ],
        "target_system": "robot-1",
        "timestamp": 123456789.0,
        "changeset_hash": "abcdef123456"
    }
    file_path = tmp_path / "changeset.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return str(file_path)

def test_changeset_load_and_translate(test_changeset_json, mock_transport):
    executor = MissionContractExecutor("exec-1", mock_transport)
    cs = executor.load_changeset(test_changeset_json)
    assert cs.operation_id == "op-1234"
    
    goal = executor.translate_to_goal(cs)
    assert goal.goal_id == "op-1234"
    assert goal.mission_type == "NAVIGATE"
    assert len(goal.parameters["actions"]) == 1

def test_executor_state_machine(test_changeset_json, mock_transport):
    executor = MissionContractExecutor("exec-1", mock_transport)
    cs = executor.load_changeset(test_changeset_json)
    goal = executor.translate_to_goal(cs)
    
    assert executor.phase == MissionPhase.IDLE
    res = executor.execute(goal)
    assert res["status"] == "success"
    assert executor.phase == MissionPhase.COMPLETED
    assert len(mock_transport.get_published_goals()) == 1

def test_invalid_transition_raises(mock_transport):
    executor = MissionContractExecutor("exec-1", mock_transport)
    executor.phase = MissionPhase.COMPLETED
    with pytest.raises(InvalidTransitionError):
        executor.execute(None)

def test_telemetry_bridge_ingest():
    bridge = TelemetryBridge()
    for i in range(5):
        bridge.ingest("sys-A", {"val": i})
    history = bridge.get_history("sys-A", 10)
    assert len(history) == 5
    assert history[0].checksum != history[1].checksum

def test_orbital_trajectory_interpolation():
    node = OrbitalTrajectoryNode()
    pts = [
        OrbitalTrajectoryPoint(0.0, 0,0,0, 0,0,0, 100),
        OrbitalTrajectoryPoint(10.0, 10,20,30, 1,2,3, 90),
        OrbitalTrajectoryPoint(20.0, 20,40,60, 2,4,6, 80)
    ]
    mid = node.interpolate(pts, 5.0)
    assert mid.x == 5.0
    assert mid.y == 10.0
    assert mid.z == 15.0
    assert mid.mass == 95.0

def test_trajectory_validation_errors():
    node = OrbitalTrajectoryNode()
    pts = [
        OrbitalTrajectoryPoint(10.0, 0,0,0, 0,0,0, 100),
        OrbitalTrajectoryPoint(5.0, 10,20,30, 1,2,3, 90)
    ]
    errors = node.validate_trajectory(pts)
    assert len(errors) == 1
    assert "Non-monotonic" in errors[0]
