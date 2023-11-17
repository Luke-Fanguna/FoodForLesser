8 API specification: 
1. Grocery List - Customer
1.1 - Create a new grocery list - /lists/ (POST)
	*Creates a new grocery list*
	Input: None 
Output: Grocery List Id
1.2 - Add new grocery list item - /lists/{list_id}/items/{item_name} (PUT)
	*Adds a new grocery item to your grocery list*
	Input: Grocery item name
	Output: None
1.3 - Delete grocery list item - /lists/{list_id}/items/{item_name} (DELETE)
	*Deletes a grocery item from your grocery list*
	Input: Grocery item name
	Output: None

2. Items search
2.1 - Get Stores - /stores/ (GET)
	*Retrieves the list of stores with distances*
	Input: Location
	Output: Store locations within a 10 mile radius
2.2 - Get distributed grocery list - /stores/{list_id}/distribute (POST)
	*Decides which groceries should go to which stores*
	Input: list_id
	Output: List of items and groceries 
2.3 - Get best for basket - /stores/{list_id}/best (POST)
	*Retrieves the store that has the best price overall for the entire list of items in grocery list*
	Input: list_id
	Output: store_id

3. CrowdSourcing
3.1 - Upload new grocery price posting - /crowdsourcing/{store_id}/{item_name}/upload/{grocery_price} (POST)
	*Adds a new grocery price posting*
	Input: item_name, Grocery price, store_id
	Output: posting_id
3.2 - Update pre-existing posted price - /crowdsourcing/{posting_id}/update/{grocery_price} (PUT)
	*Changes grocery price posting* 
	Input: posting id, Grocery price
	Output: None
3.3 - Delete grocery price posting - /crowdsourcing/{posting_id}/delete (DELETE)
	*Removes grocery price posting*
	Input: posting_id
	Output: None

3 Example Flows:
1. LilNHo is a helpful citizen,  LilNHo finds eggs for half off deal at Costco and wants to share his find with others! He opens up Food4Lesser and creates a new grocery price posting for everyone to see. In his excitement, he accidentally makes a typo. He quickly updates the price of his post and goes on with shopping. Later when he is leaving, he realizes many people saw his post and came to Costco to buy eggs. With the eggs sold out, he deletes his posting so no one else comes to Costco disappointed.  
Starts by calling POST /crowdsourcing/{store_id}/{grocery_id}/upload/{grocery_price} to share the deal he found.
Then he calls PUT /crowdsourcing/{posting_id}/update/{grocery_price} when he realizes he made a typo and wants to update the price of his posting.
Last, he calls DELETE /crowdsourcing/{posting_id}/delete when he finds there are no more eggs.

2. Josh lives with 3 of his friends and is looking for a way to grocery shop efficiently for the household. He discovers FoodForLesser and is ecstatic! First, Josh creates his grocery list by calling POST /lists. He then adds a list of items into his grocery list.
To do so he:
calls POST /lists/1/items/chicken_breast to add chicken breast for the gains 
Calls POST /lists/1/items/milk to add milk to his list 
Calls POST /lists/1/items/cheese to add cheese to his list 
Calls POST /lists/1/items/tomato to add tomato to his list 
Finally, he calls POST /stores/1/distribute to get the cheapest store for each item in his list
Now with his distributed list of grocery items with their respective store(s), he and his roommates can effectively split up their grocery needs, in which each roommate can go to one grocery store and get the item that is cheapest there. 

3. Misaki is a single mother. She wants to find a store that is close by with cheap groceries so her and her child won’t starve. She desperately needs baby food and caffeine. She requests a list of stores near her location by calling GET /stores. This gives her a list of stores within ten miles of her. She then makes her own grocery list by calling POST /lists. She wants to add coffee, baby food, and top ramen to her list and find the grocery store where the total cost of her list would be the cheapest. 
To do so she:
Calls POST /lists/1/items/coffee to add coffee to her list
Calls POST /lists/1/items/baby_food to add baby food to her list
Calls POST /lists/1/items/top_ramen to add top ramen to her list
Finally, she calls POST /stores/1/best which will give her the store that would give her the cheapest list
