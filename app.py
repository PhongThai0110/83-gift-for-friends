import streamlit as st
import json
import time
import os
from PIL import Image
import base64
import streamlit.components.v1 as components
# Hàm để mã hóa ảnh cục bộ sang base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Hàm tạo style cho nền web bằng ảnh
def set_png_as_page_bg(bin_file):
    bin_str = get_base64_of_bin_file(bin_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Thêm một lớp phủ mờ để chữ và hộp quà dễ nhìn hơn */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(255, 245, 247, 0.3); 
        z-index: -1;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
# Giả sử ảnh của bạn tên là background.jpg nằm trong assets/images/
set_png_as_page_bg('assets/image/background.jpg')
# 1. CẤU HÌNH TRANG (UX: Tiêu đề và icon hiển thị trên tab trình duyệt)
st.set_page_config(page_title="Hộp Quà Bí Mật 8/3", page_icon="🎁", layout="centered")
# Thêm đoạn này vào file app.py của bạn (ngay dưới st.set_page_config)
def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Gọi hàm đọc file CSS
local_css("assets/css/style.css")
# 2. KHỞI TẠO SESSION STATE (Quản lý trạng thái các màn chơi)
if 'stage' not in st.session_state:
    st.session_state.stage = 0 # 0: Nhập mã, 1: Thử thách 1, 2: Thử thách 2, 3: Thử thách 3, 4: Mở quà
if 'energy' not in st.session_state:
    st.session_state.energy = 0
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_msg' not in st.session_state:
    st.session_state.user_msg = ""

# 3. HÀM HỖ TRỢ ĐỌC DỮ LIỆU
def load_messages():
    try:
        with open('data/messages.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_image_path(img_name):
    # Lấy đường dẫn an toàn đến thư mục assets
    return os.path.join("assets", "image", img_name)

# 4. GIAO DIỆN CHÍNH
st.markdown("<h1 style='text-align: center; color: #D81B60;'>✨ Trạm Giải Mã Mùng 8/3 ✨</h1>", unsafe_allow_html=True)

# Hiển thị ảnh hộp quà (Căn giữa bằng st.columns)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.stage < 4:
        try:
            st.image(get_image_path("locked_box.png"), use_container_width=True)
        except:
            st.info("*(Chưa tìm thấy ảnh locked_box.png trong assets/images)*")
    else:
        try:
            st.image(get_image_path("opened_box.png"), use_container_width=True)
        except:
            st.info("*(Chưa tìm thấy ảnh opened_box.png trong assets/images)*")

st.divider()

# ==========================================
# MÀN 0: NHẬP MÃ BÍ MẬT
# ==========================================
if st.session_state.stage == 0:
    st.markdown("<h3 style='text-align: center;'>Nhập mã bí mật để bắt đầu:</h3>", unsafe_allow_html=True)
    secret_code = st.text_input("Mã của bạn:", type="password", help="Hỏi người gửi nếu bạn không biết mã nhé!")
    
    if st.button("Mở khóa 🚀", use_container_width=True):
        messages = load_messages()
        code_lower = secret_code.strip().lower()
        
        # Kiểm tra mã
        if code_lower in messages:
            st.session_state.user_name = messages[code_lower]["name"]
            st.session_state.user_msg = messages[code_lower]["message"]
        else:
            # Rơi vào trường hợp default nếu nhập sai
            st.session_state.user_name = messages.get("default", {}).get("name", "Bạn hiền")
            st.session_state.user_msg = messages.get("default", {}).get("message", "Chúc bạn 8/3 vui vẻ!")
        
        st.session_state.stage = 1
        st.rerun()

# ==========================================
# MÀN 1: THỬ THÁCH SỐ 8
# ==========================================
elif st.session_state.stage == 1:
    st.subheader(f"👋 Chào bạn!")
    st.write("**Thử thách 1:** Từ 1 đến 10, bạn hãy nghĩ xem con số nào là biểu tượng của ngày quốc tế phụ nữ?")
    
    slider_val = st.slider("Chọn một con số:", min_value=1, max_value=10, value=1)
    
    if slider_val == 8:
        st.success("Tuyệt vời! Bạn đã vượt qua thử thách đầu tiên.")
        if st.button("Tiếp tục ➡️"):
            st.session_state.stage = 2
            st.rerun()
    else:
        st.warning("Gợi ý: Ngày lễ này diễn ra vào đầu tháng 3 đó!")

# ==========================================
# MÀN 2: CÂU HỎI TRẮC NGHIỆM
# ==========================================
elif st.session_state.stage == 2:
    st.write("**Thử thách 2:** Trả lời câu hỏi hóc búa sau đây:")
    st.write("Vì sao phụ nữ luôn đúng?")
    
    answer = st.radio(
        "Chọn đáp án chuẩn nhất:",
        ("A. Vì khoa học chứng minh thế.", 
         "B. Vì họ có giác quan thứ 6.", 
         "C. Đơn giản vì họ là phụ nữ, không có nhưng!", 
         "D. Tớ không biết.")
    )
    
    if st.button("Chốt đáp án 🔒"):
        if answer.startswith("C"):
            st.success("Chính xác! Chân lý không bao giờ sai. Đi tiếp thôi!")
            time.sleep(1) # Tạo độ trễ nhỏ để UX mượt hơn
            st.session_state.stage = 3
            st.rerun()
        else:
            st.error("Sai rồi! Hãy suy nghĩ lại về 'quyền năng' tối thượng đi nào!")

# ==========================================
# MÀN 3: TRUYỀN NĂNG LƯỢNG MỞ HỘP
# ==========================================
elif st.session_state.stage == 3:
    st.write("**Thử thách cuối cùng:** Chiếc hộp cần một chút tình yêu để tự mở nắp. Hãy nhấn nút dưới đây đủ 3 lần!")
    
    # Hiển thị thanh tiến trình năng lượng
    progress = st.progress(st.session_state.energy * 33)
    
    if st.button("⚡ Truyền Năng Lượng ⚡", use_container_width=True):
        st.session_state.energy += 1
        if st.session_state.energy >= 3:
            st.session_state.stage = 4
            st.rerun()
        else:
            st.rerun() # Load lại thanh tiến trình

# ==========================================
# MÀN 4: PHẦN THƯỞNG & THIỆP CHÚC MỪNG
# ==========================================
elif st.session_state.stage == 4:
    # Hiệu ứng nổ bóng bay và rớt tuyết
    st.balloons()
    st.snow()
    
    st.success("🎉 CHIẾC HỘP ĐÃ MỞ THÀNH CÔNG! 🎉")
    
    # CSS Nội tuyến để tạo một tấm thiệp lộng lẫy
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #ffe6ea 100%);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(216, 27, 96, 0.2);
        text-align: center;
        margin-top: 20px;
        border: 2px solid #FF7A9A;
    ">
        <h2 style="color: #D81B60; margin-bottom: 20px;">Gửi {st.session_state.user_name} 🌷</h2>
        <p style="color: #5C102A; font-size: 18px; line-height: 1.6; font-weight: 500;">
            {st.session_state.user_msg}
        </p>
        <hr style="border-top: 1px dashed #FF7A9A; margin: 20px 0;">
        <p style="color: #FF7A9A; font-style: italic; font-size: 14px;">
            Món quà công nghệ được code riêng tặng cậu! ❤️
        </p>
    </div>
    """
    heart_html = f"""
<style>
    canvas {{
        position: absolute;
        width: 100%;
        height: 100%;
    }}
    .heart-container {{
        position: relative; 
        height: 500px; 
        width: 100%; 
        background: transparent; 
        display: flex; 
        justify-content: center; 
        align-items: center;
    }}
    /* Hiệu ứng đập cho trái tim */
    #pinkboard {{
        animation: animate 1.3s infinite;
    }}
    @keyframes animate {{
        0% {{ transform: scale(1); }}
        30% {{ transform: scale(.8); }}
        60% {{ transform: scale(1.1); }}
        100% {{ transform: scale(1); }}
    }}
    .name-overlay {{
        position: absolute; 
        z-index: 10; 
        color: white; 
        /* Sử dụng font chữ mềm mại hơn hoặc font máy đánh chữ nếu muốn chất công nghệ */
        font-family: 'Courier New', cursive; 
        /* Hiệu ứng hào quang đa tầng (Neon Glow) */
        text-shadow: 
            0 0 5px #fff, 
            0 0 10px #FF7A9A, 
            0 0 20px #FF7A9A, 
            0 0 40px #FF7A9A;
        font-size: 2.8em; /* Tăng kích thước một chút cho nổi bật */
        font-weight: bold;
        text-align: center;
        /* Nghiêng nhẹ 5-7 độ để tạo cảm giác nghệ thuật, bớt cứng nhắc */
        transform: rotate(-7deg); 
        pointer-events: none;
        width: 100%;
    }}
</style>

<div class="heart-container">
    <canvas id="pinkboard"></canvas>
    <h1 class="name-overlay">{st.session_state.user_name}</h1>
</div>

<script>
    /* Logic JS được đọc trực tiếp từ file của bạn */
    {open('8_3chocacce.html', 'r', encoding='utf-8').read().split('<script>')[1].split('</script>')[0]}
</script>
"""
    
    # Hiển thị trái tim
    components.html(heart_html, height=550)

    # Hiển thị tấm thiệp
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Nút chơi lại từ đầu
    st.write("")
    if st.button("🔄 Khóa hộp lại"):
        st.session_state.stage = 0
        st.session_state.energy = 0
        st.rerun()