from pygoogle_image import image as pi
import csv
import pandas

csv_path = r"C:\Users\jorda\OneDrive - IU International University of Applied Sciences\Dokumente\images.csv"

df = pandas.read_csv(csv_path)

if 'images' not in df.columns:
    print("Image column not found in csv") 
else :
    for keyword in df['images']:
        print(f"Downloading images for {keyword}")
        pi.download(keywords=keyword, limit=1, directory=r"C:\Users\jorda\PycharmProjects\agentic_llm\openai\images")
    