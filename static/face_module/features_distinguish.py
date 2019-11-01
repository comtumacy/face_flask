# coding=utf-8
import dlib          # 人脸处理的库 Dlib
import numpy as np   # 数据处理的库 numpy
import cv2           # 图像处理的库 OpenCv
from skimage import io
from templates.teacher.face_distinguish.get_student_features_sql import get_student_features_sql


# 计算两个128D向量间的欧式距离
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


def features_distinguish(table_name, Tno):
    # 用来存放所有录入人脸特征的数组
    features_known_arr = get_student_features_sql(table_name)
    print("数据库中人脸个数为", len(features_known_arr))

    # 人脸识别模型，提取128D的特征矢量
    facerec = dlib.face_recognition_model_v1("static/face_module/data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

    # Dlib 检测器和预测器
    # The detector and predictor will be used
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('static/face_module/data/data_dlib/shape_predictor_68_face_landmarks.dat')

    # 读取单张彩色rgb图片,读取的图片以numpy数组形式计算
    img_rd = io.imread('D:\\face\\static\\photo\\teacher\\{}.jpg'.format(Tno))
    # cv2.cvtColor(p1,p2) 是颜色空间转换函数，p1是需要转换的图片，p2是转换成何种格式。
    # cv2.COLOR_BGR2RGB 将BGR格式转换成RGB格式
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    # 人脸检测器
    # 参数为检验对象和采样次数
    faces = detector(img_gray, 1)

    # 检测到人脸
    if len(faces) != 0:
        # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
        features_cap_arr = []
        for i in range(len(faces)):
            shape = predictor(img_rd, faces[i])
            features_cap_arr.append(facerec.compute_face_descriptor(img_rd, shape))

        # 遍历捕获到的图像中所有的人脸
        for k in range(len(faces)):
            # 对于某张人脸，遍历所有存储的人脸特征
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
                similar_person_num = e_distance_list.index(min(e_distance_list))
                print("Minimum e distance with person", int(similar_person_num)+1)

                if min(e_distance_list) < 0.4:
                    return True, int(similar_person_num) + 1
                else:
                    return False, int(similar_person_num) + 1
