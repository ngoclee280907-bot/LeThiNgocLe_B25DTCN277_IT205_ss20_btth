# PHÂN TÍCH BÀI TOÁN
# - Dữ liệu được lưu dưới dạng List chứa Dictionary
# - Mỗi vé gồm:
#   ticket_id, buyer_name, price, status, seat
#
# - seat được lưu bằng Tuple:
#   ("A", 1)
#
# - Chức năng:
#   1. Hiển thị danh sách vé
#   2. Đặt vé mới
#   3. Đổi chỗ ngồi
#   4. Hủy vé
#   5. Báo cáo doanh thu
#   6. Thoát
#
# - Sử dụng logging để ghi lại các hoạt động
# - Sử dụng try except để tránh chương trình bị crash
# - Do tuple là immutable nên khi đổi ghế phải tạo tuple mới
#
# LOGIC DOANH THU:
# Chỉ cộng tiền các vé có trạng thái Booked
# Không cộng các vé Cancelled

import logging

logging.basicConfig(
    filename="arena_tickets.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ticket_db = [
    {
        "ticket_id": "T01",
        "buyer_name": "Nguyen Van A",
        "price": 500.0,
        "status": "Booked",
        "seat": ("A", 1)
    },
    {
        "ticket_id": "T02",
        "buyer_name": "Tran Thi B",
        "price": 300.0,
        "status": "Cancelled",
        "seat": ("B", 5)
    },
    {
        "ticket_id": "T03",
        "buyer_name": "Le Van C",
        "price": 500.0,
        "status": "Booked",
        "seat": ("A", 2)
    }
]


# hàm tìm vé theo mã
def find_ticket(ticket_id):
    for ticket in ticket_db:
        if ticket["ticket_id"] == ticket_id:
            return ticket
    return None


# hàm tính doanh thu
def calculate_total_revenue(ticket_list):
    total = 0.0

    for ticket in ticket_list:
        try:
            if ticket["status"] == "Booked":
                total += ticket["price"]
        except KeyError:
            logging.error("Missing key while calculating revenue")
            return 0.0

    return total


