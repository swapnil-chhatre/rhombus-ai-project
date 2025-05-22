// src/utils/dataTypeUtils.js
// Mapping between internal data types and user-friendly display names
export const dataTypeMapping = {
    'object': 'Text',
    'int64': 'Integer',
    'float64': 'Decimal',
    'datetime64[ns]': 'Date/Time',
    'bool': 'Boolean',
    'category': 'Category',
    'timedelta[ns]': 'Time Duration',
    'complex128': 'Complex Number',
  };
  
  // Reverse mapping for converting display names to internal types
  export const reverseTypeMapping = Object.entries(dataTypeMapping)
    .reduce((acc, [key, value]) => {
      acc[value] = key;
      return acc;
    }, {});
  
  // Get all available data types for the dropdown
  export const getAvailableTypes = () => Object.values(dataTypeMapping);
  
  // Get user-friendly name for a pandas type
  export const getFriendlyTypeName = (pandasType) => {
    return dataTypeMapping[pandasType] || pandasType;
  };
  
  // Format bytes to human-readable format
  export const formatBytes = (bytes, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';
  
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  
    const i = Math.floor(Math.log(bytes) / Math.log(k));
  
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  };