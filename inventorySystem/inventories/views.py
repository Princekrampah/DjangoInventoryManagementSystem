from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Inventory
#Update form import
from .forms import InventoryUpdateForm, AddInventoryForm
# flash messages
from django.contrib import messages
# dataframe
from django_pandas.io import read_frame
# plotly
import plotly
import plotly.express as px
# json
import json


@login_required()
def inventoryList(request):
    inventories = Inventory.objects.all()
    context = {
        "inventories": inventories
    }
    return render(request, "inventories/inventory_list.html", context=context)


@login_required()
def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }
    return render(request, "inventories/per_product.html", context=context)


@login_required()
def update(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        updateForm = InventoryUpdateForm(data=request.POST)
        if updateForm.is_valid():
            inventory.name = updateForm.data['name']
            inventory.quantity_in_stock = updateForm.data['quantity_in_stock']
            inventory.quantity_sold = updateForm.data['quantity_sold']
            inventory.cost_per_item = updateForm.data['cost_per_item']
            inventory.sales = float(inventory.cost_per_item) * float(inventory.quantity_sold)
            inventory.save()
            messages.success(request, "Update Successful")
            return redirect(f"/inventory/per_product_view/{pk}/")
    else:
        updateForm = InventoryUpdateForm(instance=inventory)

    return render(request, "inventories/inventory_update.html", {'form' : updateForm})


@login_required()
def delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.success(request, "Inventory Deleted")
    return redirect("/inventory/")

    
    # messages.debug()
    # messages.info()
    # messages.success()
    # messages.warning()
    # messages.error()


@login_required()
def add_product(request):
    if request.method == "POST":
        updateForm = AddInventoryForm(data=request.POST)
        if updateForm.is_valid():
            new_invetory = updateForm.save(commit=False)
            new_invetory.sales = float(updateForm.data['cost_per_item']) * float(updateForm.data['quantity_sold'])
            new_invetory.save()
            messages.success(request, "Successfully Added Product")
            return redirect(f"/inventory/")
    else:
        updateForm = AddInventoryForm()

    return render(request, "inventories/inventory_add.html", {'form' : updateForm})


@login_required()
def dashboard(request):
    inventories = Inventory.objects.all()
    df = read_frame(inventories)
    
    # sales graph
    print(df.columns)
    sales_graph_df = df.groupby(by="last_sales_date", as_index=False, sort=False)['sales'].sum()
    print(sales_graph_df.sales)
    print(sales_graph_df.columns)
    sales_graph = px.line(sales_graph_df, x = sales_graph_df.last_sales_date, y = sales_graph_df.sales, title="Sales Trend")
    sales_graph = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)

    
    # best performing product
    best_performing_product_df = df.groupby(by="name").sum().sort_values(by="quantity_sold")
    best_performing_product = px.bar(best_performing_product_df, 
                                    x = best_performing_product_df.index, 
                                    y = best_performing_product_df.quantity_sold, 
                                    title="Best Performing Product"
                                )
    best_performing_product = json.dumps(best_performing_product, cls=plotly.utils.PlotlyJSONEncoder)


    # best performing product in sales
    sales_graph_df_per_product_df = df.groupby(by="name", as_index=False, sort=False)['sales'].sum()
    best_performing_product_per_product = px.pie(sales_graph_df_per_product_df, 
                                    names = "name", 
                                    values = "sales", 
                                    title="Product Performance By Sales",
                                    # https://plotly.com/python/discrete-color/
                                    color_discrete_sequence=px.colors.qualitative.Bold,
                                )
    best_performing_product_per_product = json.dumps(best_performing_product_per_product, cls=plotly.utils.PlotlyJSONEncoder)


     # Most Product In Stock
    most_product_in_stock_df = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    most_product_in_stock = px.pie(most_product_in_stock_df, 
                                    names = most_product_in_stock_df.index, 
                                    values = most_product_in_stock_df.quantity_in_stock, 
                                    title="Most Product In Stock"
                                )
    most_product_in_stock = json.dumps(most_product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "sales_graph": sales_graph,
        "best_performing_product": best_performing_product,
        "most_product_in_stock": most_product_in_stock,
        "best_performing_product_per_product": best_performing_product_per_product
    }

    return render(request,"inventories/dashboard.html", context=context)