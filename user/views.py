from django.contrib.auth import get_user_model
import json
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, ResumeForm, JobForm
from . models import User_Details, Questions, Contactus, tech_test_model, ForceSignout_User, Job
import pandas as pd
import numpy as np
# import spacy
import fitz
from json2html import *
from django.contrib import messages
from datetime import datetime, timedelta
from .otp import send_mail 
from django.db.models import Subquery
import numpy as np





# # custom 404 view
# def custom_404(request, exception):
#     return render(request, '404.html', status=404)

def home(request):
    context = {}
    return render(request, 'user/home.html', context)

def about(request):
    return render(request, 'user/about.html')

def resend1(request):
    otp = send_mail(mail)
    print("OTP For SignUP: ", otp)
    return redirect("verification")

def resend2(request):
    otp = send_mail(user_mail)
    print("OTP : ", otp)
    return redirect("reset_pwd")

def signup(request):
    msg = ""
    if request.method == 'POST':
        global form_1
        form_1 = SignUpForm(request.POST)
        if form_1.is_valid():
            User = get_user_model()
            mail_1 = request.POST['email']
            queryset = User.objects.filter(email=mail_1)
            if queryset.exists():
                msg = "This email is already exists!!!"
                user = queryset.first()  
                return render(request, 'user/pages-register.html', {"msg":msg , 'form':form_1})
            
            global mail 
            mail = request.POST['email']
            global random_otp
            random_otp =  send_mail(mail)
            print('----otp : ',random_otp)
            # verification(request)
            return redirect("verification")
            # return render(request, 'user/verification.html')
        else:
            msg = 'form is not valid'
    else:   
        form_1 = SignUpForm()
    return render(request,'user/pages-register.html', {'form': form_1, 'msg': msg})



def verification(request):
    msg = ""
    if request.method == "POST":
        print("we are in request.post ...")
        # user_otp = request.POST['candidate_otp']
        user_otp = request.POST.get("candidate_otp", "default user")
        user_otp = int(user_otp)
        print("user_otp  = ", user_otp)
        if random_otp == user_otp:
            user = form_1.save()
            msg = 'user created'
            return redirect("success_otp")
        else:
            print("otp not matched")
            msg = "Incorrect OTP"        
    return render(request, 'user/verification.html', {"msg": msg})

def success_otp(request):
    return render(request, 'user/success_otp.html')

def reset_success(request):
    return render(request, 'user/reset_success.html')

def forgot_pwd(request):
    msg = ""
    if request.method == "POST":
        User = get_user_model()
        global user_mail
        user_mail = request.POST.get("new_email", "default email")
        print("--------",user_mail)
        queryset = User.objects.filter(email=user_mail)
        if queryset.exists():
            user = queryset.first()  
        else:
            msg = "No user found with this email"
            return render(request, 'user/forgot_pwd.html', {"msg": msg})
        global temp_otp
        temp_otp = send_mail(user_mail)
        print("temp_otp : ", temp_otp)
        return redirect("reset_pwd")
        # return render(request, 'user/reset_pwd.html')
    return render(request, 'user/forgot_pwd.html')



def reset_pwd(request):
    msg = ''
    if request.method == "POST":
        # y = User.objects.all()
        # print("all the users: ", y)
        print("we are in request.post ...")
        user_otp = request.POST.get("reset_otp", "default user")
        user_otp = int(user_otp)
        print("user_otp  = ", user_otp)
        pwd1 = request.POST['password1']
        pwd2 = request.POST['password2']    
        if temp_otp == user_otp and pwd1 == pwd2:
            User = get_user_model()
            user = User.objects.get(email=user_mail)
            user.set_password(pwd1)
            user.save()
            return redirect("reset_success")
        elif len(pwd1) <8 or len(pwd2) <8:
            msg = "Password length should be greater than 8" 
        elif pwd1 != pwd2:
            msg = "Password does not match"
        elif temp_otp != user_otp:
            msg = "OTP not matched"
        else:
            print("OTP not matched")
            msg = "Incorrect OTP"        
    return render(request, 'user/reset_pwd.html', {"msg": msg})

