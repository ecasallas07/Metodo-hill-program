"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import numpy as np
from rxconfig import config


# Back-end
class Decrypt(rx.State):
    form_data = {}
    result = []
    
    def split_matrix(self, elements, n):
        arr = list(elements)
        return [arr[i:i+int(n)] for i in range(0, len(arr), int(n))]

    def matrix_reverse(self, arr):
        np_matrix = np.array(arr,dtype=int)
        try:
            inv_matrix = np.linalg.inv(np_matrix)
            return inv_matrix.tolist()
        except np.linalg.LinAlgError as e:
            return str(e)

    def handle_submit(self, form_data: dict):
        
        self.result = []
        alphabet = form_data["alphabet"]
        key = form_data["matrix_key"]
        message = form_data["message"]
        message_list = [char for char in message]

        # Define the number of matrix columns and rows
        list_e=key.split(',')
        print(key)
        n_matrix = abs(len(list_e) / 3)
      
        # Array to save numbers of letters 
        message_numbers = []

        # Organize by rows
        matrix_key = self.split_matrix(list_e,n_matrix)
        # reverse matrix
        matrix_inverse = self.matrix_reverse(matrix_key)
       
       
        #calculate matrix inverse for mod 27 or 28  
        if len(alphabet) == 27:
            for i in range(len(matrix_inverse)):
                for j in range(len(matrix_inverse[i])):
                    matrix_inverse[i][j] = matrix_inverse[i][j] % 27
        elif len(alphabet) == 28:
            for i in range(len(matrix_inverse)):
                for j in range(len(matrix_inverse[i])):
                    matrix_inverse[i][j] = matrix_inverse[i][j] % 28
                    
        # matrix module finished            
        matrix_inverse_int = [[int(round(matrix_inverse[i][j])) for j in range(len(matrix_inverse[i]))] for i in range(len(matrix_inverse))]
        
        # Verification that message count is a multiple of n_matrix
        while True:
            if len(message_list) % n_matrix != 0:   
                message_list.append('_')
                continue
            else:
                break

        # Convert message to matrix with number representation
        # print(message_list)
        alphabet_dict = {}

        if len(alphabet) == 27:
            alphabet_dict = {chr(65+i): i for i in range(26)}
            print(alphabet_dict)
            alphabet_dict["_"] = 26
        elif len(alphabet) == 28:
            alphabet_dict = {chr(65+i): i for i in range(14)}
            alphabet_dict["Ñ"] = 14
            alphabet_dict.update({chr(65+i-1): i for i in range(15, 27)})
            alphabet_dict["_"] = 27

        message_list = [char.upper() for char in message_list]
        for char in message_list:
            if char in alphabet_dict:
                message_numbers.append(alphabet_dict[char])
        
        matrix_finish = self.split_matrix(message_numbers, n_matrix)
        print("matrx finish:",matrix_finish)
        matrix_finish_np = np.array(matrix_finish)
        matrix_finish = np.transpose(matrix_finish_np).tolist()
        
        # multiply matrix and inverse matrix  to decrypt message
        multiply = np.dot(matrix_inverse_int,matrix_finish).tolist()
        
        if len(alphabet) == 27:
            for i in range(len(multiply)):
                for j in range(len(multiply[i])):
                    multiply[i][j]= multiply[i][j] % 27
        elif len(alphabet) == 28:
            for i in range(len(multiply)):
                for j in range(len(multiply[i])):
                    multiply[i][j]= multiply[i][j] % 28                    
                
            
        matrix_letters=np.transpose(multiply)
        
            
        # invert alphabte for acces  to letters . how invert the dictionary
        reversed_alphabet_dict = {v: k for k, v in alphabet_dict.items()}
        
        #matrix messagge decrypt
        letter_decrypt= []
                
        for i in range(len(matrix_letters)):
            for j in range(len(matrix_letters[i])):
                num = matrix_letters[i][j]
                if num in reversed_alphabet_dict:
                    letter_decrypt.append(reversed_alphabet_dict[num])

        self.result.append(letter_decrypt)
        
        # Print the result
        print("Result:", self.result)
    
    
