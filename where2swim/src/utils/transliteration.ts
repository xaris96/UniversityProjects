const GREEK_TO_LATIN: Record<string, string> = {
  α: 'a', β: 'v', γ: 'g', δ: 'd', ε: 'e', ζ: 'z', η: 'i', θ: 'th', ι: 'i', κ: 'k', λ: 'l', μ: 'm',
  ν: 'n', ξ: 'x', ο: 'o', π: 'p', ρ: 'r', σ: 's', ς: 's', τ: 't', υ: 'y', φ: 'f', χ: 'ch', ψ: 'ps', ω: 'o',
  ά: 'a', έ: 'e', ή: 'i', ί: 'i', ό: 'o', ύ: 'y', ώ: 'o', ϊ: 'i', ΐ: 'i', ϋ: 'y', ΰ: 'y',
};

// Greek digraphs that represent a single sound different from their
// letter-by-letter transliteration (μπ = "b", not "mp") — handled before
// per-character mapping so common toponyms still match correctly.
const DIGRAPHS: [RegExp, string][] = [
  [/μπ/g, 'b'],
  [/ντ/g, 'd'],
  [/γκ/g, 'g'],
  [/γγ/g, 'g'],
];

// Normalizes a name for cross-script matching: lowercase, strip accents,
// transliterate Greek letters to Latin, strip non-alphanumerics. Lets
// "Κερατόκαμπος" match a beach only ever stored as "Keratokambos" (and
// vice versa) — some auto-imported beaches only ever had a Latin name
// tagged in OpenStreetMap.
export function normalizeForSearch(text: string): string {
  let stripped = text
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase();
  for (const [pattern, replacement] of DIGRAPHS) {
    stripped = stripped.replace(pattern, replacement);
  }
  const transliterated = stripped
    .split('')
    .map((ch) => GREEK_TO_LATIN[ch] ?? ch)
    .join('');
  return transliterated.replace(/[^a-z0-9]+/g, '');
}

const VOICED_NEXT = new Set(['β', 'γ', 'δ', 'ζ', 'λ', 'μ', 'ν', 'ρ']);
const VOWELS = new Set(['α', 'ε', 'η', 'ι', 'ο', 'υ', 'ω', 'ά', 'έ', 'ή', 'ί', 'ό', 'ύ', 'ώ']);
const GREEK_RUN = /[Ͱ-Ͽἀ-῿]+/g;

function isAlpha(ch: string | undefined): boolean {
  return ch === 'α' || ch === 'ά';
}
function isEpsilon(ch: string | undefined): boolean {
  return ch === 'ε' || ch === 'έ';
}
function isEta(ch: string | undefined): boolean {
  return ch === 'η' || ch === 'ή';
}
function isOmicron(ch: string | undefined): boolean {
  return ch === 'ο' || ch === 'ό';
}
function isUpsilon(ch: string | undefined): boolean {
  return ch === 'υ' || ch === 'ύ';
}

// Transliterates a single Greek word (no spaces/punctuation) to Latin
// following ELOT 743 (the Greek standard used on road signs/passports):
// μπ/ντ/γκ are "b/d/g" word-initially but "mp/nt/gk" mid-word, γγ is
// always "ng", and αυ/ευ/ηυ become "av/ev/iv" before voiced sounds or
// "af/ef/if" before voiceless ones — unlike the phonetic flattening in
// normalizeForSearch, which throws this distinction away on purpose.
function transliterateWord(word: string): string {
  const chars = word.toLowerCase().split('');
  let out = '';
  let i = 0;
  let atWordStart = true;
  while (i < chars.length) {
    const c = chars[i];
    const c2 = chars[i + 1];

    if (c === 'μ' && c2 === 'π') {
      out += atWordStart ? 'b' : 'mp';
      i += 2;
    } else if (c === 'ν' && c2 === 'τ') {
      out += atWordStart ? 'd' : 'nt';
      i += 2;
    } else if (c === 'γ' && c2 === 'κ') {
      out += atWordStart ? 'g' : 'gk';
      i += 2;
    } else if (c === 'γ' && c2 === 'γ') {
      out += 'ng';
      i += 2;
    } else if (c === 'τ' && c2 === 'σ') {
      out += 'ts';
      i += 2;
    } else if (c === 'τ' && c2 === 'ζ') {
      out += 'tz';
      i += 2;
    } else if ((isAlpha(c) || isEpsilon(c) || isEta(c)) && isUpsilon(c2)) {
      const next = chars[i + 2];
      const voiced = next !== undefined && (VOICED_NEXT.has(next) || VOWELS.has(next));
      const base = isAlpha(c) ? 'a' : isEpsilon(c) ? 'e' : 'i';
      out += base + (voiced ? 'v' : 'f');
      i += 2;
    } else if (isOmicron(c) && isUpsilon(c2)) {
      out += 'ou';
      i += 2;
    } else {
      out += GREEK_TO_LATIN[c] ?? c;
      i += 1;
    }
    atWordStart = false;
  }
  return out;
}

// Display-quality Greek → Latin transliteration: preserves word breaks,
// punctuation and per-word capitalization, so it can stand in directly as
// a beach's English/Greeklish name (unlike normalizeForSearch, which is
// built only for fuzzy matching and strips everything to bare lowercase).
export function transliterateForDisplay(text: string): string {
  return text.replace(GREEK_RUN, (word) => {
    const result = transliterateWord(word);
    return result.charAt(0).toUpperCase() + result.slice(1);
  });
}