def signin(request):
    form = LoginForm(request.POST or None)
    msg = ""
    if request.method == 'POST':
        if form.is_valid():
            global username
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # User = get_user_model()
            # queryset = User.objects.filter(username=username).exists()
            # print("=====", queryset)
            # role = queryset.role
            # print(role)

            global user_name_1
            user_name_1 = user
            if user is not None and user_name_1.is_admin:  
                login(request, user)
                return redirect('hr')   
            elif user is not None and user.is_masteruser:
                login(request, user)
                return redirect('usermgnt')

            elif user is not None:
                login(request, user)
                return redirect('candidate')
            else:
                msg= 'Invalid credentials'
        else:
            msg = 'Error validating form'

    # else:   
    #     msg = "You are not logged in"

    return render(request, 'user/pages-login.html', {'form': form, 'msg': msg})


# def force_signout(request):
#     return HttpResponse("You can not apply for the exam.")
#     # return render(request, 'user/force_signout.html')



def force_signout_test(request):

    if 'tab_switch_count' not in request.session:
        request.session['tab_switch_count'] = 0

    request.session['tab_switch_count'] += 1
    if request.session['tab_switch_count'] >+1 :
        # Store the user in the ForceSignout_User model
        rsm = f"media/{user_name_1}.pdf"
        force_signout_user = ForceSignout_User.objects.create(user=request.user,resume=rsm, job_type=job, reason="User tried to change tab")
        force_signout_user.save()
        del request.session['tab_switch_count']  # Reset tab switch count
        signout(request)
        return render(request, 'user/force_signout.html')
    else:
        return redirect("test")



def force_signout_tech_test(request):
    if 'tab_switch_count' not in request.session:
        request.session['tab_switch_count'] = 0
    
    request.session['tab_switch_count'] += 1
    if request.session['tab_switch_count'] >1 :
        rsm = f"media/{user_name_1}.pdf"
        force_signout_user = ForceSignout_User.objects.create(user=request.user,resume=rsm, job_type=job, reason="User tried to change tab")
        force_signout_user.save()
        del request.session['tab_switch_count']  # Reset tab switch count
        signout(request)
        return render(request, 'user/force_signout.html')
    else:
        return redirect("technical_test")

def signout(request):
        msg = ""
        logout(request)
        msg = "You have been logged out"
        messages.success(request, "You have been logged out")
        return redirect("signin")
    # return render(request, 'user/signin.html', {'msg':msg}) 


# @login_required(login_url="signin")
# def contactus(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("contactus")
#         else:
#             print(form.errors)
#         return render(request, 'user/contactus.html',{'form':form, 'query':query})
#     else:
#         form = ContactForm()
#         return render(request,'user/contactus.html', {'form':form} )

def contactus(request):
    if request.method == 'POST':
        nm = request.POST['name']
        mail = request.POST['email']
        sub = request.POST['subject']
        msg = request.POST['message']
        print("data: ", nm,mail, sub, msg)
        q = Contactus(name=nm, email=mail, msg=msg)
        q.save()
        return render(request, 'user/contactus.html')

    return render(request,'user/contactus.html')
    
def query(request): 
    query = Contactus.objects.all()
    return render(request, 'user/query.html', {'query':query})


def current_openings(request): 
    jobs = Job.objects.all()
    return render(request, 'user/current_openings.html', {'jobs': jobs})


