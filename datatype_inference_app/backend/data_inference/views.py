# data_inference/views.py
import os
import pandas as pd
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProcessedFile, ColumnMetadata
from .serializers import ProcessedFileSerializer, ColumnMetadataSerializer
from .infer_data_type import InferenceEngine

class DataInferenceViewSet(viewsets.ViewSet):
    """ViewSet for data processing operations."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = InferenceEngine()
    
    @action(detail=False, methods=['post'], url_path='upload')
    def upload_file(self, request):
        """Upload and process a data file."""
        
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj = request.FILES['file']
        apply_types = request.data.get('apply_inferred_types', 'false').lower() == 'true'
        
        # Save the uploaded file
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file_obj.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        
        try:
            # Process the file
            df, info_dict = self.engine.process_file(file_path, apply_inferred_types=apply_types)
            
            # Save processed file metadata
            processed_file = ProcessedFile.objects.create(
                file_name=file_obj.name,
                original_file=f"uploads/{file_obj.name}",
                file_size=file_obj.size,
                row_count=info_dict['total_rows'],
                column_count=info_dict['total_columns']
            )
            
            # Save the processed file
            if apply_types:
                processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed')
                os.makedirs(processed_dir, exist_ok=True)
                processed_path = os.path.join(processed_dir, f"processed_{file_obj.name}")
                df.to_csv(processed_path, index=False)
                processed_file.processed_file = f"processed/processed_{file_obj.name}"
                processed_file.save()
            
            # Save column metadata
            for col_info in info_dict['columns']:
                ColumnMetadata.objects.create(
                    processed_file=processed_file,
                    column_name=col_info['name'],
                    original_type=col_info['current_type'],
                    inferred_type=col_info['inferred_type'],
                    applied_type=col_info['inferred_type'] if apply_types else None,
                    null_count=col_info['null_count'],
                    unique_count=col_info['unique_count']
                )
            
            # Prepare response data
            response_data = {
                'file_id': processed_file.id,
                'file_name': processed_file.file_name,
                'total_rows': info_dict['total_rows'],
                'total_columns': info_dict['total_columns'],
                'memory_usage_bytes': info_dict['memory_usage_bytes'],
                'columns': info_dict['columns']
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'], url_path='apply-types')
    def apply_types(self, request, pk=None):
        """Apply custom data types to a processed file."""
        
        try:
            processed_file = ProcessedFile.objects.get(pk=pk)
        except ProcessedFile.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        
        column_types = request.data.get('column_types', {})
        if not column_types:
            return Response({"error": "No column types provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get the original file path
            file_path = os.path.join(settings.MEDIA_ROOT, processed_file.original_file.name)
            
            # Read the file
            df = self.engine.read_file(file_path)
            
            # Convert display type names to pandas dtype names
            pandas_types = {}
            for col, display_type in column_types.items():
                pandas_type = self.engine.display_dtype_mapping.get(display_type)
                if pandas_type:
                    pandas_types[col] = pandas_type
            
            # Apply the types
            converted_df = self.engine.convert_column_types(df, pandas_types)
            
            # Save the processed file
            processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed')
            os.makedirs(processed_dir, exist_ok=True)
            processed_path = os.path.join(processed_dir, f"processed_{processed_file.file_name}")
            converted_df.to_csv(processed_path, index=False)
            
            # Update the database record
            processed_file.processed_file = f"processed/processed_{processed_file.file_name}"
            processed_file.save()
            
            # Update column metadata
            for col, display_type in column_types.items():
                pandas_type = self.engine.display_dtype_mapping.get(display_type)
                try:
                    col_meta = ColumnMetadata.objects.get(processed_file=processed_file, column_name=col)
                    col_meta.applied_type = pandas_type
                    col_meta.save()
                except ColumnMetadata.DoesNotExist:
                    pass
            
            # Return success response
            return Response({
                "message": "Types applied successfully",
                "file_id": processed_file.id,
                "processed_file_url": processed_file.processed_file.url
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)