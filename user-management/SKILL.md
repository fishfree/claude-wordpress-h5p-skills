---
name: user-management
description: Use when managing existing user accounts across school systems - adding single students ("Nachzügler"), deleting users, password resets, class changes. Triggers on "Nachzügler", "User löschen", "Passwort zurücksetzen", "Klassenwechsel", "einzelnen Schüler anlegen".
---

# User Management

## Overview

Handles individual user operations across the three school systems (Azure/MS365, Moodle, VCE). Unlike `user-import-prepare` (bulk class imports), this skill handles single-user or small-group changes.

## When to Use

- Single student needs to be added mid-semester ("Nachzügler")
- Students need to be deleted (leaving school, end of year)
- Password reset lists needed
- Student changes class ("Klassenwechsel")
- NOT for bulk class imports → use `user-import-prepare`

## Operations

### 1. Nachzügler (Single Student Add)

Same rules as `user-import-prepare`, but for one or few students.

**Input:** Vorname, Nachname, Geburtsdatum, Klasse
**Output:** Append-ready lines for each system's existing CSV or new mini-CSVs

Ask user: To which existing files should the student be appended, or should new files be created?

**Azure:** Kann direkt per PowerShell (`New-MgUser`) angelegt werden.

**VCE: NIEMALS per LDAP anlegen! IMMER über CSV-Import der VCE-Weboberfläche!**
Grund: Manuell per LDAP angelegte User haben keine Home-Verzeichnisse, falsche ACLs und fehlende Attribute (`ndshomedirectory`, korrekte `vCEXprops`-Struktur). Nur der VCE-Import erstellt alles korrekt.
Workflow:
1. VCE-CSV generieren (Format: `431;Nachname;Vorname;Klasse;Geburtsdatum;Hamburg;SchülerIn`)
2. CSV über VCE-Weboberfläche importieren (Benutzerverwaltung → Import)
3. Login testen

**Moodle:** CSV generieren und über Moodle-Admin importieren.

### 2. User Deletion

## KRITISCHE SICHERHEITSREGELN FÜR LÖSCHUNGEN

**Diese Regeln sind NICHT VERHANDELBAR. Keine Ausnahmen.**

1. **IMMER Dry-Run zuerst.** Vor jeder Löschung MUSS ein Dry-Run ausgeführt werden. Die Ergebnisse MÜSSEN dem User gezeigt und bestätigt werden, bevor die eigentliche Löschung erfolgt.

2. **NIEMALS Wildcard-Suche bei Löschungen.** Nachnamen wie "Amiri" können mehrfach vorkommen. IMMER exakt nach CN/Anmeldename oder UPN identifizieren, NIEMALS nach Nachname mit Wildcard (`sn=Name*`).

3. **Jeden einzelnen Treffer verifizieren.** Vor dem Löschen: Vorname, Nachname, Klasse und Geburtsdatum anzeigen. Nur löschen wenn ALLE Felder zum gewünschten User passen.

4. **Systemübergreifend prüfen.** Bevor ein User in einem System gelöscht wird: Prüfen ob der Name auch in anderen Systemen existiert und ob es sich um denselben User handelt (gleicher Vorname + Nachname + Geburtsdatum).

5. **Reihenfolge bei systemübergreifender Löschung:**
   - Erst Dry-Run in allen Systemen
   - Ergebnisse dem User zeigen
   - Explizite Bestätigung einholen
   - Dann löschen

| Gedanke | Realität |
|---------|----------|
| "Der Nachname ist eindeutig" | Nachnamen kommen mehrfach vor. IMMER nach CN/UPN suchen. |
| "Ich kann nach Nachname suchen und dann filtern" | NEIN. Suche exakt. Wildcards + Löschung = Datenverlust. |
| "Das ist nur ein User, Dry-Run brauche ich nicht" | DOCH. Auch bei einem einzigen User. Immer. |
| "Der User soll sowieso gelöscht werden" | Prüfe trotzdem ob es der RICHTIGE User ist. |

---

**Needed info:** Exakter CN/Anmeldename ODER UPN des Users. Bei Angabe nur per Name: erst suchen, anzeigen, bestätigen lassen.

