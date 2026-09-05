'''
Q7: The Family Tree Builder (Very Hard)

Create a family tree system using nested structures with advanced data manipulation.

Requirements:

    Build a family tree structure:
    python

    family_tree = {
        "Grandfather": {
            "name": "Joseph",
            "spouse": "Mary",
            "children": {
                "John": {
                    "birth_year": 1970,
                    "spouse": "Jane",
                    "children": {
                        "Alice": {
                            "birth_year": 1995,
                            "spouse": None,
                            "children": {}
                        },
                        "Bob": {
                            "birth_year": 1998,
                            "spouse": None,
                            "children": {}
                        }
                    }
                },
                "Peter": {
                    "birth_year": 1975,
                    "spouse": "Susan",
                    "children": {
                        "Carol": {
                            "birth_year": 2000,
                            "spouse": None,
                            "children": {}
                        }
                    }
                }
            }
        }
    }

    Implement these complex functions:

        count_descendants(name) → Count all descendants recursively

        find_path(root, target) → Returns path from root to target

        get_siblings(name) → Returns list of siblings

        get_cousins(name) → Returns list of cousins

        get_generation(name) → Returns generation number (root = 0)

        get_family_members() → Returns list of all member names

        find_oldest() → Returns oldest person

        find_youngest() → Returns youngest person

        get_average_age() → Returns average age (assume current year 2026)

        get_family_by_generation() → Returns dict with generation as keys and members as values

    Bonus features:

        Add a new family member with validation (check for duplicates)

        Print the family tree as a visual diagram

        Find the longest branch (most generations)

Sample Output:
text

🌳 FAMILY TREE 🌳

👨👩👧👦 Family Members:
Joseph (Grandfather) [Generation 0]
  └── John [Generation 1]
      ├── Alice [Generation 2]
      └── Bob [Generation 2]
  └── Peter [Generation 1]
      └── Carol [Generation 2]

📊 FAMILY STATISTICS:
Total members: 7
Generations: 3
Average age: 37.8
Oldest: Joseph (88 years old)
Youngest: Carol (26 years old)

🔍 SEARCH RESULTS:
Path from root to Alice: Joseph → John → Alice
Alice's siblings: ['Bob']
Alice's cousins: ['Carol']
Alice's generation: 2

📊 MEMBERS BY GENERATION:
Generation 0: ['Joseph']
Generation 1: ['John', 'Peter']
Generation 2: ['Alice', 'Bob', 'Carol']

📏 Longest branch: Joseph → John → Alice (3 generations)

Concepts: Deeply nested dictionaries, recursion (implicit through loops), complex data traversal, set operations for finding relationships, dictionary comprehensions, advanced string formatting
'''


CURRENT_YEAR = 2026

# The raw structure exactly as given in the spec.
family_tree_raw = {
    "Grandfather": {
        "name": "Joseph",
        "spouse": "Mary",
        "children": {
            "John": {
                "birth_year": 1970,
                "spouse": "Jane",
                "children": {
                    "Alice": {"birth_year": 1995, "spouse": None, "children": {}},
                    "Bob": {"birth_year": 1998, "spouse": None, "children": {}},
                },
            },
            "Peter": {
                "birth_year": 1975,
                "spouse": "Susan",
                "children": {
                    "Carol": {"birth_year": 2000, "spouse": None, "children": {}},
                },
            },
        },
    }
}


def _get_root():
    """The raw structure wraps the root oddly ('Grandfather' -> {'name': ...}),
    unlike every other person, who is keyed directly by their own name with a
    'birth_year'. This normalizes the root into the same shape everyone else
    has, so the rest of the code can treat every person uniformly.

    NOTE: the given data has no birth_year for Joseph at all, yet the spec's
    own sample output claims 'Oldest: Joseph (88 years old)'. Working
    backwards from that (2026 - 88 = 1938) reproduces the sample's oldest AND
    youngest values exactly, so 1938 is very likely the intended value that
    was just missing from the shown code block — that's the assumption used
    here, clearly flagged rather than silently invented.
    """
    entry = family_tree_raw["Grandfather"]
    root_name = entry["name"]
    root_node = {
        "birth_year": entry.get("birth_year", 1938),
        "spouse": entry.get("spouse"),
        "children": entry.get("children", {}),  # same dict object — mutations stay in sync
    }
    return root_name, root_node


