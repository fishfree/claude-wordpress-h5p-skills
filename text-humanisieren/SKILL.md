---
name: text-humanisieren
description: Überarbeitet einen fertigen Text vor der Veröffentlichung so, dass er beim Publikum ankommt — Denke vom Markt/Leser her, nicht Verschleierung. Typische KI-Schreibspuren (Floskeln, Metronom-Rhythmus, hohle Verstärker, Zwangs-Fazit) raus, Dirks eigene Stimme und Substanz rein, damit der Text als kompetent und eigenständig gelesen und nicht reflexhaft als "bloß KI" abgetan wird. Use when Dirk is about to publish a blog post, LinkedIn post, business email, or any public text and wants it de-slopped / voice-restored. NICHT zum Recherchieren (dafür recherche-workflow) und NICHT zum Neuschreiben — nur minimal-invasive Überarbeitung eines vorhandenen Textes.
license: MIT
---

# Text-Humanisieren — Marktwirkung statt Detektor-Trickserei

Überarbeitet **einen bereits vorhandenen Text** minimal-invasiv: raus mit den KI-Schreibspuren, rein mit Dirks Stimme. Es geht **nicht** um Verschleierung — dass KI im Spiel war, ist kein Geheimnis und muss nicht versteckt werden. Es geht um **Wirkung am Markt**: Ein generischer, glatter Text verliert den Leser (und den Kunden), *bevor* die Aussage ankommt. Der „ach, das ist nur KI"-Reflex ist ein **Conversion-Killer** — er lässt den Adressaten „der hat bestimmt keine Ahnung" denken und abschalten. Ob dabei auch ein Detektor schlechter anschlägt, ist ein Nebeneffekt, nicht der Zweck.

## Leitprinzip (das Wichtigste zuerst)

> **Denke vom Leser / Markt her.** Der Job ist nicht, KI zu tarnen, sondern den Text so zu machen, dass **Substanz, Stimme und Haltung sofort sichtbar** sind — damit er als kompetent und eigenständig gelesen wird.
> Der stärkste Hebel gegen den „keine-Ahnung"-Reflex ist ein Text mit konkreter Substanz, eigenem Rhythmus und klarer Position. Genau das, was ein Sprachmodell im Default *nicht* produziert — und genau das, was am Markt Vertrauen schafft.

Daraus folgt die zentrale Regel dieses Skills:

**Unterscheide hohle KI-Mittel von Dirks echten Stilmitteln.** Dirk nutzt selbst Gedankenstriche, Fettungen und Dreierfiguren — bewusst und gut (siehe `reference/dirk-stimme.md`). Diese bleiben. Getilgt wird nur die *leere* Variante: der Gedankenstrich ohne Grund, die Fettung ohne Pointe, die Triade als Reflex.

## Ablauf

### Schritt 0 — Eingang klären
1. **Text entgegennehmen** (Dateipfad oder eingefügt).
2. **Zielformat + Register erfragen**, falls nicht offensichtlich — die Stimme unterscheidet sich je nach Kanal:
   | Register | Charakter | Referenz |
   |----------|-----------|----------|
   | **Blog / Essay** | Sie-Ansprache, szenischer Einstieg, essayistisch, Refrain-Struktur | `reference/dirk-stimme.md` §Blog |
   | **LinkedIn** | ein Gedanke, ein Hook, kürzer, teils Ich-Form, Einladung am Ende | §LinkedIn |
   | **Business-/Akquise-Mail** | diplomatisch-indirekte Hebel, peer-respektvoll | §Mail + Memory `feedback-elegant-email-framing` |
   | **Fachtext / Unterricht** | klar, BS:WI-Ton, konkret, ohne Anbiederung | §Fachtext |

### Schritt 1 — Befund (kurz!)
Lies den Text gegen `reference/ki-tells.md` und gib einen **knappen Befund** aus — kein Roman, eine Tabelle reicht:

```
BEFUND (KI-Dichte: niedrig / mittel / hoch)
- Floskeln:        3× ("es ist wichtig zu beachten", "in der heutigen …", "zusammenfassend")
- Rhythmus:        Metronom — 9 von 11 Sätzen im 15–22-Wort-Band
- Hohle Verstärker: 2× ("zweifellos", "spielt eine entscheidende Rolle")
- Zwangs-Fazit:    1× (letzter Absatz wiederholt nur die Einleitung)
- Vage Quellen:    1× ("Studien zeigen" ohne Nennung)
- Dirks Stimme:    fehlt — keine konkrete Anekdote, kein Refrain, keine Pointe
```

