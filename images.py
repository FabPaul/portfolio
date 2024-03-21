import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

places = [
  {"image": "Maritime-Museum.jpg", "name": "Maritime Museum - Littoral", "description": "Douala's maritime past in ships, trade, & fish", "link": "https://museemaritime.cm/en/"},
  {"image": "baka_pygmy.jpg", "name": "The Baaka Pygmies - East", "description": "The curious case of Central African Indigenes", "link": "https://www.youtube.com/watch?v=adcCFAgibj8&ab_channel=SLICE"},
  {"image": "baleng.jpg", "name": "Baffoussam - West ", "description": "The Capital of Grassfield Cameroon", "link": "https://www.mustvisitplace.com/best-tourist-places-to-visit-in-bafoussam-western-cameroon-africa/"},
  {"image": "Bamenda_city.jpg", "name": "Bamenda City - North West", "description": "Abakwa, Land of many opportunities", "link": "https://en.wikipedia.org/wiki/Bamenda"},
  {"image": "beach.jpg", "name": "The City of Limbe - South West", "description": "The CIty of Friendship", "link": "https://en.wikipedia.org/wiki/Limb%C3%A9,_Cameroon"},
  {"image": "Bamoun.jpg", "name": "The City of Foumban - West", "description": "The Biggest City in the West", "link": "https://discover-cameroon.com/en/foumban-en/"},
  {"image": "waza.webp", "name": "Waza National Park - Far North", "description": "Home to diverse wildlife", "link": "https://en.wikipedia.org/wiki/Waza_National_Park"},
  {"image": "Douala-Airport.jpg", "name": "Douala Air Port - Littoral", "description": "The Largest Airport in Cameroon", "link": "https://en.wikipedia.org/wiki/Douala_International_Airport"},
  {"image": "ebolowa.jpg", "name": "Ebolowa - South", "description": "Capital of the Southern Region", "link": "https://www.google.com/search?sca_esv=1151ff6db26877ce&sxsrf=ACQVn09neClfB_qzXSmWjocCiI__tB0QCw:1711025326623&q=tourist+places+in+ebolowa&tbm=isch&source=lnms&sa=X&ved=2ahUKEwjqzK2GsoWFAxVORKQEHR3pA7oQ0pQJegQICxAB&biw=958&bih=909&dpr=1"},
  {"image": "edea_pont_allemand.jpg", "name": "Japoma Bridge - Littoral", "description": "Edea German Bridge", "link": "https://en.wikipedia.org/wiki/Japoma_Bridge"},
  {"image": "ekom-nkam-waterfalls.png", "name": "Ekom Nkam Waterfall - West", "description": "Source of River Wouri", "link": "https://fr.wikipedia.org/wiki/Chutes_d%27Ekom"},
  {"image": "Gorges_de_Kola_garoua.jpg", "name": "The Kola Gorges - North", "description": "An Exclusiv rocky lamdscape of over 6km", "link": "https://fr.wikipedia.org/wiki/Gorges_de_Kola"},
  {"image": "hilton.jpg", "name": "Hilton Hotel - Centre", "description": "The Best 5 star hotel in Cameroon", "link": "https://www.hilton.com/en/hotels/yaohitw-hilton-yaounde/"},
  {"image": "mount_cameroon.jpg", "name": "Mount Cameroon -South West", "description": "The highest mountain in West Africa", "link": "https://en.wikipedia.org/wiki/Mount_Cameroon"},
  {"image": "Korup_national_park.jpg", "name": "Korup National Park - South West", "description": "One of the best Diverse Ecosystems in Africa", "link": "https://national-parks.org/cameroon/korup"},
  {"image": "botanic.jpg", "name": "Limbe Botanic Garden - South West", "description": "The Garden of Cameroon", "link": "https://www.google.com/search?sca_esv=1151ff6db26877ce&sxsrf=ACQVn0-cyiRPCQX6qO1GutWnClmuAL0e9Q:1711028261033&q=limbe+botanic+garden&tbm=isch&source=lnms&sa=X&ved=2ahUKEwjV_8v9vIWFAxVpUaQEHSAvBSsQ0pQJegQIEBAB&biw=1920&bih=911&dpr=1"},
  {"image": "kribi_sea_port.jpg", "name": "Kribi Sea Port - East", "description": "The Only Deep sea port in French Cameroon", "link": "https://pak.cm/"},
  {"image": "Lac-Baleng.jpg", "name": "Lake Baleng", "description": "One of the Most Sacred Lakes in Africa", "link": "https://web.facebook.com/TourismoCameroun/posts/le-lac-baleng-est-un-lac-de-crat%C3%A8re-situ%C3%A9-dans-la-r%C3%A9gion-de-louest-cameroun-%C3%A0-qu/2772587413053683/?_rdc=1&_rdr"},
  {"image": "Mandara-Mountains-Cameroon.jpeg", "name": "Mandara Mountain", "description": "Home of Kapsiki Peak", "link": "https://en.wikipedia.org/wiki/Mandara_Mountains"},
  {"image": "menchum_fall.jpg", "name": "Menchum Fall - North West", "description": "Biggest Waterfall in North West Cameroon", "link": "https://web.facebook.com/DreamtourCamer/posts/the-menchum-falls-about-20-km-south-of-wum-and-30-km-north-of-bafut-are-impressi/1365215073859228/?_rdc=1&_rdr"},
  {"image": "ngoundere.jpeg", "name": "The city of Ngoundere - Adamawa", "description": "Capital city of Adamawa Cameroon", "link": "https://discover-cameroon.com/en/ngaoundere-en/"},
  {"image": "mount_oku_waterfall.jpg", "name": "Oku waterfall - North West", "description": "The city of God", "link": "https://www.google.com/search?sca_esv=1151ff6db26877ce&sxsrf=ACQVn09-eVaBheg6RxiSZE89FWwCPj6Lvg:1711026844362&q=mount+oku+waterfall&tbm=isch&source=univ&fir=thfVDM2_n6swDM%252CAGY5r46hxQ9zZM%252C_%253BZLNAE0zgzw6mTM%252CurmL0yLkM1Ih3M%252C_%253Bh_6hEr171HBO5M%252Cr84O7KNab4Rs_M%252C_%253BeD6Xuhgml21hzM%252CSXrSP5XJ4YDuDM%252C_%253B_p4uNMzd1uvLnM%252ChKds1P1NWMpM9M%252C_%253BNlaTTYtBT5VgzM%252Csja34MUZXBGd3M%252C_%253BNIY0wzB_LCUdHM%252CCwbuKvVAjjyfUM%252C_%253Bw-BfZkldx5kTQM%252CVLT5RV1Fhp93KM%252C_%253BK4HHXG2olokW_M%252CurmL0yLkM1Ih3M%252C_%253BYEBkTF_--TCjwM%252ClEBjyK-5_oWntM%252C_&usg=AI4_-kTblP260NqHJ-_k2Uy9QDRs5idB7w&sa=X&ved=2ahUKEwjii4nat4WFAxWuSaQEHa0aAJEQ7Al6BAhAEDk&biw=958&bih=909&dpr=1"},
  {"image": "mountain_hotel.jpg", "name": "Buea Mountain Hotel - South West", "description": "Get the best view of Mount Cameroon", "link": "https://web.facebook.com/p/Buea-Mountain-Hotel-Parliamentarian-Flats-Hotel-Group-100069162289098/?_rdc=1&_rdr"},
  {"image": "musgun_cameroon.jpg", "name": "The Mosgun People - Far North", "description": "Home to Chadic Cemroonians", "link": "https://en.wikipedia.org/wiki/Musgum_people#:~:text=The%20Musgum%20or%20Mulwi%20are,The%20Musgum%20call%20themselves%20Mulwi.&text=A%20Musgum%20home%20in%20Cameroon%20made%20of%20earth%20and%20grass."},
  {"image": "patriotic.jpg", "name": "Patriotic Monument - Centre", "description": "The centre of attraction to Patriots", "link": "https://yaounde.cm/?p=2229"},
  {"image": "ron_point.jpg", "name": "The New Freedom - Littoral", "description": "Douala's Emblem", "link": "https://en.wikipedia.org/wiki/La_Nouvelle_Libert%C3%A9"},
  {"image": "seme.png", "name": "Seme beach Limbe - South West", "description": "Home to diverse wildlife", "link": "https://web.facebook.com/HotelSemeBeach/?_rdc=1&_rdr"},
  {"image": "ub.jpg", "name": "University Of Buea - South West", "description": "The place to be", "link": "https://en.wikipedia.org/wiki/University_of_Buea"},
  {"image": "wildlife_centre.jpeg", "name": "Limbe Wildlife Centre - South West", "description": "Home to diverse wildlife", "link": "https://fr.wikipedia.org/wiki/Limbe_Wildlife_Centre"},
  {"image": "Yaounde.png", "name": "Yaounde - Centre", "description": "Capital City", "link": "https://en.wikipedia.org/wiki/Yaound%C3%A9"},
  {"image": "wouri.jpeg", "name": "River Wouri - Littoral", "description": "River of Prounds", "link": "https://en.wikipedia.org/wiki/Wouri_River"},
  {"image": "sanaga.jpeg", "name": "River Sanaga - East", "description": "Cameroon's Longest River", "link": "https://fr.wikipedia.org/wiki/Limbe_Wildlife_Centre"},
  {"image": "debun.jpg", "name": "Debundscha - South West", "description": "Wettest place in Africa", "link": "https://en.wikipedia.org/wiki/Debundscha"},
]

insert_query = """
INSERT INTO places (image, name, description, link)
VALUES (%s, %s, %s, %s)
"""

try:
  for place in places:
    cursor.execute(insert_query, (place["image"], place["name"], place["description"], place["link"]))
  connection.commit()
  print("All places added successfully!")
except mysql.connector.Error as err:
  print(f"Error adding places: {err}")
  connection.rollback()

cursor.close()
connection.close()