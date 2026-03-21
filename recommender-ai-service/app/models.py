from django.db import models

class UserPreference(models.Model):
    customer_id = models.IntegerField(unique=True)
    genre_preferences = models.JSONField(default=dict, blank=True)
    author_preferences = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserHistory(models.Model):
    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    action_type = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

class Recommendation(models.Model):
    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    score = models.FloatField()
    source = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

class RecommenderConfig(models.Model):
    key = models.CharField(max_length=128, unique=True)
    value = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class ModelVersion(models.Model):
    name = models.CharField(max_length=128)
    artifact_path = models.CharField(max_length=512)
    trained_at = models.DateTimeField()
    metrics = models.JSONField(default=dict, blank=True)

class Feedback(models.Model):
    customer_id = models.IntegerField()
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
