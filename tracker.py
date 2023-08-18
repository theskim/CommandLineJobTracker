import json
import os
import curses

filename = "applications.json"

if not os.path.exists(filename):
    with open(filename, 'w') as f:
        json.dump([], f)
 
def read_applications():
    with open(filename, 'r') as f:
        content = f.read()
        if not content:
            return []
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Error: applications.json contains invalid data. Starting fresh.")
            return []

def add_application(stdscr):
    curses.echo()
    height, width = stdscr.getmaxyx()
    y_middle, x_middle = height // 2, width // 2

    prompts = [
        "Enter the job company: ",
        "Enter the job location: ",
        "Enter the duration: ",
        "Enter the pay: "
    ]

    responses = []
    
    for prompt in prompts:
        stdscr.clear()
        x = x_middle - len(prompt) // 2
        stdscr.addstr(y_middle, x, prompt)
        response = stdscr.getstr(y_middle + 1, x).decode("utf-8")
        if response in [ord('q'), ord('Q')]:
            return
        responses.append(response)

    company, location, duration, pay = responses
    
    selected_idx = 0
    while True:
        stdscr.clear()
        y = y_middle - len(states) // 2
        for i, state in enumerate(states):
            x = x_middle - len(state) // 2
            if i == selected_idx:
                stdscr.attron(curses.color_pair(1)) 
                stdscr.addstr(y, x, state)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, state)
            y += 1

        stdscr.addstr(height - 1, (width - len(user_instruction2)) // 2, user_instruction2)

        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]:
            return
        elif key == curses.KEY_DOWN:
            selected_idx = (selected_idx + 1) % len(states)
        elif key == curses.KEY_UP:
            selected_idx = (selected_idx - 1) % len(states)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            break

    state = states[selected_idx]

    application = {
        'company': company,
        'location': location,
        'duration': duration,
        'pay': pay,
        'state': state
    }

    applications = read_applications()
    applications.append(application)
    with open(filename, 'w') as f:
        json.dump(applications, f)

    stdscr.clear()
    success_msg = "Application added successfully!"
    x = x_middle - len(success_msg) // 2
    stdscr.addstr(y_middle, x, success_msg)
    stdscr.refresh()
    stdscr.getch()

