# data_inference/serializers.py
from rest_framework import serializers
from .models import ProcessedFile, ColumnMetadata

class ColumnMetadataSerializer(serializers.ModelSerializer):
    """Serializer for column metadata."""
    
    class Meta:
        model = ColumnMetadata
        fields = ['id', 'column_name', 'original_type', 'inferred_type', 
                  'applied_type', 'null_count', 'unique_count']

class ProcessedFileSerializer(serializers.ModelSerializer):
    """Serializer for processed files with included column data."""
    
    columns = ColumnMetadataSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProcessedFile
        fields = ['id', 'file_name', 'original_file', 'processed_file', 
                  'upload_date', 'file_size', 'row_count', 'column_count', 'columns']