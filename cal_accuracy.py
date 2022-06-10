import os
import distance

### file path
predict_path = "./result/crnn/"
gt_path = "./dataset/testing_data/"

total = 0
wrong = 0

predict_char = ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'  # en

### read gt
gts = {}
with open(gt_path+'gt.txt', 'r') as gf:
  for line in gf.readlines():
    if line != '\n':
      gts[line.split('\t', 1)[0].split('.')[0].split('/', 1)[1]] = line.split('\t', 1)[1].split('\n')[0]  # en

for f in os.listdir(predict_path):
  if f.endswith('.txt'):
    with open(predict_path+f, 'r') as pf:
      for line in pf.readlines():
        if line == '\n':
          continue
        pred_text = line.split('\n')[0]
    
    pred_removed = pred_text
    for char in pred_text:
      if predict_char.find(char) == -1:
        pred_removed = pred_removed.replace(char,"")
    
    # get gt
    gt_text = gts[f.split('.')[0]]
    
    gt_removed = gt_text
    for char in gt_text:
      if predict_char.find(char) == -1:
        gt_removed = gt_removed.replace(char,"")
    
    # print wrong predictions
    if distance.levenshtein(pred_text, gt_text) > 0:
      print('pred_text:', pred_text)#####################
      print('gt_text: ', gt_text)#######################
      print()################################

    # compute error rate
    wrong += distance.levenshtein(pred_text, gt_text)
    total += len(gt_text)
    
print('char_accuracy: ', (total - wrong)/total)
