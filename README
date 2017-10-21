# python 实现图片自动上传七牛返回地址
> 使用markdown编写文件，图片插入一直不太方便，有些markdown编辑器实现的图片插入并且自动上传的功能，但是大多要收费，免费的又存在各种限制，不能自定义图床，不够灵活等，本文利用Python这一灵活的脚本语言实现图片自动上传功能并返回图片的云端地址。（采用的图片服务器为七牛）

---

## 安装python依赖 ##

```python
pip install qiniu
pip install pillow
pip install pypiwin32
```
下载[win32clipboard](https://sourceforge.net/projects/pywin32/),直接点击安装

## 配置CameraDll.dll ##
下载CameraDll.dll以及注册.bat，双击**注册.bat** ，将其加入到系统环境中
[下载地址]()

## 编写python脚本 ##
```python
#!/usr/bin/env python
# coding=gb2312

# 此模块主要提供抓图功能，支持以下三种抓图方式：
# 快捷键 自定义 ctrl + alt + z
# ********************************************

import ctypes
import ctypes.wintypes
import os
import uuid

import win32con
import win32clipboard as w
import wx
from PIL import ImageGrab

from qiniu import Auth, put_file


def capture_choose_windows():
    # 利用QQ截图的DLL完成截图功能（借鉴）
    try:
        # 加载QQ抓图使用的dll
        dll_handle = ctypes.cdll.LoadLibrary('CameraDll.dll')

    except Exception:
        try:
            # 如果dll加载失败，则换种方法使用，直接运行，如果还失败，退出
            os.system("Rundll32.exe CameraDll.dll, CameraSubArea")
        except Exception:
            return
    else:
        try:
            # 加载dll成功，则调用抓图函数，注:没有分析清楚这个函数带的参数个数
            # 及类型，所以此语句执行后会报参数缺少4个字节，但不影响抓图功能，所
            # 以直接忽略了些异常
            dll_handle.CameraSubArea(0)
        except Exception:
            im = ImageGrab.grabclipboard()
            key = str(uuid.uuid4())
            save_pic(im, key + '.png')
            return


# 使用文件对框，保存图片
def save_pic(pic, filename='未命令图片.png'):
    app = wx.App()

    wildcard = "PNG(*.png)|*.png"
    dialog = wx.FileDialog(None, "Select a place", os.getcwd(),
                           filename, wildcard)
    if dialog.ShowModal() == wx.ID_OK:
        pic.save(dialog.GetPath().encode('gb2312'))
        upload_pic(filename, dialog.GetPath().encode('gb2312'))
    else:
        pass

    dialog.Destroy()


def upload_pic(key, path):
    access_key = '****************************************'
    secret_key = '****************************************'
    q = Auth(access_key, secret_key)
    bucket_name = 'myimage'
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_file(token, key, path)
    if info.status_code == 200:
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_TEXT, '![DESC](http://********.bkt.clouddn.com/' + str(key)+')')
        w.CloseClipboard()


if __name__ == "__main__":
    capture_choose_windows()

```
## 编写bat脚本自动运行python文件 ##
```bat
@echo off
D:
cd D:\python
start pythonw test.py
exit
```
保存为upPic.bat,右键发送桌面快捷方式
<center>
![给快捷方式设置快捷键](http://oltxnove0.bkt.clouddn.com/15e5422d-25ad-4b36-8213-e2206d8d77f9)</center>
