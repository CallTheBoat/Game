import streamlit as st
import math
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

# ---------- Minimal distance function ----------
def distance_nm(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lat2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_km = 6371.0 * c
    return dist_km * 0.539957

# ---------- Session State -----------
if "profile" not in st.session_state:
    st.session_state["profile"] = {
        "name": "",
        "surname": "",
        "age": 0,
        "facebook_friends": 0,
        "instagram_followers": 0,
        "adonboard_friends": 0,
        "photo": None,
        "friend_count": 0
    }

if "addonboard_feed" not in st.session_state:
    st.session_state["addonboard_feed"] = [
        {"post_id": 1, "text": "Hello from AddOnBoard!", "adds": 0, "shares": 0, "friend_requests": 0},
        {"post_id": 2, "text": "Another day at sea!",    "adds": 0, "shares": 0, "friend_requests": 0},
        {"post_id": 3, "text": "Looking for sponsors!",  "adds": 0, "shares": 0, "friend_requests": 0}
    ]

if "active_sponsor" not in st.session_state:
    st.session_state["active_sponsor"] = None

if "current_square" not in st.session_state:
    st.session_state["current_square"] = 0

if "total_nm" not in st.session_state:
    st.session_state["total_nm"] = 0.0

if "profile_sent" not in st.session_state:
    st.session_state["profile_sent"] = False

if "sponsor_decision" not in st.session_state:
    st.session_state["sponsor_decision"] = None

if "final_campaign_decision" not in st.session_state:
    st.session_state["final_campaign_decision"] = None

# Επιπλέον, για την "κόκκινη ειδοποίηση" στο Board Game,
# θα έχουμε ένα flag "show_red_light" => True αν sponsor_decision == "Approved"
if "show_red_light" not in st.session_state:
    st.session_state["show_red_light"] = False

# ---------- Create 4 Tabs ----------
tabs = st.tabs([
    "1. Profile Setup & AddOnBoard Feed",
    "2. Board Game",
    "3. Sponsor Requirements",
    "4. Sponsor Admin"
])

# ========== TAB 1: Profile Setup & AddOnBoard Feed ==========
with tabs[0]:
    st.title("Profile Setup & AddOnBoard Feed")
    st.info("Fill in your profile, then see the AddOnBoard 'feed' with 'Add' instead of 'like', 'Share', etc.")

    with st.form("profile_form"):
        st.session_state["profile"]["name"] = st.text_input("Name", value=st.session_state["profile"]["name"])
        st.session_state["profile"]["surname"] = st.text_input("Surname", value=st.session_state["profile"]["surname"])
        st.session_state["profile"]["age"] = st.number_input("Age", min_value=0, value=st.session_state["profile"]["age"])
        
        st.session_state["profile"]["facebook_friends"] = st.number_input(
            "Facebook Friends", min_value=0,
            value=st.session_state["profile"]["facebook_friends"]
        )
        st.session_state["profile"]["instagram_followers"] = st.number_input(
            "Instagram Followers", min_value=0,
            value=st.session_state["profile"]["instagram_followers"]
        )
        st.session_state["profile"]["adonboard_friends"] = st.number_input(
            "AdOnBoard Friends", min_value=0,
            value=st.session_state["profile"]["adonboard_friends"]
        )

        photo_file = st.file_uploader("Upload a Profile Photo", type=["jpg","jpeg","png"])
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            if photo_file is not None:
                st.session_state["profile"]["photo"] = photo_file.read()
                st.success("Profile photo uploaded!")
            else:
                st.session_state["profile"]["photo"] = None
            st.success("Profile data saved! Scroll down to see feed below.")

    # Show photo if any
    if st.session_state["profile"]["photo"]:
        st.image(st.session_state["profile"]["photo"], caption="Your Profile Photo")

    st.markdown("### AddOnBoard Feed")
    feed = st.session_state["addonboard_feed"]
    for post in feed:
        st.markdown(f"**Post {post['post_id']}**: {post['text']}")
        st.write(f"Adds: {post['adds']}, Shares: {post['shares']}, FriendRequests: {post['friend_requests']}")
        
        col1, col2, col3 = st.columns(3)
        if col1.button(f"Add (Post {post['post_id']})"):
            post["adds"] += 1
            st.experimental_rerun()
        if col2.button(f"Share (Post {post['post_id']})"):
            post["shares"] += 1
            st.experimental_rerun()
        if col3.button(f"Add Friend (Post {post['post_id']})"):
            post["friend_requests"] += 1
            st.session_state["profile"]["friend_count"] += 1
            st.experimental_rerun()
    
    st.markdown(f"**Total AdOnBoard Friends**: {st.session_state['profile']['friend_count']}")

# ========== TAB 2: Board Game ==========
with tabs[1]:
    st.title("Board Game (Passenger)")

    squares = [
        {"name": "Start",  "coords": (36.45, 28.22)},
        {"name": "Finish", "coords": (36.40, 28.15)}
    ]
    st.write(f"**Current Square**: {squares[st.session_state['current_square']]['name']}")
    st.write(f"**Total NM**: {st.session_state['total_nm']:.2f}")

    m = folium.Map(location=squares[0]["coords"], zoom_start=7)
    for sq in squares:
        folium.Marker(sq["coords"], tooltip=sq["name"]).add_to(m)
    folium.Marker(
        squares[st.session_state["current_square"]]["coords"],
        icon=folium.Icon(color="blue", icon="ship", prefix="fa"),
        tooltip="Boat Position"
    ).add_to(m)
    st_folium(m, width=700, height=450)

    # If sponsor_decision == "Approved", show the "red light" notification
    if st.session_state["sponsor_decision"] == "Approved":
        # Show a "red light" or "sirene" style icon
        st.markdown("### 🚨 **New Sponsor Notification** 🚨")
        st.info("Your sponsor has APPROVED your profile! Click below to see the official 'sponsored boat'.")
        if st.button("Open Notification"):
            st.image("https://via.placeholder.com/600x300.png?text=Boat+with+Sponsor+Logos",
                     caption="Καλώς ήρθες στο ταξίδι! Sponsored by Vodafone.")
            st.success("Enjoy your sponsored journey with custom logos & t-shirts!")
    
    if st.button("Roll the Dice"):
        if st.session_state["current_square"] == 0:
            st.session_state["current_square"] = 1
            c1 = squares[0]["coords"]
            c2 = squares[1]["coords"]
            distnm = distance_nm(c1[0], c1[1], c2[0], c2[1])
            st.session_state["total_nm"] += distnm
            st.success("Moved from Start to Finish!")
        else:
            st.warning("Already at Finish.")
    
    st.markdown("### Sponsor Offer")
    st.info("Sponsor: 'Vodafone' wants 1000 impressions, 50% discount.")
    accept_btn = st.button("Yes, Accept Sponsor")
    decline_btn = st.button("No, Decline Sponsor")

    if accept_btn:
        dur_days = 5
        sday = date.today()
        eday = sday + timedelta(days=dur_days)
        st.session_state["active_sponsor"] = {
            "sponsor_name": "Vodafone",
            "required_impressions": 1000,
            "discount_percent": 50,
            "duration_days": dur_days,
            "start_date": sday,
            "end_date": eday,
            "daily_posts": 2,
            "hours_near_beach": 4,
            "tshirts": "Vodafone T-shirts & Banners"
        }
        st.session_state["profile_sent"] = False
        st.session_state["sponsor_decision"] = None
        st.session_state["final_campaign_decision"] = None
        st.success("Sponsor accepted. See details below or tab 3.")
    elif decline_btn:
        st.warning("Declined sponsor.")
        st.session_state["active_sponsor"] = None
        st.session_state["profile_sent"] = False
        st.session_state["sponsor_decision"] = None
        st.session_state["final_campaign_decision"] = None

    sp = st.session_state["active_sponsor"]
    if sp is not None:
        st.markdown("### Sponsor Requirements (quick view)")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}%")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']}→{sp['end_date']})")
        st.write(f"- {sp['daily_posts']} posts/day")
        st.write(f"- {sp['hours_near_beach']} hours near beaches/day")
        st.write(f"- Materials: {sp['tshirts']}")

        if st.session_state["profile_sent"]:
            st.warning("Profile already sent. Wait for sponsor decision (or see Tab 3).")
        else:
            if st.button("Send My Profile to Sponsor"):
                st.session_state["profile_sent"] = True
                st.session_state["sponsor_decision"] = None
                st.session_state["final_campaign_decision"] = None
                st.success("Profile sent! Sponsor sees it in 'Sponsor Admin' tab.")

    # If at finish
    if st.session_state["current_square"] == 1:
        st.subheader("Journey Completed!")
        if st.button("Restart Game"):
            st.session_state["current_square"] = 0
            st.session_state["total_nm"]       = 0.0
            st.session_state["active_sponsor"] = None
            st.session_state["profile_sent"]   = False
            st.session_state["sponsor_decision"] = None
            st.session_state["final_campaign_decision"] = None
            st.success("Game restarted!")

