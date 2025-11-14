"""
Custom template filters for consumers app
"""

from django import template
from django.conf import settings
from datetime import datetime
import logging

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def parse_iso_date(date_str, format_str="Y-m-d H:i"):
    """
    Parse ISO date string and format it for display
    Usage: {{ date_string|parse_iso_date:"Y-m-d H:i" }}
    """
    if not date_str or date_str in ["", "null", "None", None]:
        return "N/A"

    # Convert to string if it's not already
    if not isinstance(date_str, str):
        date_str = str(date_str)

    # List of common date formats to try
    formats_to_try = [
        "%Y-%m-%dT%H:%M:%SZ",  # 2024-01-01T12:00:00Z
        "%Y-%m-%dT%H:%M:%S",  # 2024-01-01T12:00:00
        "%Y-%m-%dT%H:%M:%S.%fZ",  # 2024-01-01T12:00:00.000Z
        "%Y-%m-%dT%H:%M:%S.%f",  # 2024-01-01T12:00:00.000
        "%Y-%m-%d %H:%M:%S",  # 2024-01-01 12:00:00
        settings.API_DATE_FORMAT_WITH_SECONDS,  # From settings
    ]

    # Try to parse with different formats
    for fmt in formats_to_try:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            # Convert Django date format to Python strftime format
            django_to_python = {
                "Y": "%Y",
                "m": "%m",
                "d": "%d",
                "H": "%H",
                "i": "%M",
                "s": "%S",
            }

            # Simple format conversion for common cases
            python_format = format_str
            for django_fmt, python_fmt in django_to_python.items():
                python_format = python_format.replace(django_fmt, python_fmt)

            return parsed_date.strftime(python_format)
        except (ValueError, TypeError):
            continue

    # Try using fromisoformat for Python 3.7+
    try:
        # Handle timezone indicator
        clean_date_str = date_str.replace("Z", "+00:00")
        parsed_date = datetime.fromisoformat(clean_date_str.replace("Z", ""))

        # Convert format and return
        python_format = format_str
        django_to_python = {
            "Y": "%Y",
            "m": "%m",
            "d": "%d",
            "H": "%H",
            "i": "%M",
            "s": "%S",
        }
        for django_fmt, python_fmt in django_to_python.items():
            python_format = python_format.replace(django_fmt, python_fmt)

        return parsed_date.strftime(python_format)
    except (ValueError, AttributeError):
        pass

    # Last resort - return the original string or N/A
    logger.warning(f"Could not parse date string: {date_str}")
    return "Invalid Date"


@register.filter
def smart_default(value, default_value="N/A"):
    """
    Smart default filter that handles various empty/null cases
    Usage: {{ value|smart_default:"Default Value" }}
    """
    if value is None or value == "" or value == "null" or value == "None":
        return default_value
    return value
