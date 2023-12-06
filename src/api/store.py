from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from collections import defaultdict

router = APIRouter(
prefix="/stores",
tags=["stores"],
dependencies=[Depends(auth.get_api_key)],
)

# gets the list_id and then checks which stores have the best price
# list_id 
# get item_id with list_id from grocery_list_items
# with item_id, find the smallest for each value and unique values are found with list_id
# list_id == user_id
@router.post("/{list_id}/distribute")
def distribute_list(list_id: int):
    """ """
    with db.engine.begin() as connection:
        # gets every item from list_id
        list_exists = connection.execute(
            sqlalchemy.text("""
                                SELECT id
                                FROM grocery_list
                                WHERE grocery_list.id = :list_id
                                """),
                [{"list_id": list_id}]).fetchone()
        
        if not list_exists:
            return {"error" : "List does not exist"}

        items = connection.execute(sqlalchemy.text(
        """
        SELECT item_id
        FROM grocery_list_items
        WHERE list_id = :list_id
        """
        ),[{"list_id":list_id}]).fetchall()
        print("items",items)
        if not items:
            return {"result" : "no items in list"}
        items = [x[0] for x in items]
        print('arr',items)
        best = []
        distribute = []
        basket = set()
        # searches crowdsources entries for best price
        for item in items:
            print('loop',item)
            best = connection.execute(sqlalchemy.text(
            """
            SELECT 
                store_id,
                item_id,
                price
            FROM crowdsourced_entries
            WHERE item_id = :item_id
            ORDER BY store_id asc;
            """
            ),[{"item_id":item}]).fetchall()
            print(best)
            if len(best) == 0:
                continue
            best = min(best, key=lambda x: x[2])
            
            # joins best prices items with their stores
            if item not in basket:
                basket.add(item)
            else:
                continue
            distribute.append(
                {
                    "Store":
                    connection.execute(sqlalchemy.text(
                    """
                    SELECT
                        store_name
                    FROM stores
                    WHERE id = :store_id
                    """
                    ),[{"store_id":best[0]}]).fetchone()[0],
                    "Item":
                    connection.execute(sqlalchemy.text(
                    """
                    SELECT
                        item_name
                    FROM items
                    WHERE id = :item_id
                    """
                    ),[{"item_id":best[1]}]).fetchone()[0],
                    "Price":best[2]
                }
            )
        print(distribute)
        return distribute
        


@router.post("/{list_id}/best")
def find_best_item(list_id: int):
    """ """
    with db.engine.begin() as connection:
        #should grab all items in the users list and their quantities
        list_exists = connection.execute(
            sqlalchemy.text("""
                                SELECT id
                                FROM grocery_list
                                WHERE grocery_list.id = :list_id
                                """),
                [{"list_id": list_id}]).fetchone()
        
        if not list_exists:
            return {"error" : "List does not exist"}

        items = connection.execute(
            sqlalchemy.text("""
                            SELECT item_id, quantity
                            FROM grocery_list_items
                            WHERE list_id = :list_id 
                            """), 
            [{"list_id": list_id}]
        ).fetchall()
        
        stores = connection.execute(
            sqlalchemy.text("""
                            SELECT id
                            FROM stores
                            """)).fetchall()
        
        
        #initialize list of total prices corresponding to store id
        # prices = [0] * len(stores)
        prices = defaultdict(float)
        
        for item in items:
            for store in stores:
                #get the price of the most recent posting of the item
                itemPriceRes = connection.execute(
                    sqlalchemy.text("""
                                    SELECT COALESCE(price, :default_price) AS price
                                    FROM crowdsourced_entries
                                    WHERE created_at = (
                                        SELECT MAX(created_at) 
                                        FROM crowdsourced_entries
                                        WHERE item_id = :item_id and store_id = :store_id
                                        )
                                    """), 
                    [{"item_id": item[0], "store_id": store[0], "default_price": -1}]).scalar()
                if itemPriceRes and itemPriceRes > -1:
                    itemPrice = float(itemPriceRes)
                else:
                    #if item not in crowdsource for that store, just basically disqualify that list from being min
                    itemPrice = 999999
                #add the price of the item * quantity to the corresponding store
                #subtract 1 because first store id starts at 1 and not 0
                quantity = item[1]
                prices[store[0]] += itemPrice * quantity
        if prices:
            best_store = min(prices, key = prices.get)
        else:
            return {"result": "No stores have every item in your list."}

        #print(prices)
        #will indicate that each store is missing at least one item from the grocery list
        if best_store >= 999999:
            return {"result": "No stores have every item in your list."}
        
        store = connection.execute(
            sqlalchemy.text("""
                            SELECT store_name
                            FROM stores
                            WHERE id = :store_id
                            """), 
                    [{"store_id": best_store}]).scalar_one()

        return {"store_id": best_store, "store_name": store}

@router.post("/find")
def find_stores():
    """ """
    with db.engine.begin() as connection:
        all_stores = connection.execute(
            sqlalchemy.text("""
                            SELECT id, store_name 
                            FROM stores
                            ORDER BY id ASC
                            """)).fetchall()
    
    stores = {key: value for key, value in all_stores}
    return stores