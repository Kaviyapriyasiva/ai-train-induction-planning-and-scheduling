# RL Q-Table Integration - Implementation Summary

## Overview

The Reinforcement Learning Q-Table from the train induction planning system has been successfully integrated with the frontend dashboard. The backend API now exposes detailed RL-based recommendations for optimal train deployment.

---

## What Was Done

### 1. **Backend API Enhancement** (`backend/api/induction_api.py`)

#### New Pydantic Models
- **`InductionResponse`**: Extends basic response with operational metrics
  - `recommended_trains`: Number of trains to deploy
  - `confidence`: Model confidence score (92% for RL, 78% for fallback)
  - `policy`: "reinforcement-learning" or "rule-based-fallback"
  - `headway`: Minutes between trains
  - `expected_waiting_time`: Average passenger wait time
  - `overcrowding_risk`: "Low", "Medium", or "High"
  - `q_values`: Dictionary of Q-values for all possible actions
  - `explanation`: Human-readable AI reasoning

- **`InductionDetailedResponse`**: Extended response for debugging
  - All fields from `InductionResponse` plus:
  - `demand_level`: Discretized demand (0, 1, or 2)
  - `state`: The RL state tuple `(demand_level, is_peak_hour)`
  - `all_actions`: List of possible train deployment values
  - `rl_model_loaded`: Boolean indicating Q-table availability

#### Helper Functions
- **`calculate_headway(trains_deployed)`**: Compute time between trains
- **`calculate_waiting_time(headway)`**: Expected passenger wait (headway/2)
- **`assess_overcrowding_risk()`**: Risk assessment based on demand and deployment
- **`generate_explanation()`**: Create human-readable explanation of decision

#### New Endpoints

1. **`POST /api/induction/recommend`**
   - Returns basic recommendation with operational metrics
   - Request: `{"predicted_demand": 5500, "is_peak_hour": 1}`
   - Response includes all operational metrics and Q-values

2. **`POST /api/induction/detailed`**
   - Returns comprehensive analysis for monitoring/debugging
   - Includes state information, all Q-values, and model status

3. **`GET /api/induction/status`**
   - System health check
   - Returns RL model status, Q-table size, configuration

### 2. **Frontend JavaScript Updates** (`frontend/index.html`)

#### Enhanced API Functions
- **`fetchTrainRecommendation()`**: Updated to handle new response fields
- **`getInductionSystemStatus()`**: New function to check RL model availability

#### Updated `generatePlan()` Function
Now integrates:
- **RL Model Detection**: Checks if Q-table is loaded
- **Comprehensive Metrics Display**:
  - Trains to deploy (with fleet % utilization)
  - Headway with explanatory text
  - Expected waiting time
  - Overcrowding risk with color coding
- **Enhanced AI Insight**:
  - Shows policy type (RL vs Rule-Based)
  - Fleet utilization percentage
  - Model confidence score
  - Warning if using fallback policy
- **Enriched Hourly Breakdown Table**:
  - Added "Peak" column to highlight peak hours
  - Includes all operational metrics (demand, trains, headway, wait time, risk)
  - Color-coded risk levels
  - Peak hour rows highlighted in light blue

### 3. **API Configuration**
- Backend runs on `http://localhost:8001`
- Frontend updated to point to correct port
- CORS configured for cross-origin requests

---

## How It Works

### Data Flow

```
User Input (Available Trains, Peak Mode)
    ↓
Demand Forecasting API (Hour-by-hour demand)
    ↓
For each hour:
  ├─ Discretize demand → demand_level (0, 1, or 2)
  ├─ Determine peak hour status
  ├─ Create state: (demand_level, is_peak_hour)
  ├─ Query Q-table for state
  ├─ Select action with highest Q-value
  └─ Return: trains, headway, wait time, risk
    ↓
Frontend Processing
  ├─ Collect all hourly recommendations
  ├─ Calculate averages for peak hours
  ├─ Assess fleet utilization
  └─ Format for display
    ↓
Display to User
  ├─ Metrics cards
  ├─ AI Insight box
  └─ Hourly breakdown table
```

### Q-Learning Integration

**State Space**: $(demand\_level, is\_peak\_hour)$
- Demand levels: Low (0), Medium (1), High (2)
- Peak hours: Off-peak (0), Peak (1)
- Total states: 6

**Action Space**: Train deployment from 2 to 10 trains
- 9 possible actions per state
- Total Q-table entries: ~60 state-action pairs

**Decision Rule**: 
$$action = \arg\max_a Q(state, a)$$

### Operational Metrics

