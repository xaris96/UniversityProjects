# Project #3 – Graph Databases / Neo4j

## Files used

- `people.csv`
- `friendships.csv`
- `hobbies.csv`
- `likes.csv`
- `Proj3_Neo4j_solution.cypher`

## What the graph contains

The graph uses two node labels:

- `Person`
- `Hobby`

It uses two relationship types:

- `(:Person)-[:FRIEND {since: year}]->(:Person)`
- `(:Person)-[:LIKES]->(:Hobby)`

The `FRIEND` relationship is stored once, but the queries treat friendship as bidirectional using `-[:FRIEND]-`

## How to run

1. Open Neo4j Desktop
2. Create or open a DBMS/project
3. Start the database
4. Open the database import folder
5. Copy the following CSV files into the import folder:
   - `people.csv`
   - `friendships.csv`
   - `hobbies.csv`
   - `likes.csv`
6. Open Neo4j Browser
7. Copy and run the commands from `Proj3_Neo4j_solution.cypher`

## Required queries included

The Cypher file includes:

a. List all people  
b. Find all friends of Person A  
c. Find all people living in Paris  
d. Find all friendship pairs with the year they became friends  
e. Count number of friends each person has  
f. Find all people who like Cooking  
g. Find friends who share at least one hobby  
h. Count hobbies by city  
i. Most popular hobby  

## Expected results summary

### a. All people

Person A, Person B, Person C, Person D, Person E

### b. Friends of Person A

Person B, Person C

### c. People living in Paris

Person C, Person E

### d. Friendship pairs

| name1 | name2 | since |
|---|---|---:|
| Person B | Person D | 2017 |
| Person A | Person B | 2018 |
| Person A | Person C | 2019 |
| Person C | Person E | 2020 |

### e. Number of friends

| name | number_of_friends |
|---|---:|
| Person A | 2 |
| Person B | 2 |
| Person C | 2 |
| Person D | 1 |
| Person E | 1 |

### f. People who like Cooking

Person C, Person E

### g. Friends who share at least one hobby

| name1 | name2 | shared_hobby |
|---|---|---|
| Person A | Person C | Reading |
| Person C | Person E | Cooking |

### h. Count hobbies by city

| city | hobby | people_count |
|---|---|---:|
| London | Cycling | 1 |
| London | Reading | 1 |
| London | Traveling | 1 |
| New York | Traveling | 1 |
| Paris | Cooking | 2 |
| Paris | Reading | 1 |

### i. Most popular hobby

There is a tie with 2 people each:

- Cooking
- Reading
- Traveling

The `LIMIT 1` query returns one of them depending on the ordering used. The included query orders alphabetically after count, so it returns `Cooking`

## Additional Python script

Along with the Cypher solution, a Python script (`load_neo4j.py`) is also provided. The Cypher file contains all loading commands and all required queries, but when the whole script is executed at once in Neo4j Browser, the interface may not display all query results clearly under each query. For easier and faster verification, the Python script loads the same CSV files into Neo4j and prints the results of all required queries sequentially in the terminal

To run the Python version, install the Neo4j driver:

```bash
pip install neo4j
python load_neo4j.py --password YOUR_NEO4J_PASSWORD
```
