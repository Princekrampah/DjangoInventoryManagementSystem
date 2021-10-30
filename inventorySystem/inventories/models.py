from django.db import models



class Inventory(models.Model):
    # null is purely database related whereas blank is validation related
    name = models.CharField(max_length=100, null=False, blank=False)
    # decimal_places is he allowed number of decimal values, where as the max_digits 
    # is the total number of digits that will be in the whole number. The example below 
    # will be allowed to store a billoin numbers with 2 decimal places
    cost_per_item = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    quantity_in_stock = models.IntegerField(null=False, blank=False)
    # for IntegerFields we do not specify the max_length since its ignored
    quantity_sold = models.IntegerField(null=False, blank=False)
    sales = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    stock_date = models.DateField(auto_now_add=True)
    last_sales_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
