from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data for a simple demo hostel management system
residents = [
    {"name": "Asha Kumar", "room": "101", "fee": 4500, "status": "Paid"},
    {"name": "Rohan Singh", "room": "102", "fee": 4000, "status": "Pending"},
]

rooms = [
    {"number": "101", "type": "Single", "capacity": 1, "occupied": 1, "status": "Occupied"},
    {"number": "102", "type": "Double", "capacity": 2, "occupied": 1, "status": "Partial"},
    {"number": "103", "type": "Double", "capacity": 2, "occupied": 0, "status": "Available"},
]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        room = request.form.get("room", "").strip()
        fee = request.form.get("fee", "0").strip()
        status = request.form.get("status", "Paid").strip()

        if name and room:
            residents.append({"name": name, "room": room, "fee": int(fee or 0), "status": status})

            for room_item in rooms:
                if room_item["number"] == room:
                    room_item["occupied"] += 1
                    if room_item["occupied"] >= room_item["capacity"]:
                        room_item["status"] = "Occupied"
                    else:
                        room_item["status"] = "Partial"
                    break

        return redirect(url_for("index"))

    total_residents = len(residents)
    total_rooms = len(rooms)
    occupied_rooms = sum(1 for r in rooms if r["status"] != "Available")
    available_rooms = total_rooms - occupied_rooms
    total_fee = sum(r["fee"] for r in residents)

    return render_template(
        "index.html",
        residents=residents,
        rooms=rooms,
        total_residents=total_residents,
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        available_rooms=available_rooms,
        total_fee=total_fee,
    )


if __name__ == "__main__":
    app.run(debug=True)
