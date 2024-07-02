import numpy as np


class FormState:
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
        alphabet = form_data["alphabet"]
        key = form_data["matrix_key"]
        message = form_data["message"]
        message_list = [char for char in message]

        # Define the number of matrix columns and rows
        list_e=key.split(',')
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

        print(matrix_inverse)
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
        # numbers_matrix
        # matrix_letters=matrix_finish
        
        # multiply = np.dot (B,A)
        # self.result.append(multiply)
        # Print the result
        print("Result:", self.result)

# Example usage
form_data_example = {
    "alphabet": "ABCDEFGHIJKLMN1OPQRSTUVWXYZ_",
    "matrix_key": "4,3,1,2,2,1,1,1,1",
    "message": "A_FJKLÑOJA_N"
}

form_state = FormState()
form_state.handle_submit(form_data_example)
