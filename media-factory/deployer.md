# Media Factory Deployer

## Deploy Targets

### 1. dirk-schulenburg.net (SCP + nginx)

```bash
# Upload to website static assets
scp -i $SSH_KEY LOCAL_FILE $HETZNER_USER@$HETZNER_HOST:/home/dirk/docker/website/public/media/FILENAME
```

After upload, the file is available at: `https://dirk-schulenburg.net/media/FILENAME`

### 2. cannabis-kultur.online (WordPress MCP)

Use the EduGrow WordPress MCP tool:
```
mcp__claude_ai_MyWordPressMCP__wp_upload_media_base64(
  filename: "FILENAME",
  data: "BASE64_DATA",
  mime_type: "image/svg+xml" | "image/webp" | "audio/mpeg"
)
```

Returns: `{ id: MEDIA_ID, url: "https://cannabis-kultur.online/wp-content/uploads/..." }`

### 3. lernmodule.dirk-schulenburg.net (SCP + nginx)

```bash
# Upload to lernmodule static directory
scp -i $SSH_KEY LOCAL_FILE $HETZNER_USER@$HETZNER_HOST:/home/dirk/docker/lernmodule/html/assets/FILENAME
```

After upload: `https://lernmodule.dirk-schulenburg.net/assets/FILENAME`

### 4. Moodle (MCP)

For embedding in labels/pages — use the URL from targets 1-3 and embed via:
```html
<img src="URL" alt="DESCRIPTION" style="max-width:100%;height:auto;" />
```

Or for audio:
```html
<audio controls style="width:100%;max-width:500px;">
  <source src="URL" type="audio/mpeg" />
</audio>
```

### 5. Local file (default)

Save to: `_assets/media-factory/{PROJECT}/{TYPE}/FILENAME`

Always save locally first, then deploy to target.

## Metadata Sidecar

After every generation, write a JSON sidecar file next to the asset:

```bash
# Example: _assets/media-factory/cannabis-kultur/svg/trichome-infographic.json
cat > SIDECAR_PATH << 'EOF'
{
  "file": "trichome-infographic.svg",
  "generator": "svg-generator",
  "prompt": "Infographic showing cannabis trichome types",
  "project": "cannabis-kultur",
  "cost": 0,
  "date": "YYYY-MM-DD",
  "deployed_to": [],
  "urls": {}
}
EOF
```

Update `deployed_to` and `urls` after each successful deploy.

## File Size Validation

Before uploading, check:
- WordPress: max 50MB
- Moodle: max 20MB
- SVGs: validate no `<script>` tags (XSS prevention)

```bash
# Check SVG for scripts
grep -i '<script' FILE.svg && echo "WARNING: SVG contains scripts!" || echo "SVG clean"

# Check file size
stat --format=%s FILE  # Linux
```

## Cost Logging (Paid generators only)

Append to `_assets/media-factory/cost-log.jsonl`:
```bash
echo '{"date":"YYYY-MM-DD","generator":"GENERATOR","model":"MODEL","cost":COST,"prompt":"PROMPT_SUMMARY"}' >> _assets/media-factory/cost-log.jsonl
```
