$(sed -n '1,200p' <<'TXT'
Recommended environment
- Python 3.10+ (3.12 tested)
- GPU recommended for heavy model work

Core packages
- torch, transformers, fastapi, uvicorn, requests, aiohttp, stix2, taxii2-client, pymisp, pandas, scikit-learn
TXT
)
