from django.db import models
from django import forms
from django.contrib import admin
import sys

from recordings.models import Recording
from clips.models import Clip,CatalogClip

class Game(models.Model):
    name = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.name

class Level(models.Model):
    game = models.ForeignKey(Game, related_name='levels')
    queryClip = models.ForeignKey(Clip, related_name='queryClip', null=True, blank=True)
    correctReferenceClip = models.ForeignKey(CatalogClip, related_name='correctReferenceClip', null=True, blank=True)
    otherReferenceClip1 = models.ForeignKey(CatalogClip, related_name='otherReferenceClip1', null=True, blank=True)
    otherReferenceClip2 = models.ForeignKey(CatalogClip, related_name='otherReferenceClip2', null=True, blank=True)
    otherReferenceClip3 = models.ForeignKey(CatalogClip, related_name='otherReferenceClip3', null=True, blank=True)

    def percentCorrect(self, origin):
        allUserClassifications = self.userclassification_set.filter(origin__contains=origin)
        correctUserClassifications = self.userclassification_set.filter(correct=True, origin__contains=origin)

        if len(allUserClassifications) == 0:
            percentCorrect = 0
        else:
            percentCorrect = float(len(correctUserClassifications)) / float(len(allUserClassifications))

        return percentCorrect
            
    def userData(self, origin):
        allUserClassifications = self.userclassification_set.filter(origin__contains=origin)
        correctUserClassifications = self.userclassification_set.filter(correct=True, origin__contains=origin)

        if len(allUserClassifications) == 0:
            percentCorrect = 0
        else:
            percentCorrect = 100.0 * (float(len(correctUserClassifications)) / float(len(allUserClassifications)))

        output = {'percentCorrect' : percentCorrect, 'numCorrect' : len(correctUserClassifications), 'numTotal' : len(allUserClassifications)}
        return output

    def labelCounts(self,origin):
        allUserClassifications = self.userclassification_set.filter(origin__contains=origin)
        labelCounts = {}
        for userClassification in allUserClassifications:
            label = userClassification.reference.name
            if label in labelCounts:
                labelCounts[label] += 1
            else:
                labelCounts[label] = 0

        return labelCounts
        
    def __unicode__(self):
        return str(self.pk)

class UserClassification(models.Model):
    level = models.ForeignKey(Level, null=True)
    userEvents = models.TextField()
    query = models.ForeignKey(Clip, related_name='userQueryClip', null=True, blank=True)
    reference = models.ForeignKey(Clip, related_name='userReferenceClip', null=True, blank=True)
    remoteAddr = models.CharField(max_length = 50)
    origin = models.CharField(max_length = 200)
    userAgent = models.CharField(max_length = 200)
    guid = models.CharField(max_length = 200)
    correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now = True, auto_now_add = True)

    def __unicode__(self):
        return str(self.timestamp)

class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name'] 

class LevelAdmin(admin.ModelAdmin):
    pass

class UserClassificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'correct', 'query', 'reference', 'origin', 'guid', 'timestamp'] 

admin.site.register(Game, GameAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(UserClassification, UserClassificationAdmin)
