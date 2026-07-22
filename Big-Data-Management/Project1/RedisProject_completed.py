import asyncio
import json
import math
import time
from typing import List

import redis
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Redis Events API", version="1.0")
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Helpers

def log_action(action: str, details: dict):
    entry = {"timestamp": int(time.time()), "action": action, **details}
    r.rpush("logs", json.dumps(entry))


def event_key(event_id: str) -> str:
    return f"event:{event_id}"


def participants_key(event_id: str) -> str:
    return f"event:{event_id}:participants"


def chat_key(event_id: str) -> str:
    return f"event:{event_id}:chat"


def active_key(event_id: str) -> str:
    return f"event:{event_id}:active"


def force_stopped_key(event_id: str) -> str:
    return f"event:{event_id}:force_stopped"


def event_exists(event_id: str) -> bool:
    return bool(r.exists(event_key(event_id)))


def parse_email_list(raw: str) -> List[str]:
    if not raw or raw.strip() == "":
        return []
    return [e.strip() for e in raw.split(",") if e.strip()]


def is_event_active_now(event_id: str) -> bool:
    start = r.hget(event_key(event_id), "start_time")
    end = r.hget(event_key(event_id), "end_time")
    if not start or not end:
        return False
    now = int(time.time())
    return int(start) <= now <= int(end)


def user_is_allowed(email: str, event_id: str) -> bool:
    audience = parse_email_list(r.hget(event_key(event_id), "audience") or "")
    if not audience:
        return True
    return email in audience


def user_is_special_participant(email: str, event_id: str) -> bool:
    special = parse_email_list(r.hget(event_key(event_id), "special_participants") or "")
    return email in special


def user_can_checkin(email: str, event_id: str) -> bool:
    # Special participants are always allowed, even for private events
    return user_is_special_participant(email, event_id) or user_is_allowed(email, event_id)


def user_is_checked_in(email: str, event_id: str) -> bool:
    return r.zscore(participants_key(event_id), email) is not None


