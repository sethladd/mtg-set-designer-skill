#!/usr/bin/env python3
"""
simulate_draft.py - Stochastic draft-and-play simulator for MTG set balance.

Usage:
    python simulate_draft.py path/to/set.json [--pods 200] [--out sim_report.md]

This is a rough limited-format simulator. It:

1. Builds booster packs from set.json (Play Booster structure).
2. Runs 8-player drafts, where each drafter picks cards based on a weighted
   archetype affinity model driven by archetypes.json.
3. Builds a 40-card deck for each drafter from picks + basic lands.
4. Plays simulated games using a lane-based combat model with evasion,
   removal, and card advantage tracking.
5. Reports archetype win rates, card play rates, format speed, and flags.

**What it catches**: unsupported archetypes, dead cards, format-speed
miscalibration, bombs that warp the format, and gross color imbalances.

**What it cannot catch**: subtle mechanic synergies, complex board states,
conditional triggers, or anything that requires reading the actual rules text
beyond basic pattern matching. The designer fills in the rest via judgment.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path


# Play Booster era pack structure (2024+).
PACK_COMMONS = 7
PACK_UNCOMMONS = 3
PACK_RARES = 1
PACK_WILDCARDS = 2
WILDCARD_RARE_RATE = 0.15
WILDCARD_UNCOMMON_RATE = 0.35
PACK_MYTHIC_SLOT_RATE = 1 / 7
DECK_SIZE_NON_LAND = 23
DECK_SIZE_LAND = 17
MAX_TURNS = 15
PLAYERS_PER_POD = 8
PICKS_PER_PACK = PACK_COMMONS + PACK_UNCOMMONS + PACK_RARES + PACK_WILDCARDS
PACKS_PER_DRAFTER = 3

# Evasion keywords that affect combat.
EVASION_KEYWORDS = {"flying", "menace", "skulk", "shadow", "fear", "intimidate",
                    "horsemanship", "landwalk", "unblockable"}
# Keywords that affect blocking / defense.
DEFENSIVE_KEYWORDS = {"reach", "vigilance", "first strike", "double strike",
                      "deathtouch", "indestructible", "defender"}
# Keywords that add generic value.
VALUE_KEYWORDS = {"lifelink", "haste", "flash", "ward", "hexproof", "trample"}

# Rarity base power for card evaluation.
RARITY_BASE = {"common": 1.0, "uncommon": 1.8, "rare": 2.8, "mythic": 3.5}


def load_set(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def rarity(card: dict) -> str:
    return card.get("rarity", "common").lower()


def _has_keyword(card: dict, kw: str) -> bool:
    """Check if a card has a keyword (case-insensitive), checking both keywords array and rules text."""
    keywords = [k.lower() for k in (card.get("keywords") or [])]
    if kw.lower() in keywords:
        return True
    text = (card.get("rules_text") or "").lower()
    return kw.lower() in text


def _count_text_abilities(text: str) -> int:
    """Rough count of distinct abilities on a card."""
    if not text.strip():
        return 0
    # Count by newlines, semicolons, and ability-starting patterns.
    breaks = text.count("\n") + text.count(";")
    triggers = len(re.findall(r"\b(when|whenever|at the beginning|if)\b", text, re.IGNORECASE))
    activated = len(re.findall(r"[{:]\s*(tap|untap|\d|[WUBRG])", text, re.IGNORECASE))
    return max(1, breaks + 1, triggers + activated)


def _is_removal(card: dict) -> bool:
    """Check if a card provides removal."""
    text = (card.get("rules_text") or "").lower()
    patterns = [
        r"destroy target (creature|permanent|nonland)",
        r"exile target (creature|permanent|nonland)",
        r"deals? \d+ damage to (any target|target creature)",
        r"target creature gets -\d+/-\d+",
        r"return target (creature|nonland permanent) to its owner",
        r"fights? target",
        r"target creature.*can't block",
    ]
    return any(re.search(p, text) for p in patterns)


def _is_card_draw(card: dict) -> bool:
    text = (card.get("rules_text") or "").lower()
    return bool(re.search(r"draw (a |two |three |\d+ )card", text))


def _is_counterspell(card: dict) -> bool:
    text = (card.get("rules_text") or "").lower()
    return "counter target spell" in text or "counter target " in text


def _has_evasion(card: dict) -> bool:
    return any(_has_keyword(card, kw) for kw in EVASION_KEYWORDS)


def card_power(card: dict, mechanics: list[dict] | None = None) -> float:
    """
    Per-card power estimate for draft evaluation.

    This is more nuanced than raw rarity + stats. It accounts for:
    - Creature stat efficiency relative to mana cost
    - Evasion, defensive, and value keywords
    - Removal, card draw, and counterspell effects
    - Number of distinct abilities (complexity as a proxy for power)
    - Set-specific mechanic keywords (bonus for non-evergreen mechanics)
    """
    base = RARITY_BASE.get(rarity(card), 1.0)
    text = (card.get("rules_text") or "").lower()
    cmc = max(card.get("cmc", 1) or 1, 1)

    # --- Creature evaluation ---
    if "Creature" in card.get("type", ""):
        p = card.get("power", 0) or 0
        t = card.get("toughness", 0) or 0
        # Stat efficiency: how much body per mana?
        stat_total = p + t
        expected = cmc * 2.0  # vanilla benchmark: CMC 3 → 3/3
        efficiency = stat_total / expected if expected > 0 else 0
        base += 0.4 * max(efficiency - 0.8, 0)

        # High power relative to cost is more dangerous than high toughness.
        if p >= cmc and cmc >= 2:
            base += 0.2

        # Evasion makes damage much harder to prevent.
        if _has_evasion(card):
            # Scale evasion bonus with power — a 1/1 flyer is less scary than a 3/3 flyer.
            base += 0.3 + 0.15 * min(p, 5)

        # Defensive keywords.
        if _has_keyword(card, "deathtouch"):
            base += 0.4  # deathtouch is premium — makes any body relevant
        if _has_keyword(card, "first strike") or _has_keyword(card, "double strike"):
            base += 0.3 + 0.1 * min(p, 4)
        if _has_keyword(card, "vigilance"):
            base += 0.15 + 0.05 * min(p, 4)
        if _has_keyword(card, "reach"):
            base += 0.15
        if _has_keyword(card, "defender"):
            base -= 0.3  # can't attack, significant downside in limited

    # --- Value keywords (any card type) ---
    if _has_keyword(card, "lifelink"):
        base += 0.25
    if _has_keyword(card, "haste"):
        base += 0.2
    if _has_keyword(card, "flash"):
        base += 0.2
    if _has_keyword(card, "ward"):
        base += 0.25
    if _has_keyword(card, "hexproof"):
        base += 0.3
    if _has_keyword(card, "trample"):
        base += 0.15
    if _has_keyword(card, "indestructible"):
        base += 0.5

    # --- Spell effects ---
    if _is_removal(card):
        base += 0.6
        # Unconditional removal is better than conditional.
        if re.search(r"destroy target creature\b", text) or re.search(r"exile target creature\b", text):
            base += 0.2
    if _is_card_draw(card):
        base += 0.4
        # Drawing multiple cards is much better.
        match = re.search(r"draw (two|three|four|\d+) card", text)
        if match:
            base += 0.3
    if _is_counterspell(card):
        base += 0.3

    # --- Token generation ---
    if re.search(r"create (a|two|three|\d+) .*token", text):
        base += 0.3

    # --- ETB / death triggers (value creatures) ---
    if "Creature" in card.get("type", "") and re.search(r"when .* enters", text):
        base += 0.2
    if re.search(r"when .* dies", text):
        base += 0.15

    # --- Enchantment / artifact auras ---
    if "Aura" in (card.get("subtypes") or []):
        base -= 0.2  # auras carry inherent card disadvantage risk

    # --- Set-specific mechanic bonus ---
    # Cards with set mechanics should get a small bonus because they interact
    # with the set's synergy structures.
    if mechanics:
        mechanic_names = {m.get("name", "").lower() for m in mechanics}
        card_keywords = {k.lower() for k in (card.get("keywords") or [])}
        set_kw_count = len(card_keywords & mechanic_names)
        if set_kw_count:
            base += 0.15 * set_kw_count

    # --- Ability count bonus ---
    # Cards with multiple abilities tend to be more versatile in limited.
    abilities = _count_text_abilities(text)
    if abilities >= 2:
        base += 0.1 * min(abilities - 1, 3)

    # --- Mana cost penalty ---
    # Very expensive cards (6+) are worse in limited because you might not cast them.
    if cmc >= 6:
        base -= 0.15 * (cmc - 5)

    return max(base, 0.1)


@dataclass
class BoardCreature:
    """A creature on the battlefield during a simulated game."""
    name: str
    power: int
    toughness: int
    evasion: bool
    deathtouch: bool
    first_strike: bool
    lifelink: bool
    vigilance: bool
    reach: bool
    card_power_score: float

    @classmethod
    def from_card(cls, card: dict, power_score: float) -> "BoardCreature":
        return cls(
            name=card.get("name", "?"),
            power=card.get("power", 0) or 0,
            toughness=card.get("toughness", 0) or 0,
            evasion=_has_evasion(card),
            deathtouch=_has_keyword(card, "deathtouch"),
            first_strike=_has_keyword(card, "first strike") or _has_keyword(card, "double strike"),
            lifelink=_has_keyword(card, "lifelink"),
            vigilance=_has_keyword(card, "vigilance"),
            reach=_has_keyword(card, "reach"),
            card_power_score=power_score,
        )


@dataclass
class Drafter:
    seat: int
    colors: list[str] = field(default_factory=list)
    archetype: str | None = None
    picks: list[dict] = field(default_factory=list)

    def color_affinity(self, card: dict) -> float:
        card_colors = card.get("color", [])
        if not card_colors:
            return 0.5
        if not self.colors:
            return 0.3
        overlap = sum(1 for c in card_colors if c in self.colors)
        if overlap == len(card_colors):
            return 1.0
        if overlap >= 1:
            return 0.2
        return 0.01


def build_pack(pools_by_rarity: dict[str, list[dict]], rng: random.Random) -> list[dict]:
    pack: list[dict] = []
    pack.extend(rng.sample(pools_by_rarity["common"], k=min(PACK_COMMONS, len(pools_by_rarity["common"]))))
    pack.extend(rng.sample(pools_by_rarity["uncommon"], k=min(PACK_UNCOMMONS, len(pools_by_rarity["uncommon"]))))
    if pools_by_rarity.get("mythic") and rng.random() < PACK_MYTHIC_SLOT_RATE:
        pack.append(rng.choice(pools_by_rarity["mythic"]))
    else:
        pack.append(rng.choice(pools_by_rarity["rare"]))
    for _ in range(PACK_WILDCARDS):
        roll = rng.random()
        if roll < WILDCARD_RARE_RATE:
            if pools_by_rarity.get("mythic") and rng.random() < PACK_MYTHIC_SLOT_RATE:
                pack.append(rng.choice(pools_by_rarity["mythic"]))
            else:
                pack.append(rng.choice(pools_by_rarity["rare"]))
        elif roll < WILDCARD_RARE_RATE + WILDCARD_UNCOMMON_RATE:
            pack.append(rng.choice(pools_by_rarity["uncommon"]))
        else:
            pack.append(rng.choice(pools_by_rarity["common"]))
    return pack


def pick_card(drafter: Drafter, pack: list[dict], archetypes: dict,
              mechanics: list[dict]) -> int:
    best_idx = 0
    best_score = -1.0
    for i, card in enumerate(pack):
        score = card_power(card, mechanics) * drafter.color_affinity(card)
        if drafter.archetype and drafter.archetype in (card.get("archetypes") or []):
            score *= 1.5
        # Mono-colored cards in the drafter's colors get a small bonus even
        # without explicit archetype tagging.
        card_colors = card.get("color", [])
        if card_colors and drafter.colors and all(c in drafter.colors for c in card_colors):
            score *= 1.1
        if score > best_score:
            best_score = score
            best_idx = i
    return best_idx


def commit_colors(drafter: Drafter, archetypes: dict) -> None:
    if drafter.archetype:
        return
    if len(drafter.picks) < 4:
        return
    best_arch = None
    best_score = -1.0
    for pair, data in archetypes.items():
        score = 0.0
        for p in drafter.picks:
            if pair in (p.get("archetypes") or []):
                score += 2
            card_colors = p.get("color", [])
            if card_colors and all(c in pair for c in card_colors):
                score += 1
            elif card_colors and any(c in pair for c in card_colors):
                score += 0.3
        if score > best_score:
            best_score = score
            best_arch = pair
    if best_arch:
        drafter.archetype = best_arch
        drafter.colors = list(best_arch)


def build_deck(drafter: Drafter, mechanics: list[dict]) -> list[dict]:
    playables = [
        c for c in drafter.picks
        if not c.get("color") or all(col in drafter.colors for col in c.get("color", []))
    ]
    playables.sort(key=lambda c: card_power(c, mechanics), reverse=True)
    return playables[:DECK_SIZE_NON_LAND]


def simulate_game(deck_a: list[dict], deck_b: list[dict],
                  mechanics: list[dict], rng: random.Random) -> tuple[int, int]:
    """
    Lane-based combat simulator with evasion, removal, and card advantage.

    Each player has a "ground" lane and an "air" lane (evasive creatures).
    Ground creatures can only block ground creatures (unless they have reach).
    Evasive creatures attack in the air lane and can only be blocked by flyers/reach.
    Removal targets the strongest opposing creature.
    """
    if not deck_a or not deck_b:
        return (0, MAX_TURNS)

    # Draw opening hands (simplified: just take top cards from shuffled deck).
    lib_a = rng.sample(deck_a, k=len(deck_a))
    lib_b = rng.sample(deck_b, k=len(deck_b))
    hand_a = lib_a[:7]
    lib_a = lib_a[7:]
    hand_b = lib_b[:7]
    lib_b = lib_b[7:]

    life = {"a": 20, "b": 20}
    board: dict[str, list[BoardCreature]] = {"a": [], "b": []}
    cards_seen = {"a": 7, "b": 7}  # track card advantage

    for turn in range(1, MAX_TURNS + 1):
        for player, opp, hand, lib in [
            ("a", "b", hand_a, lib_a),
            ("b", "a", hand_b, lib_b),
        ]:
            # Draw a card.
            if lib:
                hand.append(lib.pop(0))
                cards_seen[player] += 1

            # Play the best affordable card.
            affordable = [c for c in hand if (c.get("cmc", 99) or 99) <= turn]
            if not affordable:
                continue

            card = max(affordable, key=lambda c: card_power(c, mechanics))
            hand.remove(card)
            text = (card.get("rules_text") or "").lower()

            if "Creature" in card.get("type", ""):
                creature = BoardCreature.from_card(card, card_power(card, mechanics))
                board[player].append(creature)

                # ETB removal effect (e.g., "when ~ enters, destroy target creature")
                if re.search(r"when .* enters.*destroy target creature", text):
                    if board[opp]:
                        target = max(board[opp], key=lambda c: c.card_power_score)
                        board[opp].remove(target)
                # ETB damage (e.g., "when ~ enters, deal 2 damage")
                elif re.search(r"when .* enters.*deals? (\d+) damage", text):
                    dmg_match = re.search(r"deals? (\d+) damage", text)
                    if dmg_match:
                        dmg = int(dmg_match.group(1))
                        # Try to kill a creature, otherwise hit face.
                        killed = False
                        for bc in sorted(board[opp], key=lambda c: c.toughness):
                            if bc.toughness <= dmg:
                                board[opp].remove(bc)
                                killed = True
                                break
                        if not killed:
                            life[opp] -= dmg
                # ETB card draw
                if re.search(r"when .* enters.*draw", text):
                    if lib:
                        hand.append(lib.pop(0))
                        cards_seen[player] += 1

            else:
                # Non-creature spell.
                if _is_removal(card):
                    # Remove the strongest opposing creature.
                    if board[opp]:
                        target = max(board[opp], key=lambda c: c.card_power_score)
                        board[opp].remove(target)
                if _is_card_draw(card):
                    draw_count = 1
                    match = re.search(r"draw (two|three|four|\d+)", text)
                    if match:
                        word = match.group(1)
                        draw_count = {"two": 2, "three": 3, "four": 4}.get(word, 0)
                        if not draw_count:
                            try:
                                draw_count = int(word)
                            except ValueError:
                                draw_count = 1
                    for _ in range(draw_count):
                        if lib:
                            hand.append(lib.pop(0))
                            cards_seen[player] += 1
                if _is_counterspell(card):
                    # Simplified: counterspells just add virtual card advantage.
                    cards_seen[player] += 0.5
                # Token generation
                token_match = re.search(r"create (a|one|two|three|four|\d+) (\d+)/(\d+)", text)
                if token_match:
                    count_word = token_match.group(1)
                    tp = int(token_match.group(2))
                    tt = int(token_match.group(3))
                    count = {"a": 1, "one": 1, "two": 2, "three": 3, "four": 4}.get(count_word, 0)
                    if not count:
                        try:
                            count = int(count_word)
                        except ValueError:
                            count = 1
                    for _ in range(count):
                        board[player].append(BoardCreature(
                            name="Token", power=tp, toughness=tt,
                            evasion=False, deathtouch=False, first_strike=False,
                            lifelink=False, vigilance=False, reach=False,
                            card_power_score=0.5,
                        ))

            # --- Combat phase ---
            if not board[player]:
                continue

            # Split into evasive and ground attackers.
            evasive_attackers = [c for c in board[player] if c.evasion]
            ground_attackers = [c for c in board[player] if not c.evasion]

            # Evasive creatures: only blocked by flyers/reach.
            air_blockers = [c for c in board[opp] if c.evasion or c.reach]
            evasive_damage = 0
            for attacker in evasive_attackers:
                blocked = False
                for blocker in air_blockers:
                    if blocker.toughness > 0:
                        # Block: trade damage.
                        if attacker.deathtouch or attacker.power >= blocker.toughness:
                            blocker.toughness = 0  # mark dead
                        if blocker.deathtouch or blocker.power >= attacker.toughness:
                            attacker.toughness = 0
                        blocked = True
                        break
                if not blocked:
                    evasive_damage += attacker.power
                    if attacker.lifelink:
                        life[player] += attacker.power

            # Ground creatures: opponent decides blocking.
            # Simplified: opponent blocks the biggest attacker with their best ground blocker.
            ground_blockers = [c for c in board[opp] if not c.evasion and c.toughness > 0]
            ground_damage = 0
            for attacker in sorted(ground_attackers, key=lambda c: c.power, reverse=True):
                if attacker.toughness <= 0:
                    continue
                if ground_blockers:
                    # Assign best available blocker.
                    blocker = max(ground_blockers, key=lambda c: c.toughness)
                    ground_blockers.remove(blocker)
                    # First strike advantage.
                    if attacker.first_strike and not blocker.first_strike:
                        if attacker.power >= blocker.toughness or attacker.deathtouch:
                            blocker.toughness = 0
                        else:
                            if blocker.deathtouch or blocker.power >= attacker.toughness:
                                attacker.toughness = 0
                    elif blocker.first_strike and not attacker.first_strike:
                        if blocker.power >= attacker.toughness or blocker.deathtouch:
                            attacker.toughness = 0
                        else:
                            if attacker.power >= blocker.toughness or attacker.deathtouch:
                                blocker.toughness = 0
                    else:
                        # Simultaneous damage.
                        if attacker.power >= blocker.toughness or attacker.deathtouch:
                            blocker.toughness = 0
                        if blocker.power >= attacker.toughness or blocker.deathtouch:
                            attacker.toughness = 0
                    if attacker.lifelink and blocker.toughness <= 0:
                        life[player] += attacker.power
                else:
                    # Unblocked.
                    ground_damage += attacker.power
                    if attacker.lifelink:
                        life[player] += attacker.power

            total_damage = evasive_damage + ground_damage
            life[opp] -= total_damage

            # Remove dead creatures.
            board[player] = [c for c in board[player] if c.toughness > 0]
            board[opp] = [c for c in board[opp] if c.toughness > 0]

            if life[opp] <= 0:
                return (1 if player == "a" else 2, turn)

    # Timeout: higher life wins, tie if equal.
    if life["a"] > life["b"]:
        return (1, MAX_TURNS)
    elif life["b"] > life["a"]:
        return (2, MAX_TURNS)
    return (0, MAX_TURNS)


def run_pod(set_data: dict, rng: random.Random) -> dict:
    cards = set_data.get("cards", [])
    archetypes = set_data.get("archetypes", {})
    mechanics = set_data.get("mechanics", [])
    pools_by_rarity = {r: [c for c in cards if rarity(c) == r]
                       for r in ("common", "uncommon", "rare", "mythic")}

    drafters = [Drafter(seat=i) for i in range(PLAYERS_PER_POD)]

    for pack_num in range(PACKS_PER_DRAFTER):
        packs = [build_pack(pools_by_rarity, rng) for _ in range(PLAYERS_PER_POD)]
        for pick_num in range(PICKS_PER_PACK):
            for i, d in enumerate(drafters):
                pack_idx = (i + (pick_num if pack_num % 2 == 0 else -pick_num)) % PLAYERS_PER_POD
                if not packs[pack_idx]:
                    continue
                idx = pick_card(d, packs[pack_idx], archetypes, mechanics)
                card = packs[pack_idx].pop(idx)
                d.picks.append(card)
                commit_colors(d, archetypes)

    decks = [build_deck(d, mechanics) for d in drafters]

    results = {"wins_by_archetype": defaultdict(int),
               "games_by_archetype": defaultdict(int), "turns": []}
    card_plays: Counter = Counter()
    for i, d in enumerate(drafters):
        for c in decks[i]:
            card_plays[c.get("name", "?")] += 1

    for i in range(PLAYERS_PER_POD):
        for j in range(i + 1, PLAYERS_PER_POD):
            for _ in range(2):
                winner, turn = simulate_game(decks[i], decks[j], mechanics, rng)
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
    cards = set_data.get("cards", [])
    by_name = {c.get("name"): c for c in cards}
    total_decks = pods_run * PLAYERS_PER_POD
    out: list[str] = []
    warnings: list[str] = []

    out.append(f"# Simulated Draft Report: {set_data.get('set_name', 'Unnamed')}")
    out.append(f"Pods simulated: **{pods_run}**")
    out.append("")
    out.append("> **Note:** This simulator models combat with evasion lanes, removal,")
    out.append("> card draw, and keyword interactions, but it *cannot* model set-specific")
    out.append("> mechanic synergies, conditional triggers, or complex board states.")
    out.append("> Use it to catch gross imbalances — not to fine-tune.")
    out.append("")

    # --- Archetype win rates ---
    out.append("## Archetype win rates")
    wins = agg["wins_by_archetype"]
    games = agg["games_by_archetype"]
    out.append("| Archetype | Games | Wins | Win rate |")
    out.append("|---|---|---|---|")
    for arch in sorted(games, key=lambda k: -games[k]):
        g = games[arch]
        w = wins.get(arch, 0)
        rate = w / g if g else 0
        flag = ""
        if rate < 0.42 or rate > 0.58:
            flag = " ⚠️"
            warnings.append(f"Archetype {arch} win rate {rate:.0%} outside healthy band (42–58%)")
        out.append(f"| {arch} | {g} | {w} | {rate:.0%}{flag} |")
    out.append("")

    # --- Format speed ---
    if agg["turns"]:
        mean_turn = statistics.mean(agg["turns"])
        median_turn = statistics.median(agg["turns"])
        out.append("## Format speed")
        out.append(f"- Average game length: **turn {mean_turn:.1f}** (median {median_turn:.1f})")
        if mean_turn < 7:
            warnings.append(f"Format is very fast (avg turn {mean_turn:.1f})")
        elif mean_turn > 12:
            warnings.append(f"Format is very slow (avg turn {mean_turn:.1f})")
        out.append("")

    # --- Card play rates (fixed: filter by rarity before counting) ---
    plays = agg["card_plays"]
    commons = {c.get("name") for c in cards if rarity(c) == "common"}
    uncommons = {c.get("name") for c in cards if rarity(c) == "uncommon"}

    common_plays = {n: p for n, p in plays.items() if n in commons}
    uncommon_plays = {n: p for n, p in plays.items() if n in uncommons}

    out.append("## Card play rate outliers")

    # Commons.
    high_commons = [(n, p) for n, p in common_plays.items()
                    if total_decks > 0 and p / total_decks > 0.85]
    low_commons = [(n, p) for n, p in common_plays.items()
                   if total_decks > 0 and p / total_decks < 0.05]
    # Also flag commons that never appeared at all.
    unseen_commons = [c.get("name") for c in cards
                      if rarity(c) == "common" and c.get("name") not in plays]

    out.append(f"### Commons ({len(commons)} total)")
    out.append(f"- Near-ubiquitous (>85% of decks): {len(high_commons)}")
    for name, p in sorted(high_commons, key=lambda x: -x[1])[:10]:
        out.append(f"  - {name} ({p / total_decks:.0%})")
        warnings.append(f"Common {name} in {p / total_decks:.0%} of decks (possible auto-include)")

    out.append(f"- Rarely played (<5% of decks): {len(low_commons)}")
    for name, p in sorted(low_commons, key=lambda x: x[1])[:10]:
        out.append(f"  - {name} ({p / total_decks:.0%})")

    if unseen_commons:
        out.append(f"- Never drafted: {len(unseen_commons)}")
        for name in unseen_commons[:10]:
            out.append(f"  - {name}")

    if len(low_commons) + len(unseen_commons) > len(commons) * 0.4:
        warnings.append(
            f"{len(low_commons) + len(unseen_commons)} of {len(commons)} commons are rarely/never "
            f"played — check if off-color cards are getting stranded or if some cards are too weak"
        )
    out.append("")

    # Uncommons.
    low_uncommons = [(n, p) for n, p in uncommon_plays.items()
                     if total_decks > 0 and p / total_decks < 0.03]
    if low_uncommons:
        out.append(f"### Uncommons — rarely played (<3%)")
        for name, p in sorted(low_uncommons, key=lambda x: x[1])[:10]:
            out.append(f"  - {name} ({p / total_decks:.0%})")
        out.append("")

    # --- Summary ---
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
