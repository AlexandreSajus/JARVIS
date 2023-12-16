from taipy.gui import Gui, State, invoke_callback, get_state_id
import time
from threading import Thread

conversation = {"Conversation": []}


def style_conv(state: State, idx: int, row: int) -> str:
    """
    Apply a style to the conversation table depending on the message's author.

    Args:
        - state: The current state of the app.
        - idx: The index of the message in the table.
        - row: The row of the message in the table.

    Returns:
        The style to apply to the message.
    """
    if idx is None:
        return None
    elif idx % 2 == 0:
        return "user_message"
    else:
        return "gpt_message"


selected_row = [1]

page = """
<|layout|columns=300px 1|
<|part|render=True|class_name=sidebar|
# Taipy **Chat**{: .color-primary} # {: .logo-text}
<|New Conversation|button|class_name=fullwidth plain|id=reset_app_button|>
|>

<|part|render=True|class_name=p2 align-item-bottom table|
<|{conversation}|table|style=style_conv|show_all|width=100%|rebuild|selected={selected_row}|>
<|part|class_name=card mt1|
|>
|>
|>
"""

state_id_list = []


def on_init(state: State):
    state_id = get_state_id(state)
    state_id_list.append(state_id)


def client_handler(gui, state_id_list):
    while True:
        time.sleep(0.5)
        if len(state_id_list) > 0:
            invoke_callback(gui, state_id_list[0], update_conv, [])


def update_conv(state):
    # Read conv.txt
    with open("conv.txt", "r") as f:
        conv = f.read()
    # Add each lines as a list in conversation
    conversation["Conversation"] = conv.split("\n")
    state.conversation = conversation
    state.selected_row = [len(state.conversation["Conversation"]) - 1]


gui = Gui(page)

t = Thread(
    target=client_handler,
    args=(
        gui,
        state_id_list,
    ),
)
t.start()

gui.run(debug=True, dark_mode=True, use_reloader=True)
