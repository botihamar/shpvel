"""Preflight check to avoid Telegram polling conflicts.

Contract:
- Reads BOT_TOKEN from environment (via dotenv like the rest of the project).
- Calls getMe and a single short long-poll getUpdates (timeout>0) to detect 409 Conflict.
- Exit codes:
  - 0: OK to start polling
  - 2: BOT_TOKEN missing/placeholder
  - 3: Telegram conflict detected (another instance polling)
  - 4: Other error
"""

from __future__ import annotations

import asyncio
import os
import sys

from dotenv import load_dotenv


def _is_placeholder_token(token: str) -> bool:
    t = token.strip()
    return (not t) or t == "YOUR_BOT_TOKEN_HERE" or t.startswith("<")


async def _run(token: str) -> int:
    from telegram import Bot
    from telegram.error import Conflict
    from telegram.error import RetryAfter

    bot = Bot(token=token)
    me = await bot.get_me()
    print(f"[preflight] Token OK. Bot: @{me.username} (id={me.id})")

    try:
        # IMPORTANT:
        # - Telegram only returns 409 Conflict for getUpdates when another poller is active.
        # - To trigger that, we must actually start a (short) long poll by setting timeout>0.
        # - Keep it small to avoid waiting too long on a clean system.
        await bot.get_updates(timeout=5)
    except Conflict as e:
        print("[preflight] Telegram reports a polling conflict (409).")
        print(f"[preflight] Details: {e}")
        return 3
    except RetryAfter as e:
        # Be conservative: if we're rate-limited, don't spam the API further.
        print("[preflight] Telegram rate limit hit (RetryAfter).")
        print(f"[preflight] Details: {e}")
        return 4

    print("[preflight] No polling conflict detected.")
    return 0


def main() -> int:
    # override=True ensures we test the token from .env even if BOT_TOKEN is exported
    # in the current shell environment.
    load_dotenv(override=True)
    token = os.getenv("BOT_TOKEN", "").strip()

    if _is_placeholder_token(token):
        print("[preflight] BOT_TOKEN is missing or placeholder. Fix your .env / environment.")
        return 2

    try:
        return asyncio.run(_run(token))
    except Exception as e:  # keep broad; we want a stable exit code
        print(f"[preflight] Unexpected error: {type(e).__name__}: {e}")
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
