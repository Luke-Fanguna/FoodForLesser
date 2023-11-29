# Concurrency
## 1. Case 1 - Read Skew in create a new user - /users/add (POST)
In our create user endpoint, we need to check if the username and email exist before we can add the information for a new user. This can create a read skew concurrency issue if the information is updated between our read to check if user information exists and our insert when we post new user information.

 	SELECT * FROM users WHERE username = 'josh123' OR email = 'josh897@gmail.com' -> 
  
 	        <- UPDATE users SET email = 'josh897@gmail.com' WHERE user_id = 2

          <- UPDATE users SET username = 'josh123' WHERE user_id = 2
          
 	INSERT INTO users (username, email) VALUES ('josh123', 'josh897@gmail.com') RETURNING id ->
	
In this instance, when we try to insert new user information there is an existing user with the same data already. This would cause our insert query to roll back due to the values not matching the unique constraints on username and email columns. This can be fixed by checking if the username and email already exist within our insert query. 

 	INSERT INTO users (username, email) VALUES (:username, :email) ON CONFLICT (username, email) DO NOTHING

This query checks if the username and email exist before inserting. This will guarantee that each time a valid email or username is inputted at the moment of transaction, we will insert it correctly.