def distance_km(x1: float, y1: float, x2: float, y2: float) -> float:
    # Haversine formula
    R = 6371.0
    lon1, lat1, lon2, lat2 = map(math.radians, [x1, y1, x2, y2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Front-end
html_content = """
<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redis Events Manager</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #111827; color: #f9fafb; }
        header { padding: 18px 24px; background: #1f2937; border-bottom: 1px solid #374151; }
        main { max-width: 1100px; margin: 24px auto; padding: 0 16px; }
        .card { background: #1f2937; padding: 18px; border-radius: 12px; margin-bottom: 18px; border: 1px solid #374151; }
        h1, h2 { margin-top: 0; }
        input, textarea { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #4b5563; background: #111827; color: #f9fafb; margin-top: 6px; }
        button { padding: 10px 14px; border: 0; border-radius: 8px; background: #2563eb; color: white; cursor: pointer; margin-top: 12px; }
        button:hover { background: #1d4ed8; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
        pre { background: #0b1220; padding: 12px; border-radius: 8px; overflow: auto; }
    </style>
</head>
<body>
<header><h1>Redis Events API Tester</h1></header>
<main>
    <div class="card">
        <h2>Health</h2>
        <button onclick="call('/get-events', 'out1')">GET /get-events</button>
        <pre id="out1">—</pre>
    </div>
    <div class="card">
        <h2>Create event</h2>
        <div class="grid">
            <div><label>ID<input id="eid" value="101"></label></div>
            <div><label>Title<input id="title" value="Redis Seminar"></label></div>
            <div><label>Subtitle<input id="subtitle" value="Key Value Stores"></label></div>
            <div><label>Longitude<input id="x" value="23.7275"></label></div>
            <div><label>Latitude<input id="y" value="37.9838"></label></div>
            <div><label>Radius km<input id="radius" value="5"></label></div>
            <div><label>Start unix<input id="start"></label></div>
            <div><label>End unix<input id="end"></label></div>
            <div><label>Special participants<input id="special" placeholder="speaker-placeholder"></label></div>
            <div><label>Audience<input id="audience" placeholder="leave empty for public"></label></div>
        </div>
        <button onclick="createEventRequest()">POST /create-event</button>
        <pre id="out2">—</pre>
    </div>
</main>
<script>
function nowTs(){ return Math.floor(Date.now()/1000); }
window.onload = () => { document.getElementById('start').value = nowTs(); document.getElementById('end').value = nowTs()+3600; };
async function call(url, outId, method='GET') {
    const res = await fetch(url, {method});
    const data = await res.json();
    document.getElementById(outId).textContent = JSON.stringify(data, null, 2);
}
async function createEventRequest() {
    const p = new URLSearchParams({
        title: eid('title'), subtitle: eid('subtitle'), x: eid('x'), y: eid('y'), radius: eid('radius'),
        start_time: eid('start'), end_time: eid('end'), special_participants: eid('special'), audience: eid('audience')
    });
    await call(`/create-event/${eid('eid')}?${p.toString()}`, 'out2', 'POST');
}
function eid(id){ return document.getElementById(id).value; }
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return html_content

# Endpoints
@app.post("/create-event/{event_id}")
def create_event(
    event_id: str,
    title: str,
    subtitle: str,
    x: float,
    y: float,
    radius: float,
    start_time: int,
    end_time: int,
    special_participants: str = "",
    audience: str = "",
):
    try:
        if event_exists(event_id):
            return {"status": "nok", "message": "Το event υπάρχει ήδη"}
        if start_time >= end_time:
            return {"status": "nok", "message": "Ο χρόνος λήξης πρέπει να είναι μετά τον χρόνο έναρξης"}
        if end_time - start_time > 24 * 3600:
            return {"status": "nok", "message": "Το lifetime του event πρέπει να είναι μικρότερο από 24 ώρες"}
        if radius <= 0:
            return {"status": "nok", "message": "Το radius πρέπει να είναι θετικό"}

        r.hset(event_key(event_id), mapping={
            "title": title,
            "subtitle": subtitle,
            "x": x,
            "y": y,
            "radius": radius,
            "start_time": start_time,
            "end_time": end_time,
            "special_participants": special_participants,
            "audience": audience,
        })
        r.geoadd("events:locations", (x, y, event_id))
        r.sadd("all_events", event_id)
        log_action("create_event", {"event_id": event_id, "title": title})
        return {"status": "ok", "message": f"Event {event_id} δημιουργήθηκε"}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.post("/start-event/{event_id}")
def start_event(event_id: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        if r.exists(active_key(event_id)):
            return {"status": "nok", "message": "Το event είναι ήδη ενεργό"}
        if not is_event_active_now(event_id):
            return {"status": "nok", "message": "Το event δεν είναι μέσα στο lifetime του"}
        r.set(active_key(event_id), "1")
        r.sadd("active_events", event_id)
        r.delete(force_stopped_key(event_id))
        log_action("start_event", {"event_id": event_id})
        return {"status": "ok", "message": f"Event {event_id} ξεκίνησε"}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.post("/stop-event/{event_id}")
def stop_event(event_id: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        if not r.exists(active_key(event_id)):
            return {"status": "nok", "message": "Το event δεν είναι ενεργό"}
        r.delete(active_key(event_id))
        r.srem("active_events", event_id)
        r.set(force_stopped_key(event_id), "1")
        log_action("stop_event", {"event_id": event_id})
        return {"status": "ok", "message": f"Event {event_id} σταμάτησε"}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.post("/checkin")
def checkin(email: str, event_id: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        if not r.exists(active_key(event_id)):
            return {"status": "nok", "message": "Το event δεν είναι ενεργό"}
        if not is_event_active_now(event_id):
            return {"status": "nok", "message": "Το event δεν είναι εντός χρόνου ζωής"}
        if not user_can_checkin(email, event_id):
            return {"status": "nok", "message": "Δεν επιτρέπεται η πρόσβαση"}
        if user_is_checked_in(email, event_id):
            return {"status": "nok", "message": "Ο χρήστης είναι ήδη checked-in"}
        ts = int(time.time())
        r.zadd(participants_key(event_id), {email: ts})
        log_action("checkin", {"email": email, "event_id": event_id})
        return {"status": "ok"}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.post("/checkout")
def checkout(email: str, event_id: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        if not r.exists(active_key(event_id)):
            return {"status": "nok", "message": "Το event δεν είναι ενεργό"}
        removed = r.zrem(participants_key(event_id), email)
        if removed == 0:
            return {"status": "nok", "message": "Ο χρήστης δεν βρέθηκε στο event"}
        log_action("checkout", {"email": email, "event_id": event_id})
        return {"status": "ok"}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.get("/find-events")
def find_events(email: str, x: float, y: float):
    try:
        candidates = r.smembers("active_events")
        result = []
        for event_id in candidates:
            if not event_exists(event_id):
                continue
            if not is_event_active_now(event_id):
                continue
            if not user_can_checkin(email, event_id):
                continue
            ex = float(r.hget(event_key(event_id), "x"))
            ey = float(r.hget(event_key(event_id), "y"))
            radius = float(r.hget(event_key(event_id), "radius"))
            if distance_km(x, y, ex, ey) <= radius:
                result.append(event_id)
        log_action("find_events", {"email": email, "found": len(result)})
        return {"events": sorted(result)}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.get("/get-participants/{event_id}")
def get_participants(event_id: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        raw = r.zrange(participants_key(event_id), 0, -1, withscores=True)
        participants = [{"email": email, "timestamp_of_join": int(ts)} for email, ts in raw]
        return {"participants": participants}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.get("/num-participants/{event_id}")
def num_participants(event_id: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        return {"count": r.zcard(participants_key(event_id))}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.post("/checkout-byadmin")
def checkout_byadmin(email: str, event_id: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        if not r.exists(active_key(event_id)):
            return {"status": "nok", "message": "Το event δεν είναι ενεργό"}
        removed = r.zrem(participants_key(event_id), email)
        if removed == 0:
            return {"status": "nok", "message": "Ο χρήστης δεν βρέθηκε"}
        log_action("checkout_byadmin", {"email": email, "event_id": event_id})
        return {"status": "ok"}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.post("/checkin-byadmin")
def checkin_byadmin(email: str, event_id: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        if not r.exists(active_key(event_id)):
            return {"status": "nok", "message": "Το event δεν είναι ενεργό"}
        if user_is_checked_in(email, event_id):
            return {"status": "nok", "message": "Ο χρήστης είναι ήδη checked-in"}
        ts = int(time.time())
        r.zadd(participants_key(event_id), {email: ts})
        log_action("checkin_byadmin", {"email": email, "event_id": event_id})
        return {"status": "ok"}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.get("/get-events")
def get_events():
    try:
        return {"events": sorted(list(r.smembers("active_events")))}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.post("/post-to-chat")
def post_to_chat(email: str, event_id: str, text: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        if not r.exists(active_key(event_id)):
            return {"status": "nok", "message": "Το event δεν είναι ενεργό"}
        if not is_event_active_now(event_id):
            return {"status": "nok", "message": "Το event δεν είναι εντός χρόνου ζωής"}
        if not user_is_checked_in(email, event_id) and not user_is_special_participant(email, event_id):
            return {"status": "nok", "message": "Μόνο checked-in ή special participants μπορούν να γράψουν στο chat"}
        entry = {"timestamp": int(time.time()), "email": email, "text": text}
        r.rpush(chat_key(event_id), json.dumps(entry))
        r.sadd(f"user:{email}:events_posted", event_id)
        log_action("post_to_chat", {"email": email, "event_id": event_id})
        return {"status": "ok"}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.get("/get-posts/{event_id}")
def get_posts(event_id: str):
    try:
        if not event_exists(event_id):
            return {"status": "nok", "message": "Το event δεν υπάρχει"}
        raw = r.lrange(chat_key(event_id), 0, -1)
        messages = [json.loads(m) for m in raw]
        messages.sort(key=lambda m: m["timestamp"])
        return {"messages": messages}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.get("/get-user-posts")
def get_user_posts(email: str):
    try:
        all_user_messages = []
        for event_id in r.smembers(f"user:{email}:events_posted"):
            for entry in r.lrange(chat_key(event_id), 0, -1):
                msg = json.loads(entry)
                if msg["email"] == email:
                    all_user_messages.append({"timestamp": msg["timestamp"], "text": msg["text"]})
        all_user_messages.sort(key=lambda m: m["timestamp"])
        return {"messages": all_user_messages}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


@app.get("/get-logs")
def get_logs():
    try:
        return {"logs": [json.loads(entry) for entry in r.lrange("logs", 0, -1)]}
    except Exception as e:
        return {"status": "nok", "error": str(e)}


# Scheduler
async def event_scheduler():
    while True:
        try:
            now = int(time.time())
            all_events = r.smembers("all_events")
            for event_id in all_events:
                if not event_exists(event_id):
                    continue
                start = r.hget(event_key(event_id), "start_time")
                end = r.hget(event_key(event_id), "end_time")
                if not start or not end:
                    continue
                start, end = int(start), int(end)
                is_active = bool(r.exists(active_key(event_id)))
                is_force_stopped = bool(r.exists(force_stopped_key(event_id)))

                if start <= now <= end and not is_active and not is_force_stopped:
                    r.set(active_key(event_id), "1")
                    r.sadd("active_events", event_id)
                    log_action("scheduler_start", {"event_id": event_id})

                elif now > end:
                    if is_active:
                        r.delete(active_key(event_id))
                        r.srem("active_events", event_id)
                        log_action("scheduler_stop", {"event_id": event_id})
                    if is_force_stopped:
                        r.delete(force_stopped_key(event_id))
        except Exception as e:
            print("[SCHEDULER ERROR]", e)
        await asyncio.sleep(60)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(event_scheduler())
