#!/usr/bin/env python3
"""
simulate_draft.py - Stochastic draft-and-play simulator for MTG set balance.

Usage:
    python simulate_draft.py path/to/set.json [--pods 200] [--out sim_report.md]

This is a rough limited-format simulator. It:

1. Builds booster packs from set.json (10 commons, 3 uncommons, 1 rare/mythic).
2. Runs 8-player drafts, where each drafter picks cards based on a weighted
   archetype affinity model driven by archetypes.json.
3. Builds a 40-card deck for each drafter from picks + basic lands.
4. Plays simulated games pair-round-robin using a simple creature-curve-plus-
   removal combat model.
5. Reports archetype win rates, card play rates, format speed, and flags.

The simulator is intentionally *rough*. It cannot catch every broken card. Its
job is to catch the most common failure modes: unsupported archetypes, dead
cards, bombs that win 90% of games, format-speed miscalibration. The designer
fills in the rest via judgment.
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path


PACK_COMMONS = 10
PACK_UNCOMMONS = 3
PACK_RARES = 1
PACK_MYTHIC_SLOT_RATE = 1 / 8  # 1-in-8 rares is a mythic
DECK_SIZE_NON_LAND = 23
DECK_SIZE_LAND = 17
MAX_TURNS = 20
PLAYERS_PER_POD = 8
PICKS_PER_PACK = PACK_COMMONS + PACK_UNCOMMONS + PACK_RARES
PACKS_PER_DRAFTER = 3


@dataclass
class Drafter:
    seat: int
    colors: list[str] = field(default_factory=list)
    archetype: str | None = None
    picks: list[dict] = field(default_factory=list)

    def color_affinity(self, card: dict) -> float:
        """How well a card fits this drafter's current color commitment."""
        card_colors = card.get("color", [])
        if not card_colors:
            return 0.5  # colorless goes anywhere
        if not self.colors:
            return 0.3  # early picks, no commitment yet
        overlap = sum(1 for c in card_colors if c in self.colors)
        if overlap == len(card_colors):
            return 1.0
        if overlap >= 1:
            return 0.2
        return 0.01


