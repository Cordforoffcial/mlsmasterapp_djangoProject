from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(CountryGDP)
class CountryGDPAdmin(ImportExportModelAdmin):
    list_display = ('name','year','code','value')
    list_filter = ['name']
    search_fields = ['name']


@admin.register(InspectionReport)
class InspectionReportAdmin(ImportExportModelAdmin):
    list_display = ('date', 'batch_number', 'section', 'created_at', 'updated_at')
    list_filter = ['date', 'section']
    search_fields = ['batch_number', 'section']
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date', '-created_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields
        return ()


@admin.register(SampleParameters)
class SampleParametersAdmin(ImportExportModelAdmin):
    list_display = ('sample_number', 'heat_number', 'mass', 'length', 'created_at')
    list_filter = ['heat_number', 'created_at']
    search_fields = ['sample_number', 'heat_number']
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(WaterSystem)
class WaterSystemAdmin(ImportExportModelAdmin):
    list_display = ('water_in_temperature', 'water_out_temperature', 'water_pressure_in', 'water_pressure_out', 'created_at')
    list_filter = ['created_at']
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('temperature_difference', 'pressure_drop')
        return self.readonly_fields


@admin.register(ScaleLoadMeasurements)
class ScaleLoadMeasurementsAdmin(ImportExportModelAdmin):
    list_display = ('utn_scale', 'yield_load_main_scale', 'tensile_load_main_scale', 'created_at')
    list_filter = ['created_at']
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('total_yield_load', 'total_tensile_load',
                                          'yield_load_difference', 'tensile_load_difference')
        return self.readonly_fields


@admin.register(StressCalculation)
class StressCalculationAdmin(ImportExportModelAdmin):
    list_display = (
        'yield_stress', 
        'tensile_stress', 
        'division_type',
        'mass_per_meter',
        'cross_section_area',
        'created_at'
    )
    list_filter = ['division_type', 'created_at']
    search_fields = ['division_type']
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Physical Properties', {
            'fields': ('mass_per_meter', 'cross_section_area')
        }),
        ('Machine Readings', {
            'fields': ('yield_machine_reading', 'tensile_machine_reading')
        }),
        ('Stress Analysis Results', {
            'fields': ('yield_stress', 'tensile_stress', 'division_type')
        }),
        ('Relations', {
            'fields': ('sample_parameters', 'inspection_report')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )