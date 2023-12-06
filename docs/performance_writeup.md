users.py
create_user: 136.578 ms

list.py
- create_list: 2.035 ms
- get_list: 0.515 ms
- get_items: 0.288 ms
- set_item_quantity: 9.680 ms
- update_list: 2.438 ms
- delete_item: 0.434 ms
store.py
- distribute_list: 337.960 ms
- find_best_item: 372.472 ms
- find_stores: 0.898 ms
crowdsourcing.py
- upload_entry: 2.789 ms
- update_entry: 6.614 ms
- remove_entry: 0.430 ms

3 slowest endpoints
- Distribute: 337.960 ms
- Best: 372.472 ms
- Create user: 136.578 ms

Fake Data Modeling
	[FoodForLesser/src/api/populate_rows.py]
	Our user table has about 1,000,000 rows, stores table has 5 rows, items table has 50 rows, grocery_list has 4 rows, grocery_list_items has 2 rows, crowdsourced_entries has 3,976,358 rows. We believe that our service would scale this way because the users can grow greatly and the crowdsourced_entries will scale as well because each user can make many entries. By this we mean that the users will make many crowdsourced_entries over and over again. 


Performance Tuning

| QUERY PLAN                                                                             |
| -------------------------------------------------------------------------------------- |
| Insert on users  (cost=2216.37..2216.39 rows=1 width=72)                               |
|   InitPlan 1 (returns $0)                                                              |
|     ->  Seq Scan on users users_1  (cost=0.00..24380.10 rows=11 width=0)               |
|           Filter: ((username = 'username'::text) OR (email = 'email@gmail.com'::text)) |
|   ->  Result  (cost=0.00..0.01 rows=1 width=72)                                        |
|         One-Time Filter: (NOT $0)                                                      |

This composite index will be added so it will help with filtering. If the user does not already exist, then it will have to check the entire table if they do which can be a long process. We would like to avoid that with the index.

CREATE INDEX idx_check_existing ON users (username, email);

| QUERY PLAN                                                                               |
| ---------------------------------------------------------------------------------------- |
| Insert on users  (cost=2216.37..2216.39 rows=1 width=72)                                 |
|   InitPlan 1 (returns $0)                                                                |
|     ->  Seq Scan on users users_1  (cost=0.00..24380.10 rows=11 width=0)                 |
|           Filter: ((username = 'xusername'::text) OR (email = 'xemail@gmail.com'::text)) |
|   ->  Result  (cost=0.00..0.01 rows=1 width=72)                                          |
|         One-Time Filter: (NOT $0)                                                        |

We couldn’t find a noticeable change because it checks if the user exists and if the user exists, then the query would be pretty fast.

| QUERY PLAN                                                                                               |
| -------------------------------------------------------------------------------------------------------- |
| Seq Scan on crowdsourced_entries  (cost=0.00..16773.11 rows=400287 width=22)
  Filter: (item_id = 2) |
|   Index Cond: (item_id = 2)                                                                              |

We will be adding the following single-column index and composite index. We want the single-column index since we only want to see where a certain item is. We want the composite index to optimize filtering and ordering since that is what our query is doing.

CREATE INDEX idx_item_id ON crowdsourced_entries (item_id);
CREATE INDEX idx_item_store ON crowdsourced_entries (item_id, store_id);

| QUERY PLAN                                                                                               |
| -------------------------------------------------------------------------------------------------------- |
| Index Only Scan using idx_main_query on crowdsourced_entries  (cost=0.43..16448.26 rows=400287 width=22) |
|   Index Cond: (item_id = 2)                                                                              |

The cost lowered a little bit but it would mean that overtime we would not have to deal with a building cost.


| QUERY PLAN                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------ |
| Gather  (cost=67929.87..129634.17 rows=1 width=32)                                                                                   |
|   Workers Planned: 2                                                                                                                 |
|   Params Evaluated: $1                                                                                                               |
|   InitPlan 1 (returns $1)                                                                                                            |
|     ->  Finalize Aggregate  (cost=66929.86..66929.87 rows=1 width=8)                                                                 |
|           ->  Gather  (cost=66929.64..66929.85 rows=2 width=8)                                                                       |
|                 Workers Planned: 2                                                                                                   |
|                 ->  Partial Aggregate  (cost=65929.64..65929.65 rows=1 width=8)                                                      |
|                       ->  Parallel Seq Scan on crowdsourced_entries crowdsourced_entries_1  (cost=0.00..65846.24 rows=33362 width=8) |
|                             Filter: ((item_id = 10) AND (store_id = 3))                                                              |
|   ->  Parallel Seq Scan on crowdsourced_entries  (cost=0.00..61704.20 rows=1 width=32)                                               |
|         Filter: (created_at = $1)                                                                                                    |
| JIT:                                                                                                                                 |
|   Functions: 11                                                                                                                      |
|   Options: Inlining false, Optimization false, Expressions true, Deforming true                     |

What this explain means to us is that is is very expensive. 

We will add the following index in order to locate and aggregate through the table to avoid parallel sequential scans.
CREATE INDEX idx_item_store_created_at ON crowdsourced_entries (item_id, store_id, created_at);

| QUERY PLAN                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gather  (cost=1000.48..62704.78 rows=1 width=32)                                                                                                                       |
|   Workers Planned: 2                                                                                                                                                   |
|   Params Evaluated: $1                                                                                                                                                 |
|   InitPlan 2 (returns $1)                                                                                                                                              |
|     ->  Result  (cost=0.47..0.48 rows=1 width=8)                                                                                                                       |
|           InitPlan 1 (returns $0)                                                                                                                                      |
|             ->  Limit  (cost=0.43..0.47 rows=1 width=8)                                                                                                                |
|                   ->  Index Only Scan Backward using idx_item_store_created_at on crowdsourced_entries crowdsourced_entries_1  (cost=0.43..3401.93 rows=80069 width=8) |
|                         Index Cond: ((item_id = 10) AND (store_id = 3) AND (created_at IS NOT NULL))                                                                   |
|   ->  Parallel Seq Scan on crowdsourced_entries  (cost=0.00..61704.20 rows=1 width=32)                                                                                 |
|         Filter: (created_at = $1)                                                                                                                                      |

What this explain means to us is that the cost went down extremely and will be better in the long run. This definitely had the performance increase we expected because this would scan the table a lot and we wanted to avoid that.
