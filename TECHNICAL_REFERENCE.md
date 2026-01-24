# Technical Reference Card - RL Q-Table Integration

## Quick Reference

### System Startup
```bash
# Terminal 1: Backend
cd backend && python start_server.py
# http://127.0.0.1:8001

# Terminal 2: Frontend  
cd frontend && python -m http.server 8000 --directory .
# http://localhost:8000
```

---

## API Endpoints

### Induction Planning
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/induction/recommend` | Get train deployment |
| `POST` | `/api/induction/detailed` | Get full RL analysis |
| `GET` | `/api/induction/status` | Check system health |

### Other APIs
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/demand/predict` | Forecast demand |
| `GET` | `/api/stations` | Station information |

### Auto-Generated Docs
```
http://127.0.0.1:8001/docs          # Swagger UI
http://127.0.0.1:8001/redoc          # ReDoc
```

---

## Request/Response Examples

### Basic Recommendation
**Request:**
```json
{
  "predicted_demand": 5500,
  "is_peak_hour": 1
}
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
  "q_values": {
    "2": 0.234, "3": 0.512, "4": 0.789,
    "5": 0.923, "6": 0.956, "7": 0.834,
    "8": 0.612, "9": 0.445, "10": 0.123
  },
  "explanation": "Based on high demand levels during peak-hour..."
}
```

---

## Configuration Reference

### Demand Levels
```python
demand_level = {
    0: "Low",      # < 3,000 passengers/hour
    1: "Medium",   # 3,000 - 6,000 passengers/hour
    2: "High"      # > 6,000 passengers/hour
}
```

### Peak Hour Detection
```python
is_peak_hour = {
    0: "Off-peak",
    1: "Peak"
}

# Peak hours: 8-10 AM, 5-8 PM
```

### Formulas
```
Headway (min) = 60 / trains_deployed
Wait Time (min) = headway / 2
Fleet Utilization (%) = (trains / available_trains) * 100
```

---

## State-Action Space

### States (6 total)
```
(0, 0): Low demand, off-peak
(0, 1): Low demand, peak
(1, 0): Medium demand, off-peak
(1, 1): Medium demand, peak
(2, 0): High demand, off-peak
(2, 1): High demand, peak
```

### Actions (9 total)
```
2, 3, 4, 5, 6, 7, 8, 9, 10 trains
```

### Q-Table
```
Dictionary with (state, action) as keys
Q[(state, action)] = learned_value
```

---

## File Locations

### Core Files
| File | Purpose |
|------|---------|
| `backend/app.py` | FastAPI application |
| `backend/api/induction_api.py` | RL integration ⭐ |
| `frontend/index.html` | Dashboard ⭐ |
| `model/rl_q_table.pkl` | Q-table file |

### Scripts
| File | Purpose |
|------|---------|
| `backend/start_server.py` | Start backend |
| `backend/run.py` | Alternative runner |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | Main readme |
| `QUICK_START.md` | 5-min guide ⭐ |
| `RL_INTEGRATION.md` | Technical docs |
| `IMPLEMENTATION_SUMMARY.md` | Changes |
| `CHANGES_SUMMARY.txt` | Changelog |

---

## JavaScript Functions (Frontend)

### API Calls
```javascript
// Get recommendation
fetchTrainRecommendation(predictedDemand, isPeak)
// Returns: {recommended_trains, headway, expected_waiting_time, ...}

// Get system status
getInductionSystemStatus()
// Returns: {status, rl_model_loaded, ...}

// Demand forecast
fetchDemandForecast(hour, isWeekend, isPeak, trainsPerHour, directionId)
// Returns: {estimated_demand, weather_factor}
```

### UI Functions
```javascript
// Generate plan
generatePlan()
// Generates hourly recommendations and displays

// Switch tabs
switchTab(index)
// Switches between dashboard tabs

// Update displays
updateTrainsDisplay(val)
updateHourDisplay(val)
updateDemandDisplay(val)
```

---

## Python Backend Functions

### Q-Learning
```python
get_demand_level(demand: int) -> int
# Discretizes demand into 0, 1, or 2

calculate_headway(trains_deployed: int) -> float
# Returns 60 / trains_deployed

calculate_waiting_time(headway: float) -> float
# Returns headway / 2

assess_overcrowding_risk(demand_level, is_peak, trains) -> str
# Returns "Low", "Medium", or "High"

generate_explanation(...) -> str
# Creates human-readable explanation
```

---

## Common Curl Commands

### Test Health
```bash
curl http://127.0.0.1:8001/
```

### Test Recommendation
```bash
curl -X POST http://127.0.0.1:8001/api/induction/recommend \
  -H "Content-Type: application/json" \
  -d '{"predicted_demand": 5500, "is_peak_hour": 1}'
```

