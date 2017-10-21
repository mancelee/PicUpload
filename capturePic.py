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
