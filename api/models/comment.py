from django.db import models
from django.contrib.auth import get_user_model
from ..models.blog import Blog

"""
content : string
blog : blog reference
author : user reference
updated_at/created_at    
"""

class Comment(models.Model):
    content = models.TextField(blank=False, max_length=1000)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        # return f"{__class__}"
        return f"{__class__}(content='{self.content[:50]}', author='{self.author}', updated='{self.updated_at}'"
