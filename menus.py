"""Reusable numbered menus with input validation.

Game scenes pass real objects to these functions and receive objects back. The
module hides numeric parsing, range checks, cancellation, and duplicate choices.
"""


def choose_option(
    title,
    options,
    label=None,
    allow_cancel=False,
    input_function=input,
):
    """Display numbered options and return one valid selected object."""
    choices = list(options)
    if not choices:
        raise ValueError("A menu needs at least one option.")

    label_function = label or str

    while True:
        print()
        print(title)
        for number, choice in enumerate(choices, start=1):
            print(f"{number}. {label_function(choice)}")
        if allow_cancel:
            print("0. Cancel")

        answer = input_function("Choose an option: ").strip()
        if not answer.isdigit():
            print("Please enter one of the displayed numbers.")
            continue

        number = int(answer)
        if allow_cancel and number == 0:
            return None
        if 1 <= number <= len(choices):
            return choices[number - 1]

        print(f"Please choose a number from 1 to {len(choices)}.")


def choose_multiple(
    title,
    options,
    count,
    label=None,
    input_function=input,
):
    """Return ``count`` distinct choices, prompting one at a time."""
    choices = list(options)
    if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
        raise ValueError("Selection count must be a positive whole number.")
    if count > len(choices):
        raise ValueError("Selection count cannot exceed the available options.")

    selected = []
    remaining = list(choices)
    label_function = label or str

    print()
    print(title)
    while len(selected) < count:
        choice = choose_option(
            f"Choice {len(selected) + 1} of {count}:",
            remaining,
            label=label_function,
            input_function=input_function,
        )
        selected.append(choice)
        remaining.remove(choice)
        print(f"Added {label_function(choice)}.")

    return selected
