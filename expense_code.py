import streamlit as st
import requests

# Paste your Pushbullet Access Token here (KEEP PRIVATE)
PUSHBULLET_TOKEN = "o.mSwwdTaGJVL07XCqY3cxUEeDgSBTf6xx"

def send_push_notification(title, body, token):
    data = {
        "type": "note",
        "title": title,
        "body": body
    }
    resp = requests.post(
        "https://api.pushbullet.com/v2/pushes",
        json=data,
        headers={"Access-Token": token}
    )
    return resp.status_code

st.set_page_config(page_title="Monthly Expense Tracker", page_icon="📊")
st.title("📊 Monthly Expense Tracker")

categories = [
    "Rent / Hostel / PG Fees",
    "Food & Groceries",
    "Stationary & Academic Supplies",
    "Transport / Travel",
    "Mobile & Internet Recharge",
    "Personal Expenses / Toiletries",
    "Medical & Health",
    "Clothing & Essentials",
    "Fun & Entertainment",
    "Miscellaneous / Unexpected",
    "Tuition / Coaching Fees",
    "Fitness / Gym",
    "Savings"
]

expenses = [0.0] * len(categories)

budget = st.number_input("Enter your monthly budget (INR):", min_value=0.0, step=100.0)

if budget > 0:
    st.subheader("💸 Enter your expenses:")

    for i, category in enumerate(categories):
        expenses[i] = st.number_input(f"{category} (INR):", min_value=0.0, step=50.0, key=category)

    if st.button("Show Summary"):
        total = sum(expenses)

        st.markdown("---")
        st.subheader("📋 Expense Summary")
        for i in range(len(categories)):
            st.write(f"**{categories[i]}:** INR {expenses[i]:.2f}")
        st.write(f"### 🧮 Total Spent: INR {total:.2f}")

        if total <= budget:
            st.success(f"Remaining Balance: INR {budget - total:.2f}")
        else:
            st.error(f"Over Budget By: INR {total - budget:.2f}")

        usage = (total / budget) * 100 if budget > 0 else 0
        if usage > 100:
            st.error("🚨 You have exceeded your monthly budget!")
            send_push_notification(
                "🚨 Budget Alert",
                f"You have exceeded your budget! Spent INR {total:.2f} of INR {budget:.2f}",
                PUSHBULLET_TOKEN
            )
        elif usage > 80:
            st.warning("⚠️ You have used more than 80% of your budget.")
            send_push_notification(
                "⚠️ Budget Warning",
                f"You've used {usage:.2f}% of your budget.",
                PUSHBULLET_TOKEN
            )

        for i in range(len(expenses)):
            cat_share = (expenses[i] / total) * 100 if total > 0 else 0
            if cat_share > 40:
                st.info(f"💡 You have spent {cat_share:.2f}% on '{categories[i]}'. Consider reducing it.")

        month_review = st.radio("📆 Is it mid-month or end of month?", ["Skip", "Mid-month", "End of month"])
        if month_review == "Mid-month":
            st.write(f"🔍 MID-MONTH REVIEW: You've used {usage:.2f}% of your budget.")
        elif month_review == "End of month":
            st.write(f"📅 END OF MONTH REVIEW: Great! Total spent = INR {total:.2f}")

        for i in range(len(expenses) - 1):
            for j in range(i + 1, len(expenses)):
                if expenses[i] > 0 and expenses[i] == expenses[j]:
                    st.warning(f"🔁 Same amount (INR {expenses[i]:.2f}) in '{categories[i]}' and '{categories[j]}'. Double-check!")

        st.markdown("---")
        st.success("💰 TIP: Try to save at least 10% of your monthly budget!")
