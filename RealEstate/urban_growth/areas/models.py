from decimal import Decimal, ROUND_HALF_UP

from django.db import models


class Area(models.Model):
    CATEGORY_HIGH = "high"
    CATEGORY_MEDIUM = "medium"
    CATEGORY_LOW = "low"

    CATEGORY_CHOICES = [
        (CATEGORY_HIGH, "High Growth"),
        (CATEGORY_MEDIUM, "Medium Growth"),
        (CATEGORY_LOW, "Low Growth"),
    ]

    area_name = models.CharField(max_length=120, unique=True)
    current_price_per_sq_ft = models.DecimalField(max_digits=12, decimal_places=2)
    rental_price = models.DecimalField(max_digits=12, decimal_places=2)
    number_of_listings = models.PositiveIntegerField()
    upcoming_infrastructure = models.BooleanField(default=False)
    distance_from_metro = models.DecimalField(max_digits=6, decimal_places=2)
    growth_score = models.DecimalField(max_digits=5, decimal_places=2, editable=False, default=0)
    growth_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, editable=False, default=CATEGORY_LOW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-growth_score", "area_name"]

    def __str__(self):
        return self.area_name

    @staticmethod
    def _clamp(value):
        return max(Decimal("0"), min(Decimal("1"), value))

    def calculate_growth_score(self):
        infrastructure_component = Decimal("1") if self.upcoming_infrastructure else Decimal("0")

        current_price = Decimal(str(self.current_price_per_sq_ft))
        rental_price = Decimal(str(self.rental_price))
        distance_from_metro = Decimal(str(self.distance_from_metro))

        price_affordability = Decimal("1") - (current_price / Decimal("10000"))
        metro_proximity = Decimal("1") - (distance_from_metro / Decimal("25"))
        price_growth_component = self._clamp((price_affordability * Decimal("0.7")) + (metro_proximity * Decimal("0.3")))

        listings_component = self._clamp(Decimal(self.number_of_listings) / Decimal("100"))

        if current_price:
            rental_yield_component = self._clamp((rental_price / current_price) * Decimal("10"))
        else:
            rental_yield_component = Decimal("0")

        score = (
            (Decimal("0.4") * infrastructure_component)
            + (Decimal("0.3") * price_growth_component)
            + (Decimal("0.2") * listings_component)
            + (Decimal("0.1") * rental_yield_component)
        )
        return score.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def calculate_growth_category(self):
        score = self.growth_score
        if score >= Decimal("0.70"):
            return self.CATEGORY_HIGH
        if score >= Decimal("0.40"):
            return self.CATEGORY_MEDIUM
        return self.CATEGORY_LOW

    def save(self, *args, **kwargs):
        self.growth_score = self.calculate_growth_score()
        self.growth_category = self.calculate_growth_category()
        super().save(*args, **kwargs)