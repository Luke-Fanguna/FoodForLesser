
# Example workflow
As a helpful citizen, I want to help connect people with affordable groceries so I will contribute to crowdsourcing.

# Testing results
1. Curl statement:
   curl -X 'POST' \
  'http://127.0.0.1:8000/crowdsourcing/1/upload/1/1/5.99?inventory_levels=medium' \
  -H 'accept: application/json' \
  -H 'access_token: food' \
  -d ''
2. Reponse:
   1
