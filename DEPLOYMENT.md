# BenQual Deployment Guide

## Latest Changes (Missing Value Detection Fix)

### Backend (API)
1. **Fixed Data Completeness Calculation** (`api/validators.py`):
   - Now correctly chains validation: missing detection → numeric validation
   - Completeness calculated as: `valid_records / total_records * 100`
   - No longer always shows 100%

2. **Return Success Instead of Errors** (`api/app.py`):
   - All responses return 200 status (no more 400 errors)
   - Added `status` field: `success`, `insufficient_data`, `no_data`
   - Full quality report included even when data is insufficient
   - Supports both GET and POST methods for backward compatibility

3. **CORS Support** - Allows requests from:
   - `http://localhost:5173` (local development)
   - `https://benqual.netlify.app` (production)

### Frontend
1. **Enhanced DataResult Component** (`components/DataResult.vue`):
   - Displays status messages for insufficient/no data
   - Shows missing and invalid value details
   - Conditional rendering based on response status
   - Only shows chart when analysis is complete

2. **Enhanced Console Logging** (`views/AnalyzeView.vue`):
   - Detailed request/response logging
   - Shows all quality metrics in console
   - Easier debugging

3. **POST with JSON** - Sends data as clean JSON body

## Deployment Steps

### 1. Deploy Backend to Render

You need to redeploy your backend for the changes to take effect:

1. Push the updated code to your GitHub repository:
   ```bash
   git add .
   git commit -m "Fix CORS and switch to POST JSON requests"
   git push origin main
   ```

2. In Render dashboard:
   - Go to your `benqual` service
   - It should auto-deploy if you have auto-deploy enabled
   - OR click "Manual Deploy" > "Deploy latest commit"

3. Wait for deployment to complete (usually 2-3 minutes)

### 2. Deploy Frontend to Netlify

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy to Netlify:
   - Drag and drop the `frontend/dist` folder to Netlify
   - OR use Netlify CLI:
     ```bash
     netlify deploy --prod --dir=dist
     ```

## Testing

Once deployed, test with simple data:
1. Go to your deployed site
2. Enter: `1, 2, 3, 4, 5`
3. Click "Test"
4. Should see results without CORS errors

## API Request Format

**Endpoint:** `POST https://benqual.onrender.com/api/benford_test/`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "data": [1, 2, 3, 4, 5]
}
```

**Response:**
```json
{
  "actual_percentages": {...},
  "expected_percentages": {...},
  "p-value": 0.123,
  "chi2_stat": 1.234,
  "ks_statistic": 0.456,
  "ks_p_value": 0.789,
  "mad": 0.012,
  "records_analyzed": 5
}
```

## Troubleshooting

### Still getting CORS errors?
- Ensure backend is redeployed
- Check browser console for the exact error
- Verify the request is going to the correct URL

### Getting 400 Bad Request?
- Check that data is an array of numbers
- Verify Content-Type header is set to application/json
- Check browser network tab to see the actual request being sent