ROOT_NAME, ROOT_NODE = _get_root()


def find_node(name, _current_name=None, _current_node=None, _path=None):
    """Recursively searches the tree for `name`. Returns (node, path_list) or (None, None)."""
    if _current_name is None:
        _current_name, _current_node = ROOT_NAME, ROOT_NODE
    _path = (_path or []) + [_current_name]

    if _current_name == name:
        return _current_node, _path

    for child_name, child_node in _current_node.get("children", {}).items():
        result_node, result_path = find_node(name, child_name, child_node, _path)
        if result_node is not None:
            return result_node, result_path

    return None, None


def find_path(root_name, target_name):
    """Returns the list of names from root_name down to target_name, or None."""
    root_node, _ = find_node(root_name)
    if root_node is None:
        return None
    _, path = find_node(target_name, root_name, root_node)
    return path


def get_parent(name):
    """Returns (parent_name, parent_node), or (None, None) for the root or an unknown name."""
    def search(current_name, current_node):
        for child_name, child_node in current_node.get("children", {}).items():
            if child_name == name:
                return current_name, current_node
            found_name, found_node = search(child_name, child_node)
            if found_name is not None:
                return found_name, found_node
        return None, None

    if name == ROOT_NAME:
        return None, None
    return search(ROOT_NAME, ROOT_NODE)


def get_generation(name):
    """Root is generation 0. Returns None if the name isn't in the tree."""
    _, path = find_node(name)
    return None if path is None else len(path) - 1


def _count_descendants_node(node):
    total = 0
    for child_name, child_node in node.get("children", {}).items():
        total += 1 + _count_descendants_node(child_node)
    return total


def count_descendants(name):
    node, _ = find_node(name)
    return 0 if node is None else _count_descendants_node(node)


def _collect_names(name, node):
    names = [name]
    for child_name, child_node in node.get("children", {}).items():
        names.extend(_collect_names(child_name, child_node))
    return names


def get_family_members():
    return _collect_names(ROOT_NAME, ROOT_NODE)


def get_siblings(name):
    _, parent_node = get_parent(name)
    if parent_node is None:
        return []
    return [child_name for child_name in parent_node["children"] if child_name != name]


def get_cousins(name):
    """Children of this person's parent's siblings (i.e. children of aunts/uncles)."""
    parent_name, _ = get_parent(name)
    if parent_name is None:
        return []

    aunts_and_uncles = get_siblings(parent_name)
    cousins = []
    for au_name in aunts_and_uncles:
        au_node, _ = find_node(au_name)
        if au_node:
            cousins.extend(au_node.get("children", {}).keys())
    return cousins


def get_age(name):
    node, _ = find_node(name)
    if node is None or node.get("birth_year") is None:
        return None
    return CURRENT_YEAR - node["birth_year"]


def find_oldest():
    members = get_family_members()
    ages = {name: get_age(name) for name in members if get_age(name) is not None}
    if not ages:
        return None, None
    oldest = max(ages, key=ages.get)
    return oldest, ages[oldest]


def find_youngest():
    members = get_family_members()
    ages = {name: get_age(name) for name in members if get_age(name) is not None}
    if not ages:
        return None, None
    youngest = min(ages, key=ages.get)
    return youngest, ages[youngest]


def get_average_age():
    members = get_family_members()
    ages = [get_age(name) for name in members if get_age(name) is not None]
    return sum(ages) / len(ages) if ages else 0


def get_family_by_generation():
    """Dict comprehension + set operation: collect the distinct generation
    numbers present, then build {generation: [members]} from them."""
    members = get_family_members()
    generations = {get_generation(name) for name in members}  # set comprehension
    return {gen: [m for m in members if get_generation(m) == gen] for gen in sorted(generations)}


