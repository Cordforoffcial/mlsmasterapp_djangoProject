def division_25kgf(yield_machine_reading, tensile_machine_reading, cross_section_area):
    """Division 25kgf function"""
    A = 7.44259E-02
    B = 1.08840E-02
    C = -2.11336E-07
    D = 2.84359E-11
    
    x = yield_machine_reading
    y = tensile_machine_reading
    
    fy = A + B*x + C*x*x + D*x*x*x  
    ft = A + B*y + C*y*y + D*y*y*y
    
    yield_stress = 1000 * fy / cross_section_area
    tensile_stress = 1000 * ft / cross_section_area
    
    print("Division 25kgf Results:")
    print("Yield stress: {:.2f}".format(yield_stress))
    print("Tensile stress: {:.2f}".format(tensile_stress))
    
    return yield_stress, tensile_stress

def division_10kgf(yield_machine_reading, tensile_machine_reading, cross_section_area):
    """Division 10kgf function"""
    A = -4.81989E-01
    B = 1.17226E-02
    C = -6.85762E-07
    D = 1.60764E-10
    
    x = yield_machine_reading
    y = tensile_machine_reading
    
    fy = A + B*x + C*x*x + D*x*x*x  
    ft = A + B*y + C*y*y + D*y*y*y
    
    yield_stress = 1000 * fy / cross_section_area
    tensile_stress = 1000 * ft / cross_section_area
    
    print("Division 10kgf Results:")
    print("Yield stress: {:.2f}".format(yield_stress))
    print("Tensile stress: {:.2f}".format(tensile_stress))
    
    return yield_stress, tensile_stress

def division_50kgf(yield_machine_reading, tensile_machine_reading, cross_section_area):
    """Division 50kgf function"""
    A = 1.25491E-01
    B = 1.11779E-02
    C = -1.34602E-07
    D = 7.57921E-12
    
    x = yield_machine_reading
    y = tensile_machine_reading
    
    fy = A + B*x + C*x*x + D*x*x*x  
    ft = A + B*y + C*y*y + D*y*y*y
    
    yield_stress = 1000 * fy / cross_section_area
    tensile_stress = 1000 * ft / cross_section_area
    
    print("Division 50kgf Results:")
    print("Yield stress: {:.2f}".format(yield_stress))
    print("Tensile stress: {:.2f}".format(tensile_stress))
    
    return yield_stress, tensile_stress

def division_100kgf(yield_machine_reading, tensile_machine_reading, cross_section_area):
    """Division 100kgf function"""
    A = 8.14388E-01
    B = 1.17947E-02
    C = -1.26474E-07
    D = 3.03105E-12
    
    x = yield_machine_reading
    y = tensile_machine_reading
    
    fy = A + B*x + C*x*x + D*x*x*x  
    ft = A + B*y + C*y*y + D*y*y*y
    
    yield_stress = 1000 * fy / cross_section_area
    tensile_stress = 1000 * ft / cross_section_area
    
    print("Division 100kgf Results:")
    print("Yield stress: {:.2f}".format(yield_stress))
    print("Tensile stress: {:.2f}".format(tensile_stress))
    
    return yield_stress, tensile_stress

def main():
    print("Material Stress Calculator")
    print("=" * 40)
    
    try:
        # Get input values from keyboard
        mass = float(input("Enter mass value: "))
        length = float(input("Enter length value: "))
        utn_scale = float(input("Enter UTN scale value: "))
        yield_load_main_scale = float(input("Enter yield load main scale: "))
        yield_load_counter_part = int(input("Enter yield load counter part: "))
        tensile_load_main_scale = float(input("Enter tensile load main scale: "))
        tensile_load_counter_part = int(input("Enter tensile load counter part: "))
        
        # Calculate derived values
        mass_per_meter = mass / length
        cross_section_area = mass_per_meter / 0.00785
        
        # Calculate machine readings
        yield_machine_reading = yield_load_main_scale + utn_scale * yield_load_counter_part
        tensile_machine_reading = tensile_load_main_scale + utn_scale * tensile_load_counter_part
        
        print("\nCalculated Values:")
        print("Mass per meter: {:.4f}".format(mass_per_meter))
        print("Cross section area: {:.4f}".format(cross_section_area))
        print("Yield machine reading: {:.4f}".format(yield_machine_reading))
        print("Tensile machine reading: {:.4f}".format(tensile_machine_reading))
        print()
        
        # Select and call the appropriate division function based on UTN scale value
        print("Selected division based on UTN scale value ({:.0f}):".format(utn_scale))
        print("-" * 40)
        
        if utn_scale == 10:
            yield_stress, tensile_stress = division_10kgf(yield_machine_reading, tensile_machine_reading, cross_section_area)
        elif utn_scale == 25:
            yield_stress, tensile_stress = division_25kgf(yield_machine_reading, tensile_machine_reading, cross_section_area)
        elif utn_scale == 50:
            yield_stress, tensile_stress = division_50kgf(yield_machine_reading, tensile_machine_reading, cross_section_area)
        elif utn_scale == 100:
            yield_stress, tensile_stress = division_100kgf(yield_machine_reading, tensile_machine_reading, cross_section_area)
        else:
            print("Error: UTN scale value must be 10, 25, 50, or 100")
            print("You entered: {:.0f}".format(utn_scale))
            return
        
    except ValueError as e:
        print("Error: Invalid input - {}".format(e))
    except ZeroDivisionError:
        print("Error: Division by zero. Check your input values.")
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))

if __name__ == "__main__":
    main()