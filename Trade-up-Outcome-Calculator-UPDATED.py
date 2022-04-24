#Code might be broken as I didnt get the total number of skins for each profitable trade up with 10 skins
#Removing restrictions on trading up with wears of the same or one lower level would increase number of tradeups
#Cost not correct when using realistic float values

import warnings
warnings.simplefilter(action='ignore')
import requests
from bs4 import BeautifulSoup
import json 
import csv
import pandas as pd
import re
import numpy as np
import multiprocessing
import pprint

APPID = '730'
APIKEY = 'fo4y3EJCuaYLE4dz26GB1K7c328' #steamapis.com API key(this will expire soon)

item = requests.get('http://api.steamapis.com/market/items/'+APPID+'?api_key='+APIKEY)
item = item.content
item = json.loads(item)
#pprint.pprint(item)
item_data = item['data']


#Will create dictionary with all CSGO items name and price
item_name_list = []
safe_price_list = [] #Using safe price instead of latest price to hopefully get a more accurate answer
for item in item_data: 
    item_name_list.append(item['market_hash_name']) 
    safe_price_list.append(item['prices']['safe']) #Change between 'latest' or 'safe' for different prices
item_price_data = {'itemName':item_name_list, 'price':safe_price_list}
steam_api_data = pd.DataFrame(item_price_data)
steam_api_data.to_csv("Steam API Data.csv")

# Geting float, rarity and collection information for all skins
# All knife skins are excluded
#list_to_iterate_through = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1251, 1252, 1253, 1254, 1255, 1256, 1257, 1258, 1259, 1260, 1261, 1262, 1263, 1264, 1265, 1266, 1267]

name_list = []
min_float_list = []
max_float_list = []
rarity_list = []
collection_list = []
for i in range(1360): #list_to_iterate_through: #Range will need to be extended as more skins are released. Max currently 1268
    try:
        #Requesting the page for the numbers as per CSGO Stash website design
        r = requests.get('https://csgostash.com/skin/' + str(i))
        soup = BeautifulSoup(r.text, "html.parser")
        tags = soup.find_all("div", "marker-value cursor-default")
        
        #Using regex to extract the name
        name = soup.find("title")
        name = str(name)
        if "Knife" in name:
            continue
        if name == '<title>Not Found</title>':
            continue
        name = name[7:len(name) - 22]
        if 'Dragon King' in name: #Adjusts for the fact that this skin has an opening bracket in the name (am looking for an opening bracket to remove the wear levels so it was prematurely cutting off the skin name)
            name = name[:9]
        name_list.append(name)

        #Using regex to extract the collection
        collection = soup.find("p", "collection-text-label")
        collection = str(collection)
        collection = re.sub('^.+?>', "", collection)
        collection = re.sub('<.+$', "", collection)
        collection_list.append(collection)

        #Using regex to extract the rarity 
        rarity = soup.find("p", "nomargin")
        rarity = str(rarity)
        rarity = re.sub('^.+?>', "", rarity)
        rarity = re.sub('\s.+>', "", rarity)
        rarity = rarity.split()[0] #Removes words past the rarity
        rarity_list.append(rarity)

        #Using regex to get the min and max float 
        min = str(tags[0])
        max = str(tags[1])
        min = re.sub('^.+?>', '', min)
        max = re.sub('^.+?>', '', max)
        min = re.sub('<.+?>', '', min)
        max = re.sub('<.+?>', '', max)
        min_float_list.append(min)
        max_float_list.append(max)
    except:
        continue

#Creating data frame
float_data = {'name': name_list, 'Min Float': min_float_list, 'Max Float': max_float_list, 'Rarity': rarity_list, 'Collection': collection_list}
float_data = pd.DataFrame(float_data)
float_data = float_data[float_data.Collection != 'None'] #Removing the row for M4A4 Howl for simplicity
float_data = float_data[float_data.Collection != 'The Rising Sun Collection'] #Removing the rows from rising sun collection because of problem with the sunset storm skin name not working

float_data.to_csv("float_data.csv", index=False)

float_data = pd.read_csv("float_data.csv", index_col=False)

#Defines the assumed float as a variable so it can be easily changed later
factory_new_assumed_float = 0.03        #0.00-0.07
minimal_wear_assumed_float = 0.10       #0.07-0.15
field_tested_assumed_float = 0.2       #0.15-0.37
well_worn_assumed_float = 0.39          #0.37-0.44
battle_scarred_assumed_float = 0.6      #0.44-1.0

