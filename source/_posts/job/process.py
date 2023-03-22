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
import json
import time
# from revChatGPT.revChatGPT import Chatbot
import json
import openai

# Get your config in JSON
# config = {
#         "Authorization": "", # This is optional
#         "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..P03zJNF8Iyq0YOXL.EVNYpAR-6DdhoyJx-Utpo4VD_u46hIK_wMuXyz3nTPjrN2XJwtcv-znHenZBmXz6IcdmNGthdyUWZFHUlDZsvjoj1YbwCzDbAFL0-UbW-zt0aQY8GEU6nfCO9hYGgeSNeuVoCjJNN0LS9s__Zz8ZYopDFk8C-SVOHoFHw7LvrEUwNfw5A8tCdF6jGHOjlRHJ3AK4y_zVtbktE4TyNR6d-uQxAyIZaUFCcVm6p-PDor06aM89D45iMqsOxMN1pxpq40X-R7cTDgjuef0K2Z7v_AI_MB4oa10k-c9ty8PMBrT1K_N-PqW9F8BOh_jNBxqsloo2wkNjACvmUIj8L2qos94U9x3msS6mVQsvBUQueefenTcfa-L_TIl8svtHDao63dl9BT_8aWHonWaegJXxdFdgHjRf_XsQORElCRB3izdM3vyjgDFmiSIezWMChPhn8XRWuLovgKIRz7WZxiKvyY9BwpGDJh2U5c6Nwzx6VrCKWz8bI3GwKSJE03guYEVc0L5fvLJ7rE_WGmMgsnoY-evGkO1DqS0oL6_PDRC3Nq7NsvWz8lCBw4p7fo-l07xorwhXadD-uUwtvgveBQMYsLG6FY7CHJnlKEvtND9W2ZnARxbeIUoP_0FKKhLvntuny6SMDXsSD5bWemW6PVp01zyZYjTCFfzUwwttpeR6wVu0dZlHBEE10_ASWl-hQf0GfFJE1N0MINFqQpSn8zGVmaqNX0wv7te4Q6omrib5nmPpxhYf3mj-3YRr5Q2tM0DmF9rYXhqXnTVS4t0ikpRPXqORTzZTMxcjA900HtXtjZkNrN5CFGnNyWIr58quuP4by6cohjZDlPgIFcn63I7WijLsSUJAe3LqDxA17Wlw985pcr-z5tltO79sJT4nh8pMocgZ4QOD7CeCq2-tecXDoIWrN-rofRe_eCx34Gbuu3yaJRD5F6ikO_L8xfu4i4rHfzkyyCaRzg_RLANiBRKW_OBPf5IkfErRkv0mYtPd810S7TlvfoChLHUh_LF3K6Edi0TwLGm-9GXd-3Na7JJUnwdzLS3K63oFCSNgsuEfGbIPxBUKZuClpDQ-D5U910YJXMSI-pDpI8WUwJal0XHYz1uuNfc-wP_yyVjbqriuwroCtxOnGoFAL_l8_5Q2E_QtAABLLDtowIYn-CuWH0WA7PpnhUM3PXx-fA_siH8Z4SRRQn-V85scC0GvrWiaBbSFjvKuzXA83NGjwpp1B2HfNjAiEZAnv78auUSN5Y4tuSpPtK_7tEp0wh9pwaPwsoCFgPU7fYKFEFRgmMXKyy2tj-ItZZDAjrZcd09lUJ5L4QGz06OT1o-26H5tljCsX47Xw6fFahA501TcLBj3zdZFspMhzNQ2HMPbKNySzBPRKc7lfaZ-M823dI-NrMUxhD8_oIvUM-h4kc7tnHh3uEp2wtfF3l7hHoBXICCpgZK_4j4LQqiCeQ-RdJ8ApBmMB0MyIvZP0qv3mcf6h1CNSE2QBwZ1hMh2N_7D8XXmGHZhi_nDL8S1XaUJu-EH79sCAfpr945j-HEKBKIyLtJJHRKdTyu9ADdMJu_89qjANoMJOR4FRXYOmpdHyZIVP__n7ikhwTI-5fFCNLewNpmt4Zf1c71wCX1hJaGx2YaGRddIZrOEE4b-VwrLqeva_fihcMEP-7J1hBqKxJQj780JbU4QHCcYDOH_rMzL9cZ7ub27qcNp8ljxRUJQL7nzllWhR3xj4aH7TckU9GE7xV9mYYx9EtXLz0jPQSAYjAXVEvQ6HPzh6vFHZSRJpSHeZYSiCBrLYg_-uq2p2RXwhHDw1TA3wo4uZ0v6sAHRP_Iev9mmu08FaT6y-E7-4hy4LO_HjkQH2KQi_hLapxjJeKg5Y6Uu4eiv_vtqcMFzHadM3lY0sbjbhoIvbCA48KAqLTlcV-oUFLes2Z9QAYSCna9Vg4hLZcKoqUGX4H3s14bbOb374qV3gmsAImxIZNyJQln1bspRavk9VeXLZMxkB0AirCFbLW9auZ2Ic9IV7g1bPww6rc4uyEv-_FB_AypemNj50UVI_A7YXVtcgvRP7UCVaUyKS8OydUFJTjWM90hFl1rqNSbJ2yvKRJkA15uACx3y0dCDvE0vqE-R91uorWtRtVgb34Qmw-CdU44.qbu9eSYX_5v7RiBSIIzmzA"
# }

# chatbot = Chatbot(config, conversation_id=None)
# chatbot.refresh_session()
# def get_answer(question):
#     chatbot.reset_chat()
#     # chatbot.refresh_session()
#     resp = chatbot.get_chat_response(question)
    
#     if not isinstance(resp, ValueError) and "message" in resp and resp["message"] != "":
#         return resp["message"]
#     else:
#         print("Error: ", resp)
#         time.sleep(20)
#         return get_answer(question)
openai.organization = "org-7gghRYPSh2oYp8q64CFsl8YU"
openai.api_key = "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"

def get_answer_chatgpt(question):
    try:
        res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
            {"role": "system", "content": "你可以帮助回答一些计算机相关知识，包括mysql，redis，消息队列，操作系统等，你会先解释技术名词，然后详细回答用户的问题。如果有需要输出程序代码，默认使用Go语言。"},
            {"role": "user", "content":  f"请你详细回答，{question}"},
        ]
        ).to_dict_recursive()
        res = res["choices"][0]["message"]["content"]
        # print(res)
    except:
        time.sleep(60)
        return get_answer_chatgpt(question)
    return res

    
def get_answer_gpt3(question):
    try:
        res = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"请你回答问题：{question}(Go语言)",
                temperature=0,
                max_tokens=4000,
                top_p=0.9,
                frequency_penalty=0.5,
                presence_penalty=0
        ).to_dict_recursive()
    # print(res)
        res = res["choices"][0]["text"]
    except Exception as e:
        print(e)
        time.sleep(60)
        return get_answer_gpt3(question)
    return res

def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    files = path.glob.glob(os.path.join(current_path, "ds.json"))
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
                answer = get_answer_gpt3(question)
                mlist.append({"question":question, "answer": answer, "count":count})
                time.sleep(3.5)
                with open(os.path.join(current_path, subject + "_gpt3.txt"), 'a', encoding="utf-8") as f:
                    ans = answer
                    # ans = ans.replace("\n", "\n\n")
                    f.write("## " + question +" `"+ str(count) +"`\n" + ans + "\n\n")
                print(subject, i)

if __name__ == "__main__":
    # get_answer_chatgpt("Redis持久化方式，RDB和AOF的区别与优劣势")
    main()