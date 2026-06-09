fleet_list = []

def get_status(difference):
    if difference < 0:
        return "Tiet kiem"
    elif 0 <= difference < 2:
        return "Tieu chuan"
    elif 2 <= difference < 8:
        return "Tieu hao cao"
    else:
        return "Qua tai / That thoat"

def is_id_exist(vehicle_id):
    for vehicle in fleet_list:
        if vehicle["vehicle_id"] == vehicle_id:
            return True
    return False

def get_valid_string(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Loi: Khong duoc de trong. Vui long nhap lai.")
        else:
            return value

def get_valid_float(prompt, require_positive=False, require_non_negative=False):
    while True:
        try:
            value = float(input(prompt))
            if require_positive and value <= 0:
                print("Loi: Gia tri phai lon hon 0. Vui long nhap lai.")
                continue
            if require_non_negative and value < 0:
                print("Loi: Gia tri phai lon hon hoac bang 0. Vui long nhap lai.")
                continue
            return value
        except ValueError:
            print("Loi: Sai dinh dang so. Vui long nhap lai.")

def display_vehicles():
    if len(fleet_list) == 0:
        print("\nDanh sach doi xe hien dang trong.")
        return
    
    print("\n" + "-" * 115)
    print(f"| {'Ma XE':<10} | {'Bien so (Tai xe)':<25} | {'Dinh muc':<10} | {'So km':<10} | {'Nhien lieu':<12} | {'Chenh lech':<12} | {'Trang thai':<20} |")
    print("-" * 115)
    
    for vehicle in fleet_list:
        print(f"| {vehicle['vehicle_id']:<10} | {vehicle['driver_plate']:<25} | {vehicle['norm']:<10.2f} | {vehicle['distance']:<10.2f} | {vehicle['fuel']:<12.2f} | {vehicle['difference']:<12.2f} | {vehicle['status']:<20} |")
    print("-" * 115)

def add_vehicle():
    print("\n--- BO SUNG XE MOI VAO DOI ---")
    while True:
        vehicle_id = get_valid_string("Nhap ma dinh danh phuong tien: ")
        if is_id_exist(vehicle_id):
            print("Loi: Ma phuong tien nay da ton tai trong he thong.")
        else:
            break
            
    driver_plate = get_valid_string("Nhap Bien so xe / Ten tai xe: ")
    norm = get_valid_float("Nhap Dinh muc ly thuyet (Lit/100km): ", require_positive=True)
    distance = get_valid_float("Nhap Tong so km da di chuyen: ", require_non_negative=True)
    fuel = get_valid_float("Nhap Tong so nhien lieu tieu thu (Lit): ", require_non_negative=True)

    theory_fuel = (distance * norm) / 100.0
    difference = fuel - theory_fuel
    status = get_status(difference)

    vehicle_info = {
        "vehicle_id": vehicle_id,
        "driver_plate": driver_plate,
        "norm": norm,
        "distance": distance,
        "fuel": fuel,
        "difference": difference,
        "status": status
    }
    fleet_list.append(vehicle_info)
    print("\nThem phuong tien moi thanh cong!")

def update_log():
    print("\n--- CAP NHAT NHAT KY HANH TRINH ---")
    vehicle_id = input("Nhap ma phuong tien can cap nhat: ").strip()
    
    for vehicle in fleet_list:
        if vehicle["vehicle_id"] == vehicle_id:
            new_norm = get_valid_float("Nhap lai Dinh muc ly thuyet (Lit/100km): ", require_positive=True)
            new_distance = get_valid_float("Nhap Tong so km da di chuyen moi: ", require_non_negative=True)
            new_fuel = get_valid_float("Nhap Tong so nhien lieu tieu thu thuc te moi: ", require_non_negative=True)

            theory_fuel = (new_distance * new_norm) / 100.0
            new_difference = new_fuel - theory_fuel
            new_status = get_status(new_difference)

            vehicle["norm"] = new_norm
            vehicle["distance"] = new_distance
            vehicle["fuel"] = new_fuel
            vehicle["difference"] = new_difference
            vehicle["status"] = new_status
            
            print("\nCap nhat nhat ky thanh cong!")
            return
            
    print("\nLoi: Khong tim thay phuong tien mang ma nay.")

def delete_vehicle():
    print("\n--- XOA XE KHOI DOI QUAN LY ---")
    vehicle_id = input("Nhap ma phuong tien can xoa: ").strip()
    
    for index in range(len(fleet_list)):
        if fleet_list[index]["vehicle_id"] == vehicle_id:
            confirm = input("Ban co chac muon xoa phuong tien nay khoi doi xe khong? (Y/N): ").strip().upper()
            if confirm == "Y":
                del fleet_list[index]
                print("\nXoa phuong tien thanh cong!")
            else:
                print("\nDa huy thao tac xoa.")
            return
            
    print("\nLoi: Khong tim thay phuong tien mang ma nay.")

def search_vehicle():
    print("\n--- TIM KIEM PHUONG TIEN ---")
    keyword = input("Nhap ma xe, bien so hoac ten tai xe de tim: ").strip().lower()
    search_results = []
    
    for vehicle in fleet_list:
        if keyword == vehicle["vehicle_id"].lower() or keyword in vehicle["driver_plate"].lower():
            search_results.append(vehicle)

    if len(search_results) == 0:
        print("\nKhong tim thay phuong tien nao phu hop voi tu khoa.")
    else:
        print("\n" + "-" * 115)
        print(f"| {'Ma XE':<10} | {'Bien so (Tai xe)':<25} | {'Dinh muc':<10} | {'So km':<10} | {'Nhien lieu':<12} | {'Chenh lech':<12} | {'Trang thai':<20} |")
        print("-" * 115)
        for vehicle in search_results:
            print(f"| {vehicle['vehicle_id']:<10} | {vehicle['driver_plate']:<25} | {vehicle['norm']:<10.2f} | {vehicle['distance']:<10.2f} | {vehicle['fuel']:<12.2f} | {vehicle['difference']:<12.2f} | {vehicle['status']:<20} |")
        print("-" * 115)

def show_statistics():
    print("\n--- THONG KE HIEU SUAT HAM DOI ---")
    if len(fleet_list) == 0:
        print("Danh sach doi xe hien dang trong. Khong co du lieu thong ke.")
        return

    stats_board = {
        "Tiet kiem": 0,
        "Tieu chuan": 0,
        "Tieu hao cao": 0,
        "Qua tai / That thoat": 0
    }

    for vehicle in fleet_list:
        current_status = vehicle["status"]
        if current_status in stats_board:
            stats_board[current_status] += 1

    for performance_group, count in stats_board.items():
        print(f"Nhom {performance_group}: {count} phuong tien")

def main():
    while True:
        print("\n" + "=" * 55)
        print(" CHUONG TRINH QUAN LY HAM DOI XE - LOGISTICS")
        print("=" * 55)
        print("1. Hien thi danh sach doi xe")
        print("2. Bo sung xe moi vao doi")
        print("3. Cap nhat nhat ky hanh trinh")
        print("4. Xoa xe khoi doi quan ly")
        print("5. Tim kiem phuong tien")
        print("6. Thong ke hieu suat ham doi")
        print("8. Thoat chuong trinh")
        print("=" * 55)

        choice = input("Vui long nhap so chuc nang (1-6, 8): ").strip()

        if choice == "1":
            display_vehicles()
        elif choice == "2":
            add_vehicle()
        elif choice == "3":
            update_log()
        elif choice == "4":
            delete_vehicle()
        elif choice == "5":
            search_vehicle()
        elif choice == "6":
            show_statistics()
        elif choice == "8":
            print("\nCam on ban da su dung he thong quan ly. Tam biet!")
            break
        else:
            print("\nLoi: Chuc nang khong hop le. Vui long chon lai!")

if __name__ == "__main__":
    main()
