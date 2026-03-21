from django.db import models

class Staff(models.Model):
    user_id = models.IntegerField(unique=True)
    role = models.CharField(max_length=64)
    department = models.CharField(max_length=128)
    hired_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=32)

class StaffPermission(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    permission_codename = models.CharField(max_length=128)

    class Meta:
        unique_together = ('staff', 'permission_codename')

class StaffAttendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=32)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

class StaffPerformance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=128)
    value = models.FloatField()
    evaluated_at = models.DateTimeField(auto_now_add=True)
