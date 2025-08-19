from django.db import models
from django.contrib.auth import get_user_model
from .blog import Blog

"""
vote : tinyint?
blog : blog reference
author : user reference
liked : updated_at
"""

class Vote(models.Model):
    LOVE = 2
    LIKE = 1
    NO_VOTE = 0
    DOWN_VOTE = -1
    VOTE_TYPE_CHOICES = {
        LOVE: "Love",
        LIKE: "Like",
        NO_VOTE: "",
        DOWN_VOTE: "Down"
    }
    vote_type = models.SmallIntegerField(default=VOTE_TYPE_CHOICES[NO_VOTE], choices=VOTE_TYPE_CHOICES)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    voter = models.ForeignKey(get_user_model(), on_delete=models.PROTECT) # let's save votes when user deleted
    voted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # return f"{__class__}(id='{self.id}'), 'vote_type='{self.vote_type}')"
        return f"{__class__}(id='{self.id}', 'vote_type='{self.vote_type}', blog='{self.blog}', voter='{self.voter}', voted_at='{self.voted_at}'"
