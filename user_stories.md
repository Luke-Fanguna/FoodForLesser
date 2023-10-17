**User Stories:**
- As a grocery shopper, I want to estimate the total cost of my shopping list so that I can stay within my budget.
- As a poor college student, I want the cheapest groceries so that I can eat enough and stay healthy.
- As a vegan, I want access to FoodForLesser so that I can search niche items and know which stores have stock of it.
- As a helpful citizen, I want to help connect people with affordable groceries so I will contribute to crowdsourcing.
- As a roommate, I want an effective way to organize my house’s groceries, so each roommate can budget effectively.
- As a parent, I want a way to find where the cheapest groceries are quickly, so I can prioritize parental responsibilities.
- As a small business owner, I want a way to promote my competitive prices, so my business can do better.
- As someone with a 9 to 5 job, I want to check the stores that have the item I want in stock so that I won’t waste my time.
- As a grocery store employee, I want customers to find the items they need easily, so I will contribute to crowdsourcing.
- As a consumer, I want to be able to choose the closest stores to me so I can plan my trip better.
- As a consumer, I want to be able to constantly view the prices of items so I can know the best places ahead of time.
- As a chef, I want to be able to choose the best ingredients at the stores near me.

**Exceptions:**
- Item could not be found: If the user searches for an item that is not in the database, they should be notified that the item is not available.
- Item is sold out: If the user searches for an item that is completely sold out, they will be notified that the stock of the item is none.
- Grocery Store is closed: If the user searches for items, the list of grocery stores returned will include information of each grocery store’s hours and if they are currently open or not.
- No grocery store exists within the radius selected: If the user sets their search radius too small, and no grocery store exists within that radius, they will be notified to increase their search radius.
- Prices aren’t constantly updated: If one store has the best/cheapest prices, the other stores will not be as frequently updated. There will be a timestamp showing the last time it was updated.
- Stock will affect updating: If a store is out of stock, there is a smaller chance that consumers will go to that store and update it if it is in stock. There is also the possibility that no one will go there to check. They will be able to see the timestamp of it’s last update.
- Item is not in store: If a user searches for an item that is only purchasable online and not in stores, the user will be notified that the item is only available through online order. They will be able to see if an item is online only.
- All items are same price: The system will be put with the task of choosing which store out of all of them. This will prompt the user with the decision of which store they would like to go to.
- User alters information: Possibility of a user affecting the availability with false information. The user would be prompted to take a photo of the item.
- User forgets to update stock/price: If they forget or do not update the stock/price, the user can be prompted with a window forcing them to update. The user will be given an update list when at the store in order to make sure that they update the prices.
- User misinputs data: If a user mistakenly sets an item to out of stock, a prompt will ask them to confirm that the item is sold out with a photo.
- Validation of data: Since it is crowd sourced, we will not know whether these prices are true or not. There will be the ability to confirm a price/stock value by other consumers.