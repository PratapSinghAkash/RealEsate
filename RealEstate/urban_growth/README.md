# Predictive Urban Growth Modeling

A simple Django + SQLite web app for ranking real estate areas by a heuristic growth score.

## Features
- Django admin for manual area entry
- Growth score calculation and category labels
- Dashboard table with color-coded status
- Search filter by area name
- Chart.js bar chart visualization

## Run
```powershell
Set-Location "c:\Users\Akash\OneDrive\Desktop\RealEstate\urban_growth"
& "C:/Program Files/Python313/python.exe" manage.py runserver 127.0.0.1:8000 --noreload
```

Open `http://127.0.0.1:8000/`

## Admin
- Username: `admin`
- Password: `Admin1234!`

Use `/admin/` to add or edit area data.
