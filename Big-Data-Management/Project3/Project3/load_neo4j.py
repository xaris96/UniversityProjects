"""
Project #3 - Neo4j / Graph Databases
Python loader for people.csv, friendships.csv, hobbies.csv, likes.csv

What it does:
1. Connects to a local Neo4j database
2. Clears the existing graph
3. Creates Person and Hobby nodes
4. Creates FRIEND and LIKES relationships
5. Runs and prints the required queries a-i

Required package:
    pip install neo4j

How to run:
    python load_neo4j.py --password YOUR_NEO4J_PASSWORD
"""

from __future__ import annotations

import argparse
import csv
import getpass
import os
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase


BASE_DIR = Path(__file__).resolve().parent


def clean_value(value: str | None) -> str | None:
    """Convert empty strings to None and trim normal text values"""
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    return value


def to_int(value: str | None) -> int | None:
    """Convert CSV values to integers when possible"""
    value = clean_value(value)

    if value is None:
        return None

    return int(value)


def read_csv_rows(filename: str) -> list[dict[str, Any]]:
    """Read a CSV file from the same folder as this Python file"""
    path = BASE_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {filename}. Put it in the same folder as load_neo4j.py"
        )

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return [{key: clean_value(value) for key, value in row.items()} for row in reader]


def load_graph(session) -> None:
    """Load all CSV data into Neo4j"""

    people = read_csv_rows("people.csv")
    hobbies = read_csv_rows("hobbies.csv")
    friendships = read_csv_rows("friendships.csv")
    likes = read_csv_rows("likes.csv")

    # Convert numeric fields
    people_rows = [
        {
            "id": to_int(row["id"]),
            "name": row["name"],
            "age": to_int(row["age"]),
            "city": row["city"],
            "gender": row.get("gender"),
        }
        for row in people
    ]

    hobby_rows = [
        {
            "id": to_int(row["hobby_id"]),
            "name": row["name"],
        }
        for row in hobbies
    ]

    friendship_rows = [
        {
            "person1_id": to_int(row["person1_id"]),
            "person2_id": to_int(row["person2_id"]),
            "since": to_int(row["since"]),
        }
        for row in friendships
    ]

    like_rows = [
        {
            "person_id": to_int(row["person_id"]),
            "hobby_id": to_int(row["hobby_id"]),
        }
        for row in likes
    ]

    # Clean database
    session.run("MATCH (n) DETACH DELETE n").consume()

    # Constraints
    session.run(
        """
        CREATE CONSTRAINT person_id_unique IF NOT EXISTS
        FOR (p:Person)
        REQUIRE p.id IS UNIQUE
        """
    ).consume()

    session.run(
        """
        CREATE CONSTRAINT hobby_id_unique IF NOT EXISTS
        FOR (h:Hobby)
        REQUIRE h.id IS UNIQUE
        """
    ).consume()

    # Person nodes
    session.run(
        """
        UNWIND $rows AS row
        MERGE (p:Person {id: row.id})
        SET p.name = row.name,
            p.age = row.age,
            p.city = row.city,
            p.gender = row.gender
        """,
        rows=people_rows,
    ).consume()

    # Hobby nodes
    session.run(
        """
        UNWIND $rows AS row
        MERGE (h:Hobby {id: row.id})
        SET h.name = row.name
        """,
        rows=hobby_rows,
    ).consume()

    # FRIEND relationships
    session.run(
        """
        UNWIND $rows AS row
        MATCH (p1:Person {id: row.person1_id})
        MATCH (p2:Person {id: row.person2_id})
        MERGE (p1)-[r:FRIEND]->(p2)
        SET r.since = row.since
        """,
        rows=friendship_rows,
    ).consume()

    # LIKES relationships
    session.run(
        """
        UNWIND $rows AS row
        MATCH (p:Person {id: row.person_id})
        MATCH (h:Hobby {id: row.hobby_id})
        MERGE (p)-[:LIKES]->(h)
        """,
        rows=like_rows,
    ).consume()


