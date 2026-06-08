import sys

student_list = []

def calculate_average_score(toan, ly, hoa):#Tính average score 
    return round((toan + ly + hoa) / 3, 2)

def classify_academic_performance(dtb):#phân loại học lực
    if dtb < 5.0:
        return "Yếu"
    elif 5.0 <= dtb < 7.0:
        return "Trung bình"
    elif 7.0 <= dtb < 8.0:
        return "Khá"
    else:
        return "Giỏi"

def input_non_empty_string(prompt):# Hàm Check rỗng input
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Lỗi: Giá trị không được để trống. Vui lòng nhập lại.")

def input_valid_score(subject_name):
    """Đảm bảo người dùng nhập điểm là số hợp lệ từ 0 đến 10."""
    while True:
        try:
            score = float(input(f"Nhập điểm môn {subject_name} (0 - 10): "))
            if 0 <= score <= 10:
                return score
            else:
                print("Lỗi: Điểm phải nằm trong khoảng từ 0 đến 10. Vui lòng nhập lại.")
        except ValueError:
            print("Lỗi: Dữ liệu không hợp lệ. Vui lòng nhập một số.")

def find_student_index(student_id):#Hàm tìm index của student trong list
    for i, sv in enumerate(student_list):
        if sv["MaSV"].lower() == student_id.lower():
            return i
    return -1

def print_table_header():#In table header cho bảng 
    print(f"{'Mã SV':<10} | {'Họ và tên':<20} | {'Toán':<5} | {'Lý':<5} | {'Hóa':<5} | {'Điểm TB':<7} | {'Xếp loại':<12}")
    print("-" * 75)

def print_student_info(sv):# In student_info theo bảng
    print(f"{sv['MaSV']:<10} | {sv['HoTen']:<20} | {sv['Toan']:<5} | {sv['Ly']:<5} | {sv['Hoa']:<5} | {sv['DTB']:<7} | {sv['XepLoai']:<12}")

# 1. Hiển thị danh sách sinh viên
def display_student_list(custom_list=None):
    current_list = custom_list if custom_list is not None else student_list

    if not current_list:
        print("\nDanh sách sinh viên hiện đang trống.")
        return

    print("\n--- DANH SÁCH SINH VIÊN ---")
    print_table_header()
    for sv in current_list:
        print_student_info(sv)
    print("-" * 75)

# 2. Tiếp nhận sinh viên
def add_new_student():
    print("\n--- TIẾP NHẬN SINH VIÊN MỚI ---")
    while True:
        student_id = input_non_empty_string("Nhập mã sinh viên: ")
        if find_student_index(student_id) != -1:
            print("Lỗi: Mã sinh viên đã tồn tại. Vui lòng nhập mã khác.")
        else:
            break

    full_name = input_non_empty_string("Nhập họ và tên sinh viên: ")
    toan = input_valid_score("Toán")
    ly = input_valid_score("Lý")
    hoa = input_valid_score("Hóa")

    dtb = calculate_average_score(toan, ly, hoa)
    classification = classify_academic_performance(dtb)

    new_student = {
        "MaSV": student_id,
        "HoTen": full_name,
        "Toan": toan,
        "Ly": ly,
        "Hoa": hoa,
        "DTB": dtb,
        "XepLoai": classification
    }

    student_list.append(new_student)
    print(f"\nĐã thêm thành công sinh viên {full_name} (Xếp loại: {classification}).")

# 3. Cập nhật kết quả học tập
def update_student_results():
    print("\n--- CẬP NHẬT KẾT QUẢ HỌC TẬP ---")
    student_id = input("Nhập mã sinh viên cần cập nhật: ").strip()
    index = find_student_index(student_id)

    if index == -1:
        print("Thông báo: Không tìm thấy sinh viên có mã này trong hệ thống.")
        return

    print("Nhập thông tin điểm mới:")
    toan = input_valid_score("Toán")
    ly = input_valid_score("Lý")
    hoa = input_valid_score("Hóa")

    dtb = calculate_average_score(toan, ly, hoa)
    classification = classify_academic_performance(dtb)

    sv = student_list[index]
    sv["Toan"] = toan
    sv["Ly"] = ly
    sv["Hoa"] = hoa
    sv["DTB"] = dtb
    sv["XepLoai"] = classification

    print("\nĐã cập nhật điểm và học lực thành công.")

# 4. Xóa sinh viên
def delete_student():
    print("\n--- XÓA SINH VIÊN ---")
    student_id = input("Nhập mã sinh viên cần xóa: ").strip()
    index = find_student_index(student_id)

    if index == -1:
        print("Thông báo: Không tìm thấy sinh viên có mã này trong hệ thống.")
        return

    confirm = input("Bạn có chắc muốn xóa? (y/n): ").strip().lower()
    if confirm == 'y':
        deleted_student = student_list.pop(index)
        print(f"Đã xóa thành công sinh viên {deleted_student['HoTen']} khỏi danh sách.")
    else:
        print("Hủy thao tác xóa.")

# 5. Tìm kiếm sinh viên
def search_student():
    print("\n--- TÌM KIẾM SINH VIÊN ---")
    keyword = input("Nhập mã sinh viên hoặc tên sinh viên cần tìm: ").strip().lower()

    results = []
    for sv in student_list:
        if (keyword == sv["MaSV"].lower()) or (keyword in sv["HoTen"].lower()):
            results.append(sv)

    if results:
        display_student_list(results)
    else:
        print("Thông báo: Không tìm thấy sinh viên phù hợp.")

# 6. Thống kê điểm trung bình
def calculate_statistics():
    print("\n--- THỐNG KÊ HỌC LỰC ---")
    if not student_list:
        print("Danh sách sinh viên hiện đang trống, không thể thống kê.")
        return

    stats = {"Giỏi": 0, "Khá": 0, "Trung bình": 0, "Yếu": 0}

    for sv in student_list:
        stats[sv["XepLoai"]] += 1

    print("Kết quả thống kê:")
    print(f"- Sinh viên Giỏi       : {stats['Giỏi']}")
    print(f"- Sinh viên Khá        : {stats['Khá']}")
    print(f"- Sinh viên Trung bình : {stats['Trung bình']}")
    print(f"- Sinh viên Yếu        : {stats['Yếu']}")
#Hiển thị menu
def print_menu():
    print("\n" + "="*45)
    print("   CHƯƠNG TRÌNH QUẢN LÝ SINH VIÊN RIKKEI")
    print("="*45)
    print("1. Hiển thị danh sách sinh viên")
    print("2. Tiếp nhận sinh viên")
    print("3. Cập nhật kết quả học tập")
    print("4. Xóa sinh viên")
    print("5. Tìm kiếm sinh viên")
    print("6. Thống kê điểm trung bình")
    print("7. Thoát chương trình")
    print("="*45)
def main_menu():
    while True:
        print_menu()
        choice = input("Vui lòng chọn chức năng (1-7): ").strip()
        if choice == '1':
            display_student_list()
        elif choice == '2':
            add_new_student()
        elif choice == '3':
            update_student_results()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            search_student()
        elif choice == '6':
            calculate_statistics()
        elif choice == '7':
            print("Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            sys.exit()
        else:
            print("Lỗi: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 7.")
if __name__ == "__main__":
    main_menu()




