query = "name=John+Doe&age=29&tags=python,sql,go&active="
query1 = "&name&=John+Doe&age=29&tags=python,sql,go&active=&store&"
query2 = "&name&=John+Doe&age=29&tags=python,sql,go&active=&store&"

def parse_query(query):

    parameters = query.split("&")

    print("parameters: ", parameters)
    param_list = {}
    for item in parameters:
        if "=" in item:
            left,right = item.split("=",1)
            if left == '':
                continue
            param_list[left] = right


    print("param list: ", param_list)

    return param_list

parse_query(query1)