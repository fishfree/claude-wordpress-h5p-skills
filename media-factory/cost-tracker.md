# Media Factory Cost Tracker

## Purpose

Track spending on paid API generators (Nano Banana, Veo 3.1, HeyGen) to prevent surprise bills.

## Cost Log

File: `_assets/media-factory/cost-log.jsonl`
Format: One JSON object per line (JSONL).

```jsonl
{"date":"2026-03-12","generator":"ai-image","model":"gemini-3-pro-image-preview","cost":0.13,"prompt":"Cannabis trichome illustration","project":"cannabis-kultur"}
{"date":"2026-03-12","generator":"ai-video","model":"veo-3.1-fast","cost":1.20,"prompt":"Stecklinge cutting process 8s","project":"stecklingsmeister"}
```

## Reading the Log

Show month-to-date total at the start of any paid generation:

```bash
# Month-to-date total
MONTH=$(date +%Y-%m)
grep "\"date\":\"$MONTH" _assets/media-factory/cost-log.jsonl 2>/dev/null | \
  python3 -c "import sys,json; lines=[json.loads(l) for l in sys.stdin]; print(f'Monat: ${sum(l[\"cost\"] for l in lines):.2f} USD ({len(lines)} Generierungen)')" \
  2>/dev/null || echo "Noch keine Kosten diesen Monat."
```

## Budget Limit

If `_assets/media-factory/config.json` has `"monthlyBudgetLimit"` set (not null):
- Check before each paid generation
- If limit would be exceeded → warn user and ask for confirmation
- Format: "Monatsbudget: $X.XX / $LIMIT. Diese Generierung ($Y.YY) würde das Limit überschreiten. Trotzdem fortfahren?"

## Confirmation Template

Before every paid API call, show:

```
Kostenpflichtige Generierung:
  Generator: [NAME]
  Modell: [MODEL]
  Geschätzte Kosten: ~$[COST]
  Monatsausgaben bisher: $[MTD]

Generieren? (j/n)
```

Wait for explicit "j" or "ja" before proceeding.
