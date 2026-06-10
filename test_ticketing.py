from btth import calculate_total_revenue


def test_revenue_with_booked_and_cancelled():
    tickets = [
        {"ticket_id": "T01", "price": 500.0, "status": "Booked"},
        {"ticket_id": "T02", "price": 300.0, "status": "Cancelled"},
        {"ticket_id": "T03", "price": 700.0, "status": "Booked"}
    ]
    assert calculate_total_revenue(tickets) == 1200.0

def test_revenue_empty_list():
    tickets = []
    assert calculate_total_revenue(tickets) == 0.0