# nlp = spacy.load('user/model-last')     
def parse_data(request, id):
    pass

    user_name_new = str(User_Details.objects.get(pk=id))[:-4]
    doc = fitz.open(f'media/{user_name_new}.pdf')
    print(user_name_new)
    text = ""
        # Read the content of the uploaded resume
    # try:
    #     with uploaded_file.open() as f:
    #         doc = fitz.open(f)
    # except:
    #     print("Bhaii ahiya thi problem aave chhe")
    #     return HttpResponse("<h2>supports only PDF formats...</h2>")
    for page in doc:
        text += page.get_text()
    # parsed_data = parse_text(text)
        
    doc = nlp(text)      
    parsed_data = [{'label': ent.label_, 'text': ent.text} for ent in doc.ents]


    with open(f'user/templates/user/json_files/{user_name_new}.json', 'w') as f:
        f.write(str(parsed_data))
        f.close()
    with open(f'user/templates/user/json_files/{user_name_new}.json', 'r') as f:
        parsed_data = json.dumps(parsed_data)      #take a dictionary as input and returns a string as output.
        input_data = json.loads(parsed_data)       #take a string as input and returns a dictionary as output.

    # html = render_to_string(input_data)

    done = json2html.convert(json=input_data)

    with open(f"user/templates/user/parsed_resumes/{user_name_new}.html",'w', encoding="utf-8  ") as f:
        f.write(f"""<center> <h2>Resume of  {user_name_new.title()} </h2>""" )
        f.writelines(done)
        f.write("</center>")

    #return JsonResponse(parsed_data, safe=False)   #In order to allow non-dict objects to be serialized set the safe parameter to False
    return render(request, f'user/parsed_resumes/{user_name_new}.html', {'input_data':input_data}, content_type="text/html", )



def delete_ufm(request):
    if request.method == 'POST':
        print("request.POST:",request.POST)
        id = request.POST['sid']
        q = ForceSignout_User.objects.filter(pk=id).first()
        resume_file = q.user
        q.delete()
        res = f'media/{resume_file}.pdf'
        os.remove(res)

        try:
            user_nm = Questions.objects.filter(user_name=str(resume_file)).first()
            print("userrrr name: ", user_nm)
            u_id = user_nm.id
            print("___________",u_id)
            user_nm.delete()
        except Exception as e:
            print("Error", e)

        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})        
    
def delete_query(request):
    if request.method == 'POST':
        print("request.POST:",request.POST)
        id = request.POST['sid']
        q = Contactus.objects.get(pk=id)
        q.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})   

def delete_job(request):
    if request.method == 'POST':
        print("request.POST:",request.POST)
        id = request.POST['sid']
        q = Job.objects.get(pk=id)
        q.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})   

def delete(request, id):
    user = User_Details.objects.get(pk=id)
    print(user.id)
    print("Userrr: ",user)
    temp_user = str(user)

    user_del = Questions.objects.filter(user_name=temp_user[:-4])
    user_tech_del = tech_test_model.objects.filter(user_name=temp_user[:-4])
    print("del: ", user_del)
    user_del.delete()
    user_tech_del.delete()
    print("Tech test user deleted: ", user_tech_del)
    user.delete()

    pdf = f'media/{temp_user}'
    apt_test = f'user/templates/user/test_check/{temp_user[:-3]}html'
    json = f'user/templates/user/json_files/{temp_user[:-3]}json'
    resume = f'user/templates/user/parsed_resumes/{temp_user[:-3]}html'
    tech_test = f'user/templates/user/tech_test_check/{temp_user[:-3]}html'
    
    
    try:    
        if os.path.exists(pdf):
            os.remove(pdf)
            print("Deleted successfully: ",pdf)
        if os.path.exists(apt_test):
            os.remove(apt_test)
            print("Deleted successfully", apt_test)
        if os.path.exists(json):
            os.remove(json)
            print("Deleted successfully", json)
        if os.path.exists(resume):
            os.remove(resume)
            print("Deleted successfully", resume)
        if os.path.exists(tech_test):
            os.remove(tech_test)
            print("Deleted successfully", tech_test)

    except OSError as e:
        print(e)
    except Exception as e:
        print(e)

    
    if temp_user[:-4] in user_results:
        user_results.remove(temp_user[:-4])
        print(f"{temp_user[:-4]} removed")
        print("user list: ", user_results)
    
    if temp_user[:-4] in tech_test_users:
        tech_test_users.remove(temp_user[:-4])
        print(f"{temp_user[:-4]} removed")
        print("user list: ", tech_test_users)
    
    return redirect("hr")
    

