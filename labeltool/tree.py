import os

def tree(menu):
    dataset_name = []
    for item in menu:
        if item['dataset_name'] not in dataset_name:
            dataset_name.append(item['dataset_name'])
    print dataset_name
    class_list = []
    for name in dataset_name:
        print name
        tmp = {}
        tmp["text"] = name
        tmp['href'] = "summary"
        # tmp['href']
        tmp["nodes"] =[]
        for item in menu:
            if item['dataset_name'] == name:
                tp = {}
                tp["text"] = item['name']
                tp["href"] = item['tasks_id']
                tp["tags"] = item['status']
                tmp["nodes"].append(tp)
        class_list.append (tmp)
    return class_list
