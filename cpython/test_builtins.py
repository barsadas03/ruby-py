# Comprehensive verification test for:
# 1. Global Builtins: clamp, is_prime, reverse_str, inspect_obj, stats
# 2. String Methods: "hello".reverse(), "hello".reverse_str(), str.reverse("hello")
# 3. Math Module: math.clamp(val, min, max), math.is_prime(n)
# 4. String Module: string.reverse_str(s), string.reverse(s)

import math
import string

print("=" * 65)
print("TESTING DUAL BUILT-IN & MODULE / METHOD FUNCTIONALITY")
print("=" * 65)

# --- 1. CLAMP (Global Builtin & math.clamp) ---
print("\n[1] Testing clamp (Global & math.clamp)...")
assert clamp(150, 0, 100) == 100
assert clamp(-5, 0, 100) == 0
assert clamp(42, 0, 100) == 42
assert math.clamp(150, 0, 100) == 100
assert math.clamp(-5, 0, 100) == 0
assert math.clamp(42, 0, 100) == 42
assert clamp(3.14, 0.0, 5.0) == 3.14
assert math.clamp(3.14, 0.0, 5.0) == 3.14
print("  Global: clamp(150, 0, 100)      ->", clamp(150, 0, 100))
print("  Module: math.clamp(150, 0, 100) ->", math.clamp(150, 0, 100))
print("  PASS clamp!")

# --- 2. IS_PRIME (Global Builtin & math.is_prime) ---
print("\n[2] Testing is_prime (Global & math.is_prime)...")
assert is_prime(997) is True
assert is_prime(996) is False
assert math.is_prime(997) is True
assert math.is_prime(996) is False
assert is_prime(2) is True and math.is_prime(2) is True
assert is_prime(1) is False and math.is_prime(1) is False
print("  Global: is_prime(997)           ->", is_prime(997))
print("  Module: math.is_prime(997)      ->", math.is_prime(997))
print("  PASS is_prime!")

# --- 3. REVERSE (Global Builtin, String Methods, & string.reverse_str) ---
print("\n[3] Testing string reversing (Global, str.reverse, string.reverse_str)...")
s = "Hello World"
assert reverse_str(s) == "dlroW olleH"
assert s.reverse() == "dlroW olleH"
assert s.reverse_str() == "dlroW olleH"
assert str.reverse(s) == "dlroW olleH"
assert string.reverse_str(s) == "dlroW olleH"
assert string.reverse(s) == "dlroW olleH"

# Test Unicode / Emoji support
emoji_str = "Python 3.14 🚀"
assert emoji_str.reverse() == "🚀 41.3 nohtyP"
assert string.reverse_str(emoji_str) == "🚀 41.3 nohtyP"

print("  Global: reverse_str('Hello World') ->", reverse_str(s))
print("  Method: 'Hello World'.reverse()    ->", s.reverse())
print("  Method: 'Hello World'.reverse_str()->", s.reverse_str())
print("  Module: string.reverse_str(s)      ->", string.reverse_str(s))
print("  Module: string.reverse(s)          ->", string.reverse(s))
print("  Emoji : 'Python 3.14 🚀'.reverse() ->", emoji_str.reverse())
print("  PASS reverse!")

# --- 4. INSPECT_OBJ (Global Builtin) ---
print("\n[4] Testing inspect_obj...")
info = inspect_obj([10, 20, 30])
assert info["type"] == "list"
assert info["refcount"] >= 1
assert info["size"] > 0
assert info["address"].startswith("0x")
print("  inspect_obj([10, 20, 30]) ->", info)
print("  PASS inspect_obj!")

# --- 5. STATS (Global Builtin) ---
print("\n[5] Testing stats...")
stat_res = stats([10, 20, 30, 40, 50])
assert stat_res["count"] == 5
assert stat_res["sum"] == 150.0
assert stat_res["min"] == 10.0
assert stat_res["max"] == 50.0
assert stat_res["mean"] == 30.0
print("  stats([10, 20, 30, 40, 50]) ->", stat_res)
print("  PASS stats!")

print("\n" + "=" * 65)
print("ALL TESTS PASSED: GLOBAL BUILTINS, METHODS & MODULES WORKING!")
print("=" * 65)
