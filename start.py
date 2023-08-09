import json
import random
from datetime import datetime
import os
from PIL import Image
import streamlit as st

st.title("Welcome to Our Questionnaire")
st.info("fill it well please,for Academic progress")
st.divider()

# 初始化
base = './data/UserStudy/'
if "lst1" not in st.session_state:  # 获取所有问卷
    st.session_state.lst1 = os.listdir("./data/UserStudy")


def init():
    for _key in st.session_state.keys():
        del st.session_state[_key]


# 页面渲染
st.markdown("你想填下面的哪个问卷呢？", True)
q_select = st.selectbox("↓↓↓",
                        st.session_state.lst1, on_change=init)  # 选择的问卷名为q_select
if q_select != "please choose questionnaire":
    f"你选择了 {q_select}."

if "index" not in st.session_state:  # 定义图片顺序
    st.session_state.index = 0

if q_select != "please choose questionnaire" and "imageA" not in st.session_state:  # 若问卷需要初始化且问卷已经选择，则获取图片
    st.session_state.imageA = os.listdir("./data/UserStudy/" + q_select + "/methodA/")
    st.session_state.imageB = os.listdir("./data/UserStudy/" + q_select + "/methodB/")
    st.session_state.imageOri = os.listdir("./data/UserStudy/" + q_select + "/GT_imgs/")
    st.session_state.imageGuide = os.listdir("./data/UserStudy/" + q_select + "/guide/")

    if "choose" not in st.session_state:  # 初始化用户选择结果
        st.session_state.choose = dict.fromkeys(range(len(st.session_state.imageA)))

if q_select != "please choose questionnaire" and "describe" not in st.session_state:  # 获取所有图片描述
    st.session_state.describe_list = []
    for line in open("./data/UserStudy/" + q_select + "/describe.txt", encoding='utf-8'):
        st.session_state.describe_list.append(line.strip('\n'))

st.divider()

# 图片内容
if q_select != "please choose questionnaire":
    st.markdown(st.session_state.describe_list[0])
    st.markdown("描述 ---> （ " + st.session_state.describe_list[st.session_state.index + 1] + " )",
                True)

r14c1, r14c2, r14c3 = st.columns([2, 2, 1])

if q_select != "please choose questionnaire" and "rand_list" not in st.session_state:  # 生成随机数，0——A组在左，1——A组在右
    st.session_state.rand_list = []
    for i in range(len(st.session_state.imageA)):
        st.session_state.rand_list.append(random.randint(0, 1))

if q_select == "please choose questionnaire" or "imageA" not in st.session_state:
    _1, r04c2, _2 = st.columns([1, 8, 1])
    with _1:
        pass
    with r04c2:
        st.image(Image.open(r"./data/占位.png"))
    with _2:
        pass

with r14c1:
    if q_select == "please choose questionnaire" or "imageA" not in st.session_state:
        pass
    else:
        st.markdown("<br>__*A组图片*__", True)
        if st.session_state.rand_list[st.session_state.index] == 0:
            st.image(Image.open(base + q_select + '/methodA/' + st.session_state.imageA[st.session_state.index]))
        else:
            st.image(Image.open(base + q_select + '/methodB/' + st.session_state.imageB[st.session_state.index]))

with r14c2:
    if q_select == "please choose questionnaire" or "imageB" not in st.session_state:
        pass
    else:
        st.markdown("<br>__*B组图片*__", True)
        if st.session_state.rand_list[st.session_state.index] == 1:
            st.image(Image.open(base + q_select + '/methodA/' + st.session_state.imageA[st.session_state.index]))
        else:
            st.image(Image.open(base + q_select + '/methodB/' + st.session_state.imageB[st.session_state.index]))

with r14c3:
    if q_select == "please choose questionnaire" or "imageOri" not in st.session_state:
        pass
    else:
        st.markdown("__*原图*__", True)
        st.image(Image.open(base + q_select + '/GT_imgs/' + st.session_state.imageOri[st.session_state.index]).resize(
            (128, 128), Image.BILINEAR))

    if q_select == "please choose questionnaire" or "imageGuide" not in st.session_state:
        pass
    else:
        st.markdown("__*引导图*__", True)
        st.image(Image.open(base + q_select + '/guide/' + st.session_state.imageGuide[st.session_state.index]).resize(
            (128, 128), Image.BILINEAR))


# 选择与提交
def judge_submit():
    for value in st.session_state.choose.values():
        if not value:
            return False
    return True


if q_select != "please choose questionnaire":

    r25c1, r25c2 = st.columns(2)
    # 选择逻辑改为——找A，将自身训练的图片放在methodA,若用户找到了真正的A，就记录√（表示我们效果更好）
    with r25c1:
        if st.button("A组更好"):
            if st.session_state.rand_list[st.session_state.index] == 0:
                st.session_state.choose[st.session_state.index] = "Y"
            else:
                st.session_state.choose[st.session_state.index] = "N"

        if judge_submit():
            st.success("你已经完成全部的问题了，可以提交了哦~")

    with r25c2:
        if st.button("B组更好"):
            if st.session_state.rand_list[st.session_state.index] == 1:
                st.session_state.choose[st.session_state.index] = "Y"
            else:
                st.session_state.choose[st.session_state.index] = "N"

        if judge_submit():
            st.success("你已经完成全部的问题了，可以提交了哦~")

    if st.session_state.choose[st.session_state.index]:
        if st.session_state.choose[st.session_state.index] == "Y" and st.session_state.rand_list[
            st.session_state.index] == 0 or st.session_state.choose[st.session_state.index] == "N" and \
                st.session_state.rand_list[st.session_state.index] == 1:
            st.markdown("**<div style='color:green'>↑↑↑ 本组你已经选择了A~</div>**", True)
        else:
            st.markdown("**<div style='color:green'>↑↑↑ 本组你已经选择了B~</div>**", True)
    else:
        st.markdown("**<div style='color:green'>↑↑↑ 本组你还没有做出公正的评判哦~</div>**", True)

    st.divider()


# 切换按钮
def _pre():
    if st.session_state.index != 0:
        st.session_state.index -= 1


def _next():
    if st.session_state.index != len(st.session_state.imageA) - 1:
        st.session_state.index += 1


if q_select != "please choose questionnaire":
    # st.markdown("**<div style='color:green'>下面是切换图片的按钮</div>**", True)
    r35c1, r35c2 = st.columns(2)
    with r35c1:
        if st.button("上一组",
                     key=None, help=None,
                     on_click=_pre, args=None,
                     kwargs=None):
            pass

    with r35c2:
        if st.button("下一组",
                     key=None, help=None,
                     on_click=_next, args=None,
                     kwargs=None):
            pass

    # 提交按钮
    r46c1, r46c2 = st.columns([1, 2])
    with r46c1:
        st.markdown("这是第 " + str(st.session_state.index + 1) + " 组，总共 " + str(len(st.session_state.imageA)) + " 组")
    with r46c2:
        if st.button("提交"):
            tmp = True
            for value in st.session_state.choose.values():
                if not value:
                    tmp = False
            if tmp:
                now = datetime.strftime(datetime.now(), '%m%d%H%M%S')
                fname = './result/' + now + 'joints.txt'
                with open(fname, 'a') as f:
                    f.write(q_select + " ")
                    f.write(json.dumps(st.session_state.choose))

                # 提交问卷初始化
                for key in st.session_state.keys():
                    del st.session_state[key]

                st.success("你成功提交了问卷！请选择别的问卷完成或退出页面~")
            else:
                st.error("你还有选项没有完成，不能提交哦~")
