from django.db import models

class Comment(models.Model):
    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, default='active')

class CommentReply(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author_id = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CommentVote(models.Model):
    customer_id = models.IntegerField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(1, 'Up'), (-1, 'Down')])

    class Meta:
        unique_together = ('customer_id', 'comment')

class BookRatingAggregate(models.Model):
    book_id = models.IntegerField(unique=True)
    avg_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)

class ReviewReport(models.Model):
    reporter_id = models.IntegerField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.CharField(max_length=256)
    status = models.CharField(max_length=32, default='pending')
    reviewed_at = models.DateTimeField(null=True, blank=True)
