
# Example workflow
LilNHo is a helpful citizen, LilNHo finds eggs for half off deal at Costco and wants to share his find with others! He opens up Food4Lesser and creates a new grocery price posting for everyone to see. In his excitement, he accidentally makes a typo. He quickly updates the price of his post and goes on with shopping. Later when he is leaving, he realizes many people saw his post and came to Costco to buy eggs. With the eggs sold out, he deletes his posting so no one else comes to Costco disappointed.
Starts by calling POST /crowdsourcing/{store_id}/{grocery_id}/upload/{grocery_price} to share the deal he found. Then he calls PUT /crowdsourcing/{posting_id}/update/{grocery_price} when he realizes he made a typo and wants to update the price of his posting. Last, he calls DELETE /crowdsourcing/{posting_id}/delete when he finds there are no more eggs.

# Testing results
1. curl -X 'POST' \
  'https://food-for-lesser.onrender.com/crowdsourcing/1/upload/1/1/4.99?inventory_levels=medium' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
- Response: 1 
 
2. curl -X 'PUT' \
  'https://food-for-lesser.onrender.com/crowdsourcing/1/update/3.99' \
  -H 'accept: application/json' \
  -H 'access_token: food'
- Response: "OK"

4. curl -X 'DELETE' \
  'https://food-for-lesser.onrender.com/crowdsourcing/1/delete' \
  -H 'accept: application/json' \
  -H 'access_token: food'
- Response: "OK"
