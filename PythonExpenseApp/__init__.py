# ===================================================================
# PYTHON EXPENSE APP PACKAGE INITIALIZATION
# ===================================================================
# This file marks the PythonExpenseApp directory as a Python package
# and handles package-level imports and configuration.
#
# PACKAGE PURPOSE:
# The PythonExpenseApp package provides a comprehensive trip management
# system with the following core modules:
#
# 1. main.py - Application entry point and main dashboard
# 2. db_connection.py - Database connectivity and query management
# 3. student.py - Student entity and user management
# 4. activity.py - Activity management and scheduling
# 5. expense.py - Financial transaction and debt tracking
# 6. feedback.py - Student feedback and rating system
# 7. statistics.py - Analytics and sentiment analysis
# 8. gui/ - User interface components and windows
#
# PACKAGE STRUCTURE:
# PythonExpenseApp/
# ├── __init__.py (this file)
# ├── main.py
# ├── db_connection.py
# ├── student.py
# ├── activity.py
# ├── expense.py
# ├── feedback.py
# ├── statistics.py
# ├── daily_program.py
# ├── group.py
# └── gui/
#     ├── login_gui.py
#     ├── expense_gui.py
#     ├── activity_form_gui.py
#     └── activity_details_gui.py
# ===================================================================

"""
Trip Manager Application Package

A comprehensive Python application for managing school trips, student activities,
expenses, and feedback with an intuitive GUI interface.

This package provides:
- Student authentication and profile management
- Activity scheduling and subscription management
- Expense tracking with automatic debt calculation
- Feedback collection with sentiment analysis
- Real-time statistics and reporting

Modules:
    main: Application entry point and main dashboard
    db_connection: Database connectivity and query execution
    student: Student entity and user management
    activity: Activity management and scheduling
    expense: Financial transaction and debt tracking
    feedback: Student feedback and rating system
    statistics: Analytics and sentiment analysis
    daily_program: Schedule management utilities
    group: Student grouping functionality
    gui: User interface components package

Usage:
    python -m PythonExpenseApp.main

Requirements:
    - Python 3.8+
    - MySQL Server 8.0+
    - mysql-connector-python
    - tkinter (usually included with Python)
    - PIL (Pillow) for image processing
"""

# Package metadata - Used by setup tools and for package information
__version__ = "1.0.0"
__author__ = "Trip Manager Development Team"
__email__ = "support@tripmanager.edu"
__description__ = "Comprehensive trip management system for educational institutions"
__license__ = "MIT"

# Package-level imports - Make core classes available at package level
# This allows users to import directly from the package root
try:
    # Core entity classes - The main business objects
    from .student import Student
    from .activity import Activity
    from .expense import Expense
    from .feedback import Feedback
    from .statistics import Statistics
    from .group import Group
    
    # Database connection - Essential for all operations
    from .db_connection import DbConnection
    
    # Set what's available when someone does "from PythonExpenseApp import *"
    __all__ = [
        'Student',      # Student entity and user management
        'Activity',     # Activity management and scheduling
        'Expense',      # Financial transaction handling
        'Feedback',     # Student feedback system
        'Statistics',   # Analytics and reporting
        'Group',        # Student grouping functionality
        'DbConnection', # Database connectivity
    ]
    
except ImportError as e:
    # Handle import errors gracefully - some modules might not be available
    # during development or if dependencies are missing
    import warnings
    warnings.warn(f"Could not import all modules: {e}", ImportWarning)
    __all__ = []

