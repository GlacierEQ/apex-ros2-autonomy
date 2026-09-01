from abc import ABC, abstractmethod
from typing import List, Optional, Any
from .mission_contract import MissionGoal

class MissionTransport(ABC):
    @abstractmethod
    def publish_goal(self, goal: MissionGoal) -> None:
        pass

    @abstractmethod
    def subscribe_feedback(self, callback: Any) -> None:
        pass

    @abstractmethod
    def publish_telemetry(self, telemetry: dict) -> None:
        pass

class MockMissionTransport(MissionTransport):
    def __init__(self):
        self.published_goals: List[MissionGoal] = []
        self.telemetry_published: List[dict] = []

    def publish_goal(self, goal: MissionGoal) -> None:
        self.published_goals.append(goal)

    def subscribe_feedback(self, callback: Any) -> None:
        pass

    def publish_telemetry(self, telemetry: dict) -> None:
        self.telemetry_published.append(telemetry)

    def get_published_goals(self) -> List[MissionGoal]:
        return self.published_goals

class Ros2MissionTransport(MissionTransport):
    def __init__(self):
        try:
            import rclpy
            from rclpy.node import Node
            self.rclpy = rclpy
        except ImportError:
            raise ImportError("rclpy not found. ROS2 environment is required for Ros2MissionTransport.")

    def publish_goal(self, goal: MissionGoal) -> None:
        pass

    def subscribe_feedback(self, callback: Any) -> None:
        pass

    def publish_telemetry(self, telemetry: dict) -> None:
        pass
