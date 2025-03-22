import memory_profiler
import logging
import asyncio
import json

# Configure logger
_logger = logging.getLogger("memory_profiler")
logging.basicConfig(level=logging.INFO)

profiler_logstream = memory_profiler.LogFile("memory_profiler_logs", True)

async def memory_profiled_async(func):
    """Decorator for profiling async functions with manual control."""
    async def wrapper(*args, **kwargs):
        profiler = memory_profiler.Profile()
        profiler.enable()  # Start memory profiling
        _logger.info(f"Profiling started for {func.__name__}")
        
        result = await func(*args, **kwargs)  # Execute async function
        
        profiler.disable()  # Stop profiling
        memory_profiler.show_results(profiler, stream=profiler_logstream)  # Print results
        profiler_logstream.flush()  # Ensure logs are written
        _logger.info(f"Profiling completed for {func.__name__}")
        
        return result
    return wrapper

class Example:
    @memory_profiled_async
    async def run(self):
        """Execute the PDF conversion process with OCR results."""
        _logger.info("[create_searchable_pdf] Activity started")
        
        input_data = self.input
        blob_name = None  # Initialize blob_name
        
        if input_data.converted_document_output and input_data.converted_document_output.blob_name:
            blob_name = input_data.converted_document_output.blob_name
        
        if input_data.blob_reference.blob_name and not blob_name:
            blob_name = input_data.blob_reference.blob_name
        
        updated_blob = input_data.blob_reference.copy()
        updated_blob.blob_name = blob_name
        
        _logger.info("[create_searchable_pdf] Downloading blob content")
        content = await updated_blob.download_content()
        _logger.info("[create_searchable_pdf] Blob content downloaded")
        
        if not isinstance(content, bytes):
            raise ValueError("PDF content must be of type bytes.")
        
        # Prepare form-data payload
        json_data = json.dumps(input_data.form_recognizer_result.dict())
        files = {
            "file": ("file", content, "application/octet-stream"),
            "data": ("fr_results", json_data, "application/json"),
        }
        
        _logger.info("[create_searchable_pdf] HTTPX files created")

        return blob_name  # Return something useful

# Example usage
example = Example()
asyncio.run(example.run())  # Run the async function
