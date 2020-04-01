from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages 
from .form import StockForm

def home(request):
    import json
    import requests

    if request.method == "POST":
        ticker = request.POST['ticker']
        # api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote/?token=pk_3a8decf20ef440b8a8772c24a9420456")
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote/?token=pk_3a8decf20ef440b8a8772c24a9420456")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "ERROR..."
        return render(request,"home.html",{"api":api})

    else:
        return render(request,"home.html",{"ticker":"Enter a ticker symbol above"})


def about(request):
    return render(request,"about.html",{})

def addstock(request):
    import json
    import requests

    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,("Stock has been Added Successfully"))
            return redirect("addstock")
        else:
            messages.error(request,("Please Search for Your Stock!"))
            return redirect("addstock")
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote/?token=pk_3a8decf20ef440b8a8772c24a9420456")
            try:
                api = json.loads(api_request.content)
                output.append(api)

            except Exception as e:
                api = "ERROR..."
        return render(request,"addstock.html",{"ticker":ticker,"output":output})



def delete(request,stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.warning(request,("Stock has been Deleted!"))
    return redirect("addstock")