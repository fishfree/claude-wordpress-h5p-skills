@echo off
REM ========================================
REM Claude Skills Installation Script
REM ========================================
REM
REM Kopiert alle Skills in das Claude Desktop Skills-Verzeichnis.
REM Quellen (in Reihenfolge): claude-skills (Haupt-Repo), dann
REM claude-memory\skills (tagebuch, session-end u. a. leben dort).
REM Pro Skill wird die ERSTE gefundene Quelle mit SKILL.md genommen.
REM
REM Autor: Dirk
REM Aktualisiert: 24.06.2026 (zweite SOURCE_DIR claude-memory)
REM ========================================

echo.
echo ========================================
echo  Claude Skills Installation
echo ========================================
echo.

REM Definiere Pfade
set "SOURCE_DIR=C:\Users\mail\entwicklung\docker\claude-skills"
set "SOURCE_DIR_MEMORY=C:\Users\mail\entwicklung\claude-memory\skills"
set "TARGET_DIR=%APPDATA%\Claude\skills"

echo Source 1: %SOURCE_DIR%
echo Source 2: %SOURCE_DIR_MEMORY%
echo Target:   %TARGET_DIR%
echo.

REM Erstelle Target-Verzeichnis falls nicht vorhanden
if not exist "%TARGET_DIR%" (
    echo [INFO] Erstelle Skills-Verzeichnis: %TARGET_DIR%
    mkdir "%TARGET_DIR%"
    echo.
)

REM Liste aller Skills (nur Ordner mit SKILL.md)
echo Kopiere Skills...
echo.

REM DevOps Agent Skills
echo [DevOps Agent]
for %%S in (coding-agent debug-agent documentation-agent docker-management mcp-server-deploy mcp-key-manager n8n-workflow) do call :copyskill %%S
echo.

REM Education Agent Skills
echo [Education Agent]
for %%S in (bswi-infobrief h5p-designer h5p-generator h5p-wordpress-workflow lernfeld-zu-moodle-kurs moodle-course-workflow moodle-section-analyzer moodle-section-optimizer) do call :copyskill %%S
echo.

REM Personal Agent Skills
echo [Personal Agent]
for %%S in (blog-article-workflow recherche-workflow tagebuch session-end) do call :copyskill %%S
echo.

echo ========================================
echo  Installation abgeschlossen!
echo ========================================
echo.
echo Naechste Schritte:
echo.
echo 1. Claude Desktop KOMPLETT schliessen
echo    (auch im System Tray beenden!)
echo.
echo 2. Claude Desktop neu starten
echo.
echo Skills installiert in:
echo %TARGET_DIR%
echo.
echo ========================================
echo.
echo Druecke eine Taste zum Beenden...
pause >nul
exit /b 0

REM ========================================
REM Subroutine: copyskill ^<skill-name^>
REM Sucht den Skill zuerst in SOURCE_DIR, dann in SOURCE_DIR_MEMORY
REM und kopiert die erste Quelle mit SKILL.md.
REM ========================================
:copyskill
if exist "%SOURCE_DIR%\%~1\SKILL.md" (
    xcopy /E /I /Y "%SOURCE_DIR%\%~1" "%TARGET_DIR%\%~1" >nul 2>&1
    echo   [OK] %~1 ^(claude-skills^)
) else if exist "%SOURCE_DIR_MEMORY%\%~1\SKILL.md" (
    xcopy /E /I /Y "%SOURCE_DIR_MEMORY%\%~1" "%TARGET_DIR%\%~1" >nul 2>&1
    echo   [OK] %~1 ^(claude-memory^)
) else (
    echo   [--] %~1 ^(keine SKILL.md^)
)
goto :eof
