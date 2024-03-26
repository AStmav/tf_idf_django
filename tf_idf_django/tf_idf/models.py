from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')

class Words(models.Model):
    word = models.CharField(max_length=100)
    tf = models.FloatField()
    idf = models.FloatField()


    def __str__(self):
        return self.word


# Create your models here.idf = models.FloatField()
