import csv

if __name__ == "__main__":
    
    # Function for reading a csv file with player information and dividing players into three lists called "Dragons", "Sharks" and "Raptors"     
    def Divide_into_teams():      
        Dragons = []
        Sharks = []
        Raptors = []
        
        with open("soccer_players.csv", "r") as readfile:
            player_reader = csv.DictReader(readfile, delimiter=',')
            rows = list(player_reader)
                
            Soccer_experience = []
            No_soccer_experience = []        
                
            for row in rows:
                if row["Soccer Experience"] == "YES":  
                    Soccer_experience.append(row)
                else:
                    No_soccer_experience.append(row)
            while len(Soccer_experience) != 0:
                Dragons.append(Soccer_experience.pop())
                Sharks.append(Soccer_experience.pop())
                Raptors.append(Soccer_experience.pop())
            while len(No_soccer_experience) != 0:
                Dragons.append(No_soccer_experience.pop())
                Sharks.append(No_soccer_experience.pop())
                Raptors.append(No_soccer_experience.pop())
        
        tuple = (Dragons, Sharks, Raptors)
        
        return tuple
    
    # Function which uses the return of method "Divide_into_teams" and produces a text file with player teams
    def Write_file(tuple):
        
        Dragons, Sharks, Raptors = tuple
        
        Dragons_text = "Dragons" + "\n" 
        Sharks_text = "Sharks" + "\n"
        Raptors_text = "Raptors" + "\n"
        
        for row in Dragons:
            Dragons_text += row['Name']+", "+row['Soccer Experience']+", "+row['Guardian Name(s)'] + "\n"   
        
        for row in Sharks:
            Sharks_text += row['Name']+", "+row['Soccer Experience']+", "+row['Guardian Name(s)'] + "\n"   
        
        for row in Raptors:
            Raptors_text += row['Name']+", "+row['Soccer Experience']+", "+row['Guardian Name(s)'] + "\n"   
        
        with open("teams.txt", "w") as file:
            file.write(Dragons_text + "\n" + Sharks_text + "\n" + Raptors_text)
    
    # Function for producing welcome letters to players' guardians
    def Write_player_letters(tuple):
        
        Dragons, Sharks, Raptors = tuple
        
        for row in Dragons:
            Name = row['Name']
            Guardian_name = row['Guardian Name(s)']
            File_name = '_'.join(Name.lower().split())
            Text = "Dear {}, we would like to inform you that {} is part of the Dragons team and that the first practice session will be held on 1.10.2017 at 1:00 am.".format(Guardian_name, Name)
            with open(File_name+".txt", "w") as file:
                file.write(Text)

        for row in Sharks:
            Name = row['Name']
            Guardian_name = row['Guardian Name(s)']
            File_name = '_'.join(Name.lower().split())
            Text = "Dear {}, we would like to inform you that {} is part of the Sharks team and that the first practice session will be held on 1.10.2017 at 1:00 am.".format(Guardian_name, Name)
            with open(File_name+".txt", "w") as file:
                file.write(Text)

        for row in Raptors:
            Name = row['Name']
            Guardian_name = row['Guardian Name(s)']
            File_name = '_'.join(Name.lower().split())
            Text = "Dear {}, we would like to inform you that {} is part of the Raptors team and that the first practice session will be held on 1.10.2017 at 1:00 am.".format(Guardian_name, Name)
            with open(File_name+".txt", "w") as file:
                file.write(Text)
                
    def Main():
        Write_file(Divide_into_teams())
        Write_player_letters(Divide_into_teams())
        
    Main()        
            
                