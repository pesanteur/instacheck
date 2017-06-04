#!/usr/local/bin/python3
from lxml import html
from address import find_address
from datetime import datetime, timedelta
import requests
import json
import timestring
import login_gs
import gspread

def count_occupied_cells():
	# Todo: Make this non hard coded in the future
	"""Finds the number of non empty cells in a column in the sheet. """
	column_list = worksheet.col_values(3)
	count = 0
	for i in column_list:
		if i:
			count+= 1
	return count

#Calculates difference and last date user posted on Instagram
def days_until(date):
	date = timestring.Date(date)
	date_string = str(date)
	date_string_split = date_string.split(' ')
	real_date = datetime.strptime(date_string_split[0], '%Y-%m-%d')
	today = datetime.now()
	#subtracts 1 to remove counting today as a date in the difference
	real_day = today.replace(day=today.day-1)
	#diff = real_date - today
	real_diff = real_date - real_day
	return real_diff


def checkpopularity(instausername):
        #TODO: this doesn't work anymore, need to fix this
        url = "https://www.instagram.com/" + instausername
	userpage = requests.get(url)
	tree = html.fromstring(userpage.content)
	string = tree.xpath('//script')[6].text
	string = string[21:-1]
	parsed_json = json.loads(string)
	username = parsed_json["entry_data"]["ProfilePage"][0]["user"]["username"]
	followers = int(parsed_json["entry_data"]["ProfilePage"][0]["user"]["followed_by"]["count"])
	follows = int(parsed_json["entry_data"]["ProfilePage"][0]["user"]["follows"]["count"])
	media = parsed_json["entry_data"]["ProfilePage"][0]['user']['media']['nodes'][0]['date']
	last_post = days_until(media)
	pop_percent = followers/follows * 1.0
	print("Username: %s" % username)
	print("Followers: %s" % followers)
	print ("Follows: %s"% follows)
	print("Last post: %s" % last_post)
	print("Follower/Following Proportion: %s" % pop_percent)
	# Weights username by recency of last post
	if last_post.days <  5:
		multiplier = 3
	elif last_post.days >=  5 and last_post.days < 7:
		multiplier = 2
	elif last_post.days >=  7 and last_post.days < 14:
		multiplier = 1
	else:
		multiplier = 0.5
	score = multiplier * pop_percent
	print("Score: %s" % score)
	print("\n")
	return score

def getusername(picurl):
	instaurl = "https://www.instagram.com/p/" + picurl
	instapage = requests.get(instaurl)
	tree = html.fromstring(instapage.content)
	string = tree.xpath('//script')[6].text
	string = string[21:-1]
	parsed_json = json.loads(string)
	instausername = parsed_json["entry_data"]["PostPage"][0]["media"]["owner"]["username"]
	checkpopularity(instausername)


def gethashtag():
	hashtag = input("Which hashtag would you like to search? ")
	url = "https://www.instagram.com/explore/tags/" + hashtag
	page = requests.get(url)
	print ("Searching #%s" % hashtag)
	tree = html.fromstring(page.content)
	string = tree.xpath('//script')[6].text
	string = string[21:-1]
	#fix the string and make it pretty
	item_dict = json.loads(string)
	picturecount = len(item_dict["entry_data"]["TagPage"][0]["tag"]["media"]["nodes"])
	#get the number of pictures in this page(varies)
	parsed_json = json.loads(string)
	for i in range(picturecount):
		picurl = parsed_json["entry_data"]["TagPage"][0]["tag"]["media"]["nodes"][i]["code"]
		#prints instagram.com/p/$PICURL
		getusername(picurl)


def column_finder(title):
	column = worksheet.find(title)
	column_letter = chr(column.col + 96)
	return column_letter

if __name__ == '__main__':
    gc = login_gs.login()
    #TODO: Request filename from user
    sh = gc.open("Instascore Test")
    worksheet = sh.get_worksheet(0)

    starttime = datetime.now()
    starttime_string = str(starttime)

    print(("Starting to go through sheet at %s...") % (starttime_string))
    # TODO: Also make this non hard coded in the future, pull range using similar function as below
    title_row = worksheet.range('A1:P1')


    # TODO: Request column titles from user if not running this automatically...How to sense that?
    instascore_column = "Instascore"
    username = "Username"
    instascore_character = column_finder(instascore_column)
    username_character = column_finder(username)
    cell_count = count_occupied_cells()

    username_range = worksheet.range(("%s2:%s%s") % (username_character,username_character, cell_count))

    updated_count = 0
    for cell in username_range:
            value = cell.value
            try:
                    score = checkpopularity(value)
            except (IndexError, TypeError) as e:
                    score = "N/A"
            instascore_row = '%s%s' % (instascore_character, cell.row)
            #TODO: Change below to only use instascore_row
            worksheet.update_acell('%s%s' % (instascore_character, cell.row), score)
            updated_count +=1

    endtime = datetime.now()
    endtime_string = str(endtime)
    total_time = endtime - starttime
    total_time_string = str(total_time)

    print(("Finished updating %s rows at %s. Update took %s.\n") % (updated_count, endtime_string, total_time_string))
