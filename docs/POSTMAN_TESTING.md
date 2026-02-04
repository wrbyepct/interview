# MNIST API - Postman Testing Guide

This guide provides step-by-step instructions for manually testing the MNIST Digit Recognition API using Postman.

## Prerequisites

Before you begin, ensure you have:

1. **Postman installed**
   - Download from: [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
   - Desktop app recommended (supports file uploads without size limits)

2. **API server running**
   - Start the FastAPI server with:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port 8000
     ```
   - Verify server is running by visiting: [http://localhost:8000/docs](http://localhost:8000/docs)

3. **Test images available**
   - The `saved_images/` folder contains 10 PNG test images
   - Each image filename includes the correct label (e.g., `img_0_label_6.png` has digit 6)

## How to Import

Follow these steps to import the Postman collection and environment:

### Step 1: Open Postman
- Launch the Postman desktop application

### Step 2: Import the Collection
1. Click the **Import** button (top left corner)
2. Click **Select Files** or drag and drop
3. Navigate to the project directory and select: `postman/MNIST_API_Collection.json`
4. Click **Import**

### Step 3: Import the Environment
1. Click the **Import** button again
2. Select: `postman/MNIST_API_Environment.json`
3. Click **Import**

### Step 4: Activate the Environment
1. Look for the environment dropdown in the top-right corner
2. Select **"MNIST API - Local"**
3. The `{{base_url}}` variable will now point to `http://localhost:8000`

## Running Tests

### Running Individual Requests

1. In the Collections sidebar, expand **"MNIST API Testing"**
2. Navigate to a specific request (e.g., **Health Check > GET /health**)
3. Click **Send**
4. View results in:
   - **Body** tab: Response JSON
   - **Test Results** tab: Pass/fail status of automated test scripts

### Running All Tests with Collection Runner

1. Click the **Run** button on the "MNIST API Testing" collection
2. The Collection Runner window will open
3. Ensure all requests are selected
4. Click **Run MNIST API Testing**
5. View aggregated test results with pass/fail counts

### Viewing Test Results

After sending a request, check the **Test Results** tab:
- ✅ Green checkmarks indicate passed tests
- ❌ Red X marks indicate failed tests
- Each test validates specific response properties (status code, schema, value ranges)

## Test Cases Overview

| Request | Method | Expected Status | Expected Response |
|---------|--------|-----------------|-------------------|
| GET /health | GET | 200 OK | `{"status": "ok"}` |
| POST /predict - PNG | POST | 200 OK | `{"digit": 0-9, "confidence": 0.0-1.0}` |
| POST /predict - JPG | POST | 200 OK | `{"digit": 0-9, "confidence": 0.0-1.0}` |
| POST /predict - Invalid file | POST | 400 Bad Request | Error message with "Invalid file type" |
| POST /predict - No file | POST | 422 Unprocessable Entity | Validation error for missing field |

### Test Scripts Validation

Each request includes automated test scripts that validate:

**Health Check:**
- Status code is 200
- Response contains `status: "ok"`
- Response time < 500ms

**Prediction Requests:**
- Status code is 200
- Response time < 2000ms
- Response has `digit` and `confidence` properties
- `digit` is an integer between 0-9
- `confidence` is a float between 0.0-1.0

**Error Cases:**
- Correct error status codes (400 or 422)
- Error detail message is present

## Test Images

The `saved_images/` folder contains 10 test images:

| Filename | Expected Digit |
|----------|----------------|
| img_0_label_6.png | 6 |
| img_1_label_5.png | 5 |
| img_2_label_3.png | 3 |
| img_3_label_4.png | 4 |
| img_4_label_7.png | 7 |
| img_5_label_8.png | 8 |
| img_6_label_9.png | 9 |
| img_7_label_2.png | 2 |
| img_8_label_1.png | 1 |
| img_9_label_0.png | 0 |

### How to Use Images in Postman

1. Open a **POST /predict** request
2. Go to the **Body** tab
3. Ensure **form-data** is selected
4. Find the row with key **"file"**
5. Change the type dropdown from "Text" to **"File"**
6. Click **Select Files**
7. Navigate to `saved_images/` and select an image
8. Click **Send**

**Note:** The key name MUST be "file" to match the API's parameter name.

## Expected Results

When all tests are successful, you should see:

### Health Check
- ✅ Status code is 200
- ✅ Response has correct schema
- ✅ Response time is less than 500ms

### Predictions
- ✅ Status code is 200
- ✅ Response time is less than 2000ms
- ✅ Response has correct structure
- ✅ Digit is in valid range (0-9)
- ✅ Confidence is in valid range (0.0-1.0)
- ✅ Predicted digit matches the label in the filename (e.g., img_0_label_6.png → digit: 6)

### Error Cases
- ✅ Invalid file type returns 400
- ✅ Missing file returns 422
- ✅ Error messages are descriptive

## Troubleshooting

### "Could not get any response" or "Connection refused"
**Problem:** API server is not running or not accessible

**Solution:**
1. Check if the server is running: `ps aux | grep uvicorn`
2. Start the server: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Verify server responds: Open [http://localhost:8000/health](http://localhost:8000/health) in your browser

### "422 Unprocessable Entity" when file is provided
**Problem:** Form field name doesn't match API parameter

**Solution:**
1. In the Body tab, check the form-data key name
2. It MUST be exactly **"file"** (lowercase)
3. Ensure the field type is set to **"File"** (not "Text")

### "400 Bad Request - Invalid file type"
**Problem:** File format is not supported or Content-Type is wrong

**Solution:**
1. Only PNG and JPG/JPEG images are supported
2. Use images from the `saved_images/` folder
3. Avoid using .gif, .bmp, .webp, or other formats
4. For testing error handling, use .txt or .pdf files (this should return 400)

### Wrong body type selected
**Problem:** Using "binary" or "raw" instead of "form-data"

**Solution:**
1. In the Body tab, select **"form-data"** (first option)
2. Add a row with key "file", type "File"
3. Select your image file

### Prediction doesn't match expected label
**Problem:** Model predicts different digit than filename label

**Solution:**
- This is expected behavior for a trained model - it may make mistakes
- Check the confidence score: low confidence (<0.7) suggests uncertain prediction
- Test with multiple images to verify the API is functioning correctly
- The goal is to verify the API returns valid responses, not perfect accuracy

### Test scripts fail even with 200 response
**Problem:** Response format doesn't match expected schema

**Solution:**
1. Check the **Body** tab to see the actual response
2. Verify the response has both `digit` and `confidence` properties
3. Check the console for detailed error messages from test scripts

## Tips for Effective Testing

1. **Test Happy Path First**
   - Start with GET /health to verify connectivity
   - Then test POST /predict with a valid PNG image
   - Confirm all test scripts pass (green checkmarks)

2. **Test Error Cases**
   - After confirming happy path works, test error handling
   - This validates the API gracefully handles invalid inputs

3. **Use Collection Runner for Regression**
   - Run all tests together after code changes
   - Quickly verify nothing broke

4. **Check Response Times**
   - First request may be slower (model loading)
   - Subsequent requests should be < 2000ms
   - If consistently slow, check server resources

5. **Verify Different Image Formats**
   - Test both PNG (native format) and JPG (converted)
   - Confirms image preprocessing handles both formats

## Converting PNG to JPG (Optional)

To test JPG support, you can convert a PNG image:

**Using Python:**
```bash
python -c "from PIL import Image; img = Image.open('saved_images/img_0_label_6.png'); img.convert('RGB').save('test_digit.jpg')"
```

**Using ImageMagick:**
```bash
convert saved_images/img_0_label_6.png test_digit.jpg
```

Then use `test_digit.jpg` in the "POST /predict - JPG image" request.

## Next Steps

After completing manual testing with Postman:

1. ✅ Verify all test scripts pass
2. ✅ Document any unexpected behavior or edge cases
3. ✅ Share the collection with team members for collaborative testing
4. ✅ Consider exporting test results for reporting

For automated testing and CI/CD integration, see the pytest test suite in `test_api.py`.
