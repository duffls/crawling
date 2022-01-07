# crummy.com/software/BeautifulSoup
# pip install BeautifulSoup4

from bs4 import BeautifulSoup

#
# xml_doc = """
# <res>
#     <channel>
#         <my>
#             <song album="a1">
#                 <title>song1</title>
#                 <length>3:50</length>
#             </song>
#             <song album="a2">
#                 <title>song2</title>
#                 <length>4:50</length>
#             </song>
#             <song album="a3">
#                 <title>song3</title>
#                 <length>4:37</length>
#             </song>
#         </my>
#     </channel>
# </res>
# """
#
# soup = BeautifulSoup(xml_doc, "html.parser")
#
# #for song in soup.find_all("song"):
# for song in soup.findAll("song"):
#     #print(song)
#     print(song["album"])
#     print(song.title.string)
#     print(song.length.string)
#     print()
#
# print(soup.prettify())

with open("song.xml", "r") as f:
    soup = BeautifulSoup(f, "html.parser")
# fp = open("song.xml", "r")
# soup = BeautifulSoup(fp, "html.parser")

print(soup)
print("="*60)

for song in soup.find_all("song"):
    print(song["album"])
    print(song.title.string)
    print(song.length.string)
    print("-"*60)

