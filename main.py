import random
import importlib.util
import math
import time
import re

import os
import streamlit as st
import streamlit.components.v1 as components

st.title("일본어 단어 연습기")
st.write("오늘 하루도 열심히 단어 연습해 봅시다!")

BASE_PATH = "data"

# 1. data 안에 있는 폴더 이름 리스트로 반환
def get_subfolders(base_path=BASE_PATH):
    return [name for name in sorted(os.listdir(base_path))
            if os.path.isdir(os.path.join(base_path, name))and not name.startswith("__")]

# 2. data 안의 특정 폴더의 .py 파일들을 모듈로 가져오기
def import_modules_from_folder(folder_name):
    folder_path = os.path.join(BASE_PATH, folder_name)
    modules = {}

    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".py") and not file.startswith("__"):
            file_path = os.path.join(folder_path, file)
            module_name = f"{file[:-3]}"  # 확장자 제거

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            modules[module_name] = module

    return modules



words_category = get_subfolders()

if "step" not in st.session_state:
    st.session_state["step"] = 1



# 값이 설정되었는지 확인
if st.session_state["step"] == 1:

    st.markdown(
    """
    <style>
    button {
        animation: fadeIn 0.5s ease-in-out forwards;
        opacity: 0;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    

    for i in words_category:
        files = import_modules_from_folder(i)
        st.write(f"* {i}")
        files_names = list(files.keys())
        file_order = 1

        for k in files_names:
            time.sleep(0.05)
            if files[k].order != file_order:
                st.markdown("")
                file_order = files[k].order
            if st.button(f"{files[k].name}", key=f"button_{k}"):
                st.session_state["file_name"] = files[k].name
                st.session_state["step"] = 2
                st.session_state["the_file"] = files[k]
                st.rerun()

    
    st.write("---------------------------------------------")
    if st.button("거리 측정기"):
        st.session_state["step"] = 999
        st.rerun()

elif st.session_state["step"] == 2:
    st.markdown(
    """
    <style>
    button {
        animation: fadeIn 0.5s ease-in-out forwards;
        opacity: 0;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    the_file = st.session_state["the_file"]
    file_name = st.session_state["file_name"]

    st.success(f"[{file_name}]를 선택하셨습니다!")
    
    dict_count = sum(
        1 for k, v in vars(the_file).items()
        if isinstance(v, dict) and not k.startswith("_")
    )
    st.write(f"단어장 번호를 선택해주세요")


    dict_count_divided_by_4 = (dict_count) // 4
    dict_count_divided_by_4_rest = (dict_count) % 4

    if st.button("전체 단어", use_container_width=True):
            st.session_state["dic_num"] = "all"
            st.session_state["step"] = 3
            st.rerun()

    col_dict = {}

    for i in range(dict_count_divided_by_4):
        col1, col2, col3, col4 = st.columns(4) 
        col_dict[i] = col1, col2, col3, col4

    
    for i in range(dict_count_divided_by_4):
        m = 1
        for k in col_dict[i]:
            with k:
                if st.button(f"{i*4+m}번 단어장", key=f"{i*4+m}", use_container_width=True):
                    st.session_state["dic_num"] = i*4+m - 1 
                    st.session_state["step"] = 3
                    st.rerun()
            m = m + 1

    col1, col2, col3, col4 = st.columns(4) 
    col_list = [col1, col2, col3, col4]

    for i in range(dict_count_divided_by_4_rest):
        with col_list[i]:
            if st.button(f"{dict_count_divided_by_4*4+i+1}번 단어장", key=f"{dict_count_divided_by_4*4+i+1}", use_container_width=True):
                st.session_state["dic_num"] = dict_count_divided_by_4*4+i
                st.session_state["step"] = 3
                st.rerun()
    
elif st.session_state["step"] == 3:
    st.markdown("""
    <style>
    div.stButton > button {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        height: 2.5em;
    }
    </style>
""", unsafe_allow_html=True)
    st.markdown(
    """
    <style>
    button {
        animation: fadeIn 0.5s ease-in-out forwards;
        opacity: 0;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    the_file = st.session_state["the_file"]
    dic_num = st.session_state["dic_num"]

    st.session_state["auto_state"] = "auto"

    
    selected_file = the_file
    dict_list = [val for name, val in vars(selected_file).items()
    if not name.startswith("__") and isinstance(val, dict)]
    
    if dic_num == "all":
        all_dict = {}

        for i in dict_list:
            all_dict = all_dict | i

        st.session_state["dict"] = all_dict
        st.session_state["dict_keys"] = list(all_dict.keys())
        st.session_state["dict_length"] = len(all_dict.keys())
        st.session_state["perm_dict_length"] = len(all_dict.keys())
        dict_length = st.session_state["dict_length"]
    else:
        st.session_state["dict"] = dict_list[dic_num]
        st.session_state["dict_keys"] = list(dict_list[dic_num].keys())
        st.session_state["dict_length"] = len(dict_list[dic_num].keys())
        st.session_state["perm_dict_length"] = len(dict_list[dic_num].keys())
        dict_length = st.session_state["dict_length"]

    st.session_state["now_word_number"] = 1

    if the_file.type == "word":
        # 3등분된 열 생성
        col1, col2, col3, col4 = st.columns(4)

        # 각 열에 버튼 배치
        with col1:
            if st.button("기본", use_container_width=True):
                st.session_state["step"] = 4
                st.session_state["word_type"] = 0
                st.rerun()
        with col2:
            if st.button("단어만", use_container_width=True):
                st.session_state["step"] = 4
                st.session_state["word_type"] = 1
                st.rerun()
        with col3:
            if st.button("히라가나만", use_container_width=True):
                st.session_state["step"] = 4
                st.session_state["word_type"] = 2
                st.rerun()
        with col4:
            if st.button("랜덤", use_container_width=True):
                st.session_state["step"] = 4
                st.session_state["word_type"] = 3
                st.rerun()


        col1, col2, col3, col4 = st.columns(4)

        # 각 열에 버튼 배치
        with col1:
            if st.button("기본 (괄호제거)", use_container_width=True):
                st.session_state["step"] = 4
                st.session_state["word_type"] = 4
                st.rerun()
        with col2:
            if st.button("단어만 (괄호제거)", use_container_width=True):
                st.session_state["step"] = 4
                st.session_state["word_type"] = 5
                st.rerun()
        with col3:
            if st.button("히라가나만 (괄호제거)", use_container_width=True):
                st.session_state["step"] = 4
                st.session_state["word_type"] = 6
                st.rerun()
        with col4:
            if st.button("랜덤 (괄호제거)", use_container_width=True):
                st.session_state["step"] = 4
                st.session_state["word_type"] = 7
                st.rerun()

       
    else:
        st.session_state["word_type"] = 0
        st.session_state["step"] = 4
        st.rerun()


elif st.session_state["step"] == 4:
    the_file = st.session_state["the_file"]
    dic_num = st.session_state["dic_num"]

    dict = st.session_state["dict"]
    dict_keys = st.session_state["dict_keys"]
    dict_length = st.session_state["dict_length"]
    now_word_number = st.session_state["now_word_number"]
    perm_dict_length = st.session_state["perm_dict_length"]
    word_type = st.session_state["word_type"]
    
    auto_state = st.session_state["auto_state"]


    if len(dict_keys) == 0:
        st.session_state["step"] = 6
        st.rerun()


    words_random_int = random.randrange(0, len(dict_keys))
    now_key = dict_keys[words_random_int]

    temp_now_key = now_key

    if the_file.type == "word":
        if "[" in now_key:
            if word_type >= 4:
                temp_now_key = re.sub(r'\[[^\[\]]*\]', '', now_key)

        if "(" in now_key:
            if word_type == 0 or word_type == 4:
                head, tail = temp_now_key.split("(", 1) 
                tail = "<span style='display: inline-block; max-width: 100%; word-break: break-word;'>(" +tail + "</span>"
            elif word_type == 1 or word_type == 5:
                head, tail = temp_now_key.split("(", 1) 
                tail = ""
            elif word_type == 2 or word_type == 6:
                head, tail = temp_now_key.split("(", 1) 
                head = ""
                tail = tail[:-1]
                tail = "<span style='display: inline-block; max-width: 100%; word-break: break-word;'>" +tail + "</span>"
            elif word_type == 3 or word_type == 7:
                temp = random.choice([0, 1])
                if temp == 0:
                    head, tail = temp_now_key.split("(", 1) 
                    tail = ""
                elif temp == 1:
                    head, tail = temp_now_key.split("(", 1) 
                    head = ""
                    tail = tail[:-1]
                    tail = "<span style='display: inline-block; max-width: 100%; word-break: break-word;'>" +tail + "</span>"
        else:
            head = now_key
            tail = ""
    else:
        if "(" in now_key:
            head, tail = temp_now_key.split("(", 1) 
            tail = ""
        else:
            head = temp_now_key
            tail = ""
    

    if dic_num == "all":
        st.markdown(f'<p style="text-align:center; font-size:20px;">[ {the_file.name} 전체 ]</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p style="text-align:center; font-size:20px;">[ {the_file.name}   {dic_num+1} ]</p>', unsafe_allow_html=True)



    st.markdown(f'<p style="text-align:center; font-size:30px;">{now_word_number}/{perm_dict_length}</p>', unsafe_allow_html=True)
    st.markdown(f'''<p style="text-align:center; font-size:40px;">
    <span style="display: inline-block; max-width: 100%; word-break: break-word;">{head}</span>{tail}
</p>''', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; font-size:40px; visibility:hidden;">빈칸</p>', unsafe_allow_html=True)



    
    next_button = st.button("▶ 다음 단어", key="next_button", use_container_width=True)

    del dict_keys[words_random_int]
    st.session_state["dict_keys"] = dict_keys
    st.session_state["dict_length"] = dict_length - 1
    st.session_state["now_key"] = now_key




    st.session_state["step"] = 5





        
elif st.session_state["step"] == 5:
    the_file = st.session_state["the_file"]

    dic_num = st.session_state["dic_num"]

    dict = st.session_state["dict"]
    now_key = st.session_state["now_key"]
    dict_length = st.session_state["dict_length"]
    now_word_number = st.session_state["now_word_number"]
    perm_dict_length = st.session_state["perm_dict_length"]
    word_type = st.session_state["word_type"]

    auto_state = st.session_state["auto_state"]


    if the_file.type == "word":
        if "(" in now_key:
            head, tail = now_key.split("(", 1) 
            tail = "<span style='display: inline-block; max-width: 100%; word-break: break-word;'>(" +tail + "</span>"
        else:
            head = now_key
            tail = ""
    else:
        if "(" in now_key:
            head, tail = now_key.split("(", 1) 
            tail = "<span style='display: inline-block; max-width: 100%; word-break: break-word;'>(" +tail + "</span>"
        else:
            head = now_key
            tail = ""


    if dic_num == "all":
        st.markdown(f'<p style="text-align:center; font-size:20px;">[ {the_file.name} 전체 ]</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p style="text-align:center; font-size:20px;">[ {the_file.name}   {dic_num+1} ]</p>', unsafe_allow_html=True)

    st.markdown(f'<p style="text-align:center; font-size:30px;">{now_word_number}/{perm_dict_length}</p>', unsafe_allow_html=True)
    st.markdown(f'''<p style="text-align:center; font-size:40px;">
    <span style="display: inline-block; max-width: 100%; word-break: break-word;">{head}</span>{tail}
</p>''', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; font-size:40px;">{dict[now_key]}</p>', unsafe_allow_html=True)



    next_button = st.button("▶ 다음 단어", key="next_button", use_container_width=True)

    # 버튼이 클릭되었을 때 상태 전환
    
    st.session_state["now_word_number"] = now_word_number + 1


    st.session_state["step"] = 4

 


    
elif st.session_state["step"] == 6:
    perm_dict_length = st.session_state["perm_dict_length"]
    the_file = st.session_state["the_file"]
    dic_num = st.session_state["dic_num"]

    if the_file.type == "word":
        type = "단어"
    elif the_file.type == "sentence":
        type = "문장"

    if isinstance(dic_num, int):
        real_dic_num = dic_num + 1
    else:
        real_dic_num = "전체"

    st.markdown(f"""
<div style="
    background-color: #d4edda;
    color: #155724;
    padding: 15px;
    border-radius: 5px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    border: 1px solid #c3e6cb;">
    수고하셨습니다!
</div>
""", unsafe_allow_html=True)
    st.write("")
    st.markdown(f"""
<div style="
    background-color: #d4edda;
    color: #155724;
    padding: 15px;
    border-radius: 5px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    border: 1px solid #c3e6cb;">
    [{the_file.name}] <br>
    단어장 {real_dic_num} <br>
    {perm_dict_length}개의 {type}
</div>
""", unsafe_allow_html=True)
    st.balloons()

    st.write("")
    clicked = st.button("다른 단어장 연습하기", use_container_width=True)
     
    if clicked:
        st.session_state["step"] = 1
        st.rerun()

         
elif st.session_state["step"] == 999:
    dist = st.number_input("직선 거리", step=1, format="%d")
    angle = st.number_input("각도", step=1, format="%d")

    if st.button("입력"):
        radian = math.radians(angle)
        
        print(dist, angle)

        # 사인과 코사인 값 구하기
        st.session_state["horizontal_dist"] = dist * math.cos(radian)
        st.session_state["vertical_dist"] = dist * math.sin(radian)
        
        st.session_state["step"] = 998
        st.rerun()

elif st.session_state["step"] == 998:
    horizontal_dist = round(st.session_state["horizontal_dist"], 2)
    vertical_dist = round(st.session_state["vertical_dist"], 2)
    
    st.write(f"수평 거리 : {horizontal_dist}m")
    st.write(f"수직 거리 : {vertical_dist}m")