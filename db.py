import csv
class Database:

    def insert(self,data):
        with open('records.csv', 'r') as csvfile:
            rec_read = csv.reader(csvfile)
            for rec in rec_read:
                if len(rec) !=0:
                    if rec[0] == data['Email'] and rec[1] == data['Name'] and rec[2] == data['Date'] and rec[3] == data['Route']:
                        return 0


        with open('records.csv', 'a') as csvfile:
            write_object  = csv.writer(csvfile)
            write_object.writerow(list(data.values()))
            return 1