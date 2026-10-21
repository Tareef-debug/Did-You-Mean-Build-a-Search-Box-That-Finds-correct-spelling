import streamlit as st
menu = ["Pizza","Burger","Chicken","Fries","Pasta","Rice","Chatpati","Samosa","Biriyani","Kacchi","Palau"]
keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
positions = {}
for row, keys in enumerate(keyboard):
    for col, letter in enumerate(keys):
        positions[letter] = (row, col)
def nearby(a, b):
    if a not in positions or b not in positions: return False
    r1, c1 = positions[a]
    r2, c2 = positions[b]
    return abs(r1-r2) <= 1 and abs(c1-c2) <= 1
def spelling_distance(a, b):
    a = a.lower()
    b = b.lower()
    dp = [[0] * (len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)+1): dp[i][0] = i
    for j in range(len(b)+1): dp[0][j] = j
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            if a[i-1] == b[j-1]: cost = 0
            elif nearby(a[i-1], b[j-1]): cost = 0.5
            else: cost = 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
            if i > 1 and j > 1:
                if a[i-1] == b[j-2] and a[i-2] == b[j-1]:
                    dp[i][j] = min(dp[i][j], dp[i-2][j-2]+1)
    return dp[-1][-1]
st.set_page_config(page_title="Smart Food Corrector", page_icon="🍕")
st.title("🍕 Smart Food Menu Corrector")
st.write("Search for food even when you make spelling mistakes!")
st.subheader("Our Menu")
st.write(" | ".join(menu))
food = st.text_input("Enter food name:", placeholder="Example: piza, burger, chickn")
if st.button("Find Food"):
    if not food.strip(): st.warning("Please enter a food name")
    else:
        suggestions = sorted(menu, key=lambda item: spelling_distance(food.strip(), item))
        best = suggestions[0]
        score = spelling_distance(food.strip(), best)
        if score == 0: st.success(f"Food has been found: {best}")
        else: st.success(f"Did you mean: {best}?")
        st.write(f"Spelling difference score: {score}")
        st.subheader("Other Suggestions")
        for item in suggestions[1:4]:
            st.write(f"{item} - Score: {spelling_distance(food.strip(), item)}")
