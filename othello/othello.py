class Othello:

    Y_EMOJIS = [':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:', ':regional_indicator_d:', ':regional_indicator_e:', ':regional_indicator_f:', ':regional_indicator_g:', ':regional_indicator_h:']
    X_EMOJI = '\n\n:small_blue_diamond::zero::one::two::three::four::five::six::seven:\n'

    ABLE = ":white_small_square:"
    EMPTY = ":small_orange_diamond:"
    BLACK = ":new_moon:"
    WHITE = ":full_moon:"

    output = ''

    is_playing = False
    is_show_hint = False

    board = []
    reversible = []
    putable = []

    current_turn = BLACK

    def start(self):

        self.board = [[self.EMPTY] * 8 for i in range(8)]
        self.reversible = [[False] * 8 for i in range(8)]
        self.putable = [[False] * 8 for i in range(8)]

        self.board[3][3] = self.WHITE
        self.board[3][4] = self.BLACK
        self.board[4][3] = self.BLACK
        self.board[4][4] = self.WHITE
        self.is_playing = True
        self.output = 'ゲームを開始したよ。'
        self.output += self.get_turn_text()
        self.output += self.get_board_text()

    def finish(self):
        self.is_playing = False
        self.output = 'ゲームを中断したよ。'
        self.output += self.get_result_text()

    def toggle_hint(self):
        self.is_show_hint = not self.is_show_hint
        self.output = 'ヒント表示を{0}にしたよ。'.format('ON' if self.is_show_hint else 'OFF')
        self.output += self.get_turn_text()
        self.output += self.get_board_text()

    def put(self, x, y):
        if not self.is_playing:
            self.output = 'ゲームが開始されてないよ。'
            return
        
        if x >= 8 or y >= 8 or self.board[y][x] != self.EMPTY or not self.check_reversible(x, y, self.current_turn):
            self.output = 'そこには置けないよ。'
            return

        self.board[y][x] = self.current_turn
        for y, line in enumerate(self.board):
            for x, cell in enumerate(line):
                if self.reversible[y][x]:
                    self.board[y][x] = self.current_turn
        
        self.current_turn = self.get_next_turn(self.current_turn)
        self.output = self.get_turn_text()
        self.output += self.get_board_text()
        if self.check_finished():
            self.is_playing = False
            self.output = '決着がついたよ。'
            self.output += self.get_result_text()
            return
        
        if not self.check_putable(self.current_turn):
            self.current_turn = self.get_next_turn(self.current_turn)
            self.output += '置く場所がないよ。'
            self.output += self.get_turn_text()
            self.output += self.get_board_text()
            return
        
    def check_reversible(self, x, y, turn):
        isReversible = False
        directions = [
            [-1, -1],
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0]
        ]
        self.reversible = [[False] * 8 for i in range(8)]
        
        for direction in directions:
            targetX = x + direction[1]
            targetY = y + direction[0]
            myStoneExists = False
            while self.check_board_end(targetX, targetY):
                if self.board[targetY][targetX] == self.get_next_turn(turn):
                    targetX += direction[1]
                    targetY += direction[0]
                    continue
                elif self.board[targetY][targetX] == turn:
                    myStoneExists = True
                    break
                else:
                    myStoneExists = False
                    break

            if not myStoneExists:
                continue

            targetX = x + direction[1]
            targetY = y + direction[0]
            while self.check_board_end(targetX, targetY):
                if self.board[targetY][targetX] == self.get_next_turn(turn):
                    self.reversible[targetY][targetX] = True
                    targetX += direction[1]
                    targetY += direction[0]
                    isReversible = True
                else:
                    break
        return isReversible

    def check_putable(self, turn):
        isPutable = False
        self.putable = [[False] * 8 for i in range(8)]
        for y, line in enumerate(self.board):
            for x, cell in enumerate(line):
                if cell == self.EMPTY and self.check_reversible(x, y, turn):
                    isPutable = True
                    self.putable[y][x] = True
        return isPutable

    def check_finished(self):
        emptyCount = 0
        if not self.check_putable(self.BLACK) and not self.check_putable(self.WHITE):
            return True
        
        for line in self.board:
            for cell in line:
                emptyCount += 1 if cell == self.EMPTY else 0
        
        return True if emptyCount == 0 else False
    
    def check_board_end(self, x, y):
        return 7 >= x and x >= 0 and 7 >= y and y >= 0

    def get_next_turn(self, turn):
        return self.WHITE if turn == self.BLACK else self.BLACK

    def get_board_text(self):
        text = self.X_EMOJI
        self.check_putable(self.current_turn)
        for y, line in enumerate(self.board):
            text += self.Y_EMOJIS[y]
            for x, cell in enumerate(line):
                if self.is_show_hint and self.putable[y][x] and cell == self.EMPTY:
                    text += self.ABLE
                else:
                    text += cell

            text += '\n'

        return text

    def get_result_text(self):
        text = self.X_EMOJI
        black_count = 0
        white_count = 0
        for line in self.board:
            for cell in line:
                if cell == self.BLACK:
                    black_count += 1
                elif cell == self.WHITE:
                    white_count +=1

        bc = black_count
        wc = white_count
        for y, line in enumerate(self.board):
            text += self.Y_EMOJIS[y]
            for x, cell in enumerate(line):
                if bc > 0:
                    bc -= 1
                    text += self.BLACK
                elif wc > 0:
                    wc -= 1
                    text += self.WHITE
                else:
                    text += self.EMPTY

            text += '\n'
        

        text += '\n{0}×{1}'.format(self.BLACK, black_count)
        text += '\n{0}×{1}'.format(self.WHITE, white_count)
        if black_count != white_count:
            text += '\n{0}のかち。'.format(self.BLACK if black_count > white_count else self.WHITE)
        else:
            text += '\n\nひきわけ。マジやばくね。'

        return text

    def get_turn_text(self):
        return '\n{0}のターンだよ。'.format(self.current_turn)