@login_required(login_url="signin")
def hr(request):
    if user_name_1 is not None and user_name_1.is_admin:

        # parse_data = User_Details.objects.all()
        # # print("Parse data:" , parse_data)

        # lst = list(parse_data)
        # unique = list({resume.res: resume for resume in lst}.values())

        # from django.db.models import Q
        # unique_queryset = User_Details.objects.filter(Q(id__in=[resume.id for resume in unique]))
        # # print("unique : ",unique_queryset)

        # query = Contactus.objects.all()
        # ufm_users = ForceSignout_User.objects.all()

        # context = {
        #     'parse_data':unique_queryset,
        #     'query': query,
        #     'ufm_users' : ufm_users   
        # }

        # if request.method == 'POST':
        #     job_tile = request.POST['job_tile']
        #     dept = request.POST['depart']
        #     desc = request.POST['desc']
        #     reqr = request.POST['reqr']
        #     # print("data: ", nm,mail, sub, msg)
        #     new_job = Job(title=job_tile, department=dept, description=desc, requirements=reqr)
        #     new_job.save()
        #     return render(request, 'user/hr.html')


        # if request.method == 'POST':
        #     jn = request.POST['job_name']
        #     dept = request.POST['depart']
        #     desc = request.POST['desc']
        #     reqr = request.POST['reqr']
        #     new_job = Job(title=jn, department=dept, description=desc, requirements=reqr)
        #     new_job.save()
        #     stud_data = Job.objects.values()
        #     stud_data = list(stud_data)
        #     return JsonResponse({'status': 'Save', 'stud_data':stud_data})


        users_to_remove = ForceSignout_User.objects.values('user')
        user_details_to_remove = User_Details.objects.filter(user_nm__in=Subquery(users_to_remove))
        user_details_to_remove.delete()

        parse_data = User_Details.objects.all()
        # print("Parse data:" , parse_data)
        query = Contactus.objects.all()
        ufm_users = ForceSignout_User.objects.all()
        print("Ufm :", ufm_users)

        jobs = Job.objects.all()
        form = JobForm()
        context = {
            'parse_data': parse_data,
            'query': query,
            'ufm_users' : ufm_users,  
            'jobs' : jobs,
            'form' : form
        }
        return render(request,'user/hr.html', context)
    else:
        return redirect("hr")
    
@login_required(login_url="signin")
def usermgnt(request):
    if user_name_1 is not None and user_name_1.is_masteruser:
        context  = {}
        user_model = get_user_model()
        demps = user_model.objects.all()
        context['demps'] = demps

        if request.method=="POST":
            print("request.POST:",request.POST)
            id = request.POST['useridd']
            q = user_model.objects.get(pk=id)
            q.delete()   
        return render(request,'user/usermgnt.html',context)
    else:
        return redirect("/")



# def delete_job(request):
#     if request.method == 'POST':
#         print("request.POST:",request.POST)
#         id = request.POST['sid']
#         q = Job.objects.get(pk=id)
#         q.delete()
#         return JsonResponse({'status':1})
#     else:
#         return JsonResponse({'status':0})   
    


def editadmin(request,id):
    if request.method == 'POST':
        print("post method chheh")
        is_admin = request.POST['isadmin']
        print("--", is_admin)
        user_model = get_user_model()
        updatequery = user_model.objects.get(id=id)
        updatequery.is_admin = is_admin
        updatequery.save()
        return redirect("usermgnt")

def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            jt = request.POST['title']
            depart = request.POST['department']
            desc = request.POST['description']
            reqr = request.POST['requirements']

            usr = Job(title=jt, department=depart, description=desc, requirements=reqr)
            usr.save()
            stud_data = Job.objects.values()
            stud_data = list(stud_data)
            return JsonResponse({'status': 'Save', 'stud_data':stud_data})
        else:
            return JsonResponse({'status': 0})

