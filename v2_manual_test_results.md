# Example workflow
Josh lives with 3 of his friends and is looking for a way to grocery shop efficiently for the household. He discovers FoodForLesser and is ecstatic! First, Josh creates his grocery list by calling POST /lists. He then adds a list of items to his grocery list. To do so he: calls POST /lists/2/items/1/2/ to add item_id: 1, ketchup to his list. Calls POST /lists/1/items/2/3 to add hotdogs to his list. Calls POST /lists/1/items/3/1 to add bread to his list. He then wants to check his list so he calls GET /lists/{list_id}. Finally, he calls POST /stores/1/distribute to get the cheapest store for each item in his list Now with his distributed list of grocery items with their respective store(s), he and his roommates can effectively split up their grocery needs, in which each roommate can go to one grocery store and get the item that is cheapest there.

# Testing results
1. curl -X 'POST' \
  'http://127.0.0.1:8000/lists/?user_id=3' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response: { "list_id": 2 }
 
2. curl -X 'POST' \
  'http://127.0.0.1:8000/lists/2/items/1/2' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response: { "posting_id": 9 }

3. curl -X 'POST' \
  'http://127.0.0.1:8000/lists/2/items/2/3' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response: { "posting_id": 10 }

4. curl -X 'POST' \
  'http://127.0.0.1:8000/lists/2/items/3/1' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response: { "posting_id": 11 }

5. curl -X 'GET' \
  'http://127.0.0.1:8000/lists/2' \
  -H 'accept: application/json' \
  -H 'access_token: food'  
- Response: {
    "item_id": 1,
    "item": "Ketchup",
    "quantity": 2
  },
  {
    "item_id": 2,
    "item": "Hotdogs",
    "quantity": 3
  },
  {
    "item_id": 3,
    "item": "Bread",
    "quantity": 1
  }

6. curl -X 'POST' \
  'http://127.0.0.1:8000/lists/stores/2/distribute (POST)' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response : [
  {
    "Store": "Ralphs",
    "Item": "Ketchup",
    "Price": 3
  },
  {
    "Store": "Ralphs",
    "Item": "Hotdogs",
    "Price": 3
  },
  {
    "Store": "Costco",
    "Item": "Bread",
    "Price": 2
  }
]

7. curl -X 'DELETE' \
  'http://127.0.0.1:8000/crowdsourcing/1/delete' \
  -H 'accept: application/json' \
  -H 'access_token: food'
- Response: "OK"

# Example workflow
Misaki is a single mother. She wants to find a store that is close by with cheap groceries so her and her child won’t starve. She desperately needs baby food and caffeine. She requests a list of stores near her location by calling GET /stores. This gives her the list of stores. She then makes her own grocery list by calling POST /lists. She wants to add doritos and milk to her list and find the grocery store where the total cost of her list would be the cheapest. To do so she: Calls POST /lists/4/items/4/3 to add 3 bags of doritos to her list and calls POST /lists/4/items/8/1 to add 1 carton of milk to her list. Then, she confirms her list by callling GET /lists/4. Finally, she calls POST lists/stores/4/best which will give her the store that would give her the cheapest list

# Testing results
1. curl -X 'GET' \
  'http://127.0.0.1:8000/lists/stores/ (GET)' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response: [
  {
    "id": 1,
    "name": "Safeway"
  },
  {
    "id": 2,
    "name": "Ralphs"
  },
  {
    "id": 3,
    "name": "Costco"
  },
  {
    "id": 4,
    "name": "Smart & Final"
  },
  {
    "id": 5,
    "name": "Grocery Outlet"
  }
] 

2. curl -X 'POST' \
  'http://127.0.0.1:8000/lists/?user_id=4' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response: { "list_id" : 4}

3. curl -X 'POST' \
  'http://127.0.0.1:8000/lists/4/items/4/3' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response: { "posting_id" : 18}


5. curl -X 'POST' \
  'http://127.0.0.1:8000/lists/4/items/8/1' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response: { "posting_id" : 19}

6. curl -X 'GET' \
  'http://127.0.0.1:8000/lists/4' \
  -H 'accept: application/json' \
  -H 'access_token: food'
- Response: [
  {
    "item_id": 4,
    "item": "Doritos",
    "quantity": 3
  },
  {
    "item_id": 8,
    "item": "Milk",
    "quantity": 1
  }
] 

7. TO DO

