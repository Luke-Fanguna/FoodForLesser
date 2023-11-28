# Concurrency
## 1. Case 1 - Read Skew in create a new user - /users/add (POST)
In our create user endpoint, we need to check if the username and email exist before we can add the information for a new user. This can create a read skew concurrency issue if the information is updated between our read to check if user information exists and our insert when we post new user information.

 	SELECT * FROM users WHERE username LIKE :username OR email LIKE :email ->

 	INSERT INTO users (username, email) VALUES (:username,:email) RETURNING id ->



