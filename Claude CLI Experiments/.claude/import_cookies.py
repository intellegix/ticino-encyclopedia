#!/usr/bin/env python3
"""
Import Perplexity cookies from browser DevTools export
"""
import json
from pathlib import Path
from datetime import datetime

# Paste your cookies here (I'll update this with your actual cookies)
COOKIES_RAW = """
__cf_bm    0KwEDncUPqvJBZSfZUwbxYVAKKO3K2ufrQhpCPrCmtI-1761771538-1.0.1.1-oEsnX9p0_xY_jZsUyp.fXERZVUPIkJUFYTST4jpV9AqkoOz76E4RYAlSoUxZM5tP16DGWZ1ST0R7whePqcj7_UTruoy3JB8HaBNjHHEGi.M    .perplexity.ai    /    2025-10-29T21:28:58.046Z    177    ✓    ✓    None            Medium
__cflb    02DiuDyvFMmK5p9jVbVnMNSKYZhUL9aGmrUwE8SkgQgkc    www.perplexity.ai    /    2025-10-30T17:03:46.648Z    51    ✓    ✓    None            Medium
__ps_fva    1761761066002    .perplexity.ai    /    2026-10-29T18:04:26.000Z    21        ✓    None            Medium
__ps_lu    https://www.perplexity.ai/?login-source=floatingSignup&login-new=false    .perplexity.ai    /    2026-10-29T18:04:26.000Z    77        ✓    None            Medium
__ps_r    https://accounts.youtube.com/    .perplexity.ai    /    2026-10-29T18:04:26.000Z    35        ✓    None            Medium
__Secure-next-auth.session-token    eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..EH2WPxhK_WhKdMJv.TG5yUFRWLdGvbwFgiFWYC4PaMxdw09oej_97tcU3qED6p2aa8g8I3Mrliuua0L8mFYv_u-S1k2MnvCOrj0z6rKiqHxydiw1F9YkXJatY7HOzV-sMNWQT3Z_MdvZXDuaqqPLYQGvAyVe4cpV-HWJahF96ME0pR2Ot-uoCd25gkHxfrlvtmV-OkIFfLNLZvx_XLeqRE7gdyd4r7gEolebYxpE41yIQ-BCJYVrWWC_nDa61476JGfGsqwMF5c1PE-XVCI2gBlKJ31aGZNxLyKfpnrwBe_k-U8W9RgcJf2_z0cg65eWAQiv_elJGWqtcVWCfq6Yi-9_ztl-5-oABBRUxvG26RGJq0xwpbUPS02LrC_dci8iR75Wr7q_KSmB0YwuOyfi3w6g5oeeWMJbUV9vAM-QgVFjSBwEQSp09A2dcjaEL6R0l0T__1uij1Wg.nS1m88Yf4rPk-Ki-DfFeCg    www.perplexity.ai    /    2025-11-28T20:58:58.305Z    556    ✓    ✓    Lax            Medium
_dd_s    aid=e2dc2820-4fc5-43ab-bb56-1dd62770e8db&rum=2&id=8c71b540-5cb7-4ce2-a1da-224d9ea265f6&created=1761771538187&expire=1761772442602&logs=0    www.perplexity.ai    /    2026-10-29T20:59:02.000Z    141            Strict            Medium
_fbp    fb.1.1761761066025.330115536653295060    .perplexity.ai    /    2026-01-27T18:50:20.000Z    41                        Medium
_rdt_em    :7fd829416d54dd606228cc4f26b8da5124ee179aa9b60c38102398f65f495796,c8cf6521c193fc743c7fadcd8be04e983724764efa65b3c3913b6d22f086a11f,6d885753a801f496c4a9752ce9ad2198a753f863a1b70e9505f1741010cb5228,6d885753a801f496c4a9752ce9ad2198a753f863a1b70e9505f1741010cb5228,6d885753a801f496c4a9752ce9ad2198a753f863a1b70e9505f1741010cb5228    .perplexity.ai    /    2026-01-27T18:50:20.000Z    332        ✓    Strict            Medium
_rdt_uuid    1761761065998.75ab8f9c-09c2-4059-9fa1-642b88d6e9c1    .perplexity.ai    /    2026-01-27T18:04:25.000Z    59        ✓    Strict            Medium
CF_AppSession    n08876811bf623bf2    pplx-next-static-public.perplexity.ai    /    2025-10-30T18:03:46.673Z    30    ✓    ✓                Medium
cf_clearance    _u2eeN_IYwA8TQzIRiS.31GW4O9Dco4edhtRQuOE6XQ-1761761026-1.2.1.1-Q7hqAQ5fbfj3KWR6WrJ9cij1AgtYVFr4DuwmOXiOcNcVxa38wpmnZ7wOlfLy6F0P9hFxK7CovxgA0T5nglCHfhFARgWa6NB40qc4BnsT86OBwbDgPanI29O2Qw1tc.L3y2l4z.udutGbUdyoQg3moygkqNHKtKhUxNV8p9_MCOTPInGbXGJHPdmwUcSxExKlKxZtps49K46c5kvqfAiHSFyBO3OC4KHCSAUgjTFE7Vs    .perplexity.ai    /    2026-10-29T18:03:46.826Z    310    ✓    ✓    None    https://perplexity.ai        Medium
g_state    {"i_l":0,"i_ll":1761761027554,"i_b":"2UbWzImBdg4ki10G/a4078m1b4tovRRYfvgi6KOzp4Q"}    www.perplexity.ai    /    2026-04-27T18:03:47.000Z    89                        Medium
gov-badge    3    www.perplexity.ai    /    2026-10-29T18:04:25.000Z    10                        Medium
next-auth.callback-url    https%3A%2F%2Fwww.perplexity.ai    www.perplexity.ai    /    Session    53        ✓    None            Medium
next-auth.csrf-token    ea10ed195196e90a5323c2072cd22ef3273c0f705d5dc933133ca26d04642604%7C139aa1fc508caa23364d91c664e7dff16182351951996c82f669a4413d0a38bf    www.perplexity.ai    /    Session    151    ✓    ✓    None            Medium
pplx.metadata    {%22qc%22:3%2C%22qcu%22:11678%2C%22qcm%22:4224%2C%22qcc%22:9102%2C%22qcco%22:0%2C%22qccol%22:0%2C%22qcdr%22:3%2C%22qcs%22:0%2C%22qcd%22:0%2C%22hli%22:true%2C%22hcga%22:false%2C%22hcds%22:false%2C%22hso%22:false%2C%22hfo%22:false%2C%22hsco%22:false%2C%22hfco%22:false%2C%22hsma%22:false%2C%22hdc%22:true%2C%22fqa%22:1761762240038%2C%22lqa%22:1761762946813}    www.perplexity.ai    /    2026-12-03T20:59:05.000Z    368                        Medium
pplx.search-models-v4    {%22research%22:%22pplx_alpha%22}    www.perplexity.ai    /    2026-12-03T18:22:17.000Z    54                        Medium
pplx.session-id    db630d5a-4064-4b82-99ff-a86652e436c7    www.perplexity.ai    /    Session    51                        Medium
pplx.source-selection-v3-space-    []    www.perplexity.ai    /    2025-11-05T18:31:47.000Z    33                        Medium
pplx.source-selection-v3-space-33504f94-0ba2-4e1b-8fd3-b38ea2a975e8    [%22web%22]    www.perplexity.ai    /    2025-11-05T18:33:39.000Z    78                        Medium
pplx.visitor-id    3bee32d6-d5f3-481c-af97-3f575f79836c    www.perplexity.ai    /    2026-10-22T19:57:34.000Z    51                        Medium
segmented-control-study    1    www.perplexity.ai    /    2026-10-29T18:04:26.000Z    24                        Medium
sidebar-upgrade-badge    2    www.perplexity.ai    /    2026-10-29T20:58:58.000Z    22                        Medium
sidebarHiddenHubs    []    www.perplexity.ai    /    2026-12-03T20:58:58.000Z    19                        Medium
"""

