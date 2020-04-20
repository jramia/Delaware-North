os.chdir('C:\\Users\\JRAMIA\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages')
from pybaseball import schedule_and_record
from datetime import datetime
import openpyxl

years = ["2015", "2016", "2017", "2018"]
teams = ["ATL", "BAL", "CHW", "CIN", "CLE", "DET", "MIL", "MIN", "SDP", "STL", "TEX"]
data = pd.DataFrame()

for team in teams:
    for year in years:
        d = schedule_and_record(year, team)
        d['Year'] = year
        data = data.append(d, ignore_index=True)

data["DblHdrGm"] = ""
for i in range(0,len(data)):
    mystring = data.iloc[i,0]
    start = mystring.find('(')
    if start != -1:
        data.iloc[i,-1] = mystring[start+1]
        data.iloc[i,0] = mystring[:-4]
        
data["DblHdr"] = ""
for i in range(0,len(data)):
    if data.iloc[i,-2] == "":
        data.iloc[i,-1] = 0
    else:
        data.iloc[i,-1] = 1
        
data["Date"] = data["Date"] + " " + data["Year"]
data["Month"] = ""
data["Week"] = ""
data["Day_of_Year"] = ""
data["Day_of_Month"] = ""
data["Weekday"] = ""
for i in range(0,len(data)):
    mydate = data.iloc[i,0]
    data.iloc[i,0] = datetime.strptime(mydate, '%A, %b %d %Y').date()
    data.iloc[i,-5] = datetime.strptime(mydate, '%A, %b %d %Y').strftime('%B')
    data.iloc[i,-4] = datetime.strptime(mydate, '%A, %b %d %Y').strftime('%U')
    data.iloc[i,-3] = datetime.strptime(mydate, '%A, %b %d %Y').strftime('%j')
    data.iloc[i,-2] = datetime.strptime(mydate, '%A, %b %d %Y').strftime('%d')
    data.iloc[i,-1] = datetime.strptime(mydate, '%A, %b %d %Y').strftime('%A')
    
data["Weekend"] = ""
for i in range(0,len(data)):
    if (data.iloc[i,-2] == 'Friday') or \
       (data.iloc[i,-2] == 'Saturday') or \
       (data.iloc[i,-2] == 'Sunday'):
        data.iloc[i,-1] = 1
    else:
        data.iloc[i,-1] = 0
    
data["Home_Away"].replace(["@","Home"],[0,1],inplace=True)

data["Walkoff"] = ""
for i in range(0,len(data)):
    mystring = str(data.iloc[i,4])
    wo = mystring.find('-')
    if data.iloc[i,0]>=datetime.today().date():
        data.iloc[i,4] = ''
        data.iloc[i,-1] = ''
    elif wo != -1:
        data.iloc[i,-1] = 1
        data.iloc[i,4] = mystring[0]
    else:    
        data.iloc[i,-1] = 0
        data.iloc[i,4] = mystring[0]
        
data["W/L"].replace(["W","L"],[1,0],inplace=True)

data["Wins"] = ""
data["Losses"] = ""

for i in range(0,len(data)):
    mywl = str(data.iloc[i,8])
    wl = mywl.find('-')
    if wl != -1:
        data.iloc[i,-1] = int(mywl[wl+1:len(mywl)])
        data.iloc[i,-2] = int(mywl[0:wl])
        data.iloc[i,8] = round(data.iloc[i,-2]/(data.iloc[i,-2]+data.iloc[i,-1]),3)
        
data["Shortened"] = ""
data["Extra"] = ""
for i in range(0,len(data)):
    if data.iloc[i,0]>=datetime.today().date():
        data.iloc[i,-2] = ''
        data.iloc[i,-1] = ''
    elif data.iloc[i,7] < 9:
        data.iloc[i,-2] = 1
        data.iloc[i,-1] = 0
    elif data.iloc[i,7] > 9:
        data.iloc[i,-1] = 1
        data.iloc[i,-2] = 0
    else:
        data.iloc[i,-2] = 0
        data.iloc[i,-1] = 0

for i in range(0,len(data)):
    mygb = str(data.iloc[i,10])
    gb = mygb.find('up')
    if gb != -1:
        data.iloc[i,10] = float(mygb[gb+2:len(mygb)].lstrip())
    elif mygb == "Tied":
        data.iloc[i,10] = 0.0
    elif mygb != "None":
        data.iloc[i,10] = -float(mygb)
        
data["Team_Pitcher"] = ""
data["Opp_Pitcher"] = ""

for i in range(0,len(data)):
    if data.iloc[i,4] == 1:
        data.iloc[i,-1] = data.iloc[i,12]
        data.iloc[i,-2] = data.iloc[i,11]
    elif data.iloc[i,4] == 0:
        data.iloc[i,-1] = data.iloc[i,11]
        data.iloc[i,-2] = data.iloc[i,12]
        
