@echo off
:: This line prevents the display of each command before execution.

if exist "../.venv/Scripts/activate.bat" (
   call ../.venv/Scripts/activate.bat
) else (
   echo Error: .venv directory not found
   pause
   exit /b 1
)

echo Running isort...
python -m isort .
echo:

echo Running black...
python -m black .
echo:

echo Formatting completed successfully.