def candidate(request):
    if user_name_1 is not None:
        if User_Details.objects.filter(user_nm=request.user).exists():
            return redirect("test")
        else:
            if request.method == "POST":
                print("POST data : ", request.POST)
                global job
                job = request.POST.get('job')
                print(job)
                print("post data: ", request.POST)
                form = ResumeForm(request.POST, request.FILES)  

                # file = request.FILES['res']
                # user = User_Details.objects.create(res=file)
                uploaded_file = request.FILES['res']
                # print("uploaded file name: ",uploaded_file)

                uploaded_file.name = str(user_name_1) + '.pdf'
                # print("uploaded file.name: ", uploaded_file.name)

                file_path = f'media/{uploaded_file.name}'

                try: 
                    if os.path.exists(file_path):
                        print(f"The file '{file_path}' exists.")
                        os.remove(file_path)
                        print("removed", file_path)
                        file_d = User_Details.objects.filter(res=uploaded_file)
                        print("fiile d: ", file_d)
                        file_d.delete()
                        print("file deleted")
                        file = User_Details.objects.create(user_nm=request.user, res=uploaded_file, job_role=job)
                        # print(file)
                        file.save()
                        msg = "Click here to start test"
                        return render(request,'user/candidate.html', {'msg':msg})
                    else:
                        file = User_Details.objects.create(user_nm=request.user, res=uploaded_file, job_role=job)
                        # print(file)
                        file.save()
                        msg = "Click here to start test"
                        return render(request,'user/candidate.html', {'msg':msg})
                        # return render(request,'user/resume_uploaded.html')
                        # return HttpResponse("id :  " +str(user.pk) + str(user.res))
                                
                except OSError as e:
                    print(e)
                except Exception as e:
                    print(e)


            else:
                jobs = Job.objects.all()
                form = ResumeForm()
    else:
        return redirect("/")
    return render(request, 'user/candidate.html',{'form':form, 'jobs':jobs})


def employee(request):
    return render(request,'user/employee.html')


def dataview(request,id):
    # pass
    parse_data(request, id) 

    user = User_Details.objects.get(pk=id)
    user_name = str(user)[:-3] + 'html'
    return render(request, f'user/parsed_resumes/{user_name}')


global user_results
user_results = []

