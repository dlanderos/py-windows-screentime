def pretty_print_result(
        process: str,
        titles: set[str],
        gross_active_time: int,
        share_active_time: float,
        average_screen_area: int,
        share_screen_area: float
):
    def pretty_duration(duration: int) -> str:
        seconds = (duration / 1000) % 60
        minutes = int((duration / 60000) % 60)
        minutes_string = ("%d minutes " % minutes if minutes != 0 else "")
        hours = int((duration / 3600000) % 24)
        hours_string = ("%d hours " % hours if hours != 0 else "")
        return "%s%s%.1f seconds" % (hours_string, minutes_string, seconds)

    labeled_values = {
        "Program": "%s" % process.split("\\")[-1],
        ("Titles" if len(titles) > 1 else "Title"): ", ".join(map(lambda s: "\"%s\"" % s, titles)),
        "Gross Active Time": pretty_duration(gross_active_time),
        "Share Active Time": "%.2f percent" % (share_active_time * 100),
        "Average Screen Area": "{:,} pixels squared".format(average_screen_area),
        "Share Screen Area": "%.2f percent" % (share_screen_area * 100),
    }

    # Get the largest label
    spacing_count = 2
    max_length_label = 0
    for key in labeled_values.keys():
        if len(key) > max_length_label:
            max_length_label = len(key)
    max_length_label += spacing_count

    # Print the results
    for key, value in labeled_values.items():
        required_length_gain = max_length_label - len(key)
        spacer_string = " " * required_length_gain
        print(f"{key}:{spacer_string}{value}")
    print("")