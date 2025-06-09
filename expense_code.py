import streamlit as st

# App setup
st.set_page_config(page_title="Monthly Expense Tracker", page_icon="📊")
st.title("📊 Monthly Expense Tracker")

# Category list
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

# User input for budget
budget = st.number_input("Enter your total monthly budget (INR):", min_value=0.0, format="%.2f")

# Expenses input
expenses = []
st.subheader("Enter your expenses for each category:")
for cat in categories:
    amt = st.number_input(f"{cat} (INR):", min_value=0.0, format="%.2f", key=cat)
    expenses.append(amt)

# When user clicks "Show Summary"
if st.button("Show Summary") and budget > 0:
    total = sum(expenses)
    usage = (total / budget) * 100 if budget > 0 else 0

    st.markdown("---")
    st.subheader("📄 Expense Summary")
    for cat, amt in zip(categories, expenses):
        st.write(f"• **{cat}**: ₹{amt:.2f}")
    
    st.markdown("---")
    st.write(f"### 💰 Total Spent: ₹{total:.2f}")
    if total <= budget:
        st.success(f"Remaining Balance: ₹{budget - total:.2f}")
    else:
        st.error(f"Over Budget By: ₹{total - budget:.2f}")
    
    # Budget usage alerts
    if usage > 100:
        st.error("🚨 Alert: You have **exceeded** your monthly budget!")
    elif usage > 80:
        st.warning("⚠️ Warning: You've used more than **80%** of your budget.")
    else:
        st.info("✅ You're within your budget.")

    # Overused categories (more than 40%)
    st.markdown("#### 📌 Overused Categories")
    for cat, amt in zip(categories, expenses):
        cat_share = (amt / total * 100) if total > 0 else 0
        if cat_share > 40:
            st.warning(f"🔴 **{cat}** took up {cat_share:.2f}% of your total spending.")

    # Repetitive amounts
    st.markdown("#### 🔁 Duplicate Expenses")
    checked = set()
    found_duplicate = False
    for i in range(len(expenses)):
        for j in range(i + 1, len(expenses)):
            if expenses[i] == expenses[j] and expenses[i] > 0:
                pair = tuple(sorted([i, j]))
                if pair not in checked:
                    checked.add(pair)
                    st.info(f"🔁 ₹{expenses[i]:.2f} found in both **{categories[i]}** and **{categories[j]}**.")
                    found_duplicate = True
    if not found_duplicate:
        st.write("No duplicate expense amounts found.")

    # Time-based check
    st.markdown("#### ⏱️ Time-Based Review")
    review_time = st.radio("Is it mid-month or end of the month?", ["Skip", "Mid-Month", "End of Month"])
    if review_time == "Mid-Month":
        st.info(f"📅 MID-MONTH REVIEW: You're at {usage:.2f}% of your budget.")
    elif review_time == "End of Month":
        st.success(f"📅 END OF MONTH REVIEW: Great tracking! Total spent: ₹{total:.2f}")

    # Tip
    st.markdown("---")
    st.info("💡 TIP: Try to save at least 10% of your monthly budget if possible!")

elif st.button("Show Summary") and budget == 0:
    st.error("Please enter a valid monthly budget before proceeding.")