**Azure:**
```powershell
# IMMER erst prüfen:
Get-MgUser -UserId "vorname.nachname@bs32.de" | Select DisplayName,JobTitle,Department,AccountEnabled

# Dann löschen:
Remove-MgUser -UserId "vorname.nachname@bs32.de"
```

**Moodle:** Create CSV for Moodle user deletion (admin upload)
```
username;deleted
schaeferju;1
```

**VCE: Direkt per LDAP löschen!**

Script: `vce_delete.ps1` im UserAnlegen-Verzeichnis.

```powershell
# IMMER ZUERST DRY-RUN:
.\vce_delete.ps1 -Name "SchaeferAle" -DryRun

# Erst nach Bestätigung wirklich löschen:
.\vce_delete.ps1 -Name "SchaeferAle"

# Ganze Klasse - IMMER Dry-Run zuerst:
.\vce_delete.ps1 -Klasse "AVM2303" -DryRun
.\vce_delete.ps1 -Klasse "AVM2303"

# CSV-Liste löschen (Spalte: CN/Anmeldename)
.\vce_delete.ps1 -CsvFile "delete_list.csv" -DryRun
.\vce_delete.ps1 -CsvFile "delete_list.csv"
```

**WICHTIG:** Das `-Name` Argument ist der **exakte CN/Anmeldename** (z.B. `SchaeferAle`), NICHT der Nachname! Das Script sucht exakt nach diesem CN.

LDAP-Verbindung: `10.32.100.252:389`, Bind-DN: `cn=Admin,ou=Adm,o=CL`
Jede Löschung wird in `vce_delete_YYYY-MM-DD_HHmmss.log` protokolliert.

**Archival:** Move deleted user data to `wdhgeloescht/` folder with date.

### 3. Password Reset

**Azure:**
```powershell
# Reset to default password
Update-MgUser -UserId "user@bs32.de" -PasswordProfile @{Password="BS05_2025"; ForceChangePasswordNextSignIn=$true}
```

**Moodle:** CSV with password field:
```
username;password
schaeferju;BS05_2025
```

**VCE:** Password = Geburtsdatum ohne Punkte (z.B. `12092006`). Manuell im VCE-Admin zurücksetzen.

### 4. Klassenwechsel

Student moves from one class to another. Affects:

| System | Was ändert sich |
|--------|----------------|
| Azure | JobTitle (= Klasse), Security Group (alt entfernen, neu hinzufügen) |
| Moodle | cohort2 (neue Klasse), ggf. course1 |
| VCE | Klasse-Feld in der CSV |

**Workflow:**
1. Alte Klasse und neue Klasse erfragen
2. Für jedes System die nötigen Änderungen generieren
3. Azure: PowerShell-Befehle für Gruppen-Update
4. Moodle: Update-CSV mit neuer Kohorte
5. VCE: Neue CSV-Zeile mit neuer Klasse

## File Locations

Base: `C:\Users\mail\OneDrive - Berufliche Schule City Süd (H9)\Dokumente\schule\Verwaltung\UserAnlegen\`

| Ordner | System |
|--------|--------|
| `azure/` | MS365/Azure |
| `moodle/` | Moodle |
| `vce/` | VCE |
| `wdhgeloescht/` | Gelöschte User (Archiv) |

## Common Mistakes

| Fehler | Lösung |
|--------|--------|
| **Wildcard-Löschung nach Nachname** | **NIEMALS. Immer exakt nach CN/UPN. Nachnamen sind nicht eindeutig!** |
| **Löschung ohne Dry-Run** | **IMMER erst Dry-Run, Ergebnis zeigen, bestätigen lassen** |
| Nachzügler nur in einem System angelegt | Immer alle drei Systeme bedienen |
| Gelöschte User nicht archiviert | Immer nach `wdhgeloescht/` kopieren |
| VCE-Passwort vergessen mitzuteilen | Hinweis: Geburtsdatum ohne Punkte |
| Klassenwechsel ohne Gruppen-Update | Azure Security Group muss auch geändert werden |
| LDAP-Suche nach Nachname statt CN | Nachnamen wie Amiri, Müller etc. kommen mehrfach vor |
| Löschung ohne Gegenprüfung in anderen Systemen | Vor Löschung immer prüfen ob User in allen Systemen korrekt identifiziert |
