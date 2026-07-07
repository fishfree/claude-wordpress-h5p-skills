---
name: email-to-action
description: Process incoming emails and convert them to actionable items - calendar events, todos, or archive decisions. Analyzes email content to determine the appropriate action. Use when reviewing inbox or processing emails.
license: MIT
allowed-tools:
  - mcp__imap__imap_list_emails
  - mcp__imap__imap_move_email
  - mcp__imap__imap_bulk_move
  - mcp__imap__imap_list_folders
  - mcp__imap__imap_list_accounts
  - mcp__imap__imap_read_email
  - mcp__teams__calendar_create_event
---

# Email-to-Action Skill

Automatische Email-Verarbeitung: Analysiert Emails und schlägt passende Aktionen vor (Archivieren, Termin erstellen, Todo anlegen).

## MCP/Tool Integration

**Dieser Skill nutzt folgende Tools:**

| Tool | Zweck |
|------|-------|
| `imap_list_emails` | Emails aus Postfach abrufen |
| `imap_move_email` | Email in Zielordner verschieben |
| `imap_bulk_move` | Mehrere Emails auf einmal verschieben |
| `imap_list_folders` | Verfügbare Ordner anzeigen |
| `imap_list_accounts` | Verfügbare Accounts anzeigen |

**Zielordner (one.com Standard):**

| Kategorie | Ordner | Beschreibung |
|-----------|--------|--------------|
| Archiv | `INBOX._archiv` | Wichtige Emails zur Aufbewahrung |
| Admin | `INBOX._archiv.admin` | Verträge, Kündigungen, Kontoauszüge |
| Rechnungen | `INBOX._archiv.rechnung` | Rechnungen und Zahlungen |
| Newsletter | `INBOX._archiv.newsletter` | Newsletter zum Lesen |
| Termine | `INBOX._archiv.termin` | Terminbestätigungen |
| Spam | `INBOX.Spam` | Unerwünschte Werbung |

---

## Wann diesen Skill nutzen

- "Was ist in meinen Emails los?"
- "Sortiere meine Inbox"
- "Zeig mir wichtige Emails"
- "Verarbeite meine neuen Emails"
- "Was muss ich heute erledigen?"
- "Räume mein Postfach auf"

---

## Workflow

### Phase 1: Emails abrufen

```javascript
// Neue/ungelesene Emails abrufen
imap_list_emails({
  account: "onecom",
  folder: "INBOX",
  limit: 20,
  criteria: "UNSEEN"  // oder "ALL" für alle
})
```

### Phase 2: Kategorisierung

Für jede Email wird analysiert:

| Signal | Kategorie | Aktion |
|--------|-----------|--------|
| "Rechnung", "Invoice", "Zahlung" | `rechnung` | Archiv + Hinweis |
| "Termin", "Meeting", "Einladung" | `termin` | Archiv + Kalendereintrag vorschlagen |
| "Newsletter", "Abmelden" | `newsletter` | Archiv oder Löschen |
| "Passwort", "Konto", "Vertrag" | `admin` | Archiv |
| "Rabatt", "Sale", "Gutschein" | `werbung` | Spam oder Löschen |
| Persönliche Nachricht | `wichtig` | Im Inbox lassen |

**Klassifikations-Keywords:**

```javascript
const CATEGORIES = {
  rechnung: ['rechnung', 'invoice', 'zahlung', 'payment', 'quittung', 'receipt', 'bestellung', 'order'],
  termin: ['termin', 'meeting', 'einladung', 'appointment', 'kalender', 'calendar', 'datum', 'uhrzeit'],
  admin: ['passwort', 'password', 'konto', 'account', 'vertrag', 'contract', 'kündigung', 'bestätigung'],
  newsletter: ['newsletter', 'abmelden', 'unsubscribe', 'digest', 'weekly', 'update', 'news'],
  werbung: ['rabatt', 'discount', 'sale', 'gutschein', 'coupon', 'angebot', 'offer', 'deal', 'gratis', 'kostenlos']
};
```

### Phase 3: Aktionen vorschlagen

**Ausgabeformat:**

```markdown
## Inbox-Analyse: [Account]

### Aktionspunkte (erfordern Handlung)

| # | Von | Betreff | Aktion |
|---|-----|---------|--------|
| 1 | max@example.com | Meeting morgen | 📅 Termin anlegen |
| 2 | support@service.de | Ihre Rechnung | 💰 Prüfen + Archiv |

### Zum Archivieren

| # | Von | Betreff | Zielordner |
|---|-----|---------|------------|
| 3 | newsletter@shop.de | Wochenangebote | 📰 newsletter |
| 4 | noreply@bank.de | Kontoauszug | 📁 admin |

### Zum Löschen (Werbung/Spam)

| # | Von | Betreff |
|---|-----|---------|
| 5 | spam@random.com | Gewinnspiel |

---

**Vorgeschlagene Aktionen:**
- [ ] Email #1: Termin "Meeting" für morgen anlegen
- [ ] Emails #3-4: In Archiv-Ordner verschieben
- [ ] Email #5: Löschen

Soll ich diese Aktionen ausführen?
```

### Phase 4: Ausführung

Nach Bestätigung durch User:

```javascript
// Einzelne Email verschieben
imap_move_email({
  account: "onecom",
  sourceFolder: "INBOX",
  uid: 12345,
  targetFolder: "INBOX._archiv.newsletter"
})

// Mehrere Emails verschieben
imap_bulk_move({
  account: "onecom",
  sourceFolder: "INBOX",
  uids: [12345, 12346, 12347],
  targetFolder: "INBOX._archiv.admin"
})
```

---

## Aktionstypen

### 1. Termin-Erkennung

