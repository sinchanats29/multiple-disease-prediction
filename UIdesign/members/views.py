from django.shortcuts import render,redirect, get_object_or_404
from sklearn.linear_model import LogisticRegression
from .forms import ImageUploadForm
from PIL import Image
import joblib
import markdown2
from .models import Diabetespatientdata,parkinsonformdata,heartformdata
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from IPython.display import Markdown
from IPython.display import display
import textwrap

import google.generativeai as genai
genai.configure(api_key="AIzaSyCsxihphRnek2p2B7qx3NBM4T3nUwpwwLo")


# Create your views here.
def home(request):
    return render(request,'index.html')

@login_required(login_url='doctorlogin')
def doctorhome(request):
    return render(request,'doctorhome.html')

def diabetespatientlist(request):
    return render(request,'diabetespatientlist.html')

def heartpatientlist(request):
    return render(request,'heartpatientlist.html')

def parkinsonpatientlist(request):
    return render(request,'parkinsonpatientlist.html')

def registerpage(request):
    return render(request,'register.html')

def contactform(request):
    name = request.POST['name']
    emailid = request.POST['email']
    subject= request.POST['subject']
    message=request.POST['message']
    return render(request,'services.html')

def predictheart(request):
    return render(request,'predictheart.html')

def predictdiabetes(request):
    return render(request,'predictdiabetes.html')

def predictparkinson(request):
    return render(request,'predictparkinson.html')

def result(request):
    return render(request,'result.html')

@login_required(login_url='login')
def healthgpt(request):
    return render(request,'healthgpt.html') 

@login_required(login_url='login')
def services(request):
    return render(request,'services.html')

def output(request):
    return render(request,'output.html')

# login member
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Eroor While Logging in Try Again")
        
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'login.html')

def doctorloginpage(request):
    if request.user.is_authenticated:
        return redirect('doctorhome')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Eroor While Logging in Try Again")
        
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('doctorhome')
    return render(request,'doctorlogin.html')

# register member
def registersubmit(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username,password=password)
        user.save()
        login(request,user)
        return redirect('home')
    else:
        form = UserCreationForm()
    return render(request,'register.html')
# logout member
def logoutuser(request):
    logout(request)
    return redirect('home')

def doctorlogout(request):
    logout(request)
    return redirect('doctorhome')

# Diabetes data fetching
def display_diabetes_data(request):
    all_data = Diabetespatientdata.objects.all()  # Fetch all DiabetesData objects
    context = {'all_data': all_data}
    return render(request, 'diabetespatientlist.html', context)

# heart data fetching
def display_heart_data(request):
    all_data = heartformdata.objects.all()  # Fetch all DiabetesData objects
    context = {'all_data': all_data}
    return render(request, 'heartpatientlist.html', context)

# parkinson data fetching
def display_parkinson_data(request):
    all_data = parkinsonformdata.objects.all()  # Fetch all DiabetesData objects
    context = {'all_data': all_data}
    return render(request, 'parkinsonpatientlist.html', context)

# Individual Diabetes data fetching
def diabetes_individual_details(request, data_id):
    data_entry = get_object_or_404(Diabetespatientdata, pk=data_id)
    context = {'data_entry': data_entry}
    return render(request, 'diabetesdatadisplay.html', context)

# Individual heart data fetching
def heart_individual_details(request, data_id):
    data_entry = get_object_or_404(heartformdata, pk=data_id)
    context = {'data_entry': data_entry}
    return render(request, 'heartdatadisplay.html', context)

def update_heart_doctorverdict(request, data_id):
    heart_update = get_object_or_404(heartformdata, pk=data_id)  # Get object by ID
    heart_update.doctorverdict = request.POST['heartdoctorverdict']
    heart_update.save()
    return render(request, 'doctorhome.html')

def update_diabetes_doctorverdict(request, data_id):
    diabetes_update = get_object_or_404(Diabetespatientdata, pk=data_id)  # Get object by ID
    diabetes_update.doctorverdict = request.POST['diabetesdoctorverdict']
    diabetes_update.save()
    return render(request, 'doctorhome.html')

def update_parkinson_doctorverdict(request, data_id):
    parkinson_update = get_object_or_404(parkinsonformdata, pk=data_id)  # Get object by ID
    parkinson_update.doctorverdict = request.POST['parkinsondoctorverdict']
    parkinson_update.save()
    return render(request, 'doctorhome.html')

# Individual parkinson data fetching
def parkinson_individual_details(request, data_id):
    data_entry = get_object_or_404(parkinsonformdata, pk=data_id)
    context = {'data_entry': data_entry}
    return render(request, 'parkinsondatadisplay.html', context)

