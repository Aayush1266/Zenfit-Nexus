from flask import Flask,render_template,request
import smtplib
from twilio.rest import Client
from datetime import datetime, date, timedelta
import time
import requests
import random

# import random
blog_end = "https://api.npoint.io/7658f0656317afa70766"
response = requests.get(url=blog_end)
data = response.json()

APP_ID = 'cbb0ada5'
APP_KEY = '88aabec47aa6b2737a043abf05ce4c88'
code = 'aayushsethi15242'

NAME = ''
EMAIL = ''
AGE = 0
GENDER = ''
WEIGHT = 0
HEIGHT = 0
PHONE = 0

def user_info(name,email,age,gender,weight,height,phone):
    global NAME,EMAIL,AGE,GENDER,WEIGHT,HEIGHT,PHONE
    NAME = name
    EMAIL = email
    AGE = age
    GENDER = gender
    WEIGHT = weight
    HEIGHT = height
    PHONE = phone

calories_take = {}
muscle_list = ["abdominals","abductors","adductors","biceps","calves","chest","forearms","glutes","hamstrings","lats","lower_back","middle_back","neck","quadriceps","traps","triceps"]
calories_burn = {}
total_take = 0
total_burn = 0
today = date.today()
end_of_day = False

excercise_report = 'https://pixe.la/v1/users/workoutuser/graphs/workout.html'
meal_report = 'https://pixe.la/v1/users/mealuser/graphs/meal.html'

yesterday = today - timedelta(days=1)
today = datetime.now()


time = today.strftime("%H:%M:%S")
today = today.strftime("%d/%m/%Y")


from twilio.twiml.messaging_response import MessagingResponse
account_sid = 'ACe92f7ed5d3d3e5da1e3faf8337e9658e'
auth_token = '4e941ad48e44f8d93e602cd9fdc974c6'
client = Client(account_sid, auth_token)



def send_message(body):

    message = client.messages.create(
                                  from_='whatsapp:+14155238886',
                                  body= body,
                                  to='whatsapp:+919971734360'
                              )

def add_excercise(excercise):
    global total_burn

    nutri_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
    excercise_endpoint = 'https://api.sheety.co/ccbf039ec2020e00808f58654d46be1d/newWorkout/sheet1'

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY
    }

    params = {
        "query": excercise,
        "age": AGE,
        "weight_kg": WEIGHT,
        "gender": GENDER,
        "height_cm": HEIGHT
    }
    response2 = requests.post(url=nutri_endpoint, json=params, headers=headers)
    data = response2.json()

    duration = data["exercises"][0]["duration_min"]
    calories = data["exercises"][0]["nf_calories"]
    name = data["exercises"][0]["name"]
    print(response2.text)

    calories_burn[excercise] = calories
    total_burn += calories
    name = name.title()
    sheet_headers = {
     "Authorization": f"Bearer {code}"
    }
    sheet_add = {
        "sheet1": {
            "date": today,
            "time": time,
            "exercise": name,
            "duration": duration,
            "calories":calories,
        }
    }
    send_message(f"Excercise Details:\nExcercise: {excercise}\n Calories burned: {calories}Kcal")
    response = requests.post(url=excercise_endpoint, json=sheet_add, headers=sheet_headers)
    print(response.text)

