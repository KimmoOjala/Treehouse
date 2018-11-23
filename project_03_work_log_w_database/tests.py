import unittest
import io
import datetime
from work_log import *
from entry import *
from search import Search


class Test(unittest.TestCase):
    '''Test cases for program.'''

    def test_db_initialization(self):
        '''Test whether db is initilized correctly.'''
        db.close()
        Entry().initialize()
        assert db.get_tables() == ['entry']

    def save_entry(self, datetime_object, first_name, last_name, task_title, time_spent, notes):
        '''Method used in test cases to save a test entry.'''
        Entry.create(date_field=datetime_object,
                     first_name_field=first_name,
                     last_name_field=last_name,
                     task_title_field=task_title,
                     time_spent_field=time_spent,
                     notes_field=notes)

    def test_correct_date_string_validation(self):
        '''Tests whether date_validation method correctly validates
        and converts a date.'''
        assert isinstance(Entry().date_validation("15/10/1900"), datetime.datetime)

    def test_string_validation(self):
        '''Tests whether string_validation method correctly validates a string.'''
        assert Entry().string_validation("string", "a task title") == "string"

    def test_minutes_validation(self):
        '''Tests whether minutes_validation method correctly
        validates an integer.'''
        assert Entry().minutes_validation("15") == 15

    def test_print_entry(self):
        '''Tests whether print_entry method correctly prints an entry.'''
        self.save_entry(datetime.datetime.now(), "Stephen", "Johnson", "feature_1", 15, "")
        entry = Entry.get(first_name_field="Stephen")
        work_log_id = entry.id
        captured_print = io.StringIO()
        sys.stdout = captured_print
        Entry().print_entry_field(entry, "Title of the task")
        sys.stdout = sys.__stdout__
        captured_string = captured_print.getvalue()
        string = "Work Log ID: {} / Title of the task: feature_1".format(str(work_log_id))
        assert captured_string.strip() == string.strip()

    def test_entry_to_string(self):
        '''Tests whether entry_to_string correctly turns an entry
        into a string.'''
        self.save_entry(datetime.datetime.now(), "David", "Johnson", "feature_1", 15, "")
        entry = Entry.get(first_name_field="David")
        date_str = entry.date_field.strftime('%d/%m/%Y')
        test_string = '''Work Log ID: {}; Name: {} {};
Date of the task: {}; Title of the task: {}; Time spent: {}; Notes: {};
        '''.format(entry.id, entry.first_name_field, entry.last_name_field,
                   date_str, entry.task_title_field, str(15),
                   entry.notes_field)
        assert Search().entry_to_string(entry) == test_string

    def test_date_search(self):
        '''Tests whether date_search method returns correct search result.'''
        date_string = "24/12/2000"
        datetime_object = datetime.datetime.strptime(date_string, '%d/%m/%Y')
        self.save_entry(datetime_object, "Bill", "Johnson", "feature_1", 15, "")
        date_r = (datetime_object, datetime_object)
        assert Search().date_search(date_r) == Entry.select().where(Entry.date_field == datetime_object)

    def test_date_range_search(self):
        '''Tests whether date_range_search method returns correct search result.'''
        date_string_start = "24/12/2000"
        date_string_end = "25/12/2000"
        start_datetime = datetime.datetime.strptime(date_string_start, '%d/%m/%Y')
        end_datetime = datetime.datetime.strptime(date_string_end, '%d/%m/%Y')
        self.save_entry(start_datetime, "Bill", "Johnson", "feature_1", 15, "")
        self.save_entry(end_datetime, "Bill", "Johnson", "feature_1", 15, "")
        date_r = (start_datetime, end_datetime)
        assert Search().date_search(date_r) == Entry.select().where(Entry.date_field.between(start_datetime, end_datetime))

    def test_time_spent_search(self):
        '''Tests whether time_spent_search method returns correct search result.'''
        self.save_entry(datetime.datetime.now(), "Bill", "Johnson", "feature_1", 21, "")
        assert Search().time_spent_search(21) == Entry.select().where(Entry.time_spent_field == 21)

    def test_term_search(self):
        '''Tests whether term_search method returns correct search result.'''
        self.save_entry(datetime.datetime.now(), "Bill", "Johnson", "Helsinki", 21, "")
        assert Search().term_search("Helsinki") == Entry.select().where(Entry.task_title_field.regexp("Helsinki") | Entry.notes_field.regexp("Helsinki"))

    def test_id_number_from_string(self):
        '''Tests whether id_number_from_string returns
        correct id number from string_entry.'''
        self.save_entry(datetime.datetime.now(), "Mary", "Johnson", "Helsinki", 21, "")
        entry = Entry.get(first_name_field="Mary")
        work_log_id = entry.id
        string_entry = Search().entry_to_string(entry)
        assert Search().id_number_from_string(string_entry) == work_log_id

    def test_add_entry(self):
        '''Tests whether user can enter correct first name and whether
        add_entry method saves data correctly.
        When prompted enter: "12/12/1212"; "Tom" ; "Johnson"; "test" ; "12"; "test".'''
        Entry().add_entry()
        assert Entry.get(first_name_field="Tom").first_name_field == "Tom"

    def test_employee_search(self):
        '''Tests whether user can enter a first and a last name and
        whether test_employee_search method returns correct entries.
        When prompted enter: "Linda" and "Johnson".'''
        self.save_entry(datetime.datetime.now(), "Linda", "Johnson", "Helsinki", 21, "")
        entries_same_name = Entry.select().where((Entry.first_name_field == "Linda") & (Entry.last_name_field == "Johnson"))
        assert Search().employee_search() == entries_same_name

    def test_delete_entry(self):
        '''Tests whether user can delete an entry.
        When prompted enter "y".'''
        self.save_entry(datetime.datetime.now(), "Alfred", "Johnson", "feature_1", 15, "")
        entry = Entry.get(first_name_field="Alfred")
        work_log_id = entry.id
        Entry().delete_entry(work_log_id)
        with self.assertRaises(DoesNotExist):
            Entry.get(first_name_field="Alfred")

    def test_time_spent_prompt(self):
        '''Tests whether user can enter value for time spent in time_spent_prompt method.
        When prompted enter: "12".'''
        assert Search().time_spent_prompt() == 12

    def test_term_prompt(self):
        '''Tests whether user can enter value for time spent in term_prompt method.
        When prompted enter: "test".'''
        assert Search().term_prompt() == "test"

    def test_date_range_prompt(self):
        '''Tests if date_range_prompt method returns correct tuple.
        When prompted enter: "12/12/1212" and "12/12/1212".'''
        start_date = datetime.datetime.strptime("12/12/1212", '%d/%m/%Y')
        end_date = datetime.datetime.strptime("12/12/1212", '%d/%m/%Y')
        date_r = (start_date, end_date)
        assert Search().date_range_prompt() == date_r

    def test_date_prompt(self):
        '''Tests if date_prompt method returns correct datetime object.
        When prompted enter: "12/12/1212".'''
        date = datetime.datetime.strptime("12/12/1212", '%d/%m/%Y')
        assert Search().date_prompt() == date

    def test_employee_entries_select_valid(self):
        '''Tests if user can select valid entries in
        employee_entries_select method.
        When prompted enter: "1".'''
        self.save_entry(datetime.datetime.now(), "Beth", "Johnson", "Helsinki", 21, "")
        entries_same_name = Entry.select().where((Entry.first_name_field == "Beth") & (Entry.last_name_field == "Johnson"))
        assert Search().employee_entries_select(entries_same_name) == entries_same_name


if __name__ == '__main__':
    unittest.main()
