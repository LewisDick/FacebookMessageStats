import json, os, datetime

current_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


people = dict()
"""
Gets the name of the current user, to differentiate between them and other people
"""
with open(current_location + "\\profile_information\\profile_information.json") as current_user_data:
    current_user_info = current_user_data.read()
    current_user_json = json.loads(current_user_info)['profile']

current_user_name = current_user_json.get("name")
current_user_data.close()

current_location += "\messages"
test = next(os.walk(current_location))[1]

for folder in test:
    if os.path.exists(current_location + "\\" + folder + "\\message.json"):
        with open(current_location + "\\" + folder + "\\message.json", "r") as current_conversation:
            data = current_conversation.read()

        conversation_data = json.loads(data)

        """
        Adds people from current conversation to the dict of all people
        """
        if 'participants' in conversation_data:
            for p in conversation_data.get("participants"):
                if p not in people and p != current_user_name:
                    people.update({p:[[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]]})
        else:
            continue

        number_participants = len(conversation_data.get("participants"))
        if number_participants > 1:
            if conversation_data.get("title") not in people:
                people.update({conversation_data.get("title"): [[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]]})
        """
        Counts the occurences of a person in messages
        """
        for msg in conversation_data.get("messages"):
            if 'sender_name' in msg:
                year_index = int(datetime.datetime.fromtimestamp(msg.get("timestamp")).strftime("%Y")) - 2011
                if msg.get("sender_name") in people:
                    people[msg.get("sender_name")][0][year_index] += 1
                elif msg.get("sender_name") == current_user_name:
                    if number_participants > 1:
                        if conversation_data.get("title") in people:
                            people[conversation_data.get("title")][1][year_index] += 1
                        else:
                            people.update({conversation_data.get("title"): [[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]]})
                            people[conversation_data.get("title")][1][year_index] += 1
                    else:
                        people[conversation_data.get("participants")[0]][1][year_index] += 1
                else:
                    print(msg.get("sender_name").encode("utf-8"))
                    people.update({msg.get("sender_name"): [[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]]})
                    people[msg.get("sender_name")][0][year_index] += 1


file_out = open("test.csv", "wb")
file_out.write(
    "Person,2011,2012,2013,2014,2015,2016,2017,2018,,Person,2011,2012,2013,2014,2015,2016,2017,2018".encode("latin-1"))
file_out.write("\n".encode("latin-1"))


for p in people:
    csv_out = p.replace(',', ' ').replace('"', ' ')

    for x in people.get(p):
        for y in x:
            csv_out += ("," + str(y))
        csv_out += ','
        csv_out += ', ' + p.replace(',', ' ').replace('"', ' ')

    file_out.write(csv_out.encode("utf-8"))
    file_out.write("\n".encode("latin-1"))

file_out.close()

