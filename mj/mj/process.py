'''
Author: XF
Date: 2022-12-05 07:14:19
LastEditTime: 2023-03-03 10:40:04
LastEditors: XF
Description: 
FilePath: \\Blog\\面经\\process.py
'''

import os
import path
from Perplexity import Perplexity
import json
import time

def get_answer(question):
    try:
        prompt = f"""
你是一个面试者，精通计算机和golang相关知识，需要回答问题通过面试。
回答问题时，请使用中文！请注意分段作答！注意输出要有逻辑，有顺序，详细，深入。
你可以使用markdown输出，如果有必要的话，可以输出表格进行对比和总结，参考资料可以输出到最后。
不要输出与面试无关的信息，但是建议对问题进行深化和扩展回答，比如介绍问题的背景，思路，原理，使用场景，案例等等。
问题不建议只用一段话概括，要具体详细。

问题: {question} """
        perplexity = Perplexity()
        answer = perplexity.search(prompt)
        if answer == None or answer.json_answer_text == None or "answer" not in answer.json_answer_text:
            raise("answer fail")
        res = answer.json_answer_text["answer"]
        # print(res)
    except Exception as e:
        print(e)
        time.sleep(20)
        return get_answer(question)
    return res

    
def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    files = path.glob.glob(os.path.join(current_path, "*.json"))
    for file in files:
        subject = os.path.splitext(file)[0]
        with open(file, 'rb') as f:
            data = json.load(f)
            data = data["data"]
        
        print(subject)
        print(len(data))

        mlist = []
        for i, item in enumerate(data):
            # if i < 100:
            #     continue
            question = item['questionName']
            count = item["count"]
            if count >= 1:
                answer = get_answer(question)
                mlist.append({"question":question, "answer": answer, "count":count})
                time.sleep(3.5)
                with open(os.path.join(current_path, subject + "_perplexity.txt"), 'a', encoding="utf-8") as f:
                    ans = answer
                    # ans = ans.replace("\n", "\n\n")
                    f.write("## " + question +" `"+ str(count) +"`\n" + ans + "\n\n")
                print(subject, i)

if __name__ == "__main__":
    # get_answer_chatgpt("Redis持久化方式，RDB和AOF的区别与优劣势")
    main()