# Package configuration constants
# These can be imported and used throughout the application
class Config:
    """
    Package-wide configuration constants.
    
    This class holds configuration values that are used across
    multiple modules in the application.
    """
    
    # Application Information
    APP_NAME = "Trip Manager"
    APP_VERSION = __version__
    APP_TITLE = f"{APP_NAME} v{APP_VERSION}"
    
    # GUI Configuration
    DEFAULT_WINDOW_WIDTH = 1200
    DEFAULT_WINDOW_HEIGHT = 800
    DEFAULT_FONT_FAMILY = "Segoe UI"
    DEFAULT_FONT_SIZE = 12
    
    # Color Scheme - Modern, accessible color palette
    COLORS = {
        'primary': '#3b82f6',      # Blue - Primary action buttons
        'secondary': '#64748b',     # Gray - Secondary elements
        'success': '#059669',       # Green - Success messages, positive actions
        'warning': '#f59e0b',       # Yellow - Warnings, neutral states
        'danger': '#dc2626',        # Red - Errors, dangerous actions
        'background': '#f8fafc',    # Light gray - Main background
        'surface': '#ffffff',       # White - Card/surface background
        'text_primary': '#1e293b',  # Dark gray - Primary text
        'text_secondary': '#64748b', # Medium gray - Secondary text
        'border': '#e2e8f0',       # Light gray - Borders and dividers
    }
    
    # Business Logic Constants
    MIN_RATING = 1              # Minimum feedback rating
    MAX_RATING = 5              # Maximum feedback rating
    MIN_STUDENT_AGE = 14        # Minimum age for students
    MAX_STUDENT_AGE = 25        # Maximum age for students
    DEFAULT_ACTIVITY_DURATION = 2  # Default activity duration in hours
    
    # Database Configuration (can be overridden in db_connection.py)
    DB_CHARSET = 'utf8mb4'
    DB_COLLATION = 'utf8mb4_unicode_ci'
    
    # File and Path Configuration
    DEFAULT_LOG_LEVEL = 'INFO'
    MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Validation Rules
    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 50
    PASSWORD_MIN_LENGTH = 6
    ACTIVITY_NAME_MAX_LENGTH = 200
    EXPENSE_DESCRIPTION_MAX_LENGTH = 500
    FEEDBACK_COMMENT_MAX_LENGTH = 1000

# Utility functions available at package level
def get_version():
    """
    Get the current package version.
    
    Returns:
        str: The version string (e.g., "1.0.0")
    """
    return __version__

def get_package_info():
    """
    Get comprehensive package information.
    
    Returns:
        dict: Dictionary containing package metadata
    """
    return {
        'name': 'PythonExpenseApp',
        'version': __version__,
        'author': __author__,
        'email': __email__,
        'description': __description__,
        'license': __license__,
        'modules': __all__,
    }

# Package initialization logging
def _setup_package_logging():
    """
    Set up basic logging for the package.
    
    This function configures logging at the package level to help
    with debugging and monitoring application behavior.
    """
    import logging
    import os
    
    # Create logger for the package
    logger = logging.getLogger(__name__)
    
    # Set default logging level
    logger.setLevel(getattr(logging, Config.DEFAULT_LOG_LEVEL))
    
    # Create console handler if none exists
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger

# Initialize package logging
_package_logger = _setup_package_logging()

# Log package initialization
_package_logger.info(f"Initializing {Config.APP_TITLE}")
_package_logger.info(f"Available modules: {', '.join(__all__)}")

# Package-level exception classes
class TripManagerError(Exception):
    """
    Base exception class for Trip Manager application.
    
    All custom exceptions in the application should inherit from this class
    to provide consistent error handling across the package.
    """
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

class DatabaseError(TripManagerError):
    """Exception raised for database-related errors."""
    pass

class ValidationError(TripManagerError):
    """Exception raised for data validation errors."""
    pass

class AuthenticationError(TripManagerError):
    """Exception raised for authentication failures."""
    pass

class BusinessLogicError(TripManagerError):
    """Exception raised for business logic violations."""
    pass

# Add exception classes to __all__ so they can be imported
__all__.extend([
    'TripManagerError',
    'DatabaseError', 
    'ValidationError',
    'AuthenticationError',
    'BusinessLogicError',
    'Config',
    'get_version',
    'get_package_info'
])

# Package initialization complete
_package_logger.info("Package initialization complete")

# Development and debugging utilities
def _debug_package_status():
    """
    Print package status information for debugging.
    
    This function is useful during development to verify that
    all modules are loading correctly.
    """
    print(f"=== {Config.APP_TITLE} Package Status ===")
    print(f"Version: {__version__}")
    print(f"Available modules: {len(__all__)}")
    for module_name in __all__:
        try:
            # Try to access each exported item
            item = globals().get(module_name)
            if item:
                print(f"  ✓ {module_name}: {type(item).__name__}")
            else:
                print(f"  ✗ {module_name}: Not found")
        except Exception as e:
            print(f"  ✗ {module_name}: Error - {e}")
    print("=" * 40)

# Only run debug output if explicitly requested
if __name__ == "__main__":
    _debug_package_status()
