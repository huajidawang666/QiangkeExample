# 一个简单的示例抢课程序

## 环境配置 | Environmental Configuration
程序需要的依赖：

Python ≥ 3.8

Pip 库：
- Selenium 用于模拟浏览器环境
- DdddOcr 用于识别验证码

确保你已经安装Python，否则[点击此处](https://www.python.org/)来安装。

通过如下的方式来安装所需的Pip库。

使用`Windows徽标键`+`R`来打开`运行`对话框。
键入`cmd`来打开命令提示符。

通过键入以下命令来安装`Selenium`和`DdddOcr`。

```bash
python -m pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install ddddocr -i https://pypi.tuna.tsinghua.edu.cn/simple
```
其中`-i https://pypi.tuna.tsinghua.edu.cn/simple`可以替换为任何你偏好的镜像源，或删去（尽管不建议这样做）。
## 调试和运行 | Debugging and Running
抢课是一类高度定制化的需求。所以我们强烈推荐阅读下面的用例来让它符合你的需求。
### 关于 XPath | About XPath
通常地，网页由html文件决定它的框架。而XPath是一种能够唯一地确定每种元素的路径。

例如，在某个网站的页面上有一个按钮，而这个按钮元素在html中是这样定义的：
```html
<!DOCTYPE HTML>
<head>
    …
</head>
<body>
    <div>
        …
    </div>
    <div>
        <a id = "link" href = "…">This is a link.</a>
        <div>
            <button>
                This is a button.
            </button>
            …
        </div>
        …
    </div>
    …
</div>
```
那么，这个按钮元素的XPath即为`/html/body/div[2]/div/button`。

显然地，XPath是一种层级结构，每个元素或不含下标，或含有表示其次序的下标。如上例的`div[2]`表示该父级中的第二个div元素。

通过如下方式来获得网页上某个元素的XPath。

对网页上的某元素右键，在弹出的菜单中单击`检视`。在随后弹出的开发者控制台将会定位到检视的元素。右键控制台中被定位的元素，选择`复制完整XPath`。

在html中，ID也是能唯一确定元素的一种方式，因为html要求每一种元素的ID不能重复。例如上例中ID为`link`指代的是\<a\>元素定义的链接。

但值得注意的是，并不是所有的元素都具有自己的ID，甚至大多数元素都不会拥有ID。

### Selenium的基本使用 | Basic Usage of Selenium

使用下面的代码来初始化Selenium，并打开一个Selenium窗口，访问链接为`url`的网站：
```python
# 导入必要库
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time
import ddddocr

url = "https://example.com" # 键入需要的url

# 模拟浏览器打开网站
options = Options() # 添加启动参数
options.add_argument('--no-sandbox') # 关闭沙盒启动
driver = webdriver.Chrome(options = options)
driver.get(url)
```

要对浏览器进行任意的Selenium模拟操作，可以使用下面的代码:
```python
# 窗口最大化：
driver.maximize_window()

# 获取屏幕截图并保存
driver.save_screenshot("./screenshot.png") # 保存截图到同目录下的screenshot.png

# 对任意的元素进行操作，需要用下面的代码来找到该元素：
# 通过某元素的XPath或ID均可以找到该元素。
ExampleXPath = "/html/body/div/div/" # 某元素的XPath
ExampleID = "imput-1" #某元素的ID
driver.find_element(By.XPATH, ExampleXPath).[Behavior] # 通过XPath来找到该元素并执行某操作
driver.find_element(By.ID, ExampleID).[Behavior] # 通过ID来找到该元素并执行某操作

# 例如：
# 模拟鼠标单击某个元素 (文字, 按钮, 复选框等)：
ExampleXPath = "/html/body/div/div/" # 某元素的XPath
driver.find_element(By.XPATH, ExampleXPath).click() # 通过XPath确定元素并点击

# 模拟找寻输入框并输入文本：
ExampleID = "imput-1" # 某输入框的ID
ExampleText = "Text you wanna type" # 欲输入的某段文本
driver.find_element(By.ID, ExampleID).send_keys(ExampleText) # 通过ID找到该输入框并输入文本ExampleText

# 暂停操作一段时间，并每隔500ms扫描一次某元素是否出现。出现该元素时结束扫描，并继续程序；若一段时间后未出现，则退出程序(关闭窗口)：
Timeout = 20 # 等待的最长时间(s)
ExampleXPath = "/html/body/div/div/" # 某元素的XPath
WebDriverWait(driver, Timeout).until(lambda driver: driver.find_element(By.XPATH, ExampleXPath)) 
# 暂停操作20s，并每隔500ms扫描一次该元素是否出现。出现该元素时结束扫描，并继续程序；若20s后未出现，则退出程序(关闭窗口)

# 拖动某个元素
ExampleXPath = "/html/body/div/div/" # 欲拖动的某元素的XPath
x = 100 # 欲拖动的相对x位移(左负右正) 单位像素(px)
y = 100 # 欲拖动的相对y位移(下负上正) 单位像素(px)
ActionChains(driver).click_and_hold(driver.find_element(By.XPATH, ExampleXPath)).move_by_offset(x, y).release().perform() # 拖动某个元素向右100像素和向下100像素
```

### 关于 DdddOcr | About DdddOcr

DdddOcr是由开发者`sml2h3`和`kerlomz`开发，基于神经网络训练，用于验证码识别的Python第三方库。

[DdddOcr在Github上以MIT协议开源](https://github.com/sml2h3/ddddocr)。

详细的DdddOcr使用帮助参照[这里](https://github.com/sml2h3/ddddocr)

针对常见的滑块验证码和字符识别验证码，参见下例：
#### 1. 字符识别验证码
```python
RecaptchaXPath = "/html/body/..." # 验证码图片的XPath
recaptcha = driver.find_element(By.XPATH, RecaptchaXPath) # 找到验证码图片，并赋值给变量recaptcha

driver.save_screenshot("./screenshot.png") # 获取页面截图，并保存到同目录下的screenshot.png
screenshot = Image.open('./screenshot.png') # 打开页面截图，赋值给变量screenshot

# 获取验证码图片在屏幕上的绝对坐标
# (x1, y1)是图片左上角相对屏幕左上角的坐标
# (x2, y2)是图片右下角相对屏幕左上角的坐标
# 向右为x坐标正方向，向下为y坐标正方向
x1 = recaptcha.location['x']
y1 = recaptcha.location['y']
x2 = recaptcha.location['x'] + recaptcha.size['width']
y2 = recaptcha.location['y'] + recaptcha.size['height']

cropped = screenshot.crop((x1, y1, x2, y2))  # 对获取的截图进行裁剪
cropped.save('./cropped.png')  # 保存裁剪后的图片到同目录下的cropped.png

ocr = ddddocr.DdddOcr()  # 初始化DdddOcr，字符识别模式
with open("./cropped.png", "rb") as f:
    img_bytes = f.read()
result = ocr.classification(img_bytes)  # 识别验证码，并赋给result

# ocr.classification()返回的类型，即result的类型是字符串
# result可以直接用于Selenium中文本的输入，如：
driver.find_element(By.ID, ExampleID).send_keys(result)
```

#### 2. 滑块验证码
```python
滑块验证码需要两张图片。一张是移动的滑块，一张是被扣除的背景图。
BackgroundXPath = "/html/body/..." # 验证码背景的XPath
background = driver.find_element(By.XPATH, BackgroundXPath) # 找到验证码背景图片，并赋值给变量background

SliderXPath = "/html/body/..." # 滑块的XPath
slider = driver.find_element(By.XPATH, BackgroundXPath) # 找到滑块图片，并赋值给变量slider

driver.save_screenshot("./screenshot.png") # 获取页面截图，并保存到同目录下的screenshot.png
screenshot = Image.open('./screenshot.png') # 打开页面截图，赋值给变量screenshot

# 获取滑块和验证码背景图片在屏幕上的绝对坐标
backgroundx1 = background.location['x'] + slider.size['width'] # "+ slider.size['width']"的作用是从滑块右侧开始截图，否则会将结果识别为原本的滑块，而非被扣除的区域。
backgroundy1 = background.location['y']
backgroundx2 = background.location['x'] + background.size['width']
backgroundy2 = background.location['y'] + background.size['height']

sliderx1 = slider.location['x']
slidery1 = slider.location['y']
sliderx2 = slider.location['x'] + slider.size['width']
slidery2 = slider.location['y'] + slider.size['height']


backgroundImage = screenshot.crop((backgroundx1, backgroundy1, backgroundx2, backgroundy2))  # 对获取的截图进行裁剪，得到滑块背景
backgroundImage.save('./background.png')  # 保存裁剪后的图片到同目录下的cropped.png

sliderImage = screenshot.crop((sliderx1, slidery1, sliderx2, slidery2))  # 对获取的截图进行裁剪，得到滑块背景
sliderImage.save('./slider.png')  # 保存裁剪后的图片到同目录下的cropped.png

ocr = ddddocr.DdddOcr(det = True)  # 初始化DdddOcr，滑块模式
with open("./slider.png", "rb") as f:
    slider_bytes = f.read()
with open("./background.png", "rb") as f:
    background_bytes = f.read()
    
result = ocr.classification(slider_bytes, background_bytes, simple_target = True)  # 识别验证码，并赋给result

# ocr.classification()返回的类型，即result的类型形如：{'target_y': 0, 'target': [82, 67, 153, 138]}
# 其中的四元列表代表识别到的被扣除区域的x1, y1, x2, y2
# result不可以直接用于Selenium中滑块的滑动
# 需要用result['target'][0] + slider.size['width']转换为Integer整数类型并补齐截图时除去的slider.size['width']。如：
move.click_and_hold(driver.find_element(By.XPATH, SliderXPath)).move_by_offset(result['target'][0] + slider.size['width'], 0).release().perform()
```
