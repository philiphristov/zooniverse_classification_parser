import os
import re
import csv
import pandas
import json
import matplotlib.pyplot as plt
import matplotlib

from PIL import Image


parsed_data = []

df = pandas.read_csv("va-classifications.csv")
annotations = df["annotations"]
subject_data = df["subject_data"]

for index, row in df.iterrows():
	annotation = json.loads( row['annotations'])[0]
	subject_data = json.loads(row['subject_data'])
	values = annotation["value"]

	subject_key, subject_value =  next(iter( subject_data.items() ))
	image_name = "subject_data/" + subject_value["current_subject_number"]

	name = subject_value["current_subject_number"].replace(".jpg", "")
	file_name = "current_results/" +  name + "-(current markings)" + ".png"

	# pillow
	im = Image.open(image_name)
	im_width, im_height = im.size

	# ploting
	img = matplotlib.image.imread(image_name)
	figure, ax = plt.subplots(1)
	ax.imshow(img)

	print(name)

	for key, value in enumerate(values):
		current_x = value["x"]
		current_y = value["y"]
		current_width = value["width"]
		current_height = value["height"]

		detail_number = value["details"][0]["value"]
		detail_transcription = value["details"][1]["value"]
		print(detail_number, detail_transcription)

		if detail_number is not "" and detail_transcription is not "":
			parsed_data.append({"subject_id": subject_value["current_subject_number"], "key": str(key), "map_number":detail_number , "transcription":detail_transcription})
		# plot visualisation
		rect = matplotlib.patches.Rectangle((current_x,current_y),current_width,current_height, edgecolor='r', facecolor="none")
		ax.add_patch(rect)

		# pillow cropping
		(left, upper, right, lower) =  ( current_x, current_y, current_x + current_width , current_y + current_height )
		im_crop = im.crop(box=(left, upper, right, lower))
		file_name = "current_results/" +  name + "-" + str(key)+ ".png"
		im_crop.save(file_name, quality=95)

	figure.show()

data_frame = pandas.DataFrame(parsed_data)
data_frame.to_csv("training_data.csv")

	# save plot
	# name = subject_value["current_subject_number"].replace(".jpg", "")
	# plt.savefig(file_name)
