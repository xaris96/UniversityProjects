// Project #3 - Neo4j / Graph Databases
// people.csv, friendships.csv, hobbies.csv, likes.csv in Neo4j's import folder

// 1. Clean database and create constraints

MATCH (n) DETACH DELETE n;

CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person)
REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT hobby_id_unique IF NOT EXISTS
FOR (h:Hobby)
REQUIRE h.id IS UNIQUE;

// 2. Load nodes

LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row
MERGE (p:Person {id: toInteger(row.id)})
SET p.name = row.name,
    p.age = toInteger(row.age),
    p.city = row.city,
    p.gender = CASE
                 WHEN row.gender IS NULL OR row.gender = '' THEN null
                 ELSE row.gender
               END;

LOAD CSV WITH HEADERS FROM 'file:///hobbies.csv' AS row
MERGE (h:Hobby {id: toInteger(row.hobby_id)})
SET h.name = row.name;

// 3. Load relationships

LOAD CSV WITH HEADERS FROM 'file:///friendships.csv' AS row
MATCH (p1:Person {id: toInteger(row.person1_id)})
MATCH (p2:Person {id: toInteger(row.person2_id)})
MERGE (p1)-[r:FRIEND]->(p2)
SET r.since = toInteger(row.since);

LOAD CSV WITH HEADERS FROM 'file:///likes.csv' AS row
MATCH (p:Person {id: toInteger(row.person_id)})
MATCH (h:Hobby {id: toInteger(row.hobby_id)})
MERGE (p)-[:LIKES]->(h);

// 4. Required queries

// a. List all people

MATCH (p:Person)
RETURN p.id AS id, p.name AS name, p.age AS age, p.city AS city, p.gender AS gender
ORDER BY p.id;

// b. Find all friends of Person A

MATCH (:Person {name: 'Person A'})-[:FRIEND]-(friend:Person)
RETURN friend.name AS friend
ORDER BY friend.name;

// c. Find all people living in Paris

MATCH (p:Person {city: 'Paris'})
RETURN p.name AS name, p.age AS age, p.gender AS gender
ORDER BY p.name;

// d. Find all friendship pairs (name1, name2) with the year they became friends

MATCH (p1:Person)-[r:FRIEND]->(p2:Person)
RETURN p1.name AS name1, p2.name AS name2, r.since AS since
ORDER BY since;

// e. Count number of friends each person has

MATCH (p:Person)
OPTIONAL MATCH (p)-[:FRIEND]-(friend:Person)
RETURN p.name AS name, count(friend) AS number_of_friends
ORDER BY number_of_friends DESC, name;

// f. Find all people who like Cooking

MATCH (p:Person)-[:LIKES]->(:Hobby {name: 'Cooking'})
RETURN p.name AS name
ORDER BY name;

// g. Find friends who share at least one hobby

MATCH (p1:Person)-[:FRIEND]-(p2:Person)
MATCH (p1)-[:LIKES]->(h:Hobby)<-[:LIKES]-(p2)
WHERE p1.id < p2.id
RETURN p1.name AS name1, p2.name AS name2, h.name AS shared_hobby
ORDER BY name1, name2, shared_hobby;

// h. Count hobbies by city

MATCH (p:Person)-[:LIKES]->(h:Hobby)
RETURN p.city AS city, h.name AS hobby, count(p) AS people_count
ORDER BY city, people_count DESC, hobby;

// Alternative for h: count distinct hobbies per city

MATCH (p:Person)-[:LIKES]->(h:Hobby)
RETURN p.city AS city, count(DISTINCT h) AS distinct_hobbies
ORDER BY distinct_hobbies DESC, city;

// i. Most popular hobby

MATCH (p:Person)-[:LIKES]->(h:Hobby)
RETURN h.name AS hobby, count(p) AS people_count
ORDER BY people_count DESC, hobby
LIMIT 1;

// Alternative for i: show complete ranking of hobbies

MATCH (p:Person)-[:LIKES]->(h:Hobby)
RETURN h.name AS hobby, count(p) AS people_count
ORDER BY people_count DESC, hobby;