Der Befund macht transparent, *was* geändert wird — Dirk bleibt in Kontrolle.

### Schritt 2 — Minimal-invasiv überarbeiten
Arbeite die Tells ab (Details + Vorher/Nachher in `reference/ki-tells.md`). Kernbewegungen:

1. **Floskeln streichen oder durch Substanz ersetzen.** „Es ist wichtig zu beachten, dass X" → einfach „X". „In der heutigen schnelllebigen Welt" → konkreter Anker (Jahr, Ort, Szene).
2. **Rhythmus aufbrechen.** Zerlege einen langen Satz in einen kurzen Schlagsatz + einen langen. Setze bewusst einen Drei-Wort-Satz. Dirks Prosa *atmet* ungleichmäßig — das ist der stärkste Menschlichkeits-Marker.
3. **Hohle Verstärker raus.** „zweifellos / entscheidend / bemerkenswert / nahtlos" ersatzlos streichen oder durch ein konkretes Detail ersetzen.
4. **Vage Quellen erden.** „Studien zeigen" → konkrete Quelle mit Namen/Zahl, wenn im Text belegbar; wenn nicht belegbar, Behauptung abschwächen statt Autorität vortäuschen.
5. **Zwangs-Fazit killen.** Ein Schluss, der nur die Einleitung wiederholt, wird gestrichen oder in eine echte Pointe / offene Frage / Dirks Signatur-Closer verwandelt.
6. **Beidseitigkeit auf eine Haltung zuspitzen.** Wo der Text symmetrisch „einerseits/andererseits" hedged, obwohl die Sache klar ist: Position beziehen (Dirk tut das — „Das ist die These, die ich Ihnen anbieten möchte:").
7. **Stimme einsetzen.** Wo es trägt: ein szenischer Einstieg, ein wiederkehrendes Motiv, eine trockene Verdichtung, ein benannter konkreter Beleg. Siehe `reference/dirk-stimme.md`.

### Schritt 3 — Ausgabe
Gib zurück:
1. **Den überarbeiteten Text** (kopierfertig, im Zielformat).
2. **Changelog** — 4–8 Zeilen „was geändert & warum", damit Dirk jede Änderung nachvollziehen und zurückdrehen kann.
3. Bei Bedarf: **Vorher/Nachher-Gegenüberstellung** der 2–3 markantesten Stellen.

## Verbindliche Grenzen (Ehrlichkeits-Guardrails)

Dieser Skill überarbeitet **Dirks eigene Texte und Ideen**, die unter seinem Namen erscheinen — legitim, es geht um Stil, nicht um Täuschung über Urheberschaft. Deshalb gilt strikt:

- **NIEMALS Fakten, Zahlen oder Quellen erfinden**, um „menschlicher"/glaubwürdiger zu wirken. Das ist genau der KI-Fehler, den wir bekämpfen (Halluzination). Substanz kommt aus dem Text oder aus echter Recherche — nie aus der Luft.
- **KEINE Billig-Tricks:** keine unsichtbaren Unicode-Zeichen, keine absichtlichen Tippfehler, keine eingestreuten Zufallswörter zum „Perplexity-Aufblähen". Das ist plump, leicht zu entfernen und untergräbt Dirks Glaubwürdigkeit, wenn es auffliegt.
- **Bedeutung bleibt erhalten.** Keine Aussage verdrehen, keine Nuance verlieren. Im Zweifel Dirk fragen, statt zu raten.
- **Nicht über-humanisieren.** Ein Text, der vor gewollter Unregelmäßigkeit knirscht, ist genauso auffällig wie ein glatter KI-Text. Zielbild ist Dirks *natürliche* Prosa, nicht „maximal chaotisch".
- **Der Text gehört Dirk.** Bei größeren inhaltlichen Eingriffen (Umstellungen, Kürzungen ganzer Absätze) erst fragen.

## Was dieser Skill NICHT ist
- **Kein Recherche-Tool** — dafür `recherche-workflow`.
- **Kein Neuschreiber / Ghostwriter** — er arbeitet einen vorhandenen Text nach, er erfindet keinen.
- **Kein Detektor** — die Analyse-/Erkennungslogik lebt im Textforensik-Dossier (Artifact), hier wird sie nur zum *Verbessern* genutzt.

## Referenzen
- `reference/ki-tells.md` — Katalog der Tells mit Vorher/Nachher-Beispielen (Grundlage: Deep-Research Juli 2026).
- `reference/dirk-stimme.md` — Dirks Stimm-Profil je Register, aus echten Texten destilliert.