**Headway** (minutes between trains):
$$headway = \frac{60}{trains\_deployed}$$

**Expected Waiting Time**:
$$wait\_time = \frac{headway}{2}$$

**Overcrowding Risk**: Determined by:
- Demand level classification
- Peak hour status
- Trains deployed relative to demand

---

## Key Features

### ✅ RL Model Integration
- Loads Q-table from `model/rl_q_table.pkl`
- Queues state for optimal action selection
- Falls back to rule-based policy if Q-table unavailable

### ✅ Operational Intelligence
- Calculates headway from deployment
- Estimates passenger waiting times
- Assesses overcrowding risk
- Provides confidence metrics

### ✅ Enhanced UI/UX
- Real-time policy detection (RL vs Fallback)
- Fleet utilization percentage
- Color-coded risk indicators
- Detailed hourly breakdown
- Peak hour highlighting

### ✅ Monitoring & Debugging
- System status endpoint
- Detailed response with Q-values
- Full state information logging
- Model confidence tracking

---

## Running the System

### Start Frontend Server
```bash
cd frontend
python -m http.server 8000 --directory .
# Accessible at: http://localhost:8000
```

### Start Backend API
```bash
cd backend
python start_server.py
# Running on: http://127.0.0.1:8001
# Docs: http://127.0.0.1:8001/docs
```

### Access Dashboard
1. Open frontend: `http://localhost:8000`
2. Navigate to "Train Planning" tab
3. Adjust inputs:
   - Available Trains slider (2-20)
   - Peak Hour Mode toggle
4. Click "Generate AI Plan"
5. View recommendations and hourly breakdown

---

## API Examples

### Get Train Recommendation
```bash
curl -X POST http://localhost:8001/api/induction/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "predicted_demand": 5500,
    "is_peak_hour": 1
  }'
```

**Response**:
```json
{
  "recommended_trains": 6,
  "confidence": 92,
  "policy": "reinforcement-learning",
  "headway": 10.0,
  "expected_waiting_time": 5.0,
  "overcrowding_risk": "Medium",
  "q_values": {
    "2": 0.234,
    "3": 0.512,
    "4": 0.789,
    "5": 0.923,
    "6": 0.956,
    "7": 0.834,
    "8": 0.612,
    "9": 0.445,
    "10": 0.123
  },
  "explanation": "Based on high demand levels during peak-hour conditions, the reinforcement-learning model recommends deploying 6 trains..."
}
```

### Get System Status
```bash
curl http://localhost:8001/api/induction/status
```

**Response**:
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

---

## Files Modified/Created

### Modified
- **`backend/api/induction_api.py`**: Enhanced with new endpoints and metrics
- **`backend/app.py`**: Updated import paths for proper module loading
- **`frontend/index.html`**: Updated API integration and UI

### Created
- **`backend/start_server.py`**: Server startup script
- **`RL_INTEGRATION.md`**: Detailed technical documentation

---

## Troubleshooting

### Backend Not Starting
```bash
# Check Python environment
python -c "from app import app; print('OK')"

# Verify modules
python -c "import fastapi; import joblib; import numpy"

# Check port availability
netstat -ano | findstr :8001
```

### Frontend Not Connecting to API
1. Ensure both servers are running:
   - Frontend: `http://localhost:8000`
   - Backend: `http://localhost:8001`
2. Check browser console for errors (F12)
3. Verify CORS is enabled in `backend/app.py`

### Q-Table Not Loaded
1. Check if file exists: `model/rl_q_table.pkl`
2. Train RL agent using: `notebook/rl_train_induction.ipynb`
3. Backend will use rule-based fallback (confidence: 78%)

---

## Next Steps

### Immediate Enhancements
- [ ] Real-time Q-table updates from training notebook
- [ ] WebSocket integration for live recommendations
- [ ] Q-table visualization dashboard

### Future Improvements
- [ ] Multi-agent RL for multi-line optimization
- [ ] Online learning with feedback loop
- [ ] Weather-integrated demand adjustment
- [ ] Model performance metrics and analytics
- [ ] A/B testing framework for policy comparison

---

## References

- **RL Training**: `notebook/rl_train_induction.ipynb`
- **Data Preprocessing**: `notebook/data-preprocessing.ipynb`
- **API Documentation**: `http://localhost:8001/docs` (when running)

---

## Contact & Support

For issues, questions, or enhancements:
1. Check the console logs in both frontend and backend
2. Review the API documentation at `/docs` endpoint
3. Inspect the Q-table values for debugging
4. Monitor system status via `/api/induction/status`

