#!/usr/bin/env python
# coding=gb2312

# ��ģ����Ҫ�ṩץͼ���ܣ�֧����������ץͼ��ʽ��
# ��ݼ� �Զ��� ctrl + alt + z
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
    # ����QQ��ͼ��DLL��ɽ�ͼ���ܣ������
    try:
        # ����QQץͼʹ�õ�dll
        dll_handle = ctypes.cdll.LoadLibrary('CameraDll.dll')

    except Exception:
        try:
            # ���dll����ʧ�ܣ����ַ���ʹ�ã�ֱ�����У������ʧ�ܣ��˳�
            os.system("Rundll32.exe CameraDll.dll, CameraSubArea")
        except Exception:
            return
    else:
        try:
            # ����dll�ɹ��������ץͼ������ע:û�з����������������Ĳ�������
            # �����ͣ����Դ����ִ�к�ᱨ����ȱ��4���ֽڣ�����Ӱ��ץͼ���ܣ���
            # ��ֱ�Ӻ�����Щ�쳣
            dll_handle.CameraSubArea(0)
        except Exception:
            im = ImageGrab.grabclipboard()
            key = str(uuid.uuid4())
            save_pic(im, key + '.png')
            return


# ʹ���ļ��Կ򣬱���ͼƬ
def save_pic(pic, filename='δ����ͼƬ.png'):
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
