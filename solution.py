import csv
filenames = ['transactions1.csv', 'transactions2.csv', 'transactions3.csv']
users = {}
firstline = ''
for file in filenames:
	with open(file, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter = ' ')
		# create dict with users and relevant charges
		firstline = next(reader) # skip first line
		for row in reader:
			cols = (row[0]).split('|')
			if len(cols) > 7:
				indices_to_remove = set()
				for index in range(4, len(cols)):
					if cols[index] != 'debit' and cols[index] != 'credit' and '-' not in cols[index]:
						indices_to_remove.add(index)
				modifiedCols = []
				for index in range(len(cols)):
					if index not in indices_to_remove:
						modifiedCols.append(cols[index])
				cols = modifiedCols
			user_id = cols[0]
			if user_id in users:
				users[user_id].append(cols)
			else:	
				users[user_id] = [cols]
# sort dict by date. users = {user1: [{row1}, {row2]}
for user in users:
	users[user] = sorted(users[user], key=lambda date: date[4])
# # count max and min amount
newcsv = {}
for user in users: # user = key. users[user] = val = [list of transactions]
	num_tx = len(users[user])
	max_bal, min_bal = 0, 0
	sum_bal = 0 # exactly 2 decimal places
	lastDate = users[user][0]
	for tx in users[user]:
		amt = float(tx[2])
		currDate = tx[4]
		tx_type = tx[5]
		# new date, so update min and max if needed
		if currDate != lastDate:
			# check if sum is less than min bal or greater than max bal.
			if sum_bal < min_bal:
				min_bal = sum_bal
			elif sum_bal > max_bal:
				max_bal = sum_bal
		# update sum_bal
		if tx_type == 'debit':
			sum_bal -= amt
		else:
			sum_bal += amt
	# check for last tx date, since the check above doesn't update max_bal or min_bal for last elem
	if users[user][-1][4] != users[user][-2][4]:
		if sum_bal < min_bal:
			min_bal = sum_bal
		elif sum_bal > max_bal:
			max_bal = sum_bal
	newcsv[user] = [user, str(num_tx), str(sum_bal), str(min_bal), str(max_bal)]

# create csv file using newcsv
with open('soln.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter = '|')
	writer.writerow(firstline)
	for item in newcsv:
		writer.writerow(newcsv[item])









