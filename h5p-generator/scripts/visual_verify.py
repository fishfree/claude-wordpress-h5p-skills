#!/usr/bin/env python3
"""
Visual Verification for H5P Files

Wrapper around visual_verify.mjs that integrates with the H5P System.
Runs Puppeteer-based verification and returns structured results.

Usage:
    from visual_verify import verify_h5p, VerifyResult

    result = verify_h5p("path/to/file.h5p")
    if result.success:
        print(f"Screenshot: {result.screenshot}")
    else:
        print(f"Issues: {result.failed_checks}")
"""

import json
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class VerifyCheck:
    """Einzelne Verifikations-Pruefung"""
    name: str
    passed: bool
    message: str

    def __str__(self):
        status = "OK" if self.passed else "FAIL"
        return f"[{status}] {self.name}: {self.message}"


@dataclass
class VerifyResult:
    """Ergebnis der visuellen Verifikation"""
    success: bool
    render_success: bool = False
    content_type: str = ""
    screenshot: Optional[Path] = None
    slide_screenshots: List[Path] = field(default_factory=list)
    checks: List[VerifyCheck] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def failed_checks(self) -> List[VerifyCheck]:
        return [c for c in self.checks if not c.passed]

    @property
    def passed_checks(self) -> List[VerifyCheck]:
        return [c for c in self.checks if c.passed]

    def __str__(self):
        if self.success:
            return f"[VERIFY OK] {self.content_type}: {len(self.checks)} checks passed"
        failed = len(self.failed_checks)
        return f"[VERIFY FAIL] {self.content_type}: {failed} check(s) failed"

    def summary(self) -> str:
        lines = [f"Visual Verification: {'OK' if self.success else 'FAILED'}"]
        lines.append(f"  Content Type: {self.content_type}")
        lines.append(f"  Render: {'OK' if self.render_success else 'FAILED'}")
        for check in self.checks:
            lines.append(f"  {check}")
        if self.screenshot:
            lines.append(f"  Screenshot: {self.screenshot}")
        if self.error:
            lines.append(f"  Error: {self.error}")
        return "\n".join(lines)


# Pfad zum Node.js Script
VERIFY_SCRIPT = Path(__file__).parent / "visual_verify.mjs"


def verify_h5p(
    h5p_path: str | Path,
    output_dir: str | Path = None,
    port: int = 8090,
    timeout: int = 60
) -> VerifyResult:
    """
    Verifiziert eine H5P-Datei visuell.

    Args:
        h5p_path: Pfad zur H5P-Datei
        output_dir: Verzeichnis fuer Screenshots (default: neben H5P-Datei)
        port: Port fuer den temporaeren HTTP-Server
        timeout: Timeout in Sekunden

    Returns:
        VerifyResult mit Screenshot und Pruefergebnissen
    """
    h5p_path = Path(h5p_path)

    if not h5p_path.exists():
        return VerifyResult(
            success=False,
            error=f"H5P-Datei nicht gefunden: {h5p_path}"
        )

    if not VERIFY_SCRIPT.exists():
        return VerifyResult(
            success=False,
            error=f"Verify-Script nicht gefunden: {VERIFY_SCRIPT}"
        )

    # Node.js Command aufbauen
    cmd = ["node", str(VERIFY_SCRIPT), str(h5p_path)]

    if output_dir:
        cmd.extend(["--output-dir", str(output_dir)])
    cmd.extend(["--port", str(port)])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(VERIFY_SCRIPT.parent)
        )

        if result.returncode not in (0, 1):
            # Script-Fehler (nicht nur Test-Failure)
            error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
            return VerifyResult(
                success=False,
                error=f"Verify-Script Fehler: {error_msg}"
            )

        # JSON-Result parsen
        try:
            data = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            return VerifyResult(
                success=False,
                error=f"Ungueltige JSON-Ausgabe: {result.stdout[:200]}"
            )

        # In VerifyResult konvertieren
        checks = []
        for check in data.get('checks', []):
            checks.append(VerifyCheck(
                name=check.get('name', ''),
                passed=check.get('passed', False),
                message=check.get('message', '')
            ))

        screenshot = data.get('screenshot')
        slide_screenshots = [Path(s) for s in data.get('slideScreenshots', [])]

        return VerifyResult(
            success=data.get('success', False),
            render_success=data.get('renderSuccess', False),
            content_type=data.get('contentType', ''),
            screenshot=Path(screenshot) if screenshot else None,
            slide_screenshots=slide_screenshots,
            checks=checks,
            error=data.get('error')
        )

    except subprocess.TimeoutExpired:
        return VerifyResult(
            success=False,
            error=f"Timeout nach {timeout}s"
        )
    except FileNotFoundError:
        return VerifyResult(
            success=False,
            error="Node.js nicht gefunden. Bitte Node.js installieren."
        )
    except Exception as e:
        return VerifyResult(
            success=False,
            error=f"Verifikation fehlgeschlagen: {e}"
        )


def verify_batch(
    h5p_files: List[str | Path],
    output_dir: str | Path = None,
    port: int = 8090
) -> List[VerifyResult]:
    """
    Verifiziert mehrere H5P-Dateien.

    Args:
        h5p_files: Liste von H5P-Dateipfaden
        output_dir: Verzeichnis fuer Screenshots
        port: Startport (wird inkrementiert)

    Returns:
        Liste von VerifyResults
    """
    results = []
    for i, h5p_path in enumerate(h5p_files):
        result = verify_h5p(h5p_path, output_dir, port + i)
        results.append(result)
    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python visual_verify.py <path-to-h5p-file>")
        sys.exit(1)

    h5p_path = sys.argv[1]
    result = verify_h5p(h5p_path)
    print(result.summary())
    sys.exit(0 if result.success else 1)
