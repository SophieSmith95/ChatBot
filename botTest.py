import os
import tempfile
from shutil import copyfile

answers = []
question = " "
answer = " "
is_resposive = None

def main():
	is_resposive_bot()

def is_resposive_bot():
	global is_resposive
	u = input("Do you want your bot to be responsive(R) or to store user results(S)? (R/S) \n")
	if u.lower() == 's':
		is_resposive = False
		storing_bot()
	elif u.lower() == 'r':
		is_resposive = True
		resposive_bot()
	else:
		is_resposive_bot()

def resposive_bot():
	global question
	global answer
	question = input("Please enter the question you would like your bot to be able to answer or enter 'end' to complete \n")
	if question.lower() != 'end':
		answer = input("What would you like your bot to reply with? \n")
		print("Question = " + question + "\nAnswer = " + answer + "\n")
		answers.append(question)
		answers.append(answer)
		resposive_bot()
	else:
		check_all()

def storing_bot():
	global question
	question = input("Please enter your question or enter 'end' to complete \n")
	if question.lower() != 'end':
		print("Question = " + question + "\n")
		answers.append(question)
		storing_bot()
	else:
		check_all()

def check_all():
	print ("Your Questions and answers: ")
	for item in answers:
		print (item)
	m = input("Confirm these answers are correct. Type 'YES' if they are correct or the number of the incorrect question to amend it: \n")
	if m.lower() != "yes":
		p = input("Please enter your question ")
		answers[int(m)-1] = p
		check_all()
	else:
		if is_resposive == False:
			store_write()
		else:
			responsive_write()

def responsive_write():
	count = 0
	with tempfile.TemporaryFile() as temp:
		while count != len(answers):
			if count == 0 or count < 2:
				temp.write(bytes('    if message.lower() == "' + answers[count].lower() + '":' + '\n        bot.send_text_message(recipient_id, "' + answers[count+1] + '")\n', 'UTF-8'))
				count += 2
			else:
				temp.write(bytes('	elif message.lower() == "' + answers[count].lower() + '":' + '\n		bot.send_text_message(recipient_id, "' + answers[count+1] + '")\n', 'UTF-8'))
				count += 2
		with tempfile.TemporaryFile() as temp2:
			with open("app_copy_responsive.py", 'r') as bot:
				for line in bot:
						if "#INSERT" in line:
							temp.seek(0)
							for lines in temp:
								temp2.write(lines)
						else:
							temp2.write(bytes(line, 'UTF-8'))
			temp2.seek(0)
			print(temp2.read().decode())
		confirm_copy()

def store_write():
	count = 0
	with tempfile.TemporaryFile() as temp:
		while count != len(answers):
			if count == 0:
				temp.write(bytes('            if "ID = " + str(recipient_id) + ", Counter = ' + str(count) + '" in line:\n                bot.send_text_message(recipient_id, "' + answers[count].lower() + '")\n                count += 1\n                save_position(recipient_id)\n                return\n', "UTF-8"))
				count += 1
			elif count >=1 and count < len(answers)-1:
				temp.write(bytes('            elif "ID = " + str(recipient_id) + ", Counter = ' + str(count) + '" in line:\n                bot.send_text_message(recipient_id, "' + answers[count].lower() + '")\n                count += 1\n                save_position(recipient_id)\n                return\n', "UTF-8"))
				count += 1
			else:
				temp.write(bytes('            elif "ID = " + str(recipient_id) + ", Counter = ' + str(count) + '" in line:\n                bot.send_text_message(recipient_id, "' + answers[count].lower() + '")\n                count = 0\n                save_position(recipient_id)\n                return\n', "UTF-8"))
				count += 1
		with tempfile.TemporaryFile() as temp2:
			with open("app_copy_store.py", 'r') as bot:
				for line in bot:
						if "#INSERT" in line:
							temp.seek(0)
							for lines in temp:
								temp2.write(lines)
						else:
							temp2.write(bytes(line, 'UTF-8'))
			temp2.seek(0)
			print(temp2.read().decode())
		confirm_copy()

def write_to_file():
	count = 0
	with tempfile.TemporaryFile() as temp:
		for item in answers:
			if count < len(answers)-1:
				temp.write(bytes(item, 'UTF-8'))
				temp.write(bytes("\n", 'UTF-8'))
				count += 1
			else:
				temp.write(bytes(item, 'UTF-8'))
		temp.seek(0)
		print("Reading.....")
		print (temp.read().decode())
		confirm_copy()

def confirm_copy():
	k = input("Please copy and paste the above into a notepad file and name it app.py.\nType YES when completed \n")
	if k.lower() == "no":
		confirm_copy()
	else:
		print("Please follow the instructions on the facebook page")


main()