def display_applications(stdscr):
    applications = read_applications()
    height, width = stdscr.getmaxyx()
    y_middle = height // 2

    if not applications:
        stdscr.clear()
        msg = "No applications found."
        stdscr.addstr(y_middle, (width - len(msg)) // 2, msg)
        stdscr.refresh()
        stdscr.getch()
        return
    
    total_applications = len(applications)
    total_interviews = sum(1 for app in applications if app['state'] in ["Interview", "Offer"])
    total_offers = sum(1 for app in applications if app['state'] == "Offer")
    interview_rate = total_interviews / total_applications * 100
    offer_rate = total_offers / total_applications * 100

    stats = f"Applications: {total_applications}, Interviews: {total_interviews}, Offers: {total_offers}, Interview Rate: {interview_rate:.2f}%, Offer Rate: {offer_rate:.2f}%"

    table_header = "{:<30} | {:<20} | {:<10} | {:<15} | {:<20}".format("Company", "Location", "Duration", "Pay", "State")
    table_width = len(table_header)
    start_col = (width - table_width) // 2

    offset = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, start_col, table_header)
        stdscr.addstr(1, start_col, "-" * table_width)

        display_limit = height - 4  
        for i, app in enumerate(applications[offset:offset+display_limit]):
            y = i + 2
            stdscr.addstr(y, start_col, "{:<30} | {:<20} | {:<10} | {:<15} | {:<20}".format(app['company'], app['location'], app['duration'], app['pay'], app['state']))

        stats_col = (width - len(stats)) // 2
        stdscr.addstr(height - 2, stats_col, stats)

        stdscr.addstr(height - 1, (width - len(user_instruction2)) // 2, user_instruction2)

        key = stdscr.getch()
        if key == ord('q') or key not in [curses.KEY_DOWN, curses.KEY_UP]:
            break
        elif key == curses.KEY_DOWN:
            if offset + display_limit < len(applications):
                offset += 1
        elif key == curses.KEY_UP:
            if offset > 0:
                offset -= 1

    stdscr.clear()
    stdscr.refresh()

def remove_application(stdscr):
    applications = read_applications()
    height, width = stdscr.getmaxyx()
    y_middle = height // 2

    if not applications:
        stdscr.clear()
        msg = "No applications found."
        stdscr.addstr(y_middle, (width - len(msg)) // 2, msg)
        stdscr.getch()
        return

    table_header = "{:<30} | {:<20} | {:<10} | {:<15} | {:<20}".format("Company", "Location", "Duration", "Pay", "State")
    table_width = len(table_header)
    start_col = (width - table_width) // 2
    
    selected_idx = 0
    offset = 0
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, start_col, table_header)
        stdscr.addstr(1, start_col, "-" * table_width)

        display_limit = height - 4 

        for i, app in enumerate(applications[offset:offset+display_limit]):
            y = i + 2
            display_str = "{:<30} | {:<20} | {:<10} | {:<15} | {:<20}".format(
                app['company'], 
                app['location'], 
                app['duration'],
                app['pay'], 
                app['state']
            )
            if i == selected_idx - offset:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, start_col, display_str)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, start_col, display_str)

        stdscr.addstr(height - 1, (width - len(user_instruction)) // 2, user_instruction)
        
        key = stdscr.getch()

        if key in [ord('q'), ord('Q')]:
            break

        elif key == curses.KEY_DOWN:
            if selected_idx < len(applications) - 1:
                selected_idx += 1
                if selected_idx - offset >= display_limit:
                    offset += 1

        elif key == curses.KEY_UP:
            if selected_idx > 0:
                selected_idx -= 1
                if selected_idx < offset:
                    offset -= 1

        elif key == curses.KEY_ENTER or key in [10, 13]:
            app_to_delete = applications[selected_idx]
            confirmation_msg = f"Are you sure you want to delete {app_to_delete['company']} at {app_to_delete['location']}? (y/n)"
            stdscr.addstr(height-3, (width - len(confirmation_msg)) // 2, confirmation_msg)
            stdscr.refresh()
            response = stdscr.getch()

            if response in [ord('y'), ord('Y')]:
                applications.remove(app_to_delete)
                with open(filename, 'w') as f:
                    json.dump(applications, f)
                stdscr.addstr(height - 2, (width - 24) // 2, "Application removed successfully!")
                stdscr.getch()
                break

    stdscr.clear()
    stdscr.refresh()

def modify_application(stdscr):
    applications = read_applications()
    height, width = stdscr.getmaxyx()
    y_middle = height // 2

    if not applications:
        stdscr.clear()
        msg = "No applications found."
        stdscr.addstr(y_middle, (width - len(msg)) // 2, msg)
        stdscr.getch()
        return

    selected_idx, offset = 0, 0
    while True:
        selected_idx, offset = display_and_select_application(stdscr, applications, selected_idx, offset)
        if selected_idx is None:
            return  

        application_to_modify = applications[selected_idx]
        modify_details_menu(stdscr, application_to_modify)

        with open(filename, 'w') as f:
            json.dump(applications, f)
        
        msg = "Application modified successfully. Modify another? (y/n)"
        stdscr.addstr(height - 2, (width - len(msg)) // 2, msg)
        choice = stdscr.getch()
        if choice not in [ord('y'), ord('Y')]:
            break

    stdscr.clear()
    stdscr.refresh()

def display_and_select_application(stdscr, applications, selected_idx, offset):
    height, width = stdscr.getmaxyx()
    table_header = "{:<30} | {:<20} | {:<10} | {:<15} | {:<20}".format("Company", "Location", "Duration", "Pay", "State")
    table_width = len(table_header)
    start_col = (width - table_width) // 2

    while True:
        stdscr.clear()
        stdscr.addstr(0, start_col, table_header)
        stdscr.addstr(1, start_col, "-" * table_width)

        display_limit = height - 4 
        for i, app in enumerate(applications[offset:offset+display_limit]):
            y = i + 2
            display_str = "{:<30} | {:<20} | {:<10} | {:<15} | {:<20}".format(app['company'], app['location'], app['duration'], app['pay'], app['state'])
            if i == selected_idx - offset:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, start_col, display_str)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, start_col, display_str)

        stdscr.addstr(height-1, (width - len(user_instruction)) // 2, user_instruction)

        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]:
            return None, None
        elif key == curses.KEY_DOWN:
            if selected_idx < len(applications) - 1:
                selected_idx += 1
                if selected_idx - offset >= display_limit:
                    offset += 1
        elif key == curses.KEY_UP:
            if selected_idx > 0:
                selected_idx -= 1
                if selected_idx < offset:
                    offset -= 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return selected_idx, offset

def modify_details_menu(stdscr, application):
    height, width = stdscr.getmaxyx()
    y_middle, x_middle = height // 2, width // 2

    selected_idx = 0
    while True:
        stdscr.clear()

        y = y_middle - len(application_descriptions) // 2
        for i, option in enumerate(application_descriptions):
            x = x_middle - len(option) // 2
            if i == selected_idx:
                stdscr.attron(curses.color_pair(1))  
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option)
            y += 1

        stdscr.addstr(height - 1, (width - len(user_instruction)) // 2, user_instruction)

        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]:
            break
        elif key == curses.KEY_DOWN:
            selected_idx = (selected_idx + 1) % len(application_descriptions)
        elif key == curses.KEY_UP:
            selected_idx = (selected_idx - 1) % len(application_descriptions)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_idx == 0:
                new_value = centered_input(stdscr, "Enter new company name: ")
                application['company'] = new_value
            elif selected_idx == 1:
                new_value = centered_input(stdscr, "Enter new location: ")
                application['location'] = new_value
            elif selected_idx == 2:
                new_value = centered_input(stdscr, "Enter new duration: ")
                application['duration'] = new_value
            elif selected_idx == 3:
                new_value = centered_input(stdscr, "Enter new pay: ")
                application['pay'] = new_value
            elif selected_idx == 4:
                new_state = select_state_from_menu(stdscr)
                if new_state is not None:
                    application['state'] = new_state
            elif selected_idx == 5:
                break

def select_state_from_menu(stdscr):
    height, width = stdscr.getmaxyx()
    y_middle, x_middle = height // 2, width // 2
    selected_idx = 0
    
    while True:
        stdscr.clear()
        y = y_middle - len(states) // 2
        
        for i, state in enumerate(states):
            x = x_middle - len(state) // 2
            if i == selected_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, state)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, state)
            y += 1

        stdscr.addstr(height-1, (width - len(user_instruction)) // 2, user_instruction)
        
        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]:
            return None
        elif key == curses.KEY_DOWN:
            selected_idx = (selected_idx + 1) % len(states)
        elif key == curses.KEY_UP:
            selected_idx = (selected_idx - 1) % len(states)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return states[selected_idx]
        
