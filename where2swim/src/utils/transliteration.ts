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
