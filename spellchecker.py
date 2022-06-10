import distance
import os
import string
import pickle

dictionary_path = './dictionary/dict_sorted.pkl'
inputP = './result/crnn/'
outputP = './result/spellchecker/'

need_correct = ['bg4_3', 'bg4_335', 'bg1_120', 'bg3_175', 'bg4_408', 'bg1_464', 'bg4_104', 'bg4_286', 'bg4_182', 'bg4_498', 'bg4_109', 'bg3_460', 'bg4_280', 'bg4_106', 'bg4_349', 'bg3_161', 'bg4_476', 'bg2_221', 'bg3_283', 'bg2_302', 'bg4_384', 'bg1_127', 'bg1_17', 'bg2_293', 'bg1_18', 'bg1_19', 'bg4_74', 'bg4_23', 'bg3_130', 'bg1_392', 'bg4_95', 'bg3_491', 'bg4_392', 'bg4_418', 'bg3_275', 'bg2_120', 'bg4_300', 'bg3_349', 'bg4_11', 'bg2_288', 'bg1_193', 'bg3_216', 'bg2_69', 'bg1_106', 'bg4_430', 'bg4_489', 'bg3_152', 'bg2_111', 'bg1_209', 'bg3_116', 'bg1_182', 'bg4_114', 'bg3_245', 'bg1_327', 'bg4_282', 'bg4_38', 'bg4_100', 'bg4_94', 'bg4_70', 'bg4_482', 'bg4_27', 'bg4_373', 'bg4_453', 'bg4_457', 'bg1_203', 'bg2_245', 'bg1_201', 'bg4_14', 'bg2_100', 'bg1_269', 'bg3_69', 'bg4_205', 'bg4_194', 'bg2_433', 'bg2_216', 'bg4_178', 'bg4_47', 'bg4_229', 'bg3_331', 'bg2_267', 'bg4_386', 'bg2_174', 'bg3_295', 'bg3_250', 'bg4_270', 'bg4_261', 'bg3_390', 'bg2_319', 'bg4_398', 'bg4_314', 'bg4_452', 'bg2_40', 'bg2_103', 'bg4_138', 'bg2_90', 'bg3_202', 'bg4_333', 'bg4_39', 'bg4_7', 'bg4_220', 'bg1_77', 'bg4_277', 'bg4_265', 'bg3_228', 'bg4_134', 'bg1_103', 'bg4_395', 'bg4_195', 'bg4_461', 'bg2_195', 'bg4_152', 'bg4_271', 'bg1_460', 'bg3_474', 'bg3_330', 'bg3_211', 'bg2_473', 'bg4_458', 'bg1_125', 'bg2_294', 'bg4_354', 'bg4_317', 'bg4_196', 'bg3_136', 'bg4_137', 'bg4_184', 'bg3_409', 'bg1_91', 'bg4_352', 'bg3_252', 'bg4_379', 'bg4_36', 'bg1_491', 'bg1_130', 'bg1_233', 'bg4_484', 'bg2_316', 'bg1_495', 'bg4_492', 'bg1_66', 'bg3_321', 'bg3_243', 'bg4_269', 'bg4_435', 'bg3_207', 'bg4_246', 'bg2_470', 'bg4_494', 'bg4_212', 'bg4_61', 'bg4_281', 'bg4_347', 'bg4_86', 'bg4_493', 'bg1_44', 'bg3_260', 'bg4_247', 'bg4_413', 'bg2_50', 'bg1_476', 'bg4_487', 'bg2_447', 'bg1_82', 'bg3_32', 'bg4_108', 'bg2_269', 'bg4_218', 'bg1_447', 'bg2_75', 'bg3_214', 'bg4_284', 'bg1_320', 'bg2_53', 'bg2_74', 'bg3_177', 'bg3_21', 'bg4_308', 'bg4_402', 'bg3_209', 'bg3_290', 'bg1_302', 'bg4_90', 'bg4_155', 'bg1_81', 'bg2_192', 'bg2_348', 'bg3_407', 'bg2_64', 'bg1_96', 'bg4_276', 'bg2_49', 'bg4_419', 'bg2_282', 'bg1_283', 'bg1_134', 'bg1_102', 'bg4_371', 'bg4_295', 'bg4_337', 'bg2_223', 'bg2_297', 'bg2_280', 'bg1_398', 'bg4_234', 'bg4_239', 'bg2_309', 'bg2_415', 'bg4_20', 'bg4_119', 'bg4_186', 'bg2_5', 'bg4_42', 'bg3_458', 'bg2_460', 'bg2_271', 'bg1_0', 'bg4_421', 'bg2_66', 'bg1_258', 'bg1_22', 'bg4_454', 'bg4_213', 'bg4_495', 'bg4_436', 'bg2_300', 'bg4_340', 'bg4_336', 'bg2_392', 'bg2_89', 'bg3_210', 'bg1_457', 'bg4_301', 'bg4_1', 'bg2_420', 'bg4_422', 'bg4_206', 'bg2_451', 'bg3_148', 'bg3_466', 'bg3_406']

