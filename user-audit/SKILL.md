---
name: user-audit
description: Use when comparing user lists across school systems to find inconsistencies - students missing in one system, orphaned accounts, duplicates. Triggers on "User abgleichen", "Audit", "wer fehlt", "Systeme vergleichen", "Inkonsistenzen finden", "aufräumen".
---

# User Audit

## Overview

Compares user data across Azure/MS365, Moodle, and VCE to find inconsistencies: missing users, orphaned accounts, duplicates, and class mismatches. Produces an actionable report.

## When to Use

- Regular audit (e.g., start/end of semester)
- Suspicion that users are missing in one system
- Before bulk deletion (end of school year cleanup)
- After migration or system changes
- NOT for creating users → use `user-import-prepare`
- NOT for single-user changes → use `user-management`

## Data Sources

### VCE: Live LDAP-Abfrage (automatisch)

VCE-Daten werden **direkt per LDAP** aus dem eDirectory abgefragt - kein manueller Export nötig.

**LDAP-Verbindung:**
- Server: `10.32.100.252:389`
- Bind-DN: `cn=Admin,ou=Adm,o=CL`
- Passwort: `vCE_2021#`
- Tree: `LANDWEHR-TREE` (NetIQ eDirectory 9.2.9)

**Schüler-Daten:**
- Base-DN: `ou=Schueler,ou=BS32,ou=Unterricht,o=CL`
- Filter: `(objectClass=inetOrgPerson)`
- Paged Search erforderlich (>800 Einträge)

**Relevante LDAP-Attribute:**

| Attribut | Inhalt | Beispiel |
|----------|--------|----------|
| `sn` | Nachname | Abdalla |
| `givenName` | Vorname | Rickard |
| `cn` / `uid` | Anmeldename | AbdallaRic |
| `vCEtype` | User-Typ (431=Schüler) | 431 |
| `groupMembership` | Klasse (DN-Format) | `cn=TE2401,ou=Klassen,ou=BS32,ou=Unterricht,o=CL` |
| `vCEXprops` | Geburtsdatum etc. | `DoB=16.11.1998` |

**Klasse extrahieren:** Aus `groupMembership` per Regex: `cn=([^,]+),ou=Klassen` → Klasse
**Geburtsdatum extrahieren:** Aus `vCEXprops` per Regex: `DoB=(\d{2}\.\d{2}\.\d{4})` → Datum

**Export-Script:** `vce_export.ps1` im UserAnlegen-Verzeichnis. Erzeugt `vce_export_YYYY-MM-DD.csv`.

**Klassenstruktur im LDAP:**
- `ou=Klassen,ou=BS32,ou=Unterricht,o=CL` - Alle Klassen als Gruppen
- `ou=Lehrer,ou=BS32,ou=Unterricht,o=CL` - Lehrkräfte
- `ou=Administratoren,ou=BS32,ou=Unterricht,o=CL` - Admins (vceAdmin, schuAdmin)

### Azure/MS365: CSV oder PowerShell

CSV-Export aus Azure Portal oder PowerShell:
```powershell
Get-MgUser -Filter "Department eq 'Schüler'" -All | Select DisplayName,UserPrincipalName,JobTitle,Department
```
Typischer Speicherort: `azure/`

### Moodle: CSV-Export

CSV-Export aus Moodle Admin (Nutzer/Bulk-Aktionen).
Typischer Speicherort: `moodle/`

## Matching Strategy

Users across systems are matched by **normalized name** since usernames differ per system.

### Normalization Steps:
1. Lowercase
2. Apply character replacement (ä→ae, ö→oe, ü→ue, ß→ss, etc.)
3. Remove spaces and hyphens
4. Result: `juergenschaefer` matches across all systems

### Match by:
- **Primary:** Normalized Vorname + Nachname
- **Secondary:** Geburtsdatum (to resolve same-name conflicts)
- **Tertiary:** Klasse (additional confirmation)

## Report Structure

Generate a markdown report with these sections:

### 1. Summary
```
Geprüfte Systeme: Azure, Moodle, VCE
Datum: [today]
Azure-User: 245
Moodle-User: 238
VCE-User: 898
```

### 2. Missing Users (per system)

| Name | Klasse | Vorhanden in | Fehlt in |
|------|--------|-------------|----------|
| Max Müller | BG2414 | Azure, VCE | Moodle |

### 3. Orphaned Accounts
Users that exist in a system but not in any source list (possible former students).

### 4. Class Mismatches
Same user, different class assignment across systems.

### 5. Duplicate Detection
Users with very similar names that might be duplicates or data entry errors.

### 6. Recommended Actions
Concrete steps to fix each issue found:
- "Add Max Müller to Moodle (use `user-management` skill)"
- "Remove orphaned account hans.meier@bs32.de from Azure"
- "Verify: Is 'Schäfer, Alexej' in BG2414 (Azure) or BG2514 (VCE)?"

## Output

Save report as: `UserAnlegen/audit_[YYYY-MM-DD].md`

## Common Mistakes

| Fehler | Lösung |
|--------|--------|
| Umlaut-Mismatch beim Vergleich | Immer normalisieren vor Vergleich |
| Lehrer in Schüler-Audit | Separat behandeln oder explizit ausschließen |
| LDAP nicht erreichbar | Nur im Schulnetz (10.32.x.x), Server: 10.32.100.252 |
| VCE-Schüler ohne Klasse | Prüfen ob Altlasten, ggf. löschen |
