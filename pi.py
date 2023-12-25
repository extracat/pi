from flask import Flask, request, jsonify
app = Flask(__name__)

file_path = './data/pi_dec_10b.txt'

@app.route('/find_position', methods=['GET'])
def find_position_api():
    string_to_search = request.args.get('string')
    position = findPosition(file_path, string_to_search)
    return jsonify({'position': position})

@app.route('/find_positions', methods=['GET'])
def find_positions_api():
    string_to_search = request.args.get('string')
    positions = findPositions(file_path, string_to_search)
    return jsonify({'positions': positions})

@app.route('/read_from_position', methods=['GET'])
def read_from_position_api():
    start_position = int(request.args.get('start_position'))
    length = int(request.args.get('length'))
    text = readFromPosition(file_path, start_position, length)
    return jsonify({'text': text})

def readFromPosition(file_path, start_position, length):
    with open(file_path, 'r', encoding='utf-8') as file:
        file.seek(start_position)  # Перемещаемся к позиции start_position
        return file.read(length)   # Читаем length символов

def findPosition(file_path, string_to_search):
    string_length = len(string_to_search)
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk_size = 4096  # Размер блока чтения
        overlap = string_length - 1
        prev_chunk_end = ''  # Хранение конца предыдущего блока для перекрытия
        total_read = 0  # Счетчик общего числа прочитанных символов

        while True:
            chunk = file.read(chunk_size)

            # Объединяем конец предыдущего блока с текущим блоком для проверки перекрытия
            combined_chunk = prev_chunk_end + chunk

            position = combined_chunk.find(string_to_search)
            if position >= 0:
                # Возвращаем позицию в файле, учитывая сдвиг, вызванный prev_chunk_end
                return total_read + position - len(prev_chunk_end)

            total_read += len(chunk)

            # Сохраняем часть блока для возможного перекрытия со следующим блоком
            prev_chunk_end = chunk[-overlap:] if len(chunk) >= overlap else chunk

            if not chunk:
                return -1  # Строка не найдена
     
def findPositions(file_path, string_to_search):
    string_length = len(string_to_search)
    positions = []  # Список для хранения всех позиций найденной строки
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk_size = 4096
        overlap = string_length - 1
        prev_chunk_end = ''
        total_read = 0

        while True:
            chunk = file.read(chunk_size)
            if not chunk and not positions:
                return -1  # Строка не найдена

            combined_chunk = prev_chunk_end + chunk

            # Поиск и добавление всех вхождений строки в текущем комбинированном блоке
            start = 0
            while start < len(combined_chunk):
                position = combined_chunk.find(string_to_search, start)
                if position == -1:
                    break
                positions.append(total_read + position - len(prev_chunk_end))
                start = position + string_length

            total_read += len(chunk)

            if len(chunk) < chunk_size:
                break  # Конец файла

            prev_chunk_end = chunk[-overlap:]

    return positions
            
# Использование функции
string_to_search = '1'

if __name__ == '__main__':
    app.run(debug=True)


# position = findPosition(file_path, string_to_search)
# print(f"Позиция: {position:,}") 

# positions = findPositions(file_path, string_to_search)
# print(f"Позиции: {positions}")

# extracted_text = readFromPosition(file_path, position-len(string_to_search), len(string_to_search)*3)
# print(extracted_text)


# while True:
#     position = findPosition(file_path, string_to_search)
#     print(position)
#     
#     if position < 0:
#         break
#     
#     string_to_search = str(int(position))

