# coding=utf-8
import dlib          # 人脸处理的库 Dlib
import numpy as np   # 数据处理的库 numpy
import cv2           # 图像处理的库 OpenCv
import pandas as pd  # 数据处理的库 Pandas
from skimage import io

# 人脸识别模型，提取128D的特征矢量
# face recognition model, the object maps human faces into 128D vectors
# Refer this tutorial: http://dlib.net/python/index.html#dlib.face_recognition_model_v1
facerec = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


# 计算两个128D向量间的欧式距离
# compute the e-distance between two 128D features
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


# 处理存放所有人脸特征的 csv
path_features_known_csv = "data/data_faces_from_camera/features_all.csv"
csv_rd = pd.read_csv(path_features_known_csv, header=None)
# 所有人脸的csv_rd特征： csv_rd如下
#         0         1         2    ...       125       126       127
# 0 -0.041625  0.128115  0.029375  ...  0.025229  0.149856 -0.011032
# 1 -0.049821  0.138014  0.027642  ...  0.015095  0.148459 -0.008056


# 用来存放所有录入人脸特征的数组
# the array to save the features of faces in the database
features_known_arr = []


# 读取已知人脸数据
# print known faces
for i in range(csv_rd.shape[0]):
    features_someone_arr = []
    for j in range(0, len(csv_rd.ix[i, :])):
        features_someone_arr.append(csv_rd.ix[i, :][j])
    features_known_arr.append(features_someone_arr)
# features_known_arr 为一个数组嵌套数组，每个对象保存着每个人的128个特征，此数组长度为人脸个数
print("数据库中人脸个数为", len(features_known_arr))


# Dlib 检测器和预测器
# The detector and predictor will be used
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')


# 读取单张彩色rgb图片,读取的图片以numpy数组形式计算
img_rd = io.imread("img_face_1.jpg")
# cv2.cvtColor(p1,p2) 是颜色空间转换函数，p1是需要转换的图片，p2是转换成何种格式。
# cv2.COLOR_BGR2RGB 将BGR格式转换成RGB格式
img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
# 人脸检测器
# 参数为检验对象和采样次数
faces = detector(img_gray, 1)

# 检测到人脸 when face detected
if len(faces) != 0:
    # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
    features_cap_arr = []
    for i in range(len(faces)):
        shape = predictor(img_rd, faces[i])
        features_cap_arr.append(facerec.compute_face_descriptor(img_rd, shape))

    # 遍历捕获到的图像中所有的人脸
    for k in range(len(faces)):
        # 对于某张人脸，遍历所有存储的人脸特征
            # for every faces detected, compare the faces in the database
            e_distance_list = []
            for i in range(len(features_known_arr)):
                # 如果 person_X 数据不为空
                if str(features_known_arr[i][0]) != '0.0':
                    print("with person", str(i + 1), "the e distance: ", end='')
                    e_distance_tmp = return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                    print(e_distance_tmp)
                    e_distance_list.append(e_distance_tmp)
                else:
                    # 空数据 person_X
                    e_distance_list.append(999999999)
            # Find the one with minimum e distance
            similar_person_num = e_distance_list.index(min(e_distance_list))
            print("Minimum e distance with person", int(similar_person_num)+1)

            if min(e_distance_list) < 0.4:
                print("true")
            else:
                print("Unknown person")