def diabetesdatadisplay(request):
    return render(request,'diabetesdatadisplay.html')

def parkinsondatadisplay(request):
    return render(request,'parkinsondatadisplay.html')

def heartdatadisplay(request):
    return render(request,'heartdatadisplay.html')


# healthgpt model

ALLOWED_TOPICS = ["heart", "diabetes", "parkinson","health","healthy","affects","diet","cardiac","attack","arrest"]

def to_markdown(text):
  text = text.replace('•', '  *')
  markdown_content =  markdown2.markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
  return markdown_content

def ask_gemini(question):
    question_words = question.lower().split()
    related_topics = [topic for topic in question_words if topic in ALLOWED_TOPICS]

    if related_topics:
        model = genai.GenerativeModel("gemini-1.5-pro-latest") 
        response = model.generate_content(question)
        response_markdown = to_markdown(response.text)
        return response_markdown
    else:
        text = "Please ask questions related to heart disease, diabetes, or Parkinson's disease."
        return text

def index(request):
    if request.method == "POST":
        question = request.POST.get('question')
        if question:
            answer = ask_gemini(question)
            return render(request, 'healthgpt.html', {'question': question, 'answer': answer})
        else:
            return redirect('index')  # Redirect if no question submitted

    return render(request, 'healthgpt.html')

    # end healthgpt model



#  Image Model 
@login_required(login_url='login')
def process_image(request):

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            imagedata = Image.open(image)
            response = get_gemini_response(imagedata)
            return render(request, 'output.html', {'image_description': response})
    else:
        form = ImageUploadForm()
    return render(request, 'healthyfood.html')

def get_gemini_response(imagedata):
    input = """Reply only if image is related to food or else reply give me only food related image
    if image is related to food in first paragraph tell about the food in second paragraph give calories of the food and 
    in third paragraph tell how it helps, affects,harm to health, heart ,diabetes disease
    and don't mention it is related to food
    """
    model1 = genai.GenerativeModel('gemini-1.5-flash')
    response = model1.generate_content([input,imagedata])
    # return response.text
    response_markdown = to_markdown(response.text)
    return response_markdown

# End image model

# predict diabetes model

def diabetesresults(request):
    cls = joblib.load('diabetes_model.sav')
    lis = []
    lis.append(float(request.POST['Pregnancies']))
    lis.append(float(request.POST['Glucose']))
    lis.append(float(request.POST['BloodPressure']))
    lis.append(float(request.POST['SkinThickness']))
    lis.append(float(request.POST['Insulin']))
    lis.append(float(request.POST['BMI']))
    lis.append(float(request.POST['DiabetesPedigreeFunction']))
    lis.append(float(request.POST['Age']))
    # print(lis)
    ans = cls.predict([lis])
    print(ans)
    if 1 in ans:
        result = "You Have Diabetes,Take care of your Health"
    else:
        result = "You don't have Diabetes"

    new_data = Diabetespatientdata(
                user_id = request.POST['user_id'],
                name = request.POST['name'],
                pregnancies=request.POST['Pregnancies'],
                glucose=request.POST['Glucose'],
                blood_pressure=request.POST['BloodPressure'],
                skin_thickness=request.POST['SkinThickness'],
                insulin=request.POST['Insulin'],
                bmi=request.POST['BMI'],
                diabetes_pedigree_function=request.POST['DiabetesPedigreeFunction'],
                age=request.POST['Age'],
                modelprediction = result
            )
    new_data.save()
    return render(request, 'result.html', {'ans': result})

# end predict diabetes model

# predict heart disease model