**Signale:**
- Datum im Betreff/Inhalt
- Uhrzeit-Muster (10:00, 10 Uhr)
- Keywords: meeting, termin, einladung

**Output:**
```markdown
📅 **Termin erkannt:**
- Was: [Betreff/Thema]
- Wann: [Datum/Uhrzeit wenn erkennbar]
- Mit: [Absender/Teilnehmer]

→ Termin in Teams-Kalender eintragen? (via teams MCP: calendar_create_event)
```

### 2. Rechnungs-Erkennung

**Signale:**
- Keywords: rechnung, invoice, zahlung
- Beträge (€, EUR)
- Fälligkeitsdatum

**Output:**
```markdown
💰 **Rechnung erkannt:**
- Von: [Absender]
- Betreff: [Betreff]
- Betrag: [wenn erkennbar]
- Fällig: [wenn erkennbar]

→ Prüfen und nach `_archiv.rechnung` verschieben?
```

### 3. Admin/Wichtig-Erkennung

**Signale:**
- Kontobenachrichtigungen
- Vertragsänderungen
- Passwort-Resets
- Offizieller Absender

**Output:**
```markdown
📁 **Administrative Email:**
- Von: [Absender]
- Typ: [Kontomeldung/Vertrag/etc.]

→ Nach `_archiv.admin` verschieben?
```

### 4. Newsletter-Erkennung

**Signale:**
- "Newsletter" im Betreff/Absender
- Unsubscribe-Link
- Marketing-Absender
- Regelmäßige Frequenz

**Output:**
```markdown
📰 **Newsletter:**
- Von: [Absender]
- Interessant: [Ja/Nein basierend auf Historie]

→ Lesen und archivieren oder direkt archivieren?
```

---

## Ordner-Struktur (one.com)

```
INBOX/
├── _archiv/
│   ├── admin/          # Konten, Verträge, Passwörter
│   ├── newsletter/     # Newsletter zum Lesen
│   ├── rechnung/       # Rechnungen, Zahlungen
│   ├── termin/         # Terminbestätigungen
│   └── wichtig/        # Sonstiges Wichtiges
├── Sent/
├── Drafts/
├── Spam/
└── Trash/
```

---

## Beispiel-Session

**User:** "Was ist in meinen Emails los?"

**Claude:**

1. Emails abrufen:
```javascript
imap_list_emails({ account: "onecom", folder: "INBOX", limit: 20, criteria: "UNSEEN" })
```

2. Analyse erstellen:

```markdown
## Inbox-Analyse: onecom

Du hast **8 ungelesene Emails**.

### Erfordert Handlung (2)

| Von | Betreff | Aktion |
|-----|---------|--------|
| chef@firma.de | Meeting Freitag 14 Uhr | 📅 Termin anlegen |
| amazon.de | Ihre Rechnung #123 | 💰 Prüfen |

### Zum Archivieren (4)

| Von | Betreff | → Ordner |
|-----|---------|----------|
| bank.de | Kontoauszug Januar | admin |
| spotify.com | Zahlungsbestätigung | rechnung |
| newsletter@tech.de | Tech-News #42 | newsletter |
| support@service.de | Ticket geschlossen | admin |

### Werbung/Spam (2)

| Von | Betreff |
|-----|---------|
| promo@shop.xyz | 50% RABATT!!! |
| win@lottery.com | Sie haben gewonnen |

---

**Empfohlene Aktionen:**
1. Termin "Meeting" für Freitag 14 Uhr anlegen
2. Amazon-Rechnung prüfen, dann archivieren
3. 4 Emails in Archiv-Ordner verschieben
4. 2 Spam-Emails löschen

Soll ich die Archivierung und Löschung durchführen?
```

3. Nach Bestätigung:
```javascript
imap_bulk_move({
  account: "onecom",
  sourceFolder: "INBOX",
  uids: [101, 102],  // bank.de, support
  targetFolder: "INBOX._archiv.admin"
})
// ... weitere Moves
```

---

## Konfiguration

### Sensitivität anpassen

```javascript
// Konservativ: Nur eindeutige Fälle auto-archivieren
const AUTO_ARCHIVE_CONFIDENCE = 0.9;

// Aggressiv: Auch unsichere Fälle vorschlagen
const AUTO_ARCHIVE_CONFIDENCE = 0.6;
```

### Absender-Whitelists

```javascript
// Diese Absender nie automatisch archivieren
const WHITELIST = [
  '@firma.de',
  '@schule.de',
  'familie@'
];

// Diese Absender immer als Newsletter behandeln
const NEWSLETTER_DOMAINS = [
  'newsletter@',
  'noreply@',
  'marketing@'
];
```

---

## Best Practices

### Do

- Immer Zusammenfassung zeigen vor Bulk-Aktionen
- Persönliche Emails (Familie, Freunde) nie auto-archivieren
- Bei Unsicherheit nachfragen statt handeln
- Rechnungen nur nach Prüfung archivieren

### Don't

- Emails löschen ohne explizite Bestätigung
- Alle Newsletter als Spam behandeln
- Aktionen ohne Überblick ausführen
- Sensible Emails (Bank, Verträge) ignorieren

---

## Fehlerbehandlung

### "Folder not found"
```
→ imap_list_folders aufrufen
→ Ordner-Pfad prüfen (INBOX._archiv vs INBOX/Archiv)
```

### "Email already moved"
```
→ Email wurde bereits verarbeitet
→ Inbox neu laden
```

---

## Verwandte Skills

- **email-send**: Auf wichtige Emails antworten
- **weekly-digest**: Wochenübersicht der Email-Aktivität

---

*Zuletzt aktualisiert: 12.03.2026*
*Version: 1.1 — MCP-Prefixes gefixt, Teams-Kalender hinzugefuegt*