def label_float(row): #Adds an assumed value for the float. For skins when assumed float is outside the range of the skin, a placeholder value of X is used
    min_possible_float = float(row['Min Float'])
    max_possible_float = float(row['Max Float'])
    if row['wear'] == 1:
        if factory_new_assumed_float < min_possible_float or factory_new_assumed_float > max_possible_float:
            return (max_possible_float - ((max_possible_float - min_possible_float) * 0.1))
        else:
            return factory_new_assumed_float
    if row['wear'] == 2:
        if minimal_wear_assumed_float < min_possible_float or minimal_wear_assumed_float > max_possible_float:
            return (max_possible_float - ((max_possible_float - min_possible_float) * 0.1))
        else:
            return minimal_wear_assumed_float
    if row['wear'] == 3:
        if field_tested_assumed_float < min_possible_float or field_tested_assumed_float > max_possible_float:
            return (max_possible_float - ((max_possible_float - min_possible_float) * 0.1))
        else:
            return field_tested_assumed_float
    if row['wear'] == 4:
        if well_worn_assumed_float < min_possible_float or factory_new_assumed_float > max_possible_float:
            return (max_possible_float - ((max_possible_float - min_possible_float) * 0.1))
        else:
            return well_worn_assumed_float
    if row['wear'] == 5:
        if battle_scarred_assumed_float < min_possible_float or battle_scarred_assumed_float > max_possible_float:
            return (max_possible_float - ((max_possible_float - min_possible_float) * 0.1))
        else:
            return battle_scarred_assumed_float

def label_min_wear(row): 
    if row['wear'] == 1:
        return 0
    if row['wear'] == 2:
        return 0.07
    if row['wear'] == 3:
        return 0.15
    if row['wear'] == 4:
        return 0.37
    if row['wear'] == 5:
        return 0.44

def label_max_wear(row): 
    if row['wear'] == 1:
        return 0.07
    if row['wear'] == 2:
        return 0.15
    if row['wear'] == 3:
        return 0.37
    if row['wear'] == 4:
        return 0.44
    if row['wear'] == 5:
        return 1

def label_statrak(row):
    name = str(row['name'])
    return "StatTrak™ " + name

#Initialising the data to be used in the normal tradeups
steam_api_data['shortenedName'] = steam_api_data.itemName.str.split(" \(", expand = True)[0] #Creating a new column based on a string split of name column
steam_api_data['wear'] = steam_api_data.itemName.str.split(" \(", expand = True)[1] 
steam_api_data['wear'] = steam_api_data['wear'].map(lambda x: str(x)[:-1]) #Adds new column for wear and removes the closing bracket

steam_api_data.insert(0, 'name', steam_api_data.pop('shortenedName')) #Makes the shortened name the first column
steam_api_data.drop('itemName', axis=1, inplace=True)

all_data = steam_api_data.merge(float_data, on='name') #Merging the dataframes
all_data.drop(all_data.loc[all_data['Collection']=='The Rising Sun Collection'].index, inplace=True) #Removes rising sun collection as the sunset storm skin names were broken

all_data.loc[all_data.wear == "Battle-Scarred", "wear"] = 5 #Changing wear names to numbers as it makes it easier to index out all relevant skins later
all_data.loc[all_data.wear == "Well-Worn", "wear"] = 4
all_data.loc[all_data.wear == "Field-Tested", "wear"] = 3
all_data.loc[all_data.wear == "Minimal Wear", "wear"] = 2
all_data.loc[all_data.wear == "Factory New", "wear"] = 1

all_data.loc[all_data.Rarity == "Consumer", "Rarity"] = 6 #Changing wear names to numbers as it makes it easier to index out all relevant skins later
all_data.loc[all_data.Rarity == "Industrial", "Rarity"] = 5
all_data.loc[all_data.Rarity == "Mil-Spec", "Rarity"] = 4
all_data.loc[all_data.Rarity == "Restricted", "Rarity"] = 3
all_data.loc[all_data.Rarity == "Classified", "Rarity"] = 2
all_data.loc[all_data.Rarity == "Covert", "Rarity"] = 1

all_data['assumedFloat'] = all_data.apply(lambda row: label_float(row), axis=1)
all_data['minForWear'] = all_data.apply(lambda row: label_min_wear(row), axis=1)
all_data['maxForWear'] = all_data.apply(lambda row: label_max_wear(row), axis=1)

