# 簡介
我們的專題題目是文字辨識與校正，將單行文字的圖片檔(.jpg)經過辨識模型與校正錯字後輸出成文字檔(.txt)
# 架構圖
![](https://i.imgur.com/8Jbt22j.png)


# 需要安裝的環境＆版本
| module         | version  |
| -------------- | -------- |
| Python         | 3.7.11   |
| torch          | 1.9.0    |
| torchvision    | 0.10.0   |
| beautifulsoup4 | 4.10.0   |
| Distance       | 0.1.3    |
| easyocr        | 1.5.0    |
| opencv-python  | 4.5.3.56 |
| requests       | 2.27.1   |
| transformers   | 4.19.2   |
| trdg           | 1.7.0    |

# train
* 我們用的訓練資料在 ```dataset/training_data```。
* 我們用 [deep-text-recognition-benchmark](https://github.com/clovaai/deep-text-recognition-benchmark) 訓練 CRNN 模型。
* 訓練好模型放在 ```model```。

# test
* 資料放在 ```dataset/testing_data```。
* 因為不用 detector，所以須修改以下 code：
    1. 將 readtext 的參數新增 ```detector=True```：
    ```python
    def readtext(self, image, decoder = 'greedy', beamWidth= 5, batch_size = 1,\
                     workers = 0, allowlist = None, blocklist = None, detail = 1,\
                     rotation_info = None, paragraph = False, min_size = 20,\
                     contrast_ths = 0.1,adjust_contrast = 0.5, filter_ths = 0.003,\
                     text_threshold = 0.7, low_text = 0.4, link_threshold = 0.4,\
                     canvas_size = 2560, mag_ratio = 1.,\
                     slope_ths = 0.1, ycenter_ths = 0.5, height_ths = 0.5,\
                     width_ths = 0.5, y_ths = 0.5, x_ths = 1.0, add_margin = 0.1, output_format='standard'):
    ```
    改成
    ```python
    def readtext(self, image, decoder = 'greedy', beamWidth= 5, batch_size = 1,\
                     workers = 0, allowlist = None, blocklist = None, detail = 1,\
                     rotation_info = None, paragraph = False, min_size = 20,\
                     contrast_ths = 0.1,adjust_contrast = 0.5, filter_ths = 0.003,\
                     text_threshold = 0.7, low_text = 0.4, link_threshold = 0.4,\
                     canvas_size = 2560, mag_ratio = 1.,\
                     slope_ths = 0.1, ycenter_ths = 0.5, height_ths = 0.5,\
                     width_ths = 0.5, y_ths = 0.5, x_ths = 1.0, add_margin = 0.1, output_format='standard', detector=True):
    ```
    
    2. 將 readtext 裡的
    ```python
    horizontal_list, free_list = self.detect(img, min_size, text_threshold,\
                                                     low_text, link_threshold,\
                                                     canvas_size, mag_ratio,\
                                                     slope_ths, ycenter_ths,\
                                                     height_ths,width_ths,\
                                                     add_margin, False)
    # get the 1st result from hor & free list as self.detect returns a list of depth 3
    horizontal_list, free_list = horizontal_list[0], free_list[0]
    ```
    改成
    ```python
    if detector:
        horizontal_list, free_list = self.detect(img, min_size, text_threshold,\
                                                 low_text, link_threshold,\
                                                 canvas_size, mag_ratio,\
                                                 slope_ths, ycenter_ths,\
                                                 height_ths,width_ths,\
                                                 add_margin, False)
        # get the 1st result from hor & free list as self.detect returns a list of depth 3
        horizontal_list, free_list = horizontal_list[0], free_list[0]
    else:
        horizontal_list, free_list = None, None
    ```
* 執行 ```crnn_test.py``` (可修改 ```crnn_test.py``` 中的路徑)。
* 預設輸出在 ```result/crnn```。
* 執行 ```SpellChecker.py``` (可修改 ```SpellChecker.py``` 中的路徑)。
* 預設輸出在 ```result/spellchecker```。
* 執行 ```mlm.py``` (可修改 ```mlm.py``` 中的路徑)。
* 預設輸出在 ```result/mlm```。
* 最後執行 ```cal_accuracy.py``` 計算字元準確率。
* 可執行 ```generate_dict.py``` 繼續更新字典。

# 結果

|                           | accuracy | accuracy (針對 crnn 中 confident < 0.5 的資料) |
| ------------------------- | -------- | --- |
| crnn                      | 0.9081   |     |
| crnn + spellchecker       | 0.8983   | 0.9085 |
| crnn + spellchecker + mlm | 0.8945   | 0.9080 |

| CRNN                      | accuracy |
| ------------------------- | -------- |
| 全字元                    | 0.9081   |
| 不看大小寫                | 0.9103   |
| 英文 + 數字 （去掉標點符號） | 0.9477   |


# reference
* [CRNN](https://github.com/JaidedAI/EasyOCR)
* [deep-text-recognition-benchmark (CRNN-train)](https://github.com/clovaai/deep-text-recognition-benchmark)
* [TRDG-文字圖片生成器](https://github.com/Belval/TextRecognitionDataGenerator)