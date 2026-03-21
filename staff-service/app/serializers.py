from rest_framework import serializers
from .models import Staff, StaffPermission, StaffAttendance, StaffPerformance

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class StaffPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPermission
        fields = '__all__'

class StaffAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAttendance
        fields = '__all__'

class StaffPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPerformance
        fields = '__all__'
