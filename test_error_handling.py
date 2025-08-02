import requests
import json

# URL of the advanced_materials_testing endpoint
url = 'http://127.0.0.1:8000/advanced_materials_testing/'

# Test cases for error handling
test_cases = [
    {
        "name": "Invalid JSON structure",
        "data": "This is not JSON",
        "expected_status": 400
    },
    {
        "name": "Missing sample_parameters",
        "data": {
            "water_system": {
                "water_pressure_in": 2.5,
                "water_pressure_out": 1.8
            },
            "scale_load_measurements": {
                "utn_scale": 85.5
            }
        },
        "expected_status": 200  # This should still work, as sample_parameters is optional
    },
    {
        "name": "Invalid numeric value",
        "data": {
            "sample_parameters": {
                "sample_number": "TEST-002",
                "mass": "not-a-number",
                "length": 200.0
            }
        },
        "expected_status": 400
    },
    {
        "name": "Invalid data structure",
        "data": {
            "sample_parameters": "not-an-object",
            "water_system": {},
            "scale_load_measurements": {}
        },
        "expected_status": 400
    }
]

# Run tests
print("Running error handling tests...\n")
for i, test in enumerate(test_cases, 1):
    print(f"Test {i}: {test['name']}")
    
    try:
        # Send POST request
        if isinstance(test['data'], str):
            # Send raw string for invalid JSON test
            response = requests.post(
                url,
                data=test['data'],
                headers={'Content-Type': 'application/json'}
            )
        else:
            # Send JSON data
            response = requests.post(
                url,
                data=json.dumps(test['data']),
                headers={'Content-Type': 'application/json'}
            )
        
        # Check status code
        status_match = response.status_code == test['expected_status']
        
        # Print results
        print(f"  Status Code: {response.status_code} (Expected: {test['expected_status']})")
        try:
            print(f"  Response: {response.json()}")
        except:
            print(f"  Response: {response.text}")
        
        print(f"  Result: {'PASS' if status_match else 'FAIL'}")
    except Exception as e:
        print(f"  Error: {str(e)}")
        print(f"  Result: FAIL")
    
    print()

print("All tests completed.")