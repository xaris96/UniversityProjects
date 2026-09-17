-- Where2Swim: community-submitted beaches
-- Run this once in the Supabase SQL Editor (Project > SQL Editor > New query)
-- for a brand-new project. If you already ran an earlier version of this
-- file, use migration_private_submissions.sql instead — it upgrades an
-- existing table in place without losing data.

create table if not exists community_beaches (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 2 and 60),
  prefecture text not null check (prefecture in ('chania', 'rethymno', 'heraklion', 'lasithi')),
  coast text not null check (coast in ('N', 'S', 'E', 'W')),
  latitude double precision not null check (latitude between 34.7 and 35.8),
  longitude double precision not null check (longitude between 23.3 and 26.5),
  submitted_at timestamptz not null default now(),
  -- Every submission starts private to the device that made it. You (the
  -- project owner) review pending rows in Table Editor and flip status to
  -- 'approved' for the ones you want everyone to see.
  status text not null default 'pending' check (status in ('pending', 'approved')),
  submitted_by uuid references auth.users (id)
);

alter table community_beaches enable row level security;

-- Everyone can see approved beaches; a device can also see its own
-- still-pending submissions (and nobody else's).
create policy "Read approved or own"
  on community_beaches for select
  using (status = 'approved' or submitted_by = auth.uid());

-- Anyone (anonymous auth) can submit, but only ever as pending and only
-- tagged with their own device id — nobody can self-approve or submit on
-- someone else's behalf. There is intentionally no update/delete policy,
-- so only you (via the Supabase dashboard, which bypasses RLS) can approve
-- or remove a row.
create policy "Insert own pending"
  on community_beaches for insert
  with check (submitted_by = auth.uid() and status = 'pending');
