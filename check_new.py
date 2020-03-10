import http.client
import re
import requests
import time

#File name that contains all the sitemap links
originalFileName = "test.xml"

# Add here the code you need to check
theFlag={"200":[], "301":[], "302":[]}

class Serverresponsecode:
    def __init__(self, file_name):
        self.file_name = file_name
        self.links_filename = None
        self.results_filename = None
         
    #Return a new name for the file that has the sitemap links then the results
    #"_all_links.txt"
    #"_results.txt"
    def change_File_name(self, rename_str, links=False):
        the_file = self.file_name.split(".")
        file_name = the_file[0];
        new_link_file_name = file_name + rename_str
        createFile = open(new_link_file_name, "a")
        createFile.close()
        if links:
            self.links_filename = new_link_file_name
        else:
            self.results_filename = new_link_file_name
    #test_all_links.xml
    #test_results.txt
    
    #Extract links and add it to a file
    def extract_links_add_to_new_file(self):
        #Link pattern
        pattern = "(https:\/\/.*?)<\/loc"

        #Open the file that contains all sitemap links
        originalFile = open(self.file_name, "r")

        #Read the opened file
        theTextFile = originalFile.read()

        #Search all the links; 
        #The 'match' variable will have as a list all the links
        match = re.findall(pattern, theTextFile)
        
        linkFile = open(self.links_filename, "r+")
        linkFile.truncate(0)
        for aLink in match:
            aLink = aLink.strip()
            #Add links to the new file that will be created
            linkFile.write(aLink + "\n")
            
            
    def write_targeted_report(self):
        allLinks = open(self.links_filename, "r")
        for line in allLinks.readlines():
            line = line.strip()            
            x = requests.get(line, allow_redirects=False)
            for the_key in theFlag:                
                if (the_key == str(x.status_code)):                    
                    theFlag[the_key].append(line)                
            time.sleep(1)        
        allLinks.close()
        
    def write_final_report(self):
        final_report = open(self.results_filename,"w")
        final_report.truncate(0)
        #final_report.write()
        
    
        for response in theFlag:
            final_report.write ("-------------------------------------------------------------------" + "\n")
            final_report.write (response + "\n")
            if theFlag[response]:
                for line_result in theFlag[response]:
                    final_report.write(line_result + "\n")            
                final_report.write ("-------------------------------------------------------------------" + "\n")
                final_report.write("\n \n \n")
            else:
                final_report.write ("No results" + "\n")
                final_report.write ("-------------------------------------------------------------------" + "\n")
        final_report.close()
        
        
#Here is the new file name
links_file = Serverresponsecode(originalFileName)

#Create the empty files
links_file.change_File_name("_all_links.txt", links=True)
links_file.change_File_name("_results.txt")

#Extract links then add it to the file
links_file.extract_links_add_to_new_file()

#Write the targeted links - flag server response
links_file.write_targeted_report()

#Write final report
links_file.write_final_report()

print ("-------------------------------------------------------------------")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>Test successful<<<<<<<<<<<<<<<<<<<<<<<<<<")
print ("-------------------------------------------------------------------")