# ========== TAB 3: Sponsor Requirements (Passenger) ==========
with tabs[2]:
    st.title("Sponsor Requirements (Passenger Final)")

    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.info("No active sponsor. Accept one in Board Game tab.")
    else:
        st.success(f"Sponsor: {sp['sponsor_name']}")
        st.write(f"- Required Impressions: {sp['required_impressions']}")
        st.write(f"- Discount: {sp['discount_percent']}%")
        st.write(f"- Duration: {sp['duration_days']} days ({sp['start_date']} -> {sp['end_date']})")
        st.write(f"- {sp['daily_posts']} posts/day")
        st.write(f"- {sp['hours_near_beach']} hours near beaches/day")
        st.write(f"- Materials: {sp['tshirts']}")

        if not st.session_state["profile_sent"]:
            st.warning("You haven't sent your profile. See Board Game tab.")
        else:
            dec = st.session_state["sponsor_decision"]
            if dec is None:
                st.info("Waiting for sponsor decision (Tab 4).")
            elif dec == "Rejected":
                st.error("Sponsor REJECTED your profile!")
            elif dec == "Approved":
                st.success("Sponsor APPROVED your profile!")
                st.markdown("#### Final Acceptance?")

                final_dec = st.session_state["final_campaign_decision"]
                if final_dec == "Yes":
                    st.success("You have FINALLY accepted the sponsor's campaign!")
                elif final_dec == "No":
                    st.warning("You refused the final campaign. No sponsor for you.")
                elif final_dec == "Think":
                    st.info("Still thinking…")
                else:
                    yes_btn   = st.button("Yes, I accept the final campaign!")
                    no_btn    = st.button("No, I refuse the final campaign.")
                    think_btn = st.button("I Will Think About It.")
                    if yes_btn:
                        st.session_state["final_campaign_decision"] = "Yes"
                        st.success("You have FINALLY accepted the sponsor's campaign!")
                    elif no_btn:
                        st.session_state["final_campaign_decision"] = "No"
                        st.warning("You refused the final campaign. Maybe next time.")
                    elif think_btn:
                        st.session_state["final_campaign_decision"] = "Think"
                        st.info("You're still thinking…")