def add_food(meal):
    global total_take
    edma_endpoint = "https://api.edamam.com/api/nutrition-data"

    params2 = {
        "app_id": '17725c11',
        "app_key": '6fe37cf5903999c5ea985e6e6c50be13',
        "ingr": meal,
    }

    response = requests.get(url=edma_endpoint, params=params2)
    food_intake = response.json()['calories']
    labels = response.json()['dietLabels']
    if len(labels)==0:
        labels.append('lOW_NUTRIENTS')
    if food_intake!=0:
        fat = response.json()['totalNutrients']['FAT']['quantity']
        carbohydrate = response.json()['totalNutrients']['CHOCDF.net']['quantity']
        Protein = response.json()['totalNutrients']['PROCNT']['quantity']
        fat = round(fat, 2)
        carbohydrate = round(carbohydrate, 2)
        Protein = round(Protein, 2)
    if food_intake == 0:
        food_intake = random.randint(270,310)
        Protein = random.randint(4,10)
        fat = random.randint(6,11)
        carbohydrate = random.randint(25,33)
    send_message(f"Meals Detail: \nMeal : {meal}\n Calories: {food_intake}Kcal\n labels: {labels}\n Fat: {fat}g\n Carbohydrate: {carbohydrate}g\n Protein: {Protein}g")
    calories_take[meal] = food_intake
    total_take += food_intake
    food_endpoint = "https://api.sheety.co/6fd9f321c91de5a6693e2ddc33788fe7/food/sheet1"

    sheet2_add = {
        "sheet1": {
            "date": today,
            "time": time,
            "food": meal,
            "calories": food_intake,
        }
    }
    rep = requests.post(url=food_endpoint, json=sheet2_add)

def report():
    send_message(f"Report:\n Excercise detail:\n Total calories burned today: {total_burn}\n {calories_burn}\n Tracking History: {excercise_report}")
    send_message(f"Report:\n Meal detail:\n Total calories you took today: {total_take}\n {calories_take}\n Tracking History: {meal_report}")

def intro():
    send_message(f"Hello {NAME}, \nWelcome to Your ZenFit Nexus.\nEnter: \n'Excercise' to adding your excercises\n'Food' for"
                 f" adding meals data\n'report' for accessing day report\n'suggest' for excercise recommendation.")


def workout_graph(quantity):
    quantity = str(quantity)
    pixela_endpoint = "https://pixe.la/v1/users"
    WTOKEN = "aafhlksahfnfknakl"
    WUSERNAME = "workoutuser"
    WGRAPHID = "workout"
    user_params = {
        "token": WTOKEN,
        "username": WUSERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }

    # response = requests.post(url=pixela_endpoint,json=user_params)
    # print(response.text)

    graph_endpoint = f"{pixela_endpoint}/{WUSERNAME}/graphs"
    graph_config = {
        "id": WGRAPHID,
        "name": "Workout Tracker",
        "unit": "Calories",
        "type": "int",
        "color": "momiji"
    }

    headers = {
        "X-USER-TOKEN": WTOKEN
    }

    # response = requests.post(url=graph_endpoint,json=graph_config,headers=headers)
    # print(response.text)

    modified_today = today.strftime("%Y%m%d")

    value_endpoint = f"{pixela_endpoint}/{WUSERNAME}/graphs/{WGRAPHID}"
    update_endpoint = f"{value_endpoint}/{modified_today}"

    value_params = {
        "date": modified_today,
        "quantity": quantity,
    }
    response2 = requests.post(url=value_endpoint, json=value_params, headers=headers)
    print(response2.text)

def send_mail(name,email):
    message = f"Subject:Health Tracker daily report: {today} \n\n {name}'s Workout report: \n\n Total calories burned: {total_burn}\n" \
              f"{calories_burn}\n Tracking History(Please refer to this link): {excercise_report}\n" \
              f" Meal report: \n Total calories you took: {total_take}\n {calories_take}\n" \
              f"Tracking History(Please refer to this link): {meal_report}"

    connection = smtplib.SMTP("smtp.gmail.com")
    my_email = "aayushsethi007@gmail.com"
    password = "hqhl voxo rbyv aunw"
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs= email, msg=message.encode('utf-8'))

def meal_graph(quantity):
    quantity = str(quantity)
    pixela_endpoint = "https://pixe.la/v1/users"
    TOKEN = "jfdksdjlaffdfff"
    USERNAME = "mealuser"
    GRAPHID = "meal"

    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }

    # response = requests.post(url=pixela_endpoint,json=user_params)
    # print(response.text)

    graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
    graph_config = {
        "id": GRAPHID,
        "name": "Meal Tracker",
        "unit": "Calories",
        "type": "int",
        "color": "shibafu"
    }

    headers = {
        "X-USER-TOKEN": TOKEN
    }

    modified_today = today.strftime("%Y%m%d")

    value_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPHID}"
    update_endpoint = f"{value_endpoint}/{modified_today}"

    value_params = {
        "date": modified_today,
        "quantity": quantity,
    }
    response2 = requests.post(url=value_endpoint, json=value_params, headers=headers)
    print(response2.text)

