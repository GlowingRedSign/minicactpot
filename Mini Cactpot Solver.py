# Mini-Cactpot Solver provides the user with an optimal choice of line to play
# on a Mini-Cactpot ticket in FFXIV. 

# Mini-Cactpot is played in FFXIV on a 3x3 grid with one uncovered space, 
# revealing a number from 1-9, and the other spaces each hiding a different 
# number from 1-9 with no repeats. The player chooses three more spaces to 
# reveal, then chooses a row, column, or diagonal to play. The chosen
# line is summed, and the user's winnings are determined by comparing the total
# of the chosen line to a payout table.

# This program solves a Mini-Cactpot ticket by asking the user to 
# input the contents of their ticket, and based on this input, 
# determining the expected value #
# of each line. The solution is the line with the highest expected value. 
  

import itertools

ticket = {'a':'X', 'b':'X', 'c':'X', 'd':'X', 'e':'X', 'f':'X', 'g':'X',       
          'h':'X', 'i':'X'}                                   
# This pre-loads the ticket with an X to represent each 
# unrevealed space. As the user inputs the numbers in revealed spaces, those 
# numbers will replace the X in the relevant spaces.
          
available_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9] 
# Mini-Cactpot spaces each contain one number from one to nine, with 
# no repeats.

# getspaces() shows the user a blank ticket with a label for each possible
# space, then ask the user to input the revealed spaces on their Mini-Cactpot
# ticket. It accomplishes this by asking the user to choose the label that 
# matches the space they have revealed, then asking the user to input the 
# value revealed in that space. The values are stored in the dict ticket and
# passed on for solving.

def getspaces(ticket):
    spacesleft = 4 # Each completed ticket has four revealed spaces.
    while spacesleft > 0:
        print 'a | b | c'
        print '__|___|__'
        print 'd | e | f'
        print '__|___|__'
        print 'g | h | i'
        print '  |   |  '
        print "Spaces to reveal: " + str(spacesleft)
        choice = raw_input("Please choose the letter that matches the " + 
        "revealed space: ")
        value = int(raw_input("Please enter the number in that space: "))
        ticket[choice] = value
        available_numbers.remove(value)

        print "This is what your ticket looks like so far:"
        print str(ticket['a']) + ' |' + str(ticket['b']) + ' |' \
        + str(ticket['c'])
        print '__|__|__'
        print str(ticket['d']) + ' |' + str(ticket['e'] )+ ' |' \
        + str(ticket['f'])
        print '__|__|__'
        print str(ticket['g']) + ' |' + str(ticket['h']) + ' |' \
        + str(ticket['i'])
        print '  |  |  '
        spacesleft -= 1        
    return(ticket)
ticket = getspaces(ticket)

# Prints a representation of the ticket with the revealed values in their
# spaces so the user can confirm that they input the revealed spaces correctly.
print "Here's what your completed ticket looks like: "
print str(ticket['a']) + ' |' + str(ticket['b']) + ' |' + str(ticket['c'])
print '__|__|__'
print str(ticket['d']) + ' |' + str(ticket['e'] )+ ' |' + str(ticket['f'])
print '__|__|__'
print str(ticket['g']) + ' |' + str(ticket['h']) + ' |' + str(ticket['i'])
print ''

print "Here are the possible lines you can choose: "
print '4 5   6   7 8'
print '3   |   |  '
print '  __|___|__'
print '2   |   |  '
print '  __|___|__'
print '1   |   |  '
print '    |   |  '


lines = [[], [], [], [], [], [], [], [], []] # List of possible payout lines.
lines[1] = [ticket['g'], ticket['h'], ticket['i']]
lines[2] = [ticket['d'], ticket['e'], ticket['f']]
lines[3] = [ticket['a'], ticket['b'], ticket['c']]
lines[4] = [ticket['a'], ticket['e'], ticket['i']]
lines[5] = [ticket['a'], ticket['d'], ticket['g']]
lines[6] = [ticket['b'], ticket['e'], ticket['h']]
lines[7] = [ticket['c'], ticket['f'], ticket['i']]
lines[8] = [ticket['c'], ticket['e'], ticket['g']]

# "table" correlates the possible total numbers with the number
# of possible combinations of the available unrevealed numbers that would add 
# up to that total number, and the payout for that total number. 
# These numbers will be used to compute the Expected Value of choosing a 
# particular line. table[key][0] is the number of possibilities, while
# table[key][1] is the payout if the total of the chosen line is table[key].
# Payout values are taken from a Mini-Cactpot ticket inside FFXIV, and are the
# same for all Mini-Cactpot tickets.

table = {6:[0,10000], 7:[0,36], 8:[0,720], 9:[0,360], 10:[0,80],
         11:[0,252], 12:[0,108], 13:[0,72], 14:[0,54], 15:[0,180],
         16:[0,72], 17:[0,180], 18:[0,119], 19:[0,36], 20:[0,306],
         21:[0,1080], 22:[0,144], 23:[0,1800], 24:[0,3600]}


# This block generates a solution to the ticket by reading each line of the 
# ticket as the user has input it, and computing the expected value of choosing
# that line. The expected value is determined by weighting the value of each
# possible total's payout by the likelihood that the line will add up to that 
# total, then summing the weighted payouts for each line.

solution = ''
solution_payout = 0

for number in range(1,9): #Iterates across all the possible payout lines.
    table = {6:[0,10000], 7:[0,36], 8:[0,720], 9:[0,360], 10:[0,80],
         11:[0,252], 12:[0,108], 13:[0,72], 14:[0,54], 15:[0,180],
         16:[0,72], 17:[0,180], 18:[0,119], 19:[0,36], 20:[0,306],
         21:[0,1080], 22:[0,144], 23:[0,1800], 24:[0,3600]}
    unknowns = 0
    possibilities = []
    revealed_total = 0
    expected_value = 0
    possible_lines = 0
    for space in lines[number]: 
        if space == 'X': # This happens when the space is still unrevealed.
            unknowns += 1
        if space != 'X': # This happens when the user input a revealed value.
            revealed_total += space
    number_of_Xs = unknowns
    while number_of_Xs > 0:
        lines[number].remove('X')
        number_of_Xs -= 1 #Removes each 'X' marker to allow arithmetic.
    possibilities = list(itertools.permutations(available_numbers, unknowns))
    # Generates a list of all possibile permutations of available numbers
    # of length equal to unknowns
    for permutation in possibilities:
        line_total = 0
        for digit in permutation:
            line_total += digit
        line_total += revealed_total
        table[line_total][0] += 1
	# table[line_total][0] keeps track of the number of possibilities for
        # each line_total.
    for total in table:
        # Adds up the number of possible lines by adding up the number of
        # possibilities for each line total.
        possible_lines += table[total][0]
    for total in table:
        likelihood = table[total][0] / float(possible_lines)
        expected_value += likelihood * table[total][1]
    print "If you choose line " + str(number) + " your expected payout is: "
    print expected_value
    if expected_value > solution_payout:
        solution = str(number)
        solution_payout = expected_value

print "\nThe best choice is line " + solution + " with an expected payout of:"
print solution_payout

raw_input()
