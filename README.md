# Zijing-Guest
THSS software engineering course project

backend start(develop only):

python manage.py runserver_plus --cert-file certificate.crt --key-file certificate.key 0.0.0.0:8000

## Code Style
### Frontend
https://vuejs.org/v2/style-guide/

变量名：全小写+下划线。

函数：驼峰；组件：全小写+短横杠‘-’。

如果使用了组件/模板，且修改不多，可以按照它作者的规范。

使用eslint进行检查

### Backend
变量命名：全小写,下划线连接。

函数命名：全小写，下划线连接。

try,except处理异常。

缩进4个空格。

## Branch Usage
### main
stable released version. Allowed commit: meeting minutes, update Readme
### develop(Default)
newest iteration version. Allowed commit: bug fix

host: https://c02.whiteffire.cn:8000

**Write your code in branches below. After passing tests, create a new PR to develop**



## Interface Document
https://c02.whiteffire.cn:8000/swagger
