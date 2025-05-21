# data_inference/models.py
from django.db import models

class ProcessedFile(models.Model):
    """Model to store information about processed files."""
    
    file_name = models.CharField(max_length=255)
    original_file = models.FileField(upload_to='uploads/')
    processed_file = models.FileField(upload_to='processed/', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField()
    row_count = models.IntegerField()
    column_count = models.IntegerField()
    
    def __str__(self):
        return self.file_name

class ColumnMetadata(models.Model):
    """Model to store metadata about columns in processed files."""
    
    processed_file = models.ForeignKey(ProcessedFile, on_delete=models.CASCADE, related_name='columns')
    column_name = models.CharField(max_length=255)
    original_type = models.CharField(max_length=100)
    inferred_type = models.CharField(max_length=100)
    applied_type = models.CharField(max_length=100, null=True, blank=True)
    null_count = models.IntegerField()
    unique_count = models.IntegerField()
    
    def __str__(self):
        return f"{self.processed_file.file_name} - {self.column_name}"