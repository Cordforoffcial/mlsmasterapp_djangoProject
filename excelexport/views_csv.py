import csv
from django.http import HttpResponse
from .models import StressCalculation, InspectionReport

def mechanical_inspection_csv_export(request):
    """
    Export mechanical inspection report data as CSV
    """
    # Fetch all stress calculations with related data
    stress_calculations = StressCalculation.objects.select_related(
        'sample_parameters', 'inspection_report'
    ).order_by('created_at')[:15]  # Get oldest 15 records in ascending time order
    
    # Get header data from the latest inspection report
    header_data = {
        'section': '',
        'lot_no': '',
        'date_of_rolling': ''
    }
    
    latest_inspection = InspectionReport.objects.order_by('-created_at').first()
    if latest_inspection:
        header_data['section'] = latest_inspection.section
        header_data['lot_no'] = latest_inspection.batch_number
        header_data['date_of_rolling'] = latest_inspection.date.strftime('%Y-%m-%d')
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mechanical_properties_report.csv"'
    
    writer = csv.writer(response)
    
    # Write header information
    writer.writerow(['Final Inspection Report - Mechanical Properties'])
    writer.writerow([])  # Empty row
    writer.writerow(['Section:', header_data['section']])
    writer.writerow(['Lot No:', header_data['lot_no']])
    writer.writerow(['Date of Rolling:', header_data['date_of_rolling']])
    writer.writerow([])  # Empty row
    
    # Write table headers
    headers = [
        'S. No', 'Heat Number', 'Time', 'Mass (kg)', 'Length (m)', 
        'Mass/Meter (kg/m)', 'Cross Sec Area (mm²)', 'Calibrated Yield Load (kN)',
        'Yield Stress (N/mm²)', 'Calibrated Tensile Load (kN)', 'Tensile Stress (N/mm²)',
        'Elongation %', 'Bend Test'
    ]
    writer.writerow(headers)
    
    # Write data rows
    for i, calc in enumerate(stress_calculations, 1):
        sample = calc.sample_parameters
        
        row = [
            i,  # Serial number
            sample.heat_number if sample else '',
            calc.created_at.strftime('%H:%M:%S') if calc.created_at else '',
            f"{sample.mass:.2f}" if sample and sample.mass else '',
            f"{sample.length:.3f}" if sample and sample.length else '',
            f"{calc.mass_per_meter:.4f}" if calc.mass_per_meter else '',
            f"{calc.cross_section_area:.2f}" if calc.cross_section_area else '',
            f"{calc.yield_machine_reading:.1f}" if calc.yield_machine_reading else '',
            f"{calc.yield_stress:.2f}" if calc.yield_stress else '',
            f"{calc.tensile_machine_reading:.1f}" if calc.tensile_machine_reading else '',
            f"{calc.tensile_stress:.2f}" if calc.tensile_stress else '',
            '',  # Elongation - not in current model
            ''   # Bend Test - not in current model
        ]
        writer.writerow(row)
    
    # Add summary statistics if we have data
    if stress_calculations:
        writer.writerow([])  # Empty row
        
        # Calculate summary statistics
        numeric_data = {
            'mass': [],
            'length': [],
            'mass_per_meter': [],
            'cross_section_area': [],
            'calibrated_yield_load': [],
            'yield_stress': [],
            'calibrated_tensile_load': [],
            'tensile_stress': []
        }
        
        for calc in stress_calculations:
            sample = calc.sample_parameters
            if sample and sample.mass:
                numeric_data['mass'].append(sample.mass)
            if sample and sample.length:
                numeric_data['length'].append(sample.length)
            if calc.mass_per_meter:
                numeric_data['mass_per_meter'].append(calc.mass_per_meter)
            if calc.cross_section_area:
                numeric_data['cross_section_area'].append(calc.cross_section_area)
            if calc.yield_machine_reading:
                numeric_data['calibrated_yield_load'].append(calc.yield_machine_reading)
            if calc.yield_stress:
                numeric_data['yield_stress'].append(calc.yield_stress)
            if calc.tensile_machine_reading:
                numeric_data['calibrated_tensile_load'].append(calc.tensile_machine_reading)
            if calc.tensile_stress:
                numeric_data['tensile_stress'].append(calc.tensile_stress)
        
        # Write Min row
        min_row = ['Min', '', '']
        for field in ['mass', 'length', 'mass_per_meter', 'cross_section_area', 
                     'calibrated_yield_load', 'yield_stress', 'calibrated_tensile_load', 'tensile_stress']:
            if numeric_data[field]:
                min_row.append(f"{min(numeric_data[field]):.2f}")
            else:
                min_row.append('')
        min_row.extend(['', ''])  # Elongation and Bend Test
        writer.writerow(min_row)
        
        # Write Max row
        max_row = ['Max', '', '']
        for field in ['mass', 'length', 'mass_per_meter', 'cross_section_area', 
                     'calibrated_yield_load', 'yield_stress', 'calibrated_tensile_load', 'tensile_stress']:
            if numeric_data[field]:
                max_row.append(f"{max(numeric_data[field]):.2f}")
            else:
                max_row.append('')
        max_row.extend(['', ''])  # Elongation and Bend Test
        writer.writerow(max_row)
        
        # Write Average row
        avg_row = ['AVG', '', '']
        for field in ['mass', 'length', 'mass_per_meter', 'cross_section_area', 
                     'calibrated_yield_load', 'yield_stress', 'calibrated_tensile_load', 'tensile_stress']:
            if numeric_data[field]:
                avg_row.append(f"{sum(numeric_data[field])/len(numeric_data[field]):.2f}")
            else:
                avg_row.append('')
        avg_row.extend(['', ''])  # Elongation and Bend Test
        writer.writerow(avg_row)
    
    return response