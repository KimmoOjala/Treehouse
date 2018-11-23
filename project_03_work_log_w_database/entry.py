import datetime
import os

from peewee import *

db = SqliteDatabase('work_log_5.db')


class Entry(Model):
    date_field = DateTimeField()
    task_title_field = TextField()
    first_name_field = CharField()
    last_name_field = CharField()
    time_spent_field = IntegerField()
    notes_field = TextField()

    class Meta:
        database = db

    def initialize(self):
        """Create the database and the table if they don't exist."""
        db.connect()
        db.create_tables([Entry], safe=True)

    def date_validation(self, date_string):
        '''Validates compliance of date with date format. Loops until
        user enters a valid date. Returns date in datetime format.'''
        while(True):
            try:
                datetime_object = datetime.datetime.strptime(date_string, '%d/%m/%Y')
                break
            except ValueError:
                date_string = input("That was not a valid Entry. "
                                    "Please use DD/MM/YYYY: ")
                continue
        return datetime_object

    def string_validation(self, entry_string, field_text):
        '''Checks whether entry_string is an empty string. Prompts and
        loops until user enters a string. Returns the original string.'''
        while(True):
            if entry_string != "":
                break
            else:
                entry_string = input("Please enter {}: ".format(field_text))
        return entry_string

    def minutes_validation(self, time_spent):
        '''Validates whether a value can be converted to an integer.
        Loops until user enters an integer. Returns time spent as an
        integer.'''
        while(True):
            try:
                int(time_spent)
                break
            except ValueError:
                time_spent = input("That was not a valid Entry. "
                                   "Please enter rounded minutes: ")
        return int(time_spent)

    def add_entry(self):
        """Add an entry"""
        self.clear_screen()
        print("\n")
        date_string = input("Please enter the date of the task,"
                            " use DD/MM/YYYY: ")
        datetime_object = self.date_validation(date_string)
        first_name = input("Please enter your first name: ").strip()
        first_name = self.string_validation(first_name, "your first name")
        last_name = input("Please enter your last name: ").strip()
        last_name = self.string_validation(last_name, "your last name")
        task_title = input("Please enter the title of the task: ").strip()
        task_title = self.string_validation(task_title, "the title of the task")
        time_spent = input("Please enter time spent (rounded minutes): ")
        time_spent = self.minutes_validation(time_spent)
        notes = input("Notes (Optional, you can leave this empty): ")
        if input('Save entry? [Yn] ').lower() != 'n':
            Entry.create(date_field=datetime_object,
                         first_name_field=first_name,
                         last_name_field=last_name,
                         task_title_field=task_title,
                         time_spent_field=time_spent,
                         notes_field=notes)
            input("The entry has been saved."
                  " Please press enter to return to menu.")

    def edit_choice_loop(self, id_number):
        '''Takes in entry. Prompts the user to choose what to edit
        in the Work Log Entry or if user chooses to delete the entry.
        Calls enter_save_new_field_value and delete_entry methods
        and passes on id number of entry. Passes on the field to be
        edited to enter_save_new_field_value method.'''
        self.clear_screen()
        print("\n")
        choice = input("Please enter the below order letter to:""\n"
                       "a) edit the Date of the task ""\n"
                       "b) edit the Title of the task ""\n"
                       "c) edit Time Spent""\n"
                       "d) edit Notes""\n"
                       "e) delete the Work Log entry""\n"
                       "To return to menu enter \"R\".""\n"
                       ).lower()
        choices = ["a", "b", "c", "d", "e", "r"]
        while(True):
            if choice in choices:
                if choice == "a":
                    self.print_entry_field(id_number, "Date of the task")
                    self.enter_save_new_field_value(id_number, "Date of the task")
                    break
                elif choice == "b":
                    self.print_entry_field(id_number, "Title of the task")
                    self.enter_save_new_field_value(id_number, "Title of the task")
                    break
                elif choice == "c":
                    self.print_entry_field(id_number, "Time spent")
                    self.enter_save_new_field_value(id_number, "Time spent")
                    break
                elif choice == "d":
                    self.print_entry_field(id_number, "Notes")
                    self.enter_save_new_field_value(id_number, "Notes")
                    break
                elif choice == "e":
                    self.delete_entry(id_number)
                    break
                elif choice == "r":
                    break
            else:
                choice = input("That was not a valid entry.")
                continue

    def print_entry_field(self, id_number, field_str):
        '''Takes in ID number of entry and name of field to be edited.
        Prints Work_Log ID and current value of field.'''
        Entry().clear_screen()
        print("\n")
        entry = Entry.get(Entry.id == id_number)
        if field_str == "Date of the task":
            work_str = entry.date_field.strftime('%d/%m/%Y')
        elif field_str == "Title of the task":
            work_str = entry.task_title_field
        elif field_str == "Time spent":
            work_str = str(entry.time_spent_field)
        elif field_str == "Notes":
            work_str = entry.notes_field
        print("Work Log ID: {} / {}: {}".format(entry.id, field_str, work_str))

    def enter_save_new_field_value(self, id_number, field_str):
        '''Takes in entry and name of field to be edited.
        Prompts the user to enter new value for field.
        Saves the new value.'''
        entry = Entry.get(Entry.id == id_number)
        new_value = input("Please enter "
                          "new value: ")
        if field_str == "Date of the task":
            validated_value = self.date_validation(new_value)
            entry.date_field = validated_value
        elif field_str == "Title of the task":
            validated_value = self.string_validation(new_value, "the title of the task")
            entry.task_title_field = validated_value
        elif field_str == "Time spent":
            validated_value = self.minutes_validation(new_value)
            entry.time_spent_field = validated_value
        elif field_str == "Notes":
            entry.notes_field = new_value
        entry.save()
        print("The new value has been saved")
        input("Please press enter to return to menu.")

    def delete_entry(self, id_number):
        """Delete an entry"""
        Entry().clear_screen()
        print("\n")
        entry = Entry.get(Entry.id == id_number)
        print('''Work Log entry with ID number {} will be deleted.
'''.format(id_number))
        if input("Are you sure? [yN] ").lower() == 'y':
            entry.delete_instance()
            print("The entry has been deleted")

    def clear_screen(self):
        '''Clears screen'''
        os.system('cls' if os.name == 'nt' else 'clear')
