-- Where2Swim: upgrade existing community_beaches to "private until approved"
-- Run this ONCE in the Supabase SQL Editor against your existing project.
-- Safe to run even with existing rows — they get grandfathered in as
-- already-approved (they were publicly visible before this migration).

alter table community_beaches
  add column if not exists status text not null default 'pending' check (status in ('pending', 'approved')),
  add column if not exists submitted_by uuid references auth.users (id);

-- Grandfather in every row that existed before this migration.
update community_beaches set status = 'approved' where status = 'pending';

-- Replace the old fully-open policies with the new private-until-approved ones.
drop policy if exists "Public read access" on community_beaches;
drop policy if exists "Public insert access" on community_beaches;

create policy "Read approved or own"
  on community_beaches for select
  using (status = 'approved' or submitted_by = auth.uid());

create policy "Insert own pending"
  on community_beaches for insert
  with check (submitted_by = auth.uid() and status = 'pending');
