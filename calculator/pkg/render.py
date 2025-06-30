def render(expression, result):
    """
    isinstance checks if result is float
    is_integer checks if float can be coverted to integer value
    5.0 is True but 5.1 is False
    """
    if isinstance(result, float) and result.is_integer():
        result_str = str(int(result))
    else:
        result_str = str(result)

    # determines how big render should
    # chooses max width from expression and result and adds 4 for padding
    box_width = max(len(expression), len(result_str)) + 4

    box = []
    box.append("┌" + "-" * box_width + "┐")

    box.append(
        "│" + " " * 2 + expression + " " * (box_width - len(expression) - 2) + "│"
    )
    box.append("│" + " " * box_width + "│")
    box.append("│" + " " * 2 + "=" + " " * (box_width - 3) + "│")
    box.append("│" + " " * box_width + "│")
    box.append(
        "│" + " " * 2 + result_str + " " * (box_width - len(result_str) - 2) + "│"
    )
    box.append("└" + "─" * box_width + "┘")
    return "\n".join(box)
