from django.db import models
from accounts.models import User
import openai

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    ai_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    likes = models.ManyToManyField(User, related_name='liked_tweets')
    retweets = models.ManyToManyField(User, related_name='retweeted_tweets')
    
    def generate_ai_description(self):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Summarize this tweet: {self.content}",
                max_tokens=60
            )
            self.ai_description = response.choices[0].text.strip()
            self.save()
        except Exception as e:
            print(f"Error generating AI description: {e}") 

class Media(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='tweet_media/')
    type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    created_at = models.DateTimeField(auto_now_add=True) 

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet') 
