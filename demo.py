import hashlib
import pyperclip
import time

def sha256_encrypt(text):
    """Mã hóa chuỗi đầu vào bằng SHA-256"""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(text.encode('utf-8'))
    return sha256_hash.hexdigest()

def process_string(s, special_chars="!@#$%^&*()"):
    # Tách phần chữ và số
    letters = [ch for ch in s if ch.isalpha()]
    digits = [ch for ch in s if ch.isdigit()]
    
    # Tổng độ dài mong muốn
    target_length = 23
    
    # Nếu tổng số ký tự vượt quá target_length, cắt bớt
    i = min(len(letters), len(digits))
    combined = [None] * (2 * i)
    combined[::2] = letters[:i]
    combined[1::2] = digits[:i]
    
    remaining = letters[i:] + digits[i:]
    combined.extend(remaining[:target_length - len(combined)])
    
    # Nếu vẫn thiếu, cắt bớt để đủ 26 ký tự
    combined = combined[:target_length]
    
    # Tính tổng list digits
    digit_sum = sum(int(d) for d in digits) if digits else 0
    
    # Xác định ký tự đặc biệt cần chèn
    special_index = digit_sum % len(special_chars)  # Quay về đầu nếu vượt quá
    
    # Chèn đúng 5 ký tự đặc biệt theo quy luật
    positions = []
    if digit_sum > 0:
        first_digit = int(str(digit_sum)[0])
        k = digit_sum
        for _ in range(5):
            pos = k % len(combined)  # Đảm bảo vị trí hợp lệ
            while pos in positions:
                pos = (pos + 1) % len(combined)  # Tránh trùng lặp
            positions.append(pos)
            k *= first_digit  # Cập nhật k theo quy luật
    
    # Chèn ký tự đặc biệt vào vị trí
    combined_list = list(combined)
    for i, pos in enumerate(positions[:5]):
        combined_list.insert(pos, special_chars[(special_index + i) % len(special_chars)])
    
    return "".join(combined_list)  # Kết hợp lại thành chuỗi


def process_hashed_text(hashed_text):
    """Giữ nguyên thứ tự phần chữ và số, tính tích chữ số"""
    letters = "".join([char for char in hashed_text if char.isalpha()])  # Lấy phần chữ, giữ nguyên thứ tự
    digits = [int(char) for char in hashed_text if char.isdigit()]  # Lấy danh sách số, giữ nguyên thứ tự

    # Tính tích các chữ số
    product = 27 * 11 * 2003
    for num in digits:
        if num != 0:
            product *= num
        else:
            product /= 2
            product = int(product)

    # Viết hoa chữ cái ở vị trí tương ứng với chữ số xuất hiện nhiều nhất
    number = product
    number = str(number)[:4]  # Lấy 4 chữ số đầu tiên
    positions = [int(digit) for digit in str(number)]
    letters = list(letters)  # Chuyển chuỗi thành danh sách ký tự

    for pos in positions:
        while pos * 2 < len(letters) and letters[pos].isupper() and pos != 0:
            pos *= 2
        if pos < len(letters):  # Kiểm tra tránh lỗi nếu chuỗi quá ngắn
            letters[pos] = letters[pos].upper()
    letters = ''.join(letters)
    s = letters + str(product)
    return process_string(s)

# Nhận input từ người dùng
i = '1'
while i == '1':
    input_text = input("Vui lòng nhập: ")
    hashed_text = sha256_encrypt(input_text)
    processed_text = process_hashed_text(hashed_text)
    pyperclip.copy(processed_text)
    print(processed_text)
    print("Đã lưu vào bộ nhớ tạm \u2713") 
    delete = input("Để không xoá bộ nhớ tạm (bấm phím 2): ")
    if delete != '2':
        pyperclip.copy("")
        print("Đã xoá bộ nhớ tạm \u2713") 
    i = input("Tiếp tục chạy? (bấm phím 1): ")

# pyinstaller --onefile --icon=favicon.ico demo.py
# chuột phải file exe --> create a shortcut --> done