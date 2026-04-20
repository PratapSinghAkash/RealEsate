import json

from django.shortcuts import render

from .models import Area


def dashboard(request):
    query = request.GET.get("q", "").strip()
    areas = Area.objects.all()

    if query:
        areas = areas.filter(area_name__icontains=query)

    areas = list(areas)
    total_count = len(areas)
    high_count = sum(1 for area in areas if area.growth_category == Area.CATEGORY_HIGH)
    medium_count = sum(1 for area in areas if area.growth_category == Area.CATEGORY_MEDIUM)
    low_count = sum(1 for area in areas if area.growth_category == Area.CATEGORY_LOW)

    chart_data = {
        "labels": [area.area_name for area in areas],
        "scores": [float(area.growth_score) for area in areas],
    }

    return render(
        request,
        "areas/dashboard.html",
        {
            "areas": areas,
            "query": query,
            "total_count": total_count,
            "high_count": high_count,
            "medium_count": medium_count,
            "low_count": low_count,
            "chart_data": json.dumps(chart_data),
        },
    )