# utils/file_utils.py
import os
import logging

logger = logging.getLogger(__name__)


def delete_temp_file(file_path: str) -> None:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted temp file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to delete temp file {file_path}: {e}")
        # don't raise — cleanup failure shouldn't crash the pipeline
