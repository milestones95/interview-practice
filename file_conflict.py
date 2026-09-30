class files:

    def __init__(self):
        self.files = {}


    def is_valid_sync(self, batch: list[tuple[ str, int]]):

        for file in batch:

            file_id,v = file

            # If the file doesn't exist then we can add the file because there's nothing to conflict. We would just add the new file. It's like if an engineer puts a new file to the repository. There are no other versions and so that gets added to the server 
            if file_id not in self.files:
                self.files[file_id] = file_version()
                self.files[file_id].versions.add(v)
            
            else:
                
                if v not in self.files[file_id].versions:
                    return False
                elif v < self.files[file_id].latest_version:
                    return False

                else:
                    latest = self.files[file_id].latest_version + 1
                    self.files[file_id].latest_version = latest
                    self.files[file_id].versions.add(latest)

        return True
            

class file_version:
    def __init__(self):
        self.versions = set()
        self.latest_version = 1


test = files()
fv = file_version()
fv.versions.add(1)
fv.versions.add(2)
fv.versions.add(3)
fv.versions.add(6)
fv.versions.add(8)




fv.latest_version = 8
test.files = {"1": fv}

result1 = test.is_valid_sync([("1",8)])
# result2 = test.is_valid_sync([(2,2),(3,3)])
result3 = test.is_valid_sync([("1",3)])
result4 = test.is_valid_sync([("2",2)])




print("result1: ", result1)
# print("result2: ", result2)
print("result3: ", result3)
print("result4: ", result4)











