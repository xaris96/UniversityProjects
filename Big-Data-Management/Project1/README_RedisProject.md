# Redis Events API – Project 1

Υλοποίηση της εκφώνησης *Project #1 – Redis / Key-Value Stores* με χρήση FastAPI και Redis.

## Description

Η εφαρμογή υλοποιεί ένα σύστημα διαχείρισης events με τις εξής λειτουργίες:

* δημιουργία και ενεργοποίηση events
* διαχείριση συμμετεχόντων (check-in / checkout)
* υποστήριξη public και private events
* chat ανά event
* εύρεση κοντινών events με βάση γεωγραφική θέση
* scheduler για αυτόματη ενεργοποίηση και απενεργοποίηση events
* καταγραφή ενεργειών (logs)

## Technologies

* Python (FastAPI)
* Redis (in-memory key-value store)
* Uvicorn

## Redis Data Structures

* HASH `event:{id}` για αποθήκευση στοιχείων event
* SET `all_events` για όλα τα events
* SET `active_events` για τα ενεργά events
* ZSET `event:{id}:participants` για participants με timestamp εισόδου
* LIST `event:{id}:chat` για μηνύματα chat
* SET `user:{email}:events_posted` για events στα οποία έχει γράψει ο χρήστης
* LIST `logs` για καταγραφή ενεργειών
* GEO `events:locations` για αποθήκευση γεωγραφικών δεδομένων

## Installation

```bash
pip install -r requirements.txt
```

## Run Redis

Απαιτείται Redis server στη θύρα 6379:

```bash
redis-server
```

## Run Application

```bash
uvicorn RedisProject_completed:app --reload
```

## Access

Frontend:

```text
http://127.0.0.1:8000/
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

* start-event(event-id)
* stop-event(event-id)
* checkin(email, event-id)
* checkout(email, event-id)
* find-events(email, x, y)
* get-participants(event-id)
* num-participants(event-id)
* checkout-byadmin(email, event-id)
* checkin-byadmin(email, event-id)
* get-events()
* post-to-chat(email, event-id, text)
* get-posts(event-id)
* get-user-posts(email)

## Scheduler

Υλοποιείται background scheduler που εκτελείται κάθε 60 δευτερόλεπτα και:

* ενεργοποιεί events όταν ξεκινά το χρονικό τους διάστημα
* απενεργοποιεί events όταν λήγει

## Assumptions

* Ένα event θεωρείται ενεργό μόνο αν βρίσκεται εντός του χρονικού του διαστήματος και έχει ενεργοποιηθεί (manual ή μέσω scheduler)
* Αν το audience είναι κενό, το event είναι public
* Αν το audience περιέχει emails, το event είναι private
* Οι special participants έχουν πρόσβαση ανεξάρτητα από το audience
* Για συμμετοχή στο chat απαιτείται check-in ή special participant
* Τα αποτελέσματα επιστρέφονται σε αύξουσα χρονική σειρά όπου απαιτείται

## Testing

Η εφαρμογή μπορεί να ελεγχθεί μέσω:

* του frontend interface
* του Swagger UI (/docs)
* HTTP requests (π.χ. curl)

## Submission

Το project περιλαμβάνει:

* RedisProject_completed.py
* requirements.txt
* README.md
* screenshots από testing