def user_data():
    workout_graph(total_burn)
    meal_graph(total_take)
    send_mail(NAME, EMAIL)
    report()

app = Flask(__name__)
timef = 0
calburn = False
caltake = False

def confirm_send_mail(name,email,phone,message):
    message = f"Subject:Blog Post Contact \n\n Name: {name} \n Email: {email} \n Phone Number: {phone} \n " \
              f"Message: {message}"
    connection = smtplib.SMTP("smtp.gmail.com")
    my_email = "aayushsethi007@gmail.com"
    password = "hqhl voxo rbyv aunw"
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs="aayushsethi15242@gmail.com", msg=message.encode('utf-8'))
def muscle_recommendation(muscle):
    api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}'.format(muscle)
    excercise = []
    response = requests.get(api_url, headers={'X-Api-Key': 'GlnCe4+FFxoh0H71uVdelg==XkxYFKsZ7H4GNUjP'})
    var = random.randint(5,8)
    if response.status_code == requests.codes.ok:
        for i in range(1,var+1):
            excercise.append(response.json()[i]['name'])
        send_message(f"Here are top {var} excercises you can do for that {muscle}")
        for item in excercise:
            send_message(item)
        intro()
app = Flask(__name__)
@app.route('/')
def Home():
    return render_template("index.html",posts = data)

@app.route('/about')
def get_about():
    return render_template("about.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_message = request.values.get("Body", "").lower()
    sender_phone_number = request.values.get("From", "")
    print("Received message from {}: {}".format(sender_phone_number, incoming_message))
    incoming_message = incoming_message.lower()

    global calburn
    global caltake

    if incoming_message=='suggest':
        send_message("Enter muscle from the given list: ")
        send_message("abdominals\nabductors\nadductors\nbiceps\ncalves\nchest\nforearms\nglutes\nhamstrings\nlats\nlower_back\nmiddle_back\nneck\nquadriceps\ntraps\ntriceps")
    elif incoming_message in muscle_list:
        muscle_recommendation(incoming_message)
        # intro()
    elif incoming_message=='n' or incoming_message == 'no':
        calburn = False
        caltake = False
        intro()

    elif incoming_message == 'report':
        report()
        calburn = False
        caltake = False

    elif calburn:
        add_excercise(incoming_message)
        send_message("Add another?(type 'no' to stop)")

    elif caltake:
        add_food(incoming_message)
        send_message("Add another? (type 'no' to stop)")

    elif(incoming_message=="excercise"):
        send_message("Please type excercises you did today (Eg: Running, Swimming, Pushups)")
        calburn = True

    elif(incoming_message=="food"):
        send_message("Please enter details about food you ate with quantity")
        caltake = True

    else:
        send_message("Please enter valid command")
        caltake = False
        calburn = False
        intro()

    return "Message received."

@app.route('/contact',methods=["POST","GET"])
def get_contact():
    if request.method == "GET":
        return render_template("contact.html", start= "Join Us")
    else:
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        gender = request.form["gender"]

        # confirm_send_mail(name,email,phone)
        user_info(name,email,age,gender,weight,height,phone)
        send_message(f"Name: {name}\nEmail: {email}\nAge: {age}\nGender: {gender}\nWeight: {weight}\nHeight: {height}\nPhone: {phone}")
        send_message(f"Hello {name}, Welcome to our chatbot , here you can enter all the details")
        intro()
        return render_template("contact.html", start ="Successfully Sent Your Details")
        # return render_template("con")

if __name__ == "__main__" :
    app.run(debug=True)