#Initialising the data to be used in the stattrak tradeups. This data is hardcoded and so will need to be adjusted when new skins come out
stattrak_data = pd.read_csv("Stattrak item names.csv")
stattrak_data['shortenedName'] = stattrak_data.Name.str.split(" \(", expand = True)[0] #Creating a new column based on a string split of name column
stattrak_data['wear'] = stattrak_data.Name.str.split(" \(", expand = True)[1] 
stattrak_data['wear'] = stattrak_data['wear'].map(lambda x: str(x)[:-1]) #Adds new column for wear and removes the closing bracket
stattrak_data.insert(0, 'name', stattrak_data.pop('shortenedName')) #Makes the shortened name the first column
del stattrak_data['Name'] #Deleting the extra column
stattrak_data = stattrak_data.merge(float_data, on='name') #Merging the dataframes
stattrak_data.drop(stattrak_data.loc[stattrak_data['Collection']=='The Rising Sun Collection'].index, inplace=True) #Removes rising sun collection as the sunset storm skin names were broken
stattrak_data['name'] = stattrak_data.apply(lambda row: label_statrak(row), axis=1) #Adding the word statrak to all weapon names
stattrak_data = stattrak_data.merge(steam_api_data, on=['name', 'wear']) #Steam api was returning duplicated data meaning there were multiple instances of the same skin in output

stattrak_data.loc[stattrak_data.wear == "Battle-Scarred", "wear"] = 5
stattrak_data.loc[stattrak_data.wear == "Well-Worn", "wear"] = 4
stattrak_data.loc[stattrak_data.wear == "Field-Tested", "wear"] = 3
stattrak_data.loc[stattrak_data.wear == "Minimal Wear", "wear"] = 2
stattrak_data.loc[stattrak_data.wear == "Factory New", "wear"] = 1

stattrak_data.loc[stattrak_data.Rarity == "Consumer", "Rarity"] = 6 
stattrak_data.loc[stattrak_data.Rarity == "Industrial", "Rarity"] = 5
stattrak_data.loc[stattrak_data.Rarity == "Mil-Spec", "Rarity"] = 4
stattrak_data.loc[stattrak_data.Rarity == "Restricted", "Rarity"] = 3
stattrak_data.loc[stattrak_data.Rarity == "Classified", "Rarity"] = 2
stattrak_data.loc[stattrak_data.Rarity == "Covert", "Rarity"] = 1

stattrak_data['assumedFloat'] = stattrak_data.apply(lambda row: label_float(row), axis=1)
stattrak_data['minForWear'] = stattrak_data.apply(lambda row: label_min_wear(row), axis=1)
stattrak_data['maxForWear'] = stattrak_data.apply(lambda row: label_max_wear(row), axis=1)