# pyspellerchecker
class SpellCheck:
    def __init__(self):
        self.dictionary = None
        with open(dictionary_path, 'rb') as f:
            self.dictionary = pickle.load(f)
    
    def correction(self, text):
        words = text.split()
        
        for i in range(len(words)):
            print("now word: ", words[i])
            change_middle = 0
            change_two_ends = 0
            change_begin = 0
            change_end = 0
            
            most_likely_word = words[i]
            max_prob = 0
            
            # len = 1
            if len(words[i]) <= 1:
                continue

            # is digit or not
            if words[i].isdigit():
                continue
            
            if words[i].find(',') != -1 and words[i].find(',') != len(words[i])-1:
                is_digit = True
                for char in words[i]:
                    if (not char.isdigit()) and char == ',' and char != '.':
                        is_digit = False
                        break
                if is_digit:
                    continue
            
            # change_end  .?!  ,:;%~
            if (words[i][-1] == '.' or words[i][-1] == '?' or words[i][-1] == '!') and i == len(words) - 1:
                add_end = words[i][-1]
                words[i] = words[i][:-1]
                change_end = 1
                
            elif words[i][-1] == ',' or words[i][-1] == ':' or words[i][-1] == ';' or words[i][-1] == '%' or words[i][-1] == '~':
                add_end = words[i][-1]
                words[i] = words[i][:-1]
                change_end = 1
                
            # len = 1
            if len(words[i]) == 1:
                if change_end:
                    words[i] = words[i] + add_end
                continue

            # change_begin  #$&@
            if words[i][0] == '#' or words[i][0] == '$' or words[i][0] == '&' or words[i][0] == '@':
                add_begin = words[i][0]
                words[i] = words[i][1:]
                change_begin = 1
                
            # len = 1
            if len(words[i]) == 1:
                if change_begin:
                    words[i] = add_begin + words[i]
                if change_end:
                    words[i] = words[i] + add_end
                continue

            # change_two_ends  ()[]{}"'\`            
            if (words[i][0] == '{' and words[i][-1] == '}') or (words[i][0] == '[' and words[i][-1] == ']') or (words[i][0] == '(' and words[i][-1] == ')') or (words[i][0] == '`' and words[i][-1] == '`') or (words[i][0] == '"' and words[i][-1] == '"') or (words[i][0] == "'" and words[i][-1] == "'") or (words[i][0] == '\\' and words[i][-1] == '\\'):
                add_two_ends = (words[i][0], words[i][-1])
                words[i] = words[i][1:-1]
                change_two_ends = 1
                
            # len = 1
            if len(words[i]) == 1:
                if change_two_ends:
                    words[i] = add_two_ends[0] + words[i] + add_two_ends[1]
                if change_begin:
                    words[i] = add_begin + words[i]
                if change_end:
                    words[i] = words[i] + add_end
                continue

            # change_middle  _/.
            if words[i].count('_') == 1 and (words[i][0] != '_' and words[i][-1] != '_'):
                left_word, right_word = words[i].split('_')
                most_likely_wordL = left_word
                most_likely_wordR = right_word
                max_probL = 0
                max_probR = 0
                add_middle = '_'
                change_middle = 1
            elif words[i].count('/') == 1 and (words[i][0] != '/' and words[i][-1] != '/'):
                left_word, right_word = words[i].split('/')
                most_likely_wordL = left_word
                most_likely_wordR = right_word
                max_probL = 0
                max_probR = 0
                add_middle = '/'
                change_middle = 1
            elif words[i].count('.') == 1 and (words[i][0] != '.' and words[i][-1] != '.'):
                left_word, right_word = words[i].split('.')
                most_likely_wordL = left_word
                most_likely_wordR = right_word
                max_probL = 0
                max_probR = 0
                add_middle = '.'
                change_middle = 1
                
            for dict_word, freq in self.dictionary.items():
                if change_middle:
                    if left_word.isdigit() and right_word.isdigit():
                        most_likely_word = words[i]
                        break
                    
                    if not left_word.isdigit():
                        if len(left_word) - len(dict_word) > 5:
                            continue
                        if len(dict_word) - len(left_word) > 5:
                            break
                        wrong = distance.levenshtein(left_word.lower(), dict_word.lower())
                        total = len(dict_word)
                        prob = (total - wrong) / total
                        
                        if prob == 1:
                            most_likely_wordL = left_word
                            break
        
                        elif (prob > 0.75 or wrong < 3) and total > 1 and left_word not in string.punctuation:
                            prob += (freq / 1000)
                            
                            if prob > max_probL:
                                max_probL = prob
                                most_likely_wordL = dict_word
                            
                    if not right_word.isdigit():
                        if len(right_word) - len(dict_word) > 5:
                            continue
                        if len(dict_word) - len(right_word) > 5:
                            break
                        wrong = distance.levenshtein(right_word.lower(), dict_word.lower())
                        total = len(dict_word)
                        prob = (total - wrong) / total
                        
                        if prob == 1:
                            most_likely_wordR = right_word
                            break
        
                        elif (prob > 0.75 or wrong < 3) and total > 1 and right_word not in string.punctuation:
                            prob += (freq / 1000)
                            
                            if prob > max_probR:
                                max_probR = prob
                                most_likely_wordR = dict_word
                    
                
                else:
                    if len(words[i]) - len(dict_word) > 5:
                            continue
                    if len(dict_word) - len(words[i]) > 5:
                        break
                    wrong = distance.levenshtein(words[i].lower(), dict_word.lower())
                    total = len(dict_word)
                    prob = (total - wrong) / total
                    
                    if prob == 1:
                        most_likely_word = words[i]
                        break
    
                    elif (prob > 0.75 or wrong < 3) and total > 1 and words[i] not in string.punctuation:
                        prob += (freq / 1000)
                        
                        if prob > max_prob:
                            max_prob = prob
                            most_likely_word = dict_word
                             
            if change_middle:
                most_likely_word = add_middle.join([most_likely_wordL, most_likely_wordR])
                
            if change_two_ends:
                most_likely_word = add_two_ends[0] + most_likely_word + add_two_ends[1]
                
            if change_begin:
                most_likely_word = add_begin + most_likely_word
                
            if change_end:
                most_likely_word = most_likely_word + add_end
            
            words[i] = most_likely_word
		
        return " ".join(words)

cnt = 0
for f in os.listdir(inputP):
    cnt += 1
    print(cnt)
    if f in os.listdir(outputP):
        continue
    if f.replace('.txt', '') in need_correct:
        out = open(outputP + f, 'w')
        with open(inputP + f, 'r') as txt:
            lines = txt.readlines()
            for line in lines:
                changed = 0
                str = '.\n'
                if line.find(str, 0, len(line)) != -1:
                    changed = 1
                    line = line.replace('.\n', ' \n')
                if line != '\n':
                    print(line.split('\n')[0])#####################
                    spellchecker = SpellCheck()
                    output = spellchecker.correction(line.split('\n')[0])
                    print(output)###################
                    if changed:
                        out.write(output + '.\n')
                    else:
                        out.write(output + '\n')
        out.close()
    else:
        out = open(outputP + f, 'w')
        with open(inputP + f, 'r') as txt:
            lines = txt.readlines()
            for line in lines:
                out.write(line)
        out.close()