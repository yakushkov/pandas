import pandas as pd
import os

class App:
    def __init__(self):
        self.data = None

    def input_data(self):
        folder_path = input("Input name path: ").encode('utf-8').decode('utf-8')
        sheet_name = input("Input sheet name (for xlsx) or ignore (for CSV): ").encode('utf-8').decode('utf-8')
        return folder_path, sheet_name

    def check_folder(self, folder_path):
        try: 
            files = os.listdir(folder_path)
            if not files:
                print('There is no files in folder.')
                return
            else:
                return files
        except FileNotFoundError:
            print('Folder not found.')
            return

    def check_files(self, files):
        first_file_extension = os.path.splitext(files[0])[1].lower()

        if len(files) < 2:
            print("Need two files to concat.")
            return
        
        for file_name in files:
            if not (file_name.endswith('.xlsx') or file_name.endswith('.csv')):
                print(f"File {file_name} has an unsupported extension.")
                return
            current_file_extension = os.path.splitext(file_name)[1].lower()
            if current_file_extension != first_file_extension:
                print(f"Files got different extensions: {first_file_extension} и {current_file_extension}.")
                return
        print(f"All files got same extension: {first_file_extension}")
        return first_file_extension

    def check_columns(self, dfs, input_data):
        columns_set = set(tuple(df.columns.tolist()) for df in dfs)
        if len(columns_set) > 1:
            print("Columns set are different, can't concat")
            print("Different columns were found in:")
            print(file_names)
            return False
        return True

    def edit_data(self, folder_path, extension, sheet_name):
        if extension == '.xlsx':
            try:
                df = pd.read_excel(folder_path, sheet_name=sheet_name)
                return df, df.columns.tolist()
            except Exception as e:
                print(f"Error with opening file {folder_path}: {str(e)}")
                return None, None
        elif extension == '.csv':
            try:
                df = pd.read_csv(folder_path)
                return df, df.columns.tolist()
            except Exception as e:
                print(f"Error with opening file {folder_path}: {str(e)}")
                return None, None
        else:
            print(f"Wrong extension: {extension}")
            return None, None

    def merge(self):
            input_data = self.input_data()
            folder = self.check_folder(input_data[0])
            check_extension = self.check_files(folder)

            def merge_files(folder, check_extension, input_data):
                dfs = []
                columns_set = set()
                problem_file = None
                
                for filename in folder:
                    edit_files, columns = self.edit_data(os.path.join(input_data[0], filename), check_extension, input_data[1])

                    if edit_files is not None:
                        if columns_set and set(columns) != columns_set:
                            print(columns_set, set(columns))
                            print(f"Attention: file '{filename}' got different columns!")
                            problem_file = filename
                            break  
                        dfs.append(edit_files)
                        columns_set = set(columns)

                if problem_file is None:
                    combined_df = pd.concat(dfs, ignore_index=True)
                    combined_df.to_excel('combined.xlsx', index=False)
                    print("File 'combined.xlsx' was created.")
                else:
                    print(f"Error: '{problem_file}' got different columns .")

            merge_files(folder, check_extension, input_data)

app_instance = App()
app_instance.merge()