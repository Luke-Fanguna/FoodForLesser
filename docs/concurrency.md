# Concurrency
## 1. Case 1 - Lost Update in create a new user - /users/add (POST)
In our create user endpoint, we need to check if the username and email exist before we can add the information for a new user. This can create a read skew concurrency issue if the information is updated between our read to check if user information exists and our insert when we post new user information.

 	SELECT * FROM users WHERE username = 'josh123' OR email = 'josh897@gmail.com' -> 
  
 	        <- UPDATE users SET email = 'josh897@gmail.com' WHERE user_id = 2

          <- UPDATE users SET username = 'josh123' WHERE user_id = 2
          
 	INSERT INTO users (username, email) VALUES ('josh123', 'josh897@gmail.com') RETURNING id ->
	
In this instance, when we try to insert new user information there is an existing user with the same data already. This would cause our insert query to roll back due to the values not matching the unique constraints on username and email columns. This can be fixed by checking if the username and email already exist within our insert query. 

 	WITH check_existing AS (
                SELECT id
                FROM users
                WHERE username = :username OR email = :email
            )
    	INSERT INTO users (username, email)
    	SELECT :username, :email
    	WHERE NOT EXISTS (SELECT 1 FROM check_existing)
    	RETURNING id;

This query checks if the username and email exist before inserting. This will guarantee that each time a valid email or username is inputted at the moment of transaction, we will insert it correctly.

## 2. Case 2 - Phantom Read in create a new grocery list - /lists/create (POST)
In our create list endpoint, we need to check if the user exists, as well as if there is already a grocery list under the same name, that way each user has uniquely named grocery lists. This can create a phantom read however, if multiple occurences of this endpoint are executed. For example if one transaction is reading if the list name already exists in which the query returns no, and another instance of this endpoint inserts a new grocery list with the name that the first transaction had checked for right after, then the rows retrieved by the first transaction would differ if it read from the DB again. 

 	SELECT list_name FROM grocery_list WHERE user_id = :user_id and list_name = :list_name -> 
  
 	        <- INSERT INTO grocery_list (list_name, user_id) VALUES (:list_name, (:user_id)) RETURNING id
	  
	SELECT list_name FROM grocery_list WHERE user_id = :user_id and list_name = :list_name -> 
 
 	INSERT INTO grocery_list (list_name, user_id) VALUES (:list_name, (:user_id)) RETURNING id ->
	
In this instance, the exact same select query would retrieve different rows due to the other transaction inserting a grocery list, resulting in a phantom read. This can be avoided by making the transaction serializable, so that that transactions run one at a time. 
