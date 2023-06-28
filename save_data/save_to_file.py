import csv


class SaveToFile:

    def __init__(self, filepath):
        self.filepath = filepath

    # TODO: Somtimes it skips a line when writing to .csv, not sure why
    def hi_scores(self, username, score):

        # Example without needing file.close()
        # header = ['username', 'score']
        data = [username, score]

        # open the file in the write mode
        with open(self.filepath, 'a') as file:
            # create the csv writer
            writer = csv.writer(file)

            # writer.writerow(header)

            # write a row to the csv file
            writer.writerow(data)

    def get_hi_scores(self, username):

        return_rows = []
        with open(self.filepath) as file:

            reader = csv.reader(file)

            for row in reader:
                if not row[0]:  # If row empty
                    print("Error: Row in file empty")
                if row[0] == username:  # Check first element of each row (username)
                    print(row)
                    return_rows.append(row)
                # else:
                #    print("Username does not exit")

        return return_rows

    def get_all_hi_scores(self):

        return_rows = []
        with open(self.filepath) as file:

            reader = csv.reader(file)

            for row in reader:
                # if not row:  # If row empty
                if not row:  # If row empty
                    print("Error: Row in file empty")
                else:  # Check first element of each row (username)
                    print(row)
                    return_rows.append(row)
                # else:
                #    print("Username does not exit")

        return return_rows