def centered_input(stdscr, prompt):
    height, width = stdscr.getmaxyx()
    y_middle, x_middle = height // 2, width // 2
    x = x_middle - len(prompt) // 2
    stdscr.clear()
    stdscr.addstr(y_middle, x, prompt)
    stdscr.refresh()
    curses.echo()
    value = stdscr.getstr(y_middle + 1, x).decode('utf-8')
    curses.noecho() 
    return value

def display_menu(stdscr, selected_idx):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    x_middle = width // 2

    logo_art = '''
██╗███╗░░██╗████████╗███████╗██████╗░███╗░░██╗░██████╗██╗░░██╗██╗██████╗░
██║████╗░██║╚══██╔══╝██╔════╝██╔══██╗████╗░██║██╔════╝██║░░██║██║██╔══██╗
██║██╔██╗██║░░░██║░░░█████╗░░██████╔╝██╔██╗██║╚█████╗░███████║██║██████╔╝
██║██║╚████║░░░██║░░░██╔══╝░░██╔══██╗██║╚████║░╚═══██╗██╔══██║██║██╔═══╝░
██║██║░╚███║░░░██║░░░███████╗██║░░██║██║░╚███║██████╔╝██║░░██║██║██║░░░░░
╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░

████████╗██████╗░░█████╗░░█████╗░██╗░░██╗███████╗██████╗░
╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██╔════╝██╔══██╗
░░░██║░░░██████╔╝███████║██║░░╚═╝█████═╝░█████╗░░██████╔╝
░░░██║░░░██╔══██╗██╔══██║██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
░░░██║░░░██║░░██║██║░░██║╚█████╔╝██║░╚██╗███████╗██║░░██║
░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
'''
    art_lines = logo_art.split('\n')

    for i, line in enumerate(art_lines):
        x = x_middle - len(line) // 2
        stdscr.addstr(i, x, line)
    
    separator_y = len(art_lines) + 1
    stdscr.addstr(separator_y, (width - 40) // 2, '-'*40)
    start_y = separator_y + 2

    max_display_items = (height - start_y) // 3

    start_idx = max(0, selected_idx - max_display_items + 1)
    end_idx = start_idx + max_display_items

    if selected_idx < max_display_items:
        start_idx = 0
        end_idx = max_display_items

    for i, option in enumerate(menu_options[start_idx:end_idx]):
        x = x_middle - len(option) // 2
        y = start_y + i * 3
        if i + start_idx == selected_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, option)

    stdscr.refresh()
    
def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.curs_set(0)
    current_row = 0

    while True:
        display_menu(stdscr, current_row)
        
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                add_application(stdscr)
            elif current_row == 1:
                display_applications(stdscr)
            elif current_row == 2:
                remove_application(stdscr)
            elif current_row == 3:
                modify_application(stdscr)
            elif current_row == 4:
                break

menu_options = [
    "Add a new application",
    "Display current applications",
    "Remove a job application",
    "Modify a job application",
    "Quit"
]

application_descriptions = [
    "Company",
    "Location",
    "Duration",
    "Pay",
    "State",
    "Finished Modifying"
]

states = [
    "Rejected",
    "No Response",
    "Online Assessment",
    "Interview",
    "Offer"
]

user_instruction = "\u2191 and \u2193 keys to navigate. Enter to select. q to quit."
user_instruction2 = "\u2191 and \u2193 keys to navigate. q to quit. Any other key to return to main menu."
curses.wrapper(main)
if __name__ == "__main__":
    main()