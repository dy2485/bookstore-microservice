from rest_framework import serializers
from .models import UserPreference, UserHistory, Recommendation, RecommenderConfig, ModelVersion, Feedback

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'

class UserHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHistory
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'

class RecommenderConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommenderConfig
        fields = '__all__'

class ModelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelVersion
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
