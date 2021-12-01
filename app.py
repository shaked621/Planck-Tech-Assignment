from re import A
import requests
import datetime as dt
import json

from flask import Flask, request


def get_menu():
    headers = {
        'authority': 'tenbis-static.azureedge.net',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'origin': 'https://www.10bis.co.il',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'he,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
        'if-none-match': '0x8D9B4A0B76EBA79',
        'if-modified-since': 'Wed, 01 Dec 2021 08:01:01 GMT',
    }
    response = requests.get('https://tenbis-static.azureedge.net/restaurant-menu/19156_en', headers=headers)
    jsonres=json.loads(response.content)
    return jsonres

def get_catgory(menu, category_name):
    for category in menu["categoriesList"]:
        if category["categoryName"] == category_name:
            return category
    return "NO Category was found"

def get_item(category,id):
    for dish in category["dishList"]:
        if dish["dishId"] == id:
            return dish
    return "NO Item was found"

def check_item_catgory(items):
    menu=get_menu
    catgory=[]
    id_item=[]
    item_in_catgory=[]
    for key,value in items.items():
        catgory.append(key)
        id_item.append(value)
        items_in_catgory=get_catgory(menu,key)

def checkout(items):
    menu=get_menu()
    total=0
    for key,val in items.items():
        catgory=get_catgory(menu,key)
        for id in val:
            item=get_item(catgory,int(id))
            print(item["dishPrice"])
            total+=item["dishPrice"]
    return total
    

app = Flask(__name__)

@app.route('/')
def entry_point():
    return 'Hello World!'

#Drinks
@app.route('/drinks')
def get_drinks():
    menu=get_menu()
    return get_catgory(menu,"Drinks")

@app.route('/drink/<int:id>', methods=["GET"])
def get_drink(id: int):
    menu=get_menu()
    drinks = get_catgory(menu,"Drinks")
    return get_item(drinks,id)
#------------------------------------

#Pizzas
@app.route('/pizzas')
def get_pizzas():
    menu=get_menu()
    return get_catgory(menu,"Pizzas")


@app.route('/pizza/<int:id>')
def get_pizza(id: int):
    menu=get_menu()
    pizzas=get_catgory(menu,"Pizzas")
    return get_item(pizzas,id)
#------------------------------------


#Desserts
@app.route('/desserts')
def get_desserts():
    menu=get_menu()
    return get_catgory(menu,"Desserts")


@app.route('/dessert/<int:id>')
def get_dessert(id: int):
    menu=get_menu()
    pizzas=get_catgory(menu,"Desserts")
    return get_item(pizzas,id)
#------------------------------------



@app.route('/order', methods=["POST"])
def order():
    print(request.data)
    itemJSON=request.data.decode('utf8').replace("'", '"')
    items = json.loads(itemJSON)
    total_amount=checkout(items)
    if total_amount>0:
        return total_amount
    else:
        return "Error in the order"

    

if __name__ == '__main__':
    app.run(debug=True, port=5000)


