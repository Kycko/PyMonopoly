#!/usr/bin/python3
import random

def write_to_file(file, data, method='w'):
	list = open(file, method, encoding='utf-8')
	list.writelines(data)
	list.close()

array = []
for game in range(2):
	x = random.randrange(100)
	array.append(str(x)+'\n')
	y = 101
	while y > x:
		y = random.randrange(100)
	array.append(str(y)+'\n')
	array.append(str(random.randrange(1000000))+'\n')
	score = []
	day = []
	for i in range(7):
		score.append(random.randrange(1500))
		date = ''
		for cifra in (32, 13, 16):
			temp = str(random.randrange(1, cifra))
			if len(temp) == 1:
				temp = '0' + temp
			if cifra in (32, 13):
				temp += '.'
			date += temp
		day.append(date)

	max = day[0]
	for i in range(1, 7):
		if day[i][6:] > max[6:]:
			max = day[i]
		elif day[i][6:] == max[6:] and day[i][3:5] > max[3:5]:
			max = day[i]
		elif day[i][6:] == max[6:] and day[i][3:5] == max[3:5] and day[i][:2] > max[:2]:
			max = day[i]

	count = 1
	while count != 0:
		count = 0
		for i in range(6):
			if score[i] < score[i+1]:
				temp = score[i+1]
				score[i+1] = score[i]
				score[i] = temp
				temp = day[i+1]
				day[i+1] = day[i]
				day[i] = temp
				count += 1

	for i in range(7):
		if max == day[i]:
			color = '1'
		else:
			color = '0'
		array.append('Антоний ' + str(score[i]) + ' ' + day[i] + ' ' + color + '\n')

write_to_file('settings/stats', array)
