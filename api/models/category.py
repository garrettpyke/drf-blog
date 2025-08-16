from django.db import models

"""
subject: string
genre: string
created_at
"""

class Category(models.Model):
    subject = models.CharField(blank=True, max_length=50)
    genre = models.CharField(blank=True, max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{__class__}(subject='{self.subject}', genre='{self.genre}', created_at='{self.created_at}'"