import logging

logging.basicConfig(
    filename="arena_tickets.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ticket_db = [
    { "ticket_id": "T01", "buyer_name": "Nguyen Van A","price": 500.0, "status": "Booked", "seat": ("A", 1)},
    { "ticket_id": "T02","buyer_name": "Tran Thi B","price": 300.0,"status": "Cancelled","seat": ("B", 5)},
    { "ticket_id": "T03","buyer_name": "Le Van C","price": 500.0,"status": "Booked","seat": ("A", 2)}
]

def find_ticket_by_id(tickets, ticket_id):
    """Find ticket by ID."""
    for ticket in tickets:
        if ticket.get("ticket_id") == ticket_id:
            return ticket
    return None


def calculate_total_revenue(ticket_list):
    """
    Calculate valid revenue.
    Only count Booked tickets.
    """
    total = 0.0

    for ticket in ticket_list:
        try:
            if ticket["status"] == "Booked":
                total += ticket["price"]
        except KeyError as error:
            logging.error(
                f"Missing key while calculating revenue: {error}"
            )
            return 0.0

    return total


def display_tickets(tickets):
    """Display ticket list."""

    if not tickets:
        print("Hiện chưa có vé nào trong hệ thống.")
        return

    print("\n--- DANH SÁCH VÉ ---")
    print(
        f"{'Mã Vé':<8} | {'Tên Khách Hàng':<20} | "
        f"{'Giá Vé':<8} | {'Chỗ Ngồi':<10} | {'Trạng Thái'}"
    )
    print("-" * 70)
    for ticket in tickets:
        try:
            seat = f"{ticket['seat'][0]}-{ticket['seat'][1]}"
            status = ticket["status"]
            if status == "Cancelled":
                status += " [ĐÃ HỦY]"
            print(
                f"{ticket['ticket_id']:<8} | "
                f"{ticket['buyer_name']:<20} | "
                f"{ticket['price']:<8} | "
                f"{seat:<10} | "
                f"{status}"
            )
        except KeyError as error:
            print(
                "Lỗi: Một vé đang bị thiếu dữ liệu, "
                "vui lòng kiểm tra lại."
            )
            logging.error(
                f"Missing key while displaying ticket: {error}"
            )

    print("-" * 70)

    logging.info("User viewed ticket list.")


def book_ticket(tickets):
    """Book a new ticket."""
    print("\n--- ĐẶT VÉ MỚI ---")
    ticket_id = input("Nhập mã vé: ").strip()
    if find_ticket_by_id(tickets, ticket_id):
        print(f"Lỗi: Mã vé {ticket_id} đã tồn tại.")
        logging.warning(
            f"Duplicate ticket ID entered: {ticket_id}"
        )
        return
    buyer_name = input("Nhập tên khách hàng: ").strip()
    while True:
        try:
            price = float(input("Nhập giá vé: "))

            if price <= 0:
                print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break

        except ValueError:
            print("Giá vé phải là số. Vui lòng nhập lại.")
            logging.warning(
                "Invalid price input while booking ticket"
            )

    seat_area = input("Nhập khu vực ghế: ").upper()
    while True:
        try:
            seat_number = int(input("Nhập số ghế: "))
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

    new_ticket = { "ticket_id": ticket_id,"buyer_name": buyer_name,"price": price,"status": "Booked","seat": (seat_area, seat_number)}
    tickets.append(new_ticket)
    print(
        f"\nThành công: Đã đặt vé {ticket_id} "
        f"cho khách hàng {buyer_name}"
    )

    logging.info(
        f"Booked new ticket {ticket_id} for {buyer_name}"
    )

def change_seat(tickets):
    """Change seat."""
    print("\n--- ĐỔI CHỖ NGỒI ---")
    ticket_id = input("Nhập mã vé cần đổi chỗ: ").strip()
    ticket = find_ticket_by_id(tickets, ticket_id)
    if not ticket:
        print(f"Không tìm thấy vé mang mã {ticket_id}.")
        logging.warning(
            f"Change seat failed - Ticket {ticket_id} not found"
        )
        return
    new_area = input("Nhập khu vực ghế mới: ").upper()
    while True:
        try:
            new_number = int(
                input("Nhập số ghế mới: ")
            )
            break
        except ValueError:
            print(
                "Số ghế phải là số nguyên. "
                "Vui lòng nhập lại."
            )
    ticket["seat"] = (new_area, new_number)
    print(
        f"\nThành công: Đã đổi chỗ vé "
        f"{ticket_id} sang {new_area}-{new_number}."
    )

    logging.info(
        f"Seat changed for ticket "
        f"{ticket_id} to {new_area}-{new_number}"
    )

def cancel_ticket(tickets):
    """Cancel ticket."""
    print("\n--- HỦY VÉ ---")
    ticket_id = input("Nhập mã vé cần hủy: ").strip()
    ticket = find_ticket_by_id(tickets, ticket_id)
    if not ticket:
        print(f"Không tìm thấy vé mang mã {ticket_id}.")
        logging.warning(
            f"Cancel ticket failed - Ticket {ticket_id} not found"
        )
        return
    if ticket["status"] == "Cancelled":
        print(
            f"Vé {ticket_id} đã ở trạng thái "
            "Cancelled trước đó."
        )
        return
    ticket["status"] = "Cancelled"
    print(f"\nThành công: Vé {ticket_id} đã được hủy.")
    logging.warning(
        f"Ticket {ticket_id} has been cancelled."
    )

def calculate_revenue(tickets):
    """Revenue report."""
    print("\n--- BÁO CÁO DOANH THU ---")
    try:
        booked_count = 0
        cancelled_count = 0
        for ticket in tickets:
            if ticket["status"] == "Booked":
                booked_count += 1
            elif ticket["status"] == "Cancelled":
                cancelled_count += 1
        total = calculate_total_revenue(tickets)
        print(f"Tổng số vé đã đặt: {booked_count}")
        print(f"Tổng số vé đã hủy: {cancelled_count}")
        print(f"Tổng doanh thu hợp lệ: {total}")
        logging.info(
            f"Revenue report generated. Total: {total}"
        )
    except KeyError as error:
        print(
            "Lỗi: Một vé đang bị thiếu dữ liệu doanh thu."
        )
        logging.error(
            f"Missing key while calculating revenue: {error}"
        )

def show_menu():
    """Display menu."""
    print("\n=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===")
    print("1. Xem danh sách vé đã bán")
    print("2. Đặt vé mới")
    print("3. Đổi chỗ ngồi (Cập nhật vé)")
    print("4. Hủy vé")
    print("5. Báo cáo doanh thu")
    print("6. Thoát chương trình")
    print("========================================")

if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Chọn chức năng (1-6): ").strip()
        if choice == "1":
            display_tickets(ticket_db)
        elif choice == "2":
            book_ticket(ticket_db)
        elif choice == "3":
            change_seat(ticket_db)
        elif choice == "4":
            cancel_ticket(ticket_db)
        elif choice == "5":
            calculate_revenue(ticket_db)
        elif choice == "6":
            print(
                "Cảm ơn bạn đã sử dụng hệ thống "
                "quản lý vé Rikkei Esports."
            )
            logging.info(
                "Ticket management system closed."
            )
            break
        else:
            print("Lựa chọn không hợp lệ.")