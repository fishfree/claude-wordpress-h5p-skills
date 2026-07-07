---
name: email-send
description: Compose and send emails via SMTP through the IMAP MCP server. Supports drafting, review, and sending with templates for common email types. Use when the user wants to write or send an email.
license: MIT
allowed-tools:
  - mcp__imap__smtp_send_email
  - mcp__imap__imap_list_accounts
---

# Email-Send Skill

Komfortable Email-Erstellung mit Review-Workflow und SMTP-Versand über den IMAP MCP Server.

## MCP/Tool Integration

**Dieser Skill nutzt folgende Tools:**

| Tool | Zweck |
|------|-------|
| `smtp_send_email` | Email über SMTP versenden |
| `imap_list_accounts` | Verfügbare Email-Accounts anzeigen |

**Verfügbare Accounts:**

| Account-Key | Email | Verwendung |
|-------------|-------|------------|
| `onecom` | mail@dirk-schulenburg.net | Standard für private Emails |
| `gmx` | [konfiguriert] | Alternative |
| `gmail` | [konfiguriert] | Google-Services |

---

## Wann diesen Skill nutzen

- "Schreibe eine Email an [Empfänger]"
- "Sende eine Nachricht an [Person]"
- "Verfasse eine Email über [Thema]"
- "Antworte auf diese Email"
- "Schicke [Person] eine Erinnerung"

---

## Workflow

### Phase 1: Informationen sammeln

**Pflichtfelder:**
```
- Empfänger (to): Email-Adresse
- Betreff (subject): Kurze, aussagekräftige Betreffzeile
- Inhalt: Text der Email
```

**Optionale Felder:**
```
- CC: Weitere Empfänger (öffentlich)
- BCC: Weitere Empfänger (verdeckt)
- Reply-To: Abweichende Antwort-Adresse
- Account: onecom (default), gmx, oder gmail
- Format: text oder html
```

### Phase 2: Entwurf erstellen

**Entwurf-Struktur:**
```markdown
## Email-Entwurf

**An:** empfaenger@example.com
**CC:** -
**Betreff:** [Betreffzeile]
**Account:** onecom (mail@dirk-schulenburg.net)

---

[Email-Inhalt hier]

---

**Signatur:**
Mit freundlichen Grüßen
Dirk Schulenburg
```

### Phase 3: Review & Bestätigung

**WICHTIG:** Vor dem Versand IMMER den Entwurf zeigen und bestätigen lassen!

```
✅ Empfänger korrekt?
✅ Betreff aussagekräftig?
✅ Inhalt vollständig?
✅ Ton angemessen?
✅ Keine sensiblen Daten?
```

**Frage den User:**
> "Soll ich diese Email so versenden? (Ja/Nein/Ändern)"

### Phase 4: Versand

**MCP Tool-Aufruf:**
```javascript
smtp_send_email({
  account: "onecom",
  to: "empfaenger@example.com",
  subject: "Betreffzeile",
  text: "Email-Inhalt als Plain Text",
  html: "<p>Optional: HTML-Version</p>",  // optional
  cc: "cc@example.com",  // optional
  bcc: "bcc@example.com",  // optional
  replyTo: "other@example.com"  // optional
})
```

**Erfolgsmeldung:**
```
✅ Email erfolgreich versendet!
- Empfänger: empfaenger@example.com
- Betreff: [Betreffzeile]
- Message-ID: [ID vom Server]
```

---

## Email-Templates

### Formelle Anfrage

```
Betreff: Anfrage bezüglich [Thema]

Sehr geehrte(r) [Anrede] [Name],

ich wende mich an Sie bezüglich [Thema/Anliegen].

[Hauptinhalt: Was wird angefragt/benötigt]

[Optional: Hintergrund/Kontext]

Für Rückfragen stehe ich gerne zur Verfügung.

Mit freundlichen Grüßen
Dirk Schulenburg
```

### Informelle Nachricht

