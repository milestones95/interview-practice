from datetime import datetime,timedelta

class User_Logins:


# we need to make sure each logged every we count has a unique user. if we've seen the user before within 24 hours we should not count it. Hashmap?
# we need to make sure we see the difference to know if a login in is still within the valid timeframe or not
    def __init__(self):
        self.logins = {}

    def new_request(self, user_id: str, timestamp: datetime):

        self.logins[user_id] = self.logins.get(user_id,[])
        self.logins[user_id].append(timestamp)
    


    def getCount(self):

        users = self.logins.values()
        count = 0
        for user_times in users:
            diff = datetime.now() - user_times[len(user_times)-1]

            if diff < timedelta(hours=24):
                count+=1

        return count