def test_check(request, id): 
    user_name_test = str(User_Details.objects.get(pk=id))[:-4]

    user_0 = Questions.objects.filter(user_name=str(user_name_test))
    global test_user_len
    test_user_len = len(user_0)
    if user_0 is not None and test_user_len>0:
        
        first_item = user_0.first()  # Retrieve the first item in the queryset
        user_0 = first_item.user_name  # Replace 'field_name' with the name of the field you want to retrieve
        print("user_0: ",user_0)
        
        if os.path.exists(f'user/templates/user/test_check/{user_name_test}.html'):
            print("os file exits")
            return render(request, f"""user/test_check/{user_name_test}.html""")
        else:
            
            model_data = Questions.objects.filter(user_name=user_0).values()
            mydata = model_data[0]['selected_answer']
            mydata = eval(mydata)

            ques_lst = model_data[0]['question_number']
            ques_lst = eval(ques_lst)

            # print("Data : ",request.POST)
            # print("form is valid")
            user_answers = {}

            question_num = mydata.keys()
            question_num = {key: mydata[key] for key in question_num if key.startswith('question_')}
            # question_num = {key.split('_')[1]: value for key, value in question_num.items()}
            lst = []
            for key, value in question_num.items():
                question_num = key.split('_')[1]
                lst.append(question_num)
                # question_num = key
                user_answers[question_num] = value.strip()
            # print("lst  :  ",lst)
            print("user ans : " , user_answers)
                
            global score 
            score = 0
            user_wrong = []
            correct_ans = []
            correct_ans_lst = []

            i = 1
            for index, row in apt_data.iterrows():
                while i <= len(lst):
                    question_num = lst[index]   
                    print("Question num : ", question_num)
                    correct_answer = apt_data['Answers'][int(question_num)] 
                    print("correct_answer: ",correct_answer)
                    if user_answers.get(question_num) == correct_answer:
                        correct_ans_lst.append(apt_data['Questions'][int(question_num)])
                        print("True")
                        score += 1
                    else:
                        print("False")   
                        user_wrong.append(apt_data['Questions'][int(question_num)])
                        correct_ans.append(correct_answer)
                    index+=1
                    i +=1
                    print("--------------------------------------")
                num_questions = apt_sample.shape[0]
                context = {
                    'score': score, 
                    'user_wrong': user_wrong, 
                    'correct_ans': correct_ans, 
                    'correct_ans_lst': correct_ans_lst, 
                    'num_questions': num_questions,
                    'user_name_test' : user_name_test
                    } 

            print("Correct: ", correct_ans_lst)
            print("wrong : ", user_wrong)
            attempted_ques = len(correct_ans_lst) + len(user_wrong)  
            skip_ques = num_questions - attempted_ques

            with open(f'user/templates/user/test_check/{user_name_test}.html', 'w',encoding="utf-8") as f:
                f.write(f""" <center> <h1> Test Result of {user_name_test.title()}: {str(score)}/{num_questions} <br> """)
                print(f'Score of {user_name_test} : {score}/{num_questions}') 
                f.write(f""" <h2> Attempted Questions : {attempted_ques} and Skipped Questions : {skip_ques}  </h2> """)

                if len(correct_ans_lst) == 0:   
                    f.write("<h2> Correcct Answers = 0")
                else:
                    f.write(f"""<table border=1 width=50%>
                        <tr>
                            <th> No. </th>
                            <th> Correct Answers </th>
                        </tr>""")

                    for i in correct_ans_lst:  
                        f.write(f"""
                                <tr>
                                    <td align="center">{correct_ans_lst.index(i) + 1}</td>
                                    <td> {i} </td>
                                </tr>
                        """) 

                if len(user_wrong) == 0:
                    f.write("<h2> Wrong Answers = 0")
                else:
                    f.write(f"""</table> <br> <table border=1 width=50%>
                            <tr>
                                <th> No. </th>
                                <th> Wrong Answers </th>
                            </tr>""")

                    for i in user_wrong:  
                        f.write(f"""
                                <tr>
                                    <td align="center">{user_wrong.index(i) + 1}</td>
                                    <td> {i} </td>  
                                </tr>
                        """) 
                
                f.write(f"</table></center>")

            return render(request, f"""user/test_check/{user_name_test}.html""", context)

 

global apt_data 
apt_data = pd.read_csv("user/templates/user/QA_CSV/new_aptitute.csv")
apt_data['Options'] = apt_data['Options'].str.split(',')
global apt_sample
apt_sample = apt_data.sample(15)  





@login_required(login_url="signin")
def test(request): 
    msg = ""
    if 'apt_sample' not in request.session:
        apt_data = pd.read_csv("user/templates/user/QA_CSV/new_aptitute.csv")
        apt_data['Options'] = apt_data['Options'].str.split(',')
        apt_sample = apt_data.sample(15)
        request.session['apt_sample'] = apt_sample.to_dict(orient='records')
    else:
        apt_sample = pd.DataFrame(request.session['apt_sample'])

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=30)  # Set the timer to 30 minutes
    end_time_unix_timestamp = int(end_time.timestamp() * 1000)  # Convert to Unix timestamp in milliseconds
    

    force_signout_user = ForceSignout_User.objects.filter(user=request.user).exists()
    print("user_fs = ",force_signout_user)
    if force_signout_user:
        return render(request, "user/force_signout.html")
        # return HttpResponse("You are not allowed to take the test.")
    elif Questions.objects.filter(user_name=request.user).exists():
        return render(request, 'user/applied_test.html')
        # return HttpResponse("<h3>You have already given the test</h3>")
    else:   
        if request.method == 'POST':

            global form_data    
            form_data = request.POST    

            user_answers = {}
   
            question_num = form_data.keys()
            question_num = {key: form_data[key] for key in question_num if key.startswith('question_')}
            # question_num = {key.split('_')[1]: value for key, value in question_num.items()}
            
            ques_lst = []
            for key, value in question_num.items():
                question_num = key
                user_answers[question_num] = value.strip()
                ques_lst.append(key)
            print("user ans : " , user_answers)

            question = Questions.objects.create(user_name = str(user_name_1), question_number=ques_lst, selected_answer=user_answers)
            question.save()
            return render(request, 'user/test_complete.html')
        else:
            pass
        context = {
            'apt_sample': apt_sample,
            'end_time': end_time_unix_timestamp,
        }

        # user_t = User_Details.objects.filter(user_nm=user_name_1).first()
        # print("user test: ", user_t)
        # user_id = user_t.id
        # print("id: ", user_id)
        # test_check(request, user_id)

        return render(request, 'user/test.html', context)


