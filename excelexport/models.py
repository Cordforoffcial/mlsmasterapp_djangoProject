from django.db import models
from django.core.validators import MinValueValidator

class CountryGDP(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    year = models.CharField(max_length=4)
    value = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)

    def str(self):
        return self.name

class InspectionReport(models.Model):
    date = models.DateField()
    batch_number = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def str(self):
        return f"Inspection Report - Batch {self.batch_number} ({self.date})"

class SampleParameters(models.Model):
    """
    Basic sample identification and properties
    """
    sample_number = models.CharField(
        max_length=100,
        help_text="Enter sample identification number"
    )
    heat_number = models.CharField(
        max_length=100,
        help_text="Enter heat treatment number"
    )
    mass = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter mass value (grams)"
    )
    length = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter length value (mm)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sample Parameters"
        verbose_name_plural = "Sample Parameters"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sample {self.sample_number} - Heat {self.heat_number}"

class WaterSystem(models.Model):
    """
    Cooling system parameters and measurements
    """
    water_pressure_in = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter inlet pressure (bar)"
    )
    water_pressure_out = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter outlet pressure (bar)"
    )
    water_in_temperature = models.FloatField(
        help_text="Enter inlet temperature (°C)"
    )
    water_out_temperature = models.FloatField(
        help_text="Enter outlet temperature (°C)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Water System"
        verbose_name_plural = "Water Systems"
        ordering = ['-created_at']

    def __str__(self):
        return f"Water System - In: {self.water_in_temperature}°C, Out: {self.water_out_temperature}°C"

    @property
    def temperature_difference(self):
        """Calculate temperature difference between inlet and outlet"""
        return self.water_out_temperature - self.water_in_temperature

    @property
    def pressure_drop(self):
        """Calculate pressure drop across the system"""
        return self.water_pressure_in - self.water_pressure_out
      
class ScaleLoadMeasurements(models.Model):
    """
    UTN scale and mechanical load testing data
    """
    utn_scale = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter UTN scale value"
    )
    yield_load_main_scale = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter yield load (kN)"
    )
    yield_load_counter_part = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter counter yield load (kN)"
    )
    tensile_load_main_scale = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter tensile load (kN)"
    )
    tensile_load_counter_part = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter counter tensile load (kN)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Scale & Load Measurements"
        verbose_name_plural = "Scale & Load Measurements"
        ordering = ['-created_at']

    def __str__(self):
        return f"UTN Scale: {self.utn_scale} - Yield: {self.yield_load_main_scale}kN"

    @property
    def total_yield_load(self):
        """Calculate total yield load"""
        return self.yield_load_main_scale + self.yield_load_counter_part

    @property
    def total_tensile_load(self):
        """Calculate total tensile load"""
        return self.tensile_load_main_scale + self.tensile_load_counter_part

    @property
    def yield_load_difference(self):
        """Calculate difference between main and counter yield loads"""
        return abs(self.yield_load_main_scale - self.yield_load_counter_part)

    @property
    def tensile_load_difference(self):
        """Calculate difference between main and counter tensile loads"""
        return abs(self.tensile_load_main_scale - self.tensile_load_counter_part)

class StressCalculation(models.Model):
    """
    Stores material stress calculation results
    """
    # Physical Properties
    mass_per_meter = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Mass per meter (kg/m)"
    )
    cross_section_area = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Cross section area (mm²)"
    )

    # Machine Readings
    yield_machine_reading = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Yield load machine reading (kgf)"
    )
    tensile_machine_reading = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Tensile load machine reading (kgf)"
    )

    # Stress Analysis Results
    yield_stress = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Calculated yield stress (N/mm²)"
    )
    tensile_stress = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Calculated tensile stress (N/mm²)"
    )
    division_type = models.CharField(
        max_length=50,
        help_text="Division type classification"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional relations to other models
    sample_parameters = models.ForeignKey(
        SampleParameters,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stress_calculations'
    )
    inspection_report = models.ForeignKey(
        InspectionReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stress_calculations'
    )

    class Meta:
        verbose_name = "Stress Calculation"
        verbose_name_plural = "Stress Calculations"
        ordering = ['-created_at']

    def __str__(self):
        return f"Stress Calculation - Yield: {self.yield_stress} N/mm², Tensile: {self.tensile_stress} N/mm²"