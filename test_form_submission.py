import requests
import json

# URL of the advanced_materials_testing endpoint
url = 'http://127.0.0.1:8000/advanced_materials_testing/'

# Sample data to submit
data = {
    'sample_parameters': {
        'sample_number': 'TEST-001',
        'heat_number': 'HEAT-001',
        'mass': 150.5,
        'length': 200.0
    },
    'water_system': {
        'water_pressure_in': 2.5,
        'water_pressure_out': 1.8,
        'water_in_temperature': 25.0,
        'water_out_temperature': 30.0
    },
    'scale_load_measurements': {
        'utn_scale': 85.5,
        'yield_load_main_scale': 120.0,
        'yield_load_counter_part': 118.5,
        'tensile_load_main_scale': 150.0,
        'tensile_load_counter_part': 148.5
    }
}

# Send POST request
response = requests.post(
    url,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'}
)

# Print response
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

# Check if the submission was successful
if response.status_code == 200 and response.json().get('status') == 'success':
    print("\nForm submission successful!")
    print(f"Sample ID: {response.json().get('data', {}).get('sample_id')}")
    print(f"Water System ID: {response.json().get('data', {}).get('water_system_id')}")
    print(f"Scale Load ID: {response.json().get('data', {}).get('scale_load_id')}")
else:
    print("\nForm submission failed!")
    print(f"Error: {response.json().get('message')}")