from rest_framework import serializers
from .models import Comment, CommentReply, CommentVote, BookRatingAggregate, ReviewReport

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = '__all__'

class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = '__all__'

class BookRatingAggregateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRatingAggregate
        fields = '__all__'

class ReviewReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReport
        fields = '__all__'
