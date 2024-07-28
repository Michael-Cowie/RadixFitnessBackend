@echo off
:: This line prevents the display of each command before execution.

echo Running isort...
python -m isort .
echo:

echo Running black...
python -m black .
echo:

echo Formatting completed successfully.
