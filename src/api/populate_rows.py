import sqlalchemy
import os
import dotenv
import numpy as np
from faker import Faker
import random

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

# with engine.begin() as conn:
#     conn.execute(sqlalchemy.text("""
#     DROP TABLE IF EXISTS likes;
#     DROP TABLE IF EXISTS posts;
#     DROP TABLE IF EXISTS users;
#     DROP TABLE IF EXISTS category;

#     CREATE TABLE 
#         category (
#             id int generated always as identity not null PRIMARY KEY,
#             category_name text not null
#         );

#     CREATE TABLE
#     users (
#         id int generated always as identity not null PRIMARY KEY,
#         username text unique not null,
#         full_name text not null,
#         birthday date not null,
#         device_type text not null
#     );    
        
#     CREATE TABLE
#     posts (
#         id int generated always as identity not null PRIMARY KEY,
#         title text not null, 
#         content text not null,
#         created_at timestamp not null,
#         visible boolean not null,
#         poster_id int not null references users(id),
#         category_id int  not null references category(id),
#         likes int default 0,
#         nsfw boolean default false
#     );
#     """))
    
#     # populate initial posting categories
#     for category in categories:    
#         conn.execute(sqlalchemy.text("""
#         INSERT INTO category (category_name) VALUES (:category_name);
#         """), {"category_name": category})

num_users = 1000000
fake = Faker()
posts_sample_distribution = np.random.default_rng().negative_binomial(0.04, 0.01, num_users)
total_posts = 0

# create fake posters with fake names and birthdays
with engine.begin() as conn:
    print("creating fake posters...")
    posts = []
    for i in range(num_users):
        if (i % 10 == 0):
            print(i)
        
        profile = fake.profile()
        email = fake.unique.email(domain='gmail.com')


        user_id = conn.execute(sqlalchemy.text("""
        INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id;
        """), {"username": profile['name'], "email": email}).scalar_one();

        num_posts = posts_sample_distribution[i]
        likes_sample_distribution = np.random.default_rng().negative_binomial(0.8, 0.0001, num_posts)  
        for j in range(num_posts):
            total_posts += 1
            random_price = fake.random_int(min=1, max=9999)
            formatted_price = f'{random_price // 100}.{random_price % 100:02d}'

            posts.append({
                "created_at": fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None),
                "item_id": random.randint(1,10),
                "user_id": user_id,
                "price" : float(formatted_price),
                "inventory" : random.choice(['low', 'medium', 'high']),
                "store_id" : random.randint(1,5)
            }) 

    if posts:
        conn.execute(sqlalchemy.text("""
        INSERT INTO crowdsourced_entries (created_at,item_id,user_id,price,inventory,store_id) 
        VALUES (:created_at,:item_id,:user_id,:price,:inventory,:store_id);
        """), posts)

    print("total posts: ", total_posts)
    