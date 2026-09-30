line="2026-09-08T14:32:01 ERROR user_id=8842 payment_declined card=**** retries=3"

def parse_line(line):

    print(line.split(" "))

    properties = line.split()
    time = properties[0]
    level = properties[1]

    print("propertiers: ", properties)
    new_dict = {}

    for c in properties[2:]:
        print("c: ", c)
        if "=" in c:
            left, right = c.split("=",1)
            new_dict[left] = right

    return {
        "timestamp": time,
        "level": level,
        "fields": new_dict
    }


result = parse_line(line)

print("result: ", result)