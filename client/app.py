import curses
import textwrap

# Global data storage
context = {
    "main_section_lines": [],  # Tracks lines for the main section
    "top_pane_lines": [],      # Tracks lines for the top pane
    "bottom_pane_lines": [],   # Tracks lines for the bottom pane
    "max_main_lines": 0,       # Maximum lines in the main section
    "max_side_lines": 0,       # Maximum lines in the side panes
    "main_width": 0,           # Width of the main section
    "side_width": 0,           # Width of the side panes
}

def write_to_main(main_win, new_text):
    """
    Write a new line or wrapped text to the main section.
    """
    global context
    wrapped_lines = textwrap.wrap(new_text, context["main_width"] - 4)  # Account for borders
    for line in wrapped_lines:
        if len(context["main_section_lines"]) >= context["max_main_lines"]:
            context["main_section_lines"].pop(0)  # Remove the oldest line
        context["main_section_lines"].append(line)
    
    # Redraw the Chat Window
    main_win.clear()
    main_win.box()
    main_win.addstr(0, 2, " Chat Window ", curses.color_pair(1) | curses.A_BOLD)
    line_y = 2
    for line in context["main_section_lines"]:
        main_win.addstr(line_y, 2, line, curses.color_pair(2))
        line_y += 1
    main_win.refresh()

def write_to_top_pane(top_pane, new_text):
    """
    Append a line of text to the top pane, handling overflow.
    """
    global context
    wrapped_lines = textwrap.wrap(new_text, context["side_width"] - 4)  # Account for borders
    for line in wrapped_lines:
        if len(context["top_pane_lines"]) >= context["max_side_lines"]:
            context["top_pane_lines"].pop(0)  # Remove the oldest line
        context["top_pane_lines"].append(line)
    
    # Redraw the Active Users
    top_pane.clear()
    top_pane.box()
    top_pane.addstr(0, 2, " Active Users ", curses.color_pair(1) | curses.A_BOLD)
    line_y = 2
    for line in context["top_pane_lines"]:
        top_pane.addstr(line_y, 2, line, curses.color_pair(3))
        line_y += 1
    top_pane.refresh()

def write_to_bottom_pane(bottom_pane, new_text):
    """
    Append a line of text to the bottom pane, handling overflow.
    """
    global context
    wrapped_lines = textwrap.wrap(new_text, context["side_width"] - 4)  # Account for borders
    for line in wrapped_lines:
        if len(context["bottom_pane_lines"]) >= context["max_side_lines"]:
            context["bottom_pane_lines"].pop(0)  # Remove the oldest line
        context["bottom_pane_lines"].append(line)
    
    # Redraw the Bottom Pane
    bottom_pane.clear()
    bottom_pane.box()
    bottom_pane.addstr(0, 2, " Groups ", curses.color_pair(1) | curses.A_BOLD)
    line_y = 2
    for line in context["bottom_pane_lines"]:
        bottom_pane.addstr(line_y, 2, line, curses.color_pair(4))
        line_y += 1
    bottom_pane.refresh()

def handle_user_input(main_win, footer, key, user_input):
    """
    Handles user input and updates the footer or processes special keys.
    Returns the updated `user_input` and whether to exit the program.
    """
    global context
    exit_program = False
    height, width = footer.getmaxyx()

    if key == 27:  # ESC to exit
        exit_program = True
    elif key in (curses.KEY_ENTER, 10):  # Handle Enter key
        if user_input.strip():
            write_to_main(main_win, user_input.strip())
        user_input = ""
        footer.clear()
        footer.addstr(0, 0, "Type here: ", curses.A_BOLD)
    elif key in (curses.KEY_BACKSPACE, 127):  # Handle Backspace
        if len(user_input) > 0:
            user_input = user_input[:-1]  # Remove last character
    elif key >= 32 and key <= 126:  # Printable ASCII characters
        user_input += chr(key)  # Add character to input

    # Truncate input to fit within footer width
    truncated_input = user_input[-(width - len("Type here: ") - 1):]
    footer.clear()
    footer.addstr(0, 0, "Type here: ", curses.A_BOLD)
    footer.addstr(0, len("Type here: "), truncated_input)
    footer.refresh()

    return user_input, exit_program

def clear_main_section(main_win):
    """
    Clears all content from the main section.
    """
    global context
    context["main_section_lines"].clear()  # Clear the stored lines
    main_win.clear()
    main_win.box()
    main_win.addstr(0, 2, " Chat Window ", curses.color_pair(1) | curses.A_BOLD)
    main_win.refresh()

def clear_top_pane(top_pane):
    """
    Clears all content from the top pane.
    """
    top_pane.clear()
    top_pane.box()
    top_pane.addstr(0, 2, " Active Users ", curses.color_pair(1) | curses.A_BOLD)
    top_pane.refresh()

def clear_bottom_pane(bottom_pane):
    """
    Clears all content from the bottom pane.
    """
    bottom_pane.clear()
    bottom_pane.box()
    bottom_pane.addstr(0, 2, " Groups ", curses.color_pair(1) | curses.A_BOLD)
    bottom_pane.refresh()

def clear_all_panes(main_win, top_pane, bottom_pane):
    """
    Clears all three panes: main, top, and bottom.
    """
    clear_main_section(main_win)
    clear_top_pane(top_pane)
    clear_bottom_pane(bottom_pane)

def main(stdscr):
    global context

    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Header color
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Main content
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Active Users content
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Bottom Pane content
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Footer

    # Clear and refresh the screen
    stdscr.clear()
    
    # Get screen dimensions
    height, width = stdscr.getmaxyx()
    
    # Calculate dimensions
    context["main_width"] = 4 * width // 5
    context["side_width"] = width - context["main_width"]
    side_height = height - 1  # Exclude footer height
    half_side_height = side_height // 2
    context["max_main_lines"] = side_height - 2  # Account for borders
    context["max_side_lines"] = half_side_height - 2  # Account for borders

    # Create windows
    main_win = stdscr.subwin(side_height, context["main_width"], 0, 0)  # Main section content
    top_pane = stdscr.subwin(half_side_height, context["side_width"], 0, context["main_width"])  # Top pane content
    bottom_pane = stdscr.subwin(half_side_height, context["side_width"], half_side_height, context["main_width"])  # Bottom pane content
    footer = stdscr.subwin(1, width, height - 1, 0)  # Footer input

    # Draw static borders for the panes
    main_win.box()
    top_pane.box()
    bottom_pane.box()

    # Add headers inside boxes
    main_win.addstr(0, 2, " Chat Window ", curses.color_pair(1) | curses.A_BOLD)
    top_pane.addstr(0, 2, " Active Users ", curses.color_pair(1) | curses.A_BOLD)
    bottom_pane.addstr(0, 2, " Groups ", curses.color_pair(1) | curses.A_BOLD)

    # Footer settings
    footer.bkgd(curses.color_pair(5))
    footer.addstr(0, 0, "Type here: ", curses.A_BOLD)
    footer.refresh()

    # Footer interaction
    user_input = ""
    exit_program = False

    clear_all_panes(main_win,top_pane,bottom_pane)

    while not exit_program:
        key = footer.getch()
        user_input, exit_program = handle_user_input(main_win, footer, key, user_input)

if __name__ == "__main__":
    curses.wrapper(main)