# chức năng 1
def display_tickets():
    if len(ticket_db) == 0:
        print("Hiện chưa có vé nào trong hệ thống.")
        return

    print("\n--- DANH SÁCH VÉ ---")

    print(
        f"{'Mã Vé':<10}"
        f"{'Tên Khách Hàng':<20}"
        f"{'Giá Vé':<10}"
        f"{'Chỗ Ngồi':<10}"
        f"{'Trạng Thái':<20}"
    )

    try:
        for ticket in ticket_db:
            seat = ticket["seat"]

            status = ticket["status"]

            if status == "Cancelled":
                status += " [ĐÃ HỦY]"

            print(
                f"{ticket['ticket_id']:<10}"
                f"{ticket['buyer_name']:<20}"
                f"{ticket['price']:<10}"
                f"{seat[0]}-{seat[1]:<8}"
                f"{status:<20}"
            )

        logging.info("User viewed ticket list.")

    except KeyError as e:
        print("Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
        logging.error(f"Missing key while displaying ticket: {e}")


# chức năng 2
def book_ticket():
    print("\n--- ĐẶT VÉ MỚI ---")

    ticket_id = input("Nhập mã vé: ").strip().upper()

    if find_ticket(ticket_id):
        print(f"Lỗi: Mã vé {ticket_id} đã tồn tại.")
        logging.warning(
            f"Duplicate ticket ID entered: {ticket_id}"
        )
        return

    buyer_name = input("Nhập tên khách hàng: ").title()

    while True:
        try:
            price = float(input("Nhập giá vé: "))

            if price <= 0:
                print("Giá vé phải lớn hơn 0.")
                continue

            break

        except ValueError:
            print("Giá vé phải là số.")
            logging.warning(
                "Invalid price input while booking ticket"
            )

    area = input("Nhập khu vực ghế: ").upper()

    while True:
        try:
            seat_number = int(input("Nhập số ghế: "))

            if seat_number <= 0:
                print("Số ghế phải lớn hơn 0.")
                continue

            break

        except ValueError:
            print("Số ghế phải là số nguyên.")

    new_ticket = {
        "ticket_id": ticket_id,
        "buyer_name": buyer_name,
        "price": price,
        "status": "Booked",
        "seat": (area, seat_number)
    }

    ticket_db.append(new_ticket)

    print(
        f"Thành công: Đã đặt vé {ticket_id} "
        f"cho khách hàng {buyer_name}."
    )

    logging.info(
        f"Booked new ticket {ticket_id} for {buyer_name}"
    )


# chức năng 3
def change_seat():
    print("\n--- ĐỔI CHỖ NGỒI ---")

    ticket_id = input(
        "Nhập mã vé cần đổi chỗ: "
    ).strip().upper()

    ticket = find_ticket(ticket_id)

    if ticket is None:
        print(f"Không tìm thấy vé mang mã {ticket_id}.")
        logging.warning(
            f"Change seat failed - Ticket {ticket_id} not found"
        )
        return

    new_area = input(
        "Nhập khu vực ghế mới: "
    ).upper()

    while True:
        try:
            new_number = int(
                input("Nhập số ghế mới: ")
            )

            break

        except ValueError:
            print(
                "Số ghế phải là số nguyên."
            )

    # tuple không sửa trực tiếp được
    ticket["seat"] = (new_area, new_number)

    print(
        f"Thành công: Đã đổi chỗ vé "
        f"{ticket_id} sang "
        f"{new_area}-{new_number}."
    )

    logging.info(
        f"Seat changed for ticket "
        f"{ticket_id} to "
        f"{new_area}-{new_number}"
    )


# chức năng 4
def cancel_ticket():
    print("\n--- HỦY VÉ ---")

    ticket_id = input(
        "Nhập mã vé cần hủy: "
    ).strip().upper()

    ticket = find_ticket(ticket_id)

    if ticket is None:
        print(f"Không tìm thấy vé mang mã {ticket_id}.")
        logging.warning(
            f"Cancel ticket failed - Ticket {ticket_id} not found"
        )
        return

    if ticket["status"] == "Cancelled":
        print(
            f"Vé {ticket_id} đã ở trạng thái "
            f"Cancelled trước đó."
        )
        return

    ticket["status"] = "Cancelled"

    print(f"Thành công: Vé {ticket_id} đã được hủy.")

    logging.warning(
        f"Ticket {ticket_id} has been cancelled."
    )


# chức năng 5
def calculate_revenue():
    print("\n--- BÁO CÁO DOANH THU ---")

    booked = 0
    cancelled = 0

    for ticket in ticket_db:
        if ticket["status"] == "Booked":
            booked += 1
        else:
            cancelled += 1

    total = calculate_total_revenue(ticket_db)

    print(f"Tổng số vé đã đặt: {booked}")
    print(f"Tổng số vé đã hủy: {cancelled}")
    print(f"Tổng doanh thu hợp lệ: {total}")

    logging.info(
        f"Revenue report generated. Total: {total}"
    )


# menu chính
while True:
    print("\n=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===")
    print("1. Xem danh sách vé đã bán")
    print("2. Đặt vé mới")
    print("3. Đổi chỗ ngồi")
    print("4. Hủy vé")
    print("5. Báo cáo doanh thu")
    print("6. Thoát chương trình")

    choice = input("Chọn chức năng: ")

    if choice == "1":
        display_tickets()

    elif choice == "2":
        book_ticket()

    elif choice == "3":
        change_seat()

    elif choice == "4":
        cancel_ticket()

    elif choice == "5":
        calculate_revenue()

    elif choice == "6":
        print(
            "Cảm ơn bạn đã sử dụng hệ thống."
        )

        logging.info(
            "Ticket management system closed."
        )

        break

    else:
        print("Lựa chọn không hợp lệ.")