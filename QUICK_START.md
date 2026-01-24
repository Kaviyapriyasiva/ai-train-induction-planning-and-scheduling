# Quick Start Guide - RL Q-Table Integration

## 🚀 Getting Started (5 Minutes)

### Prerequisites
- Python 3.8+
- pip packages: `fastapi`, `uvicorn`, `joblib`, `numpy`

### Step 1: Start Backend API
```bash
cd backend
python start_server.py
```
✅ Backend running on: `http://localhost:8001`

### Step 2: Start Frontend Server
```bash
cd frontend
python -m http.server 8000 --directory .
```
✅ Frontend running on: `http://localhost:8000`

### Step 3: Open Dashboard
Open browser: `http://localhost:8000`

### Step 4: Test Train Planning
1. Go to "🚆 Train Planning" tab
2. Adjust sliders:
   - Available Trains: 5-15
   - Toggle Peak Hour Mode
3. Click "🤖 Generate AI Plan"
4. View AI recommendations!

---

## 📊 Understanding the Output

### Metrics Cards

| Metric | What It Means | Example |
|--------|---------------|---------|
| **Trains to Deploy** | How many trains to run | 6 trains (60% of 10 available) |
| **Headway (min)** | Time between trains | 10 min = 60÷6 |
| **Expected Wait** | Average passenger wait | 5 min = 10÷2 |
| **Overcrowding Risk** | Congestion level | Low 🟢 / Medium 🟡 / High 🔴 |

### AI Insight Box
- **Policy Used**: "Reinforcement Learning 🤖" or "Rule-Based 📋"
- **Confidence**: Model certainty (92% = RL, 78% = Fallback)
- **Fleet Utilization**: % of available trains used
- **Model Status**: Warning if Q-table not loaded

---

## 🔧 API Endpoints

### Quick Test Commands

**Get Recommendation:**
```bash
curl -X POST http://localhost:8001/api/induction/recommend \
  -H "Content-Type: application/json" \
  -d '{"predicted_demand": 5000, "is_peak_hour": 1}'
```

**Check System Status:**
```bash
curl http://localhost:8001/api/induction/status
```

**API Documentation:**
```
http://localhost:8001/docs
```

---

## ⚙️ Configuration

### Demand Levels
- **Low**: < 3,000 passengers/hour
- **Medium**: 3,000 - 6,000 passengers/hour
- **High**: > 6,000 passengers/hour

### Train Deployment Range
- **Min**: 2 trains
- **Max**: 10 trains
- **Q-Table States**: 6 (3 demand levels × 2 peak/off-peak)

### Peak Hours
- **Morning Peak**: 8:00 AM - 10:00 AM
- **Evening Peak**: 5:00 PM - 8:00 PM
- **Off-Peak**: All other hours

---

## 🎯 How RL Works

```
┌─────────────────────────────────────┐
│  User Inputs (Demand, Peak Mode)    │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  Discretize State                   │
│  (demand_level, is_peak_hour)       │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  Query Q-Table                      │
│  Get Q-values for all actions       │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  Select Best Action                 │
│  argmax(Q-values)                   │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  Return Recommendation              │
│  (trains, headway, wait, risk)      │
└─────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Can't connect to API** | Check backend is running on port 8001 |
| **Getting rule-based fallback** | Q-table file not found. Train model or check `model/rl_q_table.pkl` |
| **Slow response** | Multiple forecasting API calls. Check demand API connectivity |
| **Port already in use** | Change port in `start_server.py` or stop other services |

### Debug Steps
```bash
# 1. Check if backend is running
curl http://localhost:8001/

# 2. Check RL model status
curl http://localhost:8001/api/induction/status

# 3. Test with simple request
curl -X POST http://localhost:8001/api/induction/recommend \
  -H "Content-Type: application/json" \
  -d '{"predicted_demand": 3000, "is_peak_hour": 0}'

# 4. Check browser console (F12) for frontend errors
```

---

## 📈 Understanding Q-Values

Q-Values represent learned value of each action in a state.

**Example Response:**
```json
"q_values": {
  "2": 0.234,    // Low value - rarely chosen
  "3": 0.512,    // Medium
  "4": 0.789,    // Good
  "5": 0.923,    // Very good
  "6": 0.956,    // BEST ← Selected
  "7": 0.834,    // Good but overdeploying
  "8": 0.612,    // Medium
  "9": 0.445,    // Low
  "10": 0.123    // Very low - wastes resources
}
```

**Why 6 trains?** Highest Q-value = Best learned strategy!

---

## 📊 Hourly Breakdown Table

Shows recommendation for each hour:

| Hour | Peak | Demand | Trains | Headway | Wait | Risk |
|------|:----:|--------|--------|---------|------|------|
| 6:00 | — | 1,200 | 2 | 30.0 | 15.0 | Low |
| 8:00 | 📍 | 6,500 | 8 | 7.5 | 3.8 | High |
| 10:00| 📍 | 5,200 | 6 | 10.0 | 5.0 | Medium |
| 17:00| 📍 | 7,100 | 8 | 7.5 | 3.8 | High |
| 22:00| — | 2,100 | 2 | 30.0 | 15.0 | Low |

- **📍** = Peak hour
- **Trains** = AI recommendation
- **Headway** = Time between trains
- **Wait** = Expected passenger wait time
- **Risk** = Overcrowding risk level

---

## 💡 Tips & Best Practices

### Interpreting Recommendations
✅ **Balanced**: Trains 5-7, Medium-High demand = Good training data
⚠️ **Edge Case**: Trains 2 (min), High demand = Risk assessment working
🔄 **Off-Peak**: Trains 2-3, Low demand = Cost optimization

### Testing the System
1. **Test Low Demand**: Set available trains = 5, demand < 3000
   - Should recommend minimal trains
   - Headway will be long
   - Risk should be "Low"

2. **Test Peak Hour**: Set available trains = 10, demand > 6000
   - Should recommend more trains
   - Headway will be short
   - Risk management active

3. **Test Fleet Constraints**: Set available trains = 3
   - Recommendations capped at 3
   - Utilization shows 100%

---

## 📚 More Information

- **Full Technical Docs**: See `RL_INTEGRATION.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Training Notebook**: See `notebook/rl_train_induction.ipynb`
- **API Docs**: Visit `http://localhost:8001/docs` (when running)

---

## ✨ What's New

✅ **Backend Enhancements**
- 3 new API endpoints
- Full operational metrics
- Q-value transparency
- System status monitoring

✅ **Frontend Updates**
- Real-time RL model detection
- Enhanced metrics display
- Fleet utilization tracking
- Detailed hourly breakdown

✅ **Integration Features**
- Seamless RL model integration
- Fallback policy support
- Comprehensive error handling
- Model confidence reporting

---

**🎉 Enjoy your AI-powered train scheduling system!**

