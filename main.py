import json
import re
import sys
from regularization import extract_id_act_text

def extract_id_action(text):
    # 定义正则表达式模式
    id_pattern = r"id=(\d+)"
    action_pattern = r"action=(\w+)"

    # 使用正则表达式进行匹配
    id_match = re.search(id_pattern, text)
    action_match = re.search(action_pattern, text)

    # 提取匹配到的值
    id_value = int(id_match.group(1)) if id_match else -1
    action_value = action_match.group(1) if action_match else "null"

    return id_value, action_value

# 读取JSON文件
json_file_path = "result_analysis.json"
with open(json_file_path, 'r', encoding='utf-8') as file1:
    task_json = json.load(file1)

# 读取JSON文件
json_file_path2 = "question.json"
with open(json_file_path2, 'r', encoding='utf-8') as file2:
    task_json2 = json.load(file2)

# 读取JSON文件
json_file_path3 = "answer1.json"
with open(json_file_path3, 'r', encoding='utf-8') as file3:
    task_json3 = json.load(file3)

right_num = 0
total_num = 0

for app in task_json:
    app_total_num = 0
    app_right_num = 0
    for task_str in task_json[app]:
        task_profile = task_json[app][task_str]
        profile = task_profile["profile"]
        task = task_profile["task"]

        question1 = ""
        item1 = ""

        found_match = False
        for question in task_json2:
            if found_match:
                break
            for item in task_json2[question]:
                text = task_json2[question][item][0]
                start_index = text.find("Task:") + len("Task:")
                end_index = text.find("Previous UI actions:")
                extracted_text = text[start_index:end_index].strip()

                if extracted_text == task:
                    question1 = question
                    item1 = item
                    found_match = True
                    break
        try:
            answer_text_list = task_json3[question1][item1]
        except:
            print('notfound')
            continue

        id_list = []
        action_list = []
        text_list = []

        for item2 in answer_text_list:
            item2 = item2.replace('\n', '')
            # print(item2)
            result = extract_id_act_text(item2)
            # result = extract_id_action(item2)
            # print(result)
            if result:
                id_list.append(result[0])
                action_list.append(result[1])
                text_list.append(result[2])
            else:
                print("No match found.")
                id_list.append(-1)
                action_list.append("null")
        for i in range(len(profile)):
            action = profile[i]
            total_num += 1
            app_total_num += 1
            label = action["label"]
            gt_id = label[0]

            if i < len(id_list):
                answer_id = id_list[i]
            else:
                print("Index out of range.")
                print(i)
            if label[1] == 'null':  # this is a tap action or ending
                if answer_id == gt_id:
                    right_num += 1
                    app_right_num += 1
            else:
                if answer_id == gt_id and text_list[i] == label[1]:
                    right_num += 1
                    app_right_num += 1                    
        #     action_input = label[1] != "null" and action_list[i] == "input"
        #     action_tap = label[1] == "null" and action_list[i] == "tap"
        #     end_task = gt_id == -1 and answer_id == -1
        #     if gt_id == answer_id and (action_input or action_tap or end_task):
        #         right_num += 1
        #         app_right_num += 1
        # # print("-----------------")
    print("app_right_num:", app_right_num)
    print("app_total_num:", app_total_num)
    print(app, ":", app_right_num / app_total_num)

# 恢复标准输出
# sys.stdout = original_stdout
print("total accuracy:", right_num / total_num)