def test_result(request,id):
    test_check(request, id)

    user = User_Details.objects.get(pk=id)
    
    # id = User_Details.objects.filter(res=user).values('id')[0]['id']
    # print("idddd:", id) 
    if test_user_len>0:
        user_name = str(user)[:-3] + 'html'
        # print(f'last score of {user_name} : {score}')
        return render(request, f'user/test_check/{user_name}')
    else:
        return HttpResponse("<h2> Candidate has not given the aptitude test. </h2>")

global tech_test_users
tech_test_users = []

def tech_test_check(request,id):
    print("users : ", tech_test_users)
    user_name_test = str(User_Details.objects.get(pk=id))[:-4]

    user_0 = tech_test_model.objects.filter(user_name=str(user_name_test))
    global tech_test_user_len 
    tech_test_user_len = len(user_0)
    if user_0 is not None and tech_test_user_len>0:

        first_item = user_0.first()  # Retrieve the first item in the queryset
        user_0 = first_item.user_name  # Replace 'field_name' with the name of the field you want to retrieve
        print("user_0: ",user_0)

        if os.path.exists(f'user/templates/user/tech_test_check/{user_name_test}.html'):
            print("os file exits")
            return render(request, f"""user/tech_test_check/{user_name_test}.html""")
        else:

            model_data = tech_test_model.objects.filter(user_name=user_0).values()
            mydata = model_data[0]['selected_answer']
            mydata = eval(mydata)

            ques_lst = model_data[0]['question_number']
            ques_lst = eval(ques_lst)
            total_ques = len(ques_lst)


            user_answers = {}
            q_write = []
            a_write = []
            score_write = []
            question_num = mydata.keys()
            question_num = {key: mydata[key] for key in question_num if key.startswith('question_')}
            # question_num = {key.split('_')[1]: value for key, value in question_num.items()}
            lst = []
            for key, value in question_num.items():
                question_num = key.split('_')[1]
                lst.append(question_num)
                # question_num = key
                user_answers[question_num] = value.strip()
            print("lst  :  ",lst)
            # print("user ans : " , user_answers)

            ans_avg = []
            global result_score
            result_score = 0
            for key, value in user_answers.items():
                question_number = int(key)
                if len(value.split())> 10:
                    q_write.append(tech_data["Questions"][question_number])
                    a_write.append(value)

                actual_a = tech_data["Answers"][question_number]
                user_ans_1 = value
                print("-------------------------------------------------------------")
                user_prompt = 'User Ans: '+user_ans_1+'\n'+'Actual Ans: '+actual_a
                print("Question: ", tech_data["Questions"][question_number])
                print("User_promt: ", user_prompt)
                print("-------------------------------------------------------------")

                user_ans_len = len(user_ans_1.split())
                print("User ans len: ", user_ans_len)

                if user_ans_len > 10:
                    for i in range(7):
                        score = get_gemini_response(input_prompt, user_prompt)
                        ans_avg.append(score)

                    print(f"7 score list : {ans_avg}")
                    print(f"Avg score is : {np.average(ans_avg)}")
                    res_scr = round(np.average(ans_avg))
                    score_write.append(round(res_scr))
                    result_score += round(np.average(ans_avg))
                ans_avg = []
            with open(f'user/templates/user/tech_test_check/{user_name_test}.html', 'w',encoding="utf-8") as f:
                f.write(f"""<center> <h1> Test Result of {user_name_test.title()}: {str(round(result_score))}/{total_ques * 10}  <br>""")
                print(f'Final Score of {user_name_test} : {round(result_score)}/{total_ques * 10}') 
                print("score list: ", score_write)
                
                for i in q_write:
                    print("----------------------Question: ", i)
                for i in a_write:
                    print("-----------------------Answer: ", i)

                if result_score>0:
                    f.write(f"""<center> <table border=1 width=50%>
                        <tr>
                            <th> No. </th>
                            <th> Question </th>
                            <th> Answer </th>
                            <th> Marks </th>
                        </tr>""")
                    
                    for i,j,k in zip(q_write,a_write,score_write):
                        f.write(f""" 
                        <tr>
                            <td align="center">{q_write.index(i) + 1}</td>
                            <td> {i} </td>
                            <td> {j} </td>
                            <td align="center"> {k} </td>
                        </tr> 
                        """)
                    f.write("</table> </center>")
                    return render(request, f"""user/tech_test_check/{user_name_test}.html""")