def trade_ups_without_10_of_same_skin():
    profitable_trade_ups = pd.DataFrame()
    guaranteed_profit_tradeups = pd.DataFrame()
    for y in range(len(all_data)):
        print(y)
        item = all_data.iloc[y]
        rarity = item[5]
        if rarity == 1: #Ignores items that are covert as there are no possible tradeups
            continue
        name, safe_price, wear, min_float, max_float, collection, assumed_float = item[0], item[1], item[2], item[3], item[4], item[6], item[7]
        if wear == 5:
            plausible_items = all_data.loc[(all_data['Rarity'] == rarity) & ((all_data['wear'] == wear) | (all_data['wear'] == wear - 1))] #Brackets are necessary around conditions. Can remove wear restrictions for more trade up options. Could continue at wears 4 and 5 because analytics show there are not many wel-worn and battle scarred trade ups
        if wear == 4:
            plausible_items = all_data.loc[(all_data['Rarity'] == rarity) & ((all_data['wear'] == wear) | (all_data['wear'] == wear - 1))] 
        if wear == 3:
            plausible_items = all_data.loc[(all_data['Rarity'] == rarity) & ((all_data['wear'] == wear) | (all_data['wear'] == wear - 1))] 
        if wear == 2:
            plausible_items = all_data.loc[(all_data['Rarity'] == rarity) & ((all_data['wear'] == wear) | (all_data['wear'] == wear - 1))] 
        if wear == 1:
            plausible_items = all_data.loc[(all_data['Rarity'] == rarity) & (all_data['wear'] == wear)] #If ith skin is factory new, only factory new skins will be considered
        try: #Put everything into a try so if there is an error, it will move onto the next second skin
            for i in range(len(plausible_items)):
                second_item = plausible_items.iloc[i]
                second_name, second_safe_price, second_wear, second_min_float, second_max_float, second_rarity, second_collection, second_assumed_float = second_item[0], second_item[1], second_item[2], second_item[3], second_item[4], second_item[5], second_item[6], second_item[7]
                for num_first_skin in range(6,10): #Performing the 5 variations of the trade up with i times the first item and 10-i times the second item. Does not calculate for 10 because a seperate function does that
                    total_cost = num_first_skin*safe_price + (10-num_first_skin)*second_safe_price
                    average_float = (num_first_skin*float(assumed_float) + (10-num_first_skin)*float(second_assumed_float)) / 10
                    trade_up_possibilities = all_data.loc[(all_data['Rarity'] == rarity - 1) & ((all_data['Collection'] == collection) | (all_data['Collection'] == second_collection))] #Extracts all the skins from the same collection as the inputs
                    unique_skins = trade_up_possibilities.drop_duplicates('name') #Dataframe from which relevant min and max float values can be extracted
                    unique_skins['outputFloat'] = average_float * (pd.to_numeric(unique_skins['Max Float'], downcast="float") - pd.to_numeric(unique_skins['Min Float'], downcast="float")) + pd.to_numeric(unique_skins['Min Float'], downcast="float") #Formula for output float of trade-up
                    trade_up_possibilities = pd.merge(trade_up_possibilities, unique_skins, on=['name', 'Min Float', 'Max Float', 'Collection', 'Rarity'], how='left')
                    trade_up_possibilities.drop(columns = ['price_y', 'wear_y', 'assumedFloat_y', 'minForWear_y', 'maxForWear_y'], inplace=True) #Removing excess columns added in merge
                    
                    #Create a dataframe here and add to it as you find the right values
                    outputs_df = pd.DataFrame()
                    for x in range(len(unique_skins)):
                        itemx = unique_skins.iloc[x]
                        namex = itemx[0]
                        outputFloat = float(itemx[-1]) #Hardcoded where to look for output float will not work if the dataframe changes
                        temp = trade_up_possibilities.loc[trade_up_possibilities['name'] == namex]
                        row = temp.loc[((pd.to_numeric(temp['minForWear_x'], downcast="float") < outputFloat) & (pd.to_numeric(temp['maxForWear_x'], downcast="float") > outputFloat))]
                        outputs_df = outputs_df.append(row)
                        
                    #Calculating and adding probabilities to the output df
                    if collection == second_collection or num_first_skin == 10:
                        skin_probability = float(1/sum(unique_skins['Collection'] == collection))
                        outputs_df['probability'] = np.where(outputs_df['Collection'] == collection, skin_probability, 0)
                    else:
                        num_first_collection = sum(outputs_df['Collection'] == collection)
                        num_second_collection = sum(outputs_df['Collection'] == second_collection)
                        num_total_skins = num_first_skin*num_first_collection + (10-num_first_skin)*num_second_collection
                        probability_collection = float(num_first_collection*num_first_skin/num_total_skins)
                        probability_second_collection = float(num_second_collection*(10-num_first_skin)/num_total_skins)
                        skin_probability_collection = probability_collection / num_first_collection
                        skin_probability_second_collection = probability_second_collection / num_second_collection #Breaks when there is a collection with no covert skin e.g. 2018 Nuke Collection
                        outputs_df['probability'] = np.where(outputs_df['Collection'] == collection, skin_probability_collection, skin_probability_second_collection)  

                    EV = sum(outputs_df['probability'] * outputs_df['price_x'])
                    EV_less_steam_fee = round(EV*0.87, 2) #Assumes fee of 13% regardless of selling price
                    outputs_df['totalCost'] = total_cost
                    outputs_df['EV'] = EV_less_steam_fee
                    if EV_less_steam_fee > total_cost:
                        outputs_df['input1'] = name
                        outputs_df['input1Num'] = num_first_skin
                        outputs_df['input1Float'] = assumed_float
                        outputs_df['input2'] = second_name
                        outputs_df['input2Num'] = (10- num_first_skin)
                        outputs_df['input2Float'] = second_assumed_float
                        percentage_return = round((EV_less_steam_fee - total_cost) / total_cost * 100, 1)
                        outputs_df['percentageReturn'] = percentage_return
                        del outputs_df['assumedFloat_x']
                        outputs_df['minDifference'] = min(outputs_df['maxForWear_x'] - outputs_df['outputFloat'])
                        profitable_trade_ups = profitable_trade_ups.append(outputs_df)
                        profitable_trade_ups = profitable_trade_ups.append(pd.Series(), ignore_index=True)
                        all_profitable = True
                        min_difference = 1
                        for skin in range(len(unique_skins)):
                            if outputs_df.iloc['ouputFloat'] < min_difference:
                                min_difference = outputs_df.iloc['ouputFloat']
                            if not (outputs_df.iloc[skin, 1] * 0.87 > outputs_df.iloc[skin, 12]):
                                all_profitable = False
                        outputs_df['minDifference'] = min_difference
                        if all_profitable == True:
                            guaranteed_profit_tradeups = guaranteed_profit_tradeups.append(outputs_df)
                            guaranteed_profit_tradeups = guaranteed_profit_tradeups.append(pd.Series(), ignore_index=True)
        except:
            continue
    profitable_trade_ups.to_csv('Profitable Trade Ups Without 10 of Same Skin.csv')
    guaranteed_profit_tradeups.to_csv('Guaranteed profit trade ups without 10 of same skin.csv')