def heartresults(request):
    # cls = pickle.load(open('heart_disease_model.sav', 'rb'))
    cls = joblib.load('heart_disease_model.sav')
    lis = []
      #age sex cp trestbps chol fbs restecg thalach exang oldpeak slope ca thal target

    lis.append(float(request.POST['age']))
    
    sex_input = request.POST['sex'].lower()  # Convert to lowercase for case-insensitivity
    if sex_input == "male":
        sex_numeric = 1.0
    else:
        sex_numeric = 0.0
    
    lis.append(float(sex_numeric))
    lis.append(float(request.POST['cp']))
    lis.append(float(request.POST['trestbps']))
    lis.append(float(request.POST['chol']))
    lis.append(float(request.POST['fbs']))
    lis.append(float(request.POST['restecg']))
    lis.append(float(request.POST['thalach']))
    lis.append(float(request.POST['exang']))
    lis.append(float(request.POST['oldpeak']))
    lis.append(float(request.POST['slope']))
    lis.append(float(request.POST['ca']))
    lis.append(float(request.POST['thal']))
    #print(lis)
    ans = cls.predict([lis])
    if 1 in ans:
        result = "You Have Heart Disease,Take care of your Health"
    else:
        result = "You don't have Heart Disease"

    heart_data = heartformdata(
                user_id = request.POST['user_id'],
                name = request.POST['name'],
                age=request.POST['age'],
                sex=request.POST['sex'],
                cp=request.POST['cp'],
                trestbps=request.POST['trestbps'],
                chol=request.POST['chol'],
                fbs=request.POST['fbs'],
                restecg=request.POST['restecg'],
                thalach=request.POST['thalach'],
                exang=request.POST['exang'],
                oldpeak=request.POST['oldpeak'],
                slope=request.POST['slope'],
                ca=request.POST['ca'],
                thal=request.POST['thal'],
                modelprediction = result
            )
    heart_data.save()

    return render(request, 'result.html', {'ans': result})

# end heart disease model

# predict parkinson model

def parkinsonresults(request):
    #cls = pickle.load(open('diabetes_model.sav', 'rb'))
    cls = joblib.load('parkinsons_model.sav')
    lis = []

    lis.append(float(request.POST['MDVP:Fo(Hz)']))
    lis.append(float(request.POST['MDVP:Fhi(Hz)']))
    lis.append(float(request.POST['MDVP:Flo(Hz)']))
    lis.append(float(request.POST['MDVP:Jitter(%)']))
    lis.append(float(request.POST['MDVP:Jitter(Abs)']))
    lis.append(float(request.POST['MDVP:RAP']))
    lis.append(float(request.POST['MDVP:PPQ']))
    lis.append(float(request.POST['Jitter:DDP']))
    lis.append(float(request.POST['MDVP:Shimmer']))
    lis.append(float(request.POST['MDVP:Shimmer(dB)']))
    lis.append(float(request.POST['Shimmer:APQ3']))
    lis.append(float(request.POST['Shimmer:APQ5']))
    lis.append(float(request.POST['MDVP:APQ']))
    lis.append(float(request.POST['Shimmer:DDA']))
    lis.append(float(request.POST['NHR']))
    lis.append(float(request.POST['HNR']))
    lis.append(float(request.POST['RPDE']))
    lis.append(float(request.POST['DFA']))
    lis.append(float(request.POST['spread1']))
    lis.append(float(request.POST['spread2']))
    lis.append(float(request.POST['D2']))
    lis.append(float(request.POST['PPE']))
    # print(lis)
    ans = cls.predict([lis])
    if 1 in ans:
        result = "You Have Parkinson Disease,Take care of your Health"
    else:
        result = "You don't have Parkinson Disease"

    parkinson_data = parkinsonformdata(
                user_id = request.POST['user_id'],
                name = request.POST['name_name'],
                MDVP_Fo_Hz = request.POST['MDVP:Fo(Hz)'],
                MDVP_Fhi_Hz = request.POST['MDVP:Fhi(Hz)'],
                MDVP_Flo_Hz=request.POST['MDVP:Flo(Hz)'],
                MDVP_Jitter_percent=request.POST['MDVP:Jitter(%)'],
                MDVP_Jitter_Abs=request.POST['MDVP:Jitter(Abs)'],
                MDVP_RAP=request.POST['MDVP:RAP'],
                MDVP_PPQ=request.POST['MDVP:PPQ'],
                Jitter_DDP=request.POST['Jitter:DDP'],
                MDVP_Shimmer=request.POST['MDVP:Shimmer'],
                Shimmer_APQ3=request.POST['Shimmer:APQ3'],
                Shimmer_APQ5=request.POST['Shimmer:APQ5'],
                MDVP_APQ=request.POST['MDVP:APQ'],
                Shimmer_DDA=request.POST['Shimmer:DDA'],
                NHR=request.POST['NHR'],
                HNR=request.POST['HNR'],
                MDVP_Shimmer_dB=request.POST['MDVP:Shimmer(dB)'],
                RPDE=request.POST['RPDE'],
                DFA=request.POST['DFA'],
                spread1=request.POST['spread1'],
                spread2=request.POST['spread2'],
                D2=request.POST['D2'],
                PPE=request.POST['PPE'],
                modelprediction = result
            )
    parkinson_data.save()

    return render(request, 'result.html', {'ans': result})

    # end parkinson model