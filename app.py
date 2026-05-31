import streamlit as st
import pandas as pd
import math
from datetime import date, timedelta

st.title("Кредитный калькулятор")

# Ввод данных
col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Сумма кредита", min_value=0.0, value=100000.0, step=1000.0)
    rate = st.number_input("Годовая ставка, %", min_value=0.0, value=12.0, step=0.1)
with col2:
    years = st.number_input("Срок кредита, лет", min_value=1, value=3, step=1)
    payment_type = st.radio("Тип платежа", ["Аннуитетный", "Дифференцированный"])

add_dates = st.checkbox("Добавить даты платежей")
if add_dates:
    first_date = st.date_input("Дата первого платежа", value=date.today())

if amount <= 0 or rate < 0 or years <= 0:
    st.error("Проверьте корректность ввода суммы, ставки и срока.")
    st.stop()

months = years * 12
monthly_rate = rate / 100 / 12

# Расчёт аннуитетного платежа
def annuity_payment(summa, r, n):
    if r == 0:
        return summa / n
    k = r * (1 + r) ** n / ((1 + r) ** n - 1)
    return summa * k

# Формирование графика платежей
balance = amount
rows = []

for m in range(1, months + 1):
    if payment_type == "Аннуитетный":
        payment = annuity_payment(amount, monthly_rate, months)
        interest = balance * monthly_rate
        principal = payment - interest
    else:  # Дифференцированный
        principal = amount / months
        interest = balance * monthly_rate
        payment = principal + interest

    end_balance = balance - principal
    if end_balance < 0:
        end_balance = 0

    row = {
        "Месяц": m,
        "Остаток долга на начало": round(balance, 2),
        "Ежемесячный платеж": round(payment, 2),
        "Процентная часть": round(interest, 2),
        "Долговая часть": round(principal, 2),
        "Остаток долга на конец": round(end_balance, 2),
    }

    if add_dates:
        row["Дата платежа"] = first_date + timedelta(days=30 * (m - 1))

    rows.append(row)
    balance = end_balance

df = pd.DataFrame(rows)

st.subheader("График платежей")
st.dataframe(df, use_container_width=True)

st.subheader("Итоги")
st.write(f"Общая сумма выплат: **{df['Ежемесячный платеж'].sum():,.2f}**")
st.write(f"Переплата по процентам: **{df['Процентная часть'].sum():,.2f}**")
