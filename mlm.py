from re import T
import torch
from transformers import BertTokenizer, BertModel, BertForMaskedLM
import os

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')
model.eval()

def predict_masked_sent(text, top_k = 5):
    text = "[CLS] %s [SEP]" % text
    tokenized_text = tokenizer.tokenize(text)
    masked_index = tokenized_text.index("[MASK]")
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])

    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]

    probs = torch.nn.functional.softmax(predictions[0, masked_index], dim=-1)
    top_k_weights, top_k_indices = torch.topk(probs, top_k, sorted=True)

    max_w = 0
    for i, pred_idx in enumerate(top_k_indices):
        predicted_token = tokenizer.convert_ids_to_tokens([pred_idx])[0]
        token_weight = top_k_weights[i]
        if token_weight > max_w:
            max_w = token_weight
            re_word = predicted_token
        print("[MASK]: '%s'"%predicted_token, " | weights:", float(token_weight))

    return re_word

need_correct = ['bg4_3', 'bg4_335', 'bg1_120', 'bg3_175', 'bg4_408', 'bg1_464', 'bg4_104', 'bg4_286', 'bg4_182', 'bg4_498', 'bg4_109', 'bg3_460', 'bg4_280', 'bg4_106', 'bg4_349', 'bg3_161', 'bg4_476', 'bg2_221', 'bg3_283', 'bg2_302', 'bg4_384', 'bg1_127', 'bg1_17', 'bg2_293', 'bg1_18', 'bg1_19', 'bg4_74', 'bg4_23', 'bg3_130', 'bg1_392', 'bg4_95', 'bg3_491', 'bg4_392', 'bg4_418', 'bg3_275', 'bg2_120', 'bg4_300', 'bg3_349', 'bg4_11', 'bg2_288', 'bg1_193', 'bg3_216', 'bg2_69', 'bg1_106', 'bg4_430', 'bg4_489', 'bg3_152', 'bg2_111', 'bg1_209', 'bg3_116', 'bg1_182', 'bg4_114', 'bg3_245', 'bg1_327', 'bg4_282', 'bg4_38', 'bg4_100', 'bg4_94', 'bg4_70', 'bg4_482', 'bg4_27', 'bg4_373', 'bg4_453', 'bg4_457', 'bg1_203', 'bg2_245', 'bg1_201', 'bg4_14', 'bg2_100', 'bg1_269', 'bg3_69', 'bg4_205', 'bg4_194', 'bg2_433', 'bg2_216', 'bg4_178', 'bg4_47', 'bg4_229', 'bg3_331', 'bg2_267', 'bg4_386', 'bg2_174', 'bg3_295', 'bg3_250', 'bg4_270', 'bg4_261', 'bg3_390', 'bg2_319', 'bg4_398', 'bg4_314', 'bg4_452', 'bg2_40', 'bg2_103', 'bg4_138', 'bg2_90', 'bg3_202', 'bg4_333', 'bg4_39', 'bg4_7', 'bg4_220', 'bg1_77', 'bg4_277', 'bg4_265', 'bg3_228', 'bg4_134', 'bg1_103', 'bg4_395', 'bg4_195', 'bg4_461', 'bg2_195', 'bg4_152', 'bg4_271', 'bg1_460', 'bg3_474', 'bg3_330', 'bg3_211', 'bg2_473', 'bg4_458', 'bg1_125', 'bg2_294', 'bg4_354', 'bg4_317', 'bg4_196', 'bg3_136', 'bg4_137', 'bg4_184', 'bg3_409', 'bg1_91', 'bg4_352', 'bg3_252', 'bg4_379', 'bg4_36', 'bg1_491', 'bg1_130', 'bg1_233', 'bg4_484', 'bg2_316', 'bg1_495', 'bg4_492', 'bg1_66', 'bg3_321', 'bg3_243', 'bg4_269', 'bg4_435', 'bg3_207', 'bg4_246', 'bg2_470', 'bg4_494', 'bg4_212', 'bg4_61', 'bg4_281', 'bg4_347', 'bg4_86', 'bg4_493', 'bg1_44', 'bg3_260', 'bg4_247', 'bg4_413', 'bg2_50', 'bg1_476', 'bg4_487', 'bg2_447', 'bg1_82', 'bg3_32', 'bg4_108', 'bg2_269', 'bg4_218', 'bg1_447', 'bg2_75', 'bg3_214', 'bg4_284', 'bg1_320', 'bg2_53', 'bg2_74', 'bg3_177', 'bg3_21', 'bg4_308', 'bg4_402', 'bg3_209', 'bg3_290', 'bg1_302', 'bg4_90', 'bg4_155', 'bg1_81', 'bg2_192', 'bg2_348', 'bg3_407', 'bg2_64', 'bg1_96', 'bg4_276', 'bg2_49', 'bg4_419', 'bg2_282', 'bg1_283', 'bg1_134', 'bg1_102', 'bg4_371', 'bg4_295', 'bg4_337', 'bg2_223', 'bg2_297', 'bg2_280', 'bg1_398', 'bg4_234', 'bg4_239', 'bg2_309', 'bg2_415', 'bg4_20', 'bg4_119', 'bg4_186', 'bg2_5', 'bg4_42', 'bg3_458', 'bg2_460', 'bg2_271', 'bg1_0', 'bg4_421', 'bg2_66', 'bg1_258', 'bg1_22', 'bg4_454', 'bg4_213', 'bg4_495', 'bg4_436', 'bg2_300', 'bg4_340', 'bg4_336', 'bg2_392', 'bg2_89', 'bg3_210', 'bg1_457', 'bg4_301', 'bg4_1', 'bg2_420', 'bg4_422', 'bg4_206', 'bg2_451', 'bg3_148', 'bg3_466', 'bg3_406']

inputP = './result/spellchecker/'
outputP = './result/mlm/'

for f in os.listdir(inputP):
    if f.replace('.txt', '') in need_correct:

        out = open(outputP + f, 'w')
        with open(inputP + f, 'r') as txt:
            lines = txt.readlines()
            for line in lines:
                predict_txt = line
                predict_txt = predict_txt.replace('.', ' ')
                pre_txt = predict_txt.split(' ')
                for i in range(len(pre_txt)):
                    changed_txt = pre_txt.copy()
                    print(changed_txt[i])
                    if not(len(changed_txt[i]) == 1 and changed_txt[i].isalpha()):
                        continue
                    changed_txt[i] = "[MASK]"
                    masked_txt = " ".join(changed_txt)
                    predict_token = predict_masked_sent(masked_txt, top_k=3)
                    if changed_txt[i] != predict_token:
                        pre_txt[i] = predict_token
                    print(" ".join(pre_txt))
                    print('\n')

                print(" ".join(pre_txt))
                corrected_line = " ".join(pre_txt)
                out.write(corrected_line)
                
        out.close()
    else:
        out = open(outputP + f, 'w')
        with open(inputP + f, 'r') as txt:
            lines = txt.readlines()
            for line in lines:
                out.write(line)
        out.close()