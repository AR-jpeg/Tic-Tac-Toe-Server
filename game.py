from __future__ import annotations
from typing import Dict, List, Union
from dataclasses import dataclass

class Utils:
	@staticmethod
	def converListToString(l: List):
		res = ""
		for e in l:
			res += str(e)

		return res

	@staticmethod
	def createSubStrings(l: Union(str, list), size: int) -> List[str]:
		if type(s) == list:
			s = Utils.convertListToString(s)

		res: List[str] = []

		for i in range(0, len(s)+1):
			for j in range(i, len(s)+1):
				if len(s[i:j]) != size:
					continue
				
				res.append(s[i:j])

		return res

	@staticmethod
	def allElementsSame(list: List[object], options: GameOptions) -> bool:
		if len(set(list)) > 1:
			return False

	@staticmethod
	def findPlayerWithSymbol(players: List[Dict[str, str]], symbol: str) -> str:
		for player in players:
			if player["symbol"] == symbol:
				return player["name"]

		return -1

@dataclass
class Player:
	name: str
	symbol: str

@dataclass
class GameOptions:
	players: List[Player]
	numberOfPlayers: int
	minSizeToWin: int
	boardSize: int
	EMPTY: str

@dataclass
class Point:
	x: int # Grids
	y: int # Collumns

@dataclass
class Board:
	options: GameOptions
	board: List[List[str]]

	def getSymbolAtPoint(self, point: Point):
		return self.board[point.y][point.x]		

	def isPointEmpty(self, point: Point):
		if self.getSymbolAtPoint(point) != self.options.EMPTY:
			return False

		return True

	def setSymbolAtPoint(self, move: Point, symbol: str):
		# Assumes the move is empty
		self.board[move.y][move.x] = symbol

	def gameOver(self, players):
		patternsToCheck = []

		for line in self.board:
			# Add horizontal patterns
			for subPattern in Utils.createSubStrings(line, self.options.minSizeToWin):
				patternsToCheck.append(subPattern)

		# Add the collumns
		collumns: List[List] = []

		for verticlePointer in range(0, len(self.board[0])):
			collumns.append([])

			for line in self.board:
				collumns[verticlePointer].append(line[verticlePointer])

		for collumn in collumns:
			for subPattern in Utils.createSubStrings(collumn, self.options.minSizeToWin):
				patternsToCheck.append(subPattern)

		# Add the top left -> bottom right diagonal
		tl_br_diagonal = []
		for i in range(len(self.board)):
			tl_br_diagonal.append(self.board[i][i])

		for subPattern in Utils.createSubStrings(tl_br_diagonal, self.options.minSizeToWin):
			patternsToCheck.append(subPattern)

		# Add the bottom left -> top right diagonal
		bl_tr_diagonal = []
		for i in range(len(self.board)-1, -1,-1):
			bl_tr_diagonal.append(list(reversed(self.board[i]))[i])

		for subPattern in Utils.createSubStrings(bl_tr_diagonal, self.options.minSizeToWin):
			patternsToCheck.append(subPattern)


		for pattern in patternsToCheck:
			if Utils.allElementsSame(pattern) and set(pattern) != set([self.options.EMPTY]):
				# Return who won, not just the symbol
				return True, Utils.findPlayerWithSymbol(players, pattern[0])
		
		return False, ""

	@staticmethod
	def createBoard(options: GameOptions) -> List[List[str]]:
		board: List[List[str]] = []

		for i in range(options.boardSize):
			board.append([])
			for k in range(options.boardSize):
				board[i].append(options.EMPTY)

class Game:
	def __init__(self, options: GameOptions, gameId: int) -> None:
		# Setup the gameboard
		self.board = Board()
		self.board.options = options
		self.board = Board.createBoard(options)

		self.minSizeToWin = options.minSizeToWin
		self.players: List[Player] = []
		self.options = options
		self.id = gameId

		self.playersConnected: int = 0
		self.nextPlayerToMove: int = 0

	def setMove(self, move: Point, symbol: str):
		if not self.board.isPointEmpty(move):
			return -1

		if move.x > len(self.board) - 1 or move.y > len(self.board):
			return -1
		
		self.board.setSymbolAtPoint(move, symbol)
		return 1

	def createPlayer(self, player: Player):
		# Before we add the new player in, we need to make sure that the name
		# and symbol aren't already being used by another player.
		for p in self.players:
			if p.name == player.name:
				return -1
			
			if p.symbol == player.symbol:
				-1

		# Also make sure that that player's symbol isn't more than 1 character long
		if len(player.symbol) > 1:
			return -1

		self.players.append(player)
		
		return 1


# def createGame(options: GameOptions):
# 	players = options.players
# 	mainBoard = options.mainBoard
# 	minSizeToWin = options.minSizeToWin

	# while not stop:
	# 	for p in players:
	# 		if gameOver(mainBoard, minSizeToWin)[0]:
	# 			clearScreen()
	# 			printGameBoard(mainBoard)

	# 			fancyPrint(f"{ findPlayerWithSymbol(players, gameOver(mainBoard, minSizeToWin)[1]) } won, GG!", globals.GREEN)
				
	# 			stop = True
	# 			break


	# 		clearScreen()

	# 		fancyPrint(f"{p['name']}, it is now your turn. \n", globals.BLUE)
	# 		printGameBoard(mainBoard)
	# 		print("\n")

	# 		playerGrid = fancyInput("Which row would you like to place your move in? ", globals.GREEN, int) - 1
	# 		playerCollumn = fancyInput("Which collumn would you like to place your move in? ", globals.GREEN, int) - 1

	# 		playerMove = (playerGrid, playerCollumn)

	# 		# Make sure the move is always valid
	# 		while True:
	# 			try:
	# 				if isMoveValid(mainBoard, playerMove):
	# 					# Only break once the move was valid
	# 					break

	# 			except errors.SqareOutOfBoundsError:
	# 				clearScreen()

	# 				fancyPrint(f"{p['name']}, your move of ({playerGrid+1}, {playerCollumn+1}) " + 
	# 				"was not a valid move because it was out of bounds, please try entering another move! \n", globals.RED)

	# 				printGameBoard(mainBoard)

	# 				playerGrid = fancyInput("Which row would you like to place your move in? ", globals.GREEN, int) - 1
	# 				playerCollumn = fancyInput("Which collumn would you like to place your move in? ", globals.GREEN, int) - 1

	# 				playerMove = (playerGrid, playerCollumn)

	# 			except errors.SquareAlreadyTakenError:
	# 				clearScreen()

	# 				fancyPrint(f"{p['name']}, your move of ({playerGrid+1}, {playerCollumn+1}) " + 
	# 				"was not a valid move because the square you were trying to move at was already taken, please try entering another move! \n", globals.RED)

	# 				printGameBoard(mainBoard)

	# 				playerGrid = fancyInput("Which row would you like to place your move in? ", globals.GREEN, int) - 1
	# 				playerCollumn = fancyInput("Which collumn would you like to place your move in? ", globals.GREEN, int) - 1

	# 				playerMove = (playerGrid, playerCollumn)

	# 		# Once the move has been validated, set the move and move on to the next player
	# 		setMove(mainBoard, playerMove, p['symbol'])