# ========== TAB 4: Sponsor Admin ========== 
with tabs[3]:
    st.title("Sponsor Admin Page")

    sp = st.session_state["active_sponsor"]
    if sp is None:
        st.warning("No sponsor campaign accepted by passenger yet.")
    else:
        st.success(f"Sponsor: {sp['sponsor_name']} is active.")
        
        if not st.session_state["profile_sent"]:
            st.info("Passenger has NOT sent their profile yet.")
        else:
            st.markdown("### Passenger's Profile")
            prof = st.session_state["profile"]
            st.write(f"- Name: {prof['name']}")
            st.write(f"- Surname: {prof['surname']}")
            st.write(f"- Age: {prof['age']}")
            st.write(f"- Facebook Friends: {prof['facebook_friends']}")
            st.write(f"- Instagram Followers: {prof['instagram_followers']}")
            st.write(f"- AdOnBoard Friends: {prof['adonboard_friends']}")
            st.write(f"- 'AddOnBoard' friend_count: {prof.get('friend_count',0)}")

            if prof["photo"]:
                st.image(prof["photo"], caption="Passenger's Profile Photo")

            st.markdown("#### Approve or Reject this passenger's profile?")
            dec = st.session_state["sponsor_decision"]
            if dec == "Approved":
                st.success("You have ALREADY Approved this passenger.")
            elif dec == "Rejected":
                st.error("You have Rejected this passenger.")
            else:
                approve_btn = st.button("Approve Passenger")
                reject_btn  = st.button("Reject Passenger")
                if approve_btn:
                    st.session_state["sponsor_decision"] = "Approved"
                    st.success("Passenger Approved!")
                elif reject_btn:
                    st.session_state["sponsor_decision"] = "Rejected"
                    st.error("Passenger Rejected!")
