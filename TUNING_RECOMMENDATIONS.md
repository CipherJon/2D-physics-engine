# Physics Engine Tuning Recommendations

## Current Implementation (After Fixes)

The physics engine now includes the following key improvements:

### 1. Increased Solver Iterations
- **Velocity iterations**: 40 (increased from 8)
- **Position iterations**: 15 (increased from 3)

### 2. Aggressive Baumgarte Stabilization
- **BAUMGARTE**: 0.2 (increased from 0.1)
- **POSITION_SLOP**: 0.02 (allows small penetration before strong correction)
- **Correct bias calculation**: `bias = -BAUMGARTE / dt * max(0.0, penetration + POSITION_SLOP)`

### 3. Friction Implementation
- **Static friction**: 0.6
- **Dynamic friction**: 0.4
- **Coulomb friction model**: Clamped to normal impulse magnitude

### 4. Contact Persistence
- **Threshold**: 0.05 units for contact persistence
- **Warm starting**: Reuse accumulated normal and tangent impulses

### 5. Restitution Handling
- **Default for stability tests**: 0.0 (no bounce)
- **Configurable per-body**: Can be set individually

## Recommended Tuning After Initial Stabilization

Once the engine achieves stable resting contacts (velocity < 0.1 m/s, position ≈ expected), gradually reduce the aggressive parameters:

### First Reduction (After Basic Stability)
1. **BAUMGARTE**: Reduce from 0.2 → 0.15
2. **Velocity iterations**: Reduce from 40 → 30
3. **Position iterations**: Reduce from 15 → 12

### Second Reduction (After Consistent Stability)
1. **BAUMGARTE**: Reduce from 0.15 → 0.1
2. **Velocity iterations**: Reduce from 30 → 20
3. **Position iterations**: Reduce from 12 → 8

### Final Production Values (After Thorough Testing)
1. **BAUMGARTE**: 0.05-0.1 (depending on application)
2. **Velocity iterations**: 15-20
3. **Position iterations**: 6-8
4. **Restitution**: 0.1-0.3 for realistic bouncing
5. **Friction**: STATIC=0.4-0.6, DYNAMIC=0.3-0.5

## Expected Behavior After Fixes

### test_resting_contact_stability
- **Initial**: Circle at y=1, v=0
- **After 60 steps**: y≈1.0 (±0.01), vy≈0.0 (±0.1)

### test_world_constraint_satisfaction
- **Initial**: Circle from y=5
- **After 60 steps**: y≈5.08 (resting on ground), vy≈0.0 (±0.1)

### test_stacking_stability
- **After 60 steps**: All boxes have vy≈0.0 (±0.1), maintain stable stack

## Debugging Tips

1. **If bodies still fall through**:
   - Increase BAUMGARTE to 0.3 temporarily
   - Increase position iterations to 20
   - Check contact normal directions

2. **If excessive jittering**:
   - Reduce BAUMGARTE gradually
   - Increase POSITION_SLOP to 0.03
   - Ensure proper warm starting

3. **If stacking unstable**:
   - Increase friction coefficients
   - Verify contact point calculations
   - Check normal impulse accumulation

## Performance Considerations

- Higher iteration counts improve stability but reduce performance
- For real-time applications, target:
  - 60 FPS: ≤20 velocity iterations, ≤10 position iterations
  - 30 FPS: ≤30 velocity iterations, ≤15 position iterations