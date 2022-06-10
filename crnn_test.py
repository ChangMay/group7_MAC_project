import easyocr
from os import listdir
import cv2

# load model
rd = easyocr.Reader(['en'], model_storage_directory='./model/', user_network_directory='./model/', recog_network = 'wiki_en', detector=False)

# file path
img_path = './dataset/testing_data/img/'
output_path = './result/crnn/'

# if character list differs in training and testing
train_char = '0123456789 !"#$%&\'()*+,-./:;?@[\\]^_`{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
test_char = '0123456789 !"#$%&\'()*+,-./:;?@[\\]^_`{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

cnt = 0
low_conf = []
for f in listdir(img_path):
    if f.endswith('.jpg') or f.endswith('.png'):
        print(f)##############################

        origin_img = cv2.imread(img_path+f)     # read image
        h, w, _ = origin_img.shape
        
        with open(output_path+'.'.join(f.split('.')[:-1])+'.txt', 'w') as out:
            r1 = rd.readtext(origin_img, output_format='dict', detector=False)  # predict
            print(r1)#####################

            # if character list differs in training and testing
            text = ''
            for c in r1[0]['text']:
              text += train_char[test_char.find(c)]

            if r1[0]['confident'] < 0.5:
              low_conf.append('.'.join(f.split('.')[:-1]))
              cnt += 1

            out.write(text + '\n')    # write output

print(low_conf)
print(cnt)