def print_records(title: str, records: list[dict[str, Any]]) -> None:
    """Print query results in a readable way"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

    if not records:
        print("No records returned")
        return

    for record in records:
        print(record)


def run_required_queries(session) -> None:
    """Run validation and the required project queries"""

    queries = [
        (
            "Validation: node counts",
            """
            MATCH (n)
            RETURN labels(n) AS type, count(n) AS total
            ORDER BY type
            """,
        ),
        (
            "Validation: relationship counts",
            """
            MATCH ()-[r]->()
            RETURN type(r) AS relationship, count(r) AS total
            ORDER BY relationship
            """,
        ),
        (
            "a. List all people",
            """
            MATCH (p:Person)
            RETURN p.id AS id, p.name AS name, p.age AS age, p.city AS city, p.gender AS gender
            ORDER BY p.id
            """,
        ),
        (
            "b. Find all friends of Person A",
            """
            MATCH (:Person {name: 'Person A'})-[:FRIEND]-(friend:Person)
            RETURN friend.name AS friend
            ORDER BY friend.name
            """,
        ),
        (
            "c. Find all people living in Paris",
            """
            MATCH (p:Person {city: 'Paris'})
            RETURN p.name AS name, p.age AS age, p.gender AS gender
            ORDER BY p.name
            """,
        ),
        (
            "d. Find all friendship pairs with the year they became friends",
            """
            MATCH (p1:Person)-[r:FRIEND]->(p2:Person)
            RETURN p1.name AS name1, p2.name AS name2, r.since AS since
            ORDER BY since
            """,
        ),
        (
            "e. Count number of friends each person has",
            """
            MATCH (p:Person)
            OPTIONAL MATCH (p)-[:FRIEND]-(friend:Person)
            RETURN p.name AS name, count(friend) AS number_of_friends
            ORDER BY number_of_friends DESC, name
            """,
        ),
        (
            "f. Find all people who like Cooking",
            """
            MATCH (p:Person)-[:LIKES]->(:Hobby {name: 'Cooking'})
            RETURN p.name AS name
            ORDER BY name
            """,
        ),
        (
            "g. Find friends who share at least one hobby",
            """
            MATCH (p1:Person)-[:FRIEND]-(p2:Person)
            MATCH (p1)-[:LIKES]->(h:Hobby)<-[:LIKES]-(p2)
            WHERE p1.id < p2.id
            RETURN p1.name AS name1, p2.name AS name2, h.name AS shared_hobby
            ORDER BY name1, name2, shared_hobby
            """,
        ),
        (
            "h. Count hobbies by city",
            """
            MATCH (p:Person)-[:LIKES]->(h:Hobby)
            RETURN p.city AS city, h.name AS hobby, count(p) AS people_count
            ORDER BY city, people_count DESC, hobby
            """,
        ),
        (
            "i. Most popular hobby - complete ranking",
            """
            MATCH (p:Person)-[:LIKES]->(h:Hobby)
            RETURN h.name AS hobby, count(p) AS people_count
            ORDER BY people_count DESC, hobby
            """,
        ),
        (
            "i. Most popular hobby - top result only",
            """
            MATCH (p:Person)-[:LIKES]->(h:Hobby)
            RETURN h.name AS hobby, count(p) AS people_count
            ORDER BY people_count DESC, hobby
            LIMIT 1
            """,
        ),
    ]

    for title, query in queries:
        records = [record.data() for record in session.run(query)]
        print_records(title, records)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load Project #3 CSV files into Neo4j.")
    parser.add_argument(
        "--uri",
        default=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        help="Neo4j Bolt URI. Default: bolt://localhost:7687",
    )
    parser.add_argument(
        "--user",
        default=os.getenv("NEO4J_USER", "neo4j"),
        help="Neo4j username. Default: neo4j",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("NEO4J_PASSWORD"),
        help="Neo4j password. If omitted, the script will ask for it.",
    )
    parser.add_argument(
        "--database",
        default=os.getenv("NEO4J_DATABASE", "neo4j"),
        help="Neo4j database name. Default: neo4j",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    password = args.password
    if not password:
        password = getpass.getpass("Neo4j password: ")

    driver = GraphDatabase.driver(args.uri, auth=(args.user, password))

    try:
        driver.verify_connectivity()

        with driver.session(database=args.database) as session:
            print("Connected to Neo4j")
            print("Loading graph from CSV files")
            load_graph(session)
            print("Graph loaded successfully")
            run_required_queries(session)

    finally:
        driver.close()


if __name__ == "__main__":
    main()