def load_set(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def rarity(card: dict) -> str:
    return card.get("rarity", "common").lower()


def card_power(card: dict) -> float:
    """Rough per-card power estimate. Used for both picking and game sim."""
    # Baseline by rarity
    base = {"common": 1.0, "uncommon": 1.5, "rare": 2.3, "mythic": 3.0}.get(rarity(card), 1.0)
    # Creature stat bonus
    if "Creature" in card.get("type", ""):
        p = card.get("power", 0) or 0
        t = card.get("toughness", 0) or 0
        cmc = max(card.get("cmc", 1), 1)
        stat_efficiency = (p + t) / cmc
        base += 0.3 * max(stat_efficiency - 2, 0)
    # Keyword bonus
    keywords = card.get("keywords", []) or []
    premium = {"flying", "deathtouch", "lifelink", "first strike", "double strike", "menace", "haste"}
    base += 0.15 * sum(1 for k in keywords if k.lower() in premium)
    # Rules text density proxy
    text = (card.get("rules_text") or "").lower()
    if "destroy target" in text or "exile target" in text:
        base += 0.4
    if "draw" in text and "card" in text:
        base += 0.3
    return base


def build_pack(pools_by_rarity: dict[str, list[dict]], rng: random.Random) -> list[dict]:
    pack: list[dict] = []
    pack.extend(rng.sample(pools_by_rarity["common"], k=min(PACK_COMMONS, len(pools_by_rarity["common"]))))
    pack.extend(rng.sample(pools_by_rarity["uncommon"], k=min(PACK_UNCOMMONS, len(pools_by_rarity["uncommon"]))))
    # Rare or mythic slot
    if pools_by_rarity.get("mythic") and rng.random() < PACK_MYTHIC_SLOT_RATE:
        pack.append(rng.choice(pools_by_rarity["mythic"]))
    else:
        pack.append(rng.choice(pools_by_rarity["rare"]))
    return pack


def pick_card(drafter: Drafter, pack: list[dict], archetypes: dict) -> int:
    best_idx = 0
    best_score = -1.0
    for i, card in enumerate(pack):
        score = card_power(card) * drafter.color_affinity(card)
        # Bonus if card matches drafter's archetype
        if drafter.archetype and drafter.archetype in (card.get("archetypes") or []):
            score *= 1.5
        if score > best_score:
            best_score = score
            best_idx = i
    return best_idx


def commit_colors(drafter: Drafter, archetypes: dict) -> None:
    """After a few picks, lock the drafter into an archetype based on picks so far."""
    if drafter.archetype:
        return
    if len(drafter.picks) < 4:
        return
    # Score each archetype by how well the current picks match it
    best_arch = None
    best_score = -1.0
    for pair, data in archetypes.items():
        score = 0.0
        for p in drafter.picks:
            if pair in (p.get("archetypes") or []):
                score += 2
            if all(c in pair for c in p.get("color", [])):
                score += 1
        if score > best_score:
            best_score = score
            best_arch = pair
    if best_arch:
        drafter.archetype = best_arch
        drafter.colors = list(best_arch)


def build_deck(drafter: Drafter) -> list[dict]:
    """Choose 23 nonland cards from picks that fit the drafter's colors."""
    playables = [
        c for c in drafter.picks
        if not c.get("color") or all(col in drafter.colors for col in c.get("color", []))
    ]
    playables.sort(key=card_power, reverse=True)
    return playables[:DECK_SIZE_NON_LAND]


def simulate_game(deck_a: list[dict], deck_b: list[dict], rng: random.Random) -> tuple[int, int]:
    """Very rough game simulator. Returns (winner, turn_ended)."""
    hands = {
        "a": rng.sample(deck_a, k=min(7, len(deck_a))) if deck_a else [],
        "b": rng.sample(deck_b, k=min(7, len(deck_b))) if deck_b else [],
    }
    life = {"a": 20, "b": 20}
    board_power = {"a": 0.0, "b": 0.0}
    for turn in range(1, MAX_TURNS + 1):
        for player, opp in (("a", "b"), ("b", "a")):
            # Play a spell per turn based on rough mana availability.
            affordable = [c for c in hands[player] if (c.get("cmc", 99) or 99) <= turn]
            if affordable:
                card = max(affordable, key=card_power)
                hands[player].remove(card)
                if "Creature" in card.get("type", ""):
                    board_power[player] += card_power(card)
                else:
                    text = (card.get("rules_text") or "").lower()
                    if "destroy target" in text or "exile target" in text:
                        board_power[opp] = max(0, board_power[opp] - 1.5)
                    if "damage to any target" in text or "damage to target player" in text:
                        life[opp] -= 2
            # Attack phase
            damage = max(0, board_power[player] - board_power[opp] * 0.5)
            life[opp] -= damage * 0.5
            if life[opp] <= 0:
                return (1 if player == "a" else 2, turn)
    # Draw - higher life wins
    if life["a"] > life["b"]:
        return (1, MAX_TURNS)
    elif life["b"] > life["a"]:
        return (2, MAX_TURNS)
    else:
        return (0, MAX_TURNS)


def run_pod(set_data: dict, rng: random.Random) -> dict:
    cards = set_data.get("cards", [])
    archetypes = set_data.get("archetypes", {})
    pools_by_rarity = {r: [c for c in cards if rarity(c) == r] for r in ("common", "uncommon", "rare", "mythic")}

    drafters = [Drafter(seat=i) for i in range(PLAYERS_PER_POD)]

    # 3 packs per drafter
    for pack_num in range(PACKS_PER_DRAFTER):
        packs = [build_pack(pools_by_rarity, rng) for _ in range(PLAYERS_PER_POD)]
        for pick_num in range(PICKS_PER_PACK):
            for i, d in enumerate(drafters):
                pack_idx = (i + (pick_num if pack_num % 2 == 0 else -pick_num)) % PLAYERS_PER_POD
                if not packs[pack_idx]:
                    continue
                idx = pick_card(d, packs[pack_idx], archetypes)
                card = packs[pack_idx].pop(idx)
                d.picks.append(card)
                commit_colors(d, archetypes)

    decks = [build_deck(d) for d in drafters]

    # Round robin
    results = {"wins_by_archetype": defaultdict(int), "games_by_archetype": defaultdict(int), "turns": []}
    card_plays: Counter = Counter()
    deck_counts_by_arch: dict = defaultdict(list)
    for i, d in enumerate(drafters):
        arch = d.archetype or "UNKNOWN"
        deck_counts_by_arch[arch].append(len(decks[i]))
        for c in decks[i]:
            card_plays[c.get("name", "?")] += 1

    for i in range(PLAYERS_PER_POD):
        for j in range(i + 1, PLAYERS_PER_POD):
            for _ in range(2):  # two games each
                winner, turn = simulate_game(decks[i], decks[j], rng)
                results["turns"].append(turn)
                arch_i = drafters[i].archetype or "UNKNOWN"
                arch_j = drafters[j].archetype or "UNKNOWN"
                results["games_by_archetype"][arch_i] += 1
                results["games_by_archetype"][arch_j] += 1
                if winner == 1:
                    results["wins_by_archetype"][arch_i] += 1
                elif winner == 2:
                    results["wins_by_archetype"][arch_j] += 1

    results["card_plays"] = dict(card_plays)
    return results


def aggregate(pods: list[dict]) -> dict:
    wins: Counter = Counter()
    games: Counter = Counter()
    turns: list[int] = []
    card_plays: Counter = Counter()
    for pod in pods:
        for arch, n in pod["wins_by_archetype"].items():
            wins[arch] += n
        for arch, n in pod["games_by_archetype"].items():
            games[arch] += n
        turns.extend(pod["turns"])
        for name, n in pod["card_plays"].items():
            card_plays[name] += n
    return {
        "wins_by_archetype": dict(wins),
        "games_by_archetype": dict(games),
        "turns": turns,
        "card_plays": dict(card_plays),
    }


def format_report(set_data: dict, agg: dict, pods_run: int) -> str:
    out: list[str] = []
    out.append(f"# Simulated Draft Report: {set_data.get('set_name', 'Unnamed')}")
    out.append(f"Pods simulated: **{pods_run}**")
    out.append("")

    # Archetype win rates
    out.append("## Archetype win rates")
    wins = agg["wins_by_archetype"]
    games = agg["games_by_archetype"]
    warnings: list[str] = []
    out.append("| Archetype | Games | Wins | Win rate |")
    out.append("|---|---|---|---|")
    for arch in sorted(games, key=lambda k: -games[k]):
        g = games[arch]
        w = wins.get(arch, 0)
        rate = w / g if g else 0
        flag = ""
        if rate < 0.42 or rate > 0.58:
            flag = " ⚠️"
            warnings.append(f"Archetype {arch} win rate {rate:.0%} outside healthy band")
        out.append(f"| {arch} | {g} | {w} | {rate:.0%}{flag} |")
    out.append("")

    # Format speed
    if agg["turns"]:
        mean_turn = statistics.mean(agg["turns"])
        out.append("## Format speed")
        out.append(f"- Average game length: **turn {mean_turn:.1f}**")
        if mean_turn < 7:
            warnings.append(f"Format is very fast (avg turn {mean_turn:.1f})")
        elif mean_turn > 12:
            warnings.append(f"Format is very slow (avg turn {mean_turn:.1f})")
        out.append("")

    # Card play rates
    cards = set_data.get("cards", [])
    by_name = {c.get("name"): c for c in cards}
    total_decks = pods_run * PLAYERS_PER_POD
    plays = agg["card_plays"]
    out.append("## Card play rate outliers")
    high = [(n, p) for n, p in plays.items() if total_decks > 0 and p / total_decks > 0.9]
    low = [(n, p) for n, p in plays.items() if total_decks > 0 and p / total_decks < 0.08]
    out.append(f"- Near-ubiquitous commons (>90% of decks): {len(high)}")
    for name, p in sorted(high, key=lambda x: -x[1])[:10]:
        c = by_name.get(name, {})
        if rarity(c) == "common":
            out.append(f"  - {name} ({p / total_decks:.0%})")
            warnings.append(f"Common {name} appears in {p / total_decks:.0%} of decks (possible auto-include)")
    out.append(f"- Near-unplayable commons (<8% of decks): {len(low)}")
    for name, p in sorted(low, key=lambda x: x[1])[:10]:
        c = by_name.get(name, {})
        if rarity(c) == "common":
            out.append(f"  - {name} ({p / total_decks:.0%})")
            warnings.append(f"Common {name} appears in only {p / total_decks:.0%} of decks (possibly unplayable)")
    out.append("")

    out.append("## Summary")
    if warnings:
        out.append(f"**{len(warnings)} warnings:**")
        for w in warnings:
            out.append(f"- {w}")
    else:
        out.append("Simulation pass clean within healthy bands.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("set_path", type=Path)
    ap.add_argument("--pods", type=int, default=50)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    set_data = load_set(args.set_path)
    rng = random.Random(args.seed)

    pods = [run_pod(set_data, rng) for _ in range(args.pods)]
    agg = aggregate(pods)
    report = format_report(set_data, agg, args.pods)

    if args.out:
        args.out.write_text(report)
        print(f"Wrote {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
