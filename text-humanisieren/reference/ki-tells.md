# KI-Tells — Katalog mit Vorher/Nachher

Grundlage: Deep-Research „Textforensik" (Juli 2026). Sortiert nach **Hebelwirkung** — oben die Änderungen, die am meisten bringen. Jede Regel: was tilgen, **warum**, und ein Beispiel.

> **Merksatz:** Nicht das einzelne Merkmal verrät die KI, sondern die *Häufung*. Und: Dirk nutzt einige dieser Mittel selbst *bewusst und gut*. Getilgt wird nur die **hohle** Variante. Im Zweifel gegen `dirk-stimme.md` prüfen.

---

## 1. Rhythmus aufbrechen (größter Hebel)

**Tell:** Fast alle Sätze im 15–25-Wort-Band, jeder Absatz 3–5 gleich lange Sätze. Metronomisch. Der zuverlässigste *stilistische* Marker (KI-Text hat niedrige „Burstiness").

**Warum:** Autoregressive Modelle kollabieren im Default zur mittleren Satzform. Menschen schreiben *bursty* — kurze Schlagsätze neben langen Ketten.

**Fix:** Zerlege einen langen Satz in einen kurzen + einen langen. Setze bewusst einen 2–4-Wort-Satz als Pointe.

> **Vorher:** „Die Digitalisierung verändert die Schule grundlegend, und es ist wichtig, dass Lehrkräfte sich anpassen, um den Anschluss nicht zu verlieren und die Schülerinnen und Schüler bestmöglich vorzubereiten."
>
> **Nachher:** „Die Digitalisierung verändert die Schule grundlegend. Nur: Die Strukturen ändern sich nicht mit. Und während die Lehrpläne noch über Tablet-Klassen diskutieren, hat die KI die Frage längst verschoben — weg vom *Zugang* zu Werkzeugen, hin zu dem, was der Mensch damit noch selbst denken muss."

---

## 2. Floskeln streichen (größter Hebel)

**Tell:** Leere Transitions- und Hedge-Phrasen. Vollständige Liste unten.

**Warum:** Hochfrequent im „Assistant"-Register, durch RLHF verstärkt. Sagen nichts.

**Fix:** Ersatzlos streichen — oder durch einen konkreten Anker ersetzen (Jahr, Ort, Zahl, Szene).

### Streichliste (DE)
| Floskel | Ersatz |
|---------|--------|
| „Es ist wichtig zu beachten, dass X" | einfach „X" |
| „Es sei angemerkt / darauf hingewiesen" | streichen |
| „In der heutigen schnelllebigen Welt / In einer Zeit, in der …" | konkrete Szene oder Jahr |
| „Zusammenfassend / Abschließend lässt sich sagen" | streichen oder echte Pointe |
| „Ein weiterer wichtiger Aspekt ist …" | direkt zum Aspekt |
| „spielt eine entscheidende Rolle" | *was genau* tut es? |
| „Tauchen wir ein / Lassen Sie uns …" | direkt anfangen |
| „Viele Experten sind sich einig, dass" | Quelle nennen oder abschwächen |
| „Ein guter Weg, dies zu erreichen, ist" | direkt sagen wie |

---

## 3. Hohle Verstärker & Superlative raus

**Tell:** „zweifellos, entscheidend, bemerkenswert, wesentlich, nahtlos, robust, ganzheitlich, umfassend, revolutionär, bahnbrechend".

**Warum:** Bewertungs-Adjektive ohne Beleg — das Modell *behauptet* Bedeutung, statt sie zu *zeigen*.

**Fix:** Streichen. Wenn die Sache wichtig ist, zeigt der konkrete Inhalt das von selbst.

> **Vorher:** „Dieser bemerkenswerte Ansatz spielt eine entscheidende Rolle bei der nahtlosen Integration."
> **Nachher:** „Der Ansatz spart drei Arbeitsschritte — die Datei landet direkt in Moodle, ohne Zwischenexport."

---

## 4. Die „nicht X, sondern Y"-Antithese entschärfen

**Tell:** „Es geht nicht um die Technik — es geht um den Menschen." / „nicht nur …, sondern auch …". Als *Reflex*, mehrfach.

**Warum:** RLHF-Artefakt; täuscht Tiefe vor. **ABER:** In Maßen ist das ein starkes rhetorisches Mittel — Dirk nutzt es gezielt („Prohibition und Legalisierung sind keine Gegensätze. Sie sind zwei Phasen derselben Einhegung.").

**Fix:** Auf **maximal eine** tragende Instanz pro Text reduzieren, und die muss eine *echte* Zuspitzung sein, keine Deko. Restliche in normale Aussagesätze auflösen.

---

## 5. Zwangs-Fazit killen

**Tell:** Schlussabsatz, der nur die Einleitung in neuen Worten wiederholt. Oft mit „Zusammenfassend" / „Insgesamt".

**Warum:** Die „Einleitung-Hauptteil-Schluss"-Schablone ist überrepräsentiert und wird als „gut strukturiert" belohnt.

**Fix:** Streichen. Ersetzen durch eine **Pointe**, eine **offene Frage** an die Leser (Dirk tut das) oder — je nach Kanal — den Signatur-Closer „Willkommen im Enterprise-Zeitalter".

---

## 6. Vage Quellen erden

**Tell:** „Studien zeigen", „Forschung legt nahe", „Experten glauben" — nie mit Namen.

**Warum:** Das Modell hat keine reale Quelle und flüchtet in die plausibel klingende Hülle.

**Fix:** Wenn im Text belegbar → konkrete Quelle + Zahl (Dirk: „Die Lancet-Studie von Nutt u.a. (2010) … Alkohol Score 72, Cannabis 20."). Wenn **nicht** belegbar → Behauptung abschwächen. **Niemals eine Quelle erfinden.**

---

## 7. Reflexhafte Beidseitigkeit zuspitzen

**Tell:** Symmetrisches „einerseits/andererseits", obwohl die Faktenlage schief ist. Refuse-to-commit.

**Warum:** Annotatoren belohnen scheinbare „Ausgewogenheit".

**Fix:** Position beziehen. Dirks Signatur: die These offen ansagen und dann tragen. Ausgewogenheit nur, wo die Sache *wirklich* offen ist.

---

## 8. Form-Tells (schwach, aber in Häufung sichtbar)

**Tell:** Gedankenstrich in jedem Absatz; Aufzählungen mit **fett-Doppelpunkt**-Anfang statt Fließtext; Emoji als Bullets; Titel-Case-Überschriften.

**Warum:** Markdown-Training der Chat-Modelle. **ABER:** em-dash und gezielte Fettung sind Teil von Dirks echtem Stil — nicht stumpf entfernen!

**Fix:** Nur die *überzähligen* Instanzen. Faustregel: höchstens 1 Gedankenstrich pro Absatz; Bullet-Listen nur, wo es wirklich eine Liste ist, sonst zu Fließtext machen; Emoji-Bullets in Fließtext raus (in LinkedIn-Posts sind 1–2 okay).

---

## 9. Anglizismen / Übersetzungs-Deutsch (bei DE-Texten)

**Tell:** „adressieren" (statt ansprechen/angehen), „liefern" (deliver), „im Bereich" (in the space of), „beleuchten" (shed light on), „nahtlos/robust/ganzheitlich" als Buzzwords.

**Warum:** Das Modell „denkt" englisch-gewichtet; Idiome kommen als Lehnübersetzung durch.

**Fix:** Durch idiomatisches Deutsch ersetzen.

---

## 10. Leftover-Gerüst (immer entfernen)

**Tell:** „Certainly! Here is …", „Als KI-Sprachmodell …", „Ich hoffe, das hilft!", Platzhalter „[Quelle einfügen]", „Hier ist ein möglicher Entwurf:".

**Warum:** Unbearbeitete Roh-Ausgabe. **Stärkster** Beweis für ungeprüfte Übernahme.

**Fix:** Restlos raus. (Bei Dirks Texten praktisch nie vorhanden, aber prüfen.)

---

## Reihenfolge beim Überarbeiten
1. Leftover-Gerüst raus (10)
2. Floskeln raus (2)
3. Rhythmus aufbrechen (1)
4. Hohle Verstärker (3)
5. Antithese/Beidseitigkeit zuspitzen (4, 7)
6. Zwangs-Fazit (5)
7. Quellen erden (6)
8. Anglizismen (9)
9. Form fein justieren (8)
10. **Stimme einsetzen** — der Schritt, der aus „nicht mehr KI" ein „klingt nach Dirk" macht (siehe `dirk-stimme.md`).