def tech_test_result(request,id):
    tech_test_check(request, id)

    user = User_Details.objects.get(pk=id)

    # id = UserResume.objects.filter(res=user).values('id')[0]['id']
    # print("idddd:", id) 
    if tech_test_user_len>0:
        user_name = str(user)[:-3] + 'html'
        # print(f'last score of {user_name} : {result_score}')
        return render(request, f'user/tech_test_check/{user_name}')
    else:
        return HttpResponse("<h2> Candidate has not given the technical test. </h2>")


def result(request):
    return render(request, 'user/result.html') 

def test_complete(request):
    return render(request, 'user/test_complete.html')

def apt_info(request):
    return render(request, 'user/apt_info.html')



from .gemini import get_gemini_response, input_prompt


# global tech_data
# tech_data = pd.read_csv(f"C:/Users/Operator/Documents/My Received Files/Akshit/Palak/Palak/CampusX/webscraping/QA_CSV/tech_test.csv")
# global tech_sample
# tech_sample = tech_data.sample(15)

@login_required(login_url="signin")
def tech_test(request):
    msg=""
    global tech_data
    tech_data = pd.read_csv(f"user/templates/user/QA_CSV/Tech_test/{job}.csv")
    if 'tech_sample' not in request.session:
        tech_data = pd.read_csv(f"user/templates/user/QA_CSV/Tech_test/{job}.csv")
        tech_sample = tech_data.sample(15)
        request.session['tech_sample'] = tech_sample.to_dict(orient='records')
    else:
        tech_sample = pd.DataFrame(request.session['tech_sample'])


    start_time = datetime.now()
    # print("start time: ", start_time)
    end_time = start_time + timedelta(minutes=60)  # Set the timer to 30 minutes
    # print("end time: ", end_time)

    end_time_unix_timestamp = int(end_time.timestamp() * 1000)  # Convert to Unix timestamp in milliseconds


    if tech_test_model.objects.filter(user_name=request.user).exists():
        return render(request, 'user/applied_test.html')
        # return HttpResponse("<h3>You have already given the test</h3>")
    else:
        if request.method == "POST":
            global form_data_model 
            form_data_model = request.POST  
            user_answers = {}

            question_num = form_data_model.keys()
            question_num = {key: form_data_model[key] for key in question_num if key.startswith('question_')}
            
            ques_lst = []   
            for key, value in question_num.items():
                question_num = key
                # Replace line breaks with spaces
                cleaned_answer = value.replace('\r\n', ' ')
                user_answers[question_num] = cleaned_answer.strip()
                ques_lst.append(key)
            print("user ans --------------- : ", user_answers)


            question = tech_test_model.objects.create(user_name = str(user_name_1), question_number=ques_lst, selected_answer=user_answers)
            question.save() 

            # test_check(request, user_id)
            # tech_test_check(request, user_id)
            return render(request, 'user/thanks.html')

        else:
            pass
        context = {
            'tech_sample': tech_sample,
            'end_time': end_time_unix_timestamp 
        }
        return render(request, 'user/tech_test.html', context)

    
def thanks(request):
    return render(request, 'user/thanks.html')