```
Betreff: [Thema]

Hallo [Name],

[Inhalt der Nachricht]

Viele Grüße
Dirk
```

### Erinnerung/Follow-up

```
Betreff: Erinnerung: [Ursprüngliches Thema]

Hallo [Name],

ich möchte kurz an [Thema/Termin/Aufgabe] erinnern.

[Details zur Erinnerung]

[Optional: Deadline oder nächste Schritte]

Viele Grüße
Dirk
```

### Terminvorschlag

```
Betreff: Terminvorschlag: [Thema des Meetings]

Hallo [Name],

ich würde gerne einen Termin für [Thema] vereinbaren.

Folgende Zeiten wären möglich:
- [Datum 1], [Uhrzeit]
- [Datum 2], [Uhrzeit]
- [Datum 3], [Uhrzeit]

[Optional: Agenda-Punkte]

Bitte gib Bescheid, welcher Termin passt.

Viele Grüße
Dirk
```

### Danksagung

```
Betreff: Danke für [Anlass]

Hallo [Name],

vielen Dank für [Grund der Danksagung].

[Optional: Spezifische Erwähnung was besonders geschätzt wurde]

Viele Grüße
Dirk
```

---

## Best Practices

### Do

- Immer Entwurf zur Review zeigen vor dem Versand
- Betreffzeile kurz und aussagekräftig halten
- Bei formellen Emails: Vollständige Anrede und Grußformel
- Sensible Informationen vermeiden (Passwörter, etc.)
- Bei Unsicherheit nachfragen (Ton, Empfänger, etc.)

### Don't

- Emails versenden ohne explizite Bestätigung
- Lange Betreffzeilen (max. 50-60 Zeichen)
- "Re:" oder "Fwd:" im Betreff bei neuen Emails
- HTML-Formatierung wenn Plain Text reicht
- Mehrere Themen in einer Email vermischen

---

## Account-Auswahl

| Kontext | Empfohlener Account |
|---------|---------------------|
| Private Kommunikation | `onecom` |
| Schulkontakte | `onecom` |
| Google-bezogen | `gmail` |
| Fallback | `gmx` |

---

## Fehlerbehandlung

### "Account not configured"
```
→ Account-Key prüfen: onecom, gmx, gmail
→ Alternativ: imap_list_accounts aufrufen für verfügbare Accounts
```

### "SMTP connection failed"
```
→ Server-Status prüfen: https://mcp-imap.dirk-schulenburg.net/health
→ Port-Blockierung auf Server? (465 für SSL)
```

### "Invalid email address"
```
→ Email-Format prüfen: name@domain.tld
→ Tippfehler in der Adresse?
```

---

## Beispiel-Workflow

**User:** "Schreibe eine Email an max@example.com und erinnere ihn an unser Meeting morgen"

**Claude:**
1. Informationen sammeln:
   - To: max@example.com
   - Betreff: "Erinnerung: Meeting morgen"
   - Template: Erinnerung/Follow-up

2. Entwurf erstellen:
```
## Email-Entwurf

**An:** max@example.com
**Betreff:** Erinnerung: Meeting morgen
**Account:** onecom (mail@dirk-schulenburg.net)

---

Hallo Max,

ich möchte kurz an unser Meeting morgen erinnern.

Viele Grüße
Dirk

---
```

3. Bestätigung einholen:
> "Soll ich diese Email so versenden?"

4. Nach Bestätigung: `smtp_send_email` aufrufen

5. Erfolgsmeldung:
> "✅ Email erfolgreich an max@example.com versendet!"

---

## Verwandte Skills

- **recherche-workflow**: Informationen sammeln vor dem Schreiben
- **blog-article-workflow**: Längere Texte strukturieren

---

*Zuletzt aktualisiert: 12.03.2026*
*Version: 1.1 - Fixed MCP tool prefix (mcp__imap__ statt mcp__MCP_DOCKER__)*
