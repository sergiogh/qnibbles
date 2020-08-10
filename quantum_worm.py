import random
from qiskit import IBMQ, Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.quantum_info import Statevector

from worm import Worm

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
SPLIT_LR = 'split_lr'

valid_movements = [UP, LEFT, RIGHT, DOWN]

class Quantumworm(Worm):

	def __init__(self, name, width, height, direction, qubits):

		super().__init__(name, width, height, direction)
		startx = random.randint(6, width - 4)
		starty = random.randint(6, height - 4)
		self.coordinates = [{'x': startx,     'y': starty, 'probability': 1.0},
							{'x': startx - 1, 'y': starty, 'probability': 1.0},
							{'x': startx - 2, 'y': starty, 'probability': 1.0}]
		self.qubits = qubits
		# Our Quantum worm may have several heads!
		self.heads = [{'x': self.coordinates[0]['x'], 'y': self.coordinates[0]['y'], 'direction': direction, 'probability': 1}]

	def random_walk(position):
		return False

	def randomQuantumMovement(self, valid_movements):

		# Potential valid movements: L, R, U, L+R (superposition), TOWARDS_APPLE_X * 2, TOWARDS_APPLE_Y  * 2--> 8 possibilities --> 3 qubits
		# Limit superposition to avoid crushing the board
		if(len(self.heads)<4): valid_movements.append(SPLIT_LR)

		# For the moment it takes a naive pure random approach. Therefore the quantum worm is "dumber" than the classical
		qc = QuantumCircuit(3)
		qc.h(range(3))
		qc.measure_all()

		backend = Aer.get_backend("qasm_simulator")
		while True:
			result = execute(qc, backend=backend, shots=1).result().get_counts()
			for t in result:
				result = int(t, 2)

			if (result < len(valid_movements)): break

		print("------")
		print("Q RANDOM MOVEMENT RESULT: ")
		print(valid_movements[result])
		return valid_movements[result]

	def calculateNewQuantumMovement(self, head, board):

		heads = []

		if head['direction'] == UP:
			newHead = {'x': head['x'], 'y': head['y'] - 1, 'direction': UP, 'probability': head['probability']}
			heads.append(newHead)
		elif head['direction'] == DOWN:
			newHead = {'x': head['x'], 'y': head['y'] + 1, 'direction': DOWN, 'probability': head['probability']}
			heads.append(newHead)
		elif head['direction'] == LEFT:
			newHead = {'x': head['x'] - 1, 'y': head['y'], 'direction': LEFT, 'probability': head['probability']}
			heads.append(newHead)
		elif head['direction'] == RIGHT:
			newHead = {'x': head['x'] + 1, 'y': head['y'], 'direction': RIGHT, 'probability': head['probability']}
			heads.append(newHead)

		elif head['direction'] == SPLIT_LR:
			# Check the three possibilities and grow wherever there is space.
			splitted_heads = []
			if (board.getStatus(head['x'] + 1, head['y']) <= 1):
				newHead = {'x': head['x'] + 1, 'y': head['y'], 'direction': LEFT, 'probability': head['probability'] * 0.5}
				splitted_heads.append(newHead)
			if (board.getStatus(head['x'] - 1, head['y']) <= 1):
				newHead = {'x': head['x'] - 1, 'y': head['y'], 'direction': RIGHT, 'probability': head['probability'] * 0.5}
				splitted_heads.append(newHead)
			if (board.getStatus(head['x'], head['y'] - 1) <= 1):
				newHead = {'x': head['x'], 'y': head['y'] - 1, 'direction': UP, 'probability': head['probability'] * 0.5}
				splitted_heads.append(newHead)
			if (board.getStatus(head['x'], head['y'] + 1) <= 1):
				newHead = {'x': head['x'], 'y': head['y'] + 1, 'direction': DOWN, 'probability': head['probability'] * 0.5}
				splitted_heads.append(newHead)

			for splitted_head in splitted_heads:
				splitted_head['probability'] = 1/len(splitted_heads)
			print("==================")
			print("NEW SPLITTED HEADS")
			print(splitted_heads)
			heads += splitted_heads


		print("RESULT OF CALCULATE QuantumWormMovement")
		print(heads)
		return heads

	def calculateQuantumRandomDirection(self, apple, board):

		potential_directions = []

        # Calculate direction for each existing head
		for head in self.heads:

			valid_movements = [UP, LEFT, RIGHT, DOWN]

	        # Add more random weight to tilt towards the apple
			if(apple['x'] > self.coordinates[0]['x']):
				valid_movements.append(RIGHT)
			else:
				valid_movements.append(LEFT)

			if(apple['y'] < self.coordinates[0]['y']):
				valid_movements.append(UP)
			else:
				valid_movements.append(DOWN)

			if head['x'] == 0:
				valid_movements = list(filter(lambda a: a != LEFT, valid_movements))
			if head['x'] >= self.board_width - 1:
				valid_movements = list(filter(lambda a: a != RIGHT, valid_movements))
			if head['y'] == 0:
				valid_movements = list(filter(lambda a: a != UP, valid_movements))
			if head['y'] >= self.board_height - 1:
				valid_movements = list(filter(lambda a: a != DOWN, valid_movements))

			head['direction'] = self.randomQuantumMovement(valid_movements) # Get a random movement
			print("------------------------")
			print("Q INITIAL DIRECTION GUESS: ")
			print(head['direction'])


			if (head['direction'] != SPLIT_LR):
				# Remove non classical potential directions
				valid_movements = [a for a in valid_movements if a not in (SPLIT_LR)]
				print("Q VALID MOVEMENTS: ")
				print(valid_movements)
				change_direction = True

				while(change_direction == True):
					potentialNewHead = self.calculateNewQuantumMovement(head, board)[0]
					print("------------------------")
					print("Q TRY NO SPLIT HEAD")
					print(head)
					if (board.getStatus(potentialNewHead['x'], potentialNewHead['y']) == 1):
						change_direction = True
						valid_movements = list(filter(lambda a: a != head['direction'], valid_movements))   # Remove invalid direction from the list
						print("------------------------")
						print("Q HIT SOMETHING. NEW POTENTIAL MOVEMENTS (no split)")
						print(valid_movements)
						if(len(valid_movements) == 0):
							head['direction'] = ''
							change_direction = False
						else:
							head['direction'] = self.randomMovement(valid_movements)
							print("Q NEW TRY NEW DIRECTION:")
							print(head)

					else:
						change_direction = False


				potential_directions.append(head['direction'])

			## We need to consider whether we are taking a single direction, or we got a quantum split
			elif (head['direction'] in [SPLIT_LR]):
				potentialNewHeads = self.calculateNewQuantumMovement(head, board)
				print("------------------------")
				print("Q POTENTIAL HEADS: ")
				print(potentialNewHeads)
				head_directions = []
				for potentialNewHead in potentialNewHeads:
					if (board.getStatus(potentialNewHead['x'], potentialNewHead['y']) != 1):
						potential_directions.append(potentialNewHead['direction'])



		print("------------------------")
		print("Q ALL HEADS FOR THIS ROUND ")
		print(self.heads)
		print("------------------------")
		print("Q ALL DIRECTIONS FOR THIS ROUND ")
		print(potential_directions)
		return potential_directions

	def killHeadWithoutDirection(self):
		new_heads = []
		for head in self.heads:
			if (len(head['direction']) != 0):
				new_heads.append(head)
		self.heads = new_heads

	def growQuantumWorm(self, board):
		new_heads = []
		for head in self.heads:
			print("GROW FOR HEAD: ")
			print(head)
			if (board.getStatus(head['x'], head['y']) >= 1):
				print("HEAD IMPACTED BOARD: ")
				print(head)
				board.printGrid()
			elif (board.getStatus(head['x'], head['y']) > head['probability']):
				# The head has come back to the snake. We don't kill it but we stop from reproducing. Unless it is the last surviving one
				print("HEAD IMPACTED ITSELF WITH PROBABABILITY: ")
				print(head)
				board.activateCollision(head['x'], head['y'], head['probability'])
				self.coordinates.insert(0, head)
			else:
				print("SAFE HEAD")
				new_heads.append(head)
				self.coordinates.insert(0, head)

		self.heads = new_heads
		if(len(self.heads) == 0):
			self.storeResults()
			self.die()

	def getHeads(self):
		return self.heads

	def __getCoordinatesFromBinary(self, binary_result):
		n = int(binary_result, 2)
		y = int(n / 16) + 1
		x = n - ((y - 1) * 16) + 1
		coordinates = {'x': x, 'y': y}
		return coordinates

	def quantumRandomStartingPoint(self, qubits):
		qc = QuantumCircuit(qubits)
		qc.h(range(qubits))
		qc.measure_all()

		backend = Aer.get_backend("qasm_simulator")
		result = execute(qc, backend=backend, shots=1).result()
		for r in result.get_counts():
			return self.__getCoordinatesFromBinary(r)
