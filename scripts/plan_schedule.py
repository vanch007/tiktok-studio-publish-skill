#!/usr/bin/env python3
"""Create a deterministic TikTok upload schedule and non-repeating music rotation.

This planner has no network or browser side effects. It only emits JSON so the
Computer Use operator can apply and verify the plan in the confirmed session.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", required=True, help="First slot, e.g. 2026-08-07T13:30")
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument(
        "--interval-minutes",
        type=int,
        default=None,
        help="Fixed interval mode; omit when using --daily-slots.",
    )
    parser.add_argument(
        "--daily-slots",
        nargs="+",
        help="Local daily times such as 00:30 13:30 20:30.",
    )
    parser.add_argument("--timezone", default="Asia/Kuala_Lumpur")
    parser.add_argument("--music-pool", nargs="+", required=True)
    parser.add_argument("--music-db", type=int, default=-40)
    return parser.parse_args()


def build_plan(args: argparse.Namespace) -> dict:
    if args.count < 1:
        raise SystemExit("count must be positive")
    if args.interval_minutes is not None and args.interval_minutes < 15:
        raise SystemExit("interval-minutes must be at least 15")
    if args.interval_minutes is None and not args.daily_slots:
        args.interval_minutes = 480
    if args.interval_minutes is not None and args.daily_slots:
        raise SystemExit("choose either interval-minutes or daily-slots")
    if not args.music_pool:
        raise SystemExit("music-pool must not be empty")
    tz = ZoneInfo(args.timezone)
    start = datetime.fromisoformat(args.start).replace(tzinfo=tz)
    if args.daily_slots:
        try:
            slot_times = sorted(
                (datetime.strptime(value, "%H:%M").time() for value in args.daily_slots),
                key=lambda value: (value.hour, value.minute),
            )
        except ValueError as exc:
            raise SystemExit("daily-slots must use HH:MM") from exc
        slots = []
        day = start.date()
        while len(slots) < args.count:
            for slot_time in slot_times:
                candidate = datetime.combine(day, slot_time, tzinfo=tz)
                if candidate >= start:
                    slots.append(candidate)
                    if len(slots) >= args.count:
                        break
            day += timedelta(days=1)
    else:
        slots = [
            start + timedelta(minutes=args.interval_minutes * index)
            for index in range(args.count)
        ]

    items = []
    for sequence, slot in enumerate(slots, start=1):
        track = args.music_pool[(sequence - 1) % len(args.music_pool)]
        if items and track == items[-1]["music_track"]:
            raise SystemExit("music pool must contain at least two distinct tracks")
        items.append(
            {
                "sequence": sequence,
                "schedule_at": slot.isoformat(timespec="minutes"),
                "music_track": track,
                "music_db": args.music_db,
            }
        )
    return {
        "timezone": args.timezone,
        "interval_minutes": args.interval_minutes,
        "daily_slots": args.daily_slots,
        "music_pool": args.music_pool,
        "items": items,
    }


if __name__ == "__main__":
    print(json.dumps(build_plan(parse_args()), ensure_ascii=False, indent=2))