data["Save"].replace(["None"],[''],inplace=True)

for i in range(0,len(data)):
    mytime = str(data.iloc[i,14])
    time = mytime.find(':')
    if time != -1:
        data.iloc[i,14] = datetime.strptime(mytime, '%I:%M').time()
        
data["D/N"].replace(["D","N"],[1,0],inplace=True)

for i in range(0,len(data)):
    if pd.isnull(data.iloc[i,18]) == True:
        data.iloc[i,18] = 0
    else:
        data.iloc[i,18] = 1
    
# Create "Interleague" variable        
AL = ["BAL","BOS","NYY","TBR","TOR","CHW","CLE","DET","KCR","MIN","HOU","LAA","OAK","SEA","TEX"] # Create list of AL teams
NL = ["ATL","MIA","NYM","PHI","WSN","CHC","CIN","MIL","PIT","STL","ARI","COL","LAD","SDP","SFG"] # Create list of NL teams

data["Interleague"] = "" # Create empty "Interleague" column in dataframe

# Iterate through each row in dataframe to test if team and opponent are in same league
# If TRUE then Interleague = 0. If FALSE then Interleague = 1
for i in range(0,len(data)):
    if (data.iloc[i,1] in AL and data.iloc[i,3] in AL) or \
       (data.iloc[i,1] in NL and data.iloc[i,3] in NL):
        data.iloc[i,-1] = 0
    else:
        data.iloc[i,-1] = 1
        
# Create "Rival" variable
ALE = ["BAL","BOS","NYY","TBR","TOR"] # Create list of ALE teams
ALC = ["CHW","CLE","DET","KCR","MIN"] # Create list of ALC teams
ALW = ["HOU","LAA","OAK","SEA","TEX"] # Create list of ALW teams
NLE = ["ATL","MIA","NYM","PHI","WSN"] # Create list of NLE teams
NLC = ["CHC","CIN","MIL","PIT","STL"] # Create list of NLC teams
NLW = ["ARI","COL","LAD","SDP","SFG"] # Create list of NLW teams

data["Rival"] = "" # Create empty "Rival" column in dataframe

# Iterate through each row in dataframe to test if team and opponent are in same division
# If TRUE then Rival = 1. If FALSE then Rival = 0
for i in range(0,len(data)):
    if (data.iloc[i,1] in ALE and data.iloc[i,3] in ALE) or \
       (data.iloc[i,1] in ALC and data.iloc[i,3] in ALC) or \
       (data.iloc[i,1] in ALW and data.iloc[i,3] in ALW) or \
       (data.iloc[i,1] in NLE and data.iloc[i,3] in NLE) or \
       (data.iloc[i,1] in NLC and data.iloc[i,3] in NLC) or \
       (data.iloc[i,1] in NLW and data.iloc[i,3] in NLW):
        data.iloc[i,-1] = 1
    else:
        data.iloc[i,-1] = 0
        
data['Gm#'] = data.groupby(['Year','Tm']).cumcount() + 1
data['HmGm#'] = data.groupby(['Year','Tm','Home_Away']).cumcount() + 1
for i in range(0,len(data)):
    if data.iloc[i,2] != 1:
        data.iloc[i,-1] = ''

cols = data.columns.tolist()
cols = [cols[0]]+[cols[37]]+[cols[38]]+[cols[19]]+[cols[22]]+[cols[23]]+[cols[24]]+[cols[25]]+[cols[26]]+[cols[27]] \
        +[cols[15]]+[cols[1]]+[cols[2]]+[cols[3]]+[cols[35]]+[cols[36]]+[cols[18]]+[cols[21]]+[cols[20]]+[cols[4]] \
        +[cols[28]]+[cols[29]]+[cols[30]]+[cols[8]]+[cols[5]]+[cols[6]]+[cols[7]]+[cols[32]]+[cols[31]]+[cols[9]] \
        +[cols[10]]+[cols[17]]+[cols[33]]+[cols[34]]+[cols[11]]+[cols[12]]+[cols[13]]+[cols[14]]+[cols[16]]
data = data[cols]

data = data.rename(index=str, columns={"D/N": "Day_Game", "Tm": "Team", "Home_Away": "Home", "Orig. Scheduled": "Rescheduled", "W/L": "Win", "W-L": "Win%", "Win": "Win_Pitcher", "Loss": "Loss_Pitcher", "Save": "Save_Pitcher", "Time": "Duration", "Attendance": "Distributed"})

os.chdir('C:\\Users\\JRAMIA\\OneDrive - Delaware North\\Analytics\\Projects\\Game Stats Pull')
writer = pd.ExcelWriter('MLB_Game_Stats.xlsx')
data.to_excel(writer,'Sheet1',index=False)
writer.save()