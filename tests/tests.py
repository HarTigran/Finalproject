import boto3
import csv
import pandas as pd

s3 = boto3.client('s3')

#fetch the file from s3
response = s3.get_object(Bucket = 'images-from-web', Key = 'test.csv')
        
# deserialize the file's content
        
lines = response['Body'].read().decode('utf-8').splitlines(True)

reader = csv.DictReader(lines)
df = pd.DataFrame(reader)

a = df[df.iloc[:,2].str.contains('00Z0Z_gHyYY95A4n0z_08I08I')][1]
# b = df[df.iloc[:,2].str.contains('00q0qIsbLOZcILZz_0hK08A')]['car_price'][0]
        
# url_list = []
# for rows in reader:
#     url_list.append(row)

print(str(a['car_price'].iloc[0]))