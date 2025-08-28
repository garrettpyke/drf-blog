from django.db import models
from django.contrib.auth import get_user_model

"""
title : string
content : text
category: Category reference
author : user reference
updated_at/created_at
"""

class Blog(models.Model):
    title = models.CharField(blank=False, max_length=50)
    content = models.TextField(blank=True, max_length=1000)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, blank=True, default=1)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        # return self.title
        return f"{__class__}(title='{self.title}', content='{self.content}', category='{self.category}', author='{self.author}', updated='{self.updated_at}'"