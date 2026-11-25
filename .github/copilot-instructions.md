# Copilot Instructions

## Project Guidelines
- For the finance dashboard, show MMK currency amounts without decimal places and style new pages consistently with existing site pages.

## Testing and Environment Setup
- When running Django checks or tests from the terminal, use cmd rather than PowerShell; activate the virtual environment with `env\Scripts\activate.bat` first, as dependencies such as django-import-export are installed there, so system Python can misleadingly report them missing.