def find_longest_branch():
    """Returns the name-path (root to leaf) with the most generations."""
    best_path = [ROOT_NAME]

    def dfs(name, node, path):
        nonlocal best_path
        if len(path) > len(best_path):
            best_path = path
        for child_name, child_node in node.get("children", {}).items():
            dfs(child_name, child_node, path + [child_name])

    dfs(ROOT_NAME, ROOT_NODE, [ROOT_NAME])
    return best_path


def add_member(parent_name, name, birth_year, spouse=None):
    """Bonus: adds a new member under an existing parent, with duplicate checking."""
    if find_node(name)[0] is not None:
        return f"\u274c '{name}' already exists in the family tree."

    parent_node, _ = find_node(parent_name)
    if parent_node is None:
        return f"\u274c Parent '{parent_name}' not found."

    parent_node.setdefault("children", {})[name] = {
        "birth_year": birth_year,
        "spouse": spouse,
        "children": {},
    }
    return f"\u2705 Added '{name}' as a child of '{parent_name}'."


def _print_subtree(node, prefix):
    children = list(node.get("children", {}).items())
    for i, (child_name, child_node) in enumerate(children):
        is_last = (i == len(children) - 1)
        connector = "\u2514\u2500\u2500 " if is_last else "\u251c\u2500\u2500 "
        gen = get_generation(child_name)
        print(f"{prefix}{connector}{child_name} [Generation {gen}]")
        extension = "    " if is_last else "\u2502   "
        _print_subtree(child_node, prefix + extension)


def print_family_tree():
    print(f"{ROOT_NAME} (Grandfather) [Generation 0]")
    _print_subtree(ROOT_NODE, "")


def print_statistics():
    members = get_family_members()
    generations = get_family_by_generation()
    oldest_name, oldest_age = find_oldest()
    youngest_name, youngest_age = find_youngest()

    print("\n\U0001f4ca FAMILY STATISTICS:")
    print(f"Total members: {len(members)}")
    print(f"Generations: {len(generations)}")
    print(f"Average age: {get_average_age():.1f}")
    print(f"Oldest: {oldest_name} ({oldest_age} years old)")
    print(f"Youngest: {youngest_name} ({youngest_age} years old)")


def print_search_results(name):
    path = find_path(ROOT_NAME, name)
    siblings = get_siblings(name)
    cousins = get_cousins(name)
    generation = get_generation(name)

    print("\n\U0001f50d SEARCH RESULTS:")
    if path is None:
        print(f"'{name}' not found in the family tree.")
        return
    print(f"Path from root to {name}: {' \u2192 '.join(path)}")
    print(f"{name}'s siblings: {siblings}")
    print(f"{name}'s cousins: {cousins}")
    print(f"{name}'s generation: {generation}")


def print_by_generation():
    print("\n\U0001f4ca MEMBERS BY GENERATION:")
    for gen, names in get_family_by_generation().items():
        print(f"Generation {gen}: {names}")


def print_longest_branch():
    branch = find_longest_branch()
    print(f"\n\U0001f4cf Longest branch: {' \u2192 '.join(branch)} ({len(branch)} generations)")


def main():
    print("\U0001f333 FAMILY TREE \U0001f333")
    print("\n\U0001f468\u200d\U0001f469\u200d\U0001f467\u200d\U0001f466 Family Members:")
    print_family_tree()

    print_statistics()
    print_search_results("Alice")
    print_by_generation()
    print_longest_branch()

    while True:
        print("\n1. Search a family member")
        print("2. Add a new family member")
        print("3. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            name = input("Enter name: ").strip()
            print_search_results(name)
        elif choice == "2":
            parent = input("Parent's name: ").strip()
            name = input("New member's name: ").strip()
            try:
                birth_year = int(input("Birth year: ").strip())
            except ValueError:
                print("\u274c Birth year must be a number.")
                continue
            spouse = input("Spouse's name (or leave blank): ").strip() or None
            print(add_member(parent, name, birth_year, spouse))
        elif choice == "3":
            print("Goodbye! \U0001f44b")
            break
        else:
            print("\u274c Invalid choice.")
            continue


if __name__ == "__main__":
    main()