def trade_ups_with_10_of_same_skin():
    profitable_trade_ups_10_of_same_skin = pd.DataFrame()
    guaranteed_profit_tradeups = pd.DataFrame()
    num_first_skin = 10 #This function will find tradeups with just one input skin, the function above will calculate tradeups for combinations of skins
    for y in range(len(all_data)):
        #print("Trade ups with 10 of same skin: " + str(y))
        item = all_data.iloc[y]
        rarity = item[5]
        if rarity == 1: #Ignores items that are covert as there are no possible tradeups
            continue
        name, safe_price, wear, min_float, max_float, collection, assumed_float = item[0], item[1], item[2], item[3], item[4], item[6], item[7]
        try: #Put everything into a try so if there is an error, it will move onto the next second skin
            total_cost = num_first_skin*safe_price
            average_float = (num_first_skin*float(assumed_float)) / 10
            trade_up_possibilities = all_data.loc[(all_data['Rarity'] == rarity - 1) & (all_data['Collection'] == collection)] #Extracts all the skins from the same collection as the inputs
            unique_skins = trade_up_possibilities.drop_duplicates('name') #Dataframe from which relevant min and max float values can be extracted
            unique_skins['outputFloat'] = average_float * (pd.to_numeric(unique_skins['Max Float'], downcast="float") - pd.to_numeric(unique_skins['Min Float'], downcast="float")) + pd.to_numeric(unique_skins['Min Float'], downcast="float") #Formula for output float of trade-up
            trade_up_possibilities = pd.merge(trade_up_possibilities, unique_skins, on=['name', 'Min Float', 'Max Float', 'Collection', 'Rarity'], how='left')
            trade_up_possibilities.drop(columns = ['price_y', 'wear_y', 'assumedFloat_y', 'minForWear_y', 'maxForWear_y'], inplace=True) #Removing excess columns added in merge
            #Create a dataframe here and add to it as you find the right values
            outputs_df = pd.DataFrame()
            for x in range(len(unique_skins)):
                itemx = unique_skins.iloc[x]
                namex = itemx[0]
                outputFloat = float(itemx[-1]) #Hardcoded where to look for output float will not work if the dataframe changes
                temp = trade_up_possibilities.loc[trade_up_possibilities['name'] == namex]
                row = temp.loc[((pd.to_numeric(temp['minForWear_x'], downcast="float") < outputFloat) & (pd.to_numeric(temp['maxForWear_x'], downcast="float") > outputFloat))]
                outputs_df = outputs_df.append(row)
                
            #Calculating and adding probabilities to the output df. More complex code not needed because we have 10 of the same skin
            skin_probability = float(1/sum(unique_skins['Collection'] == collection))
            outputs_df['probability'] = np.where(outputs_df['Collection'] == collection, skin_probability, 0)

            EV = sum(outputs_df['probability'] * outputs_df['price_x'])
            EV_less_steam_fee = round(EV*0.87, 2) #Assumes fee of 13% regardless of selling price
            outputs_df['totalCost'] = total_cost
            outputs_df['EV'] = EV_less_steam_fee
            if EV_less_steam_fee > total_cost:
                outputs_df['input'] = name
                outputs_df['inputNum'] = num_first_skin
                outputs_df['inputFloat'] = assumed_float
                percentage_return = round(((EV_less_steam_fee - total_cost) / total_cost) * 100, 1)
                outputs_df['percentageReturn'] = percentage_return
                del outputs_df['assumedFloat_x']
                outputs_df['minDifference'] = min(outputs_df['maxForWear_x'] - outputs_df['outputFloat'])
                profitable_trade_ups_10_of_same_skin = profitable_trade_ups_10_of_same_skin.append(outputs_df)
                profitable_trade_ups_10_of_same_skin = profitable_trade_ups_10_of_same_skin.append(pd.Series(), ignore_index=True) #Adds a blank line for formatting
                all_profitable = True
                for skin in range(len(unique_skins)):
                    if not (outputs_df.iloc[skin, 1] * 0.87 > outputs_df.iloc[skin, 11]):
                        all_profitable = False
                if all_profitable == True:
                    guaranteed_profit_tradeups = guaranteed_profit_tradeups.append(outputs_df)
                    guaranteed_profit_tradeups = guaranteed_profit_tradeups.append(pd.Series(), ignore_index=True)
        except:
            continue
    profitable_trade_ups_10_of_same_skin.to_csv('Profitable Trade Ups 10 of Same Skin.csv')
    guaranteed_profit_tradeups.to_csv('Guaranteed profit tradeups 10 of same item.csv')

