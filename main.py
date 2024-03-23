def generate_valid_scores():
    # Generate valid scores for single, double, and triple hits, plus bull and double bull
    singles = list(range(1, 21))
    doubles = [i * 2 for i in range(1, 21)]
    triples = [i * 3 for i in range(1, 21)]
    bullseyes = [25, 50]  # Bull and double bull
    return singles + doubles + triples + bullseyes

def score_description(score):
    if score == 25:
        return "Single Bull"
    elif score == 50:
        return "Double Bull"
    elif score in range(1, 21):
        return f"Single {score}"
    elif score in [i * 2 for i in range(1, 21)]:
        return f"Double {score // 2}"
    elif score in [i * 3 for i in range(1, 21)]:
        return f"Triple {score // 3}"
    else:
        return str(score)

def parse_dart_input(dart_input):
    # Parses inputs like "triple 20", "double 1", or "single bull" into their numerical score values
    parts = dart_input.lower().split()
    if len(parts) == 2:
        type, value = parts
        if type == "single":
            if value == "bull":
                return 25
            return int(value)
        elif type == "double":
            return int(value) * 2
        elif type == "triple":
            return int(value) * 3
    elif len(parts) == 1 and parts[0] == "bull":
        return 25  # Assuming "bull" means single bull
    return 0  # Invalid input or not recognized

def generate_combinations():
    valid_scores = generate_valid_scores()
    combinations = []
    for first_dart in valid_scores:
        for second_dart in valid_scores:
            for third_dart in [i * 2 for i in range(1, 21)] + [50]:  # Last dart must be a double
                combinations.append((first_dart, second_dart, third_dart))
    return combinations

def filter_combinations_for_score(combinations, target_score):
    return [combo for combo in combinations if sum(combo) == target_score]

def find_checkout(score):
    combinations = generate_combinations()
    possible_checkouts = filter_combinations_for_score(combinations, score)
    return possible_checkouts

def recalculate_checkout_with_remaining_darts(remaining_score):
    valid_scores = generate_valid_scores()
    combinations = []
    for first_dart in valid_scores:
        for second_dart in [i * 2 for i in range(1, 21)] + [50]:  # Last dart must be a double
            combinations.append((first_dart, second_dart))
    possible_checkouts = [combo for combo in combinations if sum(combo) == remaining_score]
    return possible_checkouts

def suggest_two_dart_finishes(preferred_double, remaining_score):
    valid_scores = generate_valid_scores()
    target_score = preferred_double * 2
    suggestions = []
    for first_dart in valid_scores:
        second_dart = target_score - first_dart
        if second_dart in valid_scores and sum([first_dart, second_dart]) == target_score:
            suggestions.append((first_dart, second_dart))
    return suggestions

def main():
    while True:  # Start of the loop to allow restarting the program
        score = int(input("Enter your score: "))
        checkouts = find_checkout(score)
        if checkouts:
            print("Possible checkout combinations:")
            for checkout in checkouts:
                descriptive_checkout = [score_description(score) for score in checkout]
                print(", ".join(descriptive_checkout))
        else:
            print("No checkout possible in one turn.")

        dart_input = input("Enter the score achieved with the first dart (e.g., 'triple 20', 'double 1', 'single bull'): ")
        first_dart_score = parse_dart_input(dart_input)
        remaining_score = score - first_dart_score

        if remaining_score <= 0:
            print("Checkout completed or score busted.")
            print("End of the program. Restarting...")
            continue  # Restart the program by continuing the loop

        new_checkouts = recalculate_checkout_with_remaining_darts(remaining_score)
        if new_checkouts:
            print("For the remaining score, possible checkouts are:")
            for checkout in new_checkouts:
                descriptive_checkout = [score_description(score) for score in checkout]
                print(", ".join(descriptive_checkout))
        else:
            print("No checkout possible with two darts.")
            preferred_double = int(input("Enter your preferred double to leave (e.g., 16 for Double 16): "))
            score_to_leave_preferred_double = preferred_double * 2
            if remaining_score > score_to_leave_preferred_double:
                print(f"Aim to leave {score_to_leave_preferred_double} for a Double {preferred_double} finish.")
                two_dart_suggestions = suggest_two_dart_finishes(preferred_double, remaining_score - score_to_leave_preferred_double)
                if two_dart_suggestions:
                    print("Suggested 2-dart finishes to leave your preferred double:")
                    for suggestion in two_dart_suggestions:
                        descriptive_suggestion = [score_description(score) for score in suggestion]
                        print(", ".join(descriptive_suggestion))
                    print("End of the program. Restarting...")
                    continue  # Restart the program by continuing the loop
                else:
                    print("No two-dart finish can leave the preferred double. Consider a different strategy.")
            else:
                print("Not enough score to leave the preferred double. Aim for a lower score or check out directly if possible.")
            print("End of the program. Restarting...")
            continue  # Restart the program by continuing the loop

if __name__ == "__main__":
    main()