class Encrypt(rx.State):
    
    
    
    form_data = {}
    result = []

    
    def split_matrix(self, elements, n):
        arr = list(elements)
        return [arr[i:i+int(n)] for i in range(0, len(arr), int(n))]
    
    def handle_submit(self,form_data:dict):
        
        self.result = []
        alphabet =  form_data['alphabet']
        key = form_data['matrix_key']
        message = form_data['message']
        message_list = [char for char in message]
        
        list_e=key.split(',')
        n_matrix = abs(len(list_e) / 3)
        
        self.split_matrix(list_e,n_matrix)
        
        
        message_numbers = []


        # Organize by rows
        matrix_key = self.split_matrix(list_e,n_matrix)

        
        while True:
            if len(message_list) % n_matrix != 0:   
                message_list.append('_')
                continue
            else:
                break
            
            
        alphabet_dict = {}

        if len(alphabet) == 27:
            alphabet_dict = {chr(65+i): i for i in range(26)}
            #chr(65+i): La función chr() toma un número entero (código ASCII) y devuelve su carácter correspondiente. 65 es el código ASCII de la letra 'A'.
            # Entonces, chr(65+i) generará los caracteres ASCII consecutivos
            # empezando desde 'A'. Por ejemplo, cuando i es 0, chr(65+0) es 'A'. Cuando i es 1, chr(65+1) es 'B', y así sucesivamente hasta 'Z'.
            print(alphabet_dict)
            alphabet_dict["_"] = 26
        elif len(alphabet) == 28:
            print("Ingreso aqui")
            alphabet_dict = {chr(65+i): i for i in range(14)}
            alphabet_dict["Ñ"] = 14
            alphabet_dict.update({chr(65+i-1): i for i in range(15, 27)})
            alphabet_dict["_"] = 27    
        
        
        message_list = [char.upper() for char in message_list]
        for char in message_list:
            if char in alphabet_dict:
                message_numbers.append(alphabet_dict[char])            
        
        
        matrix_finish = self.split_matrix(message_numbers, n_matrix)
        matrix_finish = np.transpose(matrix_finish).tolist()        
        
        
        # with this code solution problem --->    ValueError: data type must provide an itemsize
        matrix_key = np.array(matrix_key, dtype=int)
        matrix_finish = np.array(matrix_finish, dtype=int)
        
        multiply = np.dot(matrix_key,matrix_finish).tolist()
        
        if len(alphabet) == 27:
            for i in range(len(multiply)):
                for j in range(len(multiply[i])):
                    multiply[i][j] = multiply[i][j] % 27
        elif len(alphabet) == 28:
            for i in range(len(multiply)):
                for j in range(len(multiply[i])):
                    multiply[i][j] = multiply[i][j] % 28
        multiply_end =np.transpose(multiply).tolist()
        
        reversed_alphabet_dict = {k:v for v, k in alphabet_dict.items()}
        letter_encrypt= []
                
        for i in range(len(multiply_end)):
            for j in range(len(multiply_end[i])):
                num = multiply_end[i][j]
                if num in reversed_alphabet_dict:
                    letter_encrypt.append(reversed_alphabet_dict[num])

        self.result.append(letter_encrypt)
        print("Result: ",self.result)
    

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
                    href="/machine-hill",
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


def decrypt_form():
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
                                    ["ABCDEFGHIJKLMNOPQRSTUVWXYZ_","ABCDEFGHIJKLMN1OPQRSTUVWXYZ_"],
                                    name="alphabet",    
                                    required=True,
                                ),
                            rx.button(
                                "Decrypt",
                                type_="submit",
                                bg="#ecfdf5",
                                background_color="#3683D5",
                                border_radius="lg",
                                margin_top="10px",
                                cursor="pointer",
                            ),
                            rx.button(
                                "Clear",
                                type_="button",
                                bg="#ecfdf5",
                                background_color="#B74B4B",
                                border_radius="lg",
                                margin_top="10px",
                                cursor="pointer",
                                on_click=[
                                    rx.set_value("message", ""),
                                    rx.set_value("matrix_key", ""),
                                ]
                            ),
                        ),
                        on_submit=Decrypt.handle_submit,
                        reset_on_submit=True,
                    ),
                    rx.divider(),
                    rx.heading("Results"),
                    rx.text(Decrypt.result.to_string()),
                    width="100%",
                ),
                value="tab1",
            ),
            rx.tabs.content(
                rx.vstack(
                    rx.form(
                        rx.heading("Encrypt the message", size="7", margin_bottom="20px"),
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
                                    ["ABCDEFGHIJKLMNOPQRSTUVWXYZ_","ABCDEFGHIJKLMN1OPQRSTUVWXYZ_"],
                                    name="alphabet",    
                                    required=True,
                                ),
                            rx.button(
                                "Encrypt",
                                type_="submit",
                                bg="#ecfdf5",
                                background_color="#3683D5",
                                border_radius="lg",
                                margin_top="10px",
                                cursor="pointer",
                            ),
                             rx.button(
                                "Clear",
                                type_="button",
                                bg="#ecfdf5",
                                background_color="#B74B4B",
                                border_radius="lg",
                                margin_top="10px",
                                cursor="pointer",
                                on_click=[
                                    rx.set_value("message", ""),
                                    rx.set_value("matrix_key", ""),
                                ]
                            ),
                        ),
                        on_submit=Encrypt.handle_submit,
                        reset_on_submit=True,
                    ),
                    rx.divider(),
                    rx.heading("Results"),
                    rx.text(Encrypt.result.to_string()),
                    width="100%",
                ),
                value="tab2",
            ),
            default_value="tab1",
            orientation="horizontal",
        ),
    )


app = rx.App()
app.add_page(index)
app.add_page(decrypt_form, route="/machine-hill")
