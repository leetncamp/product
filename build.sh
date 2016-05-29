rm -rf build
rm -rf dist
pyinstaller --name=ph --hidden-import django --hidden-import django-bootstrap --hidden-import openpyxl --hidden-import hierarchy.migrations -F manage.py
rm -rf build
cp dist/ph ph.app
rm -rf dist
