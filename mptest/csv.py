import csv
with open('/root/workspace/demos/mptest/mptest/customer.csv','r+') as csvFile:
	dict_reader = csv.DictReader(csvFile)
	for row in dict_reader:
		headers = [k for k in row]
		print(headers)
		with open('/root/workspace/demos/mptest/mptest/customer1.csv','w+') as wFile:
			writer = csv.DictWriter(wFile,fieldnames=headers)
			writer.writeheader()
			writer.writerow(row)