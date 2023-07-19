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



streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("please select a fruit to get information")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+str(fruit_choice).lower())
    # streamlit.text(fruityvice_response.json())
    # write your own comment -what does the next line do? 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # write your own comment - what does this do?
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

streamlit.stop()

# working with snowflake-connector-python module
# import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit=streamlit.text_input("What fruit would you like to add?","jackfruit")
streamlit.write("thank you for adding ",add_my_fruit)
  
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