def statrak_trade_ups_with_10_of_same_skin():
    profitable_trade_ups_10_of_same_skin = pd.DataFrame()
    guaranteed_profit_tradeups = pd.DataFrame()
    num_first_skin = 10 #This function will find tradeups with just one input skin, the function above will calculate tradeups for combinations of skins
    for y in range(len(stattrak_data)):
        #print("Trade ups with 10 of same skin: " + str(y))
        item = stattrak_data.iloc[y]
        rarity = item[4]
        if rarity == 1: #Ignores items that are covert as there are no possible tradeups
            continue
        name, safe_price, wear, min_float, max_float, collection, assumed_float = item[0], item[6], item[1], item[8], item[9], item[5], item[7]
        try: #Put everything into a try so if there is an error, it will move onto the next second skin
            total_cost = num_first_skin*safe_price
            average_float = (num_first_skin*float(assumed_float)) / 10
            trade_up_possibilities = stattrak_data.loc[(stattrak_data['Rarity'] == rarity - 1) & (stattrak_data['Collection'] == collection)] #Extracts all the skins from the same collection as the inputs
            unique_skins = trade_up_possibilities.drop_duplicates('name') #Dataframe from which relevant min and max float values can be extracted
            unique_skins['outputFloat'] = average_float * (pd.to_numeric(unique_skins['Max Float'], downcast="float") - pd.to_numeric(unique_skins['Min Float'], downcast="float")) + pd.to_numeric(unique_skins['Min Float'], downcast="float") #Formula for output float of trade-up
            trade_up_possibilities = pd.merge(trade_up_possibilities, unique_skins, on=['name', 'Min Float', 'Max Float', 'Collection', 'Rarity'], how='left')
            trade_up_possibilities.drop(columns = ['price_y', 'wear_y', 'assumedFloat_y', 'minForWear_y', 'maxForWear_y'], inplace=True) #Removing excess columns added in merge
            
            #Create a dataframe here and add to it as you find the right values
            outputs_df = pd.DataFrame()
            for x in range(len(unique_skins)):
                itemx = unique_skins.iloc[x]
                namex = itemx[0]
                outputFloat = float(itemx[-1]) #Hardcoded where to look for output float will not work if the dataframe changes
                temp = trade_up_possibilities.loc[trade_up_possibilities['name'] == namex]
                row = temp.loc[((pd.to_numeric(temp['minForWear_x'], downcast="float") < outputFloat) & (pd.to_numeric(temp['maxForWear_x'], downcast="float") > outputFloat))]
                outputs_df = outputs_df.append(row)
                
            #Calculating and adding probabilities to the output df. More complex code not needed because we have 10 of the same skin
            skin_probability = float(1/sum(unique_skins['Collection'] == collection))
            outputs_df['probability'] = np.where(outputs_df['Collection'] == collection, skin_probability, 0)

            EV = sum(outputs_df['probability'] * outputs_df['price_x'])
            EV_less_steam_fee = round(EV*0.87, 2) #Assumes fee of 13% regardless of selling price
            outputs_df['totalCost'] = total_cost
            outputs_df['EV'] = EV_less_steam_fee
            if EV_less_steam_fee > total_cost:
                outputs_df['input'] = name
                outputs_df['inputNum'] = num_first_skin
                outputs_df['inputFloat'] = assumed_float
                percentage_return = round(((EV_less_steam_fee - total_cost) / total_cost) * 100, 1)
                outputs_df['percentageReturn'] = percentage_return
                del outputs_df['assumedFloat_x']
                outputs_df['minDifference'] = min(outputs_df['maxForWear_x'] - outputs_df['outputFloat'])
                profitable_trade_ups_10_of_same_skin = profitable_trade_ups_10_of_same_skin.append(outputs_df)
                profitable_trade_ups_10_of_same_skin = profitable_trade_ups_10_of_same_skin.append(pd.Series(), ignore_index=True) #Adds a blank line for formatting
                all_profitable = True
                for skin in range(len(unique_skins)):
                    if not (outputs_df.iloc[skin, 6] * 0.87 > outputs_df.iloc[skin, 11]):
                        all_profitable = False
                if all_profitable == True:
                    guaranteed_profit_tradeups = guaranteed_profit_tradeups.append(outputs_df)
                    guaranteed_profit_tradeups = guaranteed_profit_tradeups.append(pd.Series(), ignore_index=True)
        except:
            continue
    profitable_trade_ups_10_of_same_skin.to_csv('Statrak Profitable Trade Ups 10 of Same Skin.csv')
    guaranteed_profit_tradeups.to_csv('Statrak guaranteed profit tradeups 10 of same item.csv')

