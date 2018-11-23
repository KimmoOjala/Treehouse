import re
from entry import Entry


class Search:
    '''Class containing functionality for searches of Work Log entries'''

    browse_index = 1

    def __init__(self):
        '''Constructor'''

    def entry_to_string(self, entry):
        '''Takes in entry. Prints Work_Log ID and current value
        of all fields.'''
        Entry().clear_screen()
        print("\n")
        date_str = entry.date_field.strftime('%d/%m/%Y')
        time_spent = int(entry.time_spent_field)
        entry_string = '''Work Log ID: {}; Name: {} {};
Date of the task: {}; Title of the task: {}; Time spent: {}; Notes: {};
        '''.format(entry.id, entry.first_name_field, entry.last_name_field,
                   date_str, entry.task_title_field, time_spent,
                   entry.notes_field)
        return entry_string

    def choose_search(self):
        '''Search and edit entries'''
        Entry().clear_screen()
        print("\n")
        search_choice = input("Do you want to search by:""\n"
                              "a) Employee""\n"
                              "b) Date""\n"
                              "c) Date Range""\n"
                              "d) Time Spent""\n"
                              "e) Term""\n"
                              "\n""Please enter the order letter of"
                              " the search or \"R\" to return to menu: "
                              ).lower()

        available_choices = ["a", "b", "c", "d", "e", "r"]
        entries = []
        while(True):
            if search_choice in available_choices:
                if search_choice == 'a':
                    entries_same_name = self.employee_search()
                    if len(entries_same_name) != 0:
                        entries = self.employee_entries_select(entries_same_name)
                    break
                elif search_choice == 'b':
                    datetime_object = self.date_prompt()
                    date_r = (datetime_object, datetime_object)
                    entries = self.date_search(date_r)
                    break
                elif search_choice == 'c':
                    date_r = self.date_range_prompt()
                    entries = self.date_search(date_r)
                    break
                elif search_choice == 'd':
                    time_spent_int = self.time_spent_prompt()
                    entries = self.time_spent_search(time_spent_int)
                    break
                elif search_choice == 'e':
                    term = self.term_prompt()
                    entries = self.term_search(term)
                    break
                elif search_choice == 'r':
                    break
            else:
                search_choice = input("Please enter \"a\", \"b\", \"c\","
                                      " \"d\", \"e\" or \"R\": "
                                      ).lower().strip()
        if search_choice != "r":
            if len(entries) > 0:
                self.browse_one_by_one(entries)
            if len(entries) == 0:
                input("Your search did not find any results. Please press"
                      " enter to return to menu.")

    def employee_search(self):
        Entry().clear_screen()
        print("\n")
        print("You can enter a first name and a last name."
              " If you want to search by:\n"
              "-just a first name\n-just a last name\npress enter when"
              " prompted to enter the first/last name.\n")
        first_name = input("Please enter the first name of the employee: "
                           ).strip()
        last_name = input("Please enter the last name of the employee: "
                          ).strip()
        entries_same_name = []
        if first_name != "" and last_name != "":
            entries_same_name = Entry.select().where((Entry.first_name_field == first_name) & (Entry.last_name_field == last_name))
        elif first_name == "" and last_name != "":
            entries_same_name = Entry.select().where(Entry.last_name_field == last_name)
        elif first_name != "" and last_name == "":
            entries_same_name = Entry.select().where(Entry.first_name_field == first_name)
        return entries_same_name

    def employee_entries_select(self, entries_same_name):
        Entry().clear_screen()
        print("\nYour search found the following employees:")
        names = []
        for entry in entries_same_name:
            first_name = entry.first_name_field
            last_name = entry.last_name_field
            name = "{} {}".format(entry.first_name_field, entry.last_name_field)
            names.append(name)
        names_set = set(names)
        names_list = list(names_set)
        counter = 1
        for name in names_list:
            print("{}) {}".format(counter, name))
            counter += 1
        order_number = input("\nTo view Work Log entries please enter the"
                             " order number of the employee: ")
        order_numbers = range(1, counter)
        while(True):
            try:
                if int(order_number) in order_numbers:
                    break
                elif int(order_number) not in order_numbers:
                    order_number = input("Please enter a valid order number: ")
            except(ValueError):
                order_number = input("Please enter a valid order number: ")
        name = names_list[int(order_number)-1]
        employee_name_l = name.split()
        first_name = employee_name_l[0]
        last_name = employee_name_l[1]
        entries = Entry.select().where((Entry.first_name_field == first_name) & (Entry.last_name_field == last_name))
        return entries

    def date_range_prompt(self):
        '''Prompts user for starting and ending date of a date range.
        Calls date_validation method to validate user input. Returns
        starting and ending date as a tuple of datetime objects.'''
        Entry().clear_screen()
        print("\n")
        while(True):
            start_date_string = input("Please enter the starting date of"
                                      " the date range, as DD/MM/YYYY: ")
            start_datetime_object = Entry().date_validation(start_date_string)
            end_date_string = input("Please enter the ending date of the"
                                    " date range, as DD/MM/YYYY: ")
            end_datetime_object = Entry().date_validation(end_date_string)
            if end_datetime_object < start_datetime_object:
                print("The ending date must be equal to or later than "
                      "the starting date.")
            else:
                break
        date_r = (start_datetime_object, end_datetime_object)
        return date_r

    def date_prompt(self):
        '''Prompts user for a date.
        Calls date_validation method to validate user input. Returns
        date as datetime object.'''
        Entry().clear_screen()
        print("\n")
        date_string = input("Please enter the search date as DD/MM/YYYY: ")
        datetime_object = Entry().date_validation(date_string)
        return datetime_object

    def date_search(self, date_r):
        '''Takes in starting date (datetime object) and ending date
        (datetime object) as a tuple. Searches records in Work Log with
        'Date of Task' between starting and ending date
        (including starting date and ending date) of date range. Returns
        search results as a list of entries.'''
        entries = []
        start_datetime, end_datetime = date_r
        if start_datetime != end_datetime:
            entries = Entry.select().where(Entry.date_field.between(start_datetime, end_datetime))
        elif start_datetime == end_datetime:
            entries = Entry.select().where(Entry.date_field == start_datetime)
        return entries

    def time_spent_prompt(self):
        '''Prompts user to enter time spent on task in minutes.
        Calls date_validation method to validate user input. Returns
        time spent as an integer.'''
        Entry().clear_screen()
        print("\n")
        time_spent_string = input("Please enter the number of minutes (rounded)"
                                  " for search by time spent on task: ")
        time_spent_int = Entry().minutes_validation(time_spent_string)
        return time_spent_int

    def time_spent_search(self, time_spent_int):
        '''Takes in value of "Time spent" as integer.
        Searches records in Work log with same value.
        Returns search results as a list of entries.'''
        entries = []
        entries = Entry.select().where(Entry.time_spent_field == time_spent_int)
        return entries

    def term_prompt(self):
        '''Prompts user to enter search term. Returns search term.'''
        Entry().clear_screen()
        print("\n")
        term = input("Please enter what you want to search in "
                     "the fields \"Title of the task\" or ""\n"
                     "\"Notes\" of the Work Log entry: ")
        while(True):
            if term == "":
                term = input("Please enter a search term: ")
            else:
                break
        return term

    def term_search(self, term):
        '''Takes in search term. Searches term in fields
        "Title of the task" and "Notes" of the Work Log.
        Returns search results as a list of entries.'''
        entries = []
        entries = Entry.select().where(Entry.task_title_field.regexp(term) | Entry.notes_field.regexp(term))
        return entries

    def browse_one_by_one(self, entries):
        '''Takes in search list. Contains functionality for browsing records
        in search list one-by-one. Calls search_to_string_list to print
        first item on list as a string. Calls print_next_result and
        print_previous_result to print next/previous records in list.
        Keeps track of browse position in search list by
        updating Search.browse_index. If user chooses, calls appropriate
        function to edit or delete the entry. Passes on index number of
        the entry. If user chooses to edit the entry passes also on
        the key of the value the user chooses to edit.'''
        Entry().clear_screen()
        Search.browse_index = 1
        string_entries = []
        for entry in entries:
            entry_string = self.entry_to_string(entry)
            string_entries.append(entry_string)
        self.print_next_result(string_entries)
        available_choices = ["N", "P", "E", "R"]
        while(True):
            choice = input("\n""Please enter [N]ext, [P]revious, "
                           "[E]dit/delete or "
                           "[R]eturn to menu: "
                           ).upper()
            if choice in available_choices:
                if choice == "N":
                    Search.browse_index += 1
                    self.print_next_result(string_entries)
                    if Search.browse_index > len(string_entries):
                        Search.browse_index = len(string_entries)
                elif choice == "P":
                    Search.browse_index -= 1
                    self.print_previous_result(string_entries)
                    if Search.browse_index == 0:
                        Search.browse_index = 1
                elif choice == "E":
                    entry_string = string_entries[Search.browse_index-1]
                    id_number = self.id_number_from_string(entry_string)
                    Entry().edit_choice_loop(id_number)
                    break
                elif choice == "R":
                    break
            else:
                input("That was not a valid entry. Please press enter."
                      ).upper()

    def print_next_result(self, string_entries):
        '''Takes in list of search results as strings. Prints next record
        on list and updates Search.browse_index.'''
        Entry().clear_screen()
        print("\n")
        if Search.browse_index <= len(string_entries):
            print("Result {} of {}:".format(Search.browse_index, len(string_entries)))
            print("\n"+string_entries[Search.browse_index-1])
        else:
            print("Result {} of {}:".format(len(string_entries), len(string_entries)))
            print("\n"+string_entries[len(string_entries)-1])
            print("There are no further Work Log entries")

    def print_previous_result(self, string_entries):
        '''Takes in list of search results as strings. Prints preceding
        record on list and updates Search.browse_index.'''
        Entry().clear_screen()
        print("\n")
        if Search.browse_index >= 1:
            print("Result {} of {}:".format(Search.browse_index, len(string_entries)))
            print("\n"+string_entries[Search.browse_index-1])
        else:
            print("Result 1 of {}:".format(len(string_entries)))
            print("\n"+string_entries[0])
            print("There are no previous Work Log entries")

    def id_number_from_string(self, entry_string):
        '''Takes in Work Log record as a string. Searches ID number in
        string. Returns ID number.'''
        m = re.search(r'\d+', entry_string)
        id_number = int(m.group())
        return id_number
