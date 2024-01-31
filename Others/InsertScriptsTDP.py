import pandas as pd

class SQLInsertScriptGenerator:
    def __init__(self, file_path, table_name):
        self.file_path = file_path
        self.table_name = table_name
        self.df = None

    def load_excel(self):
        """Loads the Excel file into a DataFrame."""
        self.df = pd.read_excel(self.file_path)

    def set_sql_table_columns(self, columns):
        """Sets the DataFrame column names to match the SQL table column names."""
        self.df.columns = columns

    def generate_insert_script(self, row):
        """Generates an SQL insert script for a single row."""
        columns = row.index
        values = row.values

        script = f"INSERT INTO {self.table_name} ("
        script += ", ".join([f"[{col}]" for col in columns])
        script += ") VALUES ("

        value_list = []
        for value in values:
            if pd.isnull(value):
                value_list.append("NULL")
            elif isinstance(value, str):
                value_list.append("'" + value.replace("'", "''") + "'")
            elif isinstance(value, pd.Timestamp):
                value_list.append(f"'{value.strftime('%Y-%m-%d')}'")
            else:
                value_list.append(str(value))
        script += ", ".join(value_list)
        script += ");\n"
        return script

    def generate_all_insert_scripts(self):
        """Generates SQL insert scripts for all rows in the DataFrame."""
        return self.df.apply(self.generate_insert_script, axis=1).str.cat()

    def save_scripts_to_file(self, output_file_path):
        """Saves the generated SQL insert scripts to a file."""
        with open(output_file_path, 'w') as file:
            file.write(self.generate_all_insert_scripts())

# Example usage
generator = SQLInsertScriptGenerator('C:\Rep\ML_Trainings\Others\Load into PBI TDP Targets FctTable 29th Jan.xlsx', '[dbo].[PBI TDP Targets FctTable]')
generator.load_excel()
"""
generator.set_sql_table_columns([
    # List of SQL table column names
    "Target Year", "Category Code", "Ops Code", "Target Enrolment Type",
    "Target - Term 1", "Target - Term 2", "Target - Term 3", "Target - Term 4",
    "Liability Grouping", "Target Type", "Target Start Date", "Baseline Enrolments",
    "Target #", "Ops-Course-National-Code", "Liability Group", "Finance Location",
    "Finance Location Descripton", "Study Measure Total", "Study Measure Term 01",
    "Study Measure Term 02", "Study Measure Term 03", "Study Measure Term 04",
    "Course Liability Code", "Start Week", "End Week", "Start Term", "End Term",
    "Fund Code", "Fund Description", "Fund Category", "CourseCodeNAT", 
    "FinanceActivityCode", "TDP Start Date", "TDP End Date", "TDP Start Month", 
    "TDP End Month", "Credit Points"
])
"""
output_path = 'C:\Rep\ML_Trainings\Others\Load into PBI TDP Targets FctTable 29th Jan.sql'
generator.save_scripts_to_file(output_path)
