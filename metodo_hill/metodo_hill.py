"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import numpy as np
from rxconfig import config


# Back-end
class FormState(rx.State):
    form_data = {}

    def split_matrix(elements,n):
        arr=list(elements)
        return [arr[i:i+n] for i in range(0,len(arr),n)] # range(start,stop,step)
        
    def matrix_reverse(arr):
        np_matrix = np.array(arr)
        
        try:
            inv_matrix =np.linalg.inv(np_matrix)
            return inv_matrix.tolist()
        except np.linalg.LinAlgError as e:
            return str(e)
        
    result =""
    def handle_submit(self, form_data: dict):

        alphabet = form_data["alphabet"]
        key = form_data["matrix_key"]
        message = form_data["message"]
        message_list = [char for char in message]
        
    
        # deinifition number matrix columns and rows
        n_matrix = len(key) / 3
        
        # array save  numbers of letter 
        message_numbers = []
        
        # convert matrix key
        list = key.split(',') # se organizo por filas
        matrix_key = self.split_matrix(list, n_matrix)
        self.matrix_reverse(matrix_key)
        
        
        
        # verification message count is multiplied by n_matrix
        while True :
            if len(message_list) % n_matrix != 0:
                message_list.append('_')
                continue
            else:
                break
                
        # Convert message en matrix with representation numbers
        if alphabet[1:3] == 27:
            alphabet = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,"T":19,"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25,"_":26}
            message_list.upper()
            for i in message_list:
                if i in alphabet.key():
                    message_numbers.append(alphabet.item())
            self.split_matrix(message_numbers,n_matrix)
        elif alphabet[1:3] == 28:
            if 'ñ'.upper() in message_list:
                message_list.remove('ñ'.upper())
                message_list.append('1')
            
            alphabet = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"1":14,"O":15,"P":16,"Q":17,"R":18,"S":19,"T":20,"U":21,"V":22,"W":23,"X":24,"Y":25,"Z":26,"_":27}
            message_list.upper()
            for i in message_list:
                if i in alphabet.key():
                    message_numbers.append(alphabet.item())
            self.split_matrix(message_numbers,n_matrix)            


# Front-end
def action_bar() -> rx.Component:
    return rx.hstack(rx.input(placeholder="message encription"), rx.button("Start"))


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.box(
            rx.vstack(
                rx.heading("Enigma machine", size="9"),
                rx.text(
                    "Decrypts hidden messages",
                    rx.text.strong(" with the hill method"),
                    size="5",
                ),
                rx.link(
                    rx.button(
                        "Start",
                        color="white",
                        background_color="#D14747",
                        border_radius="5px",
                        padding="10px",
                        margin_bottom="10px",
                        cursor="pointer",
                        font_size="25px",
                    ),
                    href="/machine",
                    is_external=False,
                ),
                spacing="5",
                justify="center",
                min_height="85vh",
                width="600px",
            ),
            rx.image(
                src="machine-image.png",
                width="500px",
                height="auto",
                margin_left="100px",
            ),
            display="flex",
            flex_direction="row",
            justify_content="space-between",
            align_items="center",
            width="1000px",
        ),
    )


def machine():
    return rx.container(
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Decrypt", value="tab1"),
                rx.tabs.trigger("Encrypt", value="tab2"),
                display="flex",
                justify_content="center",
                margin_bottom="20px",
            ),
            rx.tabs.content(
                rx.vstack(
                    rx.form(
                        rx.heading("Discover the message", size="7", margin_bottom="20px"),
                        rx.vstack(
                            rx.input(
                                id="message",
                                type_="text",  
                                width="100%",   
                                height="auto",
                                padding="10px",
                                border="1px solid #ccc",
                                border_radius="5px",
                                margin_bottom="20px",
                                style={
                                "text-align": "left"
                                }
                            ),
                            rx.heading(
                                "Write the matrix by commas",size="5"
                            ),
                            rx.text(
                                "Example: "    
                            ),
                            rx.box(
                                rx.image(
                                    src="/example.png",
                                    width="500px",
                                    height="auto",
                                    margin_left="100px",
                                    ),
                            ),
                            rx.input(placeholder="Matrix", id="matrix_key"),
                            rx.heading("Alphabet:",size="5"),
                                rx.radio(
                                    ["(27 char. A=0) ABCDEFGHIJKLMNOPQRSTUVWXYZ_","(28 char. A=0) ABCDEFGHIJKLMN1OPQRSTUVWXYZ_"],
                                    name="alphabet",    
                                    required=True,
                                ),
                            rx.button(
                                "Decrypt",
                                type_="submit",
                                bg="#ecfdf5",
                                background_color="#B74B4B",
                                border_radius="lg",
                                margin_top="10px",
                                cursor="pointer",
                            ),
                        ),
                        on_submit=FormState.handle_submit,
                    ),
                    rx.divider(),
                    rx.heading("Results"),
                    rx.text(FormState.result),
                    width="100%",
                ),
                value="tab1",
            ),
            rx.tabs.content(
                rx.text("item on tab 2"),
                value="tab2",
            ),
            default_value="tab1",
            orientation="horizontal",
        ),
    )


app = rx.App()
app.add_page(index)
app.add_page(machine, route="/machine")
