import google.generativeai as genai
import os
import re
import numpy as np
from dotenv import load_dotenv

load_dotenv()

input_prompt = """You are an expert in evaluating user answers based on actual answers. Your main task is to return 
only a single score(integer number) from 1-10. Check Grammar, check if keywords are matching or not, check for coherence, 
check for length of user ans, check for quality of user ans, Then based on these evaluations give final score"""


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }]

def get_gemini_response(input_prompt, user_prompt):
    response = model.generate_content([input_prompt, user_prompt],safety_settings=safety_settings)
    res = response.text
    res = float(res)
    return res


# st.title("Ans Evaluation")
# user_ans = st.text_area("User Ans:")
# main_ans = st.text_area("Main Ans:")
# if st.button("Check"):
#     user_prompt = 'User Ans: '+user_ans+'\n'+'Actual Ans: '+main_ans
#     ans_avg = []
#     for i in range(10):
#         # temp = round(float(get_gemini_response(input_prompt, user_prompt)))
#         temp = int(get_gemini_response(input_prompt,user_prompt))
#         ans_avg.append(temp)
#     print(ans_avg)
#     print(np.average(ans_avg))
#     st.write(f"Score is {np.average(ans_avg)}")