def stattrak_trade_ups_without_10_of_same_skin():
    profitable_trade_ups = pd.DataFrame()
    guaranteed_profit_tradeups = pd.DataFrame()
    for y in range(len(stattrak_data)):
        print(y)
        item = stattrak_data.iloc[y]
        rarity = item[4]
        if rarity == 1: #Ignores items that are covert as there are no possible tradeups
            continue
        name, safe_price, wear, min_float, max_float, collection, assumed_float = item[0], item[6], item[1], item[2], item[3], item[5], item[7]
        if wear == 5:
            plausible_items = stattrak_data.loc[(stattrak_data['Rarity'] == rarity) & ((stattrak_data['wear'] == wear) | (stattrak_data['wear'] == wear - 1))] #Brackets are necessary around conditions. Can remove wear restrictions for more trade up options
        if wear == 4:
            plausible_items = stattrak_data.loc[(stattrak_data['Rarity'] == rarity) & ((stattrak_data['wear'] == wear) | (stattrak_data['wear'] == wear - 1))] 
        if wear == 3:
            plausible_items = stattrak_data.loc[(stattrak_data['Rarity'] == rarity) & ((stattrak_data['wear'] == wear) | (stattrak_data['wear'] == wear - 1))] 
        if wear == 2:
            plausible_items = stattrak_data.loc[(stattrak_data['Rarity'] == rarity) & ((stattrak_data['wear'] == wear) | (stattrak_data['wear'] == wear - 1))] 
        if wear == 1:
            plausible_items = stattrak_data.loc[(stattrak_data['Rarity'] == rarity) & (stattrak_data['wear'] == wear)] #If ith skin is factory new, only factory new skins will be considered
        try: #Put everything into a try so if there is an error, it will move onto the next second skin
            for i in range(5):#len(plausible_items)):
                second_item = plausible_items.iloc[i]
                second_name, second_safe_price, second_wear, second_min_float, second_max_float, second_collection, second_assumed_float = second_item[0], second_item[6], second_item[1], second_item[2], second_item[3], second_item[5], second_item[7]
                for num_first_skin in range(6,10): #Performing the 5 variations of the trade up with i times the first item and 10-i times the second item. Does not calculate for 10 because a seperate function does that
                    total_cost = num_first_skin*safe_price + (10-num_first_skin)*second_safe_price
                    average_float = (num_first_skin*float(assumed_float) + (10-num_first_skin)*float(second_assumed_float)) / 10
                    trade_up_possibilities = stattrak_data.loc[(stattrak_data['Rarity'] == rarity - 1) & ((stattrak_data['Collection'] == collection) | (stattrak_data['Collection'] == second_collection))] #Extracts all the skins from the same collection as the inputs
                    unique_skins = trade_up_possibilities.drop_duplicates('name') #Dataframe from which relevant min and max float values can be extracted
                    unique_skins['outputFloat'] = average_float * (pd.to_numeric(unique_skins['Max Float'], downcast="float") - pd.to_numeric(unique_skins['Min Float'], downcast="float")) + pd.to_numeric(unique_skins['Min Float'], downcast="float") #Formula for output float of trade-up
                    trade_up_possibilities = pd.merge(trade_up_possibilities, unique_skins, on=['name', 'Min Float', 'Max Float', 'Collection', 'Rarity'], how='left')
                    trade_up_possibilities.drop(columns = ['price_y', 'wear_y', 'assumedFloat_y', 'minForWear_y', 'maxForWear_y'], inplace=True) #Removing excess columns added in merge
                    
                    #Create a dataframe here and add to it as you find the right values
                    outputs_df = pd.DataFrame()
                    for x in range(len(unique_skins)):
                        itemx = unique_skins.iloc[x]
                        namex = itemx[0]
                        outputFloat = float(itemx[-1]) #Hardcoded where to look for output float will not work if the dataframe changes
                        temp = trade_up_possibilities.loc[trade_up_possibilities['name'] == namex]
                        row = temp.loc[((pd.to_numeric(temp['minForWear_x'], downcast="float") < outputFloat) & (pd.to_numeric(temp['maxForWear_x'], downcast="float") > outputFloat))]
                        outputs_df = outputs_df.append(row)
                        
                    #Calculating and adding probabilities to the output df
                    if collection == second_collection or num_first_skin == 10:
                        skin_probability = float(1/sum(unique_skins['Collection'] == collection))
                        outputs_df['probability'] = np.where(outputs_df['Collection'] == collection, skin_probability, 0)
                    else:
                        num_first_collection = sum(outputs_df['Collection'] == collection)
                        num_second_collection = sum(outputs_df['Collection'] == second_collection)
                        num_total_skins = num_first_skin*num_first_collection + (10-num_first_skin)*num_second_collection
                        probability_collection = float(num_first_collection*num_first_skin/num_total_skins)
                        probability_second_collection = float(num_second_collection*(10-num_first_skin)/num_total_skins)
                        skin_probability_collection = probability_collection / num_first_collection
                        skin_probability_second_collection = probability_second_collection / num_second_collection #Breaks when there is a collection with no covert skin e.g. 2018 Nuke Collection
                        outputs_df['probability'] = np.where(outputs_df['Collection'] == collection, skin_probability_collection, skin_probability_second_collection)  

                    EV = sum(outputs_df['probability'] * outputs_df['price_x'])
                    EV_less_steam_fee = round(EV*0.87, 2) #Assumes fee of 13% regardless of selling price
                    outputs_df['totalCost'] = total_cost
                    outputs_df['EV'] = EV_less_steam_fee
                    if EV_less_steam_fee > total_cost:
                        outputs_df['input1'] = name
                        outputs_df['input1Num'] = num_first_skin
                        outputs_df['input1Float'] = assumed_float
                        outputs_df['input2'] = second_name
                        outputs_df['input2Num'] = (10- num_first_skin)
                        outputs_df['input2Float'] = second_assumed_float
                        percentage_return = round((EV_less_steam_fee - total_cost) / total_cost * 100, 1)
                        outputs_df['percentageReturn'] = percentage_return
                        del outputs_df['assumedFloat_x']
                        outputs_df['minDifference'] = min(outputs_df['maxForWear_x'] - outputs_df['outputFloat'])
                        profitable_trade_ups = profitable_trade_ups.append(outputs_df)
                        profitable_trade_ups = profitable_trade_ups.append(pd.Series(), ignore_index=True)
                        all_profitable = True
                        for skin in range(len(unique_skins)):
                            if not (outputs_df.iloc[skin, 6] * 0.87> outputs_df.iloc[skin, 12]):
                                all_profitable = False
                        if all_profitable == True:
                            guaranteed_profit_tradeups = guaranteed_profit_tradeups.append(outputs_df)
                            guaranteed_profit_tradeups = guaranteed_profit_tradeups.append(pd.Series(), ignore_index=True)
        except:
            continue

    profitable_trade_ups.to_csv('Profitable Trade Ups Without 10 of Same Skin.csv')
    guaranteed_profit_tradeups.to_csv('Statrak guaranteed profit tradeups without 10 of same item.csv')


#Sets up each of the functions to work on one core
# if __name__ == '__main__':
#     p1 = multiprocessing.Process(target=trade_ups_with_10_of_same_skin)
#     p2 = multiprocessing.Process(target=statrak_trade_ups_with_10_of_same_skin)
#     # p3 = multiprocessing.Process(target=trade_ups_without_10_of_same_skin)
#     # p4 = multiprocessing.Process(target=stattrak_trade_ups_without_10_of_same_skin)

#     p1.start()
#     p2.start()
#     # p3.start()
#     # p4.start()

#     p1.join()
#     p2.join()
#     # p3.join()
#     # p4.join()

#trade_ups_without_10_of_same_skin() 
#trade_ups_with_10_of_same_skin() 
statrak_trade_ups_with_10_of_same_skin() 
#stattrak_trade_ups_without_10_of_same_skin() 



