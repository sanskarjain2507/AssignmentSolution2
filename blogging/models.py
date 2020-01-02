from django.db import models

class Blogs(models.Model):
    id=models.AutoField(primary_key=True)
    charblog=models.CharField(max_length=50000,blank=True,null=True)
    fileblog=models.FileField(upload_to='problem1/media',blank=True,null=True)
    fileblog_content=models.CharField(max_length=50000,blank=True,null=True)
    fileblog_updated_content=models.CharField(max_length=50000,blank=True,null=True)
    charblog_updated_content=models.CharField(max_length=50000,blank=True,null=True)
    createdTime=models.DateTimeField(auto_now_add=True)
    updationTime=models.DateTimeField(auto_now=True)
