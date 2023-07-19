#using streamlit for developing GUI
import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")
streamlit.header("Breakfast Favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# using pandas
# import pandas

#read file from s3 through pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#fruits to show
fruits_to_show= my_fruit_list.loc[fruits_selected]

#to show the dataframe in tabular for in streamlit
streamlit.dataframe(fruits_to_show)


# create a function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+str(fruit_choice).lower())
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("please select a fruit to get information")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")
# snowflake related function
def get_fruit_load_list(my_cnx):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

# add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list(my_cnx)
  streamlit.dataframe(my_data_rows)


# function to allow user to add a fruit to the list
def insert_row_snowflake(my_cnx,new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('{}')".format(new_fruit))
    return "thank you for adding "+new_fruit


add_my_fruit=streamlit.text_input("What fruit would you like to add ?")

if add_my_fruit:
  if streamlit.button('Add a fruit to the list'):
    my_cnx1=snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function=insert_row_snowflake(my_cnx1,add_my_fruit)
    streamlit.text(back_from_function)
  

