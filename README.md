# APEX ROS2 Autonomy Bridge

Bridges APEX ChangeSet state machine to ROS2 autonomous actuation. Integrates with the SpaceX aerospace estate:
- `spacex-autonomy`
- `spacex-orbital-mechanics`
- `spacex-mission-control`
- `spacex-launch-sequencer`

## Architecture
APEX ChangeSet -> `MissionContractExecutor` -> `MissionTransport` (ROS2/Mock) -> Action

## Integration
Provides Gazebo simulated worlds (`apex_test_world.sdf`) and orbital trajectory interpolation (consuming JSON emitted by `spacex-orbital-mechanics`).

## Development
```bash
make test
make docker-test
```
