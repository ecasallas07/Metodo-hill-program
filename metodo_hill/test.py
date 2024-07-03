import numpy as np


class Decrypt:
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
        matrix_finish = np.transpose(matrix_finish).tolist()
        
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

# Example usage
form_data_example = {
    "alphabet": "ABCDEFGHIJKLMN1OPQRSTUVWXYZ_",
    "matrix_key": "4,3,1,2,2,1,1,1,1",
    "message": "A_FJKLÑOJA_N"
}

form_state = Decrypt()
form_state.handle_submit(form_data_example)


class Encrypt:
    form_data = {}
    result = []
    

    def handle_submit(self,form_data:dict):
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


form_data_example = {
    "alphabet": "ABCDEFGHIJKLMN1OPQRSTUVWXYZ_",
    "matrix_key": "4,3,1,2,2,1,1,1,1",
    "message": "HOLA_MUNDO"
}

encrypt = Encrypt()
encrypt.handle_submit(form_data_example)