### Get Detailed Analysis
```bash
curl -X POST http://127.0.0.1:8001/api/induction/detailed \
  -H "Content-Type: application/json" \
  -d '{"predicted_demand": 5500, "is_peak_hour": 1}'
```

### Check Status
```bash
curl http://127.0.0.1:8001/api/induction/status | python -m json.tool
```

---

## Error Codes & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| **502 Bad Gateway** | Backend not running | Start: `python start_server.py` |
| **Connection refused** | Wrong port | Check port 8001 is used |
| **ModuleNotFoundError** | Missing package | Run: `pip install -r requirements.txt` |
| **File not found** | Q-table missing | Train model or check path |
| **CORS error** | Browser console | Check CORS in `app.py` |

---

## Environment Variables

Create `.env` file in `backend/`:
```
# Optional configuration
OPENAI_API_KEY=your_key_here
DATABASE_URL=your_db_url
```

---

## Key Metrics for Monitoring

### Backend Health
```bash
# Is Q-table loaded?
curl http://127.0.0.1:8001/api/induction/status
# Look for: "rl_model_loaded": true

# Q-table size
# Look for: "q_table_size": 60

# What policies available?
# Look for: "policies": ["reinforcement-learning", "rule-based-fallback"]
```

### API Response Quality
```
Confidence: 92% = RL model, 78% = Fallback
Policy: reinforcement-learning = Good, rule-based-fallback = Backup
Q-Values: Higher max = Better learned strategy
```

---

## Performance Optimization

### Frontend
```javascript
// Cache demand API responses
const demandCache = new Map();

// Batch API calls when possible
Promise.all([...apiCalls])

// Lazy load hourly breakdown
<details> tag with collapsible content
```

### Backend
```python
# Q-table loaded once at startup
# No repeated loads in request

# Fast Q-value lookup (dict access)
q_values = {action: q_table.get(...) for action in actions}

# Vectorized operations with NumPy
best_action = actions[np.argmax(q_values_list)]
```

---

## Integration Checklist

- [x] Q-Table loading in backend
- [x] API endpoints defined
- [x] Frontend API integration
- [x] UI metrics display
- [x] Hourly breakdown table
- [x] Peak hour highlighting
- [x] Risk color coding
- [x] Policy indicator
- [x] Confidence display
- [x] System status endpoint
- [x] Error handling
- [x] Documentation

---

## Debugging Commands

### Check Python Setup
```bash
python --version
python -c "import fastapi; print('FastAPI OK')"
python -c "import joblib; print('Joblib OK')"
python -c "import numpy; print('NumPy OK')"
```

### Check File Exists
```bash
ls model/rl_q_table.pkl
ls backend/api/induction_api.py
ls frontend/index.html
```

### Check Ports
```bash
# Windows
netstat -ano | findstr 8000
netstat -ano | findstr 8001

# macOS/Linux
lsof -i :8000
lsof -i :8001
```

### Test Backend Import
```bash
cd backend
python -c "from app import app; print('App loaded')"
python -c "from api.induction_api import router; print('Router OK')"
```

---

## Key Data Structures

### State Tuple
```python
state = (demand_level: int, is_peak_hour: int)
# Example: (2, 1) = High demand, peak hour
```

### Q-Values Dictionary
```python
q_values = {
    2: 0.234,  # Q(state, 2 trains)
    3: 0.512,  # Q(state, 3 trains)
    ...
    10: 0.123  # Q(state, 10 trains)
}
```

### Recommendation Response
```python
{
    'recommended_trains': 6,           # int
    'confidence': 92,                  # int (78-92)
    'policy': 'reinforcement-learning', # str
    'headway': 10.0,                   # float
    'expected_waiting_time': 5.0,      # float
    'overcrowding_risk': 'Medium',     # str
    'q_values': {...},                 # dict
    'explanation': '...'               # str
}
```

---

## Training New Q-Table

If you need to train a new Q-table:
1. Open: `notebook/rl_train_induction.ipynb`
2. Run all cells
3. New Q-table will be saved to: `model/rl_q_table.pkl`
4. Restart backend to load new Q-table

---

## Version Information

- **FastAPI**: 0.68+
- **Python**: 3.8+
- **Frontend**: Vanilla HTML/CSS/JS
- **Backend**: FastAPI + Uvicorn
- **Model Format**: Joblib pickle

---

## Quick Links

- **API Docs**: `http://127.0.0.1:8001/docs`
- **Frontend**: `http://localhost:8000`
- **Q-Table**: `model/rl_q_table.pkl`
- **Training**: `notebook/rl_train_induction.ipynb`

---

**Last Updated**: 2026-01-24
**Status**: ✅ Production Ready

