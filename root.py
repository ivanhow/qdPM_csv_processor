from tkinter import *
# import pandas
import time
from tkinter import filedialog, ttk
from calculations import *
# import numpy
import threading


class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title('qdPM extract')
        # self.iconbitmap('dsn_logo.ico')
        self.data_qdpm = None
        self.data_operators = None
        self.minsize(640, 400)
        self.qdpm_button = Button(text='Load qdPM data', command=self.qdpm_data_to_df).grid(column=0, row=0)
        self.qdpm_frame = Frame(self).grid(column=0, row=1)
        self.progress = ttk.Progressbar(self.qdpm_frame, orient=HORIZONTAL, length=200, mode='indeterminate')
        self.progress.grid(column=0, row=3, sticky=W, padx=100)
        self.text_qdpm = Label(self.qdpm_frame,
                               text='Load the combined csv file exported from qdPM. '
                                    'There should be 5 columns below ("Name", "Type", "Assigned to", '
                                    '"Est. Time" and "QC Time") and the text should be readable.',
                               width=143).grid(column=0, row=1)

        self.placeholder_qdpm = Text(self.qdpm_frame, height=14, width=125)
        self.placeholder_qdpm.insert(END, 'Instructions for the CSV input:\n'
                                          '1. Export the files for the month from qdPM.\n'
                                          '2. Combine them into one CSV in Excel.\n'
                                          '3. Save as "comma separated" csv file type.\n'
                                          '3. Open in Notepad and make delimeters ";" instead of tabs or commas.\n'
                                          '4. Remove in Notepad commas (","), quotation marks ("") and question marks("?") if such.\n'
                                          '5. When you load the file make sure it is readable.')
        self.placeholder_qdpm.config(state='disabled')
        self.placeholder_qdpm.grid(column=0, row=2)

        self.data_qdpm_tree = ttk.Treeview(self.qdpm_frame)

        self.operators_button = Button(text='Load operators list', command=self.operators_data_to_df).grid(column=1,
                                                                                                           row=0)
        self.operators_frame = Frame(self).grid(column=1, row=1)
        self.text_operators = Label(self.operators_frame, width=58,
                                    text='Load the csv file with operators '
                                         'names and nicks as per qdPM.').grid(column=1, row=1)

        self.placeholder_operators = Text(self.operators_frame, height=14, width=50)
        self.placeholder_operators.insert(END, 'Instructions for the CSV input:\n'
                                          '1. Update the existing operators CSV file.\n'
                                          '2. Operators names should be spelled as in qdPM.\n'
                                          '3. Operators nicks should be their initials.\n')
        self.placeholder_qdpm.config(state='disabled')
        self.placeholder_operators.grid(column=1, row=2)

        self.data_operators_tree = ttk.Treeview(self.operators_frame)
        self.process_button = Button(self.qdpm_frame, justify=LEFT, anchor="w", text='Process data',
                                     state='disabled', command=self.progress_bar)
        # self.process_button = Button(self.qdpm_frame, justify=LEFT, anchor="w", text='Process data',
        #                              state='disabled', command=lambda: calculate(self.data_qdpm, self.data_operators))
        self.process_button.grid(sticky=W, column=0, row=3)

    def clear_tree(self, tree):
        tree.delete(*tree.get_children())

    def qdpm_data_to_df(self):
        filename_qdpm = filedialog.askopenfilename(initialdir='~/Desktop', title='Select a file',
                                                   filetypes=(('csv files', '*.csv'), ('all files', '*.*')))
        if filename_qdpm:  # TODO disable process button if .....
            if self.data_qdpm_tree:
                self.data_qdpm_tree.grid_forget()
            try:
                self.data_qdpm = pandas.read_csv(filename_qdpm, sep=';')
                self.clear_tree(self.data_qdpm_tree)
                self.data_qdpm_tree['column'] = list(self.data_qdpm.columns)
                if len(list(self.data_qdpm.columns)) != 5:  # TODO check list of headings not length (nice to have)
                    test = 0/0
                self.data_qdpm_tree['show'] = 'headings'
                for column in self.data_qdpm_tree['column']:
                    self.data_qdpm_tree.heading(column, text=column)
                data_qdpm_tree_rows = self.data_qdpm.to_numpy().tolist()
                for row in data_qdpm_tree_rows:
                    self.data_qdpm_tree.insert('', 'end', values=row)
                self.data_qdpm_tree.grid(column=0, row=2)
            except ValueError:
                if self.data_qdpm_tree:
                    self.data_qdpm_tree.grid_forget()
                self.placeholder_qdpm.config(state='normal')
                self.placeholder_qdpm.delete('1.0', END)
                self.placeholder_qdpm.insert(END, "Some error with the file occurred...")
                self.placeholder_qdpm.config(state='disabled')
                self.data_qdpm = None
            except ZeroDivisionError:
                if self.data_qdpm_tree:
                    self.data_qdpm_tree.grid_forget()
                self.placeholder_qdpm.config(state='normal')
                self.placeholder_qdpm.delete('1.0', END)
                self.placeholder_qdpm.insert(END, "Some error with the file occurred...")
                self.placeholder_qdpm.config(state='disabled')
                self.data_qdpm = None
        if self.data_qdpm is not None and self.data_operators is not None:
            self.process_button.config(state='normal')

    def operators_data_to_df(self):  # Backup
        filename_operator = filedialog.askopenfilename(initialdir='~/Desktop', title='Select a file',
                                                       filetypes=(('csv files', '*.csv'), ('all files', '*.*')))
        if filename_operator:
            if self.data_operators_tree:
                self.data_operators_tree.grid_forget()
            try:
                self.data_operators = pandas.read_csv(filename_operator, sep=';')
                self.clear_tree(self.data_operators_tree)
                self.data_operators_tree['column'] = list(self.data_operators.columns)
                if len(list(self.data_operators.columns)) != 2:  # TODO check list of headings not length (nice to have)
                    test = 0 / 0
                self.data_operators_tree['show'] = 'headings'
                for column in self.data_operators_tree['column']:
                    self.data_operators_tree.heading(column, text=column)
                data_operators_tree_rows = self.data_operators.to_numpy().tolist()
                for row in data_operators_tree_rows:
                    self.data_operators_tree.insert('', 'end', values=row)
                self.data_operators_tree.grid(column=1, row=2)
            except ValueError:
                if self.data_operators_tree:
                    self.data_operators_tree.grid_forget()
                self.placeholder_operators.config(state='normal')
                self.placeholder_operators.delete('1.0', END)
                self.placeholder_operators.insert(END, "Some error with the file occurred...")
                self.placeholder_operators.config(state='disabled')
                self.data_operators = None
            except ZeroDivisionError:
                if self.data_operators_tree:
                    self.data_operators_tree.grid_forget()
                self.placeholder_operators.config(state='normal')
                self.placeholder_operators.delete('1.0', END)
                self.placeholder_operators.insert(END, "Some error with the file occurred...")
                self.placeholder_operators.config(state='disabled')
                self.data_operators = None
        if self.data_qdpm is not None and self.data_operators is not None:
            self.process_button.config(state='normal')


    # def operators_data_to_df(self):  # Backup
    #     filename_operator = filedialog.askopenfilename(initialdir='~/Desktop', title='Select a file',
    #                                                    filetypes=(('csv files', '*.csv'), ('all files', '*.*')))
    #     if filename_operator:
    #         self.data_operators = pandas.read_csv(filename_operator, sep=';')
    #         self.clear_tree(self.data_operators_tree)
    #         self.data_operators_tree['column'] = list(self.data_operators.columns)
    #         self.data_operators_tree['show'] = 'headings'
    #         for column in self.data_operators_tree['column']:
    #             self.data_operators_tree.heading(column, text=column)
    #         data_operators_tree_rows = self.data_operators.to_numpy().tolist()
    #         for row in data_operators_tree_rows:
    #             self.data_operators_tree.insert('', 'end', values=row)
    #         self.data_operators_tree.grid(column=1, row=2)
    #     if self.data_qdpm is not None and self.data_operators is not None:
    #         self.process_button.config(state='normal')

    def progress_bar(self):
        def progress_move():
            self.process_button['state'] = 'disabled'
            self.progress.start()
            calculate(self.data_qdpm, self.data_operators)
            time.sleep(5)
            self.progress.stop()
            self.process_button['state'] = 'normal'

        threading.Thread(target=progress_move).start()



