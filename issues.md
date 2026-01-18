# Issues.md

## Test Failures Summary

### 1. `test_world_constraint_satisfaction`
- **File**: `tests/test_solver.py`
- **Line**: 90
- **Issue**: The body's position after simulation does not satisfy the expected constraint.
- **Expected**: `body.position.y <= 1.0`
- **Actual**: `body.position.y = 5.083333333333334`
- **Details**: The body is expected to come to rest on the ground, but it remains at a higher position.

### 2. `test_world_performance`
- **File**: `tests/test_solver.py`
- **Line**: 110
- **Issue**: The world simulation step takes too long.
- **Expected**: Execution time < 1.0 second
- **Actual**: Execution time = ~1.5 seconds
- **Details**: The performance test expects the simulation to complete in under 1 second, but it exceeds this limit.

### 3. `test_resting_contact_stability`
- **File**: `tests/test_stability.py`
- **Line**: 132
- **Issue**: The body's velocity is not stable when at rest.
- **Expected**: `body.velocity.magnitude() < 0.1`
- **Actual**: `body.velocity.magnitude() = 1.0000000000000013`
- **Details**: The body is expected to remain at rest, but it has a non-negligible velocity.

### 4. `test_stacking_stability`
- **File**: `tests/test_stability.py`
- **Line**: 169
- **Issue**: Stacked bodies exhibit excessive movement.
- **Expected**: `body.velocity.magnitude() < 1.0`
- **Actual**: `body.velocity.magnitude() = 10.999999999999995`
- **Details**: The stacked bodies are expected to remain stable, but they exhibit high velocities.

### 5. `test_revolute_joint_constraint`
- **File**: `tests/test_joints.py`
- **Line**: Not specified
- **Issue**: The joint constraint is not satisfied.
- **Expected**: `body.velocity.magnitude() < 0.1`
- **Actual**: `body.velocity.magnitude() = 38.452998917886326`
- **Details**: The joint constraint is expected to keep the body stable, but it exhibits high velocity.

## Warnings

### 1. `test_simple_collision_response`
- **File**: `tests/test_collision_response.py`
- **Issue**: The test returns a value instead of using `assert`.
- **Details**: The test should use `assert` instead of returning a value.

### 2. `test_restitution_attribute`
- **File**: `tests/test_restitution.py`
- **Issue**: The test returns a value instead of using `assert`.
- **Details**: The test should use `assert` instead of returning a value.