def parse_cookie_line(line):
    """Parse a single cookie line from DevTools export"""
    # Split by multiple spaces (2 or more)
    import re
    parts = [p.strip() for p in re.split(r'\s{2,}', line) if p.strip()]

    if len(parts) < 4:
        print(f"Skipping line (not enough parts): {line[:80]}...")
        return None

    name = parts[0]
    value = parts[1]
    domain = parts[2]
    path = parts[3]

    # Parse expiry (if present and not "Session")
    expires = -1
    if len(parts) > 4 and parts[4] != "Session":
        try:
            # Convert ISO date to Unix timestamp
            expiry_date = datetime.fromisoformat(parts[4].replace('Z', '+00:00'))
            expires = int(expiry_date.timestamp())
        except Exception:
            expires = -1

    # Parse HttpOnly and Secure flags
    httpOnly = False
    secure = False
    sameSite = "None"

    if len(parts) > 5:
        httpOnly = '✓' in parts[5]
    if len(parts) > 6:
        secure = '✓' in parts[6]
    if len(parts) > 7 and parts[7] and parts[7] != "None":
        sameSite = parts[7]

    cookie = {
        "name": name,
        "value": value,
        "domain": domain,
        "path": path,
        "expires": expires,
        "httpOnly": httpOnly,
        "secure": secure,
        "sameSite": sameSite if sameSite in ["Strict", "Lax", "None"] else "None"
    }

    return cookie

def main():
    print("Parsing cookies from DevTools export...")

    lines = [line.strip() for line in COOKIES_RAW.split('\n') if line.strip()]
    cookies = []

    for line in lines:
        cookie = parse_cookie_line(line)
        if cookie:
            cookies.append(cookie)

    print(f"\nParsed {len(cookies)} cookies")

    # Save to session file
    session_dir = Path(__file__).parent / "sessions"
    session_dir.mkdir(parents=True, exist_ok=True)

    cookies_file = session_dir / "perplexity_cookies.json"

    with open(cookies_file, 'w') as f:
        json.dump(cookies, f, indent=2)

    print(f"\n[SUCCESS] Cookies saved to: {cookies_file}")
    print(f"\nKey cookies found:")

    for cookie in cookies:
        if any(key in cookie['name'] for key in ['session-token', 'csrf', 'clearance']):
            print(f"  ✓ {cookie['name']}: {cookie['value'][:50]}...")

    # Also save session metadata
    session_meta = {
        "authenticated": True,
        "method": "manual_cookie_import",
        "last_updated": datetime.now().isoformat(),
        "cookies_count": len(cookies)
    }

    session_file = session_dir / "session_meta.json"
    with open(session_file, 'w') as f:
        json.dump(session_meta, f, indent=2)

    print(f"\n[SUCCESS] Session metadata saved to: {session_file}")
    print("\n[NEXT STEP] Test authentication with:")
    print("  .venv/Scripts/python.exe .claude/perplexity_bridge.py --check-auth")

if __name__ == "__main__":
    main()
