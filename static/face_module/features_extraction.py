# coding=utf-8
import cv2
import os
import dlib
from skimage import io
import numpy as np

# # 要读取人脸图像文件的路径
# path_images_from_camera = "data/data_faces_from_camera/"

# Dlib 正向人脸检测器
# 功能：人脸检测画框
# 参数：无
# 返回值：默认的人脸检测器
detector = dlib.get_frontal_face_detector()

# Dlib 人脸预测器
predictor = dlib.shape_predictor("static/face_module/data/data_dlib/shape_predictor_5_face_landmarks.dat")

# Dlib 人脸识别模型
# Face recognition model, the object maps human faces into 128D vectors
face_rec = dlib.face_recognition_model_v1("static/face_module/data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


# 返回单张图像的 128D 特征
def return_128d_features(path_img):
    # 读取单张彩色rgb图片,读取的图片以numpy数组形式计算
    img_rd = io.imread(path_img)
    # cv2.cvtColor(p1,p2) 是颜色空间转换函数，p1是需要转换的图片，p2是转换成何种格式。
    # cv2.COLOR_BGR2RGB 将BGR格式转换成RGB格式
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    # 人脸检测器
    # 参数为检验对象和采样次数
    faces = detector(img_gray, 1)

    print("检测到人脸的图像: {}".format(path_img))

    # 因为有可能截下来的人脸再去检测，就检测不出来人脸了
    # 所以要确保是 检测到人脸的人脸图像 再拿去算特征
    if len(faces) != 0:
        # 人脸预测器 predictor
        shape = predictor(img_gray, faces[0])
        # 人脸识别模型 face_rec
        face_descriptor = face_rec.compute_face_descriptor(img_gray, shape)
    else:
        face_descriptor = 0
        print("检测人脸失败")

    # 返回单个人脸特征face_descriptor
    return face_descriptor


# 将文件夹中照片特征提取出来
# path_faces_person为完整文件夹某人的照片文件夹路径
def return_features_mean_person(path_faces_person):
    features_list_person = []
    photos_list = os.listdir(path_faces_person)
    # photos_list为文件名，photo_list = ['img_face_1.jpg'...]
    if photos_list:
        for i in range(len(photos_list)):
            # 调用return_128d_features()得到128d特征
            print("正在读的人脸图像：", path_faces_person + "/" + photos_list[i])
            features_128d = return_128d_features(path_faces_person + "/" + photos_list[i])
            # 遇到没有检测出人脸的图片跳过
            if features_128d == 0:
                i += 1
            else:
                features_list_person.append(features_128d)
    else:
        print("文件夹内图像文件为空" + path_faces_person + '/')

    # 计算 128D 特征的均值
    # person 的 N 张图像 x 128D -> 1 x 128D
    if features_list_person:
        # axis=0表示输出矩阵是1行，也就是求每一列的平均值
        features_mean_person_np = np.array(features_list_person).mean(axis=0)
    else:
        features_mean_person_np = '0'

    # features_mean_person_np 某人照片特征，一个128长度的数组
    return features_mean_person_np


# features_mean_person = return_features_mean_person("../photo/201606401243")
# print("特征均值:", list(features_mean_person))
