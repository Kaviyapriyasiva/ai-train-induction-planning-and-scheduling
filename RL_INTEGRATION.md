# Reinforcement Learning Q-Table Integration

## Overview

This document describes the integration between the **Reinforcement Learning Q-Table** (Backend) and the **Frontend Dashboard** for AI-assisted Train Induction Planning.

---

## Architecture

### Backend Components

#### **File**: `backend/api/induction_api.py`

**Key Features:**
- **Q-Table Loading**: Loads pre-trained RL model from `model/rl_q_table.pkl`
- **State Space**: Discretized into `(demand_level, is_peak_hour)` tuples
  - `demand_level`: 0 (Low <3000), 1 (Medium 3000-6000), 2 (High >6000)
  - `is_peak_hour`: 0 (Off-peak) or 1 (Peak)
- **Action Space**: Train deployment from 2 to 10 trains

**API Endpoints:**

1. **POST `/api/induction/recommend`**
   - Basic recommendation endpoint
   - Returns: Trains to deploy, confidence, policy, operational metrics
   ```json
   {
     "recommended_trains": 6,
     "confidence": 92,
     "policy": "reinforcement-learning",
     "headway": 10.0,
     "expected_waiting_time": 5.0,
     "overcrowding_risk": "Medium",
     "q_values": { "2": 0.5, "3": 0.7, ... },
     "explanation": "Based on high demand levels..."
   }
   ```

2. **POST `/api/induction/detailed`**
   - Extended endpoint with full Q-table analysis
   - Includes: All Q-values, demand_level, state tuple, RL model status
   - Useful for debugging and monitoring

3. **GET `/api/induction/status`**
   - System health check
   - Returns: RL model status, Q-table size, configuration

### Frontend Components

#### **File**: `frontend/index.html`

**Integration Points:**

1. **API Functions**
   - `fetchTrainRecommendation(predictedDemand, isPeak)`: Calls `/api/induction/recommend`
   - `getInductionSystemStatus()`: Checks RL model availability

2. **Train Planning Tab (Tab 3)**
   - **Inputs**: 
     - Available Trains slider (2-20)
     - Peak Hour Mode toggle
   - **Output Display**:
     - Trains to deploy
     - Headway calculation
     - Expected waiting time
     - Overcrowding risk assessment
     - AI insight with model explanation
   - **Hourly Breakdown Table**
     - Shows demand, deployment, and risk for each hour
     - Highlights peak hours
     - Aggregates recommendations

---

## Q-Learning Integration

### How the RL Model Works

1. **State**: Demand level + Peak hour status
2. **Action**: Number of trains to deploy
3. **Q-Values**: Learned value for each (state, action) pair
4. **Decision**: Argmax of Q-values for given state

### Fallback Strategy

If Q-table is not loaded:
- Uses **rule-based fallback policy** based on:
  - Demand level
  - Peak hour status
  - Fleet constraints

### Operational Calculations

```python
# Headway (minutes between trains)
headway = 60 / trains_deployed

# Expected waiting time
waiting_time = headway / 2

# Overcrowding risk assessment
risk = assess_overcrowding_risk(demand_level, is_peak, trains_deployed)
```

---

## Data Flow

```
Frontend User Input
    ↓
[Available Trains, Peak Mode]
    ↓
Demand Forecasting API → Predicted Demand
    ↓
RL Induction API
├─ State: (demand_level, is_peak)
├─ Action: Q-table lookup
└─ Result: Recommended trains
    ↓
Operational Metrics Calculation
├─ Headway
├─ Waiting Time
└─ Overcrowding Risk
    ↓
Frontend Display
└─ Metrics cards + Hourly breakdown table
```

---

## Configuration

### Constants
- `MIN_TRAINS`: 2
- `MAX_TRAINS`: 10
- Demand thresholds: [3000, 6000]
- Peak hours: 8-10 AM, 5-8 PM

### Q-Table File
- **Location**: `model/rl_q_table.pkl`
- **Format**: Dictionary with `(state, action)` tuples as keys
- **Fallback**: If missing, system uses rule-based policy

---

## Usage Example

### Get Train Recommendation
```bash
curl -X POST http://localhost:8000/api/induction/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "predicted_demand": 5500,
    "is_peak_hour": 1
  }'
```

**Response:**
```json
{
  "recommended_trains": 6,
  "confidence": 92,
  "policy": "reinforcement-learning",
  "headway": 10.0,
  "expected_waiting_time": 5.0,
  "overcrowding_risk": "Medium",
  "explanation": "Based on high demand levels during peak-hour conditions, the reinforcement-learning model recommends deploying 6 trains..."
}
```

---

## Monitoring & Debugging

### System Status Check
```bash
curl http://localhost:8000/api/induction/status
```

**Response:**
```json
{
  "status": "operational",
  "rl_model_loaded": true,
  "min_trains": 2,
  "max_trains": 10,
  "q_table_size": 60,
  "demand_levels": 3,
  "policies": ["reinforcement-learning", "rule-based-fallback"]
}
```

### Frontend Indicators
- **Model Status**: Displayed in AI Insight section
- **Confidence Score**: Shows RL vs. Fallback policy confidence
- **Policy Label**: Indicates which decision-making approach was used

---

## Troubleshooting

### Q-Table Not Loaded
- **Symptom**: Uses rule-based fallback (confidence: 78%)
- **Solution**: 
  1. Ensure `model/rl_q_table.pkl` exists
  2. Train RL agent using `notebook/rl_train_induction.ipynb`
  3. Restart backend service

### API Connection Error
- **Symptom**: Default values returned
- **Solution**:
  1. Check backend is running: `python backend/app.py`
  2. Verify API_BASE in frontend (should be `http://localhost:8000/api`)
  3. Check CORS configuration in `backend/app.py`

### Unexpected Recommendations
- **Check**:
  1. Current demand level classification
  2. Peak hour detection
  3. Q-table values via `/api/induction/detailed`

---

## Future Enhancements

- [ ] Real-time demand updates integration
- [ ] Multi-agent RL for multi-line optimization
- [ ] Weather-based demand adjustment
- [ ] Reinforcement learning with Q-table visualization
- [ ] Model performance metrics dashboard

---

## References

- **RL Model Training**: `notebook/rl_train_induction.ipynb`
- **Demand Forecasting**: `notebook/demand-forecasting.ipynb`
- **Data Preprocessing**: `notebook/data-preprocessing.ipynb`

