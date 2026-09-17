import { supabase } from './supabase';

// Every device gets a persistent, invisible anonymous identity (no login
// screen, no password) so Supabase's row-level security can tell "your
// pending submissions" apart from everyone else's, and from approved ones
// everyone can see. Requires "Anonymous Sign-ins" enabled in the Supabase
// project's Auth settings.
export async function ensureAnonymousUser(): Promise<void> {
  if (!supabase) return;
  const { data } = await supabase.auth.getSession();
  if (data.session) return;
  await supabase.auth.signInAnonymously();
}
