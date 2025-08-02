from django.db import transaction
from .models import StressCalculation
from .calclation import (
    division_10kgf,
    division_25kgf,
    division_50kgf,
    division_100kgf
)

def calculate_and_store_stress(
    mass,
    length,
    utn_scale,
    yield_load_main_scale,
    yield_load_counter_part,
    tensile_load_main_scale,
    tensile_load_counter_part,
    sample_parameters=None,
    inspection_report=None
):
    """
    Calculate stress values and store them in the database
    """
    try:
        # Calculate derived values
        mass_per_meter = mass / length
        cross_section_area = mass_per_meter / 0.00785
        
        # Calculate machine readings
        yield_machine_reading = yield_load_main_scale + utn_scale * yield_load_counter_part
        tensile_machine_reading = tensile_load_main_scale + utn_scale * tensile_load_counter_part
        
        # Select and call the appropriate division function based on UTN scale value
        division_functions = {
            10: division_10kgf,
            25: division_25kgf,
            50: division_50kgf,
            100: division_100kgf
        }
        
        if utn_scale not in division_functions:
            raise ValueError(f"Invalid UTN scale value: {utn_scale}. Must be 10, 25, 50, or 100")
            
        # Calculate stresses
        yield_stress, tensile_stress = division_functions[utn_scale](
            yield_machine_reading,
            tensile_machine_reading,
            cross_section_area
        )
        
        # Store results in database
        with transaction.atomic():
            stress_calc = StressCalculation.objects.create(
                # Physical Properties
                mass_per_meter=mass_per_meter,
                cross_section_area=cross_section_area,
                
                # Machine Readings
                yield_machine_reading=yield_machine_reading,
                tensile_machine_reading=tensile_machine_reading,
                
                # Stress Analysis Results
                yield_stress=yield_stress,
                tensile_stress=tensile_stress,
                division_type=f"Division {utn_scale}kgf",
                
                # Relations
                sample_parameters=sample_parameters,
                inspection_report=inspection_report
            )
        
        return {
            'success': True,
            'stress_calculation': stress_calc,
            'calculated_values': {
                'mass_per_meter': mass_per_meter,
                'cross_section_area': cross_section_area,
                'yield_machine_reading': yield_machine_reading,
                'tensile_machine_reading': tensile_machine_reading,
                'yield_stress': yield_stress,
                'tensile_stress': tensile_stress,
                'division_type': f"Division {utn_scale}kgf"
            }
        }
        
    except ValueError as e:
        return {'success': False, 'error': f"Invalid input - {str(e)}"}
    except ZeroDivisionError:
        return {'success': False, 'error': "Division by zero. Check your input values."}
    except Exception as e:
        return {'success': False, 'error': f"An unexpected error occurred: {str(e)}"}
