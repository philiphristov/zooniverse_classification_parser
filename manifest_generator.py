import os
import re
import csv

list_images = (os.listdir('C:/Users/fhristov/Desktop/VA/zooniverse filtered'))




with open('manifest.csv', mode='w', newline='') as manifest_file:
    manifest_writer = csv.writer(manifest_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for x in list_images:
        number = re.search('#(.+?)_', x) 
                         
        if number:
            img_nr = number.group(1)
            print(x)
            print(img_nr)
            manifest_writer.writerow([x, img_nr, "map"])