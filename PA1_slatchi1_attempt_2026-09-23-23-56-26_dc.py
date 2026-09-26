"""CMSC 471 PA1: DOGCAT. Sai Latchi.

AI assistance: ChatGPT/Codex helped me check my code and format it correctly and in order.
See pa01.pdf for the heuristic explanations and disclosure.
"""

import gzip
from pathlib import Path

import search


dict_file = Path( __file__ ).with_name( 'words34.txt.gz' )
dictionary = {}
with gzip.open( dict_file, 'rt' ) as dictionary_stream:
    for record in dictionary_stream:
        vocab_word, rarity_score = record.split( )
        dictionary[ vocab_word ] = float( rarity_score )

# Use the letter values given in the assignment.
SCRABBLE = {}
for characters, letter_value in [ ( 'aeioulnstr', 1 ), ( 'dg', 2 ), ( 'bcmp', 3 ),
                        ( 'fhvwy', 4 ), ( 'k', 5 ), ( 'jx', 6 ), ( 'qz', 10 ) ]:
    for character in characters:
        SCRABBLE[ character ] = letter_value

# Cheapest rarity for a letter at a particular position and word length.
MIN_RARITY = {}
for vocab_word in dictionary:
    for position in range( len( vocab_word ) ):
        lookup_key = ( len( vocab_word ), position, vocab_word[ position ] )
        if lookup_key not in MIN_RARITY or dictionary[ vocab_word ] < MIN_RARITY[ lookup_key ]:
            MIN_RARITY[ lookup_key ] = dictionary[ vocab_word ]


def check_word( vocab_word ):
    """Reject inputs that are not legal lowercase three- or four-letter words."""
    if not isinstance( vocab_word, str ):
        raise ValueError( 'Words must be strings.' )
    if len( vocab_word ) not in ( 3, 4 ):
        raise ValueError( 'Words must contain three or four letters.' )
    for character in vocab_word:
        if character not in 'abcdefghijklmnopqrstuvwxyz':
            raise ValueError( 'Words must contain only lowercase letters.' )
    if vocab_word not in dictionary:
        raise ValueError( 'Word is not in the supplied dictionary.' )


class DC( search.Problem ):
    """A word-changing problem using steps, Scrabble, or frequency costs."""

    def __init__( self, initial = 'dog', goal = 'cat', cost = 'steps' ):
        check_word( initial )
        check_word( goal )
        if len( initial ) != len( goal ):
            raise ValueError( 'Initial and goal words must have the same length.' )
        if cost not in ( 'steps', 'scrabble', 'frequency' ):
            raise ValueError( 'Cost must be steps, scrabble, or frequency.' )

        super( ).__init__( initial, goal )
        self.cost = cost

    def actions( self, state ):
        """Return legal actions as (position, replacement letter) pairs."""
        available_moves = [ ]
        characters = list( state )

        for position in range( len( characters ) ):
            previous_character = characters[ position ]
            for new_character in 'abcdefghijklmnopqrstuvwxyz':
                if new_character == previous_character:
                    continue
                characters[ position ] = new_character
                next_word = ''.join( characters )
                if next_word in dictionary:
                    available_moves.append( ( position, new_character ) )
            characters[ position ] = previous_character

        return available_moves

    def result( self, state, action ):
        """Apply one legal replacement."""
        position, new_character = action
        characters = list( state )
        characters[ position ] = new_character
        return ''.join( characters )

    def goal_test( self, state ):
        return state == self.goal

    def path_cost( self, c, state1, action, state2 ):
        """Add the cost of this move to the cost already accumulated."""
        if self.cost == 'frequency':
            return c + 1 + dictionary[ state2 ]

        step_price = 1
        if self.cost == 'scrabble':
            position, new_character = action
            step_price = SCRABBLE[ new_character ]
        return c + step_price

    def h( self, node ):
        """Add the unavoidable cost of correcting each wrong position."""
        remaining_cost = 0
        for position in range( len( self.goal ) ):
            goal_character = self.goal[ position ]
            if node.state[ position ] == goal_character:
                continue

            if self.cost == 'steps':
                remaining_cost += 1
            elif self.cost == 'scrabble':
                remaining_cost += SCRABBLE[ goal_character ]
            else:
                lookup_key = ( len( self.goal ), position, goal_character )
                remaining_cost += 1 + MIN_RARITY[ lookup_key ]

        return remaining_cost

    def __repr__( self ):
        return 'dc({},{},{})'.format( self.initial, self.goal